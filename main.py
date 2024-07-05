import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.title("Tiny Stories Bot")
st.caption("🚀 A Streamlit chatbot powered by BART")    



# question = st.text_input("Enter your question:")

# if st.button("Get Answer"):
#     if question:
#         response = requests.post("http://localhost:8000/generate", json={"question": question})
#         if response.status_code == 200:
#             answer = response.json()["answer"]
#             st.write("Answer:", answer)
#         else:
#             st.error("Error occurred while fetching the answer.")
#     else:
#         st.warning("Please enter a question.")



# Initialize session state
if 'messages' not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hey there!! I am here to help with tiny stories. Just ask away!!!"}]

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown(
        "This is an AI chat assistant powered by BART and TinyStories dataset. "
        "Ask questions and get AI-generated responses!"
    )
    st.markdown("---")
    st.markdown("[View frontend source code](https://github.com/sarveshkp045/frontend)")
    st.markdown("[View backend source code](https://github.com/sarveshkp045/backend)")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Send request to backend
        response = requests.post(f"{BACKEND_URL}/generate", json={"question": prompt})
        
        if response.status_code == 200:
            result = response.json()
            answer = result["answer"]
            context = result["context"]
            
            full_response = f"{answer}\n\n*Context: {context}*"
            message_placeholder.markdown(full_response)
        else:
            message_placeholder.error("Sorry, I couldn't generate an answer. Please try again.")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add a button to clear the conversation
if st.button("Clear Conversation"):
    st.session_state.messages = []
    st.session_state["messages"] = [{"role": "assistant", "content": "Hey there!! I am here to help with tiny stories. Just ask away!!!"}]
    st.experimental_rerun()