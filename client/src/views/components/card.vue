<template>
  <div 
    class="card"
    v-bind:class="{ 'card--czar': isCzar}">
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
        isCzar:Boolean,
        text:String
    },
}
</script>