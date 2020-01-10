<template>
    <div class="inGameUser__wrapper">
        <img
          class="inGameUser__image" v-bind:class="[ {'inGameUser__image--czar': isCzar},{'inGameUser__image--active': isMainUser}]"
          src="https://upload.wikimedia.org/wikipedia/commons/4/4d/Star_Wars-_The_Last_Jedi_Japan_Premiere_Red_Carpet-_Adam_Driver_%2827163437599%29_%28cropped%29.jpg"
        />
        <div class="inGameUser__AttributeWrapper">
          <span class="inGameUser__isCzar">{{isCzar?'Czar' : ''}} </span>
          <span class="inGameUser__points">{{points}}</span>
        </div>
      </div>
</template>
<script>
export default {
  data() {
    return {
        points:10,
        isCzar:true,
        isMainUser:false
    }
    }
};
</script>
