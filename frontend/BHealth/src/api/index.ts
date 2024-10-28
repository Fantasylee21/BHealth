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
			const res = await api.get(`news/special/?type=${params.type}`, {
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

	getNewsById: async function (params: { id: string }) {
		try {
			const res = await api.get(`news/news/${params.id}/`, {
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

	uploadNews: async function (formData: FormData) {
		try {
			const isSuccess = (await api.post(`news/news/`, formData, {
				headers: {
					// 'Content-Type' 不需要显式设置，浏览器会自动处理
					Authorization: `Bearer ${sessionStorage.getItem('token')}`,
				},
			})).status === 201;

			if (isSuccess) {
				ElMessage.success('上传成功');
				setTimeout(() => {
					UtilMethods.jump('/news');
				}, 500);
			} else {
				ElMessage.error('上传失败');
			}
		} catch (error) {
			console.log(`output->error`, error);
			ElMessage.error(error.response?.data?.error || '上传过程中出错');
		}
	},

	getAllDoctor : async function (params: { page: number}) {
		try {
			const res = await api.get(`users/doctors/?page=${params.page}`, {
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

	delDoctor : async function (params: { id: string}) {
		try {
			const isSuccess = (await api.delete(`users/users/${params.id}/`, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${sessionStorage.getItem('token')}`,
				}
			})).status === 204;
			if (isSuccess) {
				ElMessage.success('删除成功');
				return true;
			} else {
				ElMessage.error('删除失败');
				return false;
			}
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
			return false;
		}
	},

	searchDoctor : async function (params: {name : string, category: string, content: string}) {
		try {
			const res = await api.get(`users/doctors/special/?name=${params.name}&category=${params.category}&content=${params.content}`, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${sessionStorage.getItem('token')}`,
				}
			});
			ElMessage.success(`查询${res.data.length}条数据`);
			return res.data;
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
		}
	},

	workSchedule : async function (params: { doctor_id: number, from_time : string, end_time : string, num : number}) {
		try {
			const bodyParams = {
				from_time: params.from_time,
				end_time: params.end_time,
				num: params.num,
			}
			const res = await api.post(`users/doctors/${params.doctor_id}/workSchedule/`, bodyParams, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${sessionStorage.getItem('token')}`,
				}
			});
			ElMessage.success('放号成功');
			return res.data;
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
		}
	},

	appointDoctor : async function (params: { doctor_id: number, from_time : string, end_time : string}) {
		try {
			const res = await api.post(`users/patients/appointment/`, params, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${sessionStorage.getItem('token')}`,
				}
			})
			ElMessage.success(`预约成功，请于${params.from_time}到${params.end_time}就诊`);
			return res.data;
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
		}
	},

	askAi : async function (params: { content: string}) {
		try {
			const res = await api.post(`aiask/`, params, {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${sessionStorage.getItem('token')}`,
				}
			})
			return res.data;
		} catch (error: any) {
			console.log(`output->error`, error)
			ElMessage.error(error.response.data.error)
		}
	}
}