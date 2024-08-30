import ollama

model_name = 'mistral'

while True:
    # Take input from the user
    user_message = input("You: ")

    # Check if the user wants to stop the chat
    if user_message.lower() == 'stop':
        print("Chat ended.")
        break

    # Start the chat with streaming enabled
    stream = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': user_message}],
        stream=True,
    )

    # Print the assistant's response
    print("Assistant: ", end='', flush=True)
    for chunk in stream:
        if 'message' in chunk and 'content' in chunk['message']:
            print(chunk['message']['content'], end='', flush=True)
    
    # Print a newline for readability after the assistant's response
    print()
