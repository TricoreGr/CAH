import io from 'socket.io-client';
const socketChat = {
    socketConnect(){
     return  io.connect('http://localhost:5000');
    }
    
}
export default socketChat;