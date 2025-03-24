from langchain.text_splitter import RecursiveCharacterTextSplitter

# Function to split text into chunks
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)

