import requests

url = "https://ticketmasterstefan-skliarovv1.p.rapidapi.com/searchEvents"

payload = "apiKey=%3CREQUIRED%3E"
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'x-rapidapi-host': "Ticketmasterstefan-skliarovV1.p.rapidapi.com",
    'x-rapidapi-key': "SIGN-UP-FOR-KEY"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)