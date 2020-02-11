import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import UserAuth from "../views/userAuth.vue";
import Logout from "../views/Logout.vue";

import Play from "../views/Play.vue";
import Game from "../views/Game.vue";
import Profile from "../views/Profile.vue";
import ErrorPage from "../views/ErrorPage.vue";
import About from "../views/About.vue";

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
    component: UserAuth,
    meta: {
      title: "Login"
    }
  },
  {
    path: "/register",
    name: "Register",
    component: UserAuth,
    meta: {
      title: "Register"
    }
  },
  {
    path: "/logout",
    name: "Logout",
    component: Logout
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
    path: "/About",
    name: "About",
    component: About,
    props: true,
    meta: {
      title: "About",
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
