var recognition;
  var la = document.getElementById('ears');
      recognition = new webkitSpeechRecognition();
function startDictation() {
  document.getElementById('ears').className ="containerOn";
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.lang = "en-US";

      recognition.onresult = function(e) {
        
      for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
        document.getElementById('messageText').value = e.results[i][0].transcript;

       // recognition.stop();
       document.getElementById('ears').className ="containerOff";
         document.getElementById('chatbot-form-btn').click();
         
        // recognition.start();
        }}
      };
      
 recognition.start();
      recognition.onerror = function(e) {
        recognition.stop();
      }
      recognition.onspeechend = function() {
        //recognition.stop();
      }
      
    }


function stopDictation() {
         la.innerText="start speech";
        img.style.visibility = 'visible';
         img1.style.visibility = 'hidden';
        recognition.stop();

       }