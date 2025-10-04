import os
import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

load_dotenv(verbose=True)

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

print("======= String Prompt Template =======")

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")
# input dictionary with key (inside template) and its value
user_filled_prompt = prompt_template.invoke({"topic": "cats"})
print(user_filled_prompt)

result = model.invoke(user_filled_prompt)
response = result.content
print(f"AI response: {response}")

print("======= Chat Prompt Template =======")

chat_prompt_template = ChatPromptTemplate([
    ("system", "You are an {animal} lover and {hateOrLove} cracking jokes on them"),
    ("user", "Tell me a joke about {animal}")
])

user_filled_prompt = chat_prompt_template.invoke({"animal": "cats", "hateOrLove": "love"})
print(user_filled_prompt)

result = model.invoke(user_filled_prompt)
response = result.content
print(f"AI response: {response}")

chat_prompt_template = ChatPromptTemplate([
    ("system", "You are an {animal} lover and {hateOrLove} cracking jokes on them"),
    ("user", "Tell me a joke about {animal}")
])

user_filled_prompt = chat_prompt_template.invoke({"animal": "cats", "hateOrLove": "hate"})
print(user_filled_prompt)

result = model.invoke(user_filled_prompt)
response = result.content
print(f"AI response: {response}")

print("======= Messages Placeholder =======")

chat_prompt_template = ChatPromptTemplate([
    ("system", "You are an {animal} lover and {hateOrLove} cracking jokes on them"),
    MessagesPlaceholder("human_messages")
])

user_filled_prompt = chat_prompt_template.invoke(
    {"animal": "cats",
     "hateOrLove": "hate",
     "human_messages": [HumanMessage(content="Tell me joke about it")]})
print(user_filled_prompt)
result = model.invoke(user_filled_prompt)
response = result.content
print(f"AI response: {response}")