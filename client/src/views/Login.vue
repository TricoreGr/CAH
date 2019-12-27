<script>
import axios from 'axios';
export default {
  methods: {
    syncUsername() {
      if (this.username.length < 20) this.czarName = this.username;
      if (this.username.length == 0) this.czarName = "_________________";
    },
    syncPassword() {
      const text = "veryStr0nkP4ssw0rd";
      var passLength = this.password.length;
      this.czarPassword = text.substring(0, passLength);
      if (passLength == 0) this.czarPassword = "_________________";
    },
    login(){    
    const path = 'http://localhost:5000/users/'+this.username+'/auth';
    if(this.username && this.username.length <= 20 && this.password.length>0)
      axios.post(path,{password:this.password})
        .then(res => {
          if(res.data.token){
            localStorage.setItem('authToken',res.data.token);
            this.$router.push('/');
          }
          else
            this.error = res.data.message;
        })
        .catch(error =>{
          console.log(error);
        });
      }
  },
  data() {
    return {
      title: "Login",
      rules: {
        counter: value => value.length <= 20 || "Max 20 characters",
        required: value => !!value || "Required."
      },
      username : 'IQ^person',
      password : 'lalala',
      czarName : "_________________",
      czarPassword : "_________________",
      error : ""
    };
  },
  mounted() {
    this.syncUsername();
    this.syncPassword();
  }
};
</script>
<template>
  <v-app>
    <div class="login">
      <div class="login__headline-wrapper">
        <h1 class="login__title">
          FARTS AGAINST HUMANITY
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
                {{czarName}}
              </span>
            </div>
            <div class="card__input-wrapper">
              <span class="card__text">
                and my password
              </span>
              <span id="czar-password" class="card__input">
                {{czarPassword}}
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
              <v-text-field
                @input="syncPassword"
                :rules="[rules.required]"
                :type="'password'"
                value="lololo"
                v-model="password"
              ></v-text-field>
            </div>
          </div>
          <div class = "card__signature-wrapper">
          <span class="card__error">{{error}}</span>
          <span class="card__signature">CAH</span>
          </div>
        </div>
      </div>
      <div class="login__buttons-wrapper">
        <v-btn rounded color="black" active-class="test" @click.native="login" dark
          >LOG IN, FRIEND!</v-btn
        >
        <v-btn text small>Forgot Password?</v-btn>
      </div>
    </div>
  </v-app>
</template>
