import tkinter as tk
from tkinter import messagebox
import sys
import os

#Defining some settings
LARGE_FONT=("VERDANA",12)
welcometext_FONT=("VERDANA",10)
backgroundColor='#FAFAFA'

numberErrorMessage="You did not enter a positive number"

#Method that checks if a text is int, used for error handling
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#Main tkinter class where we old the page classes
class RobotPlantCare(tk.Tk):


    def __init__(self,sendData,*args,**kwargs):
        
        tk.Tk.__init__(self,*args,**kwargs)

        #Settings for the window
        try:
            self.iconbitmap("icon.ico")
        except:
            print("Icon not found")
        self.geometry("660x370")
        self.configure(background=backgroundColor)
        container = tk.Frame(self)

        #Setting grid sizes
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            root.grid_columnconfigure(col, minsize=20)
        for row in range(row_count):
            root.grid_rowconfigure(row, minsize=20)
        container.grid()
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        #Making the pages and storing them
        self.frames={}

        for F in (ManualControl,StartCare,Help):#,RobotControl,RobotConfigure,Help):

            if F is StartCare or F is ManualControl:
                frame=F(container,self,sendData)
            else:
                frame=F(container,self)

            self.frames[F]=frame

            frame.grid(row=0,column=0,sticky="nsew")

        #Showing the Help frame when the program starts
        self.show_frame(Help)

    #Method used for visualising pages
    def show_frame(self,cont):

        frame=self.frames[cont]
        frame.tkraise()

#Method used for the exit button
def Exit():
        answer=tk.messagebox.askquestion('Exiting application', "Are you sure you want to exit")
        if answer=="yes":
            os._exit(0)


#method for creating the menu in each frame
def Menu(self,controller,name):

        #Creating the page header and some options
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.configure(background=backgroundColor)
        label=tk.Label(self,text=name, font=LARGE_FONT,background=backgroundColor)
        label.grid(row=0,column=1,columnspan=8,padx=25,sticky="we")

        #Creating the menu buttons
        manualControlButton=tk.Button(self,text="Manual Control",
                              command=lambda:controller.show_frame(ManualControl))
        
        startCareButton=tk.Button(self,text="Start",
                              command=lambda:controller.show_frame(StartCare))
        
        helpButton=tk.Button(self,text="Help",
                              command=lambda:controller.show_frame(Help))
        
        exitButton=tk.Button(self,text="Exit",
                              command=lambda:Exit())

        #Defining parameters used for visualising the buttons
        buttonBG="#5caceb"
        defWidth=30
        defHeight=5

        #Configuring the buttons
        manualControlButton.config(width=defWidth,  height=defHeight,   background=buttonBG)
        startCareButton.config(width=defWidth,  height=defHeight,   background=buttonBG)
        helpButton.config(width=defWidth,   height=defHeight,   background=buttonBG)
        exitButton.config(width=defWidth,   height=defHeight,   background=buttonBG)

        #Visualising the menu buttons
        manualControlButton.grid(row=1,column=0,sticky="w")
        startCareButton.grid(row=2,column=0,sticky="w")
        helpButton.grid(row=3,column=0,sticky="w")
        exitButton.grid(row=4,column=0,sticky="w")



class ManualControl(tk.Frame):

    def __init__ (self, parent, controller,sendData):

        tk.Frame.__init__(self,parent)
        
        Menu(self,controller,"Manual Control")

        #Creating the buttons for the controller
        upButton=tk.Button(self,text="Forward",
                              command=lambda:sendData("Direct F"))
        downButton=tk.Button(self,text="Back",
                              command=lambda:sendData("Direct B"))
        leftButton=tk.Button(self,text="Left",
                              command=lambda:sendData("Direct L"))
        rightButton=tk.Button(self,text="Right",
                              command=lambda:sendData("Direct R"))
        stopButton=tk.Button(self,text="Stop",
                              command=lambda:sendData("Direct S"))

        #Setting them up and making them look better
        controlButtonHeight=5
        controlButtonWidth=10
        controlButtonBackground="#81DAF5"
        upButton.config(width=controlButtonWidth,   height=controlButtonHeight,   background=controlButtonBackground)
        downButton.config(width=controlButtonWidth,   height=controlButtonHeight,   background=controlButtonBackground)
        leftButton.config(width=controlButtonWidth,   height=controlButtonHeight,   background=controlButtonBackground)
        rightButton.config(width=controlButtonWidth,   height=controlButtonHeight,   background=controlButtonBackground)
        stopButton.config(width=controlButtonWidth,   height=controlButtonHeight,   background=controlButtonBackground)

        #Visualising the buttons
        upButton.grid(row=1,column=3)
        downButton.grid(row=3,column=3)
        leftButton.grid(row=2,column=2,sticky="e")
        rightButton.grid(row=2,column=4)
        stopButton.grid(row=2,column=3)
        


class StartCare(tk.Frame):

    def __init__ (self, parent, controller,sendData):

        tk.Frame.__init__(self,parent)

        potnum=0

        #Gives access to the method used for sending data without having it in the UI code
        self.sendData=sendData
        
        #Some button settings
        self.controlButtonHeight=3
        self.controlButtonWidth=6
        self.controlButtonBackground="#50AEFB"

        #Creating the UI
        Menu(self,controller,"Start Automatic Care")
        potsEntry=tk.Entry(self,textvariable=potnum,width=3)
        confirmButton=tk.Button(self,text="Confirm",
                              command=lambda:self.createLabels(potsEntry.get()))
        potsLabel=tk.Label(self,text="Write a number of pots:",background=backgroundColor)

        #Configuring the elements
        confirmButton.config(width=self.controlButtonWidth,   height=self.controlButtonHeight,   background=self.controlButtonBackground)
        potsLabel.config(padx=10,pady=10)

        #Visualising them
        potsLabel.grid(row=1,column=2,padx=10,pady=10)
        potsEntry.grid(row=1,column=3,sticky="e")
        confirmButton.grid(row=1,column=4,padx=10,pady=10)

        self.potsList=tk.Listbox(self,height=0)


    #Handling errors before making the list box
    def createLabels(self,potnum):
        if RepresentsInt(potnum) is True and int(potnum)>=0:
            self.makeListbox(potnum)
        else:
            error=tk.messagebox.showinfo(title="Error",message=numberErrorMessage)

    #Auctally making and visualising the list box
    def makeListbox(self,potnum):

        
        potsListHeight=0

        #Destroying the previous list box when the user wants to make a new one
        self.potsList.destroy()

        #Handling the size of the listbox
        if int(potnum)>15:
            potsListHeight=15
        else:
            potsListHeight=potnum

        #Creating the listbox
        self.potsList=tk.Listbox(self,height=potsListHeight)

        #Filling the listbox with default values
        for i in range(1,int(potnum)+1):
            self.potsList.insert(i,"Pot "+str(i)+" : 50 ml")

        #Making the scrollbar
        scrollbar=tk.Scrollbar(self,orient=tk.VERTICAL)
        self.potsList['yscrollcommand']=scrollbar.set
        scrollbar['command']=self.potsList.yview

        #Visualising the scrollbar and potsList
        scrollbar.grid(row=2,column=3,columnspan=2,rowspan=6,sticky=tk.N+tk.S+tk.W)
        self.potsList.grid(row=2,column=2,rowspan=8)

        #Creating the option to change the data in the listbox
        changeLabel=tk.Label(self,text="Write a number to change:",background=backgroundColor)
        changeLabel.grid(row=2,column=4,sticky="n")
        changeEntry=tk.Entry(self,width=5)
        changeEntry.grid(row=2,column=5,sticky="nw")
        
        changeButton=tk.Button(self,text="Change",
                              command=lambda:self.changeListboxValue(changeEntry.get()))
        changeButton.config(width=self.controlButtonWidth,   height=self.controlButtonHeight,   background=self.controlButtonBackground)
        changeButton.grid(row=2,column=4,padx=10,pady=10,sticky="sw")
        
        #Creating the part for entering timing and sending the options to the robot
        timingLabel=tk.Label(self,text="Time interval in hours:",background=backgroundColor)
        timingLabel.grid(row=3,column=4,sticky="n")

        self.timingEntry=tk.Entry(self,width=5)
        self.timingEntry.grid(row=3,column=5,sticky="nw")

        sendOptionsButton=tk.Button(self,text="Send options",command=lambda:self.sendOptionsData())
        sendOptionsButton.config(width=self.controlButtonWidth*2,   height=self.controlButtonHeight,   background=self.controlButtonBackground)
        sendOptionsButton.grid(row=4,column=5)

    #Collects the data, handles errors and sends to the robot
    def sendOptionsData(self):
        timing=self.timingEntry.get()

        sendDataString="Options "

        #Handling error for user input
        if RepresentsInt(timing) is True and int(timing)>=0:

            #Creating a string containing information to send to the robot
            sendDataString+=str(timing)
            sendDataString+=" "
            for i, listbox_entry in enumerate(self.potsList.get(0, tk.END)):
                
                entrydata=listbox_entry.split(' ')
                data=int(entrydata[3])
                sendDataString+=str(data)
                sendDataString+=" "

            #Sending the information
            self.sendData(sendDataString)
        else:
            error=tk.messagebox.showinfo(title="Error",message=numberErrorMessage)
            
        
    #Used for changing the options in the listbox and handling errors
    def changeListboxValue(self,newvalue):

        if RepresentsInt(newvalue) and int(newvalue) >= 0:
            
            oldvalue=self.potsList.get('active')
            oldvalueInfo=oldvalue.split(' ')
            index=int(oldvalueInfo[1])
            self.potsList.delete(index-1)
            self.potsList.insert(index-1,oldvalueInfo[0]+" "+oldvalueInfo[1]+" : "+str(newvalue)+" ml")
            
        else:
            error=tk.messagebox.showinfo(title="Error",message=numberErrorMessage)


        

class Help(tk.Frame):

    def __init__ (self, parent, controller):

        tk.Frame.__init__(self,parent)
        
        Menu(self,controller,"Help")

        #Making a simple text which gives helpful info to the user
        line1="Welcome to the dekstop app for the robot.\n"
        line2="This awesome robot is brought to you by:\n"
        line3="Boris Velkovski\n"
        line4="Special thanks to my mentors:\n"
        line5="Petar Ivanov & Velislava Emilova\n\n"
        
        line6="Use the Manual Control section to manualy \n"
        line7="control the robot by using the "
        line8="buttons. Press\nthe stop button at anytime to stop the robot "
        line9="\neven when he started his work.\n\n "
        line10="Use the send options section to pick and \n send your options. Start by selecting\na number of vases "
        line11="then check the default\n options and change them if needed. "
        line12="Select the\n timing,which the robot leaves inbetween\n his watering. "
        line13="Click the send options button\n to send your options and start the robot\n automatic tasks."

        
        helptext=line1+line2+line3+line4+line5+line6+line7+line8+line9+line10+line11+line12+line13

        
            
        text1=tk.Label(self,height=20,width=35,text=helptext)
        text1.grid(row=1,column=1,rowspan=5,columnspan=15,sticky="w")

