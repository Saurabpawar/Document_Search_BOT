# chroma_delete.py

# Function to delete file from Chroma Vector Store
def delete_file_from_vector_store(vector_store, filename):
    try:
        # Fetch the documents to delete based on the filename
        matching_docs = vector_store.get(where={"filename": filename})
        
        if matching_docs and 'documents' in matching_docs:
            # Perform the deletion
            vector_store.delete(where={"filename": filename})
            vector_store.persist()
            return True
        else:
            raise Exception("No documents with the given filename found in Chroma.")
    except Exception as e:
        print(f"[ERROR] Error deleting file from Chroma: {e}")
        raise e
