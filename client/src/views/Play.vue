<template>
  <div>
    <navbar />
    <v-app>
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
    createRoomButtonPressed() {

    }
  },
  created() {
    //call the api to get all available rooms
  }
};
</script>
