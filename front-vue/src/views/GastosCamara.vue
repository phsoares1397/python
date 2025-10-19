<template>
    <div class="min-h-screen flex flex-col items-center justify-start bg-gray-100 p-4">
        <div class="max-w-3xl text-center mb-6">
            <h1 class="text-4xl font-bold mb-4 text-gray-800">Deputados</h1>
            <p class="text-gray-600 mb-4">
                Explore os deputados com fotos e nomes. Use a busca por nome ou selecione um estado. Clique em qualquer
                deputado para acessar detalhes, dados e estatísticas.
            </p>

            <!-- Container do filtro -->
            <div class="flex flex-col sm:flex-row gap-4 mb-0 max-w-3xl mx-auto">
                <!-- Input de pesquisa -->
                <input v-model="search" type="text" placeholder="Pesquisar por nome..."
                    class="flex-1 p-3 rounded-lg border border-gray-300 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800 placeholder-gray-400 transition" />

                <!-- Select de UF -->
                <select v-model="selectedUf"
                    class="flex-1 p-3 rounded-lg border border-gray-300 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800 transition">
                    <option value="">Todos os estados</option>
                    <option v-for="uf in ufsDisponiveis" :key="uf.sigla" :value="uf.sigla">
                        {{ uf.sigla }} - {{ uf.nome }}
                    </option>
                </select>
            </div>

        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center items-center py-20">
            <svg class="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>
        </div>

        <!-- Lista de deputados -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 w-full max-w-5xl">
            <router-link v-for="deputado in filteredDeputados" :key="deputado.id"
                :to="{ name: 'DetalhesDeputado', params: { id: deputado.id } }"
                class="bg-white shadow-md rounded-lg p-4 flex flex-col items-center text-center hover:shadow-lg transition">
                <img :src="deputado.urlFoto" :alt="deputado.nome" class="w-24 h-24 rounded-full mb-2 object-cover" />
                <span class="font-semibold text-gray-800">{{ deputado.nome }}</span>
                <span class="text-sm text-gray-500">{{ deputado.siglaPartido }} - {{ deputado.siglaUf }}</span>
            </router-link>
        </div>

        <!-- Explicações flutuante -->
        <Explicacoes :conteudo="explicacaoTexto" />
    </div>
</template>

<script>
import Explicacoes from "../components/Explicacoes.vue";

export default {
    components: { Explicacoes },
    data() {
        return {
            deputados: [],
            search: "",
            selectedUf: "",
            loading: true,
            estados: [
                { sigla: "AC", nome: "Acre" },
                { sigla: "AL", nome: "Alagoas" },
                { sigla: "AP", nome: "Amapá" },
                { sigla: "AM", nome: "Amazonas" },
                { sigla: "BA", nome: "Bahia" },
                { sigla: "CE", nome: "Ceará" },
                { sigla: "DF", nome: "Distrito Federal" },
                { sigla: "ES", nome: "Espírito Santo" },
                { sigla: "GO", nome: "Goiás" },
                { sigla: "MA", nome: "Maranhão" },
                { sigla: "MT", nome: "Mato Grosso" },
                { sigla: "MS", nome: "Mato Grosso do Sul" },
                { sigla: "MG", nome: "Minas Gerais" },
                { sigla: "PA", nome: "Pará" },
                { sigla: "PB", nome: "Paraíba" },
                { sigla: "PR", nome: "Paraná" },
                { sigla: "PE", nome: "Pernambuco" },
                { sigla: "PI", nome: "Piauí" },
                { sigla: "RJ", nome: "Rio de Janeiro" },
                { sigla: "RN", nome: "Rio Grande do Norte" },
                { sigla: "RS", nome: "Rio Grande do Sul" },
                { sigla: "RO", nome: "Rondônia" },
                { sigla: "RR", nome: "Roraima" },
                { sigla: "SC", nome: "Santa Catarina" },
                { sigla: "SP", nome: "São Paulo" },
                { sigla: "SE", nome: "Sergipe" },
                { sigla: "TO", nome: "Tocantins" },
            ],
            explicacaoTexto: `
                <p class="mb-4 text-gray-700">
                Esta página lista todos os deputados, mostrando foto, nome, partido e UF. 
                Os dados são carregados diretamente do endpoint da API:
                </p>

                <pre class="bg-gray-100 p-4 rounded mb-4 overflow-x-auto"><code>
        fetch('https://phsoares.com/python/api-camara/deputados')
        .then(res =&gt; res.json())
        .then(data =&gt; {
            // 'data.dados' contém todos os deputados
            const deputados = data.dados;
            const container = document.getElementById('lista_deputados');

            deputados.forEach(d =&gt; {
                const card = document.createElement('div');
                card.className = 'bg-white shadow-md rounded-lg p-4 flex flex-col items-center text-center mb-4';
                card.innerHTML = \`
                    &lt;img src="\${d.urlFoto}" alt="\${d.nome}" class="w-24 h-24 rounded-full object-cover mb-2"&gt;
                    &lt;span class="font-semibold text-gray-800"&gt;\${d.nome}&lt;/span&gt;
                    &lt;span class="text-sm text-gray-500"&gt;\${d.siglaPartido} - \${d.siglaUf}&lt;/span&gt;
                \`;
                container.appendChild(card);
            });
        })
        .catch(err =&gt; console.error('Erro ao buscar deputados:', err));
                </code></pre>

                <p class="mb-4 text-gray-700">
                O container <code>#lista_deputados</code> usa grid responsivo do Tailwind para organizar os cards em linhas e colunas:
                </p>
                <div id="lista_deputados" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mt-4">
                <!-- Os cards serão adicionados aqui via JS -->
                </div>

                <h3 class="text-xl font-bold mt-6 mb-2">Como o endpoint funciona</h3>
                <p class="mb-4 text-gray-700">
                O endpoint <code>/python/api-camara/deputados</code> retorna todos os deputados em JSON. 
                Cada objeto contém:
                </p>
                <ul class="list-disc ml-6 mb-4 text-gray-700">
                <li><strong>id</strong>: Identificador único do deputado</li>
                <li><strong>nome</strong>: Nome do deputado</li>
                <li><strong>siglaPartido</strong>: Sigla do partido</li>
                <li><strong>siglaUf</strong>: Unidade federativa</li>
                <li><strong>urlFoto</strong>: Link para a foto do deputado</li>
                <li><strong>email</strong>: E-mail do gabinete (quando disponível)</li>
                </ul>

                <p class="mb-4 text-gray-700">
                Cada card pode ser clicado para abrir mais detalhes, utilizando outro endpoint específico 
                <code>/python/api-camara/deputado/{id}</code>, que retorna informações completas do deputado 
                incluindo CPF, nascimento, rede social, gabinete e status atual.
                </p>

                <p class="mb-4 text-gray-700">
                Este fluxo permite que a página carregue rapidamente os dados em memória, sem fazer múltiplas requisições, 
                além de possibilitar filtros por nome ou UF diretamente no front-end.
                </p>

                <p class="mb-4 text-gray-700 font-semibold">
                Resumindo: a página é uma interface dinâmica que consome a API, cria cards de deputados em grid responsivo, 
                permite filtros e navegação para detalhes de cada deputado.
                </p>
            `
        };
    },
    computed: {
        ufsDisponiveis() {
            const ufs = new Set(this.deputados.map(d => d.siglaUf));
            return this.estados.filter(e => ufs.has(e.sigla));
        },
        filteredDeputados() {
            const searchLower = this.search.toLowerCase();
            return this.deputados.filter(d =>
                (d.nome.toLowerCase().includes(searchLower) || searchLower === "") &&
                (this.selectedUf === "" || d.siglaUf === this.selectedUf)
            );
        },
    },
    async mounted() {
        try {
            const localData = localStorage.getItem("deputados");
            if (localData) {
                this.deputados = JSON.parse(localData);
            } else {
                const res = await fetch("https://phsoares.com/python/api-camara/deputados");
                const json = await res.json();
                this.deputados = json.dados;
                localStorage.setItem("deputados", JSON.stringify(this.deputados));
            }
        } catch (err) {
            console.error("Erro ao buscar deputados:", err);
        } finally {
            setTimeout(() => {
                this.loading = false;
            }, 800);
        }
    },
};
</script>

<style scoped>
/* Tailwind cuida da maior parte */
</style>