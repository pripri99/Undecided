window.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("button");
    const result = document.getElementById("result");
    const main = document.getElementsByTagName("main")[0];
    let listening = false;
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (typeof SpeechRecognition !== "undefined") {
      const recognition = new SpeechRecognition();

      const stop = () => {
        main.classList.remove("speaking");
        recognition.stop();
        button.textContent = "Start listening";
      };

      const start = () => {
        main.classList.add("speaking");
        recognition.start();
        button.textContent = "Stop listening";
      };

      const onResult = event => {
        result.innerHTML = "";
        for (const res of event.results) {
          const text = document.createTextNode(res[0].transcript);
          const p = document.createElement("p");
          if (res.isFinal) {
            p.classList.add("final");
            $.post( "/postmethod", {
                javascript_data: JSON.stringify(res[0].transcript)
            });
          }
          p.appendChild(text);
          result.appendChild(p);
        }

        

      };
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.addEventListener("result", onResult);
      button.addEventListener("click", event => {
        listening ? stop() : start();
        listening = !listening;
        console.log(listening);
        console.log(document.getElementById("messageF"));
        /*if (listening == false) {
            data = document.getElementsByClassName("final");
            console.log(data);
            // POST Data
            $.post( "/postmethod", {
                javascript_data: data
            });
        }*/
        
      });
    } else {
      button.remove();
      const message = document.getElementById("message");
      message.removeAttribute("hidden");
      message.setAttribute("aria-hidden", "false");
    }
});