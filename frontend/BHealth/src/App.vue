<template>
    <div class="common-layout">
        <el-container>
            <el-header class="header">
                <GlobalMenu/>
            </el-header>
            <el-container>
                <el-aside :width="isCollapse ? '200px' : '64px'">
                    <GlobalSidebar @toggleCollapse="toggleCollapse"/>
                </el-aside>
                <el-main class="main-content">
                    <router-view/>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import GlobalSidebar from "@/components/GlobalComponents/GlobalSidebar.vue";
import GlobalMenu from "@/components/GlobalComponents/GlobalMenu.vue";

const isCollapse = ref(false);

const toggleCollapse = () => {
    isCollapse.value = !isCollapse.value;
};
</script>

<style scoped>
.header {
    border-bottom: 1px solid var(--el-menu-border-color);
}

.el-container {
    height: 100%;
}

.el-aside {
    transition: width 0.3s;
    z-index: 2000;
    position: fixed;
    top: 0;
    bottom: 0;
    background-color: #fff;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.12);
}

.main-content {
    flex: 1;
    padding: 20px;
    overflow: auto;
    margin-left: 50px;
    width: 100%;
}
</style>
