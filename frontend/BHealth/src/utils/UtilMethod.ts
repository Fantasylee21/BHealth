import router from '@/router'

function jump(path: string) {
	router.push(path).then(r => r).catch(e => e)
}

export default {
	jump
}