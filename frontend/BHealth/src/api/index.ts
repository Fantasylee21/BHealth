import axios from 'axios'
import env from '@/utils/env'
import router from "@/router";
import {ElMessage} from "element-plus";
import {useProfileStore} from "@/stores/profile";

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
	register: async function (params: { username: string; email: string; password: string; type: string}) {
		try {
			const isSuccess = (await api.post(`users/register/`, params)).status == 201
			if (isSuccess) {
				ElMessage.success('注册成功')
				const ret = await this.login({
					username: params.username,
					password: params.password,
				})
				if (ret) {
					ElMessage.success('登录成功')
					profile.updateProfile()
					setTimeout(() => {
						router.push('/staging')
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
			localStorage.setItem('token', user.data.token)
			return user.data
		} catch (error: any) {
			console.log(`output->error`, error)
			return null
		}
	},
}