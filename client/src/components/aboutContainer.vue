<template>
      <v-app>
        <div class="about">
                <div class="about__single-image-wrapper">
                    <div class="about__image-wrapper">
                    <div  ref="imageRef" @mouseenter="hoverAnimation" @mouseleave="hoverAnimation" v-bind:style="`background-image:url(`+getHoverStatus()+')'" class="about__image">
                    </div>
                    </div>
                    <h3 class="about__name">{{name}}</h3>
                    <div class="about__image-text">
                        {{information}}
                    </div>
                    <a :href="link" target="_blank" class="about__image-link"> Spam this boi </a>
                </div>
            </div>
      </v-app>
</template>

<script>
import anime from "animejs/lib/anime.es.js";
export default {
  props: {
        images:Array,
        isHovered:Boolean,
        information:String,
        name:String,
        link:String
  },
  methods:{
      hoverAnimation(){
          var canChangePhoto = true;
          anime({
              targets:this.$refs.imageRef,
              duration:150,
              opacity:[1,0],
              complete:()=>{
                  anime({
              targets:this.$refs.imageRef,
              duration:150,
              opacity:[0,1],
              update:(anim)=>{
                  if(Math.round(anim.progress)>20 && canChangePhoto)
                  {this.isHovered=!this.isHovered;
                  canChangePhoto=false}
              }
              })
              }
      })
  },
  getHoverStatus(){
      return this.isHovered? this.images[1]:this.images[0]
  }
  }
};
</script>
