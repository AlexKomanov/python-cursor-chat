import streamlit as st
import ollama
from typing import List, Dict
import pyperclip

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """Extract code blocks from markdown text"""
    code_blocks = []
    lines = text.split('\n')
    in_code_block = False
    current_block = []
    current_language = ''
    
    for line in lines:
        if line.startswith('```'):
            if in_code_block:
                code_blocks.append({
                    'language': current_language,
                    'code': '\n'.join(current_block)
                })
                current_block = []
                in_code_block = False
            else:
                in_code_block = True
                # Extract language if specified
                current_language = line[3:].strip()
                continue
        elif in_code_block:
            current_block.append(line)
            
    return code_blocks

def copy_to_clipboard(text: str):
    """Copy text to clipboard"""
    pyperclip.copy(text)

def main():
    st.title("Chat with Qwen2.5-coder")
    initialize_session_state()

    # Display chat messages
    for msg_idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                content = message["content"]
                
                # Check for code blocks
                code_blocks = extract_code_blocks(content)
                if code_blocks:
                    # Split content into parts and display accordingly
                    parts = content.split('```')
                    for i, part in enumerate(parts):
                        if i % 2 == 0:  # Regular text/markdown
                            if part.strip():
                                st.markdown(part)
                        else:  # Code block
                            # Remove language identifier from the first line
                            code_content = '\n'.join(part.strip().split('\n')[1:])
                            with st.expander("Show Code", expanded=True):
                                st.code(code_content)
                                if st.button("Copy Code", key=f"copy_msg_{msg_idx}_{i}"):
                                    copy_to_clipboard(code_content)
                else:
                    # Regular markdown
                    st.markdown(content)
            else:
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.chat_message("assistant"):
            try:
                response = ollama.chat(
                    model='qwen2.5-coder:1.5b',
                    messages=[{"role": "user", "content": prompt}]
                )
                
                assistant_response = response['message']['content']
                
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_response}
                )
                
                # Display response with special handling for code blocks
                code_blocks = extract_code_blocks(assistant_response)
                if code_blocks:
                    parts = assistant_response.split('```')
                    for i, part in enumerate(parts):
                        if i % 2 == 0:  # Regular text/markdown
                            if part.strip():
                                st.markdown(part)
                        else:  # Code block
                            # Remove language identifier from the first line
                            code_content = '\n'.join(part.strip().split('\n')[1:])
                            with st.expander("Show Code", expanded=True):
                                st.code(code_content)
                                if st.button("Copy Code", key=f"copy_new_response_{i}"):
                                    copy_to_clipboard(code_content)
                else:
                    st.markdown(assistant_response)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 