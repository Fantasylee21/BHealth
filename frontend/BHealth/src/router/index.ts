import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'

const MainStaging = () => import('@/views/MainStaging.vue')
const NewsBoard = () => import('@/views/NewsBoard.vue')
const RegisterNumber = () => import('@/views/RegisterNumber.vue')
const LoginRegister = () => import('@/views/LoginRegister.vue')

const routes: Array<RouteRecordRaw> = [
	{
		path: '/loginRegister',
		name: 'LoginRegister',
		component: LoginRegister,
	},
	{
		path: '/staging',
		name: 'MainStaging',
		component: MainStaging,
	},
	{
		path: '/news',
		name: 'News',
		component: NewsBoard,
	},
	{
		path: '/registerNumber',
		name: 'RegisterNumber',
		component: RegisterNumber,
	},
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
