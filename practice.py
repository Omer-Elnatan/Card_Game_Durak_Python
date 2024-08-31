 # put file path for the image.



import Tkinter as tk
from PIL import ImageTk, Image

path = 'G:\project_pictures\Ace_Clover.png'

root = tk.Tk()
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()




