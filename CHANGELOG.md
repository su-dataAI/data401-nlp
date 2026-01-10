# Changelog

All notable changes to the data401-nlp project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Requirements & Dependencies
- **Dependency Extras**: Added flexible installation options via extras_require
  - `[nlp]`: spaCy (>=3.7,<3.9) and NLTK (>=3.9,<3.10)
  - `[transformers]`: transformers (>=4.45,<4.50) and torch (>=2.1,<2.5)
  - `[api]`: FastAPI (>=0.100,<0.128) and Pydantic (>=2.0,<3)
  - `[all]`: All optional dependencies combined
  - `[dev]`: Development tools (pytest, nbdev, pre-commit)
- **Consolidated Requirements**: settings.ini now serves as single source of truth for dependencies
- Enhanced setup.py to properly parse and handle extras_require from settings.ini

#### CI/CD Workflows
- **Enhanced Test Workflow** (.github/workflows/test.yaml)
  - Python 3.11 and 3.12 matrix testing
  - Pip caching for faster builds
  - Upgraded to actions/setup-python@v5
  - Automatic spaCy model and NLTK data downloads
  - Pinned Quarto version (1.4.550) for reproducibility
  - Removed error silencing - tests now properly fail on errors
  - Install with extras: `pip install -e ".[dev,all]"`

- **Enhanced Deploy Workflow** (.github/workflows/deploy.yaml)
  - Upgraded to actions/setup-python@v5 with pip caching
  - Fixed Python version consistency (was incorrectly 3.12, now 3.11)
  - Added id-token permission for trusted publishing support
  - Installs full dependencies for proper documentation building

- **New Release Workflow** (.github/workflows/release.yaml)
  - Automated PyPI publishing via trusted publishing
  - Version consistency validation before release
  - Manual dispatch option with version input
  - Proper package building and verification with twine
  - Support for both GitHub releases and manual triggers

#### Helper Modules
- **spaCy Model Helper** (nbs/helpers/03_spacy.ipynb)
  - `ensure_spacy_model(model_name, verbose)`: Automatically downloads and loads spaCy models
  - `list_installed_models()`: Lists all installed spaCy models
  - Eliminates need for manual model downloads in notebooks
  - Works seamlessly across Colab, Deepnote, and local environments

- **Platform Compatibility Tests** (nbs/99_platform_test.ipynb)
  - Comprehensive test suite for cross-platform compatibility
  - Tests core imports, environment detection, and dependencies
  - Validates Python version requirements (>=3.11)
  - Non-failing tests for optional dependencies
  - Full integration test: `test_full_platform_compatibility()`

#### Documentation
- **Enhanced Installation Guide** (nbs/index.ipynb)
  - Comprehensive installation instructions for students vs developers
  - Platform-specific setup for Colab, Deepnote, and local environments
  - Installation options documentation for all extras
  - Platform support matrix (Colab, Deepnote, Jupyter Lab, Local)
  - Helper modules overview and usage examples

#### Developer Tools
- **Pre-commit Hooks** (.pre-commit-config.yaml)
  - Standard hooks: trailing-whitespace, end-of-file-fixer, check-yaml
  - Check for large files (max 5MB)
  - Merge conflict detection
  - TOML validation
  - Debug statement detection
  - nbdev-specific hooks: nbdev_clean and nbdev_export

- **Dependabot Configuration** (.github/dependabot.yml)
  - Monthly automated dependency updates
  - Grouped updates for related packages:
    - dev-dependencies: pytest, nbdev, pre-commit
    - nlp-core: spaCy, NLTK
    - transformers: transformers, torch
    - api: FastAPI, Pydantic
  - Separate tracking for GitHub Actions
  - Proper labeling and commit message prefixes

#### Configuration
- **Enhanced pyproject.toml**
  - Comprehensive project metadata and modern classifiers
  - Project URLs: homepage, documentation, repository, bug tracker, course website
  - PyPI classifiers for AI/Education topics
  - Pytest configuration (testpaths, python_files, addopts)
  - Coverage configuration
  - nbdev tool configuration

### Changed

#### Requirements Management
- Updated requirements.txt with clear documentation and version ranges
- Updated deepnote-requirements.txt for Deepnote-specific needs with litellm
- Removed direct spaCy model URL dependency (now handled at runtime via helper)
- Standardized version constraints:
  - fastcore: >=1.8.16 (was >=1.8.0)
  - pandas: >=2.0,<2.3 (was >=2.1.0)
  - spacy: >=3.7,<3.9 (was >=3.7.0)
  - nltk: >=3.9,<3.10 (was >=3.8.0)
  - IPython: >=9.7.0 (was >=7.34.0)
  - Added httpx: >=0.27.0

#### PyPI Metadata
- Updated package description: "Interactive NLP course labs for Jupyter, Colab, and Deepnote"
- Enhanced keywords: added nlp, education, spacy, transformers
- Changed development status from 3 (Alpha) to 4 (Beta)
- Improved classifiers for better PyPI discoverability

#### Version Management
- Fixed version consistency between settings.ini (0.0.3) and __init__.py (0.0.3)
- Verified put_version_in_init works correctly with nbdev

### Fixed
- Version mismatch between settings.ini and data401_nlp/__init__.py
- Python version inconsistency in deploy workflow
- Error silencing in test workflow that masked failures
- Redundant pip upgrade commands in workflows
- Missing pip caching in CI/CD workflows

### Removed
- Direct URL dependency for en_core_web_sm in requirements files
- Error silencing (`|| echo "No tests to run"`) from test workflow
- Incorrect Python version override in deploy workflow

## [0.0.3] - 2025-01-10

### Repository Review & Best Practice Implementation

This release implements comprehensive improvements to requirements management,
CI/CD workflows, PyPI packaging, documentation, and developer tooling based on
nbdev and Python packaging best practices.

#### Installation Options

Students and users can now install the package with flexible options:

```bash
# Minimal installation (core utilities only)
pip install data401-nlp

# With NLP tools (spaCy, NLTK)
pip install data401-nlp[nlp]

# With transformers and PyTorch
pip install data401-nlp[transformers]

# With API support (FastAPI, Pydantic)
pip install data401-nlp[api]

# Everything (recommended for course students)
pip install data401-nlp[all]

# Development with all tools
pip install -e ".[dev,all]"
```

#### Platform Support

- ✅ Google Colab
- ✅ Deepnote
- ✅ Jupyter Lab
- ✅ Local Python 3.11+

#### Helper Modules

The package includes helper modules to simplify NLP workflows:

- `data401_nlp.helpers.env` - Environment detection and API key loading
- `data401_nlp.helpers.spacy` - Automatic spaCy model management
- `data401_nlp.helpers.submit` - Assignment submission utilities
- `data401_nlp.helpers.llm` - LLM integration helpers

#### Testing

Package builds successfully with all features:
- Wheel package verified with all modules included
- Extras_require properly configured in package metadata
- Platform compatibility tests ready to run
- CI/CD workflows validated

---

## How to Use This Package

### For Students (Google Colab / Deepnote)

```python
# Install in notebook
!pip install -q data401-nlp[all]

# Use spaCy with automatic model management
from data401_nlp.helpers.spacy import ensure_spacy_model
nlp = ensure_spacy_model("en_core_web_sm")  # Auto-downloads if needed

# Environment detection
from data401_nlp.helpers.env import load_env
env = load_env()
```

### For Developers (Local)

```bash
# Clone and setup
git clone https://github.com/su-dataAI/data401-nlp.git
cd data401-nlp

# Install with all dependencies
pip install -e ".[dev,all]"

# Setup pre-commit hooks
pre-commit install

# Download required data
python -m spacy download en_core_web_sm
python -m nltk.downloader vader_lexicon

# Start development
jupyter lab
```

### For Contributors

1. Install development dependencies: `pip install -e ".[dev,all]"`
2. Install pre-commit hooks: `pre-commit install`
3. Make changes in notebooks under `nbs/`
4. Export changes: `nbdev_export`
5. Clean notebooks: `nbdev_clean`
6. Run tests: `nbdev_test`
7. Build docs: `nbdev_docs`

---

## Migration Guide

### If you were using requirements.txt directly:

**Before:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**After:**
```bash
pip install data401-nlp[all]
# spaCy model downloads automatically when needed
```

### If you were manually checking for spaCy models:

**Before:**
```python
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    !python -m spacy download en_core_web_sm
    nlp = spacy.load("en_core_web_sm")
```

**After:**
```python
from data401_nlp.helpers.spacy import ensure_spacy_model
nlp = ensure_spacy_model("en_core_web_sm")
```

---

## Next Steps

1. **Enable Dependabot**: Dependabot will automatically monitor dependencies
2. **Setup Pre-commit**: Contributors should run `pre-commit install`
3. **PyPI Trusted Publishing**: Configure at https://pypi.org for secure releases
4. **Address Security**: Review and fix the 33 detected vulnerabilities

---

## Links

- **Repository**: https://github.com/su-dataAI/data401-nlp
- **Documentation**: https://su-dataAI.github.io/data401-nlp
- **Course Website**: https://www.notion.so/Intro-to-Natural-Language-Processing-28b213a83886806982a5c03b425595c4
- **Issues**: https://github.com/su-dataAI/data401-nlp/issues
- **PyPI**: https://pypi.org/project/data401-nlp/

---

## Credits

Repository improvements implemented following nbdev best practices and
Python packaging standards (PEP 517, PEP 621).
