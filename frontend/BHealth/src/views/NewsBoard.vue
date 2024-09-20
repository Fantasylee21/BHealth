<template>
    <div class="newsBoard">
        <div class="banner">
            <img src="@/assets/slide1.png" class="img" alt="" @click="imgJump">
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
            <div class="today" @click="clickToday()">今日发布</div>
            <div class="favor" @click="clickFavor()">医院精选</div>
          </div>
          <div class="AllLittleNews">
            <LittleNewsBoard class="LittleNewsBoard" v-for="(item,index) in allNews" :key="index" :imgPath="item.imgPath" :title="item.title" :description="item.description"/>
          </div>
        </div>
    </div>
</template>
<script setup>
import {onMounted, onUnmounted, ref} from 'vue'
import { ArrowLeftBold, ArrowRightBold } from '@element-plus/icons';
import router from "@/router/index.ts";
import LittleNewsBoard from "@/components/NewsBoard/LittleNewsBoard.vue";

const imgIndex = ref(0)
const imgArr = [
  'src/assets/slide1.png',
  'src/assets/slide2.png',
  'src/assets/slide1.png',
]
const titles = [
    '原神','启动','原神'
]
const next = (e) => {
    let currentImg = document.querySelector('.img');
    e>0? imgIndex.value+=1 : imgIndex.value-=1
    if(imgIndex.value >= imgArr.length ) {
        imgIndex.value=0
    }
    if(imgIndex.value <0 ) {
        imgIndex.value=imgArr.length-1
    }
    currentImg.style.opacity = '0'
    console.log('------', currentImg.src)
    setTimeout(() => {
        currentImg.src= imgArr[imgIndex.value]
        currentImg.style.opacity = '1';
    },300)
}

//设置自动播放
let autoPlayId
function autoPlay() {
    next(1)
}

onMounted(() => {
    autoPlayId = setInterval(() => {
        autoPlay()
    }, 5000)
})

onUnmounted(() => {
    clearInterval(autoPlayId)
})

//点击图片跳转对应网页
const imgJump = () => {
    router.push({path: '/news'})
}
const allNews = ref ([
  {
    imgPath: 'src/assets/slide1.png',
    title: "原神",
    description: '原神是一款开放世界冒险游戏，由中国游戏公司miHoYo开发。游戏于2020年9月28日正式发布，支持Windows、PlayStation 4、iOS和Android平台。'
  },
  {
    imgPath: 'src/assets/slide2.png',
    title: "启动",
    description: '启动是一款开放世界冒险游戏，由中国游戏公司miHoYo开发。游戏于2020年9月28日正式发布，支持Windows、PlayStation 4、iOS和Android平台。'
  },
  {
    imgPath: 'src/assets/slide1.png',
    title: "原神",
    description: '原神是一款开放世界冒险游戏，由中国游戏公司miHoYo开发。游戏于2020年9月28日正式发布，支持Windows、PlayStation 4、iOS和Android平台。'
  },
  {
    imgPath: 'src/assets/slide2.png',
    title: "启动",
    description: '启动是一款开放世界冒险游戏，由中国游戏公司miHoYo开发。游戏于2020年9月28日正式发布，支持Windows、PlayStation 4、iOS和Android平台。'
  },
  {
    imgPath: 'src/assets/slide1.png',
    title: "原神",
    description: '原神是一款开放世界冒险游戏，由中国游戏公司miHoYo开发。游戏于2020年9月28日正式发布，支持Windows、PlayStation 4、iOS和Android平台。'
  }
])

const clickToday = () => {
  console.log('今日发布')
//   激活今日发布
  document.querySelector('.today').classList.add('active')
  document.querySelector('.favor').classList.remove('active')
}

const clickFavor = () => {
  console.log('医院精选')
//   激活医院精选
  document.querySelector('.favor').classList.add('active')
  document.querySelector('.today').classList.remove('active')
}

</script>
<style scoped lang="less">
.newsBoard {

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
      .today, .favor {
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
      .favor {
        margin-left: 60px;
      }
      .favor:not(.active):hover, .today:not(.active):hover {
        color: #000000;
        background-color: #ffffff;
      }
      .favor.active, .today.active {
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