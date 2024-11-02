<template>
  <div class="newsDetail">
    <div class="news-detail-container">
      <h1 class="news-title">{{ newsDetail.title }}</h1>
      <img :src="newsDetail.front_image" alt="News Front Image" class="news-image" />
      <div v-html="newsDetail.content" class="news-content"></div>
      <p class="news-time"><strong>创建时间:</strong> {{ newsDetail.create_time }}</p>
      <p class="news-time"><strong>更新时间:</strong> {{ newsDetail.update_time }}</p>

      <p v-if="newsDetail.discretion" class="news-discretion"><strong>简介:</strong> {{ newsDetail.discretion }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import api from "@/api";
import { useRoute } from "vue-router";

const getNewsDetail = async () => {
    const $route = useRoute();
    const id = $route.params.id;
    const res = await api.getNewsDetail({ id });
    console.log('News Detail:', res.data);
    newsDetail.value = res;
    newsDetail.value.create_time = formatTime(newsDetail.value.create_time);
    newsDetail.value.update_time = formatTime(newsDetail.value.update_time);
    console.log('newsDetail:', newsDetail.value);
}

interface NewsDetail {
    id: number
    title: string
    content: string
    front_image: string
    type: string
    create_time: string
    update_time: string
    discretion: string
}

const newsDetail = ref<NewsDetail>({
    id: 0,
    title: '',
    content: '',
    front_image: '',
    type: '',
    create_time: '',
    update_time: '',
    discretion: ''
})

onMounted(() => {
    getNewsDetail();
})

const formatTime = (time: string) => {
    const date = new Date(time);
    return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`
}
</script>

<style scoped>
.newsDetail {
    margin: 0 auto;
    width: 100%;
    max-width: 1350px;
    display: flex;
    justify-content: center;
}

.news-detail-container {
    width: 100%;
    padding: 20px;
    margin-top: 100px;
    background: #f9f9f9; /* Light background color for contrast */
    border-radius: 8px; /* Rounded corners */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
}

.news-title {
    font-size: 2rem;
    margin-bottom: 15px;
    color: #333; /* Darker title color */
    border-bottom: 2px solid #e0e0e0; /* Underline for the title */
    padding-bottom: 10px; /* Space under the title */
}

.news-image {
    width: 100%;
    object-fit: cover;
    margin: 20px 0;
    border-radius: 8px; /* Rounded corners for the image */
}

.news-content {
    font-size: 1rem;
    line-height: 1.6;
    color: #555; /* Slightly lighter text color for content */
}

.news-type, .news-time, .news-discretion {
    font-size: 0.9rem; /* Smaller font size for supplementary info */
    color: #777; /* Lighter color for less emphasis */
    margin: 10px 0; /* Space between lines */
}

h1 {
    font-size: 2rem;
    margin-bottom: 10px;
}
</style>
