import os
import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnableSequence

load_dotenv(verbose=True)

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

print("======= Chat Prompt Template =======")

chat_prompt_template = ChatPromptTemplate([
    ("system", "You are an {animal} lover and {hateOrLove} cracking jokes on them"),
    ("user", "Tell me a joke about {animal}")
])

first_task = RunnableLambda(lambda t: chat_prompt_template.format_prompt(**t))
second_task = RunnableLambda(lambda p: model.invoke(p.to_messages()))
third_task = RunnableLambda(lambda r: StrOutputParser().invoke(r))

chain = RunnableSequence(first_task, second_task, third_task)
response = chain.invoke({"animal": "cats", "hateOrLove": "love"})
print(response)
