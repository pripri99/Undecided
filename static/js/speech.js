var city = "";
var keyword = "";
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
          $.ajax({
            url: "/getmethod",
            data: {
              javascript_data: JSON.stringify(res[0].transcript)
            },
            method: "GET",
            success: function (response) {
                console.log("Success")
                console.log(response)
                //document.getElementById("eventDisplay").innerHTML = response;
            },
            error: function (xhr) {
                console.log(xhr)
                document.getElementById("err").innerHTML = "Unable to Display Events Summary"
            }
        });
          /*$.post("/postmethod", {
            javascript_data: JSON.stringify(res[0].transcript)
          }, function(data){
            console.log(data)
          });*/
          //console.log(answer);
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
      //search()
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

function getEventSummary(keyword, category, distance, latitude, longitude) {
  if (distance === undefined || distance == "") {
      distance = 10
  }
  $.ajax({
      url: "/getEventsSummary",
      data: {
          k: keyword,
          c: category,
          d: distance,
          lat: latitude,
          long: longitude
      },
      method: "GET",
      success: function (response) {
          console.log("Success")
          document.getElementById("eventDisplay").innerHTML = response;
      },
      error: function (xhr) {
          console.log(xhr)
          document.getElementById("err").innerHTML = "Unable to Display Events Summary"
      }
  });
}

function search() {
  event.preventDefault();
  var latLong, latitude, longitude;
  document.getElementById("eventDisplay").innerHTML = ""
  document.getElementById("eventDetailDisplay").innerHTML = ""
  var keyword = document.getElementById("ipkeyword").value
  var category = document.getElementById("ipCategory").value
  var distance = document.getElementById("ipDistance").value
  var currentLocation = document.getElementById("currentLocation").checked
  if (currentLocation == true) {
      latLong = current.split(",")
      latitude = latLong[0]
      longitude = latLong[1]
      getEventSummary(keyword, category, distance, latitude, longitude)
  } else {
      latLong = document.getElementById("enteredLoc").value
      $.ajax({
          url: "/getEnteredLocation",
          data: {
              location: latLong
          },
          method: "GET",
          success: function (response) {
              loc = response.results[0].geometry.location
              console.log(loc)
              latitude = loc.lat;
              longitude = loc.lng;
              var abc = getEventSummary(keyword, category, distance, latitude, longitude)
              console.log(abc)
          },
          error: function (xhr) {
              console.log(xhr)
          }
      });
  }
}

function onEventClick(x) {
  $.ajax({
      url: "/fetchEventDetail",
      data: {
          i: x,
      },
      method: "GET",
      success: function (response) {
          console.log("Success")
          document.getElementById("eventDetailDisplay").scrollIntoView({ behavior: 'smooth' });
          document.getElementById("eventDetailDisplay").innerHTML = response;
      },
      error: function (xhr) {
          console.log(xhr)
      }
  });
}