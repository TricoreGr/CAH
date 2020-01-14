<template>
    <div class="inGameUser__wrapper">
    <div class="inGameUser__image-wrapper">
      <span class="inGameUser__username">{{this.$props.username}}</span>
        <img
          class="inGameUser__image slide-in-blurred-top" v-bind:class="[ {'inGameUser__image--played': hasPlayed},{'inGameUser__image--czar': isCzar},{'inGameUser__image--active': isMainUser}]"
          :src="this.$props.imageSrc"
        />
        </div>
        <div class="inGameUser__AttributeWrapper">
          <span class="inGameUser__points">{{points}}</span>
        </div>
      </div>
</template>
<script>
export default {
  props: {
    username:{type:String,default:''},
    imageSrc:{type:String,default:''},
    isCzar:{type:Boolean,default:false},
    isMainUser:{type:Boolean,default:false},
    points:{type:Number,default:10},
    hasPlayed:{type:Boolean,default:false}
  },
};
</script>
