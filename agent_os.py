from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.os import AgentOS

import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


# RAG
vector_db = ChromaDb(collection="pdf_agent", path="tmp/chromadb", persistent_client=True)
knowledge = Knowledge(vector_db=vector_db) # para armazenar o conhecimento


db = SqliteDb(session_table="agent_session", db_file="tmp/agent.db")

agent = Agent(
        id="agente_pdf",
        name="Agente de PDF",
        model=OpenAIChat(id='gpt-5-nano', api_key=os.getenv("OPENAI_API_KEY")),
        db=db, # para armazenar o historico de conversas e interações do agente
        knowledge=knowledge,
        instructions="Você deve chamar o usuário de senhor",
        description="",
        search_knowledge=True, 
        num_history_runs=3,
        debug_mode=True
)


# Agente OS 
agent_os = AgentOS(agents=[agent], # meu proprrio agente criado acima 
                   name =  "agent_pdf",
)

app = agent_os.get_app()


# Run the agent
if __name__ == "__main__":
        print("Iniciando inserção de conhecimento...")
        knowledge.insert(
            url="https://s3.sa-east-1.amazonaws.com/static.grendene.aatb.com.br/releases/2417_2T25.pdf",
            metadata={"source": "Grendene", "type":"pdf", "description": "Relatório Trimestral 2T25"},
            skip_if_exists=True,
            reader=PDFReader()
    )
    
        print("Iniciando servidor FastAPI...")
        agent_os.serve(app="agent_os:app",reload=True, host="0.0.0.0", port=10000)