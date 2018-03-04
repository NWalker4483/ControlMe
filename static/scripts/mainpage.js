function toggle(r,a) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    document.getElementById("button"+r+a).innerHTML =
    this.responseText;
    }
    };
    xhttp.open("GET", "button/"+r+"/"+a+"/", true);
    xhttp.send();
    }
    $(document).ready(function(){
        if(canGame()) {
 var prompt = "To begin using your gamepad, connect it and press any button!";
 $("#gamepadPrompt").text(prompt);

 $(window).on("gamepadconnected", function() {
     hasGP = true;
     $("#gamepadPrompt").html("Gamepad connected!");
     console.log("connection event");
     repGP = window.setInterval(reportOnGamepad,100);
 });

 $(window).on("gamepaddisconnected", function() {
     console.log("disconnection event");
     $("#gamepadPrompt").text(prompt);
     window.clearInterval(repGP);
 });

 //setup an interval for Chrome
 var checkGP = window.setInterval(function() {
     console.log('checkGP');
     if(navigator.getGamepads()[0]) {
         if(!hasGP) $(window).trigger("gamepadconnected");
         window.clearInterval(checkGP);
     }
 }, 500);
}
    var hasGP = false;
    var repGP;

    function press(a){
        $("#gamepadPrompt").html(a.axes[1]);
    
	}
    function canGame() {
        return "getGamepads" in navigator;
    }
    namespace = '/test'; // change to an empty string to use the global namespace
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('flow', function(msg) {
    $('#'+msg.data[0]+'a').html(msg.data[0]+': '+msg.data[1]);
	});
	
    $("#Sliders").on('input', '.slider',function() {
    socket.emit('robot', {motor: $(this).attr('id'),value: $(this).val()});
    return false;
	});
    function reportOnGamepad() {
        var gp = navigator.getGamepads()[0];
        //Get Button State Menu
        var html = "";
            html += "id: "+gp.id+"<br/>";
 
        for(var i=0;i<gp.buttons.length;i++) {
            html+= "Button "+(i+1)+": ";
            if(gp.buttons[i].pressed) html+= " pressed";
            html+= "<br/>";
		}
		
        for(var i=0;i<gp.axes.length; i+=2) {
            html+= "Stick "+(Math.ceil(i/2)+1)+": "+Math.round(gp.axes[i]*100)+","+Math.round(gp.axes[i+1]*100)+"<br/>";
        }
 
        $("#gamepadDisplay").html(html);

function buttonPressed(b) {
  if (typeof(b) == "object") {
    return b.pressed;
  }
  return b == 1.0;
}
function axisMoved(b) {
  if (Math.round(b.axes[0])!=0||Math.round(b.axes[1])!=0) {
    return true;
  }
  return false;
}

    if (buttonPressed(gp.buttons[0])) {
    press(gp);
  } else if (buttonPressed(gp.buttons[2])) {
    press(gp);
  }
  if (buttonPressed(gp.buttons[1])) {
    press(gp);
  } else if (buttonPressed(gp.buttons[3])) {
    press(gp);
  }
  if(axisMoved(gp)){
    press(gp);
    socket.emit('robot', {motor: $(this).attr('id'),value: [Math.round(b.axes[0]),Math.round(b.axes[1])]});
    
  }
    }

 
});

 