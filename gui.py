from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

'''
	Setting up the game
'''
game = BattleshipGame(2, 5)

root = Tk()
root.title('Battleship')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#root frames
rootContent = ttk.Frame(root, padding=(5, 5, 5, 5))
headerFrame = ttk.Frame(rootContent, borderwidth=5, relief="ridge", width=800, height=100)
oceanFrame = ttk.Frame(rootContent, borderwidth=5, relief="ridge", width=800, height=550)
chatFrame = ttk.Frame(rootContent, borderwidth=5, relief="ridge", width=200, height=650)

rootContent.grid(column=0, row=0, sticky=(N, S, E, W))
headerFrame.grid(column=0, row=0, sticky=(N, E, W), padx=5, pady=5)
oceanFrame.grid(column=0, row=1, sticky=(N, S, E, W), padx=5, pady=5)
chatFrame.grid(column=1, row=0, rowspan=2, sticky=(N, S, E), padx=5, pady=5)

rootContent.columnconfigure(0, weight=1)
rootContent.rowconfigure(0, weight=1)
oceanFrame.columnconfigure(0, weight=1)
oceanFrame.rowconfigure(0, weight=1)
headerFrame.columnconfigure(0, weight=1)
headerFrame.rowconfigure(0, weight=1)
chatFrame.columnconfigure(0, weight=1)
chatFrame.rowconfigure(0, weight=1)

#header contents
headerLabel = ttk.Label(headerFrame, text="Battleship", justify="center")

headerLabel.grid(column=0, row=0, pady=30)

#ocean contents
leftFrame = ttk.Frame(oceanFrame, borderwidth=5, relief="sunken", width=400, height=550)
rightFrame = ttk.Frame(oceanFrame, borderwidth=5, relief="sunken", width=400, height=550)
leftGridFrame = ttk.Frame(leftFrame, borderwidth=5, width=380, height=380)
rightGridFrame = ttk.Frame(rightFrame, borderwidth=5, width=380, height=380)

leftFrame.grid(column=0, row=0, sticky=(N, E, W))
rightFrame.grid(column=1, row=0, sticky=(N, E, W))
leftGridFrame.grid(column=0, row=1)
rightGridFrame.grid(column=0, row=1)

leftFrame.columnconfigure(0, weight=1)
rightFrame.rowconfigure(0, weight=1)

leftGridPositions = [ [] for _ in range(game.oceanSize) ]
rightGridPositions = [ [] for _ in range(game.oceanSize) ]
posSize = int(leftGridFrame['width'] / game.oceanSize)

image = Image.open('images/ocean.gif').resize((posSize, posSize), Image.ANTIALIAS)
oceanImg = ImageTk.PhotoImage(image)

for _row in range(0, game.oceanSize):
	for _col in range(0, game.oceanSize):
		leftGridPositions[_row].append(ttk.Label(leftGridFrame, image=oceanImg))
		rightGridPositions[_row].append(ttk.Label(rightGridFrame, image=oceanImg))

		leftGridPositions[_row][_col].grid(column=_col, row=_row, sticky=(N, S, E, W), padx=2, pady=2)
		rightGridPositions[_row][_col].grid(column=_col, row=_row, sticky=(N, S, E, W), padx=2, pady=2)

leftGridHeader = ttk.Label(leftFrame, text="You", justify="center")
rightGridHeader = ttk.Label(rightFrame, text="Opponent", justify="center")

leftGridFooter = ttk.Label(leftFrame, text="", justify="center")
rightGridFooter = ttk.Label(rightFrame, text="", justify="center")

leftGridHeader.grid(column=0, row=0, pady=20)
rightGridHeader.grid(column=0, row=0, pady=20)

leftGridFooter.grid(column=0, row=2, pady=20)
rightGridFooter.grid(column=0, row=2, pady=20)

root.update()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()