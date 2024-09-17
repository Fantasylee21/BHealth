import axios from 'axios'
import env from '@/utils/env'
import router from "@/router";

const api = axios.create({
	baseURL: env.backEnd,
	withCredentials: false,
	timeout: 50000,
})

function delay(ms: any) {
	return new Promise((resolve) => setTimeout(resolve, ms))
}

export default {

}