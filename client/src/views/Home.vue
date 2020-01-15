<template>
  <div class="home">
    <div id="app">
      <v-app>
        <navbar></navbar>
        <v-parallax
          id="hey"
          src="https://static-ssl.businessinsider.com/image/54fda64869bedd6c797376de-1200-600/cards-against-humanity-1.jp2"
          class="parallax"
        >
          <v-btn class="parallax__button" router to="/play">
            PLAY NOW!
          </v-btn>
        </v-parallax>
        <div class="home__container-left">
          <div class="home__container-left--p">
            <span class="home__container-left--title"
              >What is cards against humanity?</span
            >
            <p>
              A famous party icebreaker, Cards Against Humanity is an
              adults-only game for players mature enough to handle the
              intentionally provocative (but often hilarious) topics and
              answers. The goal is to pair the answer and question cards in the
              funniest, most provocative, or cleverest way you can.
            </p>
          </div>
        </div>
        <div class="home__container-right">
          <div class="home__container-right--p">
            <span class="home__container-right--title">How do I play?</span>
            <br />
            <p>
              Each player has 10 white cards. There is a black card in the
              middle which contains a question or a phrase with some words
              missing. Your goal is to play the white card(s) with the funniest
              response to the black card. Every player takes turns in being the
              Card Czar, who decides what the funniest white card is. The first
              player to get 5 points wins!
            </p>
          </div>
        </div>

        <v-btn router to="/play" class="home__button">TRY IT!</v-btn>
      </v-app>
    </div>
  </div>
</template>

<script>
export default {
  name: "home",
  data() {
    return {};
  }
};
</script>
