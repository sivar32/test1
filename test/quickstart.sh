#!/bin/bash
# Quick start script to set up and test the MCP DynamoDB User Server

set -e

echo "=========================================="
echo "MCP DynamoDB User Server - Quick Start"
echo "=========================================="
echo

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "Error: Please run this script from the project root directory"
    echo "Usage: bash test/quickstart.sh"
    exit 1
fi

# Step 1: Check Python
echo "1. Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "   ✓ Found: $PYTHON_VERSION"
echo

# Step 2: Create virtual environment
echo "2. Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
    echo "   ✓ Virtual environment created"
else
    echo "   ✓ Virtual environment already exists"
fi
echo

# Step 3: Activate virtual environment and install dependencies
echo "3. Installing dependencies..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "   ✓ Dependencies installed"
echo

# Step 4: Check AWS credentials
echo "4. Checking AWS credentials..."
if aws sts get-caller-identity &> /dev/null; then
    ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
    echo "   ✓ AWS credentials configured (Account: $ACCOUNT)"
else
    echo "   ✗ AWS credentials not found"
    echo
    echo "Please configure AWS credentials:"
    echo "  Option 1: Run 'aws configure'"
    echo "  Option 2: Set environment variables:"
    echo "    export AWS_ACCESS_KEY_ID='your-key'"
    echo "    export AWS_SECRET_ACCESS_KEY='your-secret'"
    echo "    export AWS_REGION='us-east-1'"
    exit 1
fi
echo

# Step 5: Setup test data
echo "5. Setting up test data in DynamoDB..."
if python test/setup_test_data.py; then
    echo "   ✓ Test data setup complete"
else
    echo "   ✗ Failed to setup test data"
    exit 1
fi
echo

# Step 6: Run tests
echo "6. Running tests..."
if python test/test_server.py; then
    echo "   ✓ Tests passed"
else
    echo "   ✗ Tests failed"
    exit 1
fi
echo

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo
echo "Next steps:"
echo "  1. Review test/claude_desktop_config.json"
echo "  2. Add the configuration to your Claude Desktop"
echo "  3. Update the 'cwd' path in the config"
echo "  4. Restart Claude Desktop"
echo
echo "To run the server manually:"
echo "  source venv/bin/activate"
echo "  python -m mcp_dynamodb_user_server.server"
echo
