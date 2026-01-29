# Build Validation Scripts

This directory contains scripts to validate nbdev/Quarto builds before pushing to GitHub Actions.

## Pre-Push Validation

The `validate-build.sh` script performs comprehensive checks to catch common build issues locally before they reach CI.

### What It Checks

1. **Required Tools**: Verifies Python, nbdev, and Quarto are installed
2. **Stale Cache**: Detects Quarto cache that might cause build issues
3. **Orphaned Files**: Finds HTML files in `_proc/` that shouldn't be there
4. **YAML Frontmatter**: Checks for mismatched `output-file` specifications in notebooks
5. **Configuration Consistency**: Ensures settings.ini and pyproject.toml are aligned
6. **nbdev_prepare**: Runs the preparation step and reports any errors
7. **Documentation Build**: (Optional) Tests the full Quarto build

### Usage

#### Manual Run

```bash
# Quick validation (skips full build)
.github/scripts/validate-build.sh

# Full validation including Quarto build
.github/scripts/validate-build.sh --full-build
```

#### Automatic Pre-Push Hook

The pre-push hook runs automatically before `git push`. It validates your build and prevents pushing broken code to GitHub.

**To skip the hook** (not recommended):
```bash
git push --no-verify
```

### Installation

The pre-push hook is installed at `.git/hooks/pre-push`. If you clone the repository fresh, you'll need to make it executable:

```bash
chmod +x .git/hooks/pre-push
```

### Common Issues

#### Issue: "Problematic YAML frontmatter"

**Symptom**: Notebook has `output-file:` that doesn't match the expected filename

**Fix**:
1. Open the notebook in Jupyter
2. Check for raw cells with YAML frontmatter
3. Remove or correct the `output-file:` line
4. Re-run `nbdev_prepare`

#### Issue: "Orphaned HTML files"

**Symptom**: Old `.html` files exist in `_proc/` directory

**Fix**:
```bash
rm -f _proc/*.html
rm -rf _proc/*_files
```

#### Issue: "Configuration files inconsistent"

**Symptom**: `custom_sidebar` setting differs between settings.ini and pyproject.toml

**Fix**: Ensure both files have the same value:
- `settings.ini`: `custom_sidebar = False`
- `pyproject.toml`: `custom_sidebar = false`

#### Issue: "Quarto cache exists"

**Symptom**: Stale cache might cause incorrect output filenames

**Fix**:
```bash
rm -rf _proc/.quarto
```

### Troubleshooting

If validation fails:

1. Read the error messages carefully
2. Run full build test: `.github/scripts/validate-build.sh --full-build`
3. Check the GitHub Actions workflow logs for similar errors
4. Clear caches and regenerate: `rm -rf _proc && nbdev_prepare`

### Maintenance

The validation script should be updated when:
- New common build issues are discovered
- nbdev or Quarto changes their behavior
- New configuration files are added to the project

## Related Files

- `.git/hooks/pre-push`: Git hook that runs validation automatically
- `.github/workflows/deploy.yaml`: GitHub Actions workflow for deployment
- `settings.ini`: nbdev configuration (legacy)
- `pyproject.toml`: Python project configuration (modern standard)
