import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'

const MainStaging = () => import('@/views/MainStaging.vue')
const News = () => import('@/views/NewsBoard.vue')
const RegisterNumber = () => import('@/views/RegisterNumber.vue')

const routes: Array<RouteRecordRaw> = [
	{
		path: '/staging',
		name: 'MainStaging',
		component: MainStaging,
	},
	{
		path: '/news',
		name: 'News',
		component: News,
	},
	{
		path: '/registerNumber',
		name: 'RegisterNumber',
		component: RegisterNumber,
	}
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach((to, from, next) => {
	sessionStorage.setItem('preRoute', to.path)
	next()
})

export default router
