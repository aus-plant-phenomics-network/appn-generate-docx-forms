## Java based docx form creation

This directory enables the creation of a docker image that has a compiled version of the form creation code.


##  Build the container
```bash
docker build -t generate-docx-form .
```

###  To access the container (if needed): 
```bash
 docker run --rm -it --entrypoint /bin/bash generate-docx-form
```

##  To generate a docx file from a yaml template:

```bash
cd ../tests

docker run --rm -v "$PWD:/work" generate-docx-form  --spec /work/demo_fields.yaml  --out /work/Demo_Form.docx
```

###  Post form generation

Use the form and fill in the fields. Then the entered user data can be extracted as a JSON list, also using the docker image built above:
```bash
#  Extract data from docx form:
docker run --rm -v "$PWD:/work" generate-docx-form  --extract /work/Demo_Form.docx  --json /work/demo_form_fields.json
```

#### We can use the script directly (requires lxml installed). 
```bash
# The following outputs to stdout:
python extract_form_fields.py -f ./Demo_Form.docx

# or by using Docker image:
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD:/work" --workdir /work generate-docx-form  --extract /work/Demo_Form.docx
```


