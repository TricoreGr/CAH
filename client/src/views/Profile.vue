<template>
  <div>
    <navbar />
    <div class="account">
      <div class="account__wrapper slide-in-blurred-top">
        <h1 class="account__username">{{ username }}</h1>
        <img class="account__user-image" :src="img" />
        <div class="account__score-wrapper">
          <div class="account__info-wrapper">
            <span class="account__info-label">Wins</span>
            <span class="account__info">{{ wins }}</span>
          </div>
          <div class="account__info-wrapper">
            <span class="account__info-label">Games</span>
            <span class="account__info">{{ gamesTotal }}</span>
          </div>
        </div>
        <div class="account__info-wrapper">
          <h3 class="account__info-label account__info-label--rank">
            Rank
          </h3>
          <span class="account__info account__info--rank">{{ rank }}</span>
        </div>
        <div class="account__email-wrapper">
          <span class="account__email-label">email</span>
          <span class="account__email">{{ email }}</span>
        </div>
        <v-btn
            rounded
            dark
            @click = "updateAccount"
            class="account__button account__button"
        >
        Update info
        </v-btn>
      </div>
      <v-btn
        rounded
        dark
        @click="overlay = true"
        class="account__button account__button--deleteAccount"
      >
        Delete Account?
      </v-btn>
    </div>
    <v-overlay :value="overlay">
      <div class="account__overlay-wrapper">
        <h3>Are you sure you want to delete your account?</h3>
        <div class="account__overlay-button-wrapper">
          <v-btn
            rounded
            class="account__cancel-button"
            @click="overlay = false"
          >
            Cancel
          </v-btn>

          <v-btn color="primary" rounded @click="deleteAccount">
            Confirm
          </v-btn>
        </div>
      </div>
    </v-overlay>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      username: "StoeBlyat",
      email: "gooduser@cah.com",
      rank: "big Boi", //todo : add ranks
      wins: 3,
      overlay: false,
      gamesTotal: 10,
      img:
        "https://upload.wikimedia.org/wikipedia/commons/4/4d/Star_Wars-_The_Last_Jedi_Japan_Premiere_Red_Carpet-_Adam_Driver_%2827163437599%29_%28cropped%29.jpg"
    };
  },
  methods: {
    fetchData() {
      const path = "http://localhost:5000/users/jwtToUsername";
      axios
        .post(path, { token: localStorage.getItem("authToken") })
        .then(res => {
          this.username = res.data["username"];
          this.email = res.data["email"];
          this.wins = res.data["wins"] ? res.data["wins"] : 0;
          this.gamesTotal = res.data["games"] ? res.data["games"] : 0;
          this.img = res.data["img"];
        })
        .catch(error => {
          //oops
          console.log(error);
        });
    },
    deleteAccount() {
      const path = "http://localhost:5000/users/delete";
      axios
        .delete(path, {data:{ token: localStorage.getItem("authToken") }})
        .then(() => {
          this.$router.push("/Logout");
        })
        .catch(error => {
          //oops
          console.log(error);
        });
    },
    updateAccount() { // Change this because it doesnt work
      const path = "http://localhost:5000/users/update";
      axios
        .update(path, { token: localStorage.getItem("authToken") })
        .then(res => {
          var messsage = res.data["message"];
          if(message == 'Update was successful')  fetchData();
        })
        .catch(error =>{
          console.log(error);
        })
    },
  },
  mounted() {
    this.fetchData();
  }
};
</script>
