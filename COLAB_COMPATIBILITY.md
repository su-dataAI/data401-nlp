# Google Colab Compatibility Guide

## Overview

This library has been updated to support Google Colab, which uses Python 3.10 and has IPython 7.34.0 pre-installed.

## Changes Made

### 1. Removed Explicit IPython Requirement

IPython is no longer explicitly required in:
- `settings.ini`
- `requirements.txt`
- `deepnote-requirements.txt`

**Why?** IPython is automatically pulled in as a transitive dependency through:
```
data401-nlp
  → dialoghelper>=0.1.6
    → ipykernel-helper
      → ipython
```

### 2. Created Colab-Specific Requirements File

A new `colab-requirements.txt` file has been created with Python 3.10 compatible pins.

**Key difference:** Pins `numpy>=1.24,<2.0` (numpy 2.x requires Python 3.11+)

### 3. Updated Documentation

`nbs/index.ipynb` now includes separate installation instructions for:
- Google Colab (using `colab-requirements.txt`)
- Deepnote (using standard installation)
- Local development

## Installation Instructions

### For Students Using Google Colab

In the first cell of your Colab notebook:

```python
# Download and install Colab-specific requirements
!wget -q https://raw.githubusercontent.com/su-dataAI/data401-nlp/main/colab-requirements.txt
!pip install -q -r colab-requirements.txt

# The spaCy model will be automatically downloaded when needed
from data401_nlp.helpers.spacy import ensure_spacy_model
nlp = ensure_spacy_model("en_core_web_sm")
```

### For Students Using Deepnote

```python
!pip install -q data401-nlp[all]
```

### For Local Development (Python 3.11+)

```bash
git clone https://github.com/su-dataAI/data401-nlp.git
cd data401-nlp
pip install -e ".[dev,all]"
```

## Technical Details

### Python Version Compatibility

| Environment | Python Version | numpy Version | IPython Version |
|------------|----------------|---------------|-----------------|
| Google Colab | 3.10 | 1.24-1.26 | 7.34.0 (pre-installed) |
| Deepnote | 3.11+ | 2.x | 9.x+ |
| Local Dev | 3.11+ | 2.x | 9.x+ |

### Dependency Chain

The library's core dependencies are compatible with Python 3.10+, except:
- **numpy 2.x** requires Python 3.11+
- **numpy 1.26.x** supports Python 3.9-3.12

### IPython Usage

IPython is used in the notebooks for visualization:
```python
from IPython.display import display, HTML
```

This works with both IPython 7.34.0 (Colab) and IPython 9.x+ (Deepnote/Local).

## Testing

To verify Colab compatibility, you can run:

```python
import sys
import numpy as np
import IPython

print(f"Python: {sys.version}")
print(f"numpy: {np.__version__}")
print(f"IPython: {IPython.__version__}")
```

Expected output in Colab:
- Python: 3.10.x
- numpy: 1.24-1.26
- IPython: 7.34.0

## Future Considerations

If you need to support only Python 3.11+, you can:
1. Remove `colab-requirements.txt`
2. Update `min_python = 3.11` in `settings.ini`
3. Allow numpy 2.x in requirements

However, this will break Google Colab compatibility unless Colab upgrades to Python 3.11+.
