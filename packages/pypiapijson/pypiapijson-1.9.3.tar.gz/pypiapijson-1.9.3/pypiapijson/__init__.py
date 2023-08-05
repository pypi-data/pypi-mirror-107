class CannotFindPackage(Exception):
	pass
class CannotFindPackagewithVersionProvided(Exception):
	pass
import requests,aiohttp
def get(name):
      try:
      	r = requests.get(f"https://pypi.org/pypi/{name}/json")
      except Exception:
      	raise CannotFindPackage("Error occured!\nI can\'t get the package info maybe check your typo or check your connection if you check it was all right, pypi api may gone maintenance.")
      if r.status_code != 200:
             raise CannotFindPackage("Error occured!\nI can\'t get the package info maybe check your typo or check your connection if you check it was all right, pypi api may gone maintenance.")
             
      else:
             js = r.json()
             return js
def getbyv(name,ver:str):
      try:
      	r = requests.get(f"https://pypi.org/pypi/{name}/{ver}/json")
      except Exception:
      	raise CannotFindPackagewithVersionProvided("Error occured!\nI can\'t get the package info with provided version maybe check your typo or check your connection if you check it was all right, pypi api may gone maintenance.")
      if r.status_code != 200:
             raise CannotFindPackagewithVersionProvided("Error occured!\nI can\'t get the package info with provided version maybe check your typo or check your connection if you check it was all right, pypi api may gone maintenance.")
            
             
      else:
             return r.json()

async def status():
             h = {"Accept" : "application/json","Content-type":"application/json"}
             async with aiohttp.ClientSession(headers=h) as s:
                   async with s.get("https://pypi.org/stats") as data:
                         if data.status == 200:
                               return await data.json()
                         else:
                               
                               print("Error!")
def helpme():
	print("Hello!\nUsage:\nget(packagename : string)\nGet information the paclage name that you provided and get the information in lastest version if there\'s no package it\'ll return none and raise error\ngetbyv(packagename : string,version : float or string) Do everything like get but you\'ll need to specify version the package have if there\'s wrong return None and raise error\nstatus()This will retrieve what package take most space and this fucntion is asynchronous function so run it with asyncio or await it.")
print("Hello! Want to get help what available function? execute helpme()\n:D")
