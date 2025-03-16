from docling.document_converter import DocumentConverter
import os


def convert_pdf_to_markdown(source_path: str, output_path: str) -> None:
    """
    Convert a PDF document to Markdown format and save it to a file.
    
    Args:
        source_path (str): Path to the source PDF file
        output_path (str): Path where to save the markdown output
    """
    # Initialize converter
    converter = DocumentConverter()
    
    # Convert the document
    result = converter.convert(source_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the markdown content to the file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result.document.export_to_markdown())
    
    print(f"Document saved as Markdown at: {output_path}")

#TODO process csvs
if __name__ == "__main__":
    source = "data/raw/PDF document-B09AE98E4A67-1.pdf"
    output_path = "data/processed/UBS_checking.md"
    convert_pdf_to_markdown(source, output_path)

# output: ## Docling Technical Report [...]"