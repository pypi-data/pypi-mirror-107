import requests,urllib,json
from uuid import UUID
from os import urandom
from binascii import hexlify
from hashlib import sha1
import base64
import string
import random
def device():
	S=1000
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))  
	m='01' + (hardwareInfo := sha1(ran.encode("utf-8"))).hexdigest() + sha1(bytes.fromhex('01') + hardwareInfo.digest() + base64.b64decode("6a8tf0Meh6T4x7b0XvwEt+Xw6k8=")).hexdigest()
	return m
class Client():
	def __init__(self , deviceId , email , password):
		self.device=deviceId
		self.head=json.loads(requests.post(headers={"NDCDEVICEID":deviceId},data=json.dumps({"email":email,"v":2,"secret":"0 "+password,"deviceID":deviceId,"clientType":100,"action":"normal","timestamp":1617132227557}),url='https://service.narvii.com/api/v1/g/s/auth/login').text)
		self.sid=self.head["sid"]
		self.profile=self.head["auid"]
class SubClient():
	def __init__(self , link , headers,deviceId,profile):
		self.api="https://service.narvii.com/api/v1/"
		self.headers={"NDCDEVICEID":deviceId,"NDCAUTH":"sid="+headers}
		self.comId=json.loads(requests.get(headers=self.headers,url='https://service.narvii.com/api/v1/g/s/link-resolution?q='+link).text)["linkInfoV2"]["path"]
		self.comId=self.comId[0:self.comId.index('/')]
		self.objectId=json.loads(requests.get(headers=self.headers,url='https://service.narvii.com/api/v1/g/s/link-resolution?q='+link).text)["linkInfoV2"]["extensions"]["linkInfo"]["objectId"]
		self.profile=profile
		option=open("/sdcard/Android/data/dddddd.txt","w").write(self.comId+'\n'+self.api)
	def send_message(self , chatId , message, messageType:int=0,embedLink=None,embedTitle=None,embedContent=None,embedImage=None):
		data=json.dumps({"type": messageType,"content": message,"attachedObject": {"link": embedLink,"title": embedTitle,"content": embedContent,"mediaList":embedImage}})
		r=requests.post(headers=self.headers,data=data,url=self.api+self.comId+'/s/chat/thread/'+chatId+'/message')
		if r.status_code!=200:print(r.text)
	class get_blog_info():
		def __init__(self , blogId,headers):
			self.comId=open("/sdcard/Android/data/dddddd.txt").read().split()[0]
			self.api=open("/sdcard/Android/data/dddddd.txt").read().split()[1]
			self.title=json.loads(requests.get(headers=headers,url=self.api+self.comId+'/s/blog/'+blogId).text)["blog"]["title"]
			self.content=json.loads(requests.get(headers=headers,url=self.api+self.comId+'/s/blog/'+blogId).text)["blog"]["content"]
			self.blogId=json.loads(requests.get(headers=headers,url=self.api+self.comId+'/s/blog/'+blogId).text)["blog"]["blogId"]
			self.authoricon=json.loads(requests.get(headers=headers,url=self.api+self.comId+'/s/blog/'+blogId).text)["blog"]["author"]["icon"]
			self.nickname=json.loads(requests.get(headers=headers,url=self.api+self.comId+'/s/blog/'+blogId).text)["blog"]["author"]["nickname"]
			self.uid=json.loads(requests.get(headers=headers,url=self.api+self.comId+'/s/blog/'+blogId).text)["blog"]["author"]["uid"]
			try:
				self.icon=json.loads(requests.get(headers=headers,url=self.api+self.comId+'/s/blog/'+blogId).text)["blog"]["icon"]
			except:
				pass
	def post_blog(self , title , content , background_color=None,background=None):
		data=json.dumps({
  "extensions": {
    "fansOnly": False,
    "style": {
      "backgroundColor": background_color,
      "backgroundMediaList": background
    }
  },
  "content": content,
  "title":title
})
		r=requests.post(headers=self.headers,data=data,url=f"https://service.narvii.com/api/v1/{self.comId}/s/blog")
		if r.status_code!=200:print(r.text)
	def delete_blog(self , blogId=None,wikiId=None):
		if blogId is not None:
			r=requests.delete(headers=self.headers,url=self.api+self.comId+'/s/blog/'+blogId)
			if r.status_code!=200 : print(r.text)
		if wikiId is not None:
			r=requests.delete(headers=self.headers,url=self.api+self.comId+'/s/item/'+wikiId)
			if r.status_code!=200 : print(r.text)
	def uids(self , start=0 , size=25):
		r=json.loads(requests.get(headers=self.headers,url=self.api+self.comId+'/s/user-profile/'+'?type=recent&'+'start='+str(start)+'&size='+str(size)).text)
		r=r["userProfileList"][start]["uid"]
		return r
	def follow(self , userId):
		r=requests.post(headers=self.headers,url=f"https://service.narvii.com/api/v1/{self.comId}/s/user-profile/{userId}/member")
		if r.status_code!=200 : print(r.text)
	def comment(self , content,blogId=None,userId=None):
		if blogId is not None:
			r=requests.post(headers=self.headers,data=json.dumps({"content":content}),url=f"{self.api}{self.comId}/s/blog/{blogId}/comment")
			if r.status_code!=200:print(r.text)
		if userId is not None:
			r=requests.post(headers=self.headers,data=json.dumps({"content":content}),url=f"{self.api}{self.comId}/s/user-profile/{userId}/comment")
			if r.status_code!=200:print(r.text)
	def check_in(self):
		r=requests.post(headers=self.headers,data=json.dumps({"timezone":180}),url=f"{self.api}{self.comId}/s/check-in")
		if r.status_code!=200:print(r.text)
	def join_community(self):
		r=requests.post(headers=self.headers,url=f"{self.api}{self.comId}/s/community/join")
		if r.status_code!=200:print(r.text)
	def invite_chat(self , chatId , userId):
		r=requests.post(headers=self.headers,url=f"{self.api}{self.comId}/s/chat/thread/{chatId}/member/{userId}")
		if r.status_code!=200:print(r.text)
	def join_chat(self , chatId):
		r=requests.post(headers=self.headers,url=f"{self.api}{self.comId}/s/chat/thread/{chatId}/member/{self.profile}")
		if r.status_code!=200:print(r.text)
	def kick(self , chatId , userId):
		r=requests.delete(headers=self.headers,url=f"{self.api}{self.comId}/s/chat/thread/{chatId}/member/{userId}")
		if r.status_code!=200:print(r.text)
	def leave_chat(self , chatId):
		r=requests.delete(headers=self.headers,url=f"{self.api}{self.comId}/s/chat/thread/{chatId}/member/{self.profile}")
		if r.status_code!=200:print(r.text)
	def online_uids(self , start=0,size=1):
		list=[]
		r=requests.get(headers=self.headers,url=f"https://service.narvii.com/api/v1/{self.comId}/s/live-layer?topic=ndtopic%3A{self.comId}%3Aonline-members&start={start}&size={size}").text
		r=json.loads(r)
		r= r["userProfileList"][start]["uid"]
		return r
	def get_chat_messageIdcon(self , start , size,chatId):
		r=requests.get(headers=self.headers,url=f"{self.api}{self.comId}/s/chat/thread/{chatId}/message")
		if r.status_code!=200:print(r.text)
		else:
			r1=json.loads(r.text)["messageList"][start]["content"]
			r2=json.loads(r.text)["messageList"][start]["messageId"]
			list=[r1,r2]
			return list
	def edit_profile(self , name=None , content=None , background_color=None , icon=None , file=None):
		data=json.dumps({
  "extensions": {
    "style": {
      "backgroundColor": background_color,
      "backgroundMediaList": None
    },
    "coverAnimation": None
  },
  "address": None,
  "content": content,
  "icon": icon,
  "latitude": 0,
  "longitude": 0,
  "mediaList": [
    [
      100,
      file,
      None,
      None,
      None,
      {
        "fileName": None
      }
    ]
  ],
  "nickname": name,
  "timestamp": 1621594695658
})
		r=requests.post(headers=self.headers,data=data,url=f"https://service.narvii.com/api/v1/{self.comId}/s/user-profile/{self.profile}")
		if r.status_code!=200:print(r.text)
	def send_coins(self , chatId=None,blogId=None,coins=None,transactionId=None):
		data=json.dumps({
  "coins": coins,
  "tippingContext": {
    "transactionId": transactionId
  },
  "timestamp": 1621595873333})
		if transactionId is None: transactionId = str(UUID(hexlify(urandom(16)).decode('ascii')))
		if chatId is not None:
			r=requests.post(headers=self.headers,data=data,url=f"https://service.narvii.com/api/v1/{self.comId}/s/chat/thread/{chatId}/tipping")
			if r.status_code!=200:print(r.text)
		if blogId is not None:
			r=requests.post(headers=self.headers,data=data,url=f"https://service.narvii.com/api/v1/{self.comId}/s/blog/{blogId}/tipping")
			if r.status_code!=200:print(r.text)
	def download_photo(self , url,name):
		urllib.request.urlretrieve(url , name)
	class wallet_info():
		def __init__(self , headers):
			r=requests.get(headers=headers,url="https://service.narvii.com/api/v1/g/s/wallet?timezone=180")
			if r.status_code!=200:print(r.text)
			else:
				self.totalCoinsFloat=json.loads(r.text)["wallet"]["totalCoinsFloat"]
				self.adsEnabled=json.loads(r.text)["wallet"]["adsEnabled"]
	def edit_chat(self,chatId,name=None,content=None,icon=None):
		r=requests.post(headers=self.headers,data=json.dumps({ "title":name,"content":content,"icon":icon }),url=f"{self.api}{self.comId}/s/chat/thread/{chatId}")
		if r.status_code!=200:print(r.text)
	def coHosts(self , chatId):
		r=requests.get(headers=self.headers,url=f"{self.api}{self.comId}/s/chat/thread/{chatId}")
		if r.status_code!=200:print(r.text)
		else: return json.loads(r.text)["thread"]["extensions"]["coHost"]