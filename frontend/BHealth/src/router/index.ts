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
const Diagnosis = () => import('@/views/DiagnosisPage.vue')

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
    meta: { requiresAuth: true }, // 需要登录
  },
  {
    path: '/news',
    name: 'News',
    component: NewsBoard,
    meta: { requiresAuth: true, allowedTypes: ['admin', 'doctor', 'patient'] },
  },
  {
    path: '/registerNumber',
    name: 'RegisterNumber',
    component: RegisterNumber,
    meta: { requiresAuth: true, allowedTypes: ['doctor', 'admin', 'patient'] },
  },
  {
    path: '/editor',
    name: 'Editor',
    component: EditNews,
    meta: { requiresAuth: true, allowedTypes: ['admin'] },
  },
  {
    path: '/newsDetail/:id',
    name: 'NewsDetail',
    component: NewsDetail,
    meta: { requiresAuth: true },
  },
  {
    path: '/diagnosis/:id',
    name: 'Diagnosis',
    component: Diagnosis,
    meta: { requiresAuth: true, allowedTypes: ['doctor', 'admin', 'patient', 'pharmacist'] },
  },
  {
    path: '/userCenter',
    name: 'UserCenter',
    component: UserCenter,
    meta: { requiresAuth: true },
  },
  {
    path: '/drugs',
    name: 'DrugsInfo',
    component: DrugsInfo,
    meta: { requiresAuth: true, allowedTypes: ['doctor', 'pharmacist'] },
  },
  {
    path: '/editCase',
    name: 'EditCase',
    component: EditCase,
    meta: { requiresAuth: true, allowedTypes: ['doctor'] },
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 登录状态判断函数
function isUserLoggedIn() {
  return sessionStorage.getItem('token') !== null;
}

// 获取用户类型和权限
function getUserType() {
  return sessionStorage.getItem('type');
}

function isSuperUser() {
  if (sessionStorage.getItem('is_superuser') === 'true') {
	return true;
  }
}

// 路由守卫
router.beforeEach((to, from, next) => {
  const isLoggedIn = isUserLoggedIn();
  const userType = getUserType();
  const superUser = isSuperUser();

  // 如果路由需要登录验证
  if (to.meta.requiresAuth) {
    if (!isLoggedIn) {
      return next({ path: '/loginRegister' });
    }

    // 如果路由有限制访问的用户类型
    if (to.meta.allowedTypes && !superUser) {
      if (!to.meta.allowedTypes.includes(userType)) {
        return next({ path: '/news' });
      }
    }
  }

  // 对于登录页面，如果已经登录，重定向到主页
  if (to.path === '/loginRegister' && isLoggedIn) {
    return next({ path: '/news' });
  }

  next();
});

export default router;