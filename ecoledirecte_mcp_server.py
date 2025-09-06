#!/usr/bin/env python3

"""
EcoleDirecte MCP Server using FastMCP
Provides homework and messages functionality from www.ecoledirecte.com
"""

import json
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any, List
import asyncio

# Add the directory containing the original plugin to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from fastmcp import FastMCP
except ImportError:
    print("FastMCP not installed. Install with: pip install fastmcp")
    sys.exit(1)

# Import the original plugin classes
try:
    from ecoledirecte_homework_plugin import EcoleDirecteHomeworkPlugin, EcoleDirecteMessagesPlugin
except ImportError:
    print("Could not import EcoleDirecte plugins. Make sure ecoledirecte_homework_plugin.py is in the same directory.")
    sys.exit(1)

# Initialize FastMCP server
mcp = FastMCP("EcoleDirecte Server")

# Global plugin instances
homework_plugin = None
messages_plugin = None

def initialize_plugins():
    """Initialize the plugin instances"""
    global homework_plugin, messages_plugin
    try:
        homework_plugin = EcoleDirecteHomeworkPlugin()
        messages_plugin = EcoleDirecteMessagesPlugin()
        return True
    except Exception as e:
        print(f"Failed to initialize plugins: {e}")
        return False

@mcp.tool()
def get_homework(kid_name: Optional[str] = None) -> str:
    """
    Retrieve homework for a specified child or for all children if no name is provided.
    
    Args:
        kid_name: The name of the child (optional). If not provided, returns homework for all children.
        
    Returns:
        JSON string containing homework data
    """
    if homework_plugin is None:
        return json.dumps({"error": "Homework plugin not initialized"})
    
    try:
        result = homework_plugin.get_homework_from_ecoledirecte(kid_name)
        return result if isinstance(result, str) else json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve homework: {str(e)}"})

@mcp.tool()
def get_messages(kid_name: Optional[str] = None, latest_n: int = 5) -> str:
    """
    Retrieve the latest messages for a specified child or for all children if no name is provided.
    
    Args:
        kid_name: The name of the child (optional). If not provided, returns messages for all children.
        latest_n: The number of latest messages to retrieve (default is 5).
        
    Returns:
        JSON string containing message data
    """
    if messages_plugin is None:
        return json.dumps({"error": "Messages plugin not initialized"})
    
    try:
        result = messages_plugin.get_messages_from_ecoledirecte(kid_name, latest_n)
        return result if isinstance(result, str) else json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve messages: {str(e)}"})

@mcp.tool()
def get_available_children() -> str:
    """
    Get the list of available children names from the configuration.
    
    Returns:
        JSON string containing the list of children names
    """
    if homework_plugin is None:
        return json.dumps({"error": "Plugin not initialized"})
    
    try:
        children_names = list(homework_plugin.students.values())
        return json.dumps({"children": children_names})
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve children list: {str(e)}"})

@mcp.tool()
def server_status() -> str:
    """
    Check the server status and configuration.
    
    Returns:
        JSON string containing server status information
    """
    status = {
        "server": "EcoleDirecte MCP Server",
        "status": "running",
        "plugins_initialized": homework_plugin is not None and messages_plugin is not None,
        "config_file_exists": os.path.exists(os.path.join(current_dir, 'ecoledirecte_2fa_data.json')),
        "timestamp": datetime.now().isoformat()
    }
    
    if homework_plugin:
        try:
            status["available_children"] = list(homework_plugin.students.values())
        except:
            status["available_children"] = []
    
    return json.dumps(status, indent=2)

def main():
    """Main entry point for the MCP server"""
    print("Starting EcoleDirecte MCP Server...")
    
    # Check for configuration file
    config_file = os.path.join(current_dir, 'ecoledirecte_2fa_data.json')
    if not os.path.exists(config_file):
        print(f"Error: Configuration file 'ecoledirecte_2fa_data.json' not found in {current_dir}")
        print("Please create this file following the instructions in the original plugin.")
        sys.exit(1)
    
    # Initialize plugins
    if not initialize_plugins():
        print("Failed to initialize plugins. Check your configuration.")
        sys.exit(1)
    
    print("Plugins initialized successfully")
    print(f"Available children: {list(homework_plugin.students.values())}")
    print("Server ready to handle requests...")
    
    # Run the MCP server
    mcp.run()

if __name__ == "__main__":
    main()