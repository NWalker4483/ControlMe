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

    function press(r,a){

    }
    function stop(r){

    }

    $(document).ready(function(){
    namespace = '/test'; // change to an empty string to use the global namespace
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('flow', function(msg) {
    $('#'+msg.data[0]+'a').html(msg.data[0]+': '+msg.data[1]);
    });
    $('.slider').live('input', function() {
    socket.emit('robot', {motor: $(this).attr('id'),value: $(this).val()});
    return false;
    });
    function canGame() {
    return "getGamepads" in navigator;
    }
    if(canGame()) {
    var prompt = "To begin using your gamepad, connect it and press any button!";
    $("#gamepadPrompt").text(prompt);

    $(window).on("gamepadconnected", function() {
    $("#gamepadPrompt").html("Gamepad connected!");
    console.log("connection event");
    });

    $(window).on("gamepaddisconnected", function() {
    console.log("disconnection event");
    $("#gamepadPrompt").text(prompt);
    });
    }
    else{
    var pro = "Try Again, Later";
    $("#gamepadPrompt").text(pro);
    }
    });