import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import Navbar from "./components/Navbar.vue";

Vue.config.productionTip = false;

Vue.component("navbar", Navbar);

new Vue({
  created() {
    document.title = this.$route.name + " - CAH";
  },
  router,
  vuetify,
  render: h => h(App)
}).$mount("#app");
