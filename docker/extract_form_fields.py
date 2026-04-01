#!/usr/bin/env python3
"""
Extract SDT (content control) values from a DOCX form.

- Prints a list of {alias, tag, type, value}
- Handles text, rich text, date, dropdown/combobox, and Word 2010+ checkbox.

Usage:
  python extract_form_fields.py /path/to/STUDY_Form.docx
"""

import sys
import zipfile
from zipfile import ZipFile
from lxml import etree
import xml.etree.ElementTree as ET
import yaml
from typing import Any, Dict, Optional
from pathlib import Path
import re
import getopt
import json


NS = {
    "w":  "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14":"http://schemas.microsoft.com/office/word/2010/wordml",
}

# Utility: gather all inner text under a node (paragraphs/runs/text)
def _gather_text(node):
    # any <w:t> descendants concatenated with spaces between paragraphs
    texts = []
    for t in node.xpath(".//w:t", namespaces=NS):
        if t.text:
            texts.append(t.text)
    return "".join(texts).strip()

def _get_alias(sdtPr):
    # alias is <w:alias w:val="...">
    alias_el = sdtPr.xpath("./w:alias", namespaces=NS)
    return alias_el[0].get("{%s}val" % NS["w"]) if alias_el else None

def _get_tag(sdtPr):
    # tag is <w:tag w:val="...">
    tag_el = sdtPr.xpath("./w:tag", namespaces=NS)
    return tag_el[0].get("{%s}val" % NS["w"]) if tag_el else None

def _has_child(sdtPr, qname):
    return len(sdtPr.xpath("./" + qname, namespaces=NS)) > 0

def _get_dropdown_items(sdtPr):
    # <w:dropDownList>/<w:comboBox> contain multiple <w:listItem w:displayText, w:value>
    items = []
    for li in sdtPr.xpath(".//w:listItem", namespaces=NS):
        display = li.get("{%s}displayText" % NS["w"])
        value   = li.get("{%s}value"       % NS["w"])
        items.append({"displayText": display, "value": value})
    return items

def _is_checkbox(sdtPr):
    # Word 2010+ checkbox lives in w14 namespace under sdtPr
    return len(sdtPr.xpath("./w14:checkbox", namespaces=NS)) > 0

def _checkbox_checked_from_pr(sdtPr):
    # optional w14:checked/w14:val=1
    chk = sdtPr.xpath("./w14:checkbox/w14:checked", namespaces=NS)
    if chk:
        val = chk[0].get("{%s}val" % NS["w14"])
        if val is not None:
            return val in ("1", "true", "on")
    return None  # unknown

def _checkbox_checked_from_content(sdtContent):
    # We seeded the visual glyph in your generator as ☒ (U+2612) for checked,
    # and ☐ (U+2610) for unchecked. Look for those in visible text.
    text = _gather_text(sdtContent)
    if "☒" in text:
        return True
    if "☐" in text:
        return False
    return None

def extract_fields(docx_path):
    with zipfile.ZipFile(docx_path, "r") as z:
        xml = z.read("word/document.xml")
    root = etree.fromstring(xml)

    results = []

    # Find all SDTs (content controls)
    for sdt in root.xpath(".//w:sdt", namespaces=NS):
        sdtPr      = sdt.find("w:sdtPr", NS)
        sdtContent = sdt.find("w:sdtContent", NS)
        if sdtPr is None or sdtContent is None:
            continue

        alias = _get_alias(sdtPr)
        tag   = _get_tag(sdtPr)

        # Determine the control "type" from markers in <w:sdtPr>
        if _is_checkbox(sdtPr):
            ctype = "checkbox"
            # Prefer explicit w14:checked; fall back to glyph in content
            checked = _checkbox_checked_from_pr(sdtPr)
            if checked is None:
                checked = _checkbox_checked_from_content(sdtContent)
            value = bool(checked) if checked is not None else None

        elif _has_child(sdtPr, "w:dropDownList"):
            ctype = "dropdown"
            # Current displayed value is the visible text inside sdtContent.
            # Items are available in sdtPr if you need them.
            value = _gather_text(sdtContent)
            items = _get_dropdown_items(sdtPr)

        elif _has_child(sdtPr, "w:comboBox"):
            ctype = "combobox"
            value = _gather_text(sdtContent)
            items = _get_dropdown_items(sdtPr)

        elif _has_child(sdtPr, "w:date"):
            ctype = "date"
            value = _gather_text(sdtContent)  # formatted string as seen in the doc

        elif _has_child(sdtPr, "w:text"):
            ctype = "text"
            value = _gather_text(sdtContent)

        else:
            # richText or other SDT flavors — just read visible text
            ctype = "richtext"
            value = _gather_text(sdtContent)

        out = {
            "alias": alias,
            "tag":   tag,
            "type":  ctype,
            "value": value,
        }
        # If you want to include item lists for dropdown/combobox:
        if ctype in ("dropdown", "combobox"):
            out["items"] = _get_dropdown_items(sdtPr)
        results.append(out)

    return results
    
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Optional


def extract_custom_xml_from_docx(
    docx_path: str,
    namespace_uri: str = "https://schema.plantphenomics.org.au/docx-form",
    root_local_name: str = "docxFormSpec",
    return_cdata_only: bool = False
) -> List[str]:
    """
    Extract custom XML parts from a DOCX file.

    Args:
        docx_path: Path to .docx file
        namespace_uri: XML namespace used in your custom XML
        root_local_name: Root element local name (without prefix)
        return_cdata_only: If True, extract only CDATA contents

    Returns:
        List of XML strings (or CDATA strings)
    """

    results = []

    with zipfile.ZipFile(docx_path, "r") as docx:
        custom_xml_parts = [
            name for name in docx.namelist()
            if name.startswith("customXml/") and name.endswith(".xml")
        ]

        for part_name in custom_xml_parts:
            xml_bytes = docx.read(part_name)
            xml_text = xml_bytes.decode("utf-8")
            
            try:
                root = ET.fromstring(xml_text)
            except ET.ParseError:
                continue  # skip non-XML parts

            expected_tag = f"{{{namespace_uri}}}{root_local_name}"
            if root.tag != expected_tag:
                continue

            if return_cdata_only:
                # ElementTree stores CDATA as normal text
                # text = text.encode("utf-8").decode("unicode_escape")
                if root.text:
                    # results.append(root.text.strip())
                    results.append(root.text.encode("utf-8").decode("unicode_escape"))
            else:
                results.append(xml_text)
     
    
    res = {
            "YAML": results,
        }

    return res
    
    
    

def deserialize_docx4j_yaml(xml_bytes: bytes) -> Any:
    """
    Deserialize YAML embedded in a custom XML part created by the
    docx4j addYamlAsCustomXml() method.

    Parameters
    ----------
    xml_bytes : bytes
        The raw XML content of the CustomXmlDataStoragePart.

    Returns
    -------
    Any
        The Python object produced by yaml.safe_load()
    """

    # Parse XML
    root = ET.fromstring(xml_bytes)

    # Sanity check: expected root element
    if not root.tag.endswith("docxFormSpec"):
        raise ValueError(f"Unexpected root element: {root.tag}")

    # ElementTree automatically exposes CDATA as .text
    yaml_text = root.text

    if yaml_text is None or not yaml_text.strip():
        raise ValueError("No YAML content found in XML CDATA")

    # Trim leading/trailing newlines and indentation
    yaml_text = yaml_text.strip()

    # Parse YAML
    return yaml.safe_load(yaml_text)




from zipfile import ZipFile
import xml.etree.ElementTree as ET
import yaml
from typing import List


def deserialize_docx4j_yaml_from_docx(docx_path: str) -> List[str]:
    """
    Extract YAML embedded in docx4j custom XML parts and return it
    as YAML-formatted strings (not Python objects).

    Each list element is a YAML document (string).
    """

    section = {}

    with ZipFile(docx_path, "r") as z:
        for name in z.namelist():
            if not name.startswith("customXml/") or not name.endswith(".xml"):
                continue

            xml_bytes = z.read(name)
            root = ET.fromstring(xml_bytes)

            if not root.tag.endswith("docxFormSpec"):
                continue

            raw_yaml = root.text
            if not raw_yaml or not raw_yaml.strip():
                continue

            # 1. Parse (validation + normalization)
            parsed = yaml.safe_load(raw_yaml)

            # 2. Re-dump as nicely formatted YAML
            yaml_text = yaml.safe_dump(
                parsed,
                sort_keys=False,
                allow_unicode=True,
                default_flow_style=False,
            )
            
            section = {
              "type": "embedded_yaml",
              "format": "yaml",
              "note": "This is the YAML code that created the docx file using code from the APPN code repository",
              "repository": "https://github.com/aus-plant-phenomics-network/appn-data-system-notes-internal/tree/main/metadata-ro-crate-git-hdf5-notes/docx-metadata-sripts/docx4j",
              "source": name,
              "content": yaml_text
            }

            # yaml_documents.append(section)

    return section



def write_yaml_from_json_content(json_obj: dict, output_path: str) -> None:
    """
    Write a valid YAML file from a JSON object containing a 'content' key
    holding YAML text.

    Parameters
    ----------
    json_obj : dict
        JSON object containing a 'content' key with YAML text
    output_path : str
        Path to the output .yaml/.yml file
    """

    if "content" not in json_obj:
        raise KeyError("JSON object does not contain a 'content' key")

    yaml_text = json_obj["content"]

    if not isinstance(yaml_text, str):
        raise TypeError("'content' must be a string containing YAML text")

    Path(output_path).write_text(yaml_text, encoding="utf-8")
    

def extract_images_from_docx(docx_path: str, output_dir: str, filename: str) -> List[str]:
    """
    Extract all images from a DOCX file into a directory.
    """
    res = []
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with ZipFile(docx_path, "r") as docx:
        for name in docx.namelist():
            if name.startswith("word/media/"):
                image_bytes = docx.read(name)
                if filename == "":
                    image_name = Path(output_path / name)
                else:
                    image_name = Path(output_path / filename)
                image_name.write_bytes(image_bytes)
                res.append(str(image_name))
                
    return res




def extract_logo_filename(json_obj: dict) -> str:
    """
    Extract the filename following 'logo/' up to the next newline
    from the 'content' field of a dictionary.

    Returns None if not found.
    """
    if "content" not in json_obj:
        raise KeyError("JSON object does not contain a 'content' key")
    yaml_text = json_obj.get("content", "")
    match = re.search(r"logo/([^\n]+)", yaml_text)
    return match.group(1) if match else ""


def usage():
    print(
        "Usage:\n"
        "  python extract_form_fields.py -f <file.docx> [-e] [-y]\n\n"
        "Options:\n"
        "  -f <file.docx>   Path to the DOCX file (required)\n"
        "  -e               Extract form fields\n"
        "  -y               Deserialize embedded docx4j YAML\n"
        "  -w               Write YAML to file <file.yml> and extract image to ./logo \n"
    )
    sys.exit(2)


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:eyw")
    except getopt.GetoptError:
        usage()

    docx_path = None
    do_extract_fields = False
    do_yaml = False
    do_write_yaml = False

    for opt, arg in opts:
        if opt == "-f":
            docx_path = arg
        elif opt == "-e":
            do_extract_fields = True
        elif opt == "-y":
            do_yaml = True
        elif opt == "-w":
            do_write_yaml = True

    if not docx_path:
        usage()

    # If neither -y or -e flag is given, default to both (optional but sensible)
    if not do_extract_fields and not do_yaml:
        do_extract_fields = True
        do_yaml = True

    output = []

    if do_extract_fields:
        fields = extract_fields(docx_path)
        output.extend(fields)

    if do_yaml:
        embedded_yaml = deserialize_docx4j_yaml_from_docx(docx_path)
        if embedded_yaml:
            output.append(embedded_yaml)
            
        if do_write_yaml:
            yml_path = Path(docx_path).with_suffix(".yml")
            write_yaml_from_json_content(
                    json_obj=embedded_yaml,
                    output_path=yml_path
            )
            
            filename = extract_logo_filename(embedded_yaml)
            im_files = extract_images_from_docx( 
                    docx_path,
                   'logo', 
                   filename
            )
            
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if do_write_yaml:
        print(f"INFO: The yaml data has been written to file: {str(yml_path)}")
        print(f"INFO: The logo images have been written to file(s): {im_files}")
    

