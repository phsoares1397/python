<template>
    <div class="min-h-screen bg-gray-100 p-6 pb-25">
        <!-- Loading -->
        <div v-if="loading" class="flex justify-center items-center py-20">
            <svg class="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>
        </div>

        <!-- Informações do deputado -->
        <div v-else
            class="bg-white shadow-md rounded-lg p-6 flex flex-col md:flex-row items-center md:items-start gap-6">
            <img :src="deputado?.ultimoStatus?.urlFoto" :alt="deputado?.ultimoStatus?.nome"
                class="w-32 h-32 rounded-full object-cover" />

            <div class="flex-1">
                <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ deputado?.ultimoStatus?.nome }}</h1>
                <p class="text-gray-600 mb-1"><strong>Partido:</strong> {{ deputado?.ultimoStatus?.siglaPartido }}</p>
                <p class="text-gray-600 mb-1"><strong>UF:</strong> {{ deputado?.ultimoStatus?.siglaUf }}</p>
                <p class="text-gray-600 mb-1"><strong>Email:</strong> {{ deputado?.ultimoStatus?.gabinete?.email || 'Não disponível' }}</p>
                <p class="text-gray-600 mb-1"><strong>Nome civil:</strong> {{ deputado?.nomeCivil }}</p>
                <p class="text-gray-600 mb-1"><strong>Data de nascimento:</strong> {{ deputado?.dataNascimento }}</p>
                <p class="text-gray-600 mb-1"><strong>UF de nascimento:</strong> {{ deputado?.ufNascimento }}</p>

                <!-- Redes sociais -->
                <div v-if="deputado?.redeSocial?.length" class="mt-4 flex flex-wrap gap-2 items-center">
                    <span class="font-semibold text-gray-700 mr-2">Redes sociais:</span>
                    <a v-for="(link, index) in deputado.redeSocial" :key="index" :href="link" target="_blank"
                        class="flex items-center gap-1 bg-blue-100 text-blue-700 hover:bg-blue-200 px-3 py-1 rounded-full text-sm transition">
                        <!-- Ícone genérico de link -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M13.828 10.172a4 4 0 010 5.656l-3.536 3.536a4 4 0 01-5.656-5.656l1.414-1.414m4.242-4.242a4 4 0 015.656 5.656l-3.536 3.536a4 4 0 01-5.656-5.656l1.414-1.414z" />
                        </svg>
                        <span class="truncate max-w-xs">{{ link }}</span>
                    </a>
                </div>
            </div>
        </div>

        <!-- Seção de gráficos / dados adicionais -->
        <div v-if="!loading" class="mt-8 grid grid-cols-1 md:grid-cols-1 gap-6">
            <div class="bg-white shadow-md rounded-lg p-4 flex flex-col">
                <h2 class="text-xl font-semibold text-gray-800 mb-4">Evolução dos gastos mensais</h2>
                <div class="flex-1 flex items-center justify-center text-gray-400">
                    <span id="grafico_wrap">
                        <div class="flex justify-center items-center py-6">
                            <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg"
                                fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z">
                                </path>
                            </svg>
                        </div>
                    </span>
                </div>
            </div>

            <div class="bg-white shadow-md rounded-lg p-4 flex flex-col">
                <h2 class="text-xl font-semibold text-gray-800 mb-4">Resumo de despesas</h2>
                <div class="flex-1 flex items-center justify-center text-gray-400">
                    <span id="gastos_mensais" class="items-center justify-center flex flex-wrap gap-4"></span>
                </div>
            </div>
        </div>
    </div>
    <Explicacoes :conteudo="explicacaoTexto" />
</template>

<script>
import Explicacoes from "../components/Explicacoes.vue";

export default {
    props: ['id'],
    components: { Explicacoes },
    data() {
        return {
            deputado: null,
            loading: true,
            explicacaoTexto: `<p class="text-gray-700 leading-relaxed mb-4">
                Esta parte do projeto integra um <strong>front-end em Vue</strong> com uma <strong>API desenvolvida em Python (FastAPI)</strong> 
                para exibir e analisar informações sobre os <strong>gastos parlamentares</strong> da Câmara dos Deputados do Brasil.
                </p>

                <h3 class="text-xl font-semibold text-gray-800 mt-6 mb-2">🧾 Fontes de dados</h3>
                <p class="text-gray-700 leading-relaxed mb-4">
                Os dados são obtidos diretamente do portal oficial 
                <a href="https://dadosabertos.camara.leg.br" target="_blank" class="text-blue-600 hover:underline">
                Dados Abertos da Câmara dos Deputados</a>.
                Durante a inicialização da API, todos os arquivos de despesas de deputados — 
                de <strong>2008 até outubro de 2025</strong> — são carregados na memória.
                Esses arquivos contêm milhões de registros com informações detalhadas, como:
                </p>

                <ul class="list-disc list-inside text-gray-700 mb-4">
                <li>Nome do parlamentar (<code>txNomeParlamentar</code>)</li>
                <li>Identificador único (<code>ideCadastro</code>)</li>
                <li>UF e partido político (<code>sgUF</code>, <code>sgPartido</code>)</li>
                <li>Descrição e valor de cada despesa (<code>txtDescricao</code>, <code>vlrLiquido</code>)</li>
                <li>Data de emissão e fornecedor (<code>datEmissao</code>, <code>txtFornecedor</code>)</li>
                </ul>

                <p class="text-gray-700 leading-relaxed mb-4">
                Esses dados são mantidos em memória para acesso rápido e servem de base para 
                as rotas da API que permitem consultar, resumir e visualizar os gastos de cada deputado.
                </p>

                <h3 class="text-xl font-semibold text-gray-800 mt-6 mb-2">⚙️ Endpoints disponíveis</h3>

                <ul class="list-disc list-inside text-gray-700 mb-4">
                <li>
                    <strong><code>/python/api-camara/deputados</code></strong><br>
                    Retorna a lista completa de deputados, com nome, partido, UF e foto.
                </li>
                <li>
                    <strong><code>/python/api-camara/deputado/{id}</code></strong><br>
                    Retorna as informações detalhadas de um deputado específico, como nome civil, data e local de nascimento, 
                    e redes sociais. Exemplo:<br>
                    <code>GET /python/api-camara/deputado/204379</code>
                </li>
                <li>
                    <strong><code>/python/api-camara/grafico/{ideCadastro}</code></strong><br>
                    Gera um <strong>gráfico de linhas</strong> (PNG) com a evolução mensal dos gastos de um deputado.
                    Este gráfico é renderizado diretamente pelo <code>matplotlib</code> no backend.
                </li>
                <li>
                    <strong><code>/python/api-camara/gastos-mensais/{ideCadastro}</code></strong><br>
                    Retorna um resumo em JSON com o <strong>total gasto por mês</strong> para o deputado informado.
                </li>
                <li>
                    <strong><code>/python/api-camara/gastos/{ideCadastro}/{ano}/{mes}</code></strong><br>
                    Retorna um detalhamento dos <strong>gastos específicos de um mês</strong>, 
                    incluindo o total e a descrição de cada tipo de despesa.
                    <br>Exemplo:
                    <code>GET /python/api-camara/gastos/204379/2024/8</code>
                </li>
                </ul>

                <hr class="my-6">

                <p class="text-gray-500 italic">
                Desenvolvido em Python com <strong>FastAPI</strong> e <strong>Vue.js</strong>. 
                Os dados e gráficos são atualizados diretamente com base nos registros públicos da Câmara dos Deputados.
                </p>
                `
        };
    },
    async mounted() {
        try {
            const res = await fetch(`https://phsoares.com/python/api-camara/deputado/${this.id}`);
            const json = await res.json();
            // Ajuste: o JSON real retorna dados dentro de "dados"
            this.deputado = json.dados || json;
        } catch (err) {
            console.error("Erro ao buscar deputado:", err);
        } finally {
            this.loading = false;
        }

        try {
            const res = await fetch(`https://phsoares.com/python/api-camara/grafico/${this.id}`);
            if (!res.ok) throw new Error("Erro ao buscar gráfico");

            const blob = await res.blob(); // pega os bytes da imagem
            const urlImagem = URL.createObjectURL(blob); // cria uma URL temporária

            const graficoWrap = document.getElementById("grafico_wrap");
            setTimeout(() => {
                graficoWrap.innerHTML = `<img src="${urlImagem}" alt="Gráfico de gastos" class="max-w-full rounded-lg" />`;
            }, 1000)
        } catch (err) {
            console.error("Erro ao carregar gráfico:", err);
            const graficoWrap = document.getElementById("grafico_wrap");
            graficoWrap.innerHTML = `<p class="text-red-500">❌ Não foi possível carregar o gráfico.</p>`;
        }

        const wrap = document.getElementById("gastos_mensais");
        try {
            const res = await fetch(`https://phsoares.com/python/api-camara/gastos_mensais/${this.id}`);
            if (!res.ok) throw new Error("Erro ao buscar gastos mensais");
            const data = await res.json();

            for (const item of data["gastos"]) {
                const ano = item.ano_mes.split("-")[0]
                const mes = item.ano_mes.split("-")[1]
                const mesAno = `${mes}/${ano}`;
                const gasto = item.gasto_total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

                const div = document.createElement("div");
                div.className = "cada_mes_ano bg-white shadow-md rounded-lg p-4 flex-column justify-between items-center";

                div.innerHTML = `
                    <div class="flex justify-between items-center w-full">
                        <div>
                            <p class="text-gray-700"><strong>Vigência:</strong> ${mesAno}</p>
                            <p class="text-gray-700"><strong>Valor total:</strong> ${gasto}</p>
                        </div>
                        <button class="ml-4 bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition text-sm">
                            Detalhes
                        </button>
                    </div>
                    <div class="mt-2 hidden detalhes bg-gray-50 p-3 rounded border text-sm"></div>
                `;

                const btn = div.querySelector("button");
                const detalhesDiv = div.querySelector(".detalhes");

                btn.addEventListener("click", async () => {
                    if (!detalhesDiv.classList.contains("hidden")) {
                        detalhesDiv.classList.add("hidden");
                        div.classList.remove("w-full")
                        btn.innerHTML = "Detalhes"
                        btn.classList.add("bg-blue-500")
                        btn.classList.remove("bg-red-500")
                        document.querySelectorAll('.cada_mes_ano').forEach(el => {
                            el.classList.remove('hidden');
                        });
                        return;
                    }

                    document.querySelectorAll('.cada_mes_ano').forEach(el => {
                        el.classList.add('hidden');
                    });

                    btn.innerHTML = "Fechar"
                    btn.classList.add("bg-red-500")
                    btn.classList.remove("bg-blue-500")
                    div.classList.remove('hidden');
                    div.classList.add("w-full")
                    detalhesDiv.classList.remove("hidden");
                    detalhesDiv.innerHTML = `
                    <div class="flex justify-center items-center py-2">
                        <svg class="animate-spin h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                        </svg>
                    </div>
                `;

                    try {
                        const detalhesRes = await fetch(`https://phsoares.com/python/api-camara/gastos/${this.id}/${ano}/${mes}`);
                        if (!detalhesRes.ok) throw new Error("Erro ao buscar detalhes");
                        const detalhes = await detalhesRes.json();

                        const gastos = detalhes.gastos_detalhados || []; // usa a chave correta

                        if (gastos.length === 0) {
                            detalhesDiv.innerHTML = `<p class="text-gray-500">Nenhum gasto registrado neste mês.</p>`;
                            return;
                        }

                        detalhesDiv.innerHTML = gastos.map(d => `
                        <div class="border-b py-1">
                            <strong>${d.descricao}</strong>: ${Number(d.valor_total).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                        </div>
                    `).join("");

                    } catch (err) {
                        console.error(err);
                        detalhesDiv.innerHTML = `<p class="text-red-500">Não foi possível carregar os detalhes.</p>`;
                    }

                });

                wrap.appendChild(div);
            }
        } catch (err) {
            console.error(err);
            wrap.innerHTML = `<p class="text-red-500">Erro ao carregar gastos mensais.</p>`;
        }
    },
};
</script>

<style scoped>
/* Tailwind cuida da maior parte */
</style>