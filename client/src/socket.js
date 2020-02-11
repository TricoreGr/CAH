import io from "socket.io-client";
import Player from "./player";
import axios from "axios";
import baseURL from "./global";
class GameSocket {
  socket = io();
  username = String;
  room = String;
  connectOptions={
    secure:true,
    reconnect:true,
    rejectUnauthorized:false
  };
  url = baseURL


  constructor(username, room) {
    this.socket = io.connect(this.url,this.connectOptions);
    this.username = username;
    this.room = room;
    this.handleConnect();
  }

  handleConnect = () => {
    this.socket.on("connect", this.joinRoom);
  };

  joinRoom = () => {
    this.socket.emit("joined", { username: this.username, room: this.room });
  };

  sendMessage = message => {
    this.socket.emit("sendMessage", {
      username: this.username,
      message: message,
      room: this.room
    });
  };

  handleMessageUpdate = updateMessages => {
    this.socket.on("newMessage", data => {
      updateMessages(data.user, data.message);
    });
  };
  handleLeave = (updateMessages, removePlayer) => {
    this.socket.on("playerLeft", data => {
      var player = new Player(data.player, "default.jpg");
      removePlayer(player);
      updateMessages(data.user, data.message);
    });
  };

  handleJoin = (updateMessages, updatePlayers, gameStarted, setBlackCard) => {
    this.socket.on("playerJoined", data => {
      var player = new Player(data.player, data.image);
      updatePlayers(player);
      updateMessages(data.user, data.message);
      if (!gameStarted) setBlackCard();
    });
  };

  handleNextRoundReady = (
    updateCzar,
    fetchWhiteCards,
    fetchBlackCard,
    updateGameState
  ) => {
    this.socket.on("nextRoundReady", () => {
      const roomUrl = baseURL +"/rooms/"+ this.room;
      axios
        .get(roomUrl + "/round/czar", {
          token: localStorage.getItem("authToken")
        })
        .then(res => {
          let czar = res.data["czar"];
          updateGameState();
          updateCzar(czar);
          fetchWhiteCards();
          fetchBlackCard();
        })
        .catch();
    });
  };

  //todo: receive username
  handlePlayerSubmission = updatePlayerSubmissionState => {
    this.socket.on("playerSubmission", data => {
      updatePlayerSubmissionState(data.username);
    });
  };

  handleCzarPickingPhase = fetchSubmittedCards => {
    this.socket.on("czarPickingPhase", () => {
      fetchSubmittedCards();
    });
  };

  handleGameEnding=finishGame=>{
    this.socket.on("game_winner", (data) => {
      finishGame(data.winner);
    });
  }

  handleWinner = updateWinner => {
    this.socket.on("round_winner", data => {
      updateWinner(data.winner);
    });
  };

  roundOver = winner => {
    this.socket.emit("round_over", {
      username: winner,
      room: this.room
    });
  };

  leaveGame = () => {
    this.socket.emit("leave", {
      username: this.username,
      room: this.room
    });
    this.socket.disconnect();
  };

  startRound = room => {
    this.socket.emit("round_start", {
      room: room
    });
  };
}
export default GameSocket;
