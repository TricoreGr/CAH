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
          v-for="link in linksAuthenticated"
          :key="link.name"
          exact
          :to="link.to"
        >
          <v-btn text>
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
              v-for="link in linksAuthenticated"
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
      linksAuthenticated: [
        {
          name: "Home",
          to: "/"
        },
        {
          name: "Play Now!",
          to: "/play"
        },
        {
          name: "Profile",
          to: "/profile"
        },
        {
          name: "Log Out",
          to: "/logout"
        }
      ]
    };
  }
};
</script>

<style lang="scss"></style>
