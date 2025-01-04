def llamaindex(question):
    from llama_index.core import (
        SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage, VectorStoreIndex
        ,get_response_synthesizer,PromptTemplate
    )
    from llama_index.llms.openai import OpenAI
    import os
    from lib.prompt import NEW_TEMPLATE_PROMPT
    from llama_index.core.retrievers import VectorIndexRetriever
    from llama_index.core.query_engine import RetrieverQueryEngine
    from llama_index.core.postprocessor import SimilarityPostprocessor

    # Load Docs
    # os.environ['OPENAI_API_KEY'] = openai_api_key
    documents = SimpleDirectoryReader(input_files = ["./faq_data.csv"]).load_data()
    llm = OpenAI(model="gpt-4-turbo")
    Settings.llm = llm

    if os.path.exists("storage"):
        storage_context = StorageContext.from_defaults(persist_dir="storage")
        index = load_index_from_storage(storage_context)
    else:
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir="storage")

    retriever = VectorIndexRetriever(index=index, similarity_top_k=10)
    synthesizer = get_response_synthesizer()

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)]
    )

    query_engine = index.as_query_engine()
    query_engine.update_prompts({"response_synthesizer:text_qa_template": PromptTemplate(NEW_TEMPLATE_PROMPT)})

    response = query_engine.query(question)

    return response