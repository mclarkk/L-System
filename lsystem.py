##Meghan Is Awesooooome!

##Square brackets are special! To the staaack

from Tkinter import *
from turtle import *
import random

class Application(Frame):
	""" A GUI application for L-Systems """

	def __init__(self, master):
		""" Initialize the frame."""
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		self.labels = []
		self.ruleBoxes = []
		self.interpBoxes = []
		self.stack = []

		self.alphabet = ""
		self.isAlphaSet = False

		self.titleLabel = Label(self, text = "I LIKE TURTLES!")
		self.titleLabel.grid(row=0,column=0,columnspan=3, sticky=W, padx=5, pady=15)

		self.label1 = Label(self, text = "Alphabet: ")
		self.label1.grid(row=1, column=0, sticky=E, padx=5)

		self.alphaBox = Entry(self)
		self.alphaBox.grid(row=1, column=1)
		
		self.alphaButton = Button(self, text = "Set Alphabet")
		self.alphaButton.grid(row=1, column=2, columnspan=2)
		self.alphaButton["command"] = self.updateAlphabet
	
		#these guys' positions are set in adjustBottom
		self.axiomLabel = Label(self, text = "Axiom: ")
		self.axiomBox = Entry(self)
		self.iterLabel = Label(self, text = "Iterations: ")
		self.iterBox = Entry(self)
		self.iterBox.insert(0, "5")
		self.posLabel = Label(self, text = "Start at: ")
		self.posBox = Entry(self)
		self.posBox.insert(0, "0 0")
		self.genButton = Button(self, text = "Generate!")
		self.genButton["command"] = self.run
		
	def updateAlphabet(self):
		#verify alphabet is good
		alphabet = self.alphaBox.get()
		alphabet = alphabet.rstrip()
		alphabet = alphabet.split() #Now it's an array of the letters
		#verify
		isGood, message = self.checkAlphabet(alphabet)
		if (not isGood):
			self.alphaBox.delete(0, END)
			self.alphaBox.insert(0, message)
			return 0
		#if here, it's good. Add brackets and update GUI
		alphabet.append("[")
		alphabet.append("]")
		self.alphabet = alphabet
		
		#destroy any old widgets
		for eachLabel in self.labels:
			eachLabel.destroy()
		for eachRuleBox in self.ruleBoxes:
			eachRuleBox.destroy()
		for eachInterpBoxes in self.interpBoxes:
			eachInterpBoxes.destroy()
		self.labels=[]
		self.ruleBoxes=[]
		self.interpBoxes=[]

		#make new widgets
		i = 6
		for j in range(0, len(alphabet)-2):
			label = Label(self, text = alphabet[j]+" ")
			label.grid(row=i, column=0, sticky=E)
			ruleBox = Entry(self)
			ruleBox.grid(row=i, column=1)
			interpBox = Entry(self)
			interpBox.grid(row=i, column=2, columnspan=2, padx=10)
			self.labels.append(label)
			self.ruleBoxes.append(ruleBox)
			self.interpBoxes.append(interpBox)
			i+=1

		self.genButton.grid(row=i, column=2, columnspan=2, pady=10)
		
		#if this is the first time setting the alphabet, 
		#finish initializing the GUI
		if not self.isAlphaSet:
			self.isAlphaSet = True
			self.ruleLabel = Label(self, text = "Replacement rules:")
			self.ruleLabel.grid(row=5, column=1, pady=5)
			self.interpLabel = Label(self, text = "Interpretation rules:")
			self.interpLabel.grid(row=5, column=2, columnspan=2)
			self.axiomLabel.grid(row=2, column=0, sticky=E)
			self.axiomBox.grid(row=2, column=1, padx=5)
			self.iterLabel.grid(row=3, column=0, sticky=E)
			self.iterBox.grid(row=3, column=1, padx=5)
			self.posLabel.grid(row=4, column=0, sticky=E)
			self.posBox.grid(row=4, column=1, padx=5)
			self.orientLabel = Label(self, text = "Initial heading:")
			self.orientLabel.grid(row=2, column=2, columnspan=2, sticky=W, padx=5)
			self.orientation = StringVar()
			self.eRadio = Radiobutton(self, text="East", variable=self.orientation, value=0)
			self.eRadio.grid(row=3, column=2, sticky=W, padx=5)
			self.nRadio = Radiobutton(self, text="North", variable=self.orientation, value=90)
			self.nRadio.grid(row=4, column=2, sticky=W, padx=5)
			self.wRadio = Radiobutton(self, text="West", variable=self.orientation, value=180)
			self.wRadio.grid(row=3, column=3, sticky=W)
			self.sRadio = Radiobutton(self, text="South", variable=self.orientation, value=270)
			self.sRadio.grid(row=4, column=3, sticky=W)
			self.eRadio.select()

	def checkAlphabet(self, alphabet):
		"""So what's an (in)valid alphabet? No [ or ] brackets! Each symbol must be a single character, and also unique."""
		valid = True
		message = ""
		for eachCharacter in alphabet:
			if eachCharacter == '[' or eachCharacter == ']':
				message = "No [ or ] brackets!"
				valid = False
			if not len(eachCharacter) == 1:
				message = "Symbols must be single characters!"
				valid = False
			if alphabet.count(eachCharacter) > 1:
				message = "Symbols must be unique!"
				valid = False
		return valid, message

	def ofAlphabet(self, s):
		"""returns True if every character in s is also in self.alphabet"""
		flag = True
		for eachChar in s:
			try:
				self.alphabet.index(eachChar)
			except:
				flag = False
		return flag
		
		
	def run(self):
		"""grab the info, verify it, generate L-system!"""
		#verification for rules and axiom: Every rewrite character is in the alphabet.
		#verification for interpretations simply means they don't crash when eval()'d.
		#(yes, this is dangerous.)
		#iterations must be a positive (>0) integer
		#coordinates must be a pair of ints/floats

		rules = []
		interpretations = []
		axiom = ""
		iterations = 0
		coordinates = []

		#Every field must be filled out, first of all.
		#verification for rules: Every character is in the alphabet.
		valid = True
		for eachRuleBox in self.ruleBoxes:
			rule = eachRuleBox.get()
			rules.append(rule)
			if rule == "":
				eachRuleBox.insert(0, "Fill me out!")
				valid = False
			elif not self.ofAlphabet(rule):
				eachRuleBox.delete(0, END)
				eachRuleBox.insert(0, "Symbols must be in the alphabet!")
				valid = False
		rules.append("[")
		rules.append("]")

		for eachInterpBox in self.interpBoxes:
			interp = eachInterpBox.get().split()
			interpretations.append(interp)
			if interp == []:
				eachInterpBox.insert(0, "Fill me out!")
				valid = False
		interpretations.append(["self.turtlePush()"])
		interpretations.append(["self.turtlePop()"])
		
		#verification for axiom: Every character is in the alphabet.
		axiom = self.axiomBox.get()
		if axiom == "":
			self.axiomBox.insert(0, "Fill me out!")
			valid = False
		elif not self.ofAlphabet(axiom):
			self.axiomBox.delete(0, END)
			self.axiomBox.insert(0, "Symbols must be in the alphabet!")
			valid = False

		#iterations must be a positive (>0) integer
		iterations = self.iterBox.get()
		if iterations == "":
			self.iterBox.insert(0, "Fill me out!")
			valid = False
		else:
			try:
				iterations = int(iterations)
				if iterations <= 0:
					self.posBox.delete(0, END)
					self.posBox.insert(0, "Must be greater than zero!")
					valid = False
			except:
				self.posBox.delete(0, END)
				self.posBox.insert(0, "Must be an integer!")
				valid = False

		#coordinates must be a pair of ints/floats
		coordinates = self.posBox.get().split()
		if coordinates == []:
			self.posBox.insert(0, "Fill me out!")
			valid = False
		elif not len(coordinates) == 2:
			self.posBox.delete(0, END)
			self.posBox.insert(0, "Must be two points!")
			valid = False
		else:
			for i in range(0,len(coordinates)):
				try:
					coordinates[i] = float(coordinates[i])
				except:
					self.posBox.delete(0, END)
					self.posBox.insert(0, "Must be integers or floats!")
					valid = False

		#grab-and-verify stage complete!
		if not valid:
			return 0
			
		#if you get here, everything is good!
		#let's generate that L-system!
		self.generateLSystem(axiom, rules, iterations, interpretations, coordinates)	

	def generateLSystem(self, axiom, rules, iterations, interpretations, coordinates):
		#generate final string
		finalString = axiom
		for i in range(0, iterations):
			s = ""
			for eachChar in finalString:
				index = self.alphabet.index(eachChar)
				s += rules[index]
			finalString = s

		#interpret it
		clear()
		title("L-System")
		speed(0) #fastest
		ht()
		pu()
		setheading(float(self.orientation.get()))
		setpos(coordinates)
		pd()
		interp = ""
		currentSymbol = ""
		try:
			for eachChar in finalString:
				currentSymbol = eachChar
				index = self.alphabet.index(currentSymbol)
				interps = interpretations[index]
				for eachInterp in interps:
					interp = eachInterp
					eval(interp)
		except:
			print "Either you closed a window, or the interpretation " + interp + " for " + currentSymbol + " broke eval()."

	def turtlePush(self):
		state = [pos(), heading()]
		self.stack.append(state)

	def turtlePop(self):
		state = self.stack.pop()
		pu()
		setpos(state[0])
		setheading(state[1])
		pd()

#main loop
root = Tk()
root.title("Meghan's Awesome(!!!) L-System Machine")
#root.geometry("450x400")

app = Application(root)

root.mainloop()

