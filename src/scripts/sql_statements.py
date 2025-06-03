
GET_DOCUMENT_TEXT_BY_ID = "SELECT Text FROM Management.dbo.DocumentOcrBlock WHERE DocumentId = {doc_id};"

# Insert the summary into the DocumentSummaryBlock table
INSERT_SUMMARY = """
    INSERT INTO Management.dbo.DocumentSummary (DocumentId, SummaryText)
    VALUES ({doc_id}, '{summary}');
"""

# Check if the document exists in the DocumentSummary table
CHECK_IF_DOC_EXISTS = """
    SELECT COUNT(*) FROM Management.dbo.DocumentSummary WHERE DocumentId = {doc_id};
"""

# Update the summary into the DocumentSummary table
UPDATE_SUMMARY = """
    UPDATE Management.dbo.DocumentSummary
    
    SET SummaryText = '{summary}'
    WHERE DocumentId = {doc_id};
"""

# Update Document summary Id
UPDATE_SUMMARY_ID = """
    UPDATE Management.dbo.Document
    SET DocumentSummaryId = {summary_id}
    WHERE ParentDocumentId = {doc_id};  
"""

GET_LAST_INSERTED_SUMMARY_ID = """
    SELECT SCOPE_IDENTITY();
"""
