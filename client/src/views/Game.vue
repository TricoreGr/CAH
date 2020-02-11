<template>
  <v-app>
    <div class="inGame" :class="{ 'inGame--czar': this.player.getIsCzar() }">
      <div v-for="index in 3" :key="index" class="inGame__animation">
        <player v-bind="roundWinner"></player>
      </div>
      <div class="inGame__statusWrapper">
        <v-btn rounded color="black" dark @click="leaveGame">
          QUIT
        </v-btn>
        <v-navigation-drawer
          v-model="drawer"
          fixed
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
            {{
              this.pickingPhase
                ? "Choose your favorite card!"
                : "You're the czar! Wait for players to submit their cards"
            }}
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
              v-if="shouldRenderButtonPriviledeges"
              dark
              class="inGame__submitButton"
              @click="shouldClickConditions"
              :disabled="!this.gameStarted && (this.players.length<2)"
            >
              {{ this.startGamePrivileges() ? "Start Game!" : "Submit!" }}
            </v-btn>
          </transition>
        </div>
        <cardCarousel
          v-on:updateSelectedCardsIndexes="updateSelectedCardsIndexes($event)"
          :selectedCardsIndexes="selectedCardsIndexes"
          :cardsToPick="cardsToPick"
          :cardTexts="carouselCards"
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
import VueJwtDecode from "vue-jwt-decode";
import baseURL from "../global"

export default {
  data() {
    return {
      /* Game state related*/
      socket: Object,
      gameStarted: false,
      pickingPhase: false,
      animationTimelissne: anime.timeline(),
      shouldRenderButton: false,

      /* Chat related */
      message: "",
      chatNotification: false,
      drawer: false,
      messages: [],

      /*Card related & picking */
      cardsToPick: -1,
      blackCard: "Waiting for players...",
      submittedCards: [],
      whiteCards: [],
      selectedCardsIndexes: [],

      /* Players related */
      players: [],
      player: Object,
      room: String,

      /*Round related*/
      submittedData: [],
      roundWinner: new Player()
    };
  },
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
      this.player.setUsername(
        VueJwtDecode.decode(localStorage.getItem("authToken")).user
      );
      this.setupSocket();
    },

    fetchOwner() {
      const path = baseURL+`/rooms/${this.room}/owner`;
      axios
        .get(path)
        .then(res => {
          this.owner = res.data["owner"];
        })
        .catch();
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
        // console.log("e (easter egg hehe)");
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
    roundWinnerAnimation(i) {
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
        this.roundWinnerAnimation(i);
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
        this.fetchBlackCard,
        this.updateGameState
      );
      this.socket.handlePlayerSubmission(this.updatePlayerSubmissionState);
      this.socket.handleCzarPickingPhase(this.fetchSubmittedCards);
      this.socket.handleWinner(this.updateWinner);
      this.socket.handleGameEnding(this.finishGame);
    },
    leaveGame() {
      this.socket.leaveGame();
      this.$router.push("/play");
    },
    finishGame(winner) {
      var winnerIndex = this.filterPlayerIndex(winner);
      if (winnerIndex == -1) {
        this.player.increasePoints();
        this.roundWinner = this.player;
      } else {
        this.players[winnerIndex].increasePoints();
        this.roundWinner = this.players[winnerIndex];
      }

      this.addGames();

      if(this.player.getUsername() == winner)
      this.addWins();

      alert("WINNER IS " + winner);
      alert("Now you're getting kicked. ");
      alert("Goobye.");
      this.leaveGame();
      this.animate("gameWinner");
    },

    animate(animation){
      switch (animation){
        case "gameWinner":this.gameWinnerAnimation();break;
        case "roundWinner":this.roundWinnerAnimation(0);break;
      }
    },
    updateGameState() {
      for (var user of this.players) {
        user.setIsCzar(false);
        user.setHasPlayed(false);
      }
      this.player.setIsCzar(false);
      this.player.setHasPlayed(false);
      this.pickingPhase = false;
      this.gameStarted = true;
    },
    testAnimation() {
      anime({
        targets: ".card--selected",
        translateY: [500, 1000],
        duration: 500,
        easing: "easeInOutQuart"
      });
    },
    submitCards() {

      this.testAnimation();
      this.player.setHasPlayed(true);
      const url =
        baseURL+"/rooms/" + this.room + "/round/whitecards";
      var selectedCards = [];

      for (var i = 0; i < this.selectedCardsIndexes.length; i++) {
        selectedCards.push(this.whiteCards[this.selectedCardsIndexes[i]]);
      }

      for (var card of selectedCards) {
        this.whiteCards = this.whiteCards.filter(element => element != card);
      }

      axios
        .post(url, {
          token: localStorage.getItem("authToken"),
          cards: selectedCards
        })

        .then(() => {
        })
        .catch();
    },
    startRound() {
      this.gameStarted = true;
      this.socket.startRound(this.room);
    },
    updateCzar(username) {
      var czarIndex = this.filterPlayerIndex(username);

      if (czarIndex == -1) this.player.setIsCzar(true);
      else this.players[czarIndex].setIsCzar(true);
    },
    updateWinner(username) {
      var winnerIndex = this.filterPlayerIndex(username);
      if (winnerIndex == -1) {
        this.player.increasePoints();
        this.roundWinner = this.player;
      } else {
        this.players[winnerIndex].increasePoints();
        this.roundWinner = this.players[winnerIndex];
      }
      this.animate("roundWinner");
    },
    updatePlayerSubmissionState(username) {
      var submittedIndex = this.filterPlayerIndex(username);
      if (submittedIndex == -1) this.player.setHasPlayed(true);
      else this.players[submittedIndex].setHasPlayed(true);
    },
    setDefaultBlackCard() {
      this.players.length >= 2
        ? (this.blackCard = `waiting for player ${this.owner} to start the game...`)
        : (this.blackCard = "waiting for "+(2-this.players.length) +`  more player${this.players.length==1?'':'s'}...`);
    },
    fetchWhiteCards() {
      const url =
        baseURL+"/rooms/" +
        this.room +
        "/players/" +
        this.player.getUsername() +
        "/whitecards";
      axios
        .get(url)
        .then(res => {
          this.whiteCards = res.data['whitecards']
        })
        .catch();
    },
    fetchBlackCard() {
      const url =
        baseURL+"/rooms/" + this.room + "/round/blackcard";
      axios
        .get(url)
        .then(res => {
          this.blackCard = res.data["blackCard"]["text"];
          this.cardsToPick = res.data["blackCard"]["pick"];
        })
        .catch();
    },
    fetchSubmittedCards() {
      this.submittedCards = [];
      this.selectedCardsIndexes=[];
      this.submittedData = null;
      this.pickingPhase = true;
      this.cardsToPick = this.player.getIsCzar()?1:0;
      const url =
        baseURL+"/rooms/" + this.room + "/round/whitecards";
      axios
        .get(url)
        .then(res => {
          this.submittedData = res.data;
          for (var i = 0; i < res.data["whiteCards"].length; i++) {
            this.submittedCards.push(res.data["whiteCards"][i].cards);
          }
        })
        .catch();
    },
    addWins(){
      axios
        .post(baseURL+"/users/"+this.player.getUsername()+"/wins")
        .then(() => {})
        .catch();
    },
    addGames(){
      axios
        .post(baseURL+"/users/"+this.player.getUsername()+"/games")
        .then(() => {})
        .catch();
    },
    //todo: next round comes
    resetPlayers() {
      for (var player of this.players) {
        player.setHasPlayed(false);
        player.setIsCzar(false);
      }
      this.$data.submittedCards = [];
      this.$data.submittedData = [];
      this.player.setIsCzar(false);
      this.player.setHasPlayed(false);
    },
    fetchPlayers() {
      const roomUrl = baseURL+"/rooms/" + this.room;
      axios
        .get(roomUrl + "/players", {
          token: localStorage.getItem("authToken")
        })
        .then(res => {
          var data = res.data;
          for (var user of data.players) {
            var player = new Player(user.username, user.img);
            player.setPoints(user.points);
            this.updatePlayers(player);
          }
        })
        .catch();
    },
    filterPlayerIndex(username) {
      if (username == this.player.getUsername()) return -1;
      else
        for (var i = 0; i < this.players.length; i++)
          if (this.players[i].getUsername() == username) return i;
    },
    submitPickedCard() {
      var selectedIndex = this.selectedCardsIndexes[0];
      var username = this.submittedData["whiteCards"][selectedIndex][
        "username"
      ];
      this.socket.roundOver(username);

      const roomUrl =
        baseURL+"/rooms/" +
        this.room +
        "/players/" +
        username +
        "/points";
      axios.post(roomUrl, {}).then(() => {
        this.player.setIsCzar(false);
        this.socket.startRound(this.room);
      });
    },
    fetchData(){
      this.fetchOwner();
    this.fetchUsername();
    this.fetchPlayers();
    },
    fetchGameState(){
      const roomUrl =
        baseURL+"/rooms/"+this.room;
      axios.get(roomUrl, {})
      .then((res) => {
        if(res.data.room.gameStarted){
          this.gameStarted = true;
          alert("game has started. Please choose another room.");
          this.$router.push("/play");
        }
        else
          this.fetchData();
      })
  },
  },
  mounted() {
    this.room = this.$router.currentRoute.params.gameId;
    this.fetchGameState();
    this.shouldRenderButton = true;
  },
  created() {
    if(!localStorage.getItem("authToken")) this.$router.push("/login")
    this.player = new Player();
    window.addEventListener("beforeunload", this.leaveGame);
  },
  destroyed() {
    this.leaveGame();
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.leaveGame);
  },
  computed: {
    carouselCards() {
      if (this.$data.pickingPhase) {
        return this.$data.submittedCards;
      } else {
        if (!this.player.getIsCzar()) return this.$data.whiteCards;
        return null;
      }
    },
    pickCardPrivileges() {
      return (
        this.player.getIsCzar() &&
        this.pickingPhase &&
        this.selectedCardsIndexes.length == 1
      );
    },
    shouldRenderButtonPriviledeges() {
      return (
        this.shouldRenderButton &&
        (this.pickCardPrivileges ||
          this.startGamePrivileges() ||
          (!this.pickingPhase &&
            this.gameStarted &&
            this.cardsToPick == this.selectedCardsIndexes.length &&
            !this.player.getHasPlayed()))
      );
    },
    shouldClickConditions() {
      return this.startGamePrivileges()
        ? this.startRound
        : this.pickingPhase
        ? this.submitPickedCard
        : this.submitCards;
    }
  }
};
</script>
