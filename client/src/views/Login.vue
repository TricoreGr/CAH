<template>
  <v-app>
    <div class="login">
      <div class="login__headline-wrapper">
        <h1 class="login__title">
          CARDS AGAINST HUMANITY
        </h1>
        <h3 class="login__subTitle">
          IEEEDIOTS EDITION
        </h3>
      </div>
      <div class="login__card-wrapper">
        <div class="card card--czar card--login-czar">
          <div class="card__content-wrapper">
            <div class="card__input-wrapper">
              <span class="card__text">
                my username is
              </span>
              <span class="card__input">
                {{ czarName }}
              </span>
            </div>
            <div class="card__input-wrapper">
              <span class="card__text">
                and my password
              </span>
              <span class="card__input">
                {{ czarPassword }}
              </span>
            </div>
          </div>
          <span class="card__signature">CAH</span>
        </div>

        <span class="login__card-tip scale-up-center">
          type in this card
          <br />
          comrade!
          <span class="login__card-tip-arrow ">
            ⟶
          </span>
        </span>
        <div class="card card--player card--login-input">
          <div class="card__content-wrapper">
            <div class="card__input-wrapper">
              <span class="card__input">
                <v-text-field
                  label="Username"
                  :type="'text'"
                  :rules="[rules.required, rules.counter]"
                  @input="syncUsername"
                  value=""
                  v-model="username"
                  counter
                ></v-text-field>
              </span>
            </div>
            <div class="card__input-wrapper">
              <span class="card__input">
                <v-text-field
                  label="Password"
                  @input="syncPassword"
                  :rules="[rules.required]"
                  :type="'password'"
                  value="lololo"
                  v-model="password"
                ></v-text-field>
              </span>
            </div>
          </div>
          <div class="card__signature-wrapper">
            <span class="card__error">{{ error }}</span>
            <span class="card__signature">CAH</span>
          </div>
        </div>
      </div>
      <div class="login__buttons-wrapper">
        <v-btn
          rounded
          color="black"
          active-class="test"
          @click.native="login"
          dark
          >LOG IN, FRIEND!</v-btn
        >
        <v-btn text small>Forgot Password?</v-btn>
      </div>
    </div>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  methods: {
    syncUsername() {
      //show username on black card
      if (this.username.length < 20) this.czarName = this.username;
      if (this.username.length == 0) this.czarName = "_________________";
    },
    syncPassword() {
      //show our password gimmick based on the letters of user's typed password
      const text = "veryStr0nkP4ssw0rd";
      var passLength = this.password.length;
      this.czarPassword = text.substring(0, passLength);
      if (passLength == 0) this.czarPassword = "_________________";
    },
    login() {
      //url for post method
      const path = "http://localhost:5000/users/" + this.username + "/auth";
      //form rules
      if (
        this.username &&
        this.username.length <= 20 &&
        this.password.length > 0
      )
        //use axios for requests
        axios
          .post(path, { password: this.password })
          .then(res => {
            if (res.data.token) {
              //save the auth token in browser
              localStorage.setItem("authToken", res.data.token);
              //redirect to homepage
              this.$router.push("/");
            }
            //auth failed
            else this.error = res.data.message;
          })
          .catch(error => {
            //oops
            console.log(error);
          });
    }
  },
  data() {
    return {
      rules: {
        //vuetify form rules
        counter: value => value.length <= 20 || "Max 20 characters",
        required: value => !!value || "Required."
      },
      //default values for cards
      username: "",
      password: "",
      czarName: "_________________",
      czarPassword: "_________________",
      error: ""
    };
  },
  mounted() {
    //set default text on mount
    this.syncUsername();
    this.syncPassword();
  }
};
</script>
