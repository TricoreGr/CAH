<template>
  <div class="home">
    <h1>HOME</h1>
    <div id="app">
      <v-app light>
        <v-content>
          <section>
            <v-parallax :src="img1" height="600">
              <v-layout column align-center justify-center class="white--text">
                <img src="assets/vuetify.png" alt="Vuetify.js" height="200" />
                <h1 class="white--text mb-2 display-1 text-center">
                  Parallax Template
                </h1>
                <div class="subheading mb-4 text-center">
                  Powered by Vuetify
                </div>
                <v-btn
                  class="mt-12"
                  color="blue lighten-2"
                  dark
                  large
                  href="/pre-made-themes"
                >
                  Get Started
                </v-btn>
              </v-layout>
            </v-parallax>
          </section>
        </v-content>
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
