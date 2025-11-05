#!/usr/bin/env python3
"""
Test script to verify the MCP server is working correctly.
This simulates how the MCP client would interact with the server.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path to import the server module
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_dynamodb_user_server.server import app


async def test_list_tools():
    """Test listing available tools."""
    print("=" * 60)
    print("Testing: List Tools")
    print("=" * 60)

    tools = await app._request_handlers["/tools/list"]()

    print(f"\nFound {len(tools['tools'])} tool(s):")
    for tool in tools['tools']:
        print(f"\n  Name: {tool['name']}")
        print(f"  Description: {tool['description']}")
        print(f"  Input Schema: {json.dumps(tool['inputSchema'], indent=4)}")

    return tools


async def test_get_user(user_id: str):
    """Test the get_user tool."""
    print("\n" + "=" * 60)
    print(f"Testing: Get User (userId={user_id})")
    print("=" * 60)

    try:
        result = await app._request_handlers["/tools/call"](
            name="get_user",
            arguments={"userId": user_id}
        )

        print(f"\nResult:")
        for content in result:
            print(content.text)

        return result
    except Exception as e:
        print(f"\nError: {e}")
        return None


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MCP DynamoDB User Server - Test Suite")
    print("=" * 60)

    # Test 1: List tools
    await test_list_tools()

    # Test 2: Get existing user (if exists)
    await test_get_user("user123")

    # Test 3: Get non-existent user
    await test_get_user("nonexistent-user")

    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)
    print("\nNotes:")
    print("- If you see 'User not found' errors, make sure you have:")
    print("  1. Created a DynamoDB table named 'users' (or set DYNAMODB_TABLE_NAME)")
    print("  2. Added test data to the table")
    print("  3. Configured AWS credentials")
    print("- Run 'python test/setup_test_data.py' to create test data")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
