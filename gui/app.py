import marimo

__generated_with = "0.19.7"
app = marimo.App(width="full")


@app.cell
def _():
    import os
    import re
    from pathlib import Path

    import httpx
    import marimo as mo
    return Path, httpx, mo, os, re


@app.cell
def _(mo):
    mo.md("""
    # YAML to DOCX
    Drop a UTF-8 YAML file into the upload area, edit it, choose an output filename, and convert it.
    """)
    return


@app.cell
def _(mo):
    yaml_upload = mo.ui.file(
        filetypes=[".yaml", ".yml", "text/yaml", "application/yaml"],
        kind="area",
        multiple=False,
        label="Drop a YAML file here or click to browse",
    )
    yaml_upload
    return (yaml_upload,)


@app.cell
def _(yaml_upload):
    if yaml_upload.value:
        uploaded = yaml_upload.value[0]
        try:
            initial_yaml = uploaded.contents.decode("utf-8")
            upload_error = ""
        except UnicodeDecodeError:
            initial_yaml = ""
            upload_error = "The selected file is not valid UTF-8."
    else:
        initial_yaml = "# Drop a YAML file above, or start typing here.\n"
        upload_error = ""
    return initial_yaml, upload_error


@app.cell
def _(initial_yaml, mo):
    yaml_editor = mo.ui.code_editor(
        value=initial_yaml,
        language="yaml",
        label="YAML content",
        min_height=460,
        show_copy_button=True,
        debounce=300,
    )
    yaml_editor
    return (yaml_editor,)


@app.cell
def _(mo):
    output_filename_docx = mo.ui.text(
        value="output.docx",
        label="Output Filename:",
        placeholder="output.docx",
        full_width=True,
    )
    convert_button = mo.ui.run_button(label="Convert and download DOCX", kind="success")
    mo.vstack([output_filename_docx, convert_button])
    return convert_button, output_filename_docx


@app.cell
def _(convert_button, httpx, mo, os, output_filename_docx, re, upload_error, yaml_editor):
    mo.stop(not convert_button.value, mo.callout("Ready to convert.", kind="info"))
    mo.stop(bool(upload_error), mo.callout(upload_error, kind="danger"))
    mo.stop(not yaml_editor.value.strip(), mo.callout("The YAML content is empty.", kind="danger"))

    raw_name = output_filename_docx.value.strip() or "output.docx"
    stem = re.sub(r"(?i)\.(docx|ya?ml)$", "", raw_name)
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem).strip(" ._-") or "output"
    download_name = f"{stem}.docx"
    api_base = os.getenv("YAMLTODOCX_API_BASE", "http://127.0.0.1:8000").rstrip("/")

    try:
        response = httpx.post(
            f"{api_base}/yamltodocx",
            data={"output_filename_docx": raw_name},
            files={"yaml_file": (f"{stem}.yaml", yaml_editor.value.encode("utf-8"), "application/yaml")},
            timeout=150.0,
        )
        response.raise_for_status()
        result = mo.vstack([
            mo.callout("Conversion completed successfully.", kind="success"),
            mo.download(data=response.content, filename=download_name, label=f"Download {download_name}"),
        ])
    except httpx.HTTPStatusError as exc:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except Exception:
            detail = exc.response.text
        result = mo.callout(f"Conversion failed: {detail}", kind="danger")
    except httpx.HTTPError as exc:
        result = mo.callout(f"Could not contact the conversion endpoint: {exc}", kind="danger")
    result
    return


if __name__ == "__main__":
    app.run()
