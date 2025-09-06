# EcoleDirecte MCP Server

A Model Context Protocol (MCP) server that integrates with Claude Desktop to retrieve homework assignments and messages from the French educational platform EcoleDirecte (www.ecoledirecte.com).

## Features

- 📚 **Homework Retrieval**: Get upcoming homework assignments for your children
- 📧 **Messages**: Retrieve the latest messages from school
- 👨‍👩‍👧‍👦 **Multi-Child Support**: Handle multiple children in the same family account
- 🔐 **Secure Authentication**: Uses EcoleDirecte's 2FA system
- 🤖 **Claude Integration**: Works seamlessly with Claude Desktop

## Prerequisites

- Python 3.7 or higher
- Active EcoleDirecte account with parent access
- Claude Desktop application

## Installation

1. **Clone or download the files** to a directory of your choice:
   ```bash
   mkdir ecoledirecte-mcp
   cd ecoledirecte-mcp
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   This will install all required dependencies:
   - `fastmcp`
   - `requests`
   - `beautifulsoup4`

## Configuration

### Step 1: Create the Authentication File

Create a file named `ecoledirecte_2fa_data.json` in the same directory as the MCP server script. This file contains your EcoleDirecte credentials and 2FA information.

#### Basic Structure

```json
[
    {
        "students": {
            "12345": "Child Name 1",
            "67890": "Child Name 2"
        },
        "student_ids": [
            "12345"
        ],
        "linked_accounts": [
            {
                "student_ids": [
                    "67890"
                ],
                "identifiant": "linked_parent_account_email@example.com"
            }
        ],
        "identifiant": "your_parent_account_email@example.com",
        "motdepasse": "your_password",
        "isReLogin": false,
        "uuid": "",
        "fa": [
            {
                "cn": "your_2fa_code_name",
                "cv": "your_2fa_code_value"
            }
        ]
    }
]
```

### Step 2: Get Your 2FA Authentication Data

The most critical part is obtaining the `fa` (two-factor authentication) data. You must extract this from your browser after logging into EcoleDirecte:

#### Instructions for Chrome/Edge:

1. **Open EcoleDirecte in your browser**:
   - Navigate to [https://www.ecoledirecte.com](https://www.ecoledirecte.com)

2. **Open Developer Tools**:
   - Press `F12` or right-click and select "Inspect"

3. **Log into your account**:
   - Enter your credentials and complete the 2FA process
   - **Important**: You must complete the full login process including 2FA

4. **Access Local Storage**:
   - In Developer Tools, go to the **Application** tab
   - In the left sidebar, expand **Storage** → **Local Storage**
   - Click on `https://www.ecoledirecte.com`

5. **Find the `fa` key**:
   - Look for a key named `fa` in the list
   - Right-click on the `fa` key and select "Copy value"

6. **Extract the values**:
   The copied value will look something like:
   ```json
   [{"cn":"device_fingerprint","cv":"abc123def456..."}]
   ```
   
   Copy the `cn` and `cv` values into your configuration file.

#### Instructions for Firefox:

1. Open EcoleDirecte and complete the login process
2. Press `F12` to open Developer Tools
3. Go to the **Storage** tab
4. Click on **Local Storage** → `https://www.ecoledirecte.com`
5. Find the `fa` key and copy its value
6. Extract the `cn` and `cv` values as described above

### Step 3: Fill in Your Configuration

1. **Get Student IDs**:
   - After logging into EcoleDirecte, the student IDs can be found in the URL when viewing a student's information
   - Or check the browser's network tab for API calls containing student IDs

2. **Complete the configuration file**:
   ```json
   [
       {
           "students": {
               "YOUR_STUDENT_ID_1": "First Child Name",
               "YOUR_STUDENT_ID_2": "Second Child Name"
           },
           "student_ids": [
               "YOUR_STUDENT_ID_1"
           ],
           "linked_accounts": [
               {
                   "student_ids": [
                       "YOUR_STUDENT_ID_2"
                   ],
                   "identifiant": "second_parent_email@example.com"
               }
           ],
           "identifiant": "your_email@example.com",
           "motdepasse": "your_password",
           "isReLogin": false,
           "uuid": "",
           "fa": [
               {
                   "cn": "your_extracted_cn_value",
                   "cv": "your_extracted_cv_value"
               }
           ]
       }
   ]
   ```

### Configuration Examples

#### Single Parent, One Child:
```json
[
    {
        "students": {
            "12345": "Marie Dupont"
        },
        "student_ids": [
            "12345"
        ],
        "linked_accounts": [],
        "identifiant": "parent@example.com",
        "motdepasse": "mypassword123",
        "isReLogin": false,
        "uuid": "",
        "fa": [
            {
                "cn": "device_fingerprint",
                "cv": "abc123def456xyz789"
            }
        ]
    }
]
```

#### Two Parents, Multiple Children:
```json
[
    {
        "students": {
            "12345": "Marie Dupont",
            "67890": "Paul Dupont"
        },
        "student_ids": [
            "12345"
        ],
        "linked_accounts": [
            {
                "student_ids": [
                    "67890"
                ],
                "identifiant": "parent2@example.com"
            }
        ],
        "identifiant": "parent1@example.com",
        "motdepasse": "mypassword123",
        "isReLogin": false,
        "uuid": "",
        "fa": [
            {
                "cn": "device_fingerprint",
                "cv": "abc123def456xyz789"
            }
        ]
    }
]
```

## Claude Desktop Integration

### Step 1: Update Claude Desktop Configuration

Edit your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude-desktop-config.json`
**Windows**: `%APPDATA%\Claude\claude-desktop-config.json`
**Linux**: `~/.config/claude-desktop/claude-desktop-config.json`

Add the EcoleDirecte MCP server:

```json
{
  "mcpServers": {
    "ecoledirecte": {
      "command": "python3",
      "args": ["/full/path/to/your/ecoledirecte_mcp_server.py"],
      "env": {}
    }
  }
}
```

**Important**: Replace `/full/path/to/your/` with the actual full path to your `ecoledirecte_mcp_server.py` file.

### Step 2: Restart Claude Desktop

Close and restart Claude Desktop for the changes to take effect.

## Usage

Once configured, you can interact with the EcoleDirecte data through Claude Desktop:

### Available Commands

#### Get Homework
```
What homework does Marie have?
Show me all upcoming homework assignments
Get homework for all my children
```

#### Get Messages  
```
Are there any new messages from school?
Show me the latest 3 messages for Paul
Get all recent messages from EcoleDirecte
```

#### Server Status
```
Check the EcoleDirecte server status
What children are available in the system?
```

### Example Conversations

**User**: "What homework does my daughter have this week?"
**Claude**: *Retrieves and displays upcoming homework assignments with due dates, subjects, and descriptions*

**User**: "Are there any new messages from the school?"
**Claude**: *Shows recent messages from teachers and administrators with subjects and content*

## Available MCP Tools

The server provides these tools to Claude:

1. **`get_homework`** - Retrieve homework for a specific child or all children
2. **`get_messages`** - Get latest messages for a specific child or all children  
3. **`get_available_children`** - List all configured children
4. **`server_status`** - Check server status and configuration

## Troubleshooting

### Common Issues

1. **"Plugin not initialized" error**:
   - Check that `ecoledirecte_2fa_data.json` exists and is properly formatted
   - Verify your credentials are correct

2. **Authentication failures**:
   - Your 2FA data may have expired - re-extract the `fa` values from your browser
   - Check that your password is correct

3. **"No homework found"**:
   - This is normal if there are no upcoming assignments
   - The plugin automatically filters out overdue homework

4. **MCP server not connecting**:
   - Verify the path in your Claude Desktop configuration is correct
   - Check that Python and all dependencies are installed
   - Look at the Claude Desktop logs for error messages

### Updating 2FA Data

The `fa` authentication data expires periodically. When you start getting authentication errors:

1. Log into EcoleDirecte in your browser again
2. Complete the 2FA process
3. Extract the new `fa` values from Local Storage
4. Update your `ecoledirecte_2fa_data.json` file
5. Restart the MCP server (restart Claude Desktop)

### Testing the Server

You can test the MCP server directly:

```bash
python3 ecoledirecte_mcp_server.py
```

This will show any configuration errors and confirm the server can start properly.

## Security Notes

- Keep your `ecoledirecte_2fa_data.json` file secure - it contains your login credentials
- Don't share this file or commit it to version control
- The 2FA tokens expire and need periodic renewal
- Consider setting appropriate file permissions: `chmod 600 ecoledirecte_2fa_data.json`

## File Structure

```
ecoledirecte-mcp/
├── ecoledirecte_mcp_server.py      # Main MCP server
├── ecoledirecte_homework_plugin.py  # Original plugin (required)
├── ecoledirecte_2fa_data.json      # Your credentials (you create this)
├── setup.sh                       # Setup script
└── README.md                      # This file
```

## Support

This is an unofficial integration with EcoleDirecte. If you encounter issues:

1. Check the troubleshooting section above
2. Verify your EcoleDirecte account works normally in the web browser
3. Ensure all file paths and configurations are correct
4. Check Python and dependency versions

## License

This project is provided as-is for educational and personal use. Please respect EcoleDirecte's terms of service when using this integration.