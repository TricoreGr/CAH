<script>
export default {
  methods: {
    syncUsername() {
      var name = document.getElementsByName("username")[0];
      var czarName = document.getElementById("czar-uername");
      if (name.value.length < 20) czarName.innerHTML = name.value;
      if (name.value.length == 0) czarName.innerHTML = "_________________";
    },
    syncPassword() {
      const text = "veryStr0nkP4ssw0rd";
      var password = document.getElementsByName("password")[0];
      var passLength = password.value.length;
      var czarPassword = document.getElementById("czar-password");
      czarPassword.innerHTML = text.substring(0, passLength);

      if (passLength == 0) czarPassword.innerHTML = "_________________";
    }
  },
  data() {
    return {
      title: "Login",
      rules: {
        counter: value => value.length <= 20 || "Max 20 characters",
        required: value => !!value || "Required."
      }
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
              <span id="czar-uername" class="card__input">
                _________________
              </span>
            </div>
            <div class="card__input-wrapper">
              <span class="card__text">
                and my password
              </span>
              <span id="czar-password" class="card__input">
                _________________
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
                  name="username"
                  value="IQ^person"
                  counter
                ></v-text-field>
              </span>
            </div>  
            <div class="card__input-wrapper">
              <v-text-field
                @input="syncPassword"
                :rules="[rules.required]"
                :type="'password'"
                name="password"
                value="lololo"
              ></v-text-field>
            </div>
          </div>
          <span class="card__signature">CAH</span>
        </div>
      </div>
      <div class="login__buttons-wrapper">
        <v-btn rounded color="black" active-class="test" dark
          >LOG IN, CUNT!</v-btn
        >
        <v-btn text small>Forgot Password?</v-btn>
      </div>
    </div>
  </v-app>
</template>
