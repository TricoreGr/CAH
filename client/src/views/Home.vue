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
          <v-btn class="parallax__button">
            PLAY NOW!
          </v-btn>
        </v-parallax>
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
