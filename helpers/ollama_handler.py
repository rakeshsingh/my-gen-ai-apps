from ollama import chat

conversation = [
    {"role": "user", "content": "Hello, how are you?"}
]
reply = chat(model='llama3.2', messages=conversation)
print(reply.message.content)
