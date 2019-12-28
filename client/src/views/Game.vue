<template>
  <div class="inGame">
    <div class="inGame__statusWrapper">
      <v-btn
        rounded
        color="black"
        active-class="test"
        @click.native="login"
        dark
      >
        QUIT
      </v-btn>
      <div class="inGame__roundWrapper">
        <span class="inGame__round">
          ROUND
        </span>
        <span class="inGame__round">
          1 / 6
        </span>
      </div>
      <div class="inGameUser__wrapper">
        <img
          class="inGameUser__image inGameUser__image--czar"
          src="https://upload.wikimedia.org/wikipedia/commons/4/4d/Star_Wars-_The_Last_Jedi_Japan_Premiere_Red_Carpet-_Adam_Driver_%2827163437599%29_%28cropped%29.jpg"
        />
        <div class="inGameUser__AttributeWrapper">
          <span class="inGameUser__isCzar"> </span>
          <span class="inGameUser__points">69</span>
        </div>
      </div>
    </div>
    <div class="inGame__mainCardWrapper">
      <div class="card card--czar">
        <div class="card__content-wrapper">
          <span class="card__text">
            Exercitation sint Lorem deserunt excepteur aliquip laboris in
            ullamco veniam dolore nostrud.
          </span>
        </div>
        <span class="card__signature">CAH</span>
      </div>
      <div class="inGame__chatButtonWrapper">
        <v-btn
          rounded
          color="black"
          active-class="test"
          @click.native="login"
          dark
        >
          CHAT
        </v-btn>
        <div class="inGame__chatNotification">
            !
        </div>
      </div>
    </div>
  </div>
</template>
