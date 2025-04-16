# Meal Server

A Python-based MCP server for accessing [TheMealDB API](https://www.themealdb.com/).

## About TheMealDB

[TheMealDB](https://www.themealdb.com/) is an open, crowd-sourced database of recipes from around the world. The database includes:

- Detailed meal recipes with ingredients and instructions
- Categorization by meal type, region, and ingredients
- Images and videos for many recipes
- Free API access for basic features

This MCP server provides a convenient interface to TheMealDB's API through Claude, Clide, or similar AI clients, allowing you to search for and retrieve meal information using natural language.

## Features

- Get meals by letter, name, ingredient, category, or area
- Get random meals
- Get all meal categories

## Usage

```
python mealserver.py
```

## MCP Client Integration

To use this server with Claude, Clide, or similar MCP-compatible clients, you need to add it to your client's MCP settings configuration. For example, with Cline (a VS Code extension for Claude), you would add it to your `cline_mcp_settings.json` file. This file is typically located at:

- Windows: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
- macOS: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- Linux: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

Add the following configuration to the `mcpServers` object in your settings file:

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

After adding this configuration, restart your MCP client or reload the window. You should then be able to use the mealserver tools in your conversations with your AI assistant.