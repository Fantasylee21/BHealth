<template>
    <div class="staging-container">
        zjq是大sl
    </div>
</template>

<script setup lang="ts">
import api from "@/api";
import {onMounted} from "vue";

const getSelfInfo = async () => {
    await api.getSelfInfo();
}

onMounted(() => {
    getSelfInfo();
})
</script>

<style scoped>
.staging-container {
    margin: 0 auto;
    width: 100%;
    display: flex;
    flex-direction: column;
}

.staging-header {
    width: 100%;
}

.staging-body {
    width: 100%;
    display: flex;
    margin-top: 10px;
}

.staging-left {
    width: 70%;
    display: flex;
    flex-direction: column;
    padding: 20px;
}

.staging-right {
    width: 30%;
    padding: 20px 100px 20px 20px;
    display: flex;
    flex-direction: column;
}


</style>