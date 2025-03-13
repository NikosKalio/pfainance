from docling.document_converter import DocumentConverter

source = "data/raw/PDF document-B09AE98E4A67-1.pdf"
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())
# Save the markdown output to a file
output_path = "data/processed/output_docling.md"
import os

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write the markdown content to the file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(result.document.export_to_markdown())

print(f"Document saved as Markdown at: {output_path}")

# output: ## Docling Technical Report [...]"