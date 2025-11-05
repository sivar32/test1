#!/usr/bin/env python3
"""
Setup script to create a test DynamoDB table and populate it with sample data.
"""

import os
import sys
import boto3
from botocore.exceptions import ClientError

# Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "users")


def create_table():
    """Create the DynamoDB users table."""
    dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)

    print(f"Creating table '{TABLE_NAME}' in region '{AWS_REGION}'...")

    try:
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "userId", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "userId", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        print(f"✓ Table creation initiated. Status: {response['TableDescription']['TableStatus']}")
        print("  Waiting for table to become active...")

        # Wait for table to be created
        waiter = dynamodb.get_waiter("table_exists")
        waiter.wait(TableName=TABLE_NAME)

        print(f"✓ Table '{TABLE_NAME}' is now active!")
        return True

    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"✓ Table '{TABLE_NAME}' already exists.")
            return True
        else:
            print(f"✗ Error creating table: {e}")
            return False


def add_test_users():
    """Add sample users to the table."""
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(TABLE_NAME)

    test_users = [
        {
            "userId": "user123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "role": "admin",
            "createdAt": "2024-01-15T10:30:00Z",
            "isActive": True
        },
        {
            "userId": "user456",
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "role": "user",
            "createdAt": "2024-02-20T14:45:00Z",
            "isActive": True
        },
        {
            "userId": "user789",
            "name": "Bob Johnson",
            "email": "bob.johnson@example.com",
            "role": "user",
            "createdAt": "2024-03-10T09:15:00Z",
            "isActive": False
        }
    ]

    print(f"\nAdding {len(test_users)} test users to table...")

    for user in test_users:
        try:
            table.put_item(Item=user)
            print(f"✓ Added user: {user['userId']} ({user['name']})")
        except ClientError as e:
            print(f"✗ Error adding user {user['userId']}: {e}")

    print(f"\n✓ Test data setup complete!")


def verify_setup():
    """Verify the table and data."""
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(TABLE_NAME)

    print(f"\nVerifying setup...")
    print(f"Table name: {table.table_name}")
    print(f"Table status: {table.table_status}")
    print(f"Item count: {table.item_count}")

    # Try to read one user
    try:
        response = table.get_item(Key={"userId": "user123"})
        if "Item" in response:
            print(f"\n✓ Sample user retrieved successfully:")
            print(f"  {response['Item']}")
    except ClientError as e:
        print(f"✗ Error verifying data: {e}")


def main():
    """Main setup function."""
    print("=" * 60)
    print("MCP DynamoDB User Server - Test Data Setup")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  AWS Region: {AWS_REGION}")
    print(f"  Table Name: {TABLE_NAME}")
    print()

    # Check AWS credentials
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        print(f"AWS Identity:")
        print(f"  Account: {identity['Account']}")
        print(f"  ARN: {identity['Arn']}")
        print()
    except Exception as e:
        print(f"✗ Error: Unable to verify AWS credentials: {e}")
        print("\nPlease configure AWS credentials using one of these methods:")
        print("  1. AWS CLI: aws configure")
        print("  2. Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
        print("  3. IAM role (if running on EC2/ECS)")
        sys.exit(1)

    # Create table
    if not create_table():
        sys.exit(1)

    # Add test data
    add_test_users()

    # Verify setup
    verify_setup()

    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nYou can now test the MCP server with:")
    print("  python test/test_server.py")
    print("\nOr run the server directly:")
    print("  python -m mcp_dynamodb_user_server.server")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
