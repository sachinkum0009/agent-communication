import os

import bs4
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool
from langchain.agents import create_agent
from langfuse.langchain import CallbackHandler
from utils import LLM_MODEL, EMBED_MODEL, BASE_URL

def main():
    llm = ChatOllama(model=LLM_MODEL, temperature=0.7, base_url=BASE_URL)
    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=BASE_URL)
    vector_store = InMemoryVectorStore(embedding=embeddings)

    langfuse_handler = CallbackHandler()

    # Only keep post title, headers, and content from the full HTML
    bs4_strainer = bs4.SoupStrainer(
        class_=("post-title", "post-header", "post-content")
    )  # type: ignore
    loader = WebBaseLoader(
        web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()

    print(f"Total characters: {len(docs[0].page_content)}")
    print(docs[0].page_content[:500])

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)

    print(f"Split blog post into {len(all_splits)} sub-documents")

    document_ids = vector_store.add_documents(documents=all_splits)

    print(document_ids[:3])

    @tool(response_format="content_and_artifact")
    def retrieve_context(query: str):
        """Retrieve information to help answer a query."""
        retrieved_docs = vector_store.similarity_search(query, k=2)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    tools = [retrieve_context]

    prompt = (
        "You have access to a tool that retrieves context from a blog post."
        "Use the tool to help anser user queries."
    )
    agent = create_agent(llm, tools, system_prompt=prompt)

    query = (
        "What is the standard method for Task Decomposition?\n\n"
        "Once you get the answer, look up common extensions of that method."
    )

    for event in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
        config={"callbacks": [langfuse_handler]},
    ):
        event["messages"][-1].pretty_print()


if __name__ == "__main__":
    main()
