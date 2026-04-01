#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage:

  Generate DOCX:
    generate-docx-form --spec form.yaml --out form.docx

  Extract fields:
    generate-docx-form --extract form.docx --json fields.json

Options:
  -s, --spec <file>        YAML spec file
  -o, --out <file>         Output DOCX file
  -x, --extract <file>     Extract fields from DOCX
  -j, --json <file>        JSON output file
  -h, --help               Show this help
EOF
}

# -------------------------
# GNU getopt parsing
# -------------------------
PARSED=$(getopt \
  --options s:o:x:j:h \
  --longoptions spec:,out:,extract:,json:,help \
  --name "$0" \
  -- "$@"
)

if [[ $? -ne 0 ]]; then
  usage
  exit 2
fi

eval set -- "$PARSED"

MODE="generate"
SPEC=""
OUT=""
EXTRACT=""
JSON_OUT=""
YAML_OUT=""


while true; do
  case "$1" in
    -s|--spec)
      SPEC="$2"
      shift 2
      ;;
    -o|--out)
      OUT="$2"
      shift 2
      ;;
    -x|--extract)
      MODE="extract"
      EXTRACT="$2"
      shift 2
      ;;
    -j|--json)
      JSON_OUT="$2"
      shift 2
      ;;
    -y|--yaml)
      YAML_OUT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      echo "> Unexpected option: $1"
      usage
      exit 1
      ;;
  esac
done

# -------------------------
# Extract mode
# -------------------------
if [[ "$MODE" == "extract" ]]; then
  if [[ -z "$EXTRACT" ]]; then
    echo "> --extract requires a DOCX file"
    exit 1
  fi

  echo "> Extracting fields from DOCX: $EXTRACT"

  if [[ -n "$JSON_OUT" ]]; then
    python3 /app/extract_form_fields.py -f "$EXTRACT" -y > "$JSON_OUT"
    echo "> JSON written to $JSON_OUT"
  else
    # Extracts embedded yaml from docx and saves it as YAML to input 
    # file name with .yml extension
    python3 /app/extract_form_fields.py -f "$EXTRACT" -w
  fi

  exit 0
fi

# -------------------------
# Generate mode
# -------------------------
if [[ -z "$SPEC" || -z "$OUT" ]]; then
  echo "> Generate mode requires --spec and --out"
  usage
  exit 1
fi

echo "> Generating DOCX..."
java -jar /app/generate-docx-form.jar \
  --spec "$SPEC" \
  --out "$OUT"

if [[ ! -f "$OUT" ]]; then
  echo "> Output DOCX not found: $OUT"
  exit 1
fi

