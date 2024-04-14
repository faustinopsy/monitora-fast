# 4 branch nesse projeto
1- main salvando no aruqivo texto
2- log-mysql salvando no banco relacional
3- log-mongo salvando no mongo NOSQL
4- log-rethinkdb salvando no rethinkdb NOSQL

-instalar o mongodb ou rethinkdb para testar a versão nosql

## Criar ambiente virtual
1º python -m venv fastapi_env 
## Ativar ambiente virtual 
2º Windows: fastapi_env\Scripts\activate 
macOS/Linux: source fastapi_env/bin/activate 
## instalar FastAPi+servidor uvicorn e biblioteca httpx
3º pip install fastapi uvicorn pip install httpx
## salvando o arquivo de dependencias
4º pip freeze > requirements.txt uvicorn main:app --reload
## instalando em outro ambiente
5º (instalar em outro local) passo 1 e passo 2 pip install -r requirements.txt

## executar o servidor
python main.py