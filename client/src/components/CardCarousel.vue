<template>
  <swiper ref="mySwiper" :options="swiperOption">
    <swiper-slide v-for="(text, index) in cardTexts" :key="index" transition="staggered" stagger="5000">
      <card
        v-on:updateSelectedIndex="updateIndex($event)"
        :selectedCardsIndexes="selectedCardsIndexes"
        :index="index"
        :text="text"
        :canBeClicked="canSelectCard"
      ></card>
    </swiper-slide>
    <div class="cardCarousel__arrow swiper-button-prev" slot="button-prev">
              <v-icon> mdi-chevron-left</v-icon>
    </div>
    <div class="cardCarousel__arrow swiper-button-next" slot="button-next">
              <v-icon> mdi-chevron-right</v-icon>
      
    </div>
  </swiper>
</template>
<script>
import card from "./Card";
import "swiper/dist/css/swiper.css";
import { swiper, swiperSlide } from "vue-awesome-swiper";

export default {
  components: { card, swiper, swiperSlide },
  props: {
    cardsToPick: Number,
    selectedCardsIndexes: Array,
    cardTexts:Array
  },
  methods: {
    updateIndex(index) {
      var updatedIndexArray = this.selectedCardsIndexes;
      if (!updatedIndexArray.includes(index)) {
        //if array is being overflown, then remove the first chosen card
        updatedIndexArray.length >= this.cardsToPick
          ? updatedIndexArray.shift()
          : "";
        //add the new card
        updatedIndexArray.push(index);
      }
      //if an index already exists in the array, it means the user chose it to be removed from his selections
      else {
        //find the chosen card index to remove from the cards to be submitted
        let indexOfElementToDelete = updatedIndexArray.indexOf(index);
        //remove that card
        updatedIndexArray.splice(indexOfElementToDelete, 1);
      }
      //update card index array of parent element
      this.$emit("updateSelectedCardsIndexes", updatedIndexArray);
    }
  },
  data() {
    return {
      swiperOption: {
        slidesPerView: 5,
        breakpoints: {
          1542: {
            slidesPerView: 5
          },
          1278: {
            slidesPerView: 4
          },
          1044: {
            slidesPerView: 2
          },
          600: {
            slidesPerView: 2
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
    },
    canSelectCard(){
      return this.cardsToPick>0
    }
  }
};
</script>
