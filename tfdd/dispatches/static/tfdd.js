    var scrollHappens=false,
        gettingMore=false,
        last_li="";
        
    function SchedulePositionCheck(nextCheck){
        setTimeout(function() {PositionCheck();}, nextCheck);
    };

    function GetMoreDispatches(last_dispatch) {
        $.ajax({
            url: last_dispatch.data("tf-more-url"),
            success: function(data) {
                var more_dispatches=$("li",data);
                
                if (more_dispatches.length>0){
                    last_dispatch.attr("id", "xxx")     // this isn't last anymore                        
                    $("#dispatch_listview",$.mobile.activePage).append(more_dispatches).listview('refresh').trigger("create");
                    last_dispatch=$("#last_dispatch", $.mobile.activePage); // reset the new last dispatch
                    gettingMore=false;
                    SchedulePositionCheck(500);          
                } else{
                    $("#list_end",$.mobile.activePage).text("");
                    gettingMore=false;
                    
                }                
                     
            },
            error: function(){
                gettingMore=false;
                SchedulePositionCheck(500);
                }
        })
      
    };

    function PositionCheck() {

        if (scrollHappens){
            scrollHappens=false;
            last_li=$("#list_end",$.mobile.activePage),    
            distance_to_bottom = ($(window).scrollTop() + $(window).height()) - last_li.offset().top;
            if (distance_to_bottom > -500 && !gettingMore) {
    
                    gettingMore=true;
                    
                    last_dispatch=$("#last_dispatch", $.mobile.activePage);

                    GetMoreDispatches(last_dispatch);
                    
            } else {                        
                SchedulePositionCheck(750);
            }
        } else{
            SchedulePositionCheck(500);
        }
    
    };


    function UpdateCheck (){

        $(".dispatch_listview").each(function(index,dispatch_listview){
             $.ajax({
                 url: $(dispatch_listview.children[0]).data("tf-update-url"),
                 success: function(data){
                     $('.cylon_eye').css("background-color","green");
                     $.mobile.loading( 'show', {
                     	text: 'Incoming Dispatch',
                     	textVisible: true,
                     });
                     setTimeout(function() {
                         $(dispatch_listview).prepend($("li", data)).listview('refresh').trigger( "create" );
                         $.mobile.loading( 'hide');
                         $('.cylon_eye').css("background-color","red");
                         }, 750);
                 }
             })
          });                   
     };

