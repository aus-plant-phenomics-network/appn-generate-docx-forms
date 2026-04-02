Below is a **ready-to-use YAML field list** for an **APPN / schema.org–aligned `Person` form**, designed to work cleanly with:

*   online forms
*   DOCX content controls
*   YAML ? JSON-LD transformers
*   RO-Crate and APPN graphs

It uses **stable semantic field keys** (derived directly from schema.org paths), with optional UI metadata.

***

## Minimal YAML field list (keys only)

This is the simplest, tool-friendly version.

```yaml
# Person identity
orcid
honorificPrefix
givenName
additionalName
familyName
name

# Contact details
email
telephone

# Role
jobTitle

# Postal address
address.streetAddress
address.addressLocality
address.addressRegion
address.postalCode
address.addressCountry

# Physical / work address
workLocation.address.streetAddress
workLocation.address.addressLocality
workLocation.address.addressRegion
workLocation.address.postalCode
workLocation.address.addressCountry
```

 Stable  
 Schema-derived  
 APPN-aligned

***

## Rich YAML field list (recommended for form generation)

This version includes labels, help text, and basic typing while **keeping field names semantically clean**.

```yaml
person:
  fields:
    - name: orcid
      label: ORCID iD
      type: string
      help: "Enter your ORCID iD (e.g. 0000-0002-1825-0097)"
      required: true

    - name: honorificPrefix
      label: Title
      type: string
      examples: [Dr, Prof, Mr, Ms]

    - name: givenName
      label: First name
      type: string
      required: true

    - name: additionalName
      label: Middle name
      type: string

    - name: familyName
      label: Family name
      type: string
      required: true

    - name: name
      label: Full display name
      type: string
      help: "e.g. Dr Joshua Charles Bowden"

    - name: email
      label: Email address
      type: string
      format: email
      required: true

    - name: telephone
      label: Telephone
      type: string

    - name: jobTitle
      label: Job title
      type: string

  postalAddress:
    - name: address.streetAddress
      label: Postal street / PO Box
      type: string

    - name: address.addressLocality
      label: City / locality
      type: string

    - name: address.addressRegion
      label: State / region
      type: string

    - name: address.postalCode
      label: Postcode
      type: string

    - name: address.addressCountry
      label: Country
      type: string
      default: AU

  workAddress:
    - name: workLocation.address.streetAddress
      label: Work street address
      type: string

    - name: workLocation.address.addressLocality
      label: Work city / locality
      type: string

    - name: workLocation.address.addressRegion
      label: Work state / region
      type: string

    - name: workLocation.address.postalCode
      label: Work postcode
      type: string

    - name: workLocation.address.addressCountry
      label: Work country
      type: string
      default: AU
```

***

## How this maps to JSON-LD (important)

### Example transformation logic (conceptual)

```text
orcid ? @id = "https://orcid.org/{orcid}"
address.* ? schema:address ? PostalAddress
workLocation.address.* ? schema:workLocation ? Place ? PostalAddress
```

 **Forms stay flat**  
 **Semantics are reconstructed downstream**

***

## Naming rules you can document for APPN

1.  **Form field name = schema.org property path**
2.  **Dot notation = RDF object nesting**
3.  **No APPN-specific prefixes in UI fields**
4.  **Identifiers (e.g. ORCID) are resolved in transformers, not forms**

***
Below is a **DOCX mapping template** that is **directly usable with your existing APPN DOCX ? YAML ? JSON-LD tooling** (including `appn-generate-docx-forms` and docx4j-based pipelines).

I’ll give you:

1.  **The design rules (very important)**
2.  **A concrete DOCX table template** (what goes in Word)
3.  **Content control / field naming conventions**
4.  **The exact JSON/YAML mapping this enables**
5.  **Notes for supervisors + students**

This is written so you can hand it directly to someone building the DOCX.

***

## 1. DOCX mapping design rules (canonical)

### ? Rule 1 — One content control = one field

Each DOCX input cell contains **exactly one bound content control**.

### ? Rule 2 — Content control *Tag* = field name

Use the **semantic field name** (not the label) as the **Tag** (and preferably also the Title).

Example:

    Tag: supervisor.orcid
    Title: supervisor.orcid

### ? Rule 3 — Role prefix first

Roles (supervisor, student) **prefix the field name**, never suffix.

 `supervisor.givenName`  
 `givenName.supervisor`

***

## 2. DOCX table template (what the Word document contains)

### Section heading

> **Supervisor Details**

Then insert a **2-column table**:

| Label | Input (content control) |
| ----- | ----------------------- |

***

### Supervisor table (DOCX layout)

**Row 1**

*   Label cell text: `ORCID iD`
*   Input cell: Plain text content control
    *   **Tag**: `supervisor.orcid`

**Row 2**

*   Label cell text: `Title`
*   Input cell:
    *   Tag: `supervisor.honorificPrefix`

**Row 3**

*   Label cell text: `First name`
*   Input cell:
    *   Tag: `supervisor.givenName`

**Row 4**

*   Label cell text: `Middle name`
*   Input cell:
    *   Tag: `supervisor.additionalName`

**Row 5**

*   Label cell text: `Family name`
*   Input cell:
    *   Tag: `supervisor.familyName`

**Row 6**

*   Label cell text: `Email address`
*   Input cell:
    *   Tag: `supervisor.email`

**Row 7**

*   Label cell text: `Job title`
*   Input cell:
    *   Tag: `supervisor.jobTitle`

***

### Student table (second section)

> **Student Details**

Exact same structure, but tags use `student.`

| Label                | Tag                      |
| -------------------- | ------------------------ |
| ORCID iD             | `student.orcid`          |
| First name           | `student.givenName`      |
| Middle name          | `student.additionalName` |
| Family name          | `student.familyName`     |
| Email address        | `student.email`          |
| Job title / position | `student.jobTitle`       |

***

## 3. Address blocks (optional but APPN-clean)

### Postal address section

> **Postal Address**

| Label           | Content control tag                  |
| --------------- | ------------------------------------ |
| Street / PO Box | `supervisor.address.streetAddress`   |
| City / locality | `supervisor.address.addressLocality` |
| State / region  | `supervisor.address.addressRegion`   |
| Postcode        | `supervisor.address.postalCode`      |
| Country         | `supervisor.address.addressCountry`  |

Repeat (if needed) for student.

***

## 4. What your extraction script will see

From DOCX ? JSON (example output):

```json
{
  "supervisor.orcid": "0000-0001-AAAA-BBBB",
  "supervisor.givenName": "Alice",
  "supervisor.familyName": "Smith",
  "supervisor.email": "alice.smith@uni.edu",

  "student.orcid": "0000-0002-CCCC-DDDD",
  "student.givenName": "Bob",
  "student.familyName": "Jones",
  "student.email": "bob.jones@uni.edu"
}
```

 Flat  
 Deterministic  
 Order-independent

***

## 5. Deterministic transformation ? JSON-LD (APPN-aligned)

### Transformation rule (conceptual)

```text
group by role prefix
 create one schema:Person per role
 if *.orcid present: set @id to https://orcid.org/{orcid}
```

### Resulting JSON-LD snippet

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://orcid.org/0000-0001-AAAA-BBBB",
      "givenName": "Alice",
      "familyName": "Smith",
      "email": "mailto:alice.smith@uni.edu",
      "jobTitle": "Supervisor"
    },
    {
      "@type": "Person",
      "@id": "https://orcid.org/0000-0002-CCCC-DDDD",
      "givenName": "Bob",
      "familyName": "Jones",
      "email": "mailto:bob.jones@uni.edu",
      "jobTitle": "PhD Student"
    }
  ]
}
```

APPN alignment is preserved because:

*   `Person` remains schema.org
*   Roles are contextual, not embedded
*   ORCID remains the canonical identifier

***

## 6. Repeatable people (advanced DOCX pattern)

If you later need **multiple supervisors**, use **indexed prefixes**:

```text
supervisors[0].orcid
supervisors[0].givenName

supervisors[1].orcid
supervisors[1].givenName
```

This is already compatible with YAML lists and JSON arrays.

***

## 7. One-page instruction you can put at the top of the DOCX

You may literally paste this into the document:

> **Instructions**
>
> Please complete the fields below.  
> Do not change field structure or formatting.  
> ORCID iDs should be entered without the URL (e.g. `0000-0002-1825-0097`).

***

## 8. Why this template works so well for APPN

 No APPN-specific UI coupling  
 Stable across schema evolution  
 Works with DOCX, web forms, Smartsheet  
 Directly validates against schema.org  
 Ideal for RO-Crate generation

***

If you want, I can next:

*   Generate an **actual `.docx` file skeleton**
*   Produce a **YAML ? DOCX auto-generator**
*   Define the **exact Python transform function**
*   Add **SHACL validation derived from DOCX**

Just tell me what the next artefact should be.

