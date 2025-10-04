import os
import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(verbose=True)
# if not os.environ.get("GOOGLE_API_KEY"):
#     os.environ.setdefault("GOOGLE_API_KEY", "AIzaSyBi51MPLVAXnZSKpjhEhBcS6I8gBtcpHz0")
# os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
result = model.invoke("What is 81 divided by 9?")

print("Full result:")
print(result)
print("Content only:")
print(result.content)