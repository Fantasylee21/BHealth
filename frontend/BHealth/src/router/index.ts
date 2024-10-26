import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'

const MainStaging = () => import('@/views/MainStaging.vue')
const NewsBoard = () => import('@/views/NewsBoard.vue')
const RegisterNumber = () => import('@/views/RegisterNumber.vue')
const LoginRegister = () => import('@/views/LoginRegister.vue')
const EditNews = () => import('@/views/EditNews.vue')
const IndividualCenter = () => import('@/views/IndividualCenter.vue')

const routes: Array<RouteRecordRaw> = [
	{
		path: '/',
		redirect: '/loginRegister',
	},
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
	{
		path: '/editor',
		name: 'Editor',
		component: EditNews,
	},
	{
		path: '/individualCenter',
		name: 'IndividualCenter',
		component: IndividualCenter,
	}
]

const router = createRouter({
	history: createWebHistory(),
	routes,
});

function isUserLoggedIn() {
	return sessionStorage.getItem('token') !== null
}

router.beforeEach((to, from, next) => {
	if (to.path === '/loginRegister') {
		if (isUserLoggedIn()) {
		  next({ path: '/staging' });
		} else {
		  next();
		}
	} else {
		if (!isUserLoggedIn()) {
		  next({ path: '/loginRegister' });
		} else {
		  next();
		}
	}

})

export default router
