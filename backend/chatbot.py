from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from vector import retriever  # <-- Import from your new vector script
import time
import sys  # 🔄 CHANGED: Required for flush during streaming

# Prompt setup
template = """You are GroSafe, a trusted Irish assistant built *only* to answer questions about child grooming, protection, abuse, support services, and official Irish agencies like Tusla, ISPCC, CUAN, DRIVE, and An Garda Síochána.

If the user's question is unrelated to these topics or not supported by the context, say:
"I'm sorry, I don't have that information. You may want to contact the relevant service directly."

ONLY answer the specific question asked — do NOT ask or answer your own follow-up questions.

Respond in no more than 3 sentences. Use only the provided context. If unsure, say: "I'm sorry, I don't have that information."

Context:
{context}

Conversation history:
{history}

Question:
{question}

Your answer:
"""

prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="granite3.1-dense:2b-instruct-q4_K_M")
chain = prompt | model

# For Client / API
chat_history = ""
def get_bot_response(user_input: str) -> str:
    global chat_history
    start = time.time()  # Start timer
    
    docs_and_scores = retriever.vectorstore.similarity_search_with_score(user_input, k=6)
    docs = [doc for doc, score in docs_and_scores if score < 1.27]
    context = "\n\n".join([doc.page_content.strip() for doc in docs[:3]])[:3000]

    if not context.strip():
        result = "I'm sorry, I don't have that information. You may want to contact the relevant service directly."
    else:
        chunks = chain.stream({
            "history": chat_history,
            "question": user_input,
            "context": context
        })
        result = "".join([chunk for chunk in chunks])

    chat_history += f"User: {user_input}\nBot: {result}\n"
    response_time = int(time.time() - start)
    return f"{result} (Response time: {response_time} sec)"

# For terminal/CLI
def handle_conversation():
    history = ""
    print("Welcome to GroSafe. Type 'exit, quit or bye' to quit.")
    while True:
        print("-" * 80)
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break

        start = time.time()

        docs_and_scores = retriever.vectorstore.similarity_search_with_score(user_input, k=6)
        docs = [doc for doc, score in docs_and_scores if score < 1.27]
        context = "\n\n".join([doc.page_content.strip() for doc in docs[:3]])[:3000]

        if not context.strip():
            result = "I'm sorry, I don't have that information. You may want to contact the relevant service directly."
            print(f"GroSafe (Granite): {result}")
            history += f"User: {user_input}\nBot: {result}\n"
        else:
            print("GroSafe (Granite): ", end="", flush=True)  # 🔄 CHANGED: Start stream line
            result = ""  # 🔄 CHANGED: Capture streamed output
            for chunk in chain.stream({  # 🔄 CHANGED: Stream instead of invoke
                "history": history,
                "question": user_input,
                "context": context
            }):
                print(chunk, end="", flush=True)  # 🔄 CHANGED: Stream output live
                result += chunk  # 🔄 CHANGED: Append for history
            print()  # 🔄 CHANGED: Newline after streaming output
            history += f"User: {user_input}\nBot: {result}\n"  # 🔄 CHANGED: Save full streamed text

        print(f"Response time: {int(time.time() - start)} sec")

if __name__ == "__main__":
    handle_conversation()
