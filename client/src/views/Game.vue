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

                this.pickCardPrivileges() ||
                  this.startGamePrivileges() ||
                  (!pickingPhase && gameStarted &&

                    cardsToPick == selectedCardsIndexes.length &&
                    !this.player.getHasPlayed())
              "
              dark
              class="inGame__submitButton"
              @click="
                startGamePrivileges()
                  ? startGame()
                  : pickingPhase
                  ? submitPickedCard()
                  : submitCards()
              "

            >
              {{ this.startGamePrivileges() ? "Start Game!" : "Submit!" }}
            </v-btn>
          </transition>
        </div>
        <cardCarousel
          v-on:updateSelectedCardsIndexes="updateSelectedCardsIndexes($event)"
          :selectedCardsIndexes="selectedCardsIndexes"
          :cardsToPick="cardsToPick"
          :cardTexts="
            pickingPhase
              ? submittedCards
              : !player.getIsCzar()
              ? whiteCards
              : null
          "
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
    pickCardPrivileges() {
      return (
        this.player.getIsCzar() &&
        this.pickingPhase &&
        this.selectedCardsIndexes.length == 1
      );
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
      return this.players.length>1&&this.owner == this.player.getUsername() && !this.gameStarted;
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
      console.log(this.roundWinner);
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

        this.fetchBlackCard,
        this.updateGameState
      );
      this.socket.handlePlayerSubmission(this.updatePlayerSubmissionState);
      this.socket.handleCzarPickingPhase(this.fetchSubmittedCards);
      this.socket.handleWinner(this.updateWinner);
    },
    updateWinner(winner){

      if(winner == this.player.getUsername())
           this.roundWinner = this.player;
      else
      for (var user of this.players){
        if(user.getUsername() == winner){
          this.roundWinner = user;
          return;
        }
      }
      this.nextRoundAnimation(0);

    },
    leaveGame() {
      this.socket.leaveGame();
      this.$router.push("/play");
    },
    updateGameState() {
      for (var user of this.players){
        user.setIsCzar(false);
        user.setHasPlayed(false);
      }
      this.player.setIsCzar(false);
      this.player.setHasPlayed(false);
      this.pickingPhase = false;
      this.gameStarted = true;
    },
    //todo; triggers event
    submitCards() {
      this.player.setHasPlayed(true);
      //todo: fix it

      const url =
        "http://localhost:5000/rooms/" + this.room + "/round/whitecards";
      var selectedCards = [];
      console.log("selectedCardIntexes", this.selectedCardsIndexes);

      for (var i = 0; i < this.selectedCardsIndexes.length; i++) {
        selectedCards.push(this.whiteCards[this.selectedCardsIndexes[i]]);
      }

      axios
        .post(url, {
          token: localStorage.getItem("authToken"),
          cards: selectedCards
        })

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


    //todo: after a user submits

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

        console.log(this.whiteCards);
    },
    fetchBlackCard() {
      const url =
        "http://localhost:5000/rooms/" + this.room + "/round/blackcard";
      axios
        .get(url)
        .then(res => {
          console.log(res.data);
          this.blackCard = res.data["blackCard"]["text"];

          console.log(res.data["blackCard"]["pick"]);
          this.cardsToPick = res.data["blackCard"]["pick"];
        })
        .catch(error => console.log(error));
    },
    fetchSubmittedCards() {
      this.pickingPhase = true;
      this.cardsToPick = 1;
      const url =
        "http://localhost:5000/rooms/" + this.room + "/round/whitecards";
      axios
        .get(url)
        .then(res => {
          this.submittedData = res.data;
          console.log("res", res.data["whiteCards"][0]);
          for (var i = 0; i < res.data["whiteCards"].length; i++) {
            console.log(i);
            console.log("card", res.data["whiteCards"][i].cards);
            this.submittedCards.push(res.data["whiteCards"][i].cards);
          }
        })
        .catch(error => console.log(error));
    },
    //todo: next round comes
    resetPlayers() {
      for (var player of this.players) {
        player.setHasPlayed(false);
        player.setIsCzar(false);
      }
      this.player.setIsCzar(false);
      this.player.setHasPlayed(false);
    },
    //todo: after czar chooses favorite card
    handleWinner(username) {
      if (username == this.player.getUsername()) {
        this.player.increasePoints();
        this.roundWinner = this.player;
      }

      for (var player of this.players) {
        if (player.getUsername() == username) {
          player.increasePoints();
          this.roundWinner = player;
          return;
        }
      }
    },
    fetchPlayers() {
      const roomUrl = "http://localhost:5000/rooms/" + this.room;
      axios
        .get(roomUrl + "/players", {
          token: localStorage.getItem("authToken")
        })
        .then(res => {
          var data = res.data;
          console.log(data);
          for (var user of data.players) {
            var player = new Player(user.username, user.img);
            player.setPoints(user.points);
            this.updatePlayers(player);
          }
        })
        .catch(error => console.log(error));
    },
    submitPickedCard() {
      var selectedIndex = this.selectedCardsIndexes[0];
      var username = this.submittedData["whiteCards"][selectedIndex]["username"];
      this.socket.roundOver(username);

      const roomUrl = "http://localhost:5000/rooms/" + this.room+"/players/"+username+"/points";
      axios.post(roomUrl,{}).then( () =>{
        this.player.setIsCzar(false);
        this.socket.startGame(this.room);
      });
      

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
      pickingPhase: false,
      blackCard: "Waiting for players...",
      whiteCards: [],
      submittedCards: [],
      players: [],
      player: Object,
      submittedData: []
    };
  },
  mounted() {
    this.room = this.$router.currentRoute.params.gameId;
    this.fetchOwner();
    this.fetchUsername();
    this.fetchPlayers();
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
