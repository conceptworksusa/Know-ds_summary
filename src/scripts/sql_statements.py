
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


#
def fetch_top_chunks_batch(self, doc_id, query_embeddings, top_n=3, threshold=0.5):
    """
    Fetch top-N chunks for a list of query embeddings from a given doc_id.

    :param doc_id: document id to filter
    :param query_embeddings: list of embeddings (list of list/array)
    :param top_n: number of top matches per query
    :param threshold: similarity threshold
    """

    # Build VALUES dynamically
    values_sql = []
    params = []
    for i, emb in enumerate(query_embeddings, start=1):
        values_sql.append(f"(%s, %s::vector)")
        params.extend([i, emb])  # query_id + embedding

    values_sql = ", ".join(values_sql)

    query = f"""
    WITH queries AS (
        SELECT * FROM (VALUES {values_sql}) AS q(query_id, query_embedding)
    )
    SELECT 
        q.query_id,
        c.chunk_id,
        c.chunk,
        1 - (c.embeddings <=> q.query_embedding) AS similarity
    FROM queries q
    JOIN LATERAL (
        SELECT chunk_id, chunk, embeddings
        FROM claimbrain.document_embeddings c
        WHERE c.doc_id = %s
          AND (1 - (c.embeddings <=> q.query_embedding)) >= %s
        ORDER BY (1 - (c.embeddings <=> q.query_embedding)) DESC
        LIMIT %s
    ) c ON true
    ORDER BY q.query_id, similarity DESC;
    """

    # Add common params (doc_id, threshold, top_n) at the end
    params.extend([doc_id, threshold, top_n])

    # Execute query
    self.cursor.execute(query, params)
    results = self.cursor.fetchall()
    return results

