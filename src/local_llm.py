from langchain_ollama.llms import OllamaLLM
from src.models import Institution, Account, Transaction, OwnershipType, AccountType, TransactionType, InstitutionType
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import ExperimentalMarkdownSyntaxTextSplitter
from langchain_text_splitters import CharacterTextSplitter

def main():
    llm = OllamaLLM(model="mistral")

    # markdown_doc = open("data/processed/output_docling.md", "r").read() 
    # headers_to_split_on = [
    #     ("#", "Header 1"),
    #     ("##", "Header 2"),
    #     # You can add more header levels if needed
    #     # ("###", "Header 3"),
    # ]
    # splitter = ExperimentalMarkdownSyntaxTextSplitter(
    #     headers_to_split_on=headers_to_split_on
    # # )
    # chunks = splitter.split_text(markdown_doc)

    with open("data/processed/UBS_checking.md", "r") as file:
        markdown_doc = file.read()

    text_splitter = CharacterTextSplitter(
    separator="<!-- image -->",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
    )
    texts = text_splitter.create_documents([markdown_doc])
    print(texts[0])



    for index, chunk in enumerate(texts):
        print(f"Chunk {index + 1}:")
        print(chunk)
        print("--------------------------------")
        # Streaming generation
        for tokens in llm.stream(f"if you see transactions, comment if they were wise or not in a sassy gay way: {chunk}"):
            print(tokens, end="", flush=True)
        print()  # Add a newline at the end
        print("--------------------------------")

if __name__ == "__main__":
    main()