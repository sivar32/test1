#!/usr/bin/env python3
"""MCP server for retrieving user information from DynamoDB."""

import os
import json
import asyncio
from typing import Any
import boto3
from botocore.exceptions import ClientError

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Initialize DynamoDB client
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "users")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

# Create server instance
app = Server("mcp-dynamodb-user-server")


@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_user",
            description="Retrieve user information from DynamoDB users table by user ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "userId": {
                        "type": "string",
                        "description": "The unique identifier for the user",
                    },
                },
                "required": ["userId"],
            },
        )
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool execution requests."""
    if name == "get_user":
        user_id = arguments.get("userId")

        if not user_id:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "userId is required"
                    }, indent=2)
                )
            ]

        try:
            response = table.get_item(Key={"userId": user_id})

            if "Item" not in response:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "User not found",
                            "userId": user_id
                        }, indent=2)
                    )
                ]

            return [
                TextContent(
                    type="text",
                    text=json.dumps(response["Item"], indent=2, default=str)
                )
            ]

        except ClientError as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Failed to retrieve user",
                        "message": str(e)
                    }, indent=2)
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Unexpected error",
                        "message": str(e)
                    }, indent=2)
                )
            ]

    raise ValueError(f"Unknown tool: {name}")


async def run_server():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-dynamodb-user-server",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    """Main entry point for the server."""
    import sys

    # Log to stderr since stdout is used for MCP communication
    print("MCP DynamoDB User Server starting...", file=sys.stderr)

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nServer stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
