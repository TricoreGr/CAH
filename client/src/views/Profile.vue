<template>
  <div>
    <navbar />
    <div class="account">
      <div class="account__wrapper slide-in-blurred-top">
        <h1 class="account__username">{{ username }}</h1>
        <img
          class="account__user-image"
          src="https://upload.wikimedia.org/wikipedia/commons/4/4d/Star_Wars-_The_Last_Jedi_Japan_Premiere_Red_Carpet-_Adam_Driver_%2827163437599%29_%28cropped%29.jpg"
        />
        <div class="account__score-wrapper">
          <div class="account__info-wrapper">
            <span class="account__info-label">Wins</span>
            <span class="account__info">3</span>
          </div>
          <div class="account__info-wrapper">
            <span class="account__info-label">Games</span>
            <span class="account__info">10</span>
          </div>
        </div>
        <div class="account__info-wrapper">
          <h3 class="account__info-label account__info-label--rank">
            Rank
          </h3>
          <span class="account__info account__info--rank">PASOL</span>
        </div>
        <div class="account__email-wrapper">
          <span class="account__email-label">email</span>
          <span class="account__email">sotostosto</span>
        </div>
      </div>
              <v-btn
            rounded
            dark
            class="account__button account__button--deleteAccount"
          >
            Delete Account?
          </v-btn>

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "StoeBlyat"
    };
  }
};
</script>
