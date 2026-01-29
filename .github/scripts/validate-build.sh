#!/usr/bin/env bash
# Pre-push validation script for nbdev/Quarto builds
# Catches common build issues before they reach GitHub Actions

set -e  # Exit on any error

echo "=== NBDev/Quarto Build Validation ==="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track validation status
VALIDATION_PASSED=true

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
        VALIDATION_PASSED=false
    fi
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 1. Check for required tools
echo "1. Checking required tools..."
command -v python3 >/dev/null 2>&1
print_status $? "Python 3 installed"

command -v nbdev_prepare >/dev/null 2>&1
print_status $? "nbdev installed"

command -v quarto >/dev/null 2>&1
print_status $? "Quarto installed"

echo ""

# 2. Check for stale Quarto cache
echo "2. Checking for stale cache..."
if [ -d "_proc/.quarto" ]; then
    print_warning "Quarto cache exists - will be cleared during build"
else
    print_status 0 "No stale cache found"
fi

echo ""

# 3. Check for orphaned HTML files in _proc
echo "3. Checking for orphaned HTML files..."
if [ -d "_proc" ]; then
    ORPHANED_HTML=$(find _proc -maxdepth 1 -name "*.html" -not -name "index.html" 2>/dev/null || true)
    if [ -n "$ORPHANED_HTML" ]; then
        print_warning "Found orphaned HTML files in _proc:"
        echo "$ORPHANED_HTML"
    else
        print_status 0 "No orphaned HTML files"
    fi
else
    print_status 0 "No _proc directory"
fi

echo ""

# 4. Check for problematic YAML frontmatter in notebooks
echo "4. Checking for problematic YAML frontmatter..."
PROBLEMATIC_NOTEBOOKS=$(python3 << 'EOF'
import json
import os
from pathlib import Path

problematic = []
nbs_dir = Path("nbs")

# Skip underscore-prefixed files and helpers
for nb_file in nbs_dir.glob("*.ipynb"):
    if nb_file.name.startswith("_") or nb_file.name.startswith("."):
        continue

    try:
        with open(nb_file) as f:
            nb = json.load(f)

        # Check for raw cells with output-file specification
        for cell in nb.get("cells", []):
            if cell.get("cell_type") == "raw":
                source = "".join(cell.get("source", []))
                if "output-file:" in source:
                    # Extract the output-file value
                    for line in source.split("\n"):
                        if "output-file:" in line:
                            output_file = line.split(":")[-1].strip()
                            expected_file = nb_file.stem + ".html"
                            if output_file != expected_file:
                                problematic.append(f"{nb_file.name}: has output-file={output_file}, expected {expected_file}")
    except Exception as e:
        print(f"Error checking {nb_file}: {e}", file=sys.stderr)

if problematic:
    for item in problematic:
        print(item)
    exit(1)
EOF
)

if [ $? -eq 0 ]; then
    print_status 0 "No problematic YAML frontmatter in notebooks"
else
    print_status 1 "Found problematic YAML frontmatter:"
    echo "$PROBLEMATIC_NOTEBOOKS"
fi

echo ""

# 5. Validate settings.ini and pyproject.toml consistency
echo "5. Checking configuration consistency..."
python3 << 'EOF'
import configparser
import toml
import sys

try:
    # Read settings.ini
    config = configparser.ConfigParser()
    config.read("settings.ini")

    # Read pyproject.toml
    with open("pyproject.toml") as f:
        pyproject = toml.load(f)

    # Check custom_sidebar consistency
    settings_custom_sidebar = config.get("DEFAULT", "custom_sidebar", fallback=None)
    pyproject_custom_sidebar = pyproject.get("tool", {}).get("nbdev", {}).get("custom_sidebar", None)

    if settings_custom_sidebar != str(pyproject_custom_sidebar).lower():
        print(f"Warning: custom_sidebar mismatch - settings.ini: {settings_custom_sidebar}, pyproject.toml: {pyproject_custom_sidebar}")
        sys.exit(1)
    else:
        print("Configuration files are consistent")
        sys.exit(0)
except Exception as e:
    print(f"Error checking configuration: {e}")
    sys.exit(1)
EOF

print_status $? "Configuration files consistent"

echo ""

# 6. Run nbdev_prepare
echo "6. Running nbdev_prepare..."
if nbdev_prepare 2>&1 | tee /tmp/nbdev_prepare.log; then
    print_status 0 "nbdev_prepare succeeded"
else
    print_status 1 "nbdev_prepare failed"
    cat /tmp/nbdev_prepare.log
fi

echo ""

# 7. Try building docs (dry run)
echo "7. Testing documentation build..."
if [ "$1" == "--full-build" ]; then
    # Full build with Quarto
    if nbdev_docs 2>&1 | tee /tmp/nbdev_docs.log; then
        print_status 0 "Documentation build succeeded"
    else
        print_status 1 "Documentation build failed"
        cat /tmp/nbdev_docs.log
    fi
else
    print_warning "Skipping full documentation build (use --full-build to test)"
fi

echo ""

# Summary
echo "=== Validation Summary ==="
if $VALIDATION_PASSED; then
    echo -e "${GREEN}All checks passed!${NC} Safe to push to GitHub."
    exit 0
else
    echo -e "${RED}Some checks failed.${NC} Please fix issues before pushing."
    exit 1
fi
