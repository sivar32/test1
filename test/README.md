# Testing the MCP DynamoDB User Server

This directory contains scripts and configuration files to help you test the MCP server locally.

## Quick Start

### 1. Install Dependencies

First, make sure you're in the project root and have installed the dependencies:

```bash
cd /home/user/test1
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

Make sure you have AWS credentials configured. You can verify this with:

```bash
aws sts get-caller-identity
```

If not configured, run:

```bash
aws configure
```

Or set environment variables:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

### 3. Create Test Data

Run the setup script to create a DynamoDB table and populate it with test users:

```bash
python test/setup_test_data.py
```

This will:
- Create a `users` table in DynamoDB (if it doesn't exist)
- Add 3 test users: user123, user456, user789
- Verify the setup

### 4. Test the Server

Run the test script to verify the server is working:

```bash
python test/test_server.py
```

This will:
- List available tools (should show `get_user`)
- Test retrieving an existing user
- Test retrieving a non-existent user

## Test Files

### `setup_test_data.py`

Creates a DynamoDB table and populates it with sample users.

**Usage:**
```bash
python test/setup_test_data.py
```

**Environment Variables:**
- `AWS_REGION`: AWS region (default: us-east-1)
- `DYNAMODB_TABLE_NAME`: Table name (default: users)

**Sample users created:**
- `user123`: John Doe (admin, active)
- `user456`: Jane Smith (user, active)
- `user789`: Bob Johnson (user, inactive)

### `test_server.py`

Tests the MCP server by simulating tool calls.

**Usage:**
```bash
python test/test_server.py
```

**What it tests:**
- Listing available tools
- Getting an existing user (user123)
- Getting a non-existent user

### `claude_desktop_config.json`

Sample Claude Desktop configuration file showing how to integrate this MCP server.

**Usage:**

Copy the contents and add to your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

**Important:** Update the `cwd` path to match your actual project location!

## Running the Server Manually

To run the MCP server directly (for use with Claude Desktop or other MCP clients):

```bash
python -m mcp_dynamodb_user_server.server
```

The server will:
- Listen on stdio for MCP requests
- Log status messages to stderr
- Communicate with MCP clients via stdout

## Troubleshooting

### "No module named 'mcp'"

Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### "Unable to locate credentials"

Configure AWS credentials:
```bash
aws configure
```

Or set environment variables.

### "Table does not exist"

Run the setup script:
```bash
python test/setup_test_data.py
```

### "Access Denied" when creating table

Your AWS credentials need DynamoDB permissions. Add this IAM policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:CreateTable",
        "dynamodb:DescribeTable",
        "dynamodb:PutItem",
        "dynamodb:GetItem"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/users"
    }
  ]
}
```

## Manual Testing with AWS CLI

You can also test the DynamoDB table directly:

**Get a user:**
```bash
aws dynamodb get-item \
  --table-name users \
  --key '{"userId": {"S": "user123"}}' \
  --region us-east-1
```

**List all users:**
```bash
aws dynamodb scan \
  --table-name users \
  --region us-east-1
```

**Add a user:**
```bash
aws dynamodb put-item \
  --table-name users \
  --item '{"userId": {"S": "test999"}, "name": {"S": "Test User"}, "email": {"S": "test@example.com"}}' \
  --region us-east-1
```

## Next Steps

1. Test the server locally with `test_server.py`
2. Add the server to Claude Desktop using the sample config
3. Restart Claude Desktop
4. Try asking Claude to get user information:
   - "Can you get user information for user123?"
   - "Look up user456 in the database"
   - "What information do we have about user789?"

## Cleanup

To delete the test table and data:

```bash
aws dynamodb delete-table --table-name users --region us-east-1
```

**Warning:** This will permanently delete all data in the table!
