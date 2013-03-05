
// dispatch list variables
var dispatch_listview=[],
    last_dispatch=[],
    last_li=[];


$.fn.extend({
    disableSelection: function() {
        this.each(function() {
            this.onselectstart = function() {
                return false;
            };
            this.unselectable = "on";
            $(this).css('-moz-user-select', 'none');
            $(this).css('-webkit-user-select', 'none');
        });
    }
});


// map related function


//hydrant functions

function Hydrant_Info(hydrant_metadata){
    response=[]
    response[0]=hydrant_metadata.ADDRESS
    response[1]="FLOW: "+hydrant_metadata.FLOW
    response[2]="HYDRANT ID: "+hydrant_metadata.HYDRANT_ID
    response[3]="DATE_INSPE: "+hydrant_metadata.DATE_INSPE
    response[4]="TYPE: "+hydrant_metadata.TYPE+" "+hydrant_metadata.TYPE0
    response[5]="VALVE SIZE: "+hydrant_metadata.VALVE_SIZE
    response[6]="VALVE TYPE: "+hydrant_metadata.VALVE_TYPE
    return response.join("</br>")    
}

function set_hydrant_click(hydrant_marker,hydrant){
    var infowindow = new google.maps.InfoWindow({
         content: Hydrant_Info(hydrant),
         position:hydrant_marker.LatLng,                     
     });
    google.maps.event.addListener(hydrant_marker, 'click',
        function() {
            infowindow.open(hydrant_map().map,hydrant_marker);
    });
}

function setHydrants(hydrants) {

    for (var index in hydrants) {
        hydrant = hydrants[index].metadata
        // need this because some hydrants have the same '0-0' id
        hydrant_unique=hydrant.LATITUDE+hydrant.LONGITUDE
        if (!hydrant_markers[hydrant_unique]) {
            var hyd_marker = new google.maps.Marker({
                map: hydrant_map().map,
                position: new google.maps.LatLng(hydrant.LATITUDE, hydrant.LONGITUDE),
                icon: "/static/img/hydrant.png"
            });
            
            hydrant_markers[hydrant_unique] = hyd_marker;
            set_hydrant_click(hyd_marker, hydrant);

        }
    }
};


function getHydrants(dspLocation){
    dfd=new $.Deferred();
    $.ajax({
        type:"GET",
        url:"http://oklahomadata.org/boundary/1.0/point/",
        dataType:"jsonp",
        data:{
          near:  dspLocation.lat()+","+dspLocation.lng()+",250m",
          sets:"hydrants",
          limit:50,
          offset:0,
          format:"jsonp",
        }
    })
    .done(function(data){
        hydrants_returned=data.meta.total_count;
        if (hydrants_returned>0){
            setHydrants(data.objects);
        }
        dfd.resolve();    
    });
    
    return dfd.promise();
};

// dispatch marker functions
function setMarker(dispatch_location,info_text){
    var dfd=$.Deferred();
    if(dispatch_location){
        
        var marker = new google.maps.Marker({
            map: hydrant_map().map,
            position: dispatch_location,
            icon: "/static/img/tfdd_map_icon.png"
        });

        hydrant_map().dispatch_marker=marker;

        var info_html="<div style='font-size: small '>"+info_text+"</div>"

        var infowindow = new google.maps.InfoWindow({
                content: info_html,
                disableAutoPan:true
                });

         google.maps.event.addListener(marker, 'click', function() {
           infowindow.open(hydrant_map().map,marker);
         }); 

         infowindow.open(hydrant_map().map,marker);
    }
     
   
   dfd.resolve(marker);
   
   return dfd.promise();  
   
};








// geocoding function
newAddress=function (address){
    var dfd=$.Deferred(),
    geocoder = geocoder || new google.maps.Geocoder();
    
    var clean_address=function (address){
        var ca=address.split("@");
        return ca[ca.length-1];
    };
    
    var accept_address= function (new_loc){
        map.setCenter(new_loc);
        dfd.resolve(new_loc);        
    };        

    var gcode= function (address){
        var gfd= new $.Deferred();
        geocoder.geocode( {
            'address': clean_address(address),
            'bounds':this.bounds,
            }, function(results, status) {
                loc=results[0].geometry.location;
                if (status !== google.maps.GeocoderStatus.OK) {
                    gfd.reject(0); //really bad, don't even bother
                }
                if (tulsaBounds.contains(loc)){
                    gfd.resolve(loc)
                } else {
                    gfd.reject(1);//not so bad, try with Tulsa, OK
                }
            
            });
        return gfd.promise();        
    };
    
    if (address){
        geocode(address)
            .done(function(loc){
               accept_address(loc);
            })
            .fail(function(result){
                if (results===1){
                    geocode(address+" Tulsa, OK")
                        .done(function(loc) {
                            accept_address(loc);
                        }):
                        .fail(function() {
                            dfd.reject();
                        };)
                } else {
                    dfd.reject();
                }
            });
    }  
        
    return dfd.promise();
};


// tfdd map 
var tfdd_map= function (element){    
    // 'tulsa 36.1539,-95.9925'
        var 
        sw= sw || new google.maps.LatLng(35.93131670856903, -96.141357421875),
        ne= ne || new google.maps.LatLng(36.26199220445664, -95.701904296875),
        tulsaLatlng=  tulsaLatlng ||  new google.maps.LatLng(36.1539,-95.9925),
        tulsaBounds=  tulsaBounds ||  new google.maps.LatLngBounds(sw,ne),
        dispatch_marker=null,
        hydrant_markers={},
        dispatchMapOptions = {
            zoom: 16,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            center:tulsaLatlng,

            panControl: false,
            scaleControl: false,
            overviewMapControl: false,

            streetViewControl: true,
            streetViewControlOptions: {
                position: google.maps.ControlPosition.LEFT_CENTER,
            },

            mapTypeControl: true,
            mapTypeControlOptions: {
                position: google.maps.ControlPosition.LEFT_BOTTOM,
            },

            zoomControl: true,
            zoomControlOptions: {
                style: google.maps.ZoomControlStyle.SMALL,
                position: google.maps.ControlPosition.RIGHT_CENTER,
            },
        };
          
    this.__defineSetter__("map", function (element){
        if (element){
            var map = map || new google.maps.Map(element, dispatchMapOptions);        
        }
        return map;
        });
        
    this.__defineGetter__("map", function(){
               return map;
           });
         
    return {
        marker: dispatch_marker,
        bounds: tulsaBounds,
        LatLng: tulsaLatlng,
        setMarker: setMarker,
        newAddress: newAddress,
            
        };               
};




