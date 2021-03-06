var current="New York";
function getUserLoc() {
    let apiKey = '11e89d5932b74164834b90e6e5d99d87';
    $.getJSON('https://ipgeolocation.abstractapi.com/v1/?api_key=' + apiKey, function(data) {
    const res = JSON.parse(JSON.stringify(data, null, 2))
    //console.log(res);
    console.log(res.city);
    current= res.city;
    document.getElementById("searchButton").disabled=false;
    });

    //document.getElementsByName('city')[0].placeholder=current;

}

        function enableDisableTB() {
            var location = document.getElementById("location");
            var enteredLoc = document.getElementById("enteredLoc");
            enteredLoc.disabled = location.checked ? false : true;
            enteredLoc.value=""
        }
        function getEventSummary(keyword,category,distance,latitude,longitude){
            if(distance===undefined || distance==""){
                distance=10
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
                    success: function(response) {
                        console.log("Success")
                        document.getElementById("eventDisplay").innerHTML = response;
                    },
                    error: function(xhr) {
                        console.log(xhr)
                        document.getElementById("err").innerHTML="Unable to Display Events Summary"
                    }
                });
        }
        function onClickSearch(){
            event.preventDefault();
            var latLong,latitude,longitude;
            document.getElementById("eventDisplay").innerHTML=""
            document.getElementById("eventDetailDisplay").innerHTML=""
            var keyword=document.getElementById("ipkeyword").value
            var category=document.getElementById("ipCategory").value
            var distance=document.getElementById("ipDistance").value
            var currentLocation=document.getElementById("currentLocation").checked
            if(currentLocation==true){
                latLong=current.split(",")
                latitude=latLong[0]
                longitude=latLong[1]
                getEventSummary(keyword,category,distance,latitude,longitude)
            }else{
                latLong=document.getElementById("enteredLoc").value
                $.ajax({
                    url: "/getEnteredLocation",
                    data: {
                        location: latLong
                    },
                    method: "GET",
                    success: function(response) {
                        loc=response.results[0].geometry.location
                        console.log(loc)
                        latitude=loc.lat;
                        longitude=loc.lng;
                        var abc=getEventSummary(keyword,category,distance,latitude,longitude)
                        console.log(abc)
                    },
                    error: function(xhr) {
                        console.log(xhr)
                    }
                });
            }
        }
        function onClickClear(){
            document.getElementById("ipkeyword").value=""
            document.getElementById("ipCategory").selectedIndex = 0
            document.getElementById("ipDistance").value=""
            document.getElementById("enteredLoc").value=""
            document.getElementById("enteredLoc").disabled=true
            document.getElementById("currentLocation").checked=true
            document.getElementById("location").checked=false
            document.getElementById("eventDisplay").innerHTML=""
            document.getElementById("eventDetailDisplay").innerHTML=""
        }

        function onEventClick(x){
            $.ajax({
                    url: "/fetchEventDetail",
                    data: {
                        i: x,
                    },
                    method: "GET",
                    success: function(response) {
                        console.log("Success")
                        document.getElementById("eventDetailDisplay").scrollIntoView({behavior: 'smooth'});
                        document.getElementById("eventDetailDisplay").innerHTML = response;
                    },
                    error: function(xhr) {
                        console.log(xhr)
                    }
                });
        }