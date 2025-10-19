import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import GastosCamara from '../views/GastosCamara.vue';
import DetalhesDeputado from '../views/DetalhesDeputado.vue'

const routes = [
    {
        path: '/python',
        component: Home,
    },
    {
        path: '/python/gastos-camara',
        component: GastosCamara,
    },
    {
        path: '/python/detalhes-deputado/:id',
        name: 'DetalhesDeputado',
        component: DetalhesDeputado,
        props: true 
    },
];

const router = createRouter({
    history: createWebHistory(), // usa URL normal (sem #)
    routes,
});

export default router;