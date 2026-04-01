import yaml
import re
import os

import getopt
import sys

from typing import List, Dict, Optional



OUTPUT_DIR = "generated"

def parse_opts(argv):
    """
    POSIX-style option parsing (getopt), similar to shell getopts.
    usage example:
    python generate_models.py -y tpa_xray_ct_booking.yaml
    """
    yaml_path = None

    try:
        opts, args = getopt.getopt(
            argv,
            "y:",
            ["yaml="]
        )
    except getopt.GetoptError as err:
        print(err)
        print("Usage: generate_models.py -y <yaml_file>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-y", "--yaml"):
            yaml_path = arg

    if not yaml_path:
        print("Error: YAML file is required")
        print("Usage: generate_models.py -y <yaml_file>")
        sys.exit(2)

    return yaml_path
    
# -----------------------------
# Helpers
# -----------------------------

def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def clean_section_name(text: str) -> str:
    text = re.sub(r"^[\s\dA-Z]+\.\s*", "", text)
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
    return "".join(word.capitalize() for word in text.split())


def snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


# -----------------------------
# Model structures
# -----------------------------

class SectionNode:
    def __init__(self, name: str):
        self.name = name
        self.fields: List[dict] = []
        self.children: List["SectionNode"] = []
        self.parent: Optional["SectionNode"] = None


# -----------------------------
# Parsing YAML → tree
# -----------------------------

def build_section_tree(rows: list) -> List[SectionNode]:
    roots: List[SectionNode] = []
    stack: List[SectionNode] = []

    for row in rows:
        if row.get("type") == "section":
            section_name = clean_section_name(row["text"])
            node = SectionNode(section_name)

            if stack:
                node.parent = stack[-1]
                stack[-1].children.append(node)
            else:
                roots.append(node)

            stack.append(node)

        elif row.get("type") == "field":
            if not stack:
                continue
            stack[-1].fields.append(row)

    return roots


# -----------------------------
# Code generation
# -----------------------------
def generate_class_code(node: SectionNode) -> str:
    class_name = node.name
    imports = ["from .form_data_mixin import FormDataMixin"]

    for child in node.children:
        imports.append(
            f"from .{snake_case(child.name)} import {child.name}"
        )

    lines = []
    lines.extend(imports)
    lines.append("")
    lines.append(f"class {class_name}(FormDataMixin):")

    # Metadata for loader
    field_names = [f["name"] for f in node.fields]
    child_attrs = [snake_case(child.name) for child in node.children]

    lines.append(f"    _field_names = {field_names!r}")
    lines.append(f"    _child_sections = {child_attrs!r}")
    lines.append("")
    lines.append("    def __init__(self, **kwargs):")

    if not node.fields and not node.children:
        lines.append("        pass")

    for field in node.fields:
        name = field["name"]
        items = field.get("items")

        if items:
            lines.append(f"        self._{name} = None")
            lines.append(f"        self.{name} = kwargs.get('{name}')")
        else:
            lines.append(f"        self.{name} = kwargs.get('{name}')")

    for child in node.children:
        attr = snake_case(child.name)
        lines.append(f"        self.{attr} = {child.name}()")

    # Validation properties
    for field in node.fields:
        name = field["name"]
        items = field.get("items")

        if items:
            allowed = repr(items)
            lines.append("")
            lines.append("    @property")
            lines.append(f"    def {name}(self):")
            lines.append(f"        return self._{name}")
            lines.append("")
            lines.append(f"    @{name}.setter")
            lines.append(f"    def {name}(self, value):")
            lines.append("        if value is None:")
            lines.append(f"            self._{name} = None")
            lines.append("            return")
            lines.append(f"        allowed = {allowed}")
            lines.append("        if value not in allowed:")
            lines.append(
                f"            raise ValueError("
                f"Invalid value for '{name}': {{value}}. "
                f"Allowed values: {{allowed}}\"\"\")"
            )
            lines.append(f"        self._{name} = value")

    return "\n".join(lines)

def write_section_files(node: SectionNode):
    filename = f"{snake_case(node.name)}.py"
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(generate_class_code(node))

    for child in node.children:
        write_section_files(child)

def write_mixin():
    with open(os.path.join(OUTPUT_DIR, "form_data_mixin.py"), "w") as f:
        f.write(
            "import json\n"
            "from typing import Dict, Any, List\n\n"
            "class FormDataMixin:\n"
            "    @staticmethod\n"
            "    def _build_value_map(data: List[dict]) -> Dict[str, Any]:\n"
            "        return {item['alias']: item.get('value') for item in data if 'alias' in item}\n\n"
            "    def load_from_json(self, data: List[dict]):\n"
            "        value_map = self._build_value_map(data)\n"
            "        for field_name in getattr(self, '_field_names', []):\n"
            "            if field_name in value_map:\n"
            "                setattr(self, field_name, value_map[field_name])\n"
            "        for child_attr in getattr(self, '_child_sections', []):\n"
            "            getattr(self, child_attr).load_from_json(data)\n"
        )
# -----------------------------
# Entry point
# -----------------------------

def generate_models(yaml_path: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # WRITE THE MIXIN FIRST
    write_mixin()

    data = load_yaml(yaml_path)
    rows = data.get("rows", [])

    roots = build_section_tree(rows)

    for root in roots:
        write_section_files(root)

    # package init
    with open(os.path.join(OUTPUT_DIR, "__init__.py"), "w") as f:
        f.write("# generated models\n")


if __name__ == "__main__":
    yaml_file = parse_opts(sys.argv[1:])
    generate_models(yaml_file)
