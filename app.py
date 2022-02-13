from flask import Flask, render_template, request
import requests
import json
import pygeohash as pgh

from requests.api import head
#import event_routes

# App Config 
app = Flask(__name__)
app.config.from_object('config')



@app.route("/")
def index():
  print(request.endpoint)
  return render_template('pages/home.html')

@app.route("/ask")
def ask():
  print(request.endpoint)
  return render_template('pages/discussion/askMeAnything.html')

@app.route("/community")
def community():
  print(request.endpoint)
  return render_template('pages/discussion/community.html')

@app.route("/conversation")
def conversation():
  print(request.endpoint)
  return render_template('pages/discussion/conversation.html')

@app.route("/register")
def register():
  return render_template('pages/auth/register.html')

@app.route("/login")
def login():
  return render_template('pages/auth/login.html')


@app.route("/logout")
def logout():
  return "Login out"


# Events search
@app.route('/event', methods=['GET'])
def event():
    print("in event")
    return render_template('pages/event.html')

@app.route("/getEnteredLocation",methods=['GET'])
def getEnteredLocation():
    headers = {
        'Content-Type': 'application/json'
    }
    loc = request.args.get('location')
    requestResponse = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+loc+"&key=AIzaSyB12zd-IK1elQmCzGLPiTy9LX7e2Fp2uf4", headers=headers)
    loc=requestResponse.json()['results'][0]['geometry']['location']
    return requestResponse.json()

@app.route("/fetchEventDetail",methods=['GET'])
def fetchEventDetail():
    headers = {
        'Content-Type': 'application/json'
    }
    id = request.args.get('i')
    requestResponse = requests.get("https://app.ticketmaster.com/discovery/v2/events/"+id+"?apikey=zNz1fE2HP3JJMYr8lAG1OfinYwVqRXh7", headers=headers)
    event=requestResponse.json()
    try:
        localDate=event['dates']['start']['localDate']
    except:
        localDate=""
    try:
        localTime=event['dates']['start']['localTime']
    except:
        localTime=""
    try:
        currency=event['priceRanges'][0]['currency']
    except:
        currency="(Currency not defined)"
    try:
        name=event['name']
    except:
        name="N/A"
    try:
        seatMap=event['seatmap']['staticUrl']
        alignment="left"
    except:
        seatMap=""
        alignment="center"
    try:
        buyTicketAt=event['url']
    except:
        buyTicketAt=""
    try:
        priceMin=str(event['priceRanges'][0]['min'])
    except:
        priceMin="N/A"
    try:
        priceMax=str(event['priceRanges'][0]['max'])
    except:
        priceMax="N/A"
    try:
        ticketStatus=event['dates']['status']['code'].capitalize()
    except:
        ticketStatus=""
    try:
        venue=event['_embedded']['venues'][0]['name']
    except:
        venue=""
    genre=[]
    try:
        if(event['classifications'][0]['subGenre']['name']!="Undefined" and event['classifications'][0]['subGenre']['name']!="undefined"):
            genre.append(event['classifications'][0]['subGenre']['name'])
    except:
        pass
    try:
        if(event['classifications'][0]['genre']['name']!="Undefined" and event['classifications'][0]['genre']['name']!="undefined"):
            genre.append(event['classifications'][0]['genre']['name'])
    except:
        pass
    try:
        if(event['classifications'][0]['segment']['name']!="Undefined" and event['classifications'][0]['segment']['name']!="undefined"):
            genre.append(event['classifications'][0]['segment']['name'])
    except:
        pass
    try:
        if event['classifications'][0]['subType']['name']!="Undefined" and event['classifications'][0]['subType']['name']!="undefined":
            genre.append(event['classifications'][0]['subType']['name'])
    except:
        pass
    try:
        if event['classifications'][0]['type']['name']!="Undefined" and event['classifications'][0]['type']['name']!="undefined":
            genre.append(event['classifications'][0]['type']['name'])
    except:
        pass
    print(genre)
    genre_string=""
    genre_string=" | ".join(genre)
    print(genre_string)


    message='''    <div id="outerDiv"><div  id="outerDivHeader">'''+name+'''</div><div id="detailDisp"> <div style="flex: 1; text-align:'''+alignment+''';">'''
    if(localDate!="" or localTime!=""):
        message=message+'''<label class="display">Date</label><br>'''+localDate+ " " + localTime +'''<br><br>'''

    

    try:
        artistArray=event['_embedded']['attractions']
        message=message+'''<label class="display">Artist / Team</label><br>'''
        for index, i in enumerate(artistArray):
            if index != 0:
                message=message+" | "
            message=message + '''<a href="'''+i['url']+'''" target="_blank">'''+i['name']+'''</a>'''
        message=message+'''<br><br>'''
    except:
        pass
    if(venue!=""):
        message=message+'''<label class="display">Venue</label><br>'''+venue+ '''<br><br>'''

    if(genre_string!=""):
        message=message+'''<label class="display">Genres</label><br>'''+genre_string+'''<br><br>'''

    if(priceMin!="N/A" or priceMax!="N/A" or currency!="(Currency not defined)"):
        message=message+'''<label class="display">Price Ranges</label><br>'''+priceMin+" - "+priceMax+" "+currency+" "+'''<br><br>'''
    
    if(ticketStatus!=""):
        message=message+'''<label class="display">Ticket Status</label><br>'''+ticketStatus+'''<br><br>'''
    
    if(buyTicketAt!=""):
        message=message+'''<label class="display">Buy Ticket At</label><br><a href="'''+buyTicketAt+'''" target="_blank">Ticketmaster</a><br><br></div>'''

    if seatMap!="":
        message=message+'''<div style="flex:1"><img src="'''+seatMap+'''" alt="Seatmap is not available" style="width:500px; "/></div>'''
    
    message=message+'''</div></div>'''
    return message

@app.route("/getEventsSummary",methods=['GET'])
def getEventsSummary():
    headers = {
        'Content-Type': 'application/json'
    }
    keywords = request.args.get('k')
    category=  request.args.get('c')
    dist= request.args.get('d')
    latitude= request.args.get('lat')
    longitude= request.args.get('long')
    geohash=pgh.encode(float(latitude),float(longitude),4)
    if(category!="default"):
        requestResponse = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?apikey=90gXEdRlVnZgTqo4zfSfAh3JkIZ9IvKR&keyword="+keywords+"&segmentId="+category+"&radius="+dist+"&unit=miles&geoPoint="+geohash, headers=headers)
    else:
        requestResponse = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?apikey=90gXEdRlVnZgTqo4zfSfAh3JkIZ9IvKR&keyword="+keywords+"&radius="+dist+"&unit=miles&geoPoint="+geohash, headers=headers)
    evnts=requestResponse.json()
    totalEvents=evnts['page']['totalElements'] 
    if totalEvents==0:
        return '''<div style="text-align: center; background-color: #f9f9f9f1; border: 1px solid lightgray;margin-left: 25%; margin-right: 25%;">No Records has been found<br></div>
        <br><hr style="color:lightgray; margin-left:10%; margin-right:10%"></div>'''
    else:
        events=evnts['_embedded']['events']
        message='''<div><table id="table"
                    data-toggle="table"
              data-filter-control="true" 
              data-show-export="true"
              data-click-to-select="true"
              data-toolbar="#toolbar"
              class="respon-table respon-table-scroll">

                    <thead role="presentation" aria-hidden="false">
		 <tr role="row" tabindex="0">
			  <th id="date" class="date" role="columnheader" data-field="date" data-filter-control="input" data-sortable="true" aria-label="Itinerary">Date</th>
			  <th id="icon" class="icon" role="columnheader" data-field="icon" data-filter-control="select" data-sortable="true" aria-label="airline">Icon</th>
			  <th id="event" class="event" role="columnheader" data-field="event" data-filter-control="select" data-sortable="true" aria-label="departing">Event</th>
			  <th id="genre" class="genre" role="columnheader" data-field="genre" data-filter-control="select" data-sortable="true" aria-label="returning">Genre</th>
        <th id="venue" class="venue" role="columnheader" data-field="venue" data-filter-control="select" data-sortable="true" aria-label="returning">Venue</th>
		 </tr>
	</thead>
                <tbody role="presentation" aria-hidden="false"> <tr role="row" tabindex="0">'''
        for event in events:
            try:
                localDate=event['dates']['start']['localDate']
            except:
                localDate=""
            try:
                localTime=event['dates']['start']['localTime']
            except:
                localTime=""
            try:
                imgUrl=event['images'][0]['url']
            except:
                imgUrl=""
            try:
                id=event['id']
            except:
                id=""
            try:
                name=event['name']
            except:
                name="N/A"
            try:
                genre=event['classifications'][0]['segment']['name']
            except:
                genre="N/A"
            try:
                venue=event['_embedded']['venues'][0]['name']
            except:
                venue="N/A"
            message=message + '''<td title="" aria-label="" headers="date" role="gridcell" tabindex="0" class="date">'''+localDate  + '''   '''+ localTime + "</td>"+'''<td class="icon" title="" aria-label="" headers="icon" role="gridcell" tabindex="0"><img class="iconImage" src="'''+ imgUrl +'''"/></td>'''+'''<td class="eventtag"  title="" aria-label="" headers="event" role="gridcell" tabindex="0"><a class="eventLink" onClick="onEventClick(\''''+id+'''\')">'''+name+'''</a></td><td class="genre" title="" aria-label="" headers="genre" role="gridcell" tabindex="0">'''+genre+'''</td><td class="venue" title="" aria-label="" headers="venue" role="gridcell" tabindex="0">'''+venue+'''</td></tr>'''
        message=message+'''</tbody></table>'''
        return message 

if __name__ == "__main__":
  app.run()