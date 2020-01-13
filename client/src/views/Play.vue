<template>
  <div>
    <v-app>
      <navbar />
      <div
        style="
        display: flex;
        flex-flow: row wrap;
        min-width: 300px;
        justify-content: space-around; 
        margin: 40px auto; 
        overflow: hidden;"
      >
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
        style="
        background-color: green;
        color: white;
        position: fixed;
        bottom: 50px;
        right: 50px;
        height: 70px;
        width: 70px;
        "
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

export default {
  components: { Room },
  data() {
    return {
      rooms: [
        {
          id: "21dfkfd",
          creator: "Dima",
          usersJoined: 8
        },
        {
          id: "21dfk5d",
          creator: "Giapa",
          usersJoined: 2
        },
        {
          id: "21df32fd",
          creator: "Kalovelo",
          usersJoined: 6
        }
      ]
    };
  },
  methods: {
    createRoomButtonPressed: function() {
      //post room method to backend
      var newRoom = {
        id: "2325dvd2",
        creator: "Stougaros",
        usersJoined: 0
      };
      this.$data.rooms.push(newRoom);
    }
  },
  created() {
    //call the api to get all available rooms
  }
};
</script>
