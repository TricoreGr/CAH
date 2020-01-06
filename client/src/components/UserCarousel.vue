<template>
  <swiper ref="mySwiper" :options="swiperOption">
    <swiper-slide v-for="text in 10" :key="text">
      <player></player>
    </swiper-slide>
    <div
      class="cardCarousel__arrow cardCarousel__arrow--mini swiper-button-prev"
      slot="button-prev"
    >
      ↼
    </div>
    <div
      class="cardCarousel__arrow cardCarousel__arrow--mini swiper-button-next"
      slot="button-next"
    >
      ⇁
    </div>
  </swiper>
</template>
<script>
import player from "./Player";
import "swiper/dist/css/swiper.css";
import { swiper, swiperSlide } from "vue-awesome-swiper";

export default {
  components: { swiper, swiperSlide, player },
  data() {
    return {
      Texts: [
        "lalalalal",
        "lololololo",
        "lelelelelle",
        "lalalallalala",
        "lululululuulu"
      ],
      swiperOption: {
        slidesPerView: 8,
        // init: false,
        breakpoints: {
          1542: {
            slidesPerView: 5
          },
          1278: {
            slidesPerView: 4
          },
          1044: {
            slidesPerView: 3
          },
          600: {
            slidesPerView: 3
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
