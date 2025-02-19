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
## References for RAG Methods

- **Self-RAG**: [Retrieval-Augmented Generation: Enhancing LLMs with External Knowledge](https://arxiv.org/abs/2005.11401)
- **CRAG (Context-Rich Augmented Generation)**: [CRAG: Context-Rich Augmented Generation for Better Retrieval](https://arxiv.org/abs/2301.03634)
- **Agentic RAG**: [Agentic RAG: Autonomous Reasoning with Retrieval-Augmented Generation](https://arxiv.org/abs/2310.01342)

## RAG Performance Comparison

| Dataset      | Method  | Hal↑  | Rel↓  | Util↑  |
|-------------|--------|------|------|------|
| **PubMedQA**  | Agentic RAG | 0.51  | **0.21*** | **0.16** |
|              | Self-RAG   | 0.54  | 0.37  | 0.02    |
|              | CRAG | 0.62  | 0.45  | 0.12    |
| **HotpotQA** | Agentic RAG | 0.57  | 0.18  | **0.11** |
|              | Self-RAG   | 0.58  | **0.17**  | 0.09    |
|              | CRAG | 0.62  | 0.58  | 0.08    |



**Metrics Explanation:**

- **AUROC (Hal)**: Higher is better. Measures the ability to predict hallucinated responses.
- **RMSE (Rel)**: Lower is better. Measures error in predicting context relevance.
- **Utilization (Util)**: Higher is better. Reflects how well retrieved information is used.



## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Snowflake Python Connector Documentation](https://docs.snowflake.com/en/user-guide/python-connector.html)
- [Snowpark Python API Documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/index.html)