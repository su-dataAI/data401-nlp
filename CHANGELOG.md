# CHANGELOG

## [0.0.7] - 2026-01-28

### Improved
- **`helpers.env` (00_env.py)**: Enhanced `.env` file discovery with upward directory traversal
  - Now searches parent directories for `.env` files, stopping at project root markers (`.git`, `pyproject.toml`, or `data401_nlp` directory)
  - Improves compatibility with notebooks in subdirectories
- **`helpers.submit` (02_submit.py)**: Fixed Deepnote compatibility and improved answer extraction
  - Resolved issues with default answer extraction in Deepnote environments
  - Ensured default answers come from active variables rather than notebook cell metadata
  - More robust handling of notebook execution contexts

### Fixed
- Corrected nbdev test directives in course notebooks (changed `#!` to `#|` syntax)
- Added test skip patterns for draft notebooks, templates, and checkpoint files to speed up testing

## [0.0.6] - 2026-01-13

### Changed
- **Slimmed down core requirements**: Removed `pandas`, `numpy`, `matplotlib`, `nltk`, and `orjson` from core package dependencies
  - These are now optional dependencies in the `[nlp]` extras group
  - Core package now only includes dependencies needed by helper modules
  - Install with `pip install data401-nlp[nlp]` or `data401-nlp[all]` for full notebook dependencies
- Updated `requirements.txt`, `colab-requirements.txt`, and `deepnote-requirements.txt` to reflect slimmed-down core
- Updated platform compatibility tests in `99_platform_test.ipynb` to distinguish core vs. optional dependencies

### Added
- `SUBMIT_API_KEY` support in `load_env()` function for Colab environments
  - Now loads submission API key from Colab userdata alongside LLM API keys

### Fixed
- Removed `nbdev_prepare` from PyPI release workflow (no longer requires Quarto)
- Fixed trusted publisher configuration in GitHub Actions release workflow

## [0.0.4] - 2026-01-10

### Added
- `review_answers()` function in `helpers.submit` module - allows students to review extracted answers from their notebooks without submitting them to the grading service

## [0.0.3] - Previous release

### Changed
- Updated dependencies and requirements

## [0.0.2] - Initial release

### Added
- Initial submission helper functionality
- Answer collection and parsing from notebooks
