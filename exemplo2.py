#  Conta corrente bancaria - FastAPI

# Gerenciar saques e depositos de clientes
# ter um saldo e acompanhar como ele evoului na minha conta corrente 

# IMPORTS ===========================================================
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field
# inicializa o fastapi
app = FastAPI(title="Conta Bancaria - Conta Correte")


# Adicionar clientes 
db_clientes = {
    "Joao": 500,
    "Maria": 0,
    "Pedro": 0,
}

# criar uma classe para as movimentações (saques e depósitos) OBS: usar pydantic (para nao aconter erros)
class Movimentacao(BaseModel):
    cliente: str = Field(..., description="Nome do cliente")
    valor: float = Field(..., gt=0, description="Valor da movimentacao")

# Criar um endpoint HOME (raiz)
@app.get("/")
def home():
    return {"message": "Bem-vindo à conta bancária!"}

# criando end points para consultar o saldo
@app.post("/saldo")
def saldo(cliente: str):
    return {"mensagem": f"O saldo do cliente {cliente} é de R${db_clientes[cliente]}."}

# Criare end points para realisar saques 
@app.post("/saque")
def saque(movimentacao: Movimentacao):
    cliente = movimentacao.cliente
    valor = movimentacao.valor
    if cliente not in db_clientes:
        return {"mensagem": f"Cliente {cliente} não encontrado."}
    if db_clientes[cliente] < valor:
        return {"mensagem": f"Saldo insuficiente para o cliente {cliente}."}
    db_clientes[cliente] -= valor
    return {"mensagem": f"Saque de R${valor} realizado para o cliente {cliente}. Novo saldo: R${db_clientes[cliente]}."}

# Criando end points para realizar depositos
@app.post("/deposito")
def deposito(movimentacao: Movimentacao):
    db_clientes[movimentacao.cliente] += movimentacao.valor
    return {"mensagem": f"Depósito de R${movimentacao.valor} realizado para o cliente {movimentacao.cliente}. Novo saldo: R${db_clientes[movimentacao.cliente]}."} 

# RUN ===========================================================
if __name__ == "__main__":
    uvicorn.run("exemplo2:app", host="0.0.0.0", port=8000,reload=True)