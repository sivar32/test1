# MCP DynamoDB User Server

A Model Context Protocol (MCP) server written in Python that provides a tool to retrieve user information from a DynamoDB users table.

## Features

- **get_user** tool: Retrieves user information from DynamoDB by user ID
- Built with Python and boto3
- Async/await support for better performance
- Comprehensive error handling

## Prerequisites

- Python 3.10 or higher
- AWS credentials configured
- A DynamoDB table for users

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install in development mode:
```bash
pip install -e .
```

## Configuration

The server uses the following environment variables:

- `AWS_REGION`: AWS region where your DynamoDB table is located (default: `us-east-1`)
- `DYNAMODB_TABLE_NAME`: Name of your DynamoDB users table (default: `users`)
- AWS credentials via standard boto3 methods (environment variables, AWS credentials file, or IAM role)

## DynamoDB Table Schema

The server expects a DynamoDB table with the following primary key:

- **Partition Key**: `userId` (String)

Example table structure:
```json
{
  "userId": "user123",
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

## Creating a Test Table

To create a test DynamoDB table:

```bash
aws dynamodb create-table \
  --table-name users \
  --attribute-definitions AttributeName=userId,AttributeType=S \
  --key-schema AttributeName=userId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

Add a test user:

```bash
aws dynamodb put-item \
  --table-name users \
  --item '{"userId": {"S": "user123"}, "name": {"S": "John Doe"}, "email": {"S": "john@example.com"}}' \
  --region us-east-1
```

## Usage

### Running directly

```bash
python -m mcp_dynamodb_user_server.server
```

Or if installed:
```bash
mcp-dynamodb-user-server
```

### Usage with Claude Desktop

Add this server to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "dynamodb-users": {
      "command": "python",
      "args": ["-m", "mcp_dynamodb_user_server.server"],
      "cwd": "/path/to/mcp-dynamodb-user-server",
      "env": {
        "AWS_REGION": "us-east-1",
        "DYNAMODB_TABLE_NAME": "users"
      }
    }
  }
}
```

Replace `/path/to/mcp-dynamodb-user-server` with the actual path to this directory.

**Alternative using virtual environment:**

```json
{
  "mcpServers": {
    "dynamodb-users": {
      "command": "/path/to/mcp-dynamodb-user-server/venv/bin/python",
      "args": ["-m", "mcp_dynamodb_user_server.server"],
      "env": {
        "AWS_REGION": "us-east-1",
        "DYNAMODB_TABLE_NAME": "users"
      }
    }
  }
}
```

## Available Tools

### get_user

Retrieves user information from the DynamoDB users table.

**Parameters:**
- `userId` (string, required): The unique identifier for the user

**Example:**
```json
{
  "userId": "user123"
}
```

**Response:**
Returns the complete user object from DynamoDB, or an error if the user is not found.

**Success response:**
```json
{
  "userId": "user123",
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

**Error response (user not found):**
```json
{
  "error": "User not found",
  "userId": "user123"
}
```

## AWS Permissions

The AWS credentials used must have the following DynamoDB permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/users"
    }
  ]
}
```

## Development

### Running tests

```bash
pytest
```

### Code formatting

```bash
black mcp_dynamodb_user_server/
```

## Troubleshooting

- **Connection errors**: Ensure AWS credentials are properly configured. Test with `aws sts get-caller-identity`
- **Table not found**: Verify the `DYNAMODB_TABLE_NAME` environment variable and that the table exists
- **Access denied**: Check that your AWS credentials have the necessary DynamoDB permissions
- **User not found**: Returns a JSON response with an error message if the userId doesn't exist in the table
- **Import errors**: Make sure you've activated your virtual environment and installed dependencies

## Project Structure

```
mcp-dynamodb-user-server/
├── mcp_dynamodb_user_server/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── pyproject.toml         # Project metadata and dependencies
├── requirements.txt       # Direct dependencies
├── README.md             # This file
└── .gitignore            # Git ignore patterns
```

## License

MIT
