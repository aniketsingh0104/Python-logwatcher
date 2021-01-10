let APP = {
    wsURL: 'ws://' + window.location.host + '/ws',
    connected: false,

    initialize: function() {
        APP.socket = new WebSocket(APP.wsURL); // create a new websocket

        // Show a connected message when the WebSocket is opened.
        APP.socket.onopen = function(event) {
            APP.connected = true;
            APP.messageUpdate('Connected to Server');
        };

        // Show a disconnected message when the WebSocket is closed.
        APP.socket.onclose = function(event) {
            APP.connected = false;
            APP.messageUpdate('Disconnected from Server');

        };

        // Handle any errors that occur.
        APP.socket.onerror = function(error) {
            APP.connected = false;
            APP.messageUpdate('Connection Error');
        };

        // Handle messages sent by the server.
        APP.socket.onmessage = function(event) {
            let payload = JSON.parse(event.data);
            let action = payload.action;
            let data = payload.data;
            console.log("Message from server:", data)
            APP.serverMessage(action, data);
        };

    },

    messageUpdate: function(message) {
        $("#message").text(message);
    },

    newMessage: function(data) {
        let message = data.message;
        if(message) {
            APP.appendLogs(message);
        }
    },


    serverMessage: function(action, data) {
        switch (action) {
            case "open": // socket connection established
                APP.messageUpdate("Connected to Server")
                break;
            case "message":
                APP.newMessage(data);
                break;
            default:
                APP.messageUpdate("Unknown Action: " + action);
        }
    },

    appendLogs: function(message) {
        let messageElement = '<span>' + message + '</span><br>'
        $("#log-message").append(messageElement);
    },
}

APP.initialize();
