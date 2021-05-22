#TO DO (erase if done) -> anytime message == 0, go to home, if 'error', display popup
import requests
from tkinter import *
from functools import partial
import time
import datetime
from multiprocessing import Process
import random
from tkinter import scrolledtext as st
import threading
#import client
#############GLOBAL VARS
playerName = ""
lobbyCode = ""
playerId = ""
inLobby = False
inGame = False
#game info
role = ""
subrole = ""
location = ""
playerOrder = []
playerNum = 0
lobbyChat = []
gameChat = []
otherPlayers = []
playerTurn = False


window = Tk()
window.title("Spy Among Us")
window.geometry("500x600")
window.resizable(0,0)
#############CLIENT
def host():
        res = requests.post('https://calm-river-76254.herokuapp.com/message', data={'message': 1, 'id': playerName})
        res.raise_for_status()
        servermsg = res.json()
        return servermsg

def join():
		global playerName
		global lobbyCode
		print(lobbyCode)
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 2, "id":playerName, "arg1": lobbyCode})
		res.raise_for_status()
		servermsg = res.json()
		return servermsg

def exit():
		global lobbyCode
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 3, "id": playerId})
		#res.raise_for_status()
		#servermsg = res.json()
		#print(servermsg)
		#return servermsg

def start():
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 5, "id": playerId})
		#res.raise_for_status()
		#servermsg = res.json()
		#return servermsg

def status_check():
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 4, "id": playerId})
		res.raise_for_status()
		servermsg = res.json()
		print(servermsg)
		return servermsg

def get_role_and_location():
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 6, "id": playerId})
		res.raise_for_status()
		servermsg = res.json()
		print(servermsg)
		return servermsg	

def send_chat_to_server(chatMsg): #lobby chat and answering questions in game
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 7, "id": playerId, "arg1":chatMsg})
		res.raise_for_status()
		servermsg = res.json()
		print(servermsg)
		return servermsg

def send_question_to_server(chatMsg,target): #lobby chat and answering questions in game
		print("\n")
		print("send game chat...")
		print("targetID "+target)
		print("\n")
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 8, "id":playerId,"arg1": chatMsg, "arg2":target})
		res.raise_for_status()
		servermsg = res.json()
		print(servermsg)
		return servermsg	
##############GUI
##auxiliary functions for GUI
def get_plist_as_string(players):
	plist = ""
	for p in players:
		if plist != "":
			plist = plist + ", "+p[5:]
		else:
			plist = plist + p[5:]
	return plist

def extract_order_of_player(plist_and_order):
	plist = plist_and_order["pList"]
	pOrder = plist_and_order["pOrder"]
	orderedList = []
	for i in range(1,9):
		#get index in pOrder of i
		if i not in pOrder:
			break
		idx = pOrder.index(i)
		#add plist[idx] to orderedList
		orderedList.append(plist[idx])
	return orderedList

def update_lobby_chat(chatQueue):
	global lobbyChat
	for q in chatQueue:
		if q not in lobbyChat:
			chatScrolledTxt.config(state="normal")
			p = q["id"]
			text = p[5:]+": "+q["message"]+"\n"
			chatScrolledTxt.insert(END,text)
			chatScrolledTxt.config(state="disabled")
			lobbyChat.append(q)

def update_game_chat(chatQueue):
	global gameChat
	for q in chatQueue:
		if q not in gameChat and q not in lobbyChat:
			chatlog.config(state="normal")
			p = q["id"]
			text = p[5:]+": "+q["message"]+"\n"
			chatlog.insert(END,text)
			chatlog.config(state="disabled")
			gameChat.append(q)

def get_plist_minus_self():
	global playerOrder
	plist = []
	for i in playerOrder:
		plist.append(i[5:])
	plist.remove(playerId[5:])
	return plist

def add_player_droplist_to_gameproperFr():
	playerList = get_plist_minus_self()
	playerDropList=OptionMenu(gameproperFr,target,*playerList)
	playerDropList.config(width=40)
	target.set(playerList[0]) 
	playerDropList.place(x=200,y=450)
##end of auxiliary functions
def startLogger():
	while True:
		update()
		time.sleep(3)
def update():
	global inLobby
	global inGame
	if inLobby == True:
		servermsg = status_check()
		if servermsg["arg1"] == 1:
			global lobbyChat
			plist = get_plist_as_string(servermsg["arg2"])
			playersInLobbyLbl.config(text=plist+" is/are here.")
			#update chatlog
			update_lobby_chat(servermsg["arg3"])
			if servermsg["isHost"] == 1:
				exitBtn.place_forget()
				startGameBtn.place_forget()	
				exitBtn.place(x=180,y=500)
				startGameBtn.place(x=250,y=500)
			else:
				exitBtn.place_forget()
				startGameBtn.place_forget()	
				exitBtn.place(x=200,y=500)		
		elif servermsg["arg1"] == 2:
			inLobby = False
			inGame = True
			servermsg2 = get_role_and_location()
			#arg1 = 1 or 0 (role)
			global role
			global subrole
			global location
			global playerOrder
			global playerNum
			playerNum = servermsg2["arg4"]
			playerOrder = extract_order_of_player(servermsg2["arg5"])
			location = servermsg2["arg2"]
			if servermsg2["arg1"] == 1:
				#1 is spy
				role = "spy"
				#displayPopUp("You are the spy!\nYou cannot see the location. :(\nYour goal is to guess the location\nwithout revealing that you are the spy.")
				goalLbl.config(text="Your goal is to guess the location\nwithout revealing that you are the spy.")
				locationLbl.config(text="You cannot see the location.")
				#locationLbl2.config(text="You cannot see the location.")
				playerAndGameInfoLbl.config(text="ROLE: Spy || SUBROLE: --|| LOCATION: --")
				roleLbl.config(text="You are the spy!",fg="white",bg="red")
			else:
				role = "innocent"
				subrole = servermsg2["arg3"]
				#displayPopUp("You are an innocent.\nYou are a/an "+subrole+" in a/an "+location+".\nYour goal is to guess the spy\nwithout revealing the location.")
				locationLbl.config(text="You are in a/an "+location+".")
				#locationLbl2.config(text="You are in a/an "+location+".")
				playerAndGameInfoLbl.config(text="ROLE: Innocent || SUBROLE: "+subrole+" || LOCATION: "+location)
				roleLbl.config(text="You are an innocent.",bg="white")
				subroleLbl.config(text="You are a/an/the "+subrole+".")
				#subroleLbl2.config(text="You are a/an/the "+subrole+".")
			add_player_droplist_to_gameproperFr()
			ordered_plist_as_string = get_plist_as_string(playerOrder)
			orderOfPlayersLbl.config(text="Below is the order of players to ask:\n"+ordered_plist_as_string)
			orderOfPlayersLbl2.config(text="Below is the order of players to ask:\n"+ordered_plist_as_string)
			playerNoLbl.config(text="You are player no. "+str(playerNum)+".")
			playerNoLbl2.config(text="You are player no. "+str(playerNum)+".")
			startGameFr.tkraise()
		elif servermsg["arg1"] == 3:
			#startGameBtn.config(state = "disabled")
			loadingFr.tkraise()
	elif inGame == True:
		servermsg = status_check()
		#update chat
		update_game_chat(servermsg["arg3"])
		#playerDropList.place_forget()
		turnLabel.config(text="")
		sendBtn2.config(state="disabled")
		#if player's turn to ask,display pop up
		if servermsg["arg4"]==1:
			turnLabel.config(text="It's your turn to ask.")
			#add_player_droplist_to_gameproperFr()
			sendBtn2.config(state="normal")
			global playerTurn
			playerTurn = True
		#	displayPopUp("Your turn to ask.")
		#if player is being asked,display popup
		elif servermsg["arg4"]==2:
			turnLabel.config(text="You are being asked!")
			sendBtn2.config(state="normal")
		#	displayPopUp("You are being asked!")
		
	#window.after(3000,update)

def displayPopUp(message):
	popUp = Tk()
	popUp.geometry("300x150")
	popUp.resizable(0,0)
	messageLabel = Label(popUp,text=message).pack()
	okBtn = Button(popUp,text="OK!",command=popUp.destroy).pack()

def onClickCreateLobby():
	global playerName 
	playerName = playerNameEntry.get()
	if playerName != "":
		servermsg = host()
		if servermsg["message"] == 1:
				displayPopUp("Succesfully created lobby!")
				global lobbyCode
				global playerId
				playerId = servermsg["id"]
				lobbyCode = servermsg["rid"]
				lobbyCodeLbl.config(text="Lobby code "+lobbyCode)								
				exitBtn.place_forget()
				startGameBtn.place_forget()	
				exitBtn.place(x=180,y=500)
				startGameBtn.place(x=250,y=500)
				global inLobby
				inLobby = True
				#update()
				threading.Thread(target=startLogger).start()
				lobbyFr.tkraise()
		else:
			displayPopUp("Failed to create lobby.")
	else:
		displayPopUp("Please enter player name.\n")

def onClickJoinLobby():
	global playerName 
	playerName = playerNameEntry.get()
	if playerName != "":
		exitBtn.place_forget()
		startGameBtn.place_forget()	
		exitBtn.place(x=200,y=500)
		askLobbyCodeFr.tkraise()
	else:
		displayPopUp("Please enter player name.\n")

def onClickEnterLobbyCode():
	global lobbyCode
	lobbyCode = lobbyCodeEntry.get()
	servermsg = join()
	if servermsg["message"] == 1:
		displayPopUp("Successfully joined lobby!")
		lobbyCodeLbl.config(text="Lobby code "+lobbyCode)
		global playerId
		playerId = servermsg["id"]
		global inLobby
		inLobby = True
		lobbyFr.tkraise()
		#status_check()
		#update()
		threading.Thread(target=startLogger).start()
	else:
		displayPopUp("Failed to join lobby. Please check lobby code.")

def onClickExit():
	#reset global vars
	exit()
	#NOTE: For now, ignore arg1, always exit
	#if servermsg["arg1"] == "ok":
	global playerName
	global lobbyCode
	global playerId
	global inLobby
	global inGame
	global role
	global subrole
	global location
	global playerOrder
	global playerNum
	global lobbyChat
	global gameChat
	global playerTurn
	playerName = ""
	lobbyCode = ""
	playerId = ""
	inLobby = False
	inGame = False
	role = ""
	subrole = ""
	location = ""
	playerOrder = []
	playerNum = 0
	lobbyChat = []
	gameChat = []
	playerTurn = False
	displayPopUp("Successfully exited lobby!")
	chatScrolledTxt.config(state="normal")
	chatlog.config(state="normal")
	chatScrolledTxt.delete(1.0,END)
	chatlog.delete(1.0,END)
	chatScrolledTxt.config(state="disabled")
	chatlog.config(state="disabled")

	hostOrJoinLobbyFr.tkraise()
	#else:
		#displayPopUp("Failed to exit lobby.")

def onClickStartGame():
	#startGameFr.tkraise()
	msg = status_check()
	playerlist = str(msg["arg2"])
	num = playerlist.count(',') + 1
	if (num < 3):
		displayPopUp("At least 3 people are needed\nbefore you can start the game.")
		return
	loadingFr.tkraise()
	start()

def onClickGotIt():
	gameproperFr.tkraise()

def onClickSend1():
	chatMsg = msgTxtBox.get("1.0","end")
	msgTxtBox.delete("1.0", END)
	servermsg = send_chat_to_server(chatMsg)

def onClickSend2():
	global playerTurn
	chatMsg = chatcontent.get("1.0","end")
	targetPlayer = target.get()
	chatcontent.delete("1.0", END)
	if playerTurn == True:
		sendBtn2.config(state="disabled")
		servermsg2 = send_question_to_server(chatMsg,playerId[0:5]+targetPlayer)
		turnLabel.config(text="")
		playerTurn = False

	else:
		sendBtn2.config(state="disabled")
		servermsg = send_chat_to_server(chatMsg)
		turnLabel.config(text="")


###############frames
loadingFr = Frame(window)
loadingFr.place(x=0,y=0,height=600,width=500)

startGameFr = Frame(window)
startGameFr.place(x=0,y=0,height=600,width=500)

lobbyFr = Frame(window)
lobbyFr.place(x=0,y=0,height=600,width=500)

gameproperFr = Frame(window)
gameproperFr.place(x=0,y=0,height=600,width=500)

askLobbyCodeFr = Frame(window)
askLobbyCodeFr.place(x=0,y=0,height=600,width=500)

hostOrJoinLobbyFr = Frame(window)
hostOrJoinLobbyFr.place(x=0,y=0,height=600,width=500)

###############hostOrJoinLobbyFrame
gameNameLbl = Label(hostOrJoinLobbyFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

inputPlayerNameLbl = Label(hostOrJoinLobbyFr,text="Player Name:",font=("bold",10),fg="black",width=25,padx=10,pady=10).place(x=40,y=140)
playerNameEntry = Entry(hostOrJoinLobbyFr)
playerNameEntry.place(x=200,y=150)


createLobbyBtn = Button(hostOrJoinLobbyFr,relief="solid",text="Create lobby",fg="white",bg="black",command=onClickCreateLobby).place(x=170,y=220)
joinLobbyBtn = Button(hostOrJoinLobbyFr,relief="solid",text="Join lobby",fg="white",bg="black",command=onClickJoinLobby).place(x=270,y=220)
###############askLobbyCodeFr
gameNameLbl2 = Label(askLobbyCodeFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

inputLobbyCodeLbl = Label(askLobbyCodeFr,text="Lobby Code:",font=("bold",10),fg="black",width=25,padx=10,pady=10).place(x=40,y=140)
lobbyCodeEntry = Entry(askLobbyCodeFr)
lobbyCodeEntry.place(x=200,y=150)

enterLobbyCodeBtn = Button(askLobbyCodeFr,relief="solid",text="Enter lobby code",fg="white",bg="black",command=onClickEnterLobbyCode).place(x=220,y=220)
###############lobbyFr
#lobbyCode = "-----"
gameNameLbl3 = Label(lobbyFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

lobbyCodeLbl = Label(lobbyFr,text="Lobby code "+lobbyCode)
lobbyCodeLbl.place(x=200,y=120)

playersInLobbyLbl = Label(lobbyFr,text="",width=75,justify="center",fg="white",bg="#808080")
playersInLobbyLbl.place(x=0,y=140)

chatScrolledTxt =  st.ScrolledText(lobbyFr,width=50,height=10,font=("Arial",9))
chatScrolledTxt.place(x=20, y=190)
chatScrolledTxt.configure(state="disabled")

msgTxtBox = Text(lobbyFr,width=42,height=2)
msgTxtBox.place(x=20,y=400)

sendBtn = Button(lobbyFr,relief="solid",text="Send",fg="white",bg="black",width=10,command=onClickSend1)
sendBtn.place(x=392,y=400)

exitBtn = Button(lobbyFr,relief="solid",text="Exit",fg="white",bg="black",command=onClickExit)
startGameBtn = Button(lobbyFr,relief="solid",text="Start game",fg="white",bg="black",command=onClickStartGame)

exitBtn.place(x=180,y=500)
startGameBtn.place(x=250,y=500)
###############startGameFr
gameNameLbl4 = Label(startGameFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

roleLbl = Label(startGameFr,text="Display role here",font=("bold",10),fg="black",width=22,pady=5)
roleLbl.place(x=175,y=150)

goalLbl = Label(startGameFr,text="Your goal is to guess the spy\nwithout revealing the location.",font=("bold",10),width=60,justify="center")
goalLbl.place(x=0,y=200)

locationLbl = Label(startGameFr,text = "Display location here",font=("bold",10))
locationLbl.place(x=175,y=250)

subroleLbl = Label(startGameFr,text="",font=("bold",10),fg="black")
subroleLbl.place(x=175,y=300)

orderOfPlayersLbl = Label(startGameFr,text="",font=("bold",10),width=60,justify="center")
orderOfPlayersLbl.place(x=0,y=350)

playerNoLbl = Label(startGameFr,text="Display player no.",font=("bold",10),fg="black")
playerNoLbl.place(x=175,y=400)


#ok button
gotItBtn = Button(startGameFr,relief="solid",text="Got it!",fg="white",bg="black",command=onClickGotIt)
gotItBtn.place(x=200,y=500)
###############gameproperFr
gameNameLbl4 = Label(gameproperFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

turnLabel = Label(gameproperFr,text="",width=75,justify="center")
turnLabel.place(x=0,y=120)

playerAndGameInfoLbl = Label(gameproperFr,text="",width=75,justify="center",fg="white",bg="#808080")
playerAndGameInfoLbl.place(x=0,y=140)


chatlog =  st.ScrolledText(gameproperFr,width=50,height=10,font=("Arial",9))
chatlog.place(x=20, y=190)
chatlog.configure(state="disabled")

chatcontent = Text(gameproperFr,width=42,height=2)
chatcontent.place(x=20,y=400)

sendBtn2 = Button(gameproperFr,state="disabled",relief="solid",text="Send",fg="white",bg="black",width=10, command=onClickSend2)
sendBtn2.place(x=392,y=400)

playerDropListLbl = Label(gameproperFr,text="Who to ask (if your turn):",width=30,justify="center",font=("bold",9),bg="black",fg="white")
playerDropListLbl.place(x=1,y=453)
#playerList = [""]
#c=StringVar()
target = StringVar()
#playerDropList=OptionMenu(gameproperFr,c,*playerList)
#playerDropList.config(width=40)
#c.set('choose who to ask')
target.set("++++")
#playerDropList.place(x=200,y=450)
#locationLbl2 = Label(gameproperFr,text = locationLbl.cget("text"),font=("bold",10))
#locationLbl2.place(x=175,y=500)


#subroleLbl2 = Label(gameproperFr,text="",font=("bold",10),fg="black")
#subroleLbl2.place(x=175,y=520)

orderOfPlayersLbl2 = Label(gameproperFr,text="",font=("bold",10),width=60,justify="center")
orderOfPlayersLbl2.place(x=0,y=500)


playerNoLbl2 = Label(gameproperFr,text="Display player no.",font=("bold",10),fg="black")
playerNoLbl2.place(x=175,y=540)



###############loadingFr
gameNameLbl5 = Label(loadingFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

loadingMessageLbl = Label(loadingFr,text="Please wait while server is busy. :) \n",font=("bold",12),fg="black")
loadingMessageLbl.place(x=100,y=220)

window.mainloop()


