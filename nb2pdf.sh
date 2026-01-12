#!/bin/bash
# Export Jupyter notebook to PDF with SVG support
# Usage: ./nb2pdf.sh notebook_name.ipynb
# Converts notebooks from nbs/ and saves to nbs/pdf/

if [ $# -eq 0 ]; then
    echo "Usage: $0 notebook_name.ipynb"
    echo "Converts nbs/notebook_name.ipynb to nbs/pdf/notebook_name.pdf"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NOTEBOOK_NAME="$1"
BASENAME=$(basename "$NOTEBOOK_NAME" .ipynb)
NOTEBOOK="$SCRIPT_DIR/nbs/$NOTEBOOK_NAME"
OUTPUT_DIR="$SCRIPT_DIR/nbs/pdf"
OUTPUT="$OUTPUT_DIR/$BASENAME.pdf"

# Check if notebook exists
if [ ! -f "$NOTEBOOK" ]; then
    echo "Error: Notebook not found: $NOTEBOOK"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Converting $NOTEBOOK_NAME to PDF..."

# Step 1: Convert to LaTeX
jupyter nbconvert --to latex "$NOTEBOOK" \
    --output "$OUTPUT_DIR/${BASENAME}_temp.tex"

# Step 2: Create symlink to images directory if it doesn't exist
if [ -d "$SCRIPT_DIR/nbs/images" ] && [ ! -e "$OUTPUT_DIR/images" ]; then
    ln -s "$SCRIPT_DIR/nbs/images" "$OUTPUT_DIR/images"
fi

# Step 3: Compile with xelatex (shell-escape for Inkscape)
cd "$OUTPUT_DIR"
xelatex -shell-escape -interaction=nonstopmode "${BASENAME}_temp.tex" > /dev/null

# Step 4: Run twice for cross-references
xelatex -shell-escape -interaction=nonstopmode "${BASENAME}_temp.tex" > /dev/null

# Step 5: Move and cleanup
mv "${BASENAME}_temp.pdf" "$BASENAME.pdf"
rm -f "${BASENAME}_temp".{tex,aux,log,out}
rm -rf "${BASENAME}_temp_files"

echo "✓ PDF created: $OUTPUT"
