<template>
  <div
    class="card tilt-in-top-1"
    v-on:click="selectCard"
    :class="[
      isCzar ? 'card--czar' : '', 
      selectedCardsIndexes //check if selectedCardsIndexes has been passed as a prop
      && selectedCardsIndexes.includes(index) ? 'card--selected' : ''
    ]"
  >
    <div class="card__content-wrapper">
      <span class="card__text">
        {{ text }}
      </span>
    </div>
    <span class="card__signature">CAH</span>
  </div>
</template>
<script>
export default {
  props: {
    selectedCardsIndexes: Array,
    index: Number,
    isCzar: Boolean,
    text: String,
    canBeClicked:Boolean
  },
  methods: {
    selectCard() {
      if(this.canBeClicked)
          this.$emit("updateSelectedIndex", this.index);
    }
  },
  data() {
    return {
      isSelected: false
    };
  },
};
</script>
