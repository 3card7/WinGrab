import tkinter as tk
import subprocess

#Creates root window
root = tk.Tk()

#Sets size of root window and title
root.geometry("800x400")
root.title("My Window")

#Function for making window buttons
def createButton(name, text, windowID):
    name = tk.Button(windowListFrame, text=text, bg="green", width=35, height=1, anchor='w', command=lambda: onButtonClick(windowID))
    return name

#Function that runs the wmctrl -l command and then splits each line into list items
def createWindowList():
    windowList = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True)
    listOfWindows = windowList.stdout.splitlines()
    return listOfWindows

#Button click comand
selectedWindow = "placeholder"
def onButtonClick(windowID):
    global selectedWindow
    print(f"{windowID} has been selected.")
    selectedWindow = windowID

#Function for the resize window command
def resize():
    resizeWidth = sizeWidthEntry.get()
    resizeLength = sizeLengthEntry.get()
    commandString = "0,100,100," + resizeWidth + "," + resizeLength
    subprocess.run(["wmctrl", "-i", "-r", selectedWindow, "-e", commandString])

#Function for the capture window command
def capture():
    fileName = fileNameEntry.get()
    saveLocation = saveLocationEntry.get()
    fileName = saveLocation + "/" + fileName + ".png"
    subprocess.run(["scrot", "-w", selectedWindow, fileName])
    subprocess.run(["wmctrl", "-i", "-r", selectedWindow, "-b", "add,hidden"])

#Function for creating the list of windows
def createList():
    listOfWindows = createWindowList()
    for widget in windowListFrame.winfo_children():
        widget.destroy()

    rowCount = 0
    for window in listOfWindows:
        newButton = createButton(window[0:10], window, window[0:10])
        newButton.grid(row=rowCount, column=0)
        rowCount += 1

#function for custom size checkbox behavior
def enableCustomSize():
    if customSizeVar.get() == 0:
        sizeWidthEntry.delete(0, tk.END)
        sizeLengthEntry.delete(0, tk.END)
        sizeWidthEntry.insert(0, "1280")
        sizeLengthEntry.insert(0, "720")
        sizeWidthEntry.config(state="disable")
        sizeLengthEntry.config(state="disable")
    elif customSizeVar.get() == 1:
        sizeWidthEntry.config(state="normal")
        sizeLengthEntry.config(state="normal")

#Function for file name checkbox behavior
def enableFileName():
    if fileNameVar.get() == 0:
        fileNameEntry.delete(0, tk.END)
        fileNameEntry.insert(0, "Screenshot")
        fileNameEntry.config(state="disabled")
    elif fileNameVar.get() == 1:
        fileNameEntry.config(state="normal")

#Function for save location
def enableSaveLocation():
    if saveLocationVar.get() == 0:
        saveLocationEntry.delete(0, tk.END)
        saveLocationEntry.insert(0, "/home/kali/Pictures")
        saveLocationEntry.config(state="disabled")
    elif saveLocationVar.get() == 1:
        saveLocationEntry.config(state="normal")

#Creating the display frames
windowListFrame = tk.Frame(root, height=10, bg="red", padx=5, pady=5)
optionsFrame = tk.Frame(root, bg="blue", padx=5, pady=5)
outputFrame = tk.Frame(root)
listOptionsFrame = tk.Frame(root, bg="purple", padx=5, pady=5)

#Calls function to create and display buttons for each window
createList()

#Place the frames
windowListFrame.grid(row=1, column=0)
optionsFrame.grid(row=1,column=1, sticky="N")
listOptionsFrame.grid(row=2, column=0)

#Creates the entry box for custom width and disables it.
sizeWidthEntry = tk.Entry(optionsFrame, width=10)
sizeWidthEntry.insert(0, "1280")
sizeWidthEntry.config(state="disabled")

#Creates the entry box for custom length and disables it.
sizeLengthEntry = tk.Entry(optionsFrame, width=10)
sizeLengthEntry.insert(0, "720")
sizeLengthEntry.config(state="disabled")

#Creates the entry box for custom file name and disables it
fileNameEntry = tk.Entry(optionsFrame, width=20)
fileNameEntry.insert(0, "Screenshot")
fileNameEntry.config(state="disabled")

#Creates the entry box for save location
saveLocationEntry = tk.Entry(optionsFrame, width=20)
saveLocationEntry.insert(0, "/home/kali/Pictures")
saveLocationEntry.config(state="disabled")

#Makes the check box for custom size
customSizeVar = tk.IntVar(value=0) #Starts button unchecked
customSizeCheck = tk.Checkbutton(optionsFrame, text="Custom Size", variable=customSizeVar, command=enableCustomSize)

#Makes the check box for custom file name
fileNameVar = tk.IntVar(value=0) #Starts button unchecked
fileNameCheck = tk.Checkbutton(optionsFrame, text="File Name", variable=fileNameVar, command=enableFileName)

#Makes the check box for save location
saveLocationVar = tk.IntVar(value=0) #Starts button unchecked
saveLocationCheck = tk.Checkbutton(optionsFrame, text="Save Location", variable=saveLocationVar, command=enableSaveLocation)

#Button to resize window
resizeButton = tk.Button(optionsFrame, text="Resize Window", bg="orange", command=resize)

#Button to capture window
captureButton = tk.Button(optionsFrame, text="Capture Window", bg="orange", command=capture)

#Button to refresh list
refreshButton = tk.Button(listOptionsFrame, text="Refresh", bg="orange", command=createList)

#Placing buttons
resizeButton.grid(row=3, column=0)
captureButton.grid(row=3, column=1)
refreshButton.grid(row=1, column=0)

#Placing the check boxes
customSizeCheck.grid(row=0, column=0)
sizeWidthEntry.grid(row=0, column=1)
sizeLengthEntry.grid(row=0, column=2)

#Placing file name
fileNameCheck.grid(row=1,column=0)
fileNameEntry.grid(row=1,column=1)

#Placing save location
saveLocationCheck.grid(row=2, column=0)
saveLocationEntry.grid(row=2, column=1)
root.mainloop()
