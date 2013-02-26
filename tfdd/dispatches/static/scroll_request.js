// this is a web worker to get more dispatches at the end of a list

var requested_url=null;

function getdispatches(tfdd_url) {
    var request = new XMLHttpRequest();
    request.open('GET', tfdd_url, false);
    request.send();
    if (request.status === 200) {
        self.postMessage(request.responseText);
    }
};
    
self.onmessage = function(event) {

    if (!(requested_url===event.data)){
        getdispatches(event.data);
    }

};