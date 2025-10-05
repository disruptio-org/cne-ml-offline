# 00_README_FOR_AI.md

## Contexto
Esta POC deve seguir integralmente o documento **Requirements.md**. O objetivo é criar uma solução totalmente **on-prem/offline** que:
- Recebe ficheiros PDF/DOCX/XLSX (ou ZIP).
- Usa IA para fazer OCR, parsing e validação automática.
- Gera um CSV final (10 colunas fixas) com os dados extraídos.
- Mostra o resultado numa UI e permite ao utilizador **descarregar** e **aprovar**.
- Quando aprovado, o job alimenta o dataset de treino e dispara um **retreino automático**.

## Ambiente
- Totalmente **offline/on-prem**, sem chamadas externas.
- Docker Compose com serviços:
  - `web` (UI React)
  - `api` (FastAPI)
  - `worker` (Celery/RQ)
  - `registry` (MLflow local ou diretório de modelos)

## Artefactos obrigatórios
1. `docker-compose.yml` com os quatro serviços definidos.
2. Implementação da API conforme **OpenAPI.yaml**.
3. Pipeline IA (OCR→layout→extração→validação→CSV).
4. UI com Upload → Resultado (viewer + tabela) → Aprovação.
5. Script de retreino incremental on-prem.
6. Teste comparativo com ficheiro `samples/golden/example_output.csv`.

## Regras chave
- CSV deve ter **10 colunas**, ordem e nomes idênticos ao dicionário de dados.
- Ordenação: `(DTMNFR, ORGAO, SIGLA, NOME_LISTA, TIPO, NUM_ORDEM)`.
- `NUM_ORDEM` **reinicia em 1** por TIPO (efetivo/suplente).
- Endpoint `POST /api/jobs/{id}/approve` deve mover os ficheiros para `data/approved/...` e emitir o evento `result.approved`.

## Estilo de geração de código
- Código **modular e executável**.
- Respeitar os Critérios de Aceitação (docs/TestPlan.md).
- Usar dependências locais: Tesseract/PaddleOCR, spaCy, FastAPI, React.
- Sem cloud APIs.

## Primeira tarefa (para o Codex)
**Tarefa 1:** Lê `docs/Requirements.md` e devolve a árvore completa do projeto com placeholders e TODOs coerentes.
Inclui apenas:
- `docker-compose.yml` vazio com serviços nomeados.
- `Makefile` com alvos `up`, `down`, `test`.
- Estrutura de pastas inicial.
Não gerar código nesta etapa.
