<template>
  <div>
    <navbar />
    <div class="account">
      <div class="account__wrapper slide-in-blurred-top">
        <h1 class="account__username">{{ username }}</h1>
        <div class="account__user-image-wrapper">
          <v-progress-circular
            indeterminate
            :width="2"
            v-if="isLoading"
          ></v-progress-circular>
          <img
            @click="
              updateModal = true;
              overlay = true;
            "
            class="account__user-image"
            :src="img"
          />
        </div>
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
      </div>
      <v-btn
        rounded
        dark
        @click="
          overlay = true;
          deleteAccountModal = true;
        "
        class="account__button account__button--deleteAccount"
      >
        Delete Account?
      </v-btn>
    </div>
    <v-overlay :value="overlay">
      <div class="account__overlay-wrapper">
        <v-card v-if="updateModal">
          <v-form ref="form">
            <v-card-text>
              <v-card-title>
                <span class="headline">User Profile</span>
              </v-card-title>

              <v-text-field
                label="User Image"
                v-model="newImage"
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="resetModal"
                >Close</v-btn
              >
              <v-btn
                color="blue darken-1"
                text
                @click="
                  dialog = false;
                  userUpdate();
                "
                >Save</v-btn
              >
            </v-card-actions>
          </v-form>
        </v-card>

        <div v-if="deleteAccountModal">
          <h3>Are you sure you want to delete your account?</h3>
          <div class="account__overlay-button-wrapper">
            <v-btn rounded class="account__cancel-button" @click="resetModal">
              Cancel
            </v-btn>

            <v-btn color="primary" rounded @click="deleteAccount">
              Confirm
            </v-btn>
          </div>
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
      username: "Loading...",
      email: "gooduser@hehe.com",
      rank: "big Boi", //todo : add ranks
      wins: 3,
      overlay: false,
      gamesTotal: 10,
      isLoading: false,
      img:"",
      updateModal: false,
      deleteAccountModal: false,
      newImage: this.img,
      newUsername: this.newUsername,
      rules: {
        //vuetify form rules
        counter: value =>
          value ? value.length <= 20 || "Max 20 characters" : "",
        required: value => (value ? !!value || "Required." : "")
      },
      serverErrors: {
        usernameExists: ""
      }
    };
  },
  methods: {
    fetchData() {
      this.isLoading = true;
      const path = "http://localhost:5000/users/jwtToUsername";
      axios
        .post(path, { token: localStorage.getItem("authToken") })
        .then(res => {
          this.username = res.data["username"];
          this.email = res.data["email"];
          this.wins = res.data["wins"] ? res.data["wins"] : 0;
          this.gamesTotal = res.data["games"] ? res.data["games"] : 0;
          this.img = res.data["img"];
          this.isLoading = false;
        })
        .catch(error => {
          //oops
          console.log(error);
        });
    },
    deleteAccount() {
      this.isLoading = true;
      const path = "http://localhost:5000/users/"+this.username;
      axios
        .delete(path, { data: { token: localStorage.getItem("authToken") } })
        .then(() => {
          this.$router.push("/logout");
          this.isLoading = false;

        })
        .catch(error => {
          //oops
          console.log(error);
        });
    },
    resetModal() {
      this.updateModal = false;
      this.deleteAccountModal = false;
      this.overlay = false;
    },
    userUpdate() {
      this.resetModal();
      var headers = {
        "Content-Type": "application/json"
      };
      //url for post method
      const path = "http://localhost:5000/users/" + this.username;
      //form rules
      if (this.$refs.form.validate())
        //use axios for requests
        axios
          .put(
            path,
            {
              token: localStorage.getItem("authToken"),
              image: this.newImage
            },
            headers
          )
          .then(res => {
            console.log(res);
            if (res.status == 200) {
              this.fetchData();
            }
          })
          .catch(error => {
            //oops
            console.log(error);
          });
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>
