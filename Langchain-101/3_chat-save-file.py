import os
import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv(verbose=True)
# if not os.environ.get("GOOGLE_API_KEY"):
#     os.environ.setdefault("GOOGLE_API_KEY", "")
# os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

chat_history_file_path = "chat_history.json"
chat_history = FileChatMessageHistory(file_path=chat_history_file_path)

system_message = SystemMessage(content="You are very helpful AI assistant.")
chat_history.add_message(system_message)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    chat_history.add_user_message(user_input)
    result = model.invoke(chat_history.messages)
    response = result.content
    print(f"AI response: {response}")
    chat_history.add_ai_message(response)

print("---------------------")
print(chat_history)