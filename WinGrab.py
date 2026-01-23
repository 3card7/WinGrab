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
    subprocess.run(["wmctrl", "-i", "-r", selectedWindow, "-e", "0,100,100,950,504"])

#Function for the capture window command
def capture():
    subprocess.run(["scrot", "-w", selectedWindow, "scripted.png"])
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
        sizeWidth.config(state="disable")
        sizeLength.config(state="disable")
    elif customSizeVar.get() == 1:
        sizeWidth.config(state="normal")
        sizeLength.config(state="normal")

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
sizeWidth = tk.Entry(optionsFrame, width=10)
sizeWidth.insert(0, "1280")
sizeWidth.config(state="disabled")

#Creates the entry box for custom length and disables it.
sizeLength = tk.Entry(optionsFrame, width=10)
sizeLength.insert(0, "720")
sizeLength.config(state="disabled")

#Makes the check box for custom size
customSizeVar = tk.IntVar(value=0) #Starts button unchecked
customCheck = tk.Checkbutton(optionsFrame, text="Custom Size", variable=customSizeVar, command=enableCustomSize)

#Button to resize window
resizeButton = tk.Button(optionsFrame, text="Resize Window", bg="orange", command=resize)

#Button to capture window
captureButton = tk.Button(optionsFrame, text="Capture Window", bg="orange", command=capture)

#Button to refresh list
refreshButton = tk.Button(listOptionsFrame, text="Refresh", bg="orange", command=createList)

#Placing buttons
resizeButton.grid(row=1, column=0)
captureButton.grid(row=1, column=1)
refreshButton.grid(row=1, column=0)

#Placing the check boxes
customCheck.grid(row=0, column=0)
sizeWidth.grid(row=0, column=1)
sizeLength.grid(row=0, column=2)

root.mainloop()
