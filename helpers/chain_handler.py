from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chat_models import init_chat_model
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_chroma import Chroma
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver



def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def setup_agent(model_provider, model):
    model = init_chat_model(str(model_provider) + str(':') + str(model))
    system_message = ''' You are a helpful assistant. Anaser the user's question as best as you can. Use the tools available to you.'''
    '''
        You are a helpful assistant.
        Answer the user's question: {input} as best you as can, considering the conversation history: {history}, 
        and the context: {context} provided by the user.
        If you are not sure about an answer, you may use the tools: {tools} available to you to find the answers. 
        Inputs to the tools need to be extracted from the user question. Do not use the same tool more than once.
        You should use your Thoughts:{agent_scratchpad} while coming back with an answer.
    '''
    

    # prompt = PromptTemplate.from_template(template)
    prompt = ChatPromptTemplate.from_messages([
                ("system", system_message),
                ("placeholder", "{messages}"),
            ])
    from helpers.tools import tools
    tools = tools
    memory = InMemorySaver()
    agent_executor = create_react_agent(model=model, tools=tools, prompt=prompt)
    return agent_executor
    
    
def setup_chain(model, retriever, chain_type="stuff", context_size=8192):
    llm = ChatOllama(
        model=model, 
        temperature=0.8, 
        num_predict=256, 
        keep_alive=-1,
        streaming=True, 
        max_tokens=context_size, 
        return_source_documents=True  
        )

    template = """ 
        You are a helpful assistant. Answer the following questions accurately, considering the history of the conversation, and the context provided.

        Context: {context}
        Chat history: {history}
        User question: {input}
        
        """

    prompt = ChatPromptTemplate.from_template(template)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    # rag_chain = create_retrieval_chain(retriever, question_answer_chain, chain_type=chain_type)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    ### Answer question ###
    return rag_chain


def setup_chain2(model, retriever):
    llm = ChatOllama(model=model, temperature=0.8, num_predict=256, keep_alive=-1)
    
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    ### Answer question ###
    system_prompt = (
        "You are an assistant named Benedict. Your task is question-answering."
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, make your best guess."
        "Keep the answer concise and short."
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain
