// this is a web worker to poll for new dispatches
var intervalID;

function checkforupdate(tfdd_update_url) {
    var request = new XMLHttpRequest();
    request.open('GET', tfdd_update_url, false);
    request.send();
    if (request.status === 200) {
        clearInterval(intervalID);
        self.postMessage(request.responseText);
    }
};
    
self.onmessage = function(event) {
    clearInterval(intervalID);
    intervalID = setInterval(checkforupdate, 3000,event.data);

};