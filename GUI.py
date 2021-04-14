import requests
from tkinter import *
from functools import partial
import time
import datetime
from multiprocessing import Process
import random
#import client
#############GLOBAL VARS
playerName = ""
lobbyCode = ""
playerId = ""
inLobby = False
inGame = False


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
		res.raise_for_status()
		servermsg = res.json()
		return servermsg

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
		

##############GUI
def update():
	global inLobby
	global inGame
	if inLobby == True:
		servermsg = status_check()
		if servermsg["arg1"] == 2:
			inLobby = False
			inGame = True
			startGameFr.tkraise()
	window.after(10000,update)

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
				update()
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
		update()
	else:
		displayPopUp("Failed to join lobby. Please check lobby code.")

def onClickExit():
	#reset global vars
	servermsg = exit()
	if servermsg["arg1"] == "ok":
		global playerName
		global lobbyCode
		global playerId
		global inLobby
		global inGame
		playerName = ""
		lobbyCode = ""
		playerId = ""
		inLobby = False
		inGame = False
		displayPopUp("Successfully exited lobby!")
		hostOrJoinLobbyFr.tkraise()
	else:
		displayPopUp(arg1)

def onClickStartGame():
	#startGameFr.tkraise()
	start()

###############frames
startGameFr = Frame(window)
startGameFr.place(x=0,y=0,height=600,width=500)

lobbyFr = Frame(window)
lobbyFr.place(x=0,y=0,height=600,width=500)

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

exitBtn = Button(lobbyFr,relief="solid",text="Exit",fg="white",bg="black",command=onClickExit)
startGameBtn = Button(lobbyFr,relief="solid",text="Start game",fg="white",bg="black",command=onClickStartGame)

exitBtn.place(x=180,y=500)
startGameBtn.place(x=250,y=500)
###############startGameFr
gameNameLbl4 = Label(startGameFr,text="Spy Among Us",font=("bold",30),fg="white",bg="black",width=22,pady=30).place(x=0,y=0)

exitBtn2 = Button(startGameFr,relief="solid",text="Exit",fg="white",bg="black",command=onClickExit)
exitBtn2.place(x=180,y=500)

window.mainloop()


