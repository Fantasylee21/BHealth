import axios from 'axios'
import env from '@/utils/env'
import router from "@/router";
import {ElMessage} from "element-plus";
import {useProfileStore} from "@/stores/profile";
import UtilMethods from "@/utils/UtilMethod";

const api = axios.create({
	baseURL: env.backEnd,
	withCredentials: false,
	timeout: 50000,
})

const profile = useProfileStore();

function delay(ms: any) {
	return new Promise((resolve) => setTimeout(resolve, ms))
}

export default {
	register: async function (params: { username: string; email: string; password: string; type: string; code: string;}) {
		try {
			const postParams = {
				username: params.username,
				email: params.email,
				password: params.password,
				code: params.code,
				type: params.type,
			}
			const isSuccess = (await api.post(`users/register/`, postParams)).status == 201
			if (isSuccess) {
				ElMessage.success('注册成功')
				const ret = await this.login({
					username: params.username,
					password: params.password,
				})
				if (ret) {
					profile.updateProfile(ret);
					ElMessage.success('登录成功')
					setTimeout(() => {
						UtilMethods.jump('/staging')
					}, 500)
				}
			} else ElMessage.error('注册失败')
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
		}
	},

	login: async function (params: { username: string; password: string }) {
    	console.log(`output->params`, params)
		try {
			const user = await api.post(`users/login/`, params)
			sessionStorage.setItem('token', user.data.token)
			return user.data
		} catch (error: any) {
			console.log(`output->error`, error)
			return null
		}
	},

	sendCode: async function (params: { email: string }) {
		try {
			const isSuccess = (await api.post(`users/mail/`, params)).status == 200
			if (isSuccess) {
				ElMessage.success('验证码已发送')
			} else ElMessage.error('验证码发送失败')
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
		}
	},

	getAllNews: async function () {
		try {
			const res = await api.get(`news/news/`, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${sessionStorage.getItem('token')}`,
				}
			});
			return res.data;
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
		}
	},

	getNewsByType: async function (params: { type: string }) {
		console.log(`output->params`, params.type)
		try {
			const res = await api.get(`/news/special/?type=${params.type}`, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${sessionStorage.getItem('token')}`,
				}
			});
			return res.data;
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
		}
	}
}