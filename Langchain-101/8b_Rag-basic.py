import os

from langchain_community.vectorstores import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import OllamaEmbeddings, OllamaLLM

embedding_model = "mxbai-embed-large"
# Define the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(current_dir, "db", "chroma_db")
print(persistent_directory)
# Define the embedding model
embeddings = OllamaEmbeddings(model=embedding_model)

# Load the existing vector store with the embedding function
db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embeddings
)

# Define the user's question
query = "Who is Odysseus' wife?"

# Retrieve relevant documents based on the query
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.5},
)
relevant_docs = retriever.invoke(query)

# Display the relevant results with metadata
print("\n--- Relevant Documents ---")
for i, doc in enumerate(relevant_docs, 1):
    print(f"Document {i}:\n{doc.page_content}\n")
    if doc.metadata:
        print(f"Source: {doc.metadata.get('source', 'Unknown')}\n")

combined_input = (
    "Here are some documents that might help answer the question: "
    + query
    + "\n\nRelevant Documents:\n"
    + "\n\n".join([doc.page_content for doc in relevant_docs])
    + "\n\nPlease provide an answer based only on the provided documents. If the answer is not found in the documents, respond with 'I'm not sure'."
)

# query = "How did Juliet die?"

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content=combined_input),
]

llm_model = "gemma3:4b"
model = OllamaLLM(model=llm_model, verbose=True)
# Invoke the model with the combined input
result = model.invoke(messages)

# Display the full result and content only
print("\n--- Generated Response ---")
# print("Full result:")
# print(result)
print("Content only:")
print(result)