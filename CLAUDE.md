# Project Instructions for Claude

## Jupyter Notebook Editing

### NotebookEdit Tool (Native)
- Uses **static cell IDs** that don't change after insertions
- `insert` mode inserts AFTER the referenced `cell_id`
- **Problem**: Multiple insertions reference original IDs, causing all new cells to pile up in the same region
- **Workaround**: Insert in **reverse order** (bottom to top), or reorder cells after insertion

### Jupyter MCP Server (Preferred)
- Uses **integer indices** that reflect current notebook state
- After inserting at index N, subsequent inserts account for the shift
- Requires notebook to be accessible via Jupyter collaboration API
- Config: `.mcp.json` with `mcpServers` key (not `mcp.servers`)

### Best Practice for Interleaved Insertions
When adding explanatory cells between existing code cells:
1. Use MCP with index-based insertion if available
2. Or insert in reverse order (last position first)
3. Or batch all insertions, then reorder with a script

## MCP Configuration

### Option 1: Local Document Mode (Recommended)
Reads notebooks directly from filesystem, executes via Jupyter kernel.
Does NOT require jupyter-collaboration extension.

```json
{
  "mcpServers": {
    "jupyter": {
      "command": ".venv/bin/python",
      "args": ["-m", "jupyter_mcp_server"],
      "env": {
        "DOCUMENT_URL": "local",
        "RUNTIME_URL": "http://localhost:8888",
        "RUNTIME_TOKEN": "your-token",
        "DOCUMENT_ID": "path/to/notebook.ipynb"
      }
    }
  }
}
```

### Option 2: Full RTC Mode
Requires `jupyter-collaboration` extension installed on the Jupyter server.
Enables real-time sync with JupyterLab.

```json
{
  "mcpServers": {
    "jupyter": {
      "command": ".venv/bin/python",
      "args": ["-m", "jupyter_mcp_server"],
      "env": {
        "JUPYTER_URL": "http://localhost:8888",
        "JUPYTER_TOKEN": "your-token",
        "DOCUMENT_ID": "path/to/notebook.ipynb"
      }
    }
  }
}
```

### Environment Variables
| Variable | Description |
|----------|-------------|
| `JUPYTER_URL` | Convenience: sets both DOCUMENT_URL and RUNTIME_URL |
| `JUPYTER_TOKEN` | Convenience: sets both tokens |
| `DOCUMENT_URL` | Where to read notebooks (`local` or `http://...`) |
| `RUNTIME_URL` | Where to execute code (`local` or `http://...`) |
| `DOCUMENT_ID` | Default notebook path |
