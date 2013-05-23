// this is a web worker to poll for incoming dispatches
var intervalID,
    request= request || new XMLHttpRequest();

request.onreadystatechange = function () {
    if (request.readyState === 4) {
        // XHR state is DONE
        if (request.status == 200) {
            clearInterval(intervalID);
            self.postMessage(request.responseText);
        }
    }
};

function checkforupdate(tfdd_update_url) {
    request.open('GET', tfdd_update_url, true);
    request.send();
};
    
self.onmessage = function(event) {
    clearInterval(intervalID);
    intervalID = setInterval(checkforupdate, 3000,event.data);

};