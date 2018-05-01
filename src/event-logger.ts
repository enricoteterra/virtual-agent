import * as io from "socket.io-client";
 
const socket = io('http://localhost:5000');

var events = [
    "click", "mousedown", "mouseup", "keydown", "change", "mouseup", 
    "click", "dblclick", "mousemove", "mouseover", "mouseout", "mousewheel", "keydown", 
    "keyup", "keypress", "textInput", "touchstart", "touchmove", "touchend", "touchcancel", 
    "resize", "scroll", "zoom", "select", "change", "submit", "reset"
];

events.forEach(function(eventName) {
    document.getElementById("canvas")!.addEventListener(eventName, function(e){
        
        let message:any = {
            "type": e.type, 
            "timeStamp": e.timeStamp,
            "unixTimeStamp": + new Date()
        }

        if (e instanceof MouseEvent) {
            message['x'] = e.x;
            message['y'] = e.y;
            message['movementX'] = e.movementX;
            message['movementY'] = e.movementY;
        }

        else if (e instanceof KeyboardEvent) {
            message['code'] = e.code;
            message['key'] = e.key;
            message['keyCode'] = e.keyCode;
        }

        socket.emit('message', message);
    })
});