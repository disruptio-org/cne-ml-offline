# TestPlan.md

## Critérios de Aceitação principais
1. **Estrutura CSV:** 10 colunas, cabeçalho, `UTF-8`, separador `;`.
2. **Sequência por TIPO:** reinicia numeração de efetivos/suplentes.
3. **Ordenação:** `(DTMNFR, ORGAO, SIGLA, NOME_LISTA, TIPO, NUM_ORDEM)`.
4. **Domínios:** valores inválidos geram erro visual e bloqueiam exportação final.
5. **UI:** viewer PDF/imagem + tabela com ícones OK/AVISO/ERRO.
6. **ZIP:** concatenar múltiplos documentos mantendo sequências por lista e TIPO.
7. **Aprovação:** cria `data/approved/.../<job_id>/` e evento `result.approved`.
8. **Retreino:** gera candidate no histórico e promove apenas se métricas não degradarem.
9. **Rollback:** revert automático em caso de regressão.
10. **Desempenho:** PDF 2–4 páginas processado em <15 s (CPU).

## Casos de teste iniciais
- TT01: Efetivos/Suplentes (reinício da numeração).
- TT02: Múltiplos órgãos (AM e CM no mesmo ficheiro).
- TT03: Coligação (campos obrigatórios preenchidos automaticamente).
- TT04: Falha de domínio (SIGLA inexistente → ERRO visual).
- TT05: ZIP concatenado e preservação de sequências.
- TT06: Aprovação → criação de dataset de treino.
- TT07: Retreino e promoção sem regressão.
