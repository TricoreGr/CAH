<template>
  <nav>
    <v-toolbar flat color="transparent" class="navbar">
      <v-toolbar-title> {{ this.$route.name }} </v-toolbar-title>
      <v-spacer></v-spacer>
      <div
        v-if="this.$vuetify.breakpoint.mdAndUp"
        class="navbar-link-container"
      >
        <router-link
          active-class="navbar-link--active"
          class="navbar-link"
          v-for="link in appropriateLinks"
          :key="link.name"
          exact
          :to="link.to"
        >
          <v-btn class="navbar-button" text>
            {{ link.name }}
          </v-btn>
        </router-link>
      </div>

      <div v-else>
        <v-menu class="navbar-menu--mobile" offset-y>
          <template v-slot:activator="{ on }">
            <v-btn icon v-on="on">
              <v-icon>mdi-menu</v-icon>
            </v-btn>
          </template>
          <v-list class="navbar-menu--mobile">
            <v-list-item
              v-for="link in appropriateLinks"
              :key="link.name"
              router
              :to="link.to"
              active-class="navbar-link--active-mobile"
            >
              <v-list-item-title> {{ link.name }} </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </v-toolbar>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      allPageLinks: [
        {
          name: "Home",
          to: "/",
          nonAuthenticated: true
        },
        {
          name: "Play Now!",
          to: "/play",
          nonAuthenticated: false
        },
        {
          name: "Profile",
          to: "/profile",
          nonAuthenticated: false
        },
        {
          name: "Log Out",
          to: "/logout",
          nonAuthenticated: false
        },
        {
          name: "Log In",
          to: "/login",
          nonAuthenticated: true
        },
        {
          name: "Register",
          to: "/register",
          nonAuthenticated: true
        }
      ]
    };
  },
  computed: {
    appropriateLinks() {
      var userIsAuthenticated = !!localStorage.getItem("authToken");
      var links = [];
      var currentLink;

      if (!userIsAuthenticated) {
        console.log(userIsAuthenticated);
        for (currentLink of this.$data.allPageLinks) {
          if (currentLink.nonAuthenticated) links.push(currentLink);
        }
      } else {
        links.push(this.$data.allPageLinks[0]);
        for (currentLink of this.$data.allPageLinks) {
          if (!currentLink.nonAuthenticated) links.push(currentLink);
        }
      }

      return links;
    }
  }
};
</script>

<style lang="scss"></style>
