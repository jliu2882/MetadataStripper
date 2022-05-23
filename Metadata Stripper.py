from tkinter import * #requires tkinter to display a GUI
from exif import Image #requires exif to manipulate the file
from tkinter.filedialog import askopenfile #requires askopenfile to get user input
import sys #requires sys to change recursion limit
sys.setrecursionlimit(10**7) #Allow program to run longer

#Package Program:
#   pyinstaller -F "Metadata Stripper.py"

#Future Features:
#   Create nicer GUI
#   Add filter to search through metadata
#   Create a "SET METADATA" feature

#Modifiable variables
maxKeyLength = 35
maxValueLength = 50
initialAppTitle = ""
finalAppTitle = "Metadata Stripper"
popupTitle = "Error"
initialWindowSize = "200x100"
finalWindowSize = "750x500"
popupSize = "250x100"

#Set up window
window = Tk()
window.title(initialAppTitle)
window.geometry(initialWindowSize)
window.resizable(0, 0)

#Global variables
selected = []
programInput = ""
openFile = None
data = None
metadataList = Listbox(window)

#Selects item within displayed metadata
def selectEvent(e):
    global selected
    selected = [metadataList.get(idx) for idx in metadataList.curselection()]

#Select all metadata for the file
def selectAll():
    global selected
    metadataList.select_set(0, END)
    selected = [metadataList.get(idx) for idx in metadataList.curselection()]

#Submit the selected values
global submit
def submit():
    global selected, metadata, metadataList
    for value in selected:
        try:
            value = value.split(" ")[0]
            if value in data:
                openFile.delete(f"{value}")
                with open(programInput, "wb") as updatedFile:
                    updatedFile.write(openFile.get_file())
            selected = []
        except Exception as e:
            clearAll(e)
            return
    
    #Update the UI for the deleted metadata
    deleted = metadataList.curselection()
    for index in deleted[::-1]:
        metadataList.delete(index)

    #Get the remaining metadata and clear the screen if possible
    leftoverData = metadataList.get(0, END)
    if not leftoverData:
        clearAll()

#Clears the screen and resets it; and if applicable displays an error message
def clearAll(message=None):
    #Reset the window
    window.title(initialAppTitle)
    window.geometry(initialWindowSize)
    for widgets in window.winfo_children():
        widgets.destroy()
    uploadButton = Button(window, text="Upload File", command=lambda:open_file())
    uploadButton.pack(pady=25)
    
    #Create popup
    if(message):
        popup = Toplevel(window)
        popup.title(popupTitle)
        popup.geometry(popupSize)
        popupFrame = Label(popup, text=message, pady=30)
        popupFrame.pack()
    
#Opens a file and displays their metadata
def open_file():
    #Clear window
    for widgets in window.winfo_children():
        widgets.destroy()
    
    #Uses global variables
    global programInput, openFile, data, submit, metadataList

    #Open the file
    file_path = askopenfile(mode="r")
    if file_path is None:
        clearAll("Invalid File")
        return
    
    #Update window
    window.title(finalAppTitle)
    window.geometry(finalWindowSize)
    
    #Set the input for the program
    programInput = file_path.name
    with open(programInput, "rb") as openFile:
        openFile = Image(openFile)
    data = dir(openFile)
    
    #Create an array for the metadata to display
    metadata = []
    try:
        for datie in data:
            datieValue = openFile.get(datie,"")
            #Deleting metadata with no values will corrupt the file
            if(str(datieValue)==""):
                continue
            metadata.append((datie,datieValue))
    except:
        clearAll("Error reading file")
        return
    
    #We should not try to display nothing
    if not metadata:
        clearAll("File has no eraseable metadata")
        return
    
    #Set up components for the new window
    frame = Frame(window)
    uploadButton = Button(window, text="Upload New File", command=lambda:open_file())
    selectAllButton = Button(frame, text="Select All", command=selectAll)
    prompt = Label(frame, text="Select Metadata to Remove", width=25, height=2)
    submitButton = Button(frame, text="Remove", command=submit)
    scrollbar = Scrollbar(window)
    metadataList = Listbox(window, width=500, selectmode=MULTIPLE, yscrollcommand=scrollbar.set, font=("Courier", 10))
    metadataList.bind("<<ListboxSelect>>", selectEvent)
    for item in metadata:
        key = str(item[0])
        value = str(item[1])
        if(len(key)>maxKeyLength):
            key = key[0:maxKeyLength-3]+"..."
        if(len(value)>maxValueLength):
            value = value[0:maxValueLength-3]+"..."
        line = f"{key:<35} | {value}"
        metadataList.insert(END, line)
    scrollbar.config(command=metadataList.yview)

    #Pack everything into the new scene
    uploadButton.pack(pady=5)
    selectAllButton.pack(side=LEFT)
    prompt.pack(side=LEFT)
    submitButton.pack(side=RIGHT)
    frame.pack(padx=1, pady=1)
    scrollbar.pack(side=RIGHT, fill=Y)
    metadataList.pack(side=LEFT, fill=BOTH)

#Create upload button to accept custom files
uploadButton = Button(window, text="Upload File", command=lambda:open_file())
uploadButton.pack(pady=25)

#Wait for user input
window.mainloop()
