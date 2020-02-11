<template>
  <v-app>
    <div class="rooms-page">
      <navbar />
      <div class="rooms-page__container">
        <v-progress-circular
          class="rooms-page__loader"
          indeterminate
          :width="5"
          size="100"
          v-if="isLoading"
        ></v-progress-circular>
        <room
          v-for="room in rooms"
          :key="room.id"
          class="roomcard"
          :creator="room.creator"
          :usersJoined="room.usersJoined"
          :id="room.id"
          :gameStarted="room.gameStarted"
        >
        </room>
      </div>
      <v-btn
        class="rooms-page__button"
        icon
        fab
        @click="createRoomButtonPressed"
        ><v-icon>mdi-plus</v-icon>
      </v-btn>
    </div>
  </v-app>
</template>

<script>
import Room from "@/components/RoomCard.vue";
import axios from "axios";
import baseURL from "../global"

export default {
  components: { Room },
  data() {
    return {
      isLoading: false,
      rooms: []
    };
  },
  methods: {
    createRoomButtonPressed: function() {
      const path = baseURL+"/rooms/";
      axios
        .post(path, { token: localStorage.getItem("authToken") })
        .then(res => {
          var id = res.data.room._id.$oid;
          var newRoom = {
            id: id,
            creator: res.data.room.owner,
            usersJoined: 0,
          };
          this.$data.rooms.push(newRoom);
          this.$router.push("/play/" + id);
        })
        .catch();

      // this.$router.push("/play/" + id);
    }
  },
  created() {
    if(!localStorage.getItem("authToken")) this.$router.push("/login")
    //call the api to get all available rooms
    const path = baseURL+"/rooms/";
    this.$data.isLoading = true;
    axios
      .get(path, { token: localStorage.getItem("authToken") })
      .then(res => {
        this.$data.isLoading = false;
        var rooms = res.data.rooms;
        for (const room of rooms) {
          var newRoom = {
            id: room._id.$oid,
            creator: room.owner,
            usersJoined: room.gamesession.players.length,
            gameStarted: room.gameStarted?true:false

          };
          this.$data.rooms.push(newRoom);
        }
      })
      .catch();
  }
};
</script>
