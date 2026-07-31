# StructuredFieldExtractor

Extracts field-name / field-value pairs from table-based DOCX forms while preserving document structure.

This is a second (or 3rd) version of this exractor - It works on Word documents that contain tables and assumes every pair of cells in a row are the key-value pair of interest, which does not work perfectly in extracting data unless the table is very ordered (not the case in most of APPN documents).

## Requirements

- This version has not been set up with docker (as for the more comprehensive template drive document creaation app with data extraction capabilities)

- Java 17+ (Java 11 should also work)
- Maven 3.9+

in PowerShell:
```
rundll32 sysdm.cpl,EditEnvironmentVariables
```

JAVA_HOME C:\Users\a1106791\tools\jdk-17.0.20+8
MAVEN_HOME C:\Users\a1106791\tools\apache-maven-3.9.16
%JAVA_HOME%\bin
%MAVEN_HOME%\bin


## Maven Dependency

Add the following dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.5</version>
</dependency>
```

## Create pom.xml

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>example</groupId>
    <artifactId>field-extractor</artifactId>
    <version>1.0</version>

    <dependencies>
        <dependency>
            <groupId>org.apache.poi</groupId>
            <artifactId>poi-ooxml</artifactId>
            <version>5.2.5</version>
        </dependency>
    </dependencies>
</project>
```

## Compile

```bash
mvn dependency:copy-dependencies
javac -cp "target/dependency/*" StructuredFieldExtractor.java
```

Linux/macOS:

```bash
java -cp ".:target/dependency/*" StructuredFieldExtractor "1_Booking_Sheet_AU__FIELD EXPERIMENT_2026.docx"
```

Windows:

```cmd
 java -cp ".;target\dependency\*" StructuredFieldExtractor "1_Booking_Sheet_AU__FIELD EXPERIMENT_2026.docx"
```

## Output Format
Some notes are included per-line:

```text
Field[name='Family Name (Lab Leader, Supervisor):', value='Bowden', table=0, row=1, col=0]
Field[name='Given Name:', value='Joshua', table=0, row=1, col=2]
Field[name='Title:', value='Dr', table=0, row=2, col=0]
Field[name='Email address:', value='joshua.bowden@adelaide.edu.au', table=0, row=2, col=2]
Field[name='Phone:', value='', table=0, row=3, col=0]
Field[name='Organisation:', value='APPN', table=0, row=4, col=0]
Field[name='Department:', value='APPN Head Office', table=0, row=5, col=0]
Field[name='Physical Address: Street / Suburb / State / Post Code / Country', value='Waite Campus', table=0, row=6, col=0]
Field[name='Postal Address: PO Box / Suburb / State / Post Code / Country', value='', table=0, row=7, col=0]
Field[name='Alternative Contact Person:', value='', table=0, row=8, col=0]
Field[name='Email address:', value='', table=0, row=9, col=0]
Field[name='Phone:', value='', table=0, row=10, col=0]
Field[name='Mobile:', value='', table=0, row=10, col=2]
Field[name='Source of funding for this project:', value='(e.g. ARC, GRDC)', table=0, row=13, col=0]
Field[name='Please specify percentage of funding source:', value='Research: % 50', table=0, row=14, col=0]
Field[name='Description of grant:', value='SA Dept of Ag. Grant 220033', table=0, row=15, col=0]
Field[name='Collaborators on this project:', value='', table=0, row=16, col=0]
Field[name='AU Customers Only ? Project Code:', value='Bus.Unit', table=0, row=17, col=0]  <----- these are out of step
Field[name='Start date:', value='End date:', table=0, row=25, col=1]   <----- the dates are not accesible
Field[name='Start date:', value='End date:', table=0, row=26, col=1]
Field[name='Start date:', value='End date:', table=0, row=27, col=1]
Field[name='Start date:', value='End date:', table=0, row=28, col=1]
...                                                                    <----- there are fields here missing
Field[name='Family Name', value='Given Name', table=0, row=31, col=0]
Field[name='Given Name', value='Email', table=0, row=31, col=1]
Field[name='Email', value='Phone', table=0, row=31, col=2]
```

Repeated fields are preserved because each occurrence is stored as a separate record with its table, row, and column coordinates.
