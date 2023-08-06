from urllib.request import urlopen
import json


def sendMessage(username, room, content):
	url = "https://blabbr.xyz/api/send?username="+username+"&room="+room+"&msg="+content;
	page = urlopen(url)
  
def getroomusers(room):
	url2 = "https://blabbr.xyz/api/get/users?room="+room
	page = urlopen(url2)
	html_bytes = page.read()
	html = html_bytes.decode("utf-8")
	jsonn = json.loads(html)
	users = []
	for user in jsonn:
	  users.append(user['username'])
	return users
