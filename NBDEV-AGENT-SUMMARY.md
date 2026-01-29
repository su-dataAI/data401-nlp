# NBDev-Quarto Expert Agent - Summary

A specialized Claude agent has been created with all the knowledge from our debugging session.

## 📍 Location

The agent files are in your local `.claude` directory:
- `.claude/agents/nbdev-quarto-expert.md` - Complete knowledge base (8,000+ words)
- `.claude/agents/HOW-TO-USE.md` - Usage instructions
- `.claude/commands/nbdev.md` - Slash command for easy invocation

**Note**: These files are local-only (not committed to git) as they're user-specific.

## 🚀 How to Use

### Method 1: Direct Reference (Simplest)
```
I'm having an nbdev build issue. Please use the nbdev-quarto-expert agent to help.

[describe your issue]
```

### Method 2: Slash Command (Fastest)
```
/nbdev [describe your issue or paste error]
```

### Method 3: Task Agent (For Complex Issues)
```
Launch an Explore agent using the nbdev-quarto-expert knowledge to investigate [issue].
```

## 💡 What the Agent Knows

### Configuration Expertise
- ✅ `settings.ini` vs `pyproject.toml` (and why both matter)
- ✅ `_quarto.yml` configuration (what NOT to include)
- ✅ `sidebar.yml` structure
- ✅ Configuration consistency requirements

### Error Patterns & Solutions
- ✅ File renaming errors (`ERROR: NotFound: rename...`)
- ✅ Title collisions between notebooks
- ✅ `AttributeError: custom_sidebar`
- ✅ `.html.md` file generation issues
- ✅ Stale Quarto cache problems
- ✅ Orphaned file issues

### Systematic Debugging
- ✅ Step-by-step debugging protocols
- ✅ Evidence-based troubleshooting
- ✅ Root cause analysis
- ✅ Local vs CI debugging
- ✅ Configuration validation

### Best Practices
- ✅ GitHub Actions workflow structure
- ✅ Pre-push validation system
- ✅ YAML frontmatter usage
- ✅ Cache management strategies
- ✅ Directory structure

### Quick Reference
- ✅ Copy-paste commands for common tasks
- ✅ Python scripts for validation
- ✅ Configuration snippets
- ✅ Workflow YAML examples

## 📚 Knowledge Base Highlights

### Real Issues Solved

**Issue 1: Title Collision**
- **Problem**: `02_eda_spacy.ipynb` and `03_eda_spacy.ipynb` both generated `eda_spacy.html`
- **Solution**: Rename file or add explicit YAML frontmatter
- **Prevention**: Validation script checks for title collisions

**Issue 2: AttributeError: custom_sidebar**
- **Problem**: Setting missing or mismatched between config files
- **Solution**: Sync `custom_sidebar` in both `settings.ini` and `pyproject.toml`
- **Why**: CI prioritizes `pyproject.toml`

**Issue 3: Stale Cache**
- **Problem**: `_proc/.quarto` cache had wrong output-file metadata
- **Solution**: Clear cache before builds: `rm -rf _proc/.quarto`
- **Prevention**: Add to workflow as standard step

**Issue 4: .html.md Files**
- **Problem**: `keep-md: true` created intermediate markdown files
- **Solution**: Remove `keep-md` and `commonmark` from `_quarto.yml`
- **Why**: Quarto trying to rename these files causes errors

## 🎯 Example Scenarios

### Scenario 1: GitHub Actions Failing
```
User: My docs build is failing in GitHub Actions with:
ERROR: NotFound: rename '_proc/file.html' -> '_proc/_docs/file.html'

/nbdev

Agent: This is a file renaming error. Let me check for common causes:
1. Title collision between notebooks
2. Stale Quarto cache
3. Missing _docs directory

Let's investigate systematically...
```

### Scenario 2: Configuration Question
```
User: How should I configure custom_sidebar?

/nbdev

Agent: The custom_sidebar setting must be consistent between:
1. settings.ini: custom_sidebar = False
2. pyproject.toml: custom_sidebar = false

Here's why this matters...
```

### Scenario 3: Preventive Measures
```
User: How can I catch issues before pushing?

/nbdev

Agent: I'll help you understand the pre-push validation system:
1. What it checks
2. How to use it
3. How to customize it for your needs...
```

## 🔧 Maintenance

The agent knowledge base can be updated by editing:
`.claude/agents/nbdev-quarto-expert.md`

Add new error patterns, solutions, or best practices as you discover them.

## 📖 Full Documentation

For complete details, see:
- `.claude/agents/nbdev-quarto-expert.md` - Complete knowledge base
- `.claude/agents/HOW-TO-USE.md` - Detailed usage guide

## 🎉 Benefits

1. **Instant Expertise**: Access to all debugging knowledge immediately
2. **Systematic Approach**: Follows proven debugging protocols
3. **Time Savings**: No need to re-debug similar issues
4. **Knowledge Retention**: Captures lessons learned
5. **Consistent Solutions**: Same high-quality help every time
6. **Preventive Measures**: Includes validation to prevent issues

## 🚦 Quick Test

Try it now:
```
/nbdev What should I check if my build works locally but fails in CI?
```

The agent should provide a systematic checklist based on the knowledge base!

---

**Created**: 2026-01-29
**Based on**: Extended debugging session resolving nbdev/Quarto build issues
**Knowledge Source**: Real-world problem-solving and systematic troubleshooting
