# Portfólio Python - Back-end

Este é o back-end do portfólio de projetos em Python, desenvolvido com **FastAPI**. Ele fornece endpoints para listar deputados, consultar detalhes, obter gráficos de gastos e informações detalhadas por mês, integrando dados oficiais da Câmara dos Deputados.

---

## 🔹 Funcionalidades

1. **Carregamento de dados**
   - CSVs de 2008 até 2025 são baixados ou lidos localmente (`Ano-2008.csv` a `Ano-2025.csv`).
   - Mantém apenas colunas relevantes para o projeto:
     - `ideCadastro`, `txNomeParlamentar`, `sgUF`, `sgPartido`, `nuDeputadoId`, `datEmissao`, `vlrDocumento`, `vlrLiquido`, `numMes`, `numAno`, etc.
   - Dados carregados em memória ao iniciar a API para consultas rápidas.

2. **Endpoints principais**

| Endpoint | Método | Descrição |
|----------|-------|-----------|
| `/python/api-camara/deputados` | GET | Lista todos os deputados da API oficial da Câmara. |
| `/python/api-camara/deputado/{id}` | GET | Detalhes de um deputado específico pelo ID. |
| `/python/api-camara/grafico/{id}` | GET | Retorna um gráfico (imagem PNG) com os gastos do deputado por mês. |
| `/python/api-camara/gastos_mensais/{id}` | GET | Retorna JSON com o total de gastos por mês do deputado. |
| `/python/api-camara/gastos/{id}/{ano}/{mes}` | GET | Retorna os detalhes dos gastos de um deputado em um determinado ano e mês. |

3. **Geração de gráficos**
   - Utiliza **Matplotlib** para gerar gráficos de linha com os gastos do deputado.
   - Imagens podem ser consumidas diretamente no front-end.

---
