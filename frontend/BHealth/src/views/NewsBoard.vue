<template>
    <div class="newsBoard">
        <div class="banner">
            <img :src="firstImg" class="img" alt="" @click="imgJump">
            <div v-for="(title,titleIndex) in titles" :key="titleIndex"  class="content">
                <transition name="scale">
                    <div v-show="imgIndex===titleIndex" >
                      <span>{{title}}</span>
                    </div>
                  </transition>
            </div>
            <div class="dot-content">
                <div v-for="(item,index) in imgArr.length" :key="index" :class="index===imgIndex?'active':'dot-box'">
                </div>
            </div>
            <div class="arrowShadowL">
              <el-icon size="40" class="left-btn" @click="next(-1)"><ArrowLeftBold /></el-icon>
            </div>
            <div class="arrowShadowR">
              <el-icon size="40" class="right-btn" @click="next(1)"><ArrowRightBold /></el-icon>
            </div>
        </div>
        <div class="bottom">
          <div class="selector">
            <div class="allNews" @click="clickAll()">全部新闻</div>
            <div class="today" @click="clickToday()">今日发布</div>
            <div class="favor" @click="clickFavor()">医院精选</div>
          </div>
          <div class="AllLittleNews">
            <LittleNewsBoard class="LittleNewsBoard"
              v-for="(item,index) in allNews"
              :key="index"
              :imgPath="item.front_image"
              :title="item.title"
              :description="item.discretion"
              @click="jumpToNewsDetail(item.id)"
            />
          </div>
        </div>
    </div>
</template>
<script setup>
import {onMounted, onUnmounted, ref} from 'vue'
import {ArrowLeftBold, ArrowRightBold} from '@element-plus/icons';
import router from "@/router/index.ts";
import LittleNewsBoard from "@/components/NewsBoard/LittleNewsBoard.vue";
import api from "@/api/index.ts";

const imgIndex = ref(0)
const imgArr = ref([]);
const titles = ref([]);
const firstImg = ref('')
const allNews = ref([])
const next = (e) => {
    let currentImg = document.querySelector('.img');
    e>0? imgIndex.value+=1 : imgIndex.value-=1
    if(imgIndex.value >= imgArr.value.length ) {
        imgIndex.value=0
    }
    if(imgIndex.value <0 ) {
        imgIndex.value=imgArr.value.length-1
    }
    currentImg.style.opacity = '0'
    console.log('------', currentImg.src)
    setTimeout(() => {
        currentImg.src= imgArr.value[imgIndex.value]
        currentImg.style.opacity = '1';
    },300)

    resetAutoPlay();
}

//设置自动播放
let autoPlayId;
let delay = 5000;

// 自动播放函数
function autoPlay() {
    next(1);
}

function startAutoPlay() {
    autoPlayId = setInterval(() => {
        autoPlay();
    }, delay);
}

// 清除并重新启动自动播放
function resetAutoPlay() {
    // 清除现有的定时器
    clearInterval(autoPlayId);
    // 重新启动自动播放
    startAutoPlay();
}

onMounted(() => {
    getAllNews();
    startAutoPlay();
});

onUnmounted(() => {
    clearInterval(autoPlayId)
})

//点击图片跳转对应网页
const imgJump = () => {
    router.push({path: '/news'})
}

const getNewsByType = async (type) => {
  allNews.value = await api.getNewsByType({type})
}

const getAllNews = async () => {
  try {
    const res = await api.getAllNews();
    firstImg.value = res.results[0].front_image;
    allNews.value = res.results;
    for (let i = 0; i < 3; i++) {
      imgArr.value.push(res.results[i].front_image);
      titles.value.push(res.results[i].title);
    }
  } catch (error) {
    console.error("Error fetching news:", error);
  }
};

const clickToday = () => {
  console.log('今日发布')
//   激活今日发布
  document.querySelector('.today').classList.add('active')
  document.querySelector('.favor').classList.remove('active')
  document.querySelector('.allNews').classList.remove('active')
  getNewsByType('today')
}

const clickFavor = () => {
  console.log('医院精选')
//   激活医院精选
  document.querySelector('.favor').classList.add('active')
  document.querySelector('.today').classList.remove('active')
  document.querySelector('.allNews').classList.remove('active')
  getNewsByType('favor')
}

const clickAll = () => {
  console.log('全部新闻')
//   激活全部新闻
  document.querySelector('.allNews').classList.add('active')
  document.querySelector('.favor').classList.remove('active')
  document.querySelector('.today').classList.remove('active')
  getNewsByType('all')
  console.log('allNews +++++++++++', allNews)
}

const getNewsById = async (id) => {
  const res = await api.getNewsById({id})
  console.log('res', res)
}

const jumpToNewsDetail = (id) => {
  getNewsById(id)
  router.push({path: '/newsDetail/' + id})
}

</script>
<style scoped lang="less">
.newsBoard {
  margin-top: 64px;
  .banner {
    position: relative;
    display: flex;
    justify-content: center;
    width: 100%;
    max-width: 100%;
    height: 500px;
    overflow: hidden;
    .left-btn, .right-btn {
      width: 0;
    }

    &:hover {
      .left-btn {
        position: absolute;
        cursor: pointer;
        width: auto;

      }

      .right-btn {
        position: absolute;
        cursor: pointer;
        width: auto;
      }
    }

    .img {
      display: none;

      &:first-child {
        display: block;
        height: 60vh;
        opacity: 1;
        transition: opacity 0.5s ease;
      }

      width: 100%;
      overflow: hidden;
      &:hover {
        cursor: pointer;
      }
    }

    .scale-enter-active {
      transition: all 1s ease-in-out;
    }

    .scale-leave-active {
      transition: all 1s linear;
    }

    .scale-enter-from {
      margin-right: 300px;
      opacity: 0;
    }

    .scale-leave-to {
      opacity: 0;
    }

    .content {
      position: absolute;
      top: 50%;
      font-size: 40px;
      color: #fff;
      font-weight: 600;

      &:hover {
        cursor: pointer;
      }
    }

    .dot-content {
      display: flex;
      position: absolute;
      bottom: 20px;
      justify-content: space-around;
      align-items: center;
      width: 100px;
      height: 30px;

      .dot-box {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background-color: #fff;
      }

      .active {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background-color: red;
      }
    }

    .arrowShadowL {
      position: absolute;
      top: 40%;
      left: 30px;
      width: 50px;
      height: 100px;
      background-color: rgba(0, 0, 0, 0.2);
      border-radius: 5%;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .arrowShadowR {
      position: absolute;
      top: 40%;
      right: 30px;
      width: 50px;
      height: 100px;
      background-color: rgba(0, 0, 0, 0.2);
      border-radius: 5%;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .arrowShadowR, .arrowShadowL {
      cursor: pointer;
    }

    .arrowShadowR:hover, .arrowShadowL:hover {
      background-color: rgba(0, 0, 0, 0.5);
    }
  }

  .bottom {

    position: relative;
    width: 1350px;
    //水平居中，位于banner下100px的位置
    margin: 50px auto 0;
    .selector {
      width: 100%;
      height: 80px;
      background-color: #f0f0f0;
      display: flex;
      align-items: center;
      margin: 0 auto;
      .today, .favor, .allNews{
        width: 200px;
        height: 100%;
        display: flex;
        align-items: center;
        cursor: pointer;
        justify-content: center;
        font-size: 20px;
        font-weight: 600;
        font-family: 'Microsoft YaHei',serif;
        color: #666666;
        margin-left: 30px;
      }
      .today {
        margin-left: 60px;
      }
      .favor {
        margin-left: 60px;
      }

      .favor:not(.active):hover, .today:not(.active):hover , .allNews:not(.active):hover{
        color: #000000;
        background-color: #ffffff;
      }
      .favor.active, .today.active, .allNews.active {
        color: #ffffff;
        background-color: #404ada;
      }
    }
    //一行放四个小新闻.每个小新闻的宽度为18%
    .AllLittleNews {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 40px;
      margin: 30px auto 0;
      width: 100%;
      .LittleNewsBoard {
        width: 100%;
        margin-top: 30px;
      }
    }
  }
}
</style>