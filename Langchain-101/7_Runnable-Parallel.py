import os
import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnableSequence, RunnableParallel

load_dotenv(verbose=True)

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

print("======= Chat Prompt Template =======")

chat_prompt_template = ChatPromptTemplate([
    SystemMessage(content="You are expert in reviewing product."),
    ("human", "List the main features of the product {product_name}.")
])


# Define pros analysis step
def analyze_pros_prompt(features):
    pros_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert product reviewer."),
            (
                "human",
                "Given these features: {features}, list the pros of these features.",
            ),
        ]
    )
    return pros_template.format_prompt(features=features)


# Define cons analysis step
def analyze_cons_prompt(features):
    cons_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert product reviewer."),
            (
                "human",
                "Given these features: {features}, list the cons of these features.",
            ),
        ]
    )
    return cons_template.format_prompt(features=features)


# Combine pros and cons into a final review
def combine_pros_cons(pros, cons):
    return f"Pros:\n{pros}\n\nCons:\n{cons}"


# Simplify branches with LCEL
pros_branch_chain = RunnableLambda(analyze_pros_prompt) | model | StrOutputParser()

cons_branch_chain = RunnableLambda(analyze_cons_prompt) | model | StrOutputParser()

chain = chat_prompt_template \
        | model \
        | StrOutputParser() \
        | RunnableParallel(branches={"pros": pros_branch_chain, "cons": cons_branch_chain}) \
        | RunnableLambda(lambda x: combine_pros_cons(x["branches"]["pros"], x["branches"]["cons"]))
response = chain.invoke({"product_name": "samsung s25 edge"})
print(response)
