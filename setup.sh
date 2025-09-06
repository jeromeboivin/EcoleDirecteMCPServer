#!/bin/bash

# EcoleDirecte MCP Server Setup Script

echo "Setting up EcoleDirecte MCP Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    exit 1
fi

# Install FastMCP if not already installed
echo "Installing FastMCP..."
pip install fastmcp

# Install required dependencies
echo "Installing dependencies..."
pip install requests beautifulsoup4

# Check if the original plugin file exists
if [ ! -f "ecoledirecte_homework_plugin.py" ]; then
    echo "Error: ecoledirecte_homework_plugin.py not found in current directory"
    echo "Please make sure this file is in the same directory as the MCP server script"
    exit 1
fi

# Check if configuration file exists
if [ ! -f "ecoledirecte_2fa_data.json" ]; then
    echo "Warning: ecoledirecte_2fa_data.json not found"
    echo "Please create this file following the instructions in the original plugin"
    echo "The server will not work without this configuration file"
fi

# Make the MCP server script executable
chmod +x ecoledirecte_mcp_server.py

# Test the server
echo "Testing the MCP server..."
python3 ecoledirecte_mcp_server.py --help

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create your ecoledirecte_2fa_data.json file if you haven't already"
echo "2. Update your Claude Desktop configuration file (~/.config/claude-desktop/claude-desktop-config.json)"
echo "   Replace '/path/to/your/' with the actual path to ecoledirecte_mcp_server.py"
echo "3. Restart Claude Desktop"
echo "4. You should now be able to ask Claude about homework and messages from EcoleDirecte"

echo ""
echo "Example configuration for Claude Desktop:"
echo "{"
echo '  "mcpServers": {'
echo '    "ecoledirecte": {'
echo '      "command": "python3",'
echo '      "args": ["'$(pwd)'/ecoledirecte_mcp_server.py"],'
echo '      "env": {}'
echo '    }'
echo '  }'
echo "}"