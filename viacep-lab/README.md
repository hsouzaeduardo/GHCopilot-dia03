# ViaCEP API

API em FastAPI que consulta endereços no [ViaCEP](https://viacep.com.br) e mantém um histórico das consultas feitas.

## Rodando

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload --port 8000
```

A API sobe em `http://localhost:8000`. Em desenvolvimento o histórico já vem populado. A documentação interativa fica em `/docs`.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/enderecos/{cep}` | Consulta um CEP no ViaCEP |
| GET | `/consultas` | Histórico de consultas já realizadas |

Há um arquivo `requests.http` na raiz com as chamadas prontas para a extensão REST Client.

## Estrutura

```
app/
  api/            rotas e injeção de dependência
  core/           modelos, contratos e casos de uso
  infra/          cliente HTTP do ViaCEP e repositório em memória
tests/            testes de unidade
```

## Configuração

A variável de ambiente `AMBIENTE` controla o seed do histórico (`desenvolvimento` por padrão). O cliente HTTP tem timeout de 5 segundos.
