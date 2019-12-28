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
    name: "Home",
    component: Home,
    meta: {
      title: "Home"
    }
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: {
      title: "Register"
    }
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: {
      title: "Register"
    }
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    meta: {
      title: "Profile"
    }
  },
  {
    path: "/play",
    name: "Play",
    component: Play,
    meta: {
      title: "Play",
      requiresAuth: true
    }
  },
  {
    path: "/play/:gameId",
    name: "Game",
    component: Game,
    props: true,
    meta: {
      title: "Game",
      requiresAuth: true
    }
  },
  {
    path: "*",
    name: "Error",
    component: ErrorPage,
    meta: {
      title: "Error"
    }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
