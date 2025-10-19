<template>
    <div class="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
        <div class="max-w-3xl text-center mb-10">
            <h1 class="text-4xl font-bold mb-4 text-gray-800">Portfólio Python</h1>
            <p class="text-gray-600 mb-4">
                Esta página serve como hub do meu portfólio de projetos em Python.
                O front-end pode ser desenvolvido com Vue, React ou Angular, e cada página se conecta a uma API
                desenvolvida em Python.
                Informações detalhadas sobre cada página podem ser visualizadas clicando no botão flutuante
                <strong>"Explicações"</strong> no canto inferior direito.
            </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 w-full max-w-4xl mx-auto p-4">
            <button @click="goTo('/python/gastos-camara')"
                class="cursor-pointer bg-white shadow-md rounded-lg py-6 px-8 text-gray-800 font-semibold hover:bg-blue-100 transition flex flex-col items-center">
                <span class="text-lg font-bold">Dados da Câmara</span>
                <span class="text-sm text-gray-400 mt-2">
                    Manipulação da API: https://dadosabertos.camara.leg.br/swagger/api.htm
                </span>
            </button>
        </div>

        <!-- Botão flutuante de explicações -->
        <Explicacoes :conteudo="explicacaoTexto" />
    </div>
</template>

<script>
import Explicacoes from "../components/Explicacoes.vue";

export default {
    components: { Explicacoes },
    methods: {
        goTo(path) {
            this.$router.push(path);
        },
    },
    data() {
        return {
            explicacaoTexto: `
            <h2 class="text-xl font-bold mb-2">O que este botão faz?</h2>
            <p class="mb-2">
                Para entender melhor o que está acontecendo em cada página do portfólio, você pode clicar no botão flutuante <strong>"Explicações"</strong> localizado no canto inferior direito.
            </p>
            <p class="mb-2">
                Cada página apresenta informações detalhadas sobre os dados exibidos, incluindo:
            </p>
            <ul class="list-disc list-inside mb-2">
                <li>Código Python utilizado para manipulação de APIs</li>
                <li>Exemplos de chamadas à API</li>
                <li>Demonstrações de funcionamento dos dados</li>
            </ul>
            <p>
                Assim, você terá acesso a explicações contextuais e detalhadas referentes a cada página, de forma interativa e centralizada.
            </p>
            `,
        };
    },
};
</script>

<style scoped>
/* Mantemos o estilo minimalista usando Tailwind */
</style>