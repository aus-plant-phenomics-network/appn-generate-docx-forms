## Automated Booking Forms with postprocessing data access

This project alows a user to define a simple form based data entry table in the common MS docx format.

It requires the user to define the fields in a YAML file that defines 'sections' and 'fields' and the software reads the template and produces a docx file that has the defined fields populated.

Example fields available in the YAML template are as follows:

```yaml
# These are a bunch of header and title test values and a logo image
formName: STUDY
title: "STUDY Form"
header_image: "/work/logo/APPN_logo_120x120.png"
header_text: "APPN Resource Booking - Data Team Demo"
section_count: "1" # used to remove extra line added to the table
# Page note to display under the table:
note: "Tip: Turn on 'Restrict Editing' → 'Filling in forms' in Word to reduce accidental edits."

# These are the rows that will be added to the DOCX table.
# There are two types of rows 
#  1. A 'section' which is a single line denoting a section.
#  2. A 'field' type, that alows entry of text, richtext, checkbox, dropdown lists.
rows:
  - type: section
    text: "Study Description"
    background: "#E2EFDA"

  - type: field
    name: studyId
    control: text
    alias: "Study Name"
    
  - type: field
    name: culturalPractice
    control: checkboxList
    items: ["irrigated", "rainfed", "fertigation", "no-till"]
    
  - type: field
    name: experementalDesignType
    control: dropdown
    items: ["RCBD", "CRD", "Split-plot", "Alpha lattice"]

  - type: field
    name: growthFacilityDesc
    control: richtext
```


Once the rows have been defined in the yaml file it is then ready to create the docx document.

## Software requirements
The software is Java 11 based and can be built in a Docker container to reduce the need to install the required Java version and development libraries. Once the library is built the contents of documents produced are controlled through setting values in the YAML file used as an argument to the program.


### 1. Build the container
```bash
cd docker
docker build -t generate-docx-form .
```
or, retrieve it from github container registry:

```bash
docker pull ghcr.io/aus-plant-phenomics-network/appn-generate-docx-forms:latest

docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "$PWD:/work" \
  ghcr.io/aus-plant-phenomics-network/appn-generate-docx-forms \
  --extract /work/booking_form.docx
```

To access the container (if needed): 
```bash
docker run --rm -it --entrypoint /bin/bash generate-docx-form
```

### 2. Generate a docx file from the yaml template:
```bash
docker run -d  -u $(id -u):$(id -g) -v "$PWD:/work" generate-docx-form  --spec /work/booking_form.yaml --out /work/booking_form.docx
```

If docx file is not produced, check the logs
```bash
#    docker logs formgen
```

Now you can use the file `STUDY_Form.docx`  and fill in the fields with project details...

### 3  Extract data from docx form
The script provided outputs a JSON list of dictionaries that extracts the field alias, tag, type, and value that a user has entered into the form:

```bash

python extract_form_fields.py -f ./booking_form_filled.doc

# or via Docker
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD:/work" --workdir /work generate-docx-form  --extract /work/booking_form_filled.docx
```
e.g.

```json

...

```



