<template>
    <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            @open="handleOpen"
            @close="handleClose"
            :router="true"
    >
        <el-menu-item @click="toggleCollapse">
            <el-icon>
                <component :is="isCollapse ? ArrowRight : ArrowLeft"/>
            </el-icon>
            <template #title>菜单栏</template>
        </el-menu-item>
<!--        <el-sub-menu index="1">-->
<!--            <template #title>-->
<!--                <el-icon>-->
<!--                    <location/>-->
<!--                </el-icon>-->
<!--                <span>Navigator One</span>-->
<!--            </template>-->
<!--            <el-menu-item-group>-->
<!--                <template #title><span>Group One</span></template>-->
<!--                <el-menu-item index="1-1">item one</el-menu-item>-->
<!--                <el-menu-item index="1-2">item two</el-menu-item>-->
<!--            </el-menu-item-group>-->
<!--            <el-menu-item-group title="Group Two">-->
<!--                <el-menu-item index="1-3">item three</el-menu-item>-->
<!--            </el-menu-item-group>-->
<!--            <el-sub-menu index="1-4">-->
<!--                <template #title><span>item four</span></template>-->
<!--                <el-menu-item index="1-4-1">item one</el-menu-item>-->
<!--            </el-sub-menu>-->
<!--        </el-sub-menu>-->
 <el-menu-item
      index="/news"
      v-if="hasAccess(['patient', 'doctor', 'admin', 'pharmacist'])"
    >
      <el-icon><Share /></el-icon>
      <template #title>医院新闻</template>
    </el-menu-item>

    <!-- 编辑新闻：仅管理员可见 -->
    <el-menu-item
      index="/editor"
      v-if="hasAccess(['admin'])"
    >
      <el-icon><Edit /></el-icon>
      <template #title>编辑新闻</template>
    </el-menu-item>

    <!-- 全部医生：仅医生可见 -->
    <el-menu-item
      index="/registerNumber"
      v-if="hasAccess(['patient', 'admin'])"
    >
      <el-icon><School /></el-icon>
      <template #title>全部医生</template>
    </el-menu-item>

    <!-- 药品库存：医生和管理员可见 -->
    <el-menu-item
      index="/drugs"
      v-if="hasAccess(['pharmacist', 'admin'])"
    >
      <el-icon><Management /></el-icon>
      <template #title>药品库存</template>
    </el-menu-item>

    <!-- 病例编辑：医生和管理员可见 -->
    <el-menu-item
      index="/editCase"
      v-if="hasAccess(['doctor', 'admin'])"
    >
      <el-icon><Document /></el-icon>
      <template #title>病例编辑</template>
    </el-menu-item>

    <!-- 个人中心：所有用户可见 -->
    <el-menu-item
      index="/userCenter"
      v-if="hasAccess(['patient', 'doctor', 'admin', 'pharmacist'])"
    >
      <el-icon><UserFilled /></el-icon>
      <template #title>个人中心</template>
    </el-menu-item>
    </el-menu>
</template>

<script lang="ts" setup>
import {ref} from 'vue';
import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
} from '@element-plus/icons-vue';
import {ArrowLeft, ArrowRight} from '@element-plus/icons-vue';
import {Edit, Management, School, Share, UserFilled} from "@element-plus/icons";

const isCollapse = ref(true);
const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath);
};
const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath);
};
const emit = defineEmits(['toggleCollapse']);
const toggleCollapse = () => {
    isCollapse.value = !isCollapse.value;
    emit('toggleCollapse');
};
const userType = ref(sessionStorage.getItem('type'));
const isSuperUser = ref(sessionStorage.getItem('is_superuser') === 'true');

// 检查用户是否有权限访问特定菜单项
const hasAccess = (allowedRoles) => {
  if (isSuperUser.value) return true; // 超级管理员可以访问所有菜单
  return allowedRoles.includes(userType.value);
};
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-menu-vertical-demo.el-menu--collapse {
    width: 64px;
}
</style>
