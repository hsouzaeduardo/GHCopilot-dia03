#Plataforma de Consulta de CEPs

Contexto: Aplicação demo para consultar ceps

## Arquitetura
- `app/api` — rotas FastAPI e esquemas Pydantic. Só entrada, saída e HTTP.
- `app/services` — casos de uso. Orquestram domínio e repositórios.
- `app/domain` — domínio puro: modelos, regras, erros e as portas (`Protocol`).
  Não importa FastAPI, Pydantic, SQLAlchemy nem cliente HTTP.
- `app/infra` — implementações das portas: repositórios, mensageria, integrações.
- `tests/` — espelha a estrutura de `app/`.


Regra de dependência: `api -> services -> domain`. `infra` implementa as portas
declaradas em `app/domain/repositorios.py`. A rota nunca fala com o banco.

## Comandos
- Instalar: `make instalar`
- Testes:   `make testes`      (equivale a `pytest -m "not integracao"`)
- Lint:     `make lint`        (`ruff check .` e `ruff format --check .`)
- Tipos:    `make tipos`       (`mypy app`, modo strict)
- Rodar:    `make rodar`
- Migration: `./scripts/nova_migracao.sh <nome_em_snake_case>`

Rode `make tudo` antes de propor o diff final e cole a saída na resposta.

## Regras inegociáveis
- Valor monetário é `Decimal`, sempre. `float` em dinheiro é bug, não estilo.
  Arredondamento só via `app.domain.antecipacao.arredondar` (2 casas, HALF_UP).
- Data e hora com fuso: `datetime` aware em UTC. `datetime.now()` sem fuso é proibido.
- Toda mudança de contrato de API atualiza `docs/api.md` no mesmo PR.
- Migrations são geradas pelo script, nunca escritas à mão, e têm `downgrade` testado.
- Nenhum segredo no código ou em arquivo versionado. Use variável de ambiente.
- Log de operação sobre recebível inclui `recebivel_id` e `cedente_id`.
  Documento de cedente ou sacado nunca vai para log.
- Exceção de domínio herda de `ErroDeDominio` e é traduzida para HTTP na camada `api`.

## O que NÃO fazer
- Não adicionar dependência nova sem ADR em `docs/adr/`.
- Não atualizar versão de pacote como efeito colateral de outra tarefa.
- Não apagar nem enfraquecer teste existente para o build passar.
- Não usar `# type: ignore`, `# noqa` ou `Any` para calar ferramenta.
- Não importar de `app.infra` dentro de `app/domain` ou `app/services`.
- Não criar pasta ou pacote novo de nível superior sem aprovação humana.

## Convenções
- Nomes de domínio em português 
- Termos técnicos consagrados em inglês 