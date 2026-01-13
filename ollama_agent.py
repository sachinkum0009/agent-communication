from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3",
    temperature=0.7,
    base_url="http://localhost:11434"
)

messages = [
    (
        "system",
        "You are a helpful assistant",
    ),
    (
        "human",
        "What is life",
    )
]

ai_msg = llm.invoke(messages)

print(ai_msg.content)
