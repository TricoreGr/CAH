import io from "socket.io-client";

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
  handleLeave = updateMessages => {
    this.socket.on("playerLeft", data => {
      updateMessages(data.user, data.message);
    });
  };

  handleJoin = updateMessages => {
    this.socket.on("playerJoined", data => {
      updateMessages(data.user, data.message);
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
