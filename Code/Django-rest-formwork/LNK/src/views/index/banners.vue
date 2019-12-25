<template>
  <div class="banner-warp">
    <swiper :options="swiperOption">
      <swiper-slide v-for="item in banners" :key="item.goods">
        <router-link :to="'/app/home/productDetail/'+item.goods" target="_blank">
          <img :src="item.image" alt="">
        </router-link>
      </swiper-slide>
      <div class="swiper-pagination" slot="pagination"></div>
    </swiper>
  </div>

</template>

<script>
import 'swiper/dist/css/swiper.css'

import { swiper, swiperSlide } from 'vue-awesome-swiper'
import {bannerGoods} from '../../api/api'

export default {
  data () {
    return {
      swiperOption: {
        pagination: {
          el: '.swiper-pagination',
          clickable: true
        },
        autoplay: {
          delay: 3000, // 时间间隔
          stopOnLastSlide: false, // 到最后一张是否停止
          disableOnInteraction: false // 用户操作之后，是否禁止自动播放
        }
      },
      banners: []
    }
  },
  created () {
    this.getBanner()
  },
  methods: {
    getBanner () {
      bannerGoods().then(response => {
        // console.log(response.data)
        this.banners = response.data
      }).catch(error => {
        console.log(error)
      })
    }
  },
  components: {
    swiper,
    swiperSlide
  }
}
</script>

<style scoped>
.banner-warp{
  height:300px;
}
</style>
