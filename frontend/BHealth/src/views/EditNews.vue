<script setup lang="ts">
import { ref } from "vue";
import WangEditor from "@/components/WangEditor/WangEditor.vue";
import {ElUpload, ElButton, ElMessage} from "element-plus";
import { CaretLeft } from "@element-plus/icons";
import api from "@/api";

const ready2Submit = ref(false);
const content = ref('');
const imageFile = ref<File | null>(null);
const imagePreview = ref<string | null>(null);
const description = ref('');
const title = ref('');

const handleSubmit = (html: string) => {
    ready2Submit.value = true;
    console.log('HTML->', html);
    content.value = html;
};

const handleImageUpload = (file: File) => {
    imageFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
    console.log('Uploaded image:', file);
};


const submitData = async () => {
    if (!title.value) {
        ElMessage.error('请填写新闻标题');
        return;
    }
    if (!description.value) {
        ElMessage.error('请填写新闻简介');
        return;
    }
    if (!imageFile.value) {
        ElMessage.error('请上传封面图片');
        return;
    }
    const formData = new FormData();
    formData.append('title', title.value);
    formData.append('content', content.value);
    formData.append('description', description.value);
    formData.append('front_image', imageFile.value);

    await api.uploadNews(formData);
};
</script>

<template>
    <h1 class="titleAll">编辑新闻界面</h1>
    <div class="edit-news-container">
        <!-- Transition between the editor and upload section -->
        <transition name="slide-fade" mode="out-in">
            <div class="edit-news-body" v-show="!ready2Submit">
                <WangEditor @getEditorHTML="handleSubmit"/>
            </div>
        </transition>
        <transition name="slide-fade" mode="out-in">
            <div v-show="ready2Submit" class="image-upload-section">
                <div class="back" @click="ready2Submit = false">
                    <el-icon size="12px"><CaretLeft /></el-icon>
                    <span class="backEdit">返回编辑</span>
                </div>
                <p class="newsP">新闻标题</p>
                <input
                    placeholder="为新闻起一个标题"
                    v-model="title"
                    class="description-input"
                    maxlength="60"

                />
                <p class="newsP">新闻简介</p>
                <input
                    placeholder="为新闻添加一小段描述"
                    v-model="description"
                    class="description-input"
                    maxlength="60"
                />
                <ElUpload
                    class="upload-demo"
                    action=""
                    :before-upload="handleImageUpload"
                    :file-list="[]"
                >
                    <ElButton type="primary">上传封面图片</ElButton>
                </ElUpload>
                <div v-if="imagePreview" class="image-preview">
                    <img :src="imagePreview" alt="Image Preview" class="preview-img" />
                </div>
                <ElButton type="success" @click="submitData" class="submit-btn">发布新闻</ElButton>
            </div>
        </transition>
    </div>
</template>

<style scoped>
.titleAll {
  /* 现有样式保持不变 */
  margin-top: 5%;
  font-size: 2.5rem;
  color: #007BFF;
  text-align: center;
  padding: 20px 0;
  margin-bottom: 20px;
  background-color: rgba(135, 206, 250, 0.7);
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.titleAll::after {
  content: "📰";
  display: inline-block; /* 或者 block */
  font-size: 1.5rem;
  margin-left: 10px;
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

.edit-news-container {
    display: flex;
    justify-content: center;
    width: 100%;
    max-width: 1350px;
    margin: 0 auto;
}

.image-upload-section {
    width: 100%;
    text-align: center;
    background: linear-gradient(135deg, #f9f9f9 30%, #eaeaea);
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    min-height: 400px;
}

.image-upload-section:hover {
    box-shadow: 0 6px 40px rgba(0, 0, 0, 0.1);
}

.upload-demo {
    margin-bottom: 20px;
}

.description-input {
    width: 100%;
    margin-bottom: 20px;
    border: 1px solid #d9d9d9;
    border-radius: 5px;
    padding: 12px;
    font-size: 16px;
    line-height: 1.5;
}

.description-input:focus {
    border-color: #409eff;
    box-shadow: 0 0 5px rgba(64, 158, 255, 0.5);
}

.submit-btn {
    width: 100%;
    background-color: #409eff;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 5px;
    transition: background-color 0.3s ease, transform 0.2s ease;
    margin-top: 30px;
}

.submit-btn:hover {
    background-color: #66b1ff;
    transform: scale(1.02);
}

.newsP {
    text-align: left;
    margin-bottom: 10px;
    font-weight: bold;
    color: #333;
    font-size: 24px;
    line-height: 1.4;
    margin-top: 20px;
}

.image-preview {
    margin: 20px auto;
    width: 280px;
    height: 260px;
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

.preview-img {
    width: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.backEdit {
    font-weight: bold;
    transition: color 0.3s ease;
    margin-left: 5px;
    font-size: 16px;
}

.back {
    cursor: pointer;
    text-align: left;
    font-weight: bold;
    color: #333;
    margin-bottom: 15px;
}

.back :hover {
    color: #409eff;
}



</style>
