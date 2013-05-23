// this is a web worker to get more dispatches at the end of a list

var requested_url=null,
    request= request || new XMLHttpRequest();

request.onreadystatechange = function () {
    if (request.readyState === 4) {
        // XHR state is DONE
        if (request.status == 200) {
            self.postMessage(request.responseText);
        }
    }
};

var getdispatches = function (tfdd_url) {
debugger;    request.open('GET', tfdd_url, true);
    request.send();
};
    
self.onmessage = function(event) {

    if (!(requested_url===event.data)){
        getdispatches(event.data);
    }

};