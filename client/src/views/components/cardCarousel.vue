<template>
  <swiper ref="mySwiper" :options="swiperOption">
    <swiper-slide v-for="index in 10" :key="index">
      <card text="test test test test test test test test test test test test test test test "></card>
    </swiper-slide>
    <div class="swiper-button-prev" slot="button-prev">↼</div>
    <div class="swiper-button-next" slot="button-next"></div>
  </swiper>
</template>
<script>
import card from "./card";
import "swiper/dist/css/swiper.css";
import { swiper, swiperSlide } from "vue-awesome-swiper";

export default {
  components: { card, swiper, swiperSlide },
  data() {
    return {
        swiperOption: {
          slidesPerView: 6,
          // init: false,
          breakpoints: {
            1542: {
              slidesPerView: 5,
            },
            1278: {
              slidesPerView: 4,
            },
            1044: {
              slidesPerView: 3,
            },
            600: {
              slidesPerView: 2,
            }
          },  
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev"
        }
      }
    };
  },
  computed: {
    swiper() {
      return this.$refs.mySwiper.swiper;
    }
  }
};
</script>
