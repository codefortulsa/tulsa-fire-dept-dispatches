    var scrollHappens=false,
        dispatch_listview=[],
        last_dispatch=[],
        last_li=[],
        UpdateCheckScheduled=false,
        PositionCheckScheduled=false;
        
    function SchedulePositionCheck(){
        if(!PositionCheckScheduled){
            PositionCheckScheduled=true;
            setTimeout(function() {
                PositionCheckScheduled=false;                
                PositionCheck();
                }, 2500);
        }
    };

    function ScheduleUpdateCheck(nextCheck){
        if (!UpdateCheckScheduled){
            UpdateCheckScheduled=true;            
            setTimeout(function() {
                UpdateCheckScheduled=false;
                UpdateCheck();
                }, nextCheck);
        }
    };
    
    function GetMoreDispatches() {
        $.ajax({
            url: last_dispatch.data("tf-more-url"),
            success: function(data) {
                var more_dispatches=$("li.dispatch",data);
                if (more_dispatches.length>0){
                    last_dispatch.attr("id", "xxx")     // this isn't last anymore
                    $("#dispatch_listview",$.mobile.activePage).append(more_dispatches).listview('refresh').trigger("create");
                    $("abbr.timeago").timeago(); 
                    last_dispatch=$("#last_dispatch", $.mobile.activePage); // reset the new last dispatch
                    gettingMore=false;
                    SchedulePositionCheck();          
                } else{
                    $("#list_end",$.mobile.activePage).text("");
                    gettingMore=false;
                    
                }                
            },
            error: function(){
                gettingMore=false;
                SchedulePositionCheck();
                }
        })
      
    };

    function PositionCheck() {
        if (scrollHappens){
            scrollHappens=false;
            if (last_li.length>0){
                distance_to_bottom = ($(window).scrollTop() + $(window).height()) - last_li.offset().top;
                if (distance_to_bottom > -1000) {
                        GetMoreDispatches();    
                } else {                        
                    SchedulePositionCheck();
                }
            }
        } else{
            SchedulePositionCheck();
        }
    };


    function UpdateCheck (){
        
         if(dispatch_listview.length>0){
             $.ajax({ 
                 url: $(dispatch_listview.children()[0]).data("tf-update-url"),
                 success: function(data){
                     $.mobile.loading( 'show', {
                     	text: 'Incoming Dispatch',
                     	textVisible: true,
                     });
                     $(dispatch_listview).prepend($("li.dispatch", data)).listview('refresh').trigger( "create" );                     
                     $("abbr.timeago").timeago();
                     ScheduleUpdateCheck(5000);                     
                     setTimeout(function() {
                         $.mobile.loading('hide');
                         }, 1500);
                 },
                error: function(){
                    ScheduleUpdateCheck(5000);                  
                }
             })
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



var
// 'tulsa 36.1539,-95.9925'
sw=new google.maps.LatLng(35.93131670856903, -96.141357421875),
ne=new google.maps.LatLng(36.26199220445664, -95.701904296875),
tulsaBounds= new google.maps.LatLngBounds(sw,ne),
geocoder = new google.maps.Geocoder();

var dispatchMapOptions = {
    zoom: 14,
    mapTypeId: google.maps.MapTypeId.ROADMAP,

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


function tulsaGeocode(address,callback){
    var clean_address=address.split("@");
    clean_address=clean_address[clean_address.length-1];
    geocoder.geocode( {
        'address': clean_address,
        'bounds':tulsaBounds,
        }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            result_location=results[0].geometry.location;
            if (tulsaBounds.contains(result_location)){
               callback(results[0].geometry.location);                
            } else {
                geocoder.geocode({
                   'address': clean_address+" Tulsa, OK",
                   'bounds':tulsaBounds, 
               }, function(results, status) {
               if (status == google.maps.GeocoderStatus.OK) {
                   callback(results[0].geometry.location);
               } 

            });
        }
    }
    });
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

function set_hydrants(hydrants) {

    for (var index in hydrants) {
        hydrant = hydrants[index].metadata
        if (!hydrant_markers[hydrant.HYDRANT_ID]) {
            hydrant_markers[hydrant.HYDRANT_ID] = true;
            var hydLatLng = new google.maps.LatLng(
            hydrant.LATITUDE, hydrant.LONGITUDE);
            var hyd_marker = new google.maps.Marker({
                map: map,
                position: hydLatLng,
                icon: "/static/img/hydrant.png"
            });

            window.setTimeout(set_hydrant_click(hyd_marker, hydrant),100);

        }
    }

};


function getHydrants(limit,offset){
    mapLatlng=map.getCenter();
    $.ajax({
        url:"http://oklahomadata.org/boundary/1.0/point/",
        data:{
          near:  mapLatlng.lat()+","+mapLatlng.lng()+",500m",
          sets:"hydrants",
          limit:limit,
          offset:0,
          format:"jsonp",
        },  
        dataType:"jsonp",
        beforeSend: function(xhr)   
            {
                xhr.setRequestHeader("Connection", "close");
            },
        success:function(data){
            hydrants_returned=data.meta.total_count;
            if (hydrants_returned>0){
                set_hydrants(data.objects);    
                if (data.objects.length == limit){
                    getHydrants(limit,limit+offset);                    
                }
            }            
        },
        error:function(data){
            
        }
        
    });
};
