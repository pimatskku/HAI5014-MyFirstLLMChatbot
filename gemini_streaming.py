import os
from openai import OpenAI

token = os.environ["GOOGLE_API_KEY"]
endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/"
model_name = "gemini-2.0-flash"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def get_response(conversation_history):
    response = client.chat.completions.create(
        messages=conversation_history,
        model=model_name,
        stream=True,
        stream_options={'include_usage': True}
    )

    assistant_response = ""
    usage = None
    for update in response:
        if update.choices and update.choices[0].delta:
            chunk = update.choices[0].delta.content or ""
            assistant_response += chunk
            print(chunk, end="")
        if update.usage:
            usage = update.usage

    if usage:
        print("\n")
        for k, v in usage.dict().items():
            print(f"{k} = {v}")
    
    return assistant_response

def main():
    conversation_history = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        }
    ]
    
    print("Welcome to the Gemini Chat Assistant! (Type 'quit' to exit)")
    while True:
        user_input = input("\nYour question: ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get assistant's response
        assistant_response = get_response(conversation_history)
        
        # Add assistant's response to history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_response
        })

if __name__ == "__main__":
    main()