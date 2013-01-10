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
            distance_to_bottom = ($(window).scrollTop() + $(window).height()) - last_li.offset().top;
            if (distance_to_bottom > -1000) {
                    GetMoreDispatches();    
            } else {                        
                SchedulePositionCheck();
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
              disableSelection : function() { 
                      this.each(function() { 
                              this.onselectstart = function() { return false; }; 
                              this.unselectable = "on"; 
                              $(this).css('-moz-user-select', 'none'); 
                              $(this).css('-webkit-user-select', 'none'); 
                      }); 
              } 
      });
