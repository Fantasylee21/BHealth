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
            <!-- 显示头像 -->
            <el-sub-menu index="1">
                <template #title>
                    <el-avatar
                        :size="40"
                        :src="avatar"
                        class="nav-avatar"
                    />
                    <span style="margin-left: 10px">{{ profile.username }}</span>
                </template>
                <el-menu-item index="profile" @click="router.push('/diagnosis/' + patientId);">我的诊断书</el-menu-item>
                <el-menu-item index="logout" @click="showDialog=true">退出登录</el-menu-item>
            </el-sub-menu>
        </el-menu>

        <el-dialog
            title="退出登录"
            v-model="showDialog"
            width="30%"
            :before-close="handleClose">
            <span >您确定要退出登录吗？</span>
            <span class="dialog-footer">
                <el-button @click="showDialog = false">取 消</el-button>
                <el-button type="primary" @click="logout">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useProfileStore } from "@/stores/profile";

const activeIndex = ref('1')
const router = useRouter()
const profile = useProfileStore()
const showDialog = ref(false)

const avatar = profile.avatar
const patientId = profile.id
const handleSelect = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}


function logout() {
    sessionStorage.removeItem('token')
    router.push('/loginRegister')
    showDialog.value = false
    console.log('Logging out...')
}

function handleClose() {
    showDialog.value = false
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

.dialog-footer {
    margin-top: 30px;
    padding: 10px;
    text-align: center;
    border-top: 1px solid #e4e7ed;
}
</style>