<template>
  <div class="rooms-page">
    <v-app>
      <navbar />
      <div class="rooms-page__container">
        <room
          v-for="room in rooms"
          :key="room.id"
          class="roomcard"
          :creator="room.creator"
          :usersJoined="room.usersJoined"
          :id="room.id"
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
    </v-app>
  </div>
</template>

<script>
import Room from "@/components/RoomCard.vue";
import axios from "axios";

export default {
  components: { Room },
  data() {
    return {
      rooms: []
    };
  },
  methods: {
    createRoomButtonPressed: function() {
      const path = "http://localhost:5000/rooms/";
      axios
        .post(path, { token: localStorage.getItem("authToken") })
        .then(res => {
          var id = res.data.room._id.$oid;
          var newRoom = {
            id: id,
            creator: res.data.room.owner,
            usersJoined: 0
          };
          this.$data.rooms.push(newRoom);
          this.$router.push("/play/" + id);
        })
        .catch(error => {
          console.log(error);
        });

      // this.$router.push("/play/" + id);
    }
  },
  created() {
    //call the api to get all available rooms
    const path = "http://localhost:5000/rooms/";
    axios
      .get(path, { token: localStorage.getItem("authToken") })
      .then(res => {
        var rooms = res.data.rooms;
        for (const room of rooms) {
          var newRoom = {
            id: room._id.$oid,
            creator: room.owner,
            usersJoined: room.gamesession.players.length
          };
          this.$data.rooms.push(newRoom);
        }
      })
      .catch(error => {
        console.log(error);
      });
  }
};
</script>
