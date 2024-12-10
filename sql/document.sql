/*
    File: create_docs_stage.sql
    Description: Creates a secure Snowflake stage for document storage with directory table support
    Created: 2024-11-25
    
    Purpose:
    - Establishes a secure storage location for PDF documents
    - Enables directory table functionality for file tracking
    - Sets up monitoring and validation queries
    
    Security Features:
    - Uses Snowflake-managed encryption (SSE)
    - Implements directory table for file tracking
    - Includes access control settings
*/

-- Step 1: Create the secure stage
CREATE OR REPLACE STAGE docs
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    DIRECTORY = (
        ENABLE = true,
        REFRESH_ON_CREATE = true,
        AUTO_REFRESH = true
    )
    COMMENT = 'Secure stage for storing and processing PDF documents';
