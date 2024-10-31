<template>
    <div class="nav-container">
        <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            :ellipsis="false"
            @select="handleSelect"
        >
            <img
                style="width: 120px; margin-left: 60px"
                src="@/assets/logo.png"
                alt="Element logo"
            />
            <div class="flex-grow"/>
<!--            显示头像-->
              <el-sub-menu index="1">
                  <template #title>
                      <el-avatar
                          :size="40"
                          :src="avatar"
                          class="nav-avatar"
                      />
                  </template>
                  <el-menu-item index="profile" @click="handleCommand('userCenter')">个人中心</el-menu-item>
                  <el-menu-item index="logout" @click="handleCommand('logout')">退出登录</el-menu-item>
              </el-sub-menu>
        </el-menu>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {useProfileStore} from "@/stores/profile";


const activeIndex = ref('1')
const router = useRouter()
const profile = useProfileStore()

const avatar = profile.avatar

const handleSelect = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}

function handleCommand(command: string) {
    if (command === 'logout') {
        sessionStorage.removeItem('token')
        router.push('/login')
        console.log('Logging out...')
    } else if (command === 'userCenter') {
        router.push('/userCenter')  // 假设有个人主页的路由
    }
}
</script>

<style>
.nav-container {
    margin: 0 auto;
    width: 1200px;
}

.flex-grow {
    flex-grow: 1;
}
</style>
