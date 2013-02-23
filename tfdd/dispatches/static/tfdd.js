
// dispatch list variables
var dispatch_listview=[],
    last_dispatch=[],
    last_li=[];

function PositionCheck() {
    if (last_li.length>0){
        distance_to_bottom = ($(window).scrollTop() + $(window).height()) - last_li.offset().top;
        if (distance_to_bottom > -2000) {
            tf_more_url=last_dispatch.data("tf-more-url");
            getMoreDispatches_worker.postMessage(tf_more_url);
            
        } 
    }
};


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


// map related functions
// 
// 

var
// 'tulsa 36.1539,-95.9925'
sw=new google.maps.LatLng(35.93131670856903, -96.141357421875),
ne=new google.maps.LatLng(36.26199220445664, -95.701904296875),
tulsaLatlng=new google.maps.LatLng(36.1539,-95.9925),
tulsaBounds= new google.maps.LatLngBounds(sw,ne),
requestHydrants=false,
geocoder = new google.maps.Geocoder();


// map page variables
var map=null,
    dispatch_address,
    dispatch_call_type_desc,
    dispatch_map_page,
    currentLocation=null,
    dispatch_marker=null;

var hydrant_markers={};

var dispatchMapOptions = {
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


function tulsaGeocode(address){
    dfd=$.Deferred();
    
    var clean_address=address.split("@");
    clean_address=clean_address[clean_address.length-1];
    
    geocoder.geocode( {
        'address': clean_address,
        'bounds':tulsaBounds,
        }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            result_location=results[0].geometry.location;
            if (tulsaBounds.contains(result_location)){
                dfd.resolve(result_location);                
            } else {
                geocoder.geocode({
                   'address': clean_address+" Tulsa, OK",
                   'bounds':tulsaBounds, 
               }, function(results, status) {
               if (status == google.maps.GeocoderStatus.OK) {
                    dfd.resolve(results[0].geometry.location);
                } else {
                    dfd.reject();
                }
                });
            }
        }
    });
    return dfd.promise();
};

function dispatchMarker(dispatch_location,info_text){
    
    var marker = new google.maps.Marker({
        map: map,
        position: dispatch_location
    });

    dispatch_marker=marker;

    var infowindow = new google.maps.InfoWindow({
            content: info_text        
            });
    
     google.maps.event.addListener(marker, 'click', function() {
       infowindow.open(map,marker);
     }); 
    infowindow.open(map,marker);
   
      
};


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
            infowindow.open(map,hydrant_marker);
    });
}

function setHydrants(hydrants) {

    for (var index in hydrants) {
        hydrant = hydrants[index].metadata
        if (!hydrant_markers[hydrant.HYDRANT_ID]) {
            var hyd_marker = new google.maps.Marker({
                map: map,
                position: new google.maps.LatLng(hydrant.LATITUDE, hydrant.LONGITUDE),
                icon: "/static/img/hydrant.png"
            });
            
            hydrant_markers[hydrant.HYDRANT_ID] = hyd_marker;
            
            set_hydrant_click(hyd_marker, hydrant);

        }
    }
};


function getHydrants(dspLocation,limit,offset){

    $.ajax({
        type:"GET",
        url:"http://oklahomadata.org/boundary/1.0/point/",
        dataType:"jsonp",
        data:{
          near:  dspLocation.lat()+","+dspLocation.lng()+",250m",
          sets:"hydrants",
          limit:limit,
          offset:offset,
          format:"jsonp",
        }
    })
    .done(function(data){
        hydrants_returned=data.meta.total_count;
        if (hydrants_returned>0){
            setHydrants(data.objects);    
            // if (data.objects.length === limit){
            //     getHydrants(dspLocation=dspLocation,limit=limit,offset=limit+offset);                    
            // }
        }             
    });

};
