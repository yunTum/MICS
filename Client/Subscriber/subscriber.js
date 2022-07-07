/* ---------- mqtt subscriber ---------- */
var mqtt = require('mqtt');

// MQTT broker setting
var client = mqtt.connect({
	host: 'localhost',
	port: 1883
});

// Connected to MQTT broker
client.on('connect', function(){
		console.log('subscriber.connected.');
});

// subscribe setting
var topic_name = 'topic_no1';
client.subscribe(topic_name);

// Recieve from MQTT broker
client.on('message', function(topic, message){
	console.log('subscriber.on.message', 'topic:', topic, 'message:', message.toString());
});