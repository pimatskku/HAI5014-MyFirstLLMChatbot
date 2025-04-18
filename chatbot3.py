import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

print("Chatbot is ready! Type 'bye' to exit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "bye":
        print("Chatbot: Goodbye!")
        break

    response = client.complete(
        stream=True,
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage(user_input),
        ],
        model_extras={'stream_options': {'include_usage': True}},
        model=model_name,
    )

    usage = {}
    for update in response:
        if update.choices and update.choices[0].delta:
            print(update.choices[0].delta.content or "", end="")
        if update.usage:
            usage = update.usage

    if usage:
        print("\n")
        for k, v in usage.items():
            print(f"{k} = {v}")

client.close()