<template>
<div class="container">
  <div id="logo"><h1 class="logo">BHealth</h1>
    <div class="CTA">
      <h1>Get ￥10</h1>
    </div>
  </div>
  <div class="leftbox">
    <nav class="nav">
      <a @click="toggleTab('profile')" :class="{ active: activeTab === 'profile' }">
        <!-- Element Plus 用户图标 -->
        <el-icon><user /></el-icon>
      </a>
      <a @click="toggleTab('payment')" :class="{ active: activeTab === 'payment' }">
        <!-- Element Plus 信用卡图标 -->
        <el-icon><credit-card /></el-icon>
      </a>
      <a @click="toggleTab('subscription')" :class="{ active: activeTab === 'subscription' }">
        <el-icon><Suitcase /></el-icon>
      </a>
      <a @click="toggleTab('privacy')" :class="{ active: activeTab === 'privacy' }">
        <!-- Element Plus 任务图标 -->
        <el-icon><Avatar /></el-icon>
      </a>
      <a @click="toggleTab('settings')" :class="{ active: activeTab === 'settings' }">
        <el-icon><Tools /></el-icon>
      </a>
    </nav>
  </div>
  <div class="rightbox">
    <div class="profile" :class="{ 'noshow': activeTab !== 'profile' }" >
      <h1>个人信息</h1>
      <h2>姓名</h2>
      <p>{{userName}}</p>
      <h2>有效期</h2>
      <p>{{expire}}</p>
      <h2>账号类型</h2>
      <p>{{type}}</p>
      <h2>邮箱</h2>
      <p>{{email}} </p>
      <h2>简介</h2>
      <p>{{ introduction }}</p>
    </div>

    <div class="payment" :class="{ 'noshow': activeTab !== 'payment' }">
      <h1>医疗卡</h1>
      <UserCard />
    </div>

    <div class="subscription" :class="{ 'noshow': activeTab !== 'subscription' }">
      <h1>工作信息</h1>
      <h2>科室</h2>
      <p>{{category}}</p>
      <h2>职称</h2>
      <p>{{title}}</p>
      <h2>毕业院校</h2>
      <p>{{school}}</p>
      <h2>工作时间</h2>
      <p>{{work_time}}</p>
    </div>

    <div class="privacy" :class="{ 'noshow': activeTab !== 'privacy' }">
      <h1>头像</h1>
      <div class="avatar-container">
        <img :src="avatarSrc" alt="avatar" class="avatar">
      </div>
      <div class="upload-div">
        <ElUpload
          class="upload-btn"
          action=""
          :before-upload="beforeUpload"
          :file-list="[]"
        >
          <el-button size="default" type="primary">更改头像</el-button>
        </ElUpload>
      </div>

    </div>

    <div class="settings" :class="{ 'noshow': activeTab !== 'settings' }">
      <h1>信息变更</h1>
      <h2>用户名<button class="btn" @click="nameInputDisabled = !nameInputDisabled">更改</button></h2>
      <p><el-input v-model="nameInput" :disabled="nameInputDisabled"></el-input> </p>
      <h2>简介<button class="btn" @click="introductionInputDisabled = !introductionInputDisabled">更改</button></h2>
      <p><el-input v-model="introductionInput" :disabled="introductionInputDisabled"></el-input></p>
      <h2>邮箱<button class="btn" @click="emailInputDisabled = !emailInputDisabled">更改</button></h2>
      <p><el-input v-model="emailInput" :disabled="emailInputDisabled"></el-input> </p>
      <el-button type="primary" @click="updateProfile" class="save">保存</el-button>
    </div>
  </div>
</div>
</template>

<script setup lang="ts">
import {onBeforeMount, ref} from 'vue';
import {Avatar, CreditCard, Suitcase, Tools, User} from "@element-plus/icons";
import UserCard from "@/components/UserCenter/UserCard.vue";
import api from "@/api";
import {useProfileStore} from "@/stores/profile";
import {ElMessage} from "element-plus";

const activeTab = ref('profile');

function toggleTab(tabName : string) {
  activeTab.value = tabName;
}

const getSelfInfo = async () => {
    await api.getSelfInfo();
}

onBeforeMount(() => {
    getSelfInfo();
})

const profile = useProfileStore();
const userName = profile.username;
const date = new Date(profile.date_joined);
const expire = `${(date.getFullYear() + 1 ).toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}`;
const email = profile.email;
const userType = profile.type;
let type = '';
if (profile.is_superuser) {
  type = '管理员';
} else {
  if (profile.type === 'doctor') {
    type = '医生';
  } else if (profile.type === 'patient'){
    type = '患者';
  } else {
    type = '取药师';
  }
}
const introduction = profile.introduction;
const avatarSrc = ref<string | null >(profile.avatar);

const school = profile.school;
const category = profile.category;
const title = profile.title;
const time = new Date(profile.work_time);
const work_time = `${time.getFullYear()}/${(time.getMonth() + 1).toString().padStart(2, '0')}/${time.getDate().toString().padStart(2, '0')}`;

const nameInput = ref<string>(profile.username);
const introductionInput = ref<string | null>(profile.introduction);
const emailInput = ref<string>(profile.email);

const nameInputDisabled = ref<boolean>(true);
const introductionInputDisabled = ref<boolean>(true);
const emailInputDisabled = ref<boolean>(true);

const uploadAvatar = async (file: File) => {
  const user_id = profile.id.toString();
  const formData = new FormData();
  formData.append('avatar', file); // 直接将 file 添加到 FormData 中

  try {
    await api.uploadAvatar({ formData, user_id });
    avatarSrc.value = URL.createObjectURL(file); // 预览上传的头像
  } catch (error) {
    ElMessage.error('头像上传失败');
  }
};

const beforeUpload = (file : File) => {
  const isImage = file.type.startsWith('image/');
  if (!isImage) {
    ElMessage.error('只能上传图片文件');
    return ;
  }
  uploadAvatar(file)
  return isImage;
};

const updateProfile = async () => {
  const data = {
    username: nameInput.value,
    email: emailInput.value,
    introduction: introductionInput.value,
    type : null,
    school: null,
    category: null,
    title: null,
    work_time: null,
    education: null,
  }
  const user_id = profile.id;
  try {
    await api.changeUserInfo(data, user_id);
    await getSelfInfo();
    nameInputDisabled.value = true;
    introductionInputDisabled.value = true;
    emailInputDisabled.value = true;
    ElMessage.success('信息更新成功');
  } catch (error) {
    ElMessage.error('信息更新失败');
  }
}

</script>

<style scoped>
body {
  background: linear-gradient(to right, #3FB6A8, #7ED386);
}


.container {
  background: #FFFFFF;
  width: 1350px;
  height: 420px;
  position: relative;
  margin: 6% auto;
  box-shadow: 2px 5px 20px rgba(119, 119, 119, 0.5);
}

.logo {
  float: right;
  margin-right: 12px;
  margin-top: 12px;
  font-family: 'Nunito Sans', sans-serif;
  color: #26a6dd;
  font-weight: 900;
  font-size: 1.5em;
  letter-spacing: 1px;
}

.CTA {
  width: 80px;
  height: 40px;
  right: -20px;
  bottom: 0;
  margin-bottom: 90px;
  position: absolute;
  z-index: 1;
  background: #359ed8;
  font-size: 1em;
  transform: rotate(-90deg);
  transition: all .5s ease-in-out;
  cursor: pointer;
  h1 {
    color: #FFFFFF;
    margin-top: 10px;
    margin-left: 9px;
  }
  &:hover {
    background: #3FB6A8;
    transform: scale(1.1);
  }
}

.leftbox {
  float: left;
  top: -5%;
  left: 5%;
  position: absolute;
  width: 7%;
  height: 110%;
  background: #4b7ddf;
  box-shadow: 2px 5px 20px rgba(119, 119, 119, 0.5);
}

nav a {
  list-style: none;
  padding: 35px;
  color: #FFFFFF;
  font-size: 1.1em;
  display: block;
  transition: all .3s ease-in-out;
  &:hover {
    color: #3FB6A8;
    transform: scale(1.2);
    cursor: pointer;
  }
  &:first-child {
    margin-top: 7px;
  }
}

.active {
  color: #3FB6A8;
}

.rightbox {
  float: right;
  width: 60%;
  height: 100%;
}

.profile, .payment, .subscription, .privacy, .settings {
  transition: opacity .5s ease-in;
  position: absolute;
  width: 70%;
}

h1 {
  font-family: 'Montserrat', sans-serif;
  color: #3680ae;
  font-size: 1em;
  margin-top: 40px;
  margin-bottom: 35px;
}

h2 {
  color: #777777;
  font-family: 'Roboto', sans-serif;
  width: 80%;
  text-transform: uppercase;
  font-size: 8px;
  letter-spacing: 1px;
  margin-left: 2px;
}

p {
  border-width: 1px;
  border-style: solid;
  border-image: linear-gradient(to right, #3FB6A8, rgba(126, 211, 134, 0.5)) 1 0;
  border-top: 0;
  width: 80%;
  font-family: 'Montserrat', sans-serif;
  font-size: .7em;
  padding: 7px 0;
  color: #070707;
}
span {
  font-size: .5em;
  color: #777777;
}

.btn {
  float: right;
  font-family: 'Roboto', sans-serif;
  text-transform: uppercase;
  font-size: 10px;
  border: none;
  color: #3FB6A8;
}

.btn:hover {
  text-decoration: underline;
  font-weight: 900;
}

input {
  border: 1px solid rgba(119, 119, 119, 0.4);
  font-family: 'Roboto', sans-serif;
  padding: 2px;
  margin: 0;
}

.privacy h2{
  margin-top: 25px;
}

.settings h2{
  margin-top: 25px;
}

.noshow {
  display: none;
}

footer {
  position: absolute;
  width: 20%;
  bottom: 0;
  right: -20px;
  text-align: right;
  font-size: 0.8em;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-family: 'Roboto', sans-serif;
  p {
    border: none;
    padding: 0;
  }
  a {
    color: #ffffff;
    text-decoration: none;
    &:hover {
      color: #7d7d7d;
    }
  }
}

.avatar {
  margin: auto 600px auto auto;
  width: 280px;
  height: 280px;
  border: 6px dashed #d9d9d9;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  transition: transform 0.3s ease;
}

.upload-div {
  margin: -30px auto -30px -40px;
  width: 100%;
  text-align: center;
}

.save {
  margin-top: 20px;
  margin-left: 340px;
}
</style>