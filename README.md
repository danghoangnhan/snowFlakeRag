# snowLakeRag# Snowflake Chatbot

 the Snowflake Chatbot application.

## Prerequisites

- Python 3.10
- pip (Python package installer)
- Git (for cloning the repository)

## System Requirements

- Operating System: Windows, macOS, or Linux
- Minimum RAM: 4GB (8GB recommended)
- Storage: At least 1GB of free space

## Installation Steps

### 1. Python Installation

First, ensure you have Python 3.10 installed:

```bash
python3 --version
```

If Python 3.10 is not installed, download it from:
[Python Official Website](https://www.python.org/downloads/)

### 2. Create and Activate Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python3.10 -m venv snowflake-env

# Activate virtual environment
# For Windows:
snowflake-env\Scripts\activate
# For Unix or MacOS:
source snowflake-env/bin/activate
```

### 3. Install Required Packages

Install all required packages using the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 4. Configure Snowflake Credentials

Create a configuration file named `dev.env` with your Snowflake credentials:

```json
{
    "account": "your_account",
    "username": "your_username",
    "password": "your_password",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema"
}
```

### 5. Running the Application

Start the Streamlit application:

```bash
streamlit run streamlit.py
```

The application will be accessible at:

- Local URL: http://localhost:8501
- Network URL: http://your-ip-address:8501

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are correctly installed:

```bash
pip list
```

2. Verify Python version:

```bash
python3 --version
```

3. Check Snowflake connectivity:

```bash
python3 -c "import snowflake.connector"
```

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Snowflake Python Connector Documentation](https://docs.snowflake.com/en/user-guide/python-connector.html)
- [Snowpark Python API Documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/index.html)