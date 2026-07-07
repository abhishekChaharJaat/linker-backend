def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc.get("_id"):
        doc["_id"] = str(doc["_id"])
    if doc.get("created_at"):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc
