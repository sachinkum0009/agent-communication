from langfuse.langchain import CallbackHandler
 
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

langfuse_handler = CallbackHandler()


BASE_URL = "http://localhost:11434"
EMBED_MODEL = "qwen3-embedding:0.6b"
LLM_MODEL = "qwen3"
 
llm = ChatOllama(model=LLM_MODEL, temperature=0.7, base_url=BASE_URL)
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm
 
response = chain.invoke(
    {"topic": "cats"}, 
    config={"callbacks": [langfuse_handler]})

print(response.content)
# from langfuse import get_client
 
# langfuse = get_client()
 
# # Create a span using a context manager
# with langfuse.start_as_current_observation(as_type="span", name="process-request") as span:
#     # Your processing logic here
#     span.update(output="Processing complete")
 
#     # Create a nested generation for an LLM call
#     with langfuse.start_as_current_observation(as_type="generation", name="llm-response", model="gpt-3.5-turbo") as generation:
#         # Your LLM call logic here
#         generation.update(output="Generated response")
#         print("something happend")
 
# # All spans are automatically closed when exiting their context blocks
 
 
# # Flush events in short-lived applications
# # langfuse.flush()