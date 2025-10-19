<template>
    <!-- Botões flutuantes e modal via teleport -->
    <teleport to="body">
        <!-- Botão de explicações -->
        <button @click="open = true"
            class="cursor-pointer fixed bottom-6 right-6 z-50 bg-blue-600 text-white px-4 py-3 rounded-full shadow-lg flex items-center space-x-2 hover:bg-blue-700 transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4m0 4h.01M12 2a10 10 0 100 20 10 10 0 000-20z" />
            </svg>
            <span>Explicações</span>
        </button>

        <!-- Botão voltar para portfólio -->
        <button @click="handleClick()"
            class="cursor-pointer fixed bottom-6 left-6 z-50 bg-white text-gray-800 px-4 py-3 rounded-full shadow-lg flex items-center space-x-2 hover:bg-gray-100 transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            <span>{{ buttonText }}</span>
        </button>

        <!-- Modal com overlay -->
        <transition name="fade">
            <div v-if="open" class="fixed inset-0 bg-black/70 flex justify-center items-center z-50">
                <transition name="scale-fade">
                    <div class="bg-white rounded-lg shadow-xl max-w-[90vw] w-full max-h-[85vh] overflow-y-auto p-6 relative">
                        <!-- Botão de fechar -->
                        <button @click="open = false" class="absolute top-3 right-3 text-gray-500 hover:text-gray-800">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>

                        <!-- Conteúdo HTML -->
                        <div class="text-gray-700 prose max-w-full" v-html="conteudo"></div>
                    </div>
                </transition>
            </div>
        </transition>
    </teleport>
</template>

<script>
import router from '../router';

export default {
    computed: {
        buttonText() {
            return this.$route.path === '/python'
                ? 'Ir para portfólio completo'
                : 'Voltar';
        }
    },
    methods: {
        handleClick() {
            if (this.$route.path === '/python') {
                window.location.href = 'https://phsoares.com';
            } else {
                router.back()
            }
        }
    },
    name: "Explicacoes",
    props: {
        conteudo: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            open: false,
        };
    },
};
</script>

<style scoped>
/* Overlay fade */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
    opacity: 1;
}

/* Modal scale + fade */
.scale-fade-enter-active,
.scale-fade-leave-active {
    transition: opacity 0.25s ease, transform 0.25s ease;
}

.scale-fade-enter-from,
.scale-fade-leave-to {
    opacity: 0;
    transform: scale(0.95);
}

.scale-fade-enter-to,
.scale-fade-leave-from {
    opacity: 1;
    transform: scale(1);
}
</style>