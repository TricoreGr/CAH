<template v-if="usersJoined<8">
  <v-card class="room-card" :class="{'room-card--gameStarted':gameStarted}">
    <v-card-title class="room-card__title">{{ creator }}'s room</v-card-title>
    <div class="room-card__subcontainer">
      <v-btn class="room-card__button" :disabled="gameStarted" @click="buttonPressed(usersJoined)">
        {{gameStarted?"PLAYING":"JOIN"}}
      </v-btn>
      <span
        class="room-card__size-label"
        :class="{ 'room-card__size-label--full': roomIsFull }"
        >{{ usersJoined }}/8</span
      >
    </div>
  </v-card>
</template>

<script>
export default {
  props: {
    creator: String,
    usersJoined: Number,
    id: String,
    gameStarted:Boolean
  },
  methods: {
    buttonPressed(usersJoined) {
      if (usersJoined > 7) return;
      var url = this.$props.id;
      this.$router.push("/play/" + url);
    }
  },
  computed: {
    roomIsFull() {
      return this.$props.usersJoined > 7;
    }
  }
};
</script>
