from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("openai_api_key"))

models = client.models.list()
print("Verfügbare Modelle:")
for model in models.data:
    print(model.id)