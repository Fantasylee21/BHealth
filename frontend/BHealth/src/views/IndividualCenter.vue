<script setup lang="ts">
import { ref, reactive } from 'vue';

const userInfo = reactive({
  username: '张三',
  email: '764012358@qq.com',
  type: '患者',
  category: '普通用户',
  introduction: '我就是我，不一样的烟火',
});

// 头像相关
const avatarUrl = ref<string | null>(null);

function handleAvatarUpload(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    avatarUrl.value = URL.createObjectURL(file);
  }
}

const isEditing = ref(false);

function toggleEdit() {
  isEditing.value = !isEditing.value;
}

function saveChanges() {
  isEditing.value = false;
  // 这里可以添加保存到服务器的逻辑，例如通过API提交数据
}
</script>

<template>
  <div class="user-profile">
    <div class="profile-avatar">
      <img :src="avatarUrl || 'https://via.placeholder.com/120'" alt="头像" class="avatar-image" />
      <label class="custom-upload">
        <input type="file" @change="handleAvatarUpload" accept="image/*" class="upload-input" />
        更换头像
      </label>
    </div>
    <div class="profile-header">
      <template v-if="isEditing">
        <input v-model="userInfo.username" class="editable-input" />
      </template>
      <template v-else>
        <h2>{{ userInfo.username }}</h2>
      </template>
      <p>{{ userInfo.type }} | {{ userInfo.category }}</p>
    </div>
    <div class="profile-info">
      <p>
        <strong>📧 邮箱:</strong>
        <template v-if="isEditing">
          <input v-model="userInfo.email" class="editable-input" />
        </template>
        <template v-else>
          {{ userInfo.email }}
        </template>
      </p>
      <p>
        <strong>💼 个人简介:</strong>
        <template v-if="isEditing">
          <input v-model="userInfo.introduction" class="editable-input" />
        </template>
        <template v-else>
          {{ userInfo.introduction }}
        </template>
      </p>
      <p>
        <strong>种类:</strong>
        <template v-if="isEditing">
          <input v-model="userInfo.type" class="editable-input" />
        </template>
        <template v-else>
          {{ userInfo.type }}
        </template>
      </p>
      <p>
        <strong>分组:</strong>
        <template v-if="isEditing">
          <input v-model="userInfo.category" class="editable-input" />
        </template>
        <template v-else>
          {{ userInfo.category }}
        </template>
      </p>
      <div class="button-group">
        <button @click="toggleEdit" v-if="!isEditing">编辑信息</button>
        <button @click="saveChanges" v-if="isEditing">保存</button>
        <button @click="toggleEdit" v-if="isEditing">取消</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-profile {
  width: 500px;
  padding: 100px;
  margin: 0 auto;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  font-family: Arial, sans-serif;
}

.profile-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 25px;
}

.avatar-image {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #eaeaea;
}

.custom-upload {
  margin-top: 15px;
  font-size: 16px;
  color: #007bff;
  cursor: pointer;
  text-decoration: underline;
}

.upload-input {
  display: none;
}

.profile-header {
  text-align: center;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.profile-header h2 {
  font-size: 28px;
  color: #333;
  margin: 0;
}

.profile-header p {
  font-size: 16px;
  color: #888;
  margin-top: 8px;
}

.profile-info p {
  margin: 15px 0;
  font-size: 18px;
  line-height: 1.6;
  color: #555;
}

.profile-info strong {
  color: #333;
}

.editable-input {
  width: 100%;
  padding: 8px;
  margin-top: 8px;
  font-size: 18px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.button-group {
  display: flex;
  gap: 15px;
  margin-top: 25px;
}

.button-group button {
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.button-group button:hover {
  background-color: #0056b3;
}
</style>
