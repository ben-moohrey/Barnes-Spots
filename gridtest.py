import tkinter as tk
from PIL import ImageTk, Image
class TestUI:
    def __init__(self, parent):

        load = Image.open("Orange_logo.png")
        load = load.resize((50,100), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(parent, image=render)
        img.image = render
        img.grid(column=2)

        self.label = tk.Label(parent, text="Test")
        self.label.grid(column=1, row=0)

        self.label2 = tk.Label(parent, text="Image")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test")
    root.configure(bg='orange')
    barnesApp = TestUI(root)
    root.mainloop()
