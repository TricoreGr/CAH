<template>
  <div class="inGame">
    <div class="inGame__statusWrapper">
      <v-btn
        rounded
        color="black"
        @click.native="login"
        dark
      >
        QUIT
      </v-btn>
      <div class="inGame__roundWrapper">
        <span class="inGame__round">
          ROUND
        </span>
        <span class="inGame__round">
          {{currentRound}} / {{totalRounds}}
        </span>
      </div>
      <player></player>
    </div>
    <div class="inGame__mainCardWrapper">
      <card
        isCzar
        text="Exercitation sint Lorem deserunt excepteur aliquip laboris in
            ullamco veniam dolore nostrud."
      ></card>
      <div class="inGame__chatButtonWrapper">
        <v-btn rounded color="black" dark>
          CHAT
        </v-btn>
        <div class="inGame__chatNotification">
          !
        </div>
      </div>
    </div>
    <div class="inGame__cardCarouselWrapper">
      <cardCarousel></cardCarousel>
    </div>
    <div class="inGame__userCarouselWrapper">
      <userCarousel></userCarousel>
    </div>
  </div>
</template>
<script>
import cardCarousel from "./components/cardCarousel";
import card from "./components/card";
import player from "./components/player";
import userCarousel from './components/userCarousel'
export default {
  components: {
    cardCarousel,
    card,
    player,
    userCarousel
  },
  data() {
    return {
      currentRound:1,
      totalRounds:6
    }
  }
};
</script>
