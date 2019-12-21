import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Play from "../views/Play.vue";
import Game from "../views/Game.vue";
import Profile from "../views/Profile.vue";
import ErrorPage from "../views/ErrorPage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/login",
    name: "login",
    component: Login
  },
  {
    path: "/register",
    name: "register",
    component: Register
  },
  {
    path: "/profile",
    name: "profile",
    component: Profile
  },
  {
    path: "/play",
    name: "play",
    component: Play,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/play/:gameId",
    name: "game",
    component: Game,
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "*",
    name: "error",
    component: ErrorPage
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});


export default router;
