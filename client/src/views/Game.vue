<template>
  <div class="inGame">
    <div class="inGame__statusWrapper">
      <v-btn
        rounded
        color="black"
        @click.native="login"
        dark
      >
        QUIT
      </v-btn>
      <v-navigation-drawer
      v-model="drawer"
      absolute
      right
      temporary
      class="chat"
    >
    <div class="chat__message-wrapper" v-for="(message,index) in messages" :key="index">
      <span class="chat__user" >{{message.user}}: </span>
      <span class="chat__message" >{{message.text}}</span>
    </div>
    <template v-slot:append>
        <v-text-field
                  :type="'text'"
                  value=""
                  outlined
                  solo
                  class="chat__input"
                  >
                </v-text-field>
                <v-btn class="chat__submit">send</v-btn>
      </template>

      </v-navigation-drawer>
      <div class="inGame__roundWrapper">
        <span class="inGame__round">
          ROUND
        </span>
        <span class="inGame__round">
          {{currentRound}} / {{totalRounds}}
        </span>
      </div>
      <player></player>
    </div>
    <div class="inGame__mainCardWrapper">
      <card
        isCzar
        text="Exercitation sint Lorem deserunt excepteur aliquip laboris in
            ullamco veniam dolore nostrud."
      ></card>
      <div class="inGame__chatButtonWrapper">
        <v-btn rounded color="black" dark @click.stop="drawer = !drawer">
          CHAT
        </v-btn>
        <div class="inGame__chatNotification">
          !
        </div>
      </div>
    </div>
    <div class="inGame__cardCarouselWrapper">
      <cardCarousel></cardCarousel>
    </div>
    <div class="inGame__userCarouselWrapper">
      <userCarousel></userCarousel>
    </div>
  </div>
</template>
<script>
import cardCarousel from "./components/cardCarousel";
import card from "./components/card";
import player from "./components/player";
import userCarousel from './components/userCarousel'
export default {
  components: {
    cardCarousel,
    card,
    player,
    userCarousel
  },
  data() {
    return {
      currentRound:1,
      totalRounds:6,
      drawer: true,
      messages:[
        {
          'user':'stougk',
          'text':'foveri ergasia , 10/10'
        },
        {
          'user':'dtektoni',
          'text':'amazing, WOW , 10/10'
        },
        {
          'user':'asidirop',
          'text':'oti kalutero exoume dei, evge , 10/10'
        },{
          'user':'stougk',
          'text':'foveri ergasia , 10/10'
        },
        {
          'user':'dtektoni',
          'text':'amazing, WOW , 10/10'
        },
        {
          'user':'asidirop',
          'text':'oti kalutero exoume dei, evge , 10/10'
        },{
          'user':'stougk',
          'text':'foveri ergasia , 10/10'
        },
        {
          'user':'dtektoni',
          'text':'amazing, WOW , 10/10'
        },
        {
          'user':'asidirop',
          'text':'oti kalutero exoume dei, evge , 10/10'
        },{
          'user':'stougk',
          'text':'foveri ergasia , 10/10'
        },
        {
          'user':'dtektoni',
          'text':'amazing, WOW , 10/10'
        },
        {
          'user':'asidirop',
          'text':'oti kalutero exoume dei, evge , 10/10'
        },{
          'user':'stougk',
          'text':'foveri ergasia , 10/10'
        },
        {
          'user':'dtektoni',
          'text':'amazing, WOW , 10/10'
        },
        {
          'user':'asidirop',
          'text':'oti kalutero exoume dei, evge , 10/10'
        }
      ]
    }
  }
};
</script>
