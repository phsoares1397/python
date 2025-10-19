# Portfólio Python - Front-end

Este é o front-end do portfólio de projetos em Python, desenvolvido com **Vue 3** e **TailwindCSS**. Ele consome endpoints da API em Python que disponibiliza dados de deputados da Câmara dos Deputados, incluindo informações pessoais, gastos mensais e detalhes adicionais.

---

## 🔹 Estrutura do Projeto

- **Componentes principais**
  - `Explicacoes.vue` — Componente flutuante que exibe explicações detalhadas sobre a página atual, endpoints utilizados e funcionamento interno.
  - `Deputados.vue` — Página que lista todos os deputados com foto, nome, partido e UF, permitindo filtros por nome e estado.
  - `DetalhesDeputado.vue` — Página de detalhes de um deputado, com foto, dados pessoais, UF de nascimento, e informações sobre gastos e estatísticas.
  
- **Rotas**
  - `/python` — Página inicial do portfólio Python.
  - `/python/deputados` — Lista de deputados.
  - `/python/deputado/:id` — Detalhes de um deputado específico.

- **Estilos**
  - TailwindCSS é utilizado para layout responsivo e estilização rápida.
  - Componentes utilizam grids e flexbox para cards e seções de informações.

---

## 🔹 Funcionalidades

1. **Lista de deputados**
   - Carrega todos os deputados via endpoint `GET /python/api-camara/deputados`.
   - Exibe nome, partido, UF e foto.
   - Filtra por nome e por UF de forma dinâmica no front-end.
   - Cada card é clicável e leva à página de detalhes do deputado.

2. **Detalhes do deputado**
   - Endpoint: `GET /python/api-camara/deputado/{id}`.
   - Mostra informações pessoais, gabinete, UF de nascimento, data de nascimento e redes sociais.
   - Integra gráficos de gastos gerados pelo backend em Python.

3. **Explicações**
   - Componente flutuante `Explicacoes.vue`.
   - Exibe detalhes da página, endpoints utilizados e fluxo de dados.
   - Pode ser usado em qualquer página do portfólio para orientar recrutadores ou usuários.

4. **Integração com API de gastos**
   - Endpoint de gastos mensais: `GET /python/api-camara/gastos_mensais/{id}`.
   - Endpoint de detalhes de gastos: `GET /python/api-camara/gastos/{id}/{ano}/{mes}`.
   - Gera cards de gastos por mês com detalhes clicáveis.

5. **Loading e feedback**
   - Spinner enquanto os dados carregam.
   - Feedback visual quando não há dados ou erro na requisição.

---

## 🔹 Tecnologias Utilizadas

- Vue 3
- TailwindCSS
- Fetch API para integração com endpoints
- Teleport + Transitions do Vue para modais e explicações flutuantes

---

## 🔹 Exemplo de uso de endpoints

```javascript
fetch('https://phsoares.com/python/api-camara/deputados')
  .then(res => res.json())
  .then(data => console.log(data.dados));

fetch('https://phsoares.com/python/api-camara/deputado/204379')
  .then(res => res.json())
  .then(data => console.log(data.dados));

fetch('https://phsoares.com/python/api-camara/gastos_mensais/220667')
  .then(res => res.json())
  .then(data => console.log(data.gastos));

fetch('https://phsoares.com/python/api-camara/gastos/220667/2025/7')
  .then(res => res.json())
  .then(data => console.log(data.gastos_detalhados));

