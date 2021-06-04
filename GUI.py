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
voteChat = []
otherPlayers = []
playerTurn = False
informedThatVotingHasStarted = False
start_time = 0
locationList = []
sentLocationGuess = False
sentSpyGuess = False
startGuessLocation = False
startGameHasEnded = False



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


def start():
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 5, "id": playerId})
		res.raise_for_status()
		servermsg = res.json()
		return servermsg

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

def send_question_to_server(chatMsg,target): #for sending player question during game chat
		print("\n")
		print("send game chat...")
		print("targetID "+target)
		print("\n")
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 8, "id":playerId,"arg1": chatMsg, "arg2":target})
		res.raise_for_status()
		servermsg = res.json()
		print(servermsg)
		return servermsg

def send_vote_to_server(target):
		print("\n")
		print("sending vote...")
		print("targetID " + target)
		print("\n")
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 9, "id":playerId, "arg1": target})
		res.raise_for_status()
		servermsg = res.json()
		print(servermsg)
		return servermsg

def get_locations():
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 10})
		res.raise_for_status()
		servermsg = res.json()
		print(servermsg)
		return servermsg

def spy_guesses_location(loc):
		print("\n")
		print("sending location guess...")
		print("location " + loc)
		print("\n")
		res = requests.post('https://calm-river-76254.herokuapp.com/message', data={"message": 11, "id":playerId, "arg1": loc})
		res.raise_for_status()
		servermsg = res.json()
		print(servermsg)
		return servermsg


##############GUI
##auxiliary functions for GUI
def reset():
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
	global voteChat
	global playerTurn
	global informedThatVotingHasStarted
	global start_time
	global locationList
	global otherPlayers
	global sentLocationGuess
	global sentSpyGuess
	global startGuessLocation
	global startGameHasEnded
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
	voteChat = []
	locationList = []
	otherPlayers = []
	playerTurn = False
	informedThatVotingHasStarted = False
	start_time = 0
	sentLocationGuess = False
	sentSpyGuess = False
	startGuessLocation = False
	startGameHasEnded = False
	chatScrolledTxt.config(state="normal")
	chatlog.config(state="normal")
	votingChatLog.config(state="normal")
	chatScrolledTxt.delete(1.0,END)
	chatlog.delete(1.0,END)
	votingChatLog.delete(1.0,END)
	chatScrolledTxt.config(state="disabled")
	chatlog.config(state="disabled")
	votingChatLog.config(state="disabled")
	voteBtn.config(state="normal")
	voteBtn.place(x=200,y=450)
	guessLocationBtn.config(state="normal")
	#backToMainBtn.place_forget()


def error_exit(msg):
	displayMsgLbl.config(text = msg)
	reset()
	start = time.time()
	while time.time()-start <= 3:
		continue
	hostOrJoinLobbyFr.tkraise()

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
	global lobbyChat
	global gameChat
	for q in chatQueue:
		if q not in gameChat and q not in lobbyChat:
			chatlog.config(state="normal")
			p = q["id"]
			text = p[5:]+": "+q["message"]+"\n"
			chatlog.insert(END,text)
			chatlog.config(state="disabled")
			gameChat.append(q)

def update_voting_chat(chatQueue):
	global lobbyChat
	global gameChat
	global voteChat
	print("/n")
	print(gameChat)
	print("/n")
	for q in chatQueue:
		if q not in gameChat and q not in lobbyChat and q not in voteChat:
			votingChatLog.config(state="normal")
			p = q["id"]
			text = p[5:]+": "+q["message"]+"\n"
			votingChatLog.insert(END,text)
			votingChatLog.config(state="disabled")
			voteChat.append(q)

def get_plist_minus_self():
	global playerOrder
	plist = []
	for i in playerOrder:
		plist.append(i[5:])
	plist.remove(playerId[5:])
	return plist

def add_player_droplist_to_gameproperFr():
	global otherPlayers
	otherPlayers = get_plist_minus_self()
	playerDropList=OptionMenu(gameproperFr,target,*otherPlayers)
	playerDropList.config(width=40)
	target.set("Select player to ask") 
	playerDropList.place(x=200,y=450)

def add_spy_droplist_to_votingFr():
	global otherPlayers
	spyDropList=OptionMenu(votingFr,target2,*otherPlayers)
	spyDropList.config(width=20)
	target2.set(otherPlayers[0]) 
	spyDropList.place(x=12,y=450)

def add_location_droplist_to_votingFr():
	servermsg = get_locations()
	no_tries = 1
	while no_tries <= 3:
		if servermsg["message"] != 0:
			break
		servermsg = get_locations()
		no_tries = no_tries + 1
	if servermsg["message"]!= 0:
		global locationList
		locationList = servermsg["arg1"]
		locationDropList=OptionMenu(votingFr,target3,*locationList)
		locationDropList.config(width=20)
		target3.set(locationList[0]) 
		locationDropList.place(x=12,y=450)
	else:
		error_exit("Oops! Sorry, something went wrong. :(")

##end of auxiliary functions
def startLogger():
	while True:
		update()
		time.sleep(3)

def startTimer():
	while True:
		vote_timer()
		time.sleep(1)

def vote_timer():
	t = int(time.time()-start_time)
	seconds = t%60
	minutes = t//60
	timerLbl.config(text = str(minutes) + " mins. & "+str(seconds)+" secs. have passed.")

def update():
	global role
	global inLobby
	global inGame
	global start_time
	global sentSpyGuess
	global sentLocationGuess
	global startGuessLocation
	global startGameHasEnded
	global playerTurn
	if inLobby == True:
		servermsg = status_check()
		no_tries = 1
		while no_tries <= 3:
			if servermsg["message"] != 0:
				break
			servermsg = status_check()
			no_tries = no_tries + 1
		if servermsg["message"] == 0:
			print("\nERROR!!!\n")
			error_exit("Oops! Sorry, something went wrong. :(")
			return
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
			no_tries = 1
			while no_tries <= 3:
				if servermsg2["message"] != 0:
					break
				servermsg2 = get_role_and_location()
				no_tries = no_tries + 1
			if servermsg2["message"] == 0:
				error_exit("Oops! Sorry, something went wrong. :(")
				return
			#arg1 = 1 or 0 (role)
			#global role
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
				goalLbl.config(text="Your goal is to guess the location\nwithout revealing that you are the spy.")
				locationLbl.config(text="You cannot see the location.")
				playerAndGameInfoLbl.config(text="ROLE: Spy || SUBROLE: --|| LOCATION: --")
				roleLbl.config(text="You are the spy!",fg="white",bg="red")
				subroleLbl.config(text="")
			else:
				role = "innocent"
				subrole = servermsg2["arg3"]
				locationLbl.config(text="You are in a/an "+location+".")
				playerAndGameInfoLbl.config(text="ROLE: Innocent || SUBROLE: "+subrole+" || LOCATION: "+location)
				roleLbl.config(text="You are an innocent.",bg="white")
				subroleLbl.config(text="You are a/an/the "+subrole+".")
			add_player_droplist_to_gameproperFr()
			ordered_plist_as_string = get_plist_as_string(playerOrder)
			orderOfPlayersLbl.config(text="Below is the order of players to ask:\n"+ordered_plist_as_string)
			orderOfPlayersLbl2.config(text="Below is the order of players to ask:\n"+ordered_plist_as_string)
			playerNoLbl.config(text="You are player no. "+str(playerNum)+".")
			playerNoLbl2.config(text="You are player no. "+str(playerNum)+".")
			startGameFr.tkraise()
		elif servermsg["arg1"] == 3:
			loadingFr.tkraise()
	elif inGame == True:
		servermsg = status_check()
		no_tries = 1
		while no_tries <= 3:
			if servermsg["message"] != 0:
				break
			servermsg = status_check()
			no_tries = no_tries + 1
		if servermsg["message"] == 0:
			error_exit("Oops! Sorry, something went wrong. :(")
			return
		#update chat
		if servermsg["arg1"] == 4:
			global informedThatVotingHasStarted
			global start_time
			#backToMainBtn.place_forget()
			if informedThatVotingHasStarted == False:
				displayMsgLbl.config(text="Chat phase is over!\nYou are given around 3 minutes to guess the spy.\nYou may chat what with other players.")
				displayMsgFr.tkraise()
				start = time.time()
				while time.time()-start <= 5:
					continue
				informedThatVotingHasStarted = True
				start_time = time.time()
				add_spy_droplist_to_votingFr()
				gameResultLbl.config(text="Waiting for everyone to finish voting.")
				votingFr.tkraise()
			else:
				threading.Thread(target=startTimer).start()
				update_voting_chat(servermsg["arg3"])
				t = time.time() - start_time
				if t//60 >= 3 and sentSpyGuess == False:
					send_no_guess_msg = send_vote_to_server("")
					no_tries = 1
					while no_tries < 3:
						if send_no_guess_msg["message"] != 0:
							break
						no_tries = no_tries + 1
					if send_no_guess_msg["message"] == 0:
						error_exit("Oops! Sorry,something went wrong. :(")
						return 
					sentSpyGuess = True
					voteBtn.config(state="disabled")
		elif servermsg["arg1"] == 5:
			gameResultLbl.config(text="Spy has been voted.\nWaiting for spy to guess location.\nSpy is given around 1 min.\nOnly the spy's timer will restart.")
			update_voting_chat(servermsg["arg3"])
			if role == "spy":
				if startGuessLocation == False:
					spyDropList.place_forget()
					voteBtn.place_forget()
					add_location_droplist_to_votingFr()
					guessLocationBtn.place(x=200,y=450)
					start_time = time.time()
					startGuessLocation = True
				t = time.time() - start_time
				if t//60>=1 and sentLocationGuess == False:
					send_no_guess_msg = spy_guesses_location("")
					no_tries = 1
					while no_tries < 3:
						if send_no_guess_msg["message"] != 0:
							break
						no_tries = no_tries + 1
					if send_no_guess_msg["message"] == 0:
						error_exit("Oops! Sorry,something went wrong. :(")
						return 
					sentLocationGuess = True
					guessLocationBtn.config(state = "disabled")
		elif servermsg["arg1"] == 6:
			gameResultLbl.config(text="Spy wins!\nClick X to exit.\nElse, you will exit\nafter around 1 min.")
			#backToMainBtn.place(x=400,y=450)
			sendBtn3.config(state="disabled")
			if startGameHasEnded == False:
				start_time = time.time()
				startGameHasEnded = True
				return
			else:
				t = time.time()-start_time
				if t>=60:
					window.destroy()
					#reset()
					#hostOrJoinLobbyFr.tkraise()
				return
		elif servermsg["arg1"] == 7:
			gameResultLbl.config(text="Innocents win!\nClick X to exit.\nElse, you will exit\nafter around 1 min.")
			#backToMainBtn.place(x=400,y=450)
			sendBtn3.config(state="disabled")
			if startGameHasEnded == False:
				start_time = time.time()
				startGameHasEnded = True
				return
			else:
				t = time.time()-start_time
				if t>=60:
					window.destroy()
					#reset()
					#hostOrJoinLobbyFr.tkraise()
				return
		else:
			update_game_chat(servermsg["arg3"])
			turnLabel.config(text="")
			sendBtn2.config(state="disabled")
			#playerTurn = False
			if servermsg["arg4"]==1:
				turnLabel.config(text="It's your turn to ask.",fg="red")
				sendBtn2.config(state="normal")
				#global playerTurn
				playerTurn = True
			elif servermsg["arg4"]==2:
				turnLabel.config(text="You are being asked!",fg="red")
				sendBtn2.config(state="normal")
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
		no_tries = 1
		while no_tries <= 3:
			if servermsg["message"] != 0:
				break
			servermsg = host()
			no_tries = no_tries + 1
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
			error_exit("Failed to create lobby.")
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
	reset()
	displayPopUp("Successfully exited lobby!")
	hostOrJoinLobbyFr.tkraise()

def onClickStartGame():
	msg = status_check()
	no_tries = 1
	while no_tries <= 3:
		if msg["message"] != 0:
			break
		msg = status_check()
		no_tries = no_tries + 1
	if msg["message"] == 0:
		error_exit("Oops! Sorry, something went wrong. :(")
		return
	playerlist = str(msg["arg2"])
	num = playerlist.count(',') + 1
	if (num < 3):
		displayPopUp("At least 3 people are needed\nbefore you can start the game.")
		return
	loadingFr.tkraise()
	#start()
	servermsg = start()
	no_tries = 1
	while no_tries <= 3:
		if servermsg["message"] != 0:
			break
		servermsg = start()
		no_tries = no_tries + 1
	if servermsg["message"] == 0:
		error_exit("Oops! Sorry, something went wrong. :(")


def onClickGotIt():
	gameproperFr.tkraise()

def onClickSend1():
	chatMsg = msgTxtBox.get("1.0","end")
	msgTxtBox.delete("1.0", END)
	servermsg = send_chat_to_server(chatMsg)
	no_tries = 1
	while no_tries <= 3:
		if servermsg["message"] != 0:
			break
		servermsg = send_chat_to_server(chatMsg)
		no_tries = no_tries + 1
	if servermsg["message"] == 0:
		error_exit("Oops! Sorry, something went wrong. :(")

def onClickSend2():
	global playerTurn
	chatMsg = chatcontent.get("1.0","end")
	targetPlayer = target.get()
	chatcontent.delete("1.0", END)
	target.set("Select player to ask")
	status = status_check()
	no_tries = 1
	while no_tries <= 3:
		if status["message"] != 0:
			break
		no_tries = no_tries + 1
	if status["message"] == 0:
		error_exit("Oops! Sorry,something went wrong. :(")
		return
	#if playerTurn == True:
	if status["arg4"] == 1:
		if targetPlayer == "Select player to ask":
			displayPopUp("Please select player to ask")
			return
		sendBtn2.config(state="disabled")
		servermsg2 = send_question_to_server(chatMsg,playerId[0:5]+targetPlayer)
		no_tries = 1
		while no_tries <= 3:
			if servermsg2["message"] != 0:
				break
			servermsg2 = send_question_to_server(chatMsg,playerId[0:5]+targetPlayer) 
			no_tries = no_tries + 1
		if servermsg2["message"] == 0:
			error_exit("Oops! Sorry, something went wrong. :(")
			return
		turnLabel.config(text="")
		playerTurn = False

	elif status["arg4"] == 2:
		sendBtn2.config(state="disabled")
		servermsg = send_chat_to_server(chatMsg)
		no_tries = 1
		while no_tries <= 3:
			if servermsg["message"] != 0:
				break
			servermsg = send_chat_to_server(chatMsg)
			no_tries = no_tries + 1
		if servermsg["message"] == 0:
			error_exit("Oops! Sorry, something went wrong. :(")
			return
		turnLabel.config(text="")

def onClickSend3():
	chatMsg = voteChatText.get("1.0","end")
	voteChatText.delete("1.0", END)
	servermsg = send_chat_to_server(chatMsg)
	no_tries = 1
	while no_tries <= 3:
		if servermsg["message"] != 0:
			break
		servermsg = send_chat_to_server(chatMsg)
		no_tries = no_tries + 1
	if servermsg["message"] == 0:
		error_exit("Oops! Sorry, something went wrong. :(")

def onClickVote():
	voteBtn.config(state="disabled")
	spyGuess = target2.get()
	servermsg = send_vote_to_server(playerId[0:5]+spyGuess)
	no_tries = 1
	while no_tries <= 3:
		if servermsg["message"] != 0:
			return
		servermsg = send_vote_to_server(playerId[0:5]+spyGuess)
		no_tries = no_tries + 1
	if servermsg["message"] == 0:
		error_exit("Oops! Sorry, something went wrong. :(")
	else:
		sentSpyGuess = True


def onClickGuessLocation():
	guessLocationBtn.config(state="disabled")
	locationGuess = target3.get()
	servermsg = spy_guesses_location(locationGuess)
	no_tries = 1
	while no_tries <= 3:
		if servermsg["message"] != 0:
			return
		servermsg = spy_guesses_location(locationGuess)
		no_tries = no_tries + 1
	if servermsg["message"] == 0:
		error_exit("Oops! Sorry, something went wrong. :(")
	else:
		sentLocationGuess = True

#def onClickBackToMain():
#	hostOrJoinLobbyFr.tkraise()
#	reset()
###############frames
displayMsgFr = Frame(window)
displayMsgFr.place(x=0,y=0,height=600,width=500)

votingFr = Frame(window)
votingFr.place(x=0,y=0,height=600,width=500)

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

locationLbl = Label(startGameFr,text = "Display location here",font=("bold",10),fg="red")
locationLbl.place(x=175,y=250)

subroleLbl = Label(startGameFr,text="",font=("bold",10),fg="black")
subroleLbl.place(x=175,y=300)

orderOfPlayersLbl = Label(startGameFr,text="",font=("bold",10),width=60,justify="center")
orderOfPlayersLbl.place(x=0,y=350)

playerNoLbl = Label(startGameFr,text="Display player no.",font=("bold",10),fg="black")
playerNoLbl.place(x=175,y=400)

gotItBtn = Button(startGameFr,relief="solid",text="Got it!",fg="white",bg="black",command=onClickGotIt)
gotItBtn.place(x=200,y=500)
###############gameproperFr
gameNameLbl4 = Label(gameproperFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

turnLabel = Label(gameproperFr,text="",width=55,justify="center",font=("bold",12))
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


target = StringVar()
target.set("++++")

p = [""]
playerDropList=OptionMenu(gameproperFr,target,*p)


orderOfPlayersLbl2 = Label(gameproperFr,text="",font=("bold",10),width=60,justify="center")
orderOfPlayersLbl2.place(x=0,y=500)


playerNoLbl2 = Label(gameproperFr,text="Display player no.",font=("bold",10),fg="black")
playerNoLbl2.place(x=175,y=540)

###############loadingFr
gameNameLbl5 = Label(loadingFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

loadingMessageLbl = Label(loadingFr,text="Please wait while server is busy. :) \n",font=("bold",12),fg="black")
loadingMessageLbl.place(x=100,y=220)

###############votingFr
gameNameLbl6 = Label(votingFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

timerLbl = Label(votingFr,text="",width=55,justify="center",fg="white",bg="#808080",font=("bold",12))
timerLbl.place(x=0,y=140)

votingChatLog =  st.ScrolledText(votingFr,width=30,height=10,font=("Arial",9))
votingChatLog.place(x=20, y=190)
votingChatLog.configure(state="disabled")

gameResultLbl = Label(votingFr,text="Game Result",fg="white",bg="#c28234",width=30,height=10,font=("Arial",9),justify="center")
gameResultLbl.place(x=275,y=190)

voteChatText = Text(votingFr,width=20,height=2)
voteChatText.place(x=20,y=400)

sendBtn3 = Button(votingFr,relief="solid",text="Send",fg="white",bg="black",width=7,command=onClickSend3)
sendBtn3.place(x=200,y=400)

target2 = StringVar()
target2.set("++++")

p2 = [""]
spyDropList=OptionMenu(votingFr,target2,*p2)

target3 = StringVar()
target3.set("++++")

p3 = [""]
locationDropList=OptionMenu(votingFr,target3,*p3)


voteBtn = Button(votingFr,relief="solid",text="Vote",fg="white",bg="black",width=7,command=onClickVote)
voteBtn.place(x=200,y=450)

guessLocationBtn = Button(votingFr,relief="solid",text="Guess",fg="white",bg="black",width=7,command=onClickGuessLocation)

#backToMainBtn = Button(votingFr,relief="solid",text="Back to Main",fg="white",bg="black",width=10,command=onClickBackToMain)
###############displayMsgFr
gameNameLbl7 = Label(displayMsgFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

displayMsgLbl = Label(displayMsgFr,font=("bold",12),fg="black")
displayMsgLbl.place(x=100,y=220)

window.mainloop()



