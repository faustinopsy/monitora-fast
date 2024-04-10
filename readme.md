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

## tabela mysql
```
CREATE TABLE `logs` (
  `idlogs` int NOT NULL AUTO_INCREMENT,
  `data` varchar(45) DEFAULT NULL,
  `http_method` varchar(45) DEFAULT NULL,
  `url` varchar(45) DEFAULT NULL,
  `user_agent` varchar(145) DEFAULT NULL,
  `client_ip` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idlogs`)
)
```