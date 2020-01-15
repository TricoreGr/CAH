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
          <span
            v-if="this.player.getIsCzar()"
            class="inGame__hint scale-up-center"
          >
            You're the czar! Choose the funniest card.
          </span>
        </transition>
      </div>
      <div class="inGame__mainCardWrapper">
        <card isCzar :text="blackCard"></card>

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
                this.startGamePrivileges() ||
                  (gameStarted &&
                    cardsToPick == selectedCardsIndexes.length &&
                    !this.player.getHasPlayed())
              "
              dark
              class="inGame__submitButton"
              @click="startGamePrivileges() ? startGame() : submitCards()"
            >
              {{ this.startGamePrivileges() ? "Start Game!" : "Submit!" }}
            </v-btn>
          </transition>
        </div>
        <cardCarousel
          v-on:updateSelectedCardsIndexes="updateSelectedCardsIndexes($event)"
          :selectedCardsIndexes="selectedCardsIndexes"
          :cardsToPick="cardsToPick"
          :cardTexts="this.player.getIsCzar() ? submittedCards : whiteCards"
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
          this.player.setUsername(res.data["username"]);
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
      if (player.username != this.player.getUsername())
        this.players.push(player);
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
    startGamePrivileges() {
      return this.owner == this.player.getUsername() && !this.gameStarted;
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
      this.socket = new GameSocket(this.player.getUsername(), this.room);
      this.socket.handleMessageUpdate(this.updateMessages);
      this.socket.handleLeave(this.updateMessages, this.removePlayer);
      this.socket.handleJoin(
        this.updateMessages,
        this.updatePlayers,
        this.gameStarted,
        this.setDefaultBlackCard,
        this.players.length
      );
      this.socket.handleNextRoundReady(
        this.updateCzar,
        this.fetchWhiteCards,
        this.fetchBlackCard
      );
      this.socket.handlePlayerSubmission(this.updatePlayerSubmissionState)
    },
    leaveGame() {
      this.socket.leaveGame();
      this.$router.push("/play");
    },
    submitCards() {
      this.player.setHasPlayed(true);
      //todo: fix it
      const url = "http://localhost:5000/rooms/";
      var selectedCards = [];
      for (var index of this.selectedCardsIndexes);
       selectedCards.push(this.whiteCards[index]);

      console.log(selectedCards);
      axios
        .post(url, { selectedCards: selectedCards })
        .then(res => {
          console.log(res);
        })
        .catch(error => console.log(error));
    },
    startGame() {
      this.gameStarted = true;
      this.socket.startGame(this.room);
    },
    updateCzar(username) {
      if (username == this.player.getUsername()) this.player.setIsCzar(true);
      for (var player of this.players) {
        if (player.getUsername() == username) {
          player.setIsCzar(true);
          return;
        }
      }
    },
    updatePlayerSubmissionState(username) {
      if (username == this.player.getUsername()) this.player.setHasPlayed(true);
      for (var player of this.players) {
        if (player.getUsername() == username) {
          player.setHasPlayed(true);
          return;
        }
      }
    },
    setDefaultBlackCard() {
      this.players.length >= 1
        ? (this.blackCard = `waiting for player ${this.owner} to start the game...`)
        : (this.blackCard = "waiting for players...");
    },
    fetchWhiteCards() {
      const url =
        "http://localhost:5000/rooms/" +
        this.room +
        "/players/" +
        this.player.getUsername() +
        "/whitecards";
      axios
        .get(url)
        .then(res => {
          this.whiteCards = res.data["whitecards"];
        })
        .catch(error => console.log(error));
    },
    fetchBlackCard() {
      const url =
        "http://localhost:5000/rooms/" + this.room + "/round/blackcard";
      axios
        .get(url)
        .then(res => {
          console.log(res.data);
          this.blackCard = res.data["blackCard"]["text"];
          this.cardsToPick = res.data["blackCard"]["pick"];
        })
        .catch(error => console.log(error));
    }
  },
  data() {
    return {
      animationTimeline: anime.timeline(),
      message: "",
      chatNotification: false,
      drawer: false,
      selectedCardsIndexes: [],
      cardsToPick: -1,
      messages: [],
      room: String,
      socket: Object,
      roundWinner: Object,
      gameStarted: false,
      pickingPhase: true,
      blackCard: "Waiting for players...",
      whiteCards: [],
      submittedCards: [],
      players: [],
      player: Object
    };
  },
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
