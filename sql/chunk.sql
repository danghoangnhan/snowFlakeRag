/*
    File: create_docs_chunks_table.sql
    Description: Creates a table to store chunked content from PDF documents
    Created: 2024-11-25
    
    This table is designed to store processed chunks of text from PDF documents
    along with their metadata for document retrieval and processing purposes.
    
    Table: DOCS_CHUNKS_TABLE
    Purpose: Stores segmented text content from PDF documents along with associated metadata
    for efficient document management and retrieval.
    
    Column Details:
    - RELATIVE_PATH: Stores the relative file path to the PDF document
    - SIZE: Records the file size of the PDF document
    - FILE_URL: Stores the complete URL to access the PDF
    - SCOPED_FILE_URL: Stores a scoped/temporary URL for restricted access
    - CHUNK: Contains the actual text segment from the PDF
    - CATEGORY: Stores the document classification for filtering purposes
    
    Usage Notes:
    - Ensure proper indexing based on your query patterns
    - Consider partitioning for large datasets
    - Monitor CHUNK column usage as it stores large text data
*/

-- Drop existing table if it exists to ensure clean creation
DROP TABLE IF EXISTS DOCS_CHUNKS_TABLE;

-- Create the table with comprehensive column definitions
CREATE OR REPLACE TABLE DOCS_CHUNKS_TABLE (
    RELATIVE_PATH VARCHAR(16777216) COMMENT 'Relative path to the PDF file within the storage system',
    
    SIZE NUMBER(38,0) COMMENT 'Size of the PDF file in bytes',
    
    FILE_URL VARCHAR(16777216) COMMENT 'Complete URL to access the PDF file',
    
    SCOPED_FILE_URL VARCHAR(16777216) COMMENT 'Temporary or scoped URL for restricted access to the PDF',
    
    CHUNK VARCHAR(16777216) COMMENT 'Extracted text segment from the PDF document',
    
    CATEGORY VARCHAR(16777216) COMMENT 'Document classification category for filtering and organization'
);


-- insert into DOCS_CHUNKS_TABLE (relative_path, size, file_url,
--                             scoped_file_url, chunk)

--     select relative_path, 
--             size,
--             file_url, 
--             build_scoped_file_url(@docs, relative_path) as scoped_file_url,
--             func.chunk as chunk
--     from 
--         directory(@docs),
--         TABLE(text_chunker (TO_VARCHAR(SNOWFLAKE.CORTEX.PARSE_DOCUMENT(@docs, 
--                               relative_path, {'mode': 'LAYOUT'})))) as func;