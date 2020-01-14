<template>
  <swiper ref="mySwiper" :options="swiperOption">
    <swiper-slide v-for="player in this.$props.players" :key="player.username">
      <player v-bind="player" ></player>
    </swiper-slide>
    <div
      class="cardCarousel__arrow cardCarousel__arrow--mini swiper-button-prev"
      slot="button-prev"
    >
              <v-icon>  mdi-chevron-left</v-icon>
    </div>
    <div
      class="cardCarousel__arrow cardCarousel__arrow--mini swiper-button-next"
      slot="button-next"
    >
              <v-icon>  mdi-chevron-right</v-icon>
    </div>
  </swiper>
</template>
<script>
import player from "./Player";
import "swiper/dist/css/swiper.css";
import { swiper, swiperSlide } from "vue-awesome-swiper";

export default {
  components: { swiper, swiperSlide, player },
  props: {
    players:Array
  },
  data() {
    return {
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
  },
  mounted(){
    console.log(this.$props);
  }
};
</script>
