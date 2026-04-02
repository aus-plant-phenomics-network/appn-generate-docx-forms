Yes — but there’s an important subtlety to be clear about up-front, because it affects how you should **interpret** and **use** `appn:Study`.

***

## Key point (very important)

?? **`appn:Study` does *not* introduce its own bespoke property set**.

In the APPN schema, `appn:Study` is defined as a **semantic profile / specialization of existing schema.org classes**, primarily:

*   `schema:Study`
*   `schema:CreativeWork`
*   and (in practice) often interchangeable with `schema:Dataset` in APPN graphs

That means:

> **The properties of `appn:Study` are inherited schema.org properties, plus contextual APPN expectations — not new `appn:` properties.**

So the correct answer is:

> **`appn:Study` uses schema.org properties; APPN constrains and interprets them rather than redefining them.**

***

## Class position in the APPN schema (conceptual)

In RDF terms, `appn:Study` is roughly:

```turtle
appn:Study rdfs:subClassOf schema:Study .
appn:Study rdfs:subClassOf schema:CreativeWork .
```

(Some uses also align it closely with `schema:Dataset`, depending on whether the study is conceptual or data-backed.)

***

## Core properties of `appn:Study`

Below is the **effective property set** you should treat as valid and expected for an APPN Study.

### Identification & description

| Property             | Meaning                                        |
| -------------------- | ---------------------------------------------- |
| `@id`                | Persistent identifier (URI, DOI, internal IRI) |
| `schema:identifier`  | Secondary IDs (local study ID, grant ID, etc.) |
| `schema:name`        | Study title                                    |
| `schema:description` | Study abstract or summary                      |
| `schema:keywords`    | Controlled or free-text keywords               |

***

### People & roles

| Property                   | Expected values                                  |
| -------------------------- | ------------------------------------------------ |
| `schema:creator`           | Supervisor / lead investigator (`schema:Person`) |
| `schema:contributor`       | Students, collaborators (`schema:Person`)        |
| `schema:accountablePerson` | Responsible person (optional)                    |
| `schema:contactPoint`      | Administrative or scientific contact             |

> ? This aligns exactly with how you model supervisors and students earlier.

***

### Temporal properties

| Property                  | Usage           |
| ------------------------- | --------------- |
| `schema:startDate`        | Study start     |
| `schema:endDate`          | Study end       |
| `schema:temporalCoverage` | Coverage period |

***

### Organisational context

| Property           | Usage                        |
| ------------------ | ---------------------------- |
| `schema:publisher` | Institution owning the study |
| `schema:funder`    | Funding body                 |
| `schema:sponsor`   | Program / initiative         |

***

### Relationships to data, experiments, facilities

| Property          | Meaning                            |
| ----------------- | ---------------------------------- |
| `schema:hasPart`  | Experiments, trials, datasets      |
| `schema:isPartOf` | Program, project, larger study     |
| `schema:about`    | Biological subject, species, trait |
| `schema:location` | Facility, site, field location     |

APPN commonly uses `hasPart` to link:

*   a Study to Experiments
*   a Study to Datasets
*   a Study to Observations

***

### Outputs & results

| Property                 | Usage            |
| ------------------------ | ---------------- |
| `schema:associatedMedia` | Images, videos   |
| `schema:subjectOf`       | Publications     |
| `schema:citation`        | Formal citations |
| `schema:mainEntity`      | Primary dataset  |

***

## Minimal valid APPN Study example

```json
{
  "@context": "https://schema.org",
  "@type": "Study",
  "@id": "https://example.org/study/2024-wheat-trial",

  "name": "Wheat Yield Response to Heat Stress",
  "description": "Controlled environment study examining yield sensitivity to heat.",

  "creator": {
    "@id": "https://orcid.org/0000-0001-AAAA-BBBB",
    "@type": "Person",
    "name": "Dr Alice Smith"
  },

  "contributor": {
    "@id": "https://orcid.org/0000-0002-CCCC-DDDD",
    "@type": "Person",
    "name": "Bob Jones"
  },

  "startDate": "2024-01-15",
  "endDate": "2025-06-30",

  "publisher": {
    "@type": "Organization",
    "name": "Australian Plant Phenomics Network"
  }
}
```

 100% APPN-compatible  
 Schema.org-valid  
 Fits directly into RO-Crate

***

## What APPN does *not* put on `appn:Study`

To avoid common mistakes:

 No `appn:studyLeader`  
 No `appn:supervisor`  
 No custom name/address fields  
 No embedded role semantics

All of that is handled through **schema.org relationships**, exactly as you have already modelled for people.

***

## How this connects to everything you’ve built so far

| Layer       | Your earlier work           | Study alignment                      |
| ----------- | --------------------------- | ------------------------------------ |
| DOCX fields | `supervisor.*`, `student.*` | ? used via `creator` / `contributor` |
| YAML        | Flat, role-scoped           | ? transforms cleanly                 |
| JSON-LD     | `schema:Study`              | ? native                             |
| SHACL       | Contextual role rules       | ? applies cleanly                    |

***

## One-sentence takeaway

> **`appn:Study` doesn’t add properties — it constrains how schema.org properties are used in a phenomics context.**

***



You include an **ROR (Research Organization Registry) ID** in an Organization **using standard schema.org patterns**. APPN expects this and does **not** define anything special for ROR.

Below are the **correct, APPN-aligned ways**, from best ? acceptable ? avoid.

***

## ? Best practice (recommended): use the ROR as the `@id`

RORs are **globally resolvable HTTP URIs**, exactly what RDF wants.

### ? Example (cleanest and preferred)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://ror.org/03yrm5c26",
  "name": "University of Adelaide",
  "url": "https://www.adelaide.edu.au"
}
```

### ? Why this is best

*   One unambiguous identity
*   No duplication
*   Automatically deduplicates orgs across datasets
*   Works with RO-Crate, DataCite, OpenAlex, Crossref, APPN

> **If you remember only one thing: use the ROR as `@id`.**

***

## ? Also recommended: include a structured `identifier` (redundancy)

Some tooling doesn’t reason over `@id`, so adding an explicit identifier helps.

### ? Pattern

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://ror.org/03yrm5c26",

  "name": "University of Adelaide",

  "identifier": {
    "@type": "PropertyValue",
    "propertyID": "ROR",
    "value": "03yrm5c26",
    "url": "https://ror.org/03yrm5c26"
  }
}
```

? This is common in:

*   DataCite JSON
*   RO-Crate practice
*   APPN-adjacent workflows

***

## ? Optional: `sameAs` (harmless, but secondary)

You *may* add `sameAs`, but **don’t rely on it alone**.

```json
"sameAs": [
  "https://ror.org/03yrm5c26",
  "https://en.wikipedia.org/wiki/University_of_Adelaide"
]
```

***

## ? What NOT to do

### ? Don’t invent custom properties

```json
"ror": "03yrm5c26"    // ? not schema.org
```

### ? Don’t use only a string identifier

```json
"identifier": "03yrm5c26"   // ? loses meaning
```

### ? Don’t mint your own Organization IRI when a ROR exists

```json
"@id": "https://example.org/orgs/adelaide-uni"  // ? weaker
```

***

## ? How this fits into APPN usage

### Study publisher

```json
{
  "@type": "Study",
  "publisher": {
    "@id": "https://ror.org/03yrm5c26",
    "@type": "Organization",
    "name": "University of Adelaide"
  }
}
```

### Person affiliation

```json
{
  "@type": "Person",
  "name": "Dr Alice Smith",
  "worksFor": {
    "@id": "https://ror.org/03yrm5c26"
  }
}
```

### Facility owner

```json
{
  "@type": "Place",
  "owner": {
    "@id": "https://ror.org/03yrm5c26"
  }
}
```

The Organization node may be **defined once** and referenced everywhere.

***

## ? DOCX / YAML field design for ROR

### YAML field

```yaml
organization.ror
organization.name
organization.url
```

### DOCX content control tag

    organization.ror

### Transform rule

```text
@id = "https://ror.org/" + organization.ror
```

***

## ? SHACL constraint (optional but recommended)

```turtle
sh:property [
  sh:path sh:self ;
  sh:pattern "^https://ror.org/0[a-z0-9]{8}$" ;
  sh:message "Organization must be identified by a valid ROR IRI." ;
] .
```

***

## ? Summary (single glance)

| Task                  | Correct way                           |
| --------------------- | ------------------------------------- |
| Identify Organization | `@id = https://ror.org/...` ?         |
| Extra safety          | `schema:identifier ? PropertyValue` ? |
| APPN schema           | No custom class needed ?              |
| Form capture          | Store ROR suffix ?                    |
| Output graph          | Use full ROR URI ?                    |

***

## Final takeaway

> **In APPN, an Organization with a ROR should be identifiable by that ROR URI — not wrapped, not renamed, not duplicated.**

Great question — Word actually supports **exactly this pattern** natively, and it’s the **right solution** for your DOCX ? metadata pipeline.

***

# ? Use a **Dropdown List Content Control** (combo box)

In Microsoft Word, the control you want is:

> **Dropdown List Content Control**  
> *(aka “Combo box” content control)*

This control allows **each list item to have**:

*   a **display label** (what the user sees)
*   a **stored value** (what your extractor reads)

You show only `AU` to the user, but the underlying value can be the full ROR URL.

***

## ? What this gives you

| Requirement                 | Supported |
| --------------------------- | --------- |
| Show short code (e.g. AU)   | ?         |
| Store full ROR URL          | ?         |
| No macros required          | ?         |
| Works with docx4j / OpenXML | ?         |
| Clean YAML/JSON extraction  | ?         |

This is the **canonical solution** for controlled vocabularies in DOCX forms.

***

# 1. How to create the control in Word (step-by-step)

1.  Enable **Developer** tab
2.  Insert ? **Dropdown List Content Control**
3.  Select the control ? **Properties**
4.  Add list items using **Add…**

### Example list entries

| Display name (Label) | Value (Stored)              |
| -------------------- | --------------------------- |
| AU                   | `https://ror.org/03yrm5c26` |
| CSIRO                | `https://ror.org/03qn8fb07` |
| UQ                   | `https://ror.org/03qn6r687` |

? The user sees only **AU**, **CSIRO**, **UQ**  
? Your extractor receives the **value** field

***

## ? Content control metadata (important)

Set these **exactly**:

    Title: organization.ror
    Tag:   organization.ror

Your pipeline should **ignore the displayed text** and **read the value**.

***

# 2. What your extraction code receives

When the user selects **AU**, the Word document stores:

```xml
<w:listItem w:displayText="AU"
            w:value="https://ror.org/03yrm5c26"/>
```

docx4j / OpenXML readers will give you:

```json
{
  "organization.ror": "https://ror.org/03yrm5c26"
}
```

? No mapping step required  
? No post-processing lookup  
? No ambiguity

***

# 3. JSON-LD / APPN transformation (trivial)

From extracted value:

```json
{
  "organization.ror": "https://ror.org/03yrm5c26"
}
```

Generate:

```json
{
  "@type": "Organization",
  "@id": "https://ror.org/03yrm5c26"
}
```

? APPN-correct  
? schema.org-native  
? RO-Crate-ready

***

# 4. YAML equivalent (for parity with web forms)

Your YAML field definition stays simple:

```yaml
organization:
  ror:
    type: dropdown
    label: Organisation
    values:
      AU: https://ror.org/03yrm5c26
      CSIRO: https://ror.org/03qn8fb07
```

DOCX dropdown == YAML dropdown == JSON-LD identity

***

# 5. What **NOT** to do

### ? Plain text field + manual mapping

```text
User types "AU" ? code looks it up
```

More fragile, harder to validate.

### ? Showing full ROR URLs to users

Bad UX, unnecessary.

### ? Using the display text as the identifier

You lose global identity.

***

# 6. When this pattern is especially valuable

This approach is ideal for:

? ROR  
? ORCID prefix authorities  
? Controlled institution lists  
? Facility codes  
? Country ? URI mappings  
? MIAPPE vocabularies

Anywhere you need **human-friendly choice** + **machine-actionable value**.

***

# ? One-sentence canonical answer

> **Use a Word dropdown list content control with label/value pairs, where the visible label is “AU” and the stored value is the ROR URI.**

***


