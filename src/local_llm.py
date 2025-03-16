from langchain_ollama.llms import OllamaLLM
from src.models import Institution, Account, Transaction,  AccountType, TransactionType, InstitutionType, TransactionParser
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import ExperimentalMarkdownSyntaxTextSplitter
from langchain_text_splitters import CharacterTextSplitter

from pydantic_ai import Agent, ModelRetry, UnexpectedModelBehavior, capture_run_messages
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from typing import List


def transaction_from_chunk(chunk: str) -> List[TransactionParser]:
    ollama_model = OpenAIModel(
        model_name="mistral", provider=OpenAIProvider(base_url="http://localhost:11434/v1")
    )
    
    # Create the agent with increased retries
    agent = Agent(ollama_model, result_type=List[TransactionParser])
    
    # Use capture_run_messages to see the full conversation
    with capture_run_messages() as messages:
        try:
            result = agent.run_sync(f"""
            Analyze this transaction data and extract the transactions:
            
            {chunk}
            
            For each transaction, extract:
            - amount: the numerical amount (should be a float like -7.00)
            - description: the transaction description as a string
            - date: the date in YYYY-MM-DD format (e.g., 2025-03-09)
            
            Format each transaction as a valid JSON object.
            If any information is missing, you can use null.
            """)
            print(result.usage())
            return result
        except UnexpectedModelBehavior as e:
            # Print the error
            print(f"Validation Error: {e}")
            
            # Print the captured messages to see the conversation
            print("\n=== Model Conversation ===")
            for msg in messages:
                print(f"[{msg['role']}]: {msg['content']}")
            
            # Return an empty list as fallback
            return []






def process_doc_with_llm(markdown_doc: str):
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
        for tokens in llm.stream(f"if you see transactions, comment if they were wise or not in a sassy drag queen way: {chunk}"):
            print(tokens, end="", flush=True)
        print()  # Add a newline at the end
        print("--------------------------------")

#TODO write functions to structure document data into db writes - each doc is from one account and one insitution and has many transactions.
 # pydantic AI agnet? #TODO needs to check if the query is written before sending it to the LLM.
#TODO once raw data is in db, then do the analysis. 
#TODO? sometimes I don't udnerstands the terms of the bank. do need to keep anything else apart from what is written in the db?


#writes transactions, 

if __name__ == "__main__":
    chunk="""PDF export is limited to 500 account transactions.

| Trade date Booking date   | Description                                 | Debit   | Credit   | Value date   | Balance   |
|---------------------------|---------------------------------------------|---------|----------|--------------|-----------|
|                           | Closing balance                             |         |          |              | 7,157.02  |
| 09.03.2025 10.03.2025     | COOP-1511 ZH STADELHOFEN; Payment UBS TWINT | -19.25  |          | 09.03.2025   | 7,157.02  |
| 09.03.2025 10.03.2025     | COOP-5725 ZH AIRPORT S.; Payment UBS TWINT  | -8.60   |          | 09.03.2025   | 7,176.27  |
| 09.03.2025 10.03.2025     | SBB MOBILE; Payment UBS TWINT               | -7.00   |          | 09.03.2025   | 7,184.87  |
| 09.03.2025 10.03.2025     | SBB MOBILE; Payment UBS TWINT               | -7.00   |          | 09.03.2025   | 7,191.87  |
| 09.03.2025 10.03.2025     | SBB MOBILE; Payment UBS TWINT               | -3.50   |          | 09.03.2025   | 7,198.87  |
| 09.03.2025 10.03.2025     | SBB Mobile                                  |         | 3.50     | 09.03.2025   | 7,202.37  |
| 08.03.2025 10.03.2025     | MIGROS ONLINE SA; Payment UBS TWINT         | -162.70 |          | 08.03.2025   | 7,198.87  |
| 07.03.2025 07.03.2025     | SBB MOBILE; Payment UBS TWINT               | -17.80  |          | 07.03.2025   | 7,361.57  |
| 07.03.2025 07.03.2025     | SBB MOBILE; Payment UBS TWINT               | -7.80   |          | 07.03.2025   | 7,379.37  |
"""
    print(transaction_from_chunk(chunk))


