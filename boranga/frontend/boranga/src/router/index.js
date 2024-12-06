import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/components/internal/Home'
import external_routes from '@/components/external/routes'
import internal_routes from '@/components/internal/routes'

const router = createRouter({
    history: createWebHistory(),
    strict: false,
    routes: [
        {
            path: '/',
            component: Home
        },
        external_routes,
        internal_routes
    ]
})

export default router;
