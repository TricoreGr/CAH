<template>
  <div 
    class="card"
    v-on:click="selectCard"
    :class="[isCzar ? 'card--czar' : '', (isSelected && selectedCardIndex==index) ? 'card--selected': '']">
    <div class="card__content-wrapper">
      <span class="card__text">
        {{text}}
      </span>
    </div>
    <span class="card__signature">CAH</span>
  </div>
</template>
<script>
export default {
    props:{
        selectedCardIndex:Number,
        index:Number,
        isCzar:Boolean,
        text:String,
    },
    methods: {
      selectCard(){
        if(this.selectedCardIndex!=this.index){
          this.isSelected=true;
          this.$emit('updateSelectedIndex', this.index);
        }
        else
          this.isSelected=!this.isSelected;

      }
    },
    data(){
      return{
      isSelected:false
      }
    }
}
</script>