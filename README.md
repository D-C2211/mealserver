# Meal Server

A Python-based MCP server for TheMealDB API.

## Features

- Get meals by letter, name, ingredient, category, or area
- Get random meals
- Get all meal categories

## Usage

```
python mealserver.py
```

## Cline Integration

To use this server with Cline, you need to add it to your `cline_mcp_settings.json` file. This file is typically located at:

- Windows: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
- macOS: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- Linux: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

Add the following configuration to the `mcpServers` object in your `cline_mcp_settings.json` file:

```json
"mealserver": {
  "command": "uv",
  "args": [
    "--directory",
    "C:\\mcp\\mealserver",
    "run",
    "mealserver.py"
  ]
}
```

Make sure to adjust the directory path to match your installation location.

After adding this configuration, restart Cline or reload the window in VS Code. You should then be able to use the mealserver tools in your conversations with Claude.