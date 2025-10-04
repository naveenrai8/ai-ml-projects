import os
import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

load_dotenv(verbose=True)

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

print("======= Chat Prompt Template =======")

chat_prompt_template = ChatPromptTemplate([
    ("system", "You are an {animal} lover and {hateOrLove} cracking jokes on them"),
    ("user", "Tell me a joke about {animal}")
])

chain = chat_prompt_template | model
result = chain.invoke({"animal": "cats", "hateOrLove": "love"})
response = result.content
print(f"AI response: {response}")

print("======= Messages Placeholder =======")

chat_prompt_template = ChatPromptTemplate([
    ("system", "You are an {animal} lover and {hateOrLove} cracking jokes on them"),
    MessagesPlaceholder("human_messages")
])

chain = chat_prompt_template | model | StrOutputParser()
response = chain.invoke(
    {"animal": "cats",
     "hateOrLove": "hate",
     "human_messages": [HumanMessage(content="Tell me joke about it")]})
print(f"AI response: {response}")
