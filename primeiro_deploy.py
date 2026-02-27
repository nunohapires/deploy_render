from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat

from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
import os
from dotenv import load_dotenv, find_dotenv

import uvicorn
from fastapi import FastAPI
import asyncio # para rodar o agente de forma assíncrona que significa que ele pode processar outras requisições enquanto espera a resposta do modelo de linguagem, melhorando a performance da API


load_dotenv(find_dotenv())


# RAG
vector_db = ChromaDb(collection="pdf_agent", path="tmp/chromadb", persistent_client=True)
knowledge = Knowledge(vector_db=vector_db) # para armazenar o conhecimento


# knowledge.insert(
#     url="https://s3.sa-east-1.amazonaws.com/static.grendene.aatb.com.br/releases/2417_2T25.pdf",
#     metadata={"source": "Grendene", "type":"pdf", "description": "Relatório Trimestral 2T25"},
#     skip_if_exists=True,#nao adicionar o mesmo conteudo mais de uma vez,
#     reader=PDFReader() #, para ler o conteudo do pdf e transformar em texto
# )

db = SqliteDb(session_table="agent_session", db_file="tmp/agent.db")

agent = Agent(
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



# APIs
app = FastAPI(title="Agente de PDF - FastAPI", description="API para interagir com o agente de PDF", version="0.1.0")

@app.post("/agent_pdf")
def agent_pdf(pergunta: str):
    response = agent.run(pergunta)
    mensage = response.messages[-1]
    return {"message": mensage.content} # isso seve para rretornar a resposta dirrerrta do agente


# Run the agent
if __name__ == "__main__":
    # CORREÇÃO: Removido o asyncio.run()
    print("Iniciando inserção de conhecimento...")
    knowledge.insert(
        url="https://s3.sa-east-1.amazonaws.com/static.grendene.aatb.com.br/releases/2417_2T25.pdf",
        metadata={"source": "Grendene", "type":"pdf", "description": "Relatório Trimestral 2T25"},
        skip_if_exists=True,
        reader=PDFReader()
    )
    
    print("Iniciando servidor FastAPI...")
    uvicorn.run("primeiro_deploy:app", host="0.0.0.0", port=8000, reload=True)