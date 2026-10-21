from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
from pathlib import Path

import marimo
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

MAX_YAML_BYTES = 5 * 1024 * 1024
DOCKER_IMAGE = os.getenv("GENERATE_DOCX_IMAGE", "generate-docx-form")
DOCKER_TIMEOUT_SECONDS = int(os.getenv("DOCKER_TIMEOUT_SECONDS", "120"))


def sanitize_stem(value: str) -> str:
    """Return a portable filename stem, regardless of supplied extension."""
    raw = Path(unicodedata.normalize("NFKC", value or "").strip()).name
    lower = raw.lower()
    for suffix in (".docx", ".yaml", ".yml"):
        if lower.endswith(suffix):
            raw = raw[: -len(suffix)]
            break
    raw = re.sub(r"[^A-Za-z0-9._-]+", "_", raw)
    raw = re.sub(r"_+", "_", raw).strip(" ._-")
    if not raw:
        raw = "output"
    return raw[:120]


app = FastAPI(title="YAML to DOCX converter")


@app.post("/yamltodocx", response_class=FileResponse)
async def yaml_to_docx(
    yaml_file: UploadFile = File(...),
    output_filename_docx: str = Form(...),
):
    stem = sanitize_stem(output_filename_docx)
    yaml_bytes = await yaml_file.read(MAX_YAML_BYTES + 1)
    if not yaml_bytes:
        raise HTTPException(status_code=400, detail="The YAML document is empty.")
    if len(yaml_bytes) > MAX_YAML_BYTES:
        raise HTTPException(status_code=413, detail="The YAML document exceeds 5 MiB.")
    try:
        yaml_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="The YAML document must be UTF-8.") from exc

    work_dir = Path(tempfile.mkdtemp(prefix="yamltodocx-"))
    yaml_path = work_dir / f"{stem}.yaml"
    docx_path = work_dir / f"{stem}.docx"
    yaml_path.write_bytes(yaml_bytes)

    cmd = [
        "docker", "run", "--rm",
        "-u", f"{os.getuid()}:{os.getgid()}",
        "-v", f"{work_dir}:/work",
        DOCKER_IMAGE,
        "--spec", f"/work/{stem}.yaml",
        "--out", f"/work/{stem}.docx",
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=DOCKER_TIMEOUT_SECONDS, check=False,
        )
    except FileNotFoundError as exc:
        shutil.rmtree(work_dir, ignore_errors=True)
        raise HTTPException(status_code=503, detail="Docker is not installed or not on PATH.") from exc
    except subprocess.TimeoutExpired as exc:
        shutil.rmtree(work_dir, ignore_errors=True)
        raise HTTPException(status_code=504, detail="DOCX conversion timed out.") from exc

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "Converter failed.").strip()[-4000:]
        shutil.rmtree(work_dir, ignore_errors=True)
        raise HTTPException(status_code=422, detail=detail)
    if not docx_path.is_file():
        shutil.rmtree(work_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail="Converter did not create the DOCX file.")

    return FileResponse(
        docx_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"{stem}.docx",
        background=BackgroundTask(shutil.rmtree, work_dir, ignore_errors=True),
    )


# Register API routes before the catch-all marimo mount.
marimo_server = marimo.create_asgi_app().with_app(path="", root="app.py")
app.mount("/", marimo_server.build())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
