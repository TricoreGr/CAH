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
    const url = "http://localhost:5000/rooms/" + this.room + "/players";
    axios
      .post(url, {
        token: localStorage.getItem("authToken")
      })
      .then(res => console.log(res))
      .catch(error => console.log(error));
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
  handleLeave = updateMessages => {
    this.socket.on("playerLeft", data => {
      updateMessages(data.user, data.message);
    });
  };

  handleJoin = (updateMessages, updatePlayers) => {
    this.socket.on("playerJoined", data => {
      var player = new Player(data.player, data.image);
      updatePlayers(player);
      updateMessages(data.user, data.message);
    });
  };

  handleJoin = (updateMessages, updatePlayers) => {
    this.socket.on("playerJoined", data => {
      var player = new Player(data.player, data.image);
      updatePlayers(player);
      updateMessages(data.user, data.message);
    });
  };

  getNextRoundInfo = () => {
    this.socket.on("nextRoundReady", data => {
      const roomUrl = "http://localhost:5000/rooms/" + this.room;
      var czar;
      axios
        .get(roomUrl + "/round/czar", {
          token: localStorage.getItem("authToken")
        })
        .then(res => console.log(res))
        .catch(error => console.log(error));
      console.log(data);
      console.log(czar);
    });
  };
  leaveGame = () => {
    this.socket.emit("leave", {
      username: this.username,
      room: this.room
    });
    this.socket.disconnect();
    this.$router.push("/play");
  };
}

export default GameSocket;
