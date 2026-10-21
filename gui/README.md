# Marimo YAML-to-DOCX application

A single-page marimo frontend mounted in FastAPI. The `POST /yamltodocx` endpoint writes the uploaded YAML into an isolated temporary directory, runs `generate-docx-form`, and streams the generated DOCX back to the browser.

## Prerequisites

- Python 3.11+
- Docker Engine, with the current user permitted to run `docker`
- A locally available Docker image named `generate-docx-form`

## Run

Open <http://127.0.0.1:8000/>. API documentation is available at <http://127.0.0.1:8000/docs>.

To use another converter image or timeout:

```bash
GENERATE_DOCX_IMAGE=my-image:tag DOCKER_TIMEOUT_SECONDS=180 python backend.py
```

## Request contract

```bash
curl -X POST http://127.0.0.1:8000/yamltodocx \
  -F 'output_filename_docx=my-form.docx' \
  -F 'yaml_file=@my-form.yaml;type=application/yaml' \
  --output my-form.docx
```

Both supplied `.yaml`/`.yml`/`.docx` extensions are removed before the server creates canonical `<stem>.yaml` and `<stem>.docx` names. Unsafe characters are replaced, path components are discarded, uploads are limited to 5 MiB, and each conversion receives a separate temporary working directory.

## Deployment note

Run this FastAPI process on a trusted Docker host. Exposing the Docker socket to a container is highly privileged and is not recommended for an internet-facing service. Add authentication, request-rate limits, and an allow-listed converter image (see below) before exposing the endpoint beyond a trusted network.



### Specifiy the build commands using the uv tool-

For this web application, I recommend using uv as a non-packaged application project, with dependencies recorded in pyproject.toml and locked in uv.lock. The uv sync command creates the virtual environment and installs the locked dependencies, while uv run executes the server inside that environment.

Option 1: Convert the downloaded project to uv

Extract the ZIP and enter the directory:

unzip marimo-yamltodocx-fastapi.zip
cd marimo-yamltodocx-fastapi


Initialize it as a non-packaged application:

```bash
uv init --bare
```

Add the required dependencies:


```bash
uv add \
  "fastapi>=0.115,<1" \
  "httpx>=0.27,<1" \
  "marimo>=0.19,<1" \
  "python-multipart>=0.0.9,<1" \
  "uvicorn[standard]>=0.30,<1"
```

This creates or updates:


```bash
pyproject.toml
uv.lock
.venv/
```

uv add records dependencies in pyproject.toml and updates the lockfile. The environment and lockfile are otherwise created automatically by project commands such as uv sync, uv lock, or uv run.

Start the application

Run the existing Python entry point:


```bash
uv run python backend.py
```

Then open:

http://127.0.0.1:8000/


FastAPI API documentation will be available at:

http://127.0.0.1:8000/docs



### Complete clean-build sequence

Starting from the downloaded ZIP, the full sequence is:

```bash
unzip marimo-yamltodocx-fastapi.zip
cd marimo-yamltodocx-fastapi

uv init --bare

uv add \
  "fastapi>=0.115,<1" \
  "httpx>=0.27,<1" \
  "marimo>=0.19,<1" \
  "python-multipart>=0.0.9,<1" \
  "uvicorn[standard]>=0.30,<1"

uv sync
uv run python backend.py
```

You technically do not need both uv add and uv sync during the initial setup because uv add resolves and installs the dependencies. Keeping uv sync in build or deployment instructions is nevertheless useful because it explicitly ensures that .venv matches uv.lock.

Reproducible deployment build

After committing both pyproject.toml and uv.lock, deployment can use:


```bash
uv sync --frozen
uv run --frozen python backend.py
```

The --frozen option means the deployment uses the existing lockfile without modifying it. This is preferable for repeatable builds.

Run through Uvicorn directly

Instead of executing the if __name__ == "__main__" block, you can invoke Uvicorn directly:


```bash
uv run uvicorn backend:app --host 0.0.0.0 --port 8000
```

For local development with automatic reload:


```bash
uv run uvicorn backend:app  --host 127.0.0.1  --port 8000 --reload
```

Do not use --reload in production.


#### Docker image prerequisite

The Python build does not build the generate-docx-form image. Before starting the web application, confirm that this image exists:


```bash
docker image inspect generate-docx-form
```

If the converter repository contains its Dockerfile, build it separately:


```bash
cd ../docker

docker build \
  --tag generate-docx-form \
  /path/to/appn-generate-docx-forms
```

Then start the web application:


```bash
uv run uvicorn backend:app \
  --host 0.0.0.0 \
  --port 8000
```

#### Useful uv maintenance commands

Update the lockfile within the declared version constraints:


```bash
uv lock --upgrade
```

Synchronize the environment afterward:


```bash
uv sync
```

Inspect installed dependencies:


```bash
uv tree
```

Check the application imports:


```bash
uv run python -m py_compile app.py backend.py
```


The key production commands are therefore:


```bash
uv sync --frozen
uv run --frozen uvicorn backend:app --host 0.0.0.0 --port 8000
```

### For improved docker image security:

An allow-listed converter image is not a particular public image. It is the exact converter image that you have built, reviewed, scanned, approved, and pinned by its immutable SHA-256 digest. For your application, that would be an approved version of generate-docx-form, not a user-supplied image name.

Recommended image reference

Instead of allowing this mutable name:

generate-docx-form


use a fully qualified, versioned, digest-pinned reference:

registry.example.org/appn/generate-docx-form:1.0.0@sha256:<approved-digest>


A digest identifies the exact image contents and cannot silently move to a different build like a tag can. Docker recommends digest references when the exact immutable image must be used.

For an organisation-hosted registry, this might look like:

ghcr.io/aus-plant-phenomics-network/generate-docx-form:1.0.0@sha256:abc123...


or:

your-registry.azurecr.io/appn/generate-docx-form:1.0.0@sha256:abc123...


The digest above is only illustrative. You must obtain the real digest from the image you build and approve.

Build and obtain the digest

Build a versioned image:

```bash
docker build \
  --tag generate-docx-form:1.0.0 \
  /path/to/appn-generate-docx-forms
```

Inspect it:

```bash
docker image inspect \
  generate-docx-form:1.0.0 \
  --format '{{index .RepoDigests 0}}'
```

A locally built image may not have a repository digest until it has been pushed. For a registry-backed image:

```bash
docker tag \
  generate-docx-form:1.0.0 \
  registry.example.org/appn/generate-docx-form:1.0.0

docker push \
  registry.example.org/appn/generate-docx-form:1.0.0
```

Then retrieve the registry digest:

```bash
docker buildx imagetools inspect \
  registry.example.org/appn/generate-docx-form:1.0.0
```

The output will include something like:

Digest: sha256:0123456789abcdef...


The approved reference becomes:

registry.example.org/appn/generate-docx-form:1.0.0@sha256:0123456789abcdef...


Docker documents docker buildx imagetools inspect as a way to view an image digest and supports pulling images by digest.

Enforce the allow-list in the FastAPI code

The important change is to remove the image name from user control. Do not let a form value, query parameter, YAML property, request header, or arbitrary environment variable select the converter image.

Use a fixed constant:

APPROVED_CONVERTER_IMAGE = (
    "registry.example.org/appn/generate-docx-form:1.0.0"
    "@sha256:0123456789abcdef..."
)


Then use only that constant:

cmd = [
    "docker",
    "run",
    "--rm",
    "-u",
    f"{os.getuid()}:{os.getgid()}",
    "-v",
    f"{work_dir}:/work",
    APPROVED_CONVERTER_IMAGE,
    "--spec",
    f"/work/{stem}.yaml",
    "--out",
    f"/work/{stem}.docx",
]


If you need staged upgrades, define a small server-side allow-list:

APPROVED_CONVERTER_IMAGES = {
    "v1": (
        "registry.example.org/appn/generate-docx-form:1.0.0"
        "@sha256:0123456789abcdef..."
    ),
}

CONVERTER_VERSION = "v1"
APPROVED_CONVERTER_IMAGE = APPROVED_CONVERTER_IMAGES[CONVERTER_VERSION]


Only administrators should be able to change CONVERTER_VERSION. The client should not select it.

Prevent automatic pulling

Pre-pull the approved image during deployment:

```bash
docker pull \
  registry.example.org/appn/generate-docx-form:1.0.0@sha256:<approved-digest>
```

Then add this to the runtime command:

--pull never


For example:

cmd = [
    "docker",
    "run",
    "--rm",
    "--pull",
    "never",
    "-u",
    f"{os.getuid()}:{os.getgid()}",
    "-v",
    f"{work_dir}:/work",
    APPROVED_CONVERTER_IMAGE,
    "--spec",
    f"/work/{stem}.yaml",
    "--out",
    f"/work/{stem}.docx",
]


This makes the server fail rather than unexpectedly retrieving an image at request time.

Harden the converter execution

I would also strengthen the generated Docker command as follows:

cmd = [
    "docker",
    "run",
    "--rm",
    "--pull",
    "never",

    "--network",
    "none",

    "--read-only",

    "--cap-drop",
    "ALL",

    "--security-opt",
    "no-new-privileges=true",

    "--pids-limit",
    "128",

    "--memory",
    "512m",

    "--cpus",
    "1.0",

    "--user",
    f"{os.getuid()}:{os.getgid()}",

    "--mount",
    f"type=bind,src={work_dir},dst=/work,rw",

    APPROVED_CONVERTER_IMAGE,

    "--spec",
    f"/work/{stem}.yaml",

    "--out",
    f"/work/{stem}.docx",
]


These controls provide:

--network none: prevents the converter from making network connections.
--read-only: makes the image’s root filesystem read-only.
--cap-drop ALL: removes Linux capabilities that the converter should not need.
--security-opt no-new-privileges=true: prevents processes from gaining additional privileges.
--pids-limit 128: reduces fork-bomb risk.
--memory 512m: limits memory consumption.
--cpus 1.0: limits CPU consumption.
--user UID:GID: runs as a non-root host user.
A single writable /work mount: restricts expected file output to the job directory.

OWASP recommends keeping the container host patched, avoiding exposure of the Docker socket, using an unprivileged user, and limiting capabilities. It warns that access to /var/run/docker.sock is effectively equivalent to highly privileged access to the host.

The converter might need a writable temporary directory internally. If --read-only causes errors, add a restricted temporary filesystem:

"--tmpfs",
"/tmp:rw,noexec,nosuid,nodev,size=64m",

Verify the approved local image

At application startup, you can check that the expected image exists:

def verify_converter_image() -> None:
    result = subprocess.run(
        [
            "docker",
            "image",
            "inspect",
            APPROVED_CONVERTER_IMAGE,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "The approved converter image is not installed: "
            f"{APPROVED_CONVERTER_IMAGE}"
        )


Call this during startup rather than waiting for the first request to fail.

Important architectural limitation

A constant in the FastAPI source is an application-level allow-list, but the service account can still run other images if the application is compromised and that account has unrestricted Docker access.

For stronger enforcement, use one of these architectures:

Run a dedicated conversion worker with permission to execute only the approved converter.
Apply a Docker authorization policy that permits container creation only for the exact digest.
Place the converter behind an internal service so the public-facing FastAPI process has no Docker access.
Use rootless Docker or another isolated runtime on a dedicated conversion host.
Run the job in a container-orchestration environment with admission policies restricting approved registries and digests.

Docker’s hardened isolation configuration demonstrates that image allow-lists can specify image@digest, meaning only an image matching both the repository name and exact digest is allowed. It also cautions that wildcards weaken the control.

Practical recommendation for this project

For your current deployment, I would use:

your-private-registry/appn/generate-docx-form:1.0.0@sha256:<reviewed-digest>


and combine it with:

--pull never
--network none
--read-only
--cap-drop ALL
--security-opt no-new-privileges=true
--pids-limit 128
--memory 512m
--cpus 1.0


This means “allow-listed” is not simply “the image is called generate-docx-form.” It means:

You control or trust the registry.
You reviewed and scanned the image.
The image is pinned to an exact digest.
Users cannot override the selected image.
The host or runtime policy prevents other images from being launched.
The converter runs with limited privileges, resources, mounts, and network access.