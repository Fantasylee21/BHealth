import {createRouter, createWebHistory, type RouteRecordRaw} from 'vue-router'

const MainStaging = () => import('@/views/MainStaging.vue')
const NewsBoard = () => import('@/views/NewsBoard.vue')
const RegisterNumber = () => import('@/views/RegisterNumber.vue')
const LoginRegister = () => import('@/views/LoginRegister.vue')
const EditNews = () => import('@/views/EditNews.vue')
const NewsDetail = () => import('@/views/NewsDetail.vue')
const UserCenter = () => import('@/views/UserCenter.vue')
const DrugsInfo = () => import('@/views/DrugsInfo.vue')
const EditCase = () => import('@/views/EditCase.vue')

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
    	path: '/newsDetail/:id',
		name: 'NewsDetail',
		component: NewsDetail,
  	},
	{
		path: '/userCenter',
		name: 'UserCenter',
		component: UserCenter,
	},
	{
		path: '/drugs',
		name: 'DrugsInfo',
		component: DrugsInfo,
	},
	{
		path: '/editCase',
		name: 'EditCase',
		component: EditCase,
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
