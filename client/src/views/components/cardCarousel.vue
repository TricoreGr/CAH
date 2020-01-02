<template>
  <swiper ref="mySwiper" :options="swiperOption">
    <swiper-slide v-for="(text,index) in Texts" :key="index">
      <card v-on:updateSelectedIndex="updateIndex($event)" v-model="selectedCardIndex" :selectedCardIndex="selectedCardIndex" :index="index" :text=text></card>
    </swiper-slide>
    <div class="cardCarousel__arrow swiper-button-prev" slot="button-prev">↼</div>
    <div class="cardCarousel__arrow swiper-button-next" slot="button-next">⇁</div>
  </swiper>
</template>
<script>
import card from "./card";
import "swiper/dist/css/swiper.css";
import { swiper, swiperSlide } from "vue-awesome-swiper";

export default {
  components: { card, swiper, swiperSlide },
  methods: {
      updateIndex(index){
        this.selectedCardIndex = index;
      }
    },
  data() {
    return {
      Texts:[
          "lalalalal",
          "lololololo",
          "lelelelelle",
          "lalalallalala",
          "lululululuulu",
          "lelelelelle",
          "lelelelelle",
          "lelelelelle",

        ],
        selectedCardIndex:-1,
        swiperOption: {
          slidesPerView: 5,
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
