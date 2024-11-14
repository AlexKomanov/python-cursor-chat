import ollama

def chat_with_qwen():
    print("Chat with Qwen2.5-coder (type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check if user wants to exit
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        try:
            # Generate response using Ollama
            response = ollama.chat(
                model='qwen2.5-coder:1.5b',
                messages=[
                    {
                        'role': 'user',
                        'content': user_input
                    }
                ]
            )
            
            # Print the response
            print("\nQwen:", response['message']['content'])
            
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    chat_with_qwen() 