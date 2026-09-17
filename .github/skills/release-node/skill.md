---
name: release-notes
description: >
  Use quando pedirem para preparar release, changelog, notas de versão ou o
  comunicado de uma entrega para o time de negócio. Gatilhos: "release notes",
  "changelog", "notas da versão", "o que entrou nessa release",
  "comunicado da entrega".
---

# Notas de release

## Fontes, nesta ordem
1. Commits desde a última tag:
   `git log $(git describe --tags --abbrev=0)..HEAD --oneline --no-merges`
2. PRs fechados no período — a descrição do PR costuma ser melhor que a
   mensagem do commit.
3. `docs/adr/` — decisão nova entra em "Mudanças internas".

## Estrutura da saída
- **Novidades** — o que o usuário passa a conseguir fazer.
- **Correções** — o sintoma que sumiu, não a causa técnica.
- **Mudanças internas** — só o que afeta outro time.
- **Atenção na atualização** — migration, mudança de contrato de API, variável
  de ambiente nova, ordem de deploy.

  ## Tom
Escreva para quem não lê código: "o cedente agora acompanha o status da
antecipação em tempo real", não "adicionado router em app/api".


Nunca invente o efeito de um commit que você não entendeu: liste sob
"Precisa de descrição" e siga.