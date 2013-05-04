"use strict";
// dispatch list variables
var dispatch_listview = [],
    last_dispatch = [],
    last_li = [];


$.fn.extend({
    disableSelection: function () {
        this.each(function () {
            this.onselectstart = function () {
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
var hydrant_set = function (owning_map) {
    var these_hydrants = {},

    Hydrant_Info = function (hydrant_metadata) {
        var response = [];
        response[0] = hydrant_metadata.ADDRESS;
        response[1] = "FLOW: "       + hydrant_metadata.FLOW;
        response[2] = "HYDRANT ID: " + hydrant_metadata.HYDRANT_ID;
        response[3] = "DATE_INSPE: " + hydrant_metadata.DATE_INSPE;
        response[4] = "TYPE: "       + hydrant_metadata.TYPE + " " + hydrant_metadata.TYPE0;
        response[5] = "VALVE SIZE: " + hydrant_metadata.VALVE_SIZE;
        response[6] = "VALVE TYPE: " + hydrant_metadata.VALVE_TYPE;
        return response.join("</br>");
    },

    set_hydrant_click = function (hydrant_marker, hydrant) {
        var infowindow = new google.maps.InfoWindow({
                content:  Hydrant_Info(hydrant),
                position: hydrant_marker.LatLng                     
         });
        google.maps.event.addListener(hydrant_marker, 'click',
            function () {
                infowindow.open(owning_map, hydrant_marker);
        });
    },

    setHydrants = function (hydrant_data) {
        for (var index in hydrant_data) {
            var hydrant = hydrant_data[index].metadata;
            // need this because some hydrants have the same '0-0' id
            var hydrant_unique=''+hydrant.LATITUDE+hydrant.LONGITUDE;
            if (!these_hydrants[hydrant_unique]) {
                var hyd_marker = new google.maps.Marker({
                    map: owning_map,
                    position: new google.maps.LatLng(hydrant.LATITUDE, hydrant.LONGITUDE),
                    icon: "/static/img/hydrant.png"
                });
            
                these_hydrants[hydrant_unique] = hyd_marker;
                set_hydrant_click(hyd_marker, hydrant);

            }
        }
    };
    
    this.getHydrants = function (loc) {
        var dfd = new $.Deferred();
        
        $.ajax({
            type:"GET",
            url:"http://oklahomadata.org/boundary/1.0/point/",
            dataType:"jsonp",
            data:{
              near:  loc.lat() + "," + loc.lng() + ",250m",
              sets:"hydrants",
              limit:50,
              offset:0,
              format:"jsonp",
            }
        })
        .done(function (data) {
            var hydrants_returned = data.meta.total_count;
            if (hydrants_returned > 0){
                setHydrants(data.objects);
            }
            dfd.resolve();    
        });        
        return dfd.promise();
    }; 
    
    this.clearHydrants = function () {
        for  (var m in these_hydrants){
            these_hydrants[m].setMap(null);
        };
        these_hydrants = {};   
    };

};



// dispatch marker functions

var dispatch= function (owning_map) {
    var sw = sw || new google.maps.LatLng(35.93131670856903, -96.141357421875),
        ne = ne || new google.maps.LatLng(36.26199220445664, -95.701904296875),
    tulsaBounds =  tulsaBounds ||  new google.maps.LatLngBounds(sw,ne);
       
    this.marker = null;
        
    this.setMarker = function (dispatch_location,info_text) {
        var dfd = $.Deferred();
        if(dispatch_location){

            this.marker = this.marker || new google.maps.Marker({
                map: owning_map,
                icon: "/static/img/tfdd_map_icon.png"
            });
         
            this.marker.setPosition(dispatch_location);
        
            var info_html = "<div style='font-size: small '>"+info_text+"</div>"

            var infowindow = new google.maps.InfoWindow({
                    content: info_html,
                    disableAutoPan:true
                    });

             google.maps.event.addListener(this.marker, 'click', function () {
               infowindow.open(owning_map,this.marker);
             }); 

             infowindow.open(owning_map,this.marker);
             dfd.resolve(this.marker);
        }
       
       return dfd.promise();  
    };


    // geocoding function
    this.setAddress = function (address) {
        var dfd=$.Deferred(),
        geocoder = geocoder || new google.maps.Geocoder(),    
        
        clean_address = function (address) {
            var ca = address.split("@");
            return ca[ca.length-1];
        },
    
        gcode = function (address) {
            var gfd = new $.Deferred();
            geocoder.geocode( {
                'address': clean_address(address),
                'bounds':tulsaBounds,
                }, function(results, status) {
                    if (status !== google.maps.GeocoderStatus.OK) {
                        gfd.reject(0); //really bad, don't even bother
                        
                    } else {
                        var loc=results[0].geometry.location;
                        if (tulsaBounds.contains(loc)){
                            gfd.resolve(loc)
                        } else {
                            gfd.reject(1);//getting close, try with Tulsa, OK
                        }
                    }            
                });
            return gfd.promise();        
        };
    

        if (address){
            gcode(address)
                .done(function (loc) {
                   dfd.resolve(loc);
                })
                .fail(function (result) {
                    if (result === 1){
                        geocode(address+" Tulsa, OK")
                            .done(function (loc) {
                                dfd.resolve(loc);
                            })
                            .fail(function () {
                                dfd.reject();
                            });
                    } else {
                        dfd.reject();
                    }
                });
        }  
        
        return dfd.promise();
    };
};

// tfdd map 
var tfdd_map= function (element) {    
    // 'tulsa 36.1539,-95.9925'
        
        var map_element = null,
        tulsaLatlng =  tulsaLatlng ||  new google.maps.LatLng(36.1539,-95.9925),
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

    if (element !== map_element){
        map_element = element;
        
        this.map = new google.maps.Map(element, dispatchMapOptions);        
        this.map.dispatch = new dispatch(this.map);
        this.map.hydrants = new hydrant_set(this.map);
    }

    return this.map;
};




