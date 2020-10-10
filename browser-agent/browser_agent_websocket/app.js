const express = require("express")
const app = express();
const fs = require("fs");
const path = require("path");
const socket = require("socket.io");
const client_key_socket_map = new Map();
const pingTimeout = 1800000
const tiger_down_message = "SYSTEM IS DOWN"
const tiger_up_message = "SYSTEM IS UP"

// ####################################################################################
app.get("/", (req, res) => {
    res.status(200).send('Welcome to Express.js App');
});




// ####################################################################################
const server = app.listen(5000, err => {
    if (err) {
        console.error("Server cannot listen");
        return false;
    }
    console.log("Server up ....")
});

const getKey = (key, domainName) => {
    return key + '-' + domainName;
}

// ####################################################################################
const io = socket(server, {
    'pingTimeout' : pingTimeout
});


io.on('connection', (socket) => {
    console.log("Made socket connection...", socket.id);
    socket.on("key", (data) => {
        client_key_socket_map.set(getKey(data.key, data.domainName), socket.id);
    });
});



// ####################################################################################
app.post('/push', function(req, res) {
    const body = req.query || {};

    if(body['TIGER_IS_DOWN']) {
        io.emit('response', tiger_down_message);    
    } else if(body['TIGER_IS_UP']) {
        io.emit('response', tiger_up_message);    
    } else if(body['CLEAN_UP']) {
        io.to(client_key_socket_map.get(getKey(body['Key'], body['DomainName'])))
        .emit('disconnect');   
    } else {
        io.to(client_key_socket_map.get(getKey(body['Key'], body['DomainName'])))
        .emit('response', body['Response']);    
    }
    
    res.send(true)
});




