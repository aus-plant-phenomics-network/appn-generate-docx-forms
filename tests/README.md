##  Build the container
```bash
docker build -t generate-docx-form .
```

N.B. There is a GitHub Action as part of this repository that can be manually triggered to build and save the docker image to GitHub Container Registry (ghcr.io)

##  To generate a docx file from a yaml template:

```bash
cd ../tests

docker run --rm -v "$PWD:/work" generate-docx-form  --spec /work/demo_fields.yaml  --out /work/demo_fields.docx
```

###  Post form generation

Use the form and fill in the fields. Then the entered user data can be extracted as a JSON list, also using the docker image built above:
```bash
#  Extract data from docx form:
docker run --rm -v "$PWD:/work" generate-docx-form  --extract /work/demo_fields_filled.docx  --json /work/demo_fields_filled.json
```
