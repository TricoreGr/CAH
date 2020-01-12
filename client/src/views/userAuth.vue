<template>
  <v-app>
    <div class="userAuth">
      <div class="userAuth__headline-wrapper">
        <h1 class="userAuth__title">
          CARDS AGAINST HUMANITY
        </h1>
        <h3 class="userAuth__subTitle">
          IEEEDIOTS EDITION
        </h3>
      </div>
      <div class="userAuth__card-wrapper">
        <div
          class="card card--czar card--userAuth-czar"
          :class="[
            formType == 'login' ? 'flip-vertical-right' : 'flip-vertical-left'
          ]"
        >
          <div class="card__content-wrapper">
            <div class="card__input-wrapper">
              <span class="card__text">
                my username is
              </span>
              <span class="card__input">
                {{ czarName }}
              </span>
            </div>
            <div class="card__input-wrapper" v-if="this.formType == 'signup'">
              <span class="card__text">
                my email is
              </span>
              <span class="card__input">
                {{ czarEmail }}
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

        <span class="userAuth__card-tip scale-up-center">
          type in this card
          <br />
          comrade!
          <span class="userAuth__card-tip-arrow ">
            ⟶
          </span>
        </span>
        <v-form
          ref="form"
          class="card card--player card--userAuth-input"
          :class="[
            formType == 'login' ? 'flip-vertical-right' : 'flip-vertical-left'
          ]"
        >
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
                  :error-messages="serverErrors.usernameExists"
                ></v-text-field>
                <v-text-field
                  label="Email"
                  :type="'text'"
                  :rules="rules.emailRules"
                  @input="syncEmail"
                  value=""
                  v-model="email"
                  :error-messages="serverErrors.emailExists"
                  v-if="this.formType == 'signup'"
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
        </v-form>
      </div>
      <div class="userAuth__buttons-wrapper">
        <v-btn
          rounded
          color="black"
          @click.native="submitHandle"
          dark
          >{{ this.formType == "login" ? "LOG IN" : "SIGN UP" }}, FRIEND!</v-btn
        >
        <v-btn text small @click.native="toggleForm"
          >{{ this.formType == "login" ? "SIGN UP" : "LOG IN" }}?</v-btn
        >
        <!-- <v-btn text small>Forgot Password?</v-btn> -->
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
    syncEmail() {
      //show username on black card
      if (this.email.length < 20) this.czarEmail = this.email;
      if (this.email.length == 0) this.czarEmail = "_________________";
    },
    syncPassword() {
      //show our password gimmick based on the letters of user's typed password
      const text = "veryStr0nkP4ssw0rd";
      var passLength = this.password.length;
      this.czarPassword = text.substring(0, passLength);
      if (passLength == 0) this.czarPassword = "_________________";
    },
    submitHandle(){
      this.formType =='login'?this.login():this.signup();
    },
    login() {
      //url for post method
      const path = "http://localhost:5000/users/login";
      //form rules
      if (
        this.$refs.form.validate()
      )
        //use axios for requests
        axios
          .post(path, { username:this.username,password: this.password })
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
    },
    signup() {
      //url for post method
      const path = "http://localhost:5000/users/signup";
      //form rules
      if (
        this.$refs.form.validate()
      )
        //use axios for requests
        axios
          .post(path, {
            username: this.username,
            email: this.email,
            password: this.password
          })
          .then(res => {
            console.log(res);
            if (res.status == 409) {
              this.serverErrors.emailExists = "Email/Username already exists"
            }

            else if (res.status == 200) {
              this.login();
          }})
          .catch(error => {
            //oops
            console.log(error);
          });
    },
    toggleForm() {
      this.formType == "login"
        ? ((this.formType = "signup"), this.$router.push("Register"))
        : ((this.formType = "login"), this.$router.push("Login"));
    },
    managePath(){
      this.$router.history.current.path.toLowerCase() == "/login" ? this.formType = 'login' : this.formType = 'signup'
    }
  },
  data() {
    return {
      formType: "signup",
      rules: {
        //vuetify form rules
        counter: value => value.length <= 20 || "Max 20 characters",
        required: value => !!value || "Required.",
        emailRules: [
          value => !!value || "E-mail is required",
          value => /.+@.+\..+/.test(value) || "E-mail must be valid"
        ]
      },
      serverErrors:{
        usernameExists:'',
        emailExists:''
      },
      //default values for cards
      username: "",
      password: "",
      email: "",
      czarName: "_________________",
      czarPassword: "_________________",
      czarEmail: "_________________",
      error: ""
    };
  },
  mounted() {
    //set default text on mount
    this.syncUsername();
    this.syncPassword();
    this.managePath();
  }
};
</script>
