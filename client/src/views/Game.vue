<template>
  <v-app>
    <div class="inGame" :class="{ 'inGame--czar': this.player.getIsCzar() }">
      <div v-for="index in 3" :key="index" class="inGame__animation">
        <player v-bind="player"></player>
      </div>
      <div class="inGame__statusWrapper">
        <v-btn rounded color="black" dark @click="leaveGame">
          QUIT
        </v-btn>
        <v-navigation-drawer
          v-model="drawer"
          absolute
          right
          temporary
          class="chat"
        >
          <div
            class="chat__message-wrapper"
            v-for="(message, index) in messages"
            :key="index"
          >
            <span class="chat__update" v-if="message.user == 'status'"
              >{{ message.user }} : {{ message.text }}</span
            >
            <div v-else>
              <span class="chat__user">{{ message.user }}: </span>
              <span class="chat__message">{{ message.text }}</span>
            </div>
          </div>

          <template v-slot:append>
            <v-text-field
              :type="'text'"
              value=""
              outlined
              solo
              class="chat__input"
              v-model="message"
              @keydown.enter="sendMessage"
            >
            </v-text-field>
            <v-btn @click.native="sendMessage" class="chat__submit">send</v-btn>
          </template>
        </v-navigation-drawer>
        <player v-bind="player"></player>
      </div>
      <div class="inGame__hint-wrapper">
        <transition name="fade">
          <span v-if="cardsToPick > 1" class="inGame__hint">
            Special Round, Choose {{ cardsToPick }} cards!
          </span>
          <span v-if="this.player.getIsCzar" class="inGame__hint">
            You're the czar! Choose the funniest card.
          </span>
        </transition>
      </div>
      <div class="inGame__mainCardWrapper">
        <card
          isCzar
          text="Exercitation sint Lorem deserunt excepteur aliquip laboris in
            ullamco veniam dolore nostrud."
        ></card>

        <div class="inGame__chatButtonWrapper">
          <v-btn
            rounded
            color="black"
            dark
            @click.native="chatNotification = false"
            @click.stop="drawer = !drawer"
            class="inGame__chatButton"
          >
            CHAT
          </v-btn>
          <div v-if="chatNotification" class="inGame__chatNotification blink">
            !
          </div>
        </div>
      </div>
      <div class="inGame__cardCarouselWrapper">
        <div class="inGame__submitButtonWrapper">
          <transition name="fade">
            <v-btn
              rounded
              color="black"
              v-if="
                this.startGamePriviladges() ||
                  (gameStarted && cardsToPick == selectedCardsIndexes.length)
              "
              dark
              :disabled="hasSubmitted"
              class="inGame__submitButton"
              @click="startGamePriviladges() ? startGame() : submitCards()"
            >
              {{ this.startGamePriviladges() ? "Start Game!" : "Submit!" }}
            </v-btn>
          </transition>
        </div>
        <cardCarousel
          v-on:updateSelectedCardsIndexes="updateSelectedCardsIndexes($event)"
          :selectedCardsIndexes="selectedCardsIndexes"
          :cardsToPick="cardsToPick"
          :cardTexts="texts"
        ></cardCarousel>
      </div>
      <div class="inGame__userCarouselWrapper">
        <userCarousel :players="players"></userCarousel>
      </div>
    </div>
  </v-app>
</template>
<script>
import cardCarousel from "@/components/CardCarousel";
import card from "@/components/Card";
import player from "@/components/Player";
import userCarousel from "@/components/UserCarousel";
import anime from "animejs/lib/anime.es.js";
import axios from "axios";
import GameSocket from "../socket";
import Player from "../player";

export default {
  components: {
    cardCarousel,
    card,
    player,
    userCarousel
  },
  methods: {
    sendMessage() {
      if (this.message) this.socket.sendMessage(this.message);
      this.message = "";
    },
    fetchUsername() {
      const path = "http://localhost:5000/users/jwtToUsername";
      axios
        .post(path, { token: localStorage.getItem("authToken") })
        .then(res => {
          this.username = res.data["username"];
          this.setupSocket();
        })
        .catch(error => {
          //oops
          console.log(error);
        });
    },
    fetchOwner() {
      const path = `http://localhost:5000/rooms/${this.room}/owner`;
      axios
        .get(path)
        .then(res => {
          this.owner = res.data["owner"];
        })
        .catch(error => {
          //oops
          console.log(error);
        });
    },
    updateMessages(user, text) {
      this.messages.push({
        user,
        text
      });
      if (!this.drawer) this.chatNotification = true;
      //wait 0.01 secs because we need to add element
      setTimeout(this.scrollToLastMessage, 10);
    },
    updatePlayers(player) {
      if (player.username != this.username) this.players.push(player);
      else {
        console.log("e (easter egg hehe)");
        this.player = player;
      }
    },
    removePlayer(player) {
      this.players = this.players.filter(
        element => element.getUsername() != player.getUsername()
      );
    },
    startGamePriviladges() {
      return this.owner == this.username && !this.gameStarted;
    },
    scrollToLastMessage() {
      //element generated by vuetify
      var test = document.getElementsByClassName(
        "v-navigation-drawer__content"
      )[0];

      //scroll to the end of the container
      test.scrollTop = test.scrollHeight;
    },
    updateSelectedCardsIndexes(indexArray) {
      this.selectedCardsIndexes = indexArray;
    },
    nextRoundAnimation(i) {
      var translate_y;
      i++;
      switch (i) {
        case 1:
          translate_y = 100;
          break;
        case 2:
          translate_y = 400;
          break;
        case 3:
          translate_y = 250;
          break;
      }
      anime({
        targets: `.inGame__animation:nth-child(${i})`,
        translateY: [500, translate_y],
        duration: 2000,
        easing: "easeInOutQuart",
        opacity: [0, 1],
        complete: () =>
          anime({
            targets: `.inGame__animation:nth-child(${i})`,
            scale: [1, 2],
            direction: "alternate",
            easing: "easeInOutSine",
            duration: 1000,
            complete: () =>
              anime({
                targets: `.inGame__animation:nth-child(${i})`,
                scale: 2,
                translateY: 0 + translate_y / 2.5,
                easing: "easeInOutQuart",
                duration: 1000,
                opacity: [1, 0]
              })
          })
      });
      if (i <= 3) {
        this.nextRoundAnimation(i);
      }
    },
    setupSocket() {
      this.socket = new GameSocket(this.username, this.room);
      this.socket.handleMessageUpdate(this.updateMessages);
      this.socket.handleLeave(this.updateMessages, this.removePlayer);
      this.socket.handleJoin(this.updateMessages, this.updatePlayers);
      this.socket.handleNextRoundReady(this.updateCzar);
    },
    leaveGame() {
      this.socket.leaveGame();
      this.$router.push("/play");
    },
    submitCards() {
      this.hasSubmitted = true;
      //todo: handle submit
    },
    startGame() {
      this.gameStarted = true;
      this.socket.startGame(this.room);
    },
    updateCzar(username) {
      if (username == this.username) this.player.setIsCzar(true);
      for (player in this.players) {
        if (player.getUsername() == username) {
          player.setIsCzar(false);
          return;
        }
      }
    }
  },
  data() {
    return {
      animationTimeline: anime.timeline(),
      username: "",
      message: "",
      chatNotification: false,
      drawer: false,
      selectedCardsIndexes: [],
      cardsToPick: 1,
      messages: [],
      hasSubmitted: false,
      room: String,
      socket: Object,
      roundWinner: Object,
      gameStarted: false,
      pickingPhase: true,
      texts: [
        "POUTSA",
        "lelelelelle",
        "lalalallalala",
        "lululululuulu",
        "lelelelelle",
        "lelelelelle",
        "lelelelelle"
      ],
      players: [],
      player: Object
    };
  },
  computed: {},
  mounted() {
    this.nextRoundAnimation(0); //for showing off purposes
    this.room = this.$router.currentRoute.params.gameId;
    this.fetchOwner();
    this.fetchUsername();
  },
  created() {
    this.player = new Player();
    window.addEventListener("beforeunload", this.leaveGame);
  },
  destroyed() {
    this.leaveGame();
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.leaveGame);
  }
};
</script>
