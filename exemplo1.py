from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="FastAPI Nuno",
    description="Eemplo daa aula 1",
    version="0.1.0",
    contact={
        "name":"Nuno",
        "email":"nuno@teste.com",
    },
)

@app.get("/") # criando um arota pradrao rot aroot
def read_root():
    return {"mensage":"Hello "}


@app.get("/hello/{name}") #decorator 
def read_hello_name(name:str):
    return {"menssage":f"Hello {name}"}\
    


if __name__ ==  "main":
    uvicorn.run(f"exemplo:app", host="0.0.0.0", port="8000",reload=True)