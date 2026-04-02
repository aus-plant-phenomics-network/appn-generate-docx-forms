Below is a **clear, APPN-aligned SHACL shape set** that validates the **Person data produced from your DOCX / YAML pipeline**, including:

*   ORCID-identified people
*   required name fields
*   email format
*   optional addresses
*   role-scoped persons (supervisor, student handled upstream)

This SHACL is written in **Turtle (`.ttl`)**, which fits naturally with the existing `appn-schema.ttl`.

***

# 1. Design intent (what this validates)

These shapes are designed to validate the **output graph**, not the raw DOCX fields.

They ensure:

 Each `schema:Person`  
 Has an ORCID IRI  
 Has basic naming fields  
 Uses schema.org properties correctly  
 Can be reused in APPN, RO-Crate, and facility graphs

Roles (supervisor/student) are **validated structurally elsewhere** (e.g. Dataset, Project, Facility shapes).

***

# 2. Prefixes

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix schema: <https://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix appn: <https://w3id.org/appn/> .
```

***

# 3. Person Shape (core)

This is the **central SHACL shape** for APPN persons.

```turtle
appn:PersonShape
  a sh:NodeShape ;
  sh:targetClass schema:Person ;

  sh:description "APPN-aligned validation rules for schema:Person with ORCID identity." ;

  # ORCID identity
  sh:property [
    sh:path sh:self ;
    sh:nodeKind sh:IRI ;
    sh:pattern "^https://orcid.org/[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9X]{4}$" ;
    sh:message "Person must be identified by a valid ORCID IRI." ;
  ] ;

  # Given name
  sh:property [
    sh:path schema:givenName ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:message "Person must have a givenName." ;
  ] ;

  # Family name
  sh:property [
    sh:path schema:familyName ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:message "Person must have a familyName." ;
  ] ;

  # Display name (recommended)
  sh:property [
    sh:path schema:name ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:message "Person should have a full display name (schema:name)." ;
    sh:severity sh:Warning ;
  ] ;

  # Email
  sh:property [
    sh:path schema:email ;
    sh:datatype xsd:string ;
    sh:pattern "^mailto:.+@.+\\..+$" ;
    sh:message "Email must be a valid mailto: URI." ;
  ] ;

  # Optional job title
  sh:property [
    sh:path schema:jobTitle ;
    sh:datatype xsd:string ;
  ] ;

  # Postal address (optional)
  sh:property [
    sh:path schema:address ;
    sh:class schema:PostalAddress ;
  ] .
```

***

# 4. PostalAddress Shape

Used for both **postal** and **work** addresses.

```turtle
appn:PostalAddressShape
  a sh:NodeShape ;
  sh:targetClass schema:PostalAddress ;

  sh:property [
    sh:path schema:streetAddress ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:message "PostalAddress must include streetAddress or PO Box." ;
  ] ;

  sh:property [
    sh:path schema:addressLocality ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:message "PostalAddress must include addressLocality (city)." ;
  ] ;

  sh:property [
    sh:path schema:addressRegion ;
    sh:datatype xsd:string ;
  ] ;

  sh:property [
    sh:path schema:postalCode ;
    sh:datatype xsd:string ;
  ] ;

  sh:property [
    sh:path schema:addressCountry ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
  ] .
```

***

# 5. Work Location (Place) Shape

Used when your form collects **physical / work addresses**.

```turtle
appn:WorkLocationShape
  a sh:NodeShape ;
  sh:targetClass schema:Place ;

  sh:property [
    sh:path schema:address ;
    sh:class schema:PostalAddress ;
    sh:minCount 1 ;
    sh:message "Work location must have a PostalAddress." ;
  ] .
```

***

# 6. Optional: Role-based constraints (Dataset / Project context)

Roles are validated **at the relationship level**, not on `Person`.

Example (for a Dataset):

```turtle
appn:DatasetSupervisorShape
  a sh:NodeShape ;
  sh:targetClass schema:Dataset ;

  sh:property [
    sh:path schema:creator ;
    sh:class schema:Person ;
    sh:minCount 1 ;
    sh:message "Dataset must have at least one supervisor (creator)." ;
  ] .
```

And for students:

```turtle
appn:DatasetStudentShape
  a sh:NodeShape ;
  sh:targetClass schema:Dataset ;

  sh:property [
    sh:path schema:contributor ;
    sh:class schema:Person ;
  ] .
```

 Same `Person` shape reused  
 Roles emerge from context  
 Perfect APPN alignment

***

# 7. How this connects to your DOCX fields

| DOCX field             | JSON-LD                | SHACL validated |
| ---------------------- | ---------------------- | --------------- |
| `supervisor.orcid`     | `@id`                  | ? ORCID IRI     |
| `supervisor.givenName` | `schema:givenName`     | ? required      |
| `student.familyName`   | `schema:familyName`    | ? required      |
| `*.email`              | `schema:email`         | ? mailto format |
| `*.address.*`          | `schema:PostalAddress` | ? structure     |

***

# 8. Validation lifecycle (recommended)

```text
DOCX
 ? flat JSON
 ? JSON-LD graph
 ? SHACL validation
 ? accept / reject / warn
```

Warnings (e.g. missing `schema:name`) ?  
Errors (e.g. missing ORCID) ?

***

# 9. Why this SHACL is APPN-correct

 Uses `schema:Person`, not a local clone  
 Treats ORCID as identity, not a property  
 Separates people from roles  
 Mirrors APPN modelling philosophy  
 Reusable across facilities, datasets, bookings

***


Below is a **direct, mechanical derivation of SHACL shapes from the YAML field lists you’ve been using**, following these rules:

1.  **Each YAML field ? one `sh:property`**
2.  **Dot-notation ? RDF path nesting**
3.  **Role prefixes (supervisor/student) are *not* in SHACL**  
    ? SHACL validates the **output Persons**, not the form roles
4.  **Cardinality + datatype come from YAML intent**
5.  **ORCID ? node IRI constraint**

This is exactly how you keep **DOCX ? YAML ? JSON-LD ? SHACL** in lock-step.

***

## 1. Input YAML (baseline)

This is the mental input we’re compiling from (you don’t need to repeat it in code):

```yaml
orcid
honorificPrefix
givenName
additionalName
familyName
name
email
telephone
jobTitle

address.streetAddress
address.addressLocality
address.addressRegion
address.postalCode
address.addressCountry

workLocation.address.streetAddress
workLocation.address.addressLocality
workLocation.address.addressRegion
workLocation.address.postalCode
workLocation.address.addressCountry
```

***

## 2. Namespace prefixes

```turtle
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix schema: <https://schema.org/> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix appn:   <https://w3id.org/appn/> .
```

***

## 3. Person Shape (derived from top-level fields)

This shape is **generated entirely from the YAML Person fields**.

```turtle
appn:PersonShape
  a sh:NodeShape ;
  sh:targetClass schema:Person ;
  sh:description "Person shape generated from APPN YAML field list" ;

  ## ORCID (derived from 'orcid')
  sh:property [
    sh:path sh:self ;
    sh:nodeKind sh:IRI ;
    sh:pattern "^https://orcid.org/[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9X]{4}$" ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "Person must be identified by a valid ORCID IRI" ;
  ] ;

  ## honorificPrefix
  sh:property [
    sh:path schema:honorificPrefix ;
    sh:datatype xsd:string ;
    sh:maxCount 1 ;
  ] ;

  ## givenName
  sh:property [
    sh:path schema:givenName ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
  ] ;

  ## additionalName
  sh:property [
    sh:path schema:additionalName ;
    sh:datatype xsd:string ;
  ] ;

  ## familyName
  sh:property [
    sh:path schema:familyName ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
  ] ;

  ## name (display name)
  sh:property [
    sh:path schema:name ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:severity sh:Warning ;
  ] ;

  ## email
  sh:property [
    sh:path schema:email ;
    sh:datatype xsd:string ;
    sh:pattern "^mailto:.+@.+\\..+$" ;
    sh:minCount 1 ;
  ] ;

  ## telephone
  sh:property [
    sh:path schema:telephone ;
    sh:datatype xsd:string ;
  ] ;

  ## jobTitle
  sh:property [
    sh:path schema:jobTitle ;
    sh:datatype xsd:string ;
  ] ;

  ## address (PostalAddress)
  sh:property [
    sh:path schema:address ;
    sh:node appn:PostalAddressShape ;
  ] ;

  ## workLocation
  sh:property [
    sh:path schema:workLocation ;
    sh:node appn:WorkLocationShape ;
  ] .
```

? Every property above comes **directly** from a YAML field  
? No supervisor/student leakage into SHACL  
? APPN- and RO-Crate-compliant

***

## 4. PostalAddress Shape (from `address.*`)

Generated from:

```yaml
address.streetAddress
address.addressLocality
address.addressRegion
address.postalCode
address.addressCountry
```

```turtle
appn:PostalAddressShape
  a sh:NodeShape ;
  sh:targetClass schema:PostalAddress ;

  sh:property [
    sh:path schema:streetAddress ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
  ] ;

  sh:property [
    sh:path schema:addressLocality ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
  ] ;

  sh:property [
    sh:path schema:addressRegion ;
    sh:datatype xsd:string ;
  ] ;

  sh:property [
    sh:path schema:postalCode ;
    sh:datatype xsd:string ;
  ] ;

  sh:property [
    sh:path schema:addressCountry ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
  ] .
```

***

## 5. WorkLocation Shape (from `workLocation.address.*`)

YAML path:

```yaml
workLocation.address.streetAddress
...
```

Generates **two levels**:

*   `schema:Place`
*   nested `schema:PostalAddress`

```turtle
appn:WorkLocationShape
  a sh:NodeShape ;
  sh:targetClass schema:Place ;

  sh:property [
    sh:path schema:address ;
    sh:node appn:PostalAddressShape ;
    sh:minCount 1 ;
  ] .
```

***

## 6. How role-scoped YAML fields disappear correctly

### Form fields

```text
supervisor.givenName
student.givenName
```

### JSON-LD output

```json
{
  "@type": "Person",
  "givenName": "Alice"
}
```

### SHACL validation

? Validated once by `appn:PersonShape`  
? Role handled by the containing object (Dataset, Project, Facility)

This is **exactly** how SHACL should be used.

***

## 7. Deterministic generation rule (you can automate this)

Here is the algorithm you are effectively using:

```text
For each YAML field:
  split by "."
  last segment ? schema property
  prefix determines nesting
  if top-level ? PersonShape
  if address.* ? PostalAddressShape
  if workLocation.address.* ? Place ? PostalAddress
```

This is why:

*   your DOCX
*   your YAML
*   your JSON-LD
*   your SHACL

stay **strictly aligned**.

***

## 8. Sanity check: what this guarantees

? All Persons have ORCIDs  
? Emails are mailto URIs  
? Names are present  
? Addresses are structurally valid  
? Same SHACL works for supervisor, student, operator, contact

***

If you want next, I can:



