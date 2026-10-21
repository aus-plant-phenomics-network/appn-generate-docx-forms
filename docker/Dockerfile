#
#  Build the container
#    docker build -t generate-docx-form .
#
#  To access the container (if needed): 
#    docker run --rm -it --entrypoint /bin/bash generate-docx-form
#
#  To generate a docx file from the yaml template:
# 
# docker run --rm -v "$PWD:/work" generate-docx-form  --spec /work/study_form.yaml  --out /work/STUDY_Form.docx
#
#
#  Use the form and fill in the fields...
#
#  Extract data from docx form:
# docker run --rm --user "$(id -u):$(id -g)" --workdir /work -v "$PWD:/work" generate-docx-form  --extract /work/STUDY_Form.docx  --json /work/study_form_fields.json
#
# We can use the script directly (requires lxml installed). 
# The following outputs to stdout:
#    python extract_form_fields.py ./STUDY_Form.doc
#
# Multi-stage build for generate-docx-form
#

# ---------- build stage ----------
FROM maven:3.9.9-eclipse-temurin-17 AS build

WORKDIR /build

COPY pom.xml .
RUN mvn -q -B dependency:go-offline

COPY src ./src
RUN mvn -q -DskipTests package


# ---------- runtime stage ----------
FROM eclipse-temurin:17-jre-jammy

# Install LibreOffice + Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Optional: install Python deps if needed
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt


RUN mkdir -p /opt/logos
COPY  \
    logo/*.png \
    /opt/logo/


WORKDIR /app

# Java app
COPY --from=build /build/target/generate-docx-form-shaded.jar \
     /app/generate-docx-form.jar

# Python extractor
COPY extract_form_fields.py /app/extract_form_fields.py
RUN chmod +x /app/extract_form_fields.py

# Unified entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Non-root user
RUN useradd -m appuser
USER appuser


ENTRYPOINT ["/app/entrypoint.sh"]