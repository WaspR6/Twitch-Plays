import socket
import threading
from turtle import right
from ahk import AHK

# If there is an error in the code above for the imports open your Command Prompt and type the following ---> pip install then whatever you are having errors. So if import socket has an error i would type pip install socket
ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')

SERVER = "irc.twitch.tv"
PORT = 6667

# Follow the following link to generate your password toaken. Paste that long ass gibrish inbetween the ""s
PASS = ""

BOT = "TwitchBot"

# Name of channel
CHANNEL = ""

# Name of Channel owner. Should be same as channel name
OWNER = ""

# Leave blank
message = ""

# Leave blank
user = ""

irc = socket.socket()

irc.connect((SERVER, PORT))
irc.send((	"PASS " + PASS + "\n" +
			"NICK " + BOT + "\n" +
			"JOIN #" + CHANNEL + "\n").encode())

def gamecontrol():

	global message

	#Movement
    #The word after the if statement is what the twitch chat will type in to get the command to trigger. 
    # The letter after ahk.key_down is the letter that your keyboard will press. The number at the end of the statement is the amount of seconds the key will be heald down.
	while True:

		if "forward" == message.lower():
			ahk.key_down('w', 2)
			message = ""

		if "stop" == message.lower():
			ahk.key_release('w')
			message = ""

		if "back" == message.lower():
			ahk.key_press('s')
			message = ""

		if "left" == message.lower():
			ahk.key_press('a')
			message = ""

		if "right" == message.lower():
			ahk.key_press('d')
			message = ""

		if "pew" == message.lower():
			ahk.key_press('up')
			message = ""

		if "aim" == message.lower():
			ahk.key_down('down')
			message = ""

		if "stop aim" == message.lower():
			ahk.key_release('down')
			message = ""

		if "look right" == message.lower():
			ahk.key_press('p')
			message = ""

		if "look left" == message.lower():
			ahk.key_press('l')
			message = ""

		if "look up" == message.lower():
			ahk.key_press('o')
			message = ""

		if "look down" == message.lower():
			ahk.key_press('k')
			message = ""

		if "lean left" == message.lower():
			ahk.key_press('v')
			message = ""

		if "lean right" == message.lower():
			ahk.key_press('b')
			message = ""

		if "crouch" == message.lower():
			ahk.key_press('c')
			message = ""

		if "gadget" == message.lower():
			ahk.key_press('4')
			message = ""

		if "gun" == message.lower():
			ahk.key_press('1')
			message = ""

		if "secondary" == message.lower():
			ahk.key_press('2')
			message = ""

		if "knife" == message.lower():
			ahk.key_press('e')
			message = ""

		if "nades" == message.lower():
			ahk.key_press('q')
			message = ""

		if "fire mode" == message.lower():
			ahk.key_press('g')
			message = ""

		if "reload" == message.lower():
			ahk.key_press('r')
			message = ""
def twitch():

	global user
	global message

	def joinchat():
		Loading = True
		while Loading:
			readbuffer_join = irc.recv(1024)
			readbuffer_join = readbuffer_join.decode()
			print(readbuffer_join)
			for line in readbuffer_join.split("\n")[0:-1]:
				print(line)
				Loading = loadingComplete(line)

	def loadingComplete(line):
		if("End of /NAMES list" in line):
			print("TwitchBot has joined " + CHANNEL + "'s Channel!")
			sendMessage(irc, "Bot Activated!!!!")
			return False
		else:
			return True

	def sendMessage(irc, message):
		messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
		irc.send((messageTemp + "\n").encode())

	def getUser(line):
	
		colons = line.count(":")
		colonless = colons-1
		separate = line.split(":", colons)
		user = separate[colonless].split("!", 1)[0]
		return user

	def getMessage(line):
		
		try:
			colons = line.count(":")
			message = (line.split(":", colons))[colons]
		except:
			message = ""
		return message

	def console(line):
		if "PRIVMSG" in line:
			return False
		else:
			return True

	joinchat()
	irc.send("CAP REQ :twitch.tv/tags\r\n".encode())
	while True:
		try:
			readbuffer = irc.recv(1024).decode()
		except:
			readbuffer = ""
		for line in readbuffer.split("\r\n"):
			if line == "":
				continue
			if "PING :tmi.twitch.tv" in line:
				print(line)
				msgg = "PONG :tmi.twitch.tv\r\n".encode()
				irc.send(msgg)
				print(msgg)
				continue
			else:
				try:
					user = getUser(line)
					message = getMessage(line)
					print(user + " : " + message)
				except Exception:
					pass

def main():
	if __name__ =='__main__':
		t1 = threading.Thread(target = twitch)
		t1.start()
		t2 = threading.Thread(target = gamecontrol)
		t2.start()
main()
