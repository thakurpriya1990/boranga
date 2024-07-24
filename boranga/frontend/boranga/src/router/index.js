import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/internal/Home'
import external_routes from '@/components/external/routes'
import internal_routes from '@/components/internal/routes'
Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            component: Home
        },
        external_routes,
        internal_routes
    ]
})
