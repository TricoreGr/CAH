import io from "socket.io-client";
import Player from "./player";
import axios from "axios";
class GameSocket {
  socket = io();
  username = String;
  room = String;

  constructor(username, room) {
    this.socket = io.connect("http://localhost:5000");
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

  handleJoin = (
    updateMessages,
    updatePlayers,
    gameStarted,
    setBlackCard,
  ) => {
    this.socket.on("playerJoined", data => {
      var player = new Player(data.player, data.image);
      updatePlayers(player);
      updateMessages(data.user, data.message);
      if (!gameStarted)
          setBlackCard();
  })}

  handleNextRoundReady = (updateCzar,fetchWhiteCards) => {
    this.socket.on("nextRoundReady", () => {
      const roomUrl = "http://localhost:5000/rooms/" + this.room;
      axios
        .get(roomUrl + "/round/czar", {
          token: localStorage.getItem("authToken")
        })
        .then(res => {
          let czar = res.data["czar"];
          updateCzar(czar);
          fetchWhiteCards();
        })
        .catch(error => console.log(error));
    });
  };
  leaveGame = () => {
    this.socket.emit("leave", {
      username: this.username,
      room: this.room
    });
    this.socket.disconnect();
  };

  startGame = room => {
    this.socket.emit("round_start", {
      room: room
    });
  };
}
export default GameSocket;
