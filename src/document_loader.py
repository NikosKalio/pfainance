from langchain_docling import DoclingLoader
import os

path = "data/raw/PDF document-B09AE98E4A67-1.pdf"
output_path = "data/processed/output.md"

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

loader = DoclingLoader(path)

docs = loader.load()

# Save document as Markdown
def save_as_markdown(documents, output_file):
    """
    Save documents to a Markdown file
    
    Args:
        documents: The loaded documents (typically a list of Document objects)
        output_file: Path to save the Markdown file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, doc in enumerate(documents):
            # Most document loaders create Document objects with page_content
            content = getattr(doc, 'page_content', str(doc))
            
            # Add page/document separator if multiple documents
            if i > 0:
                f.write("\n\n---\n\n")
                
            f.write(content)
    
    print(f"Document saved as Markdown at: {output_file}")

# Save the document
save_as_markdown(docs, output_path)

print(f"Loaded documents: {docs}")