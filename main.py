import tkinter as tk
from gui import GUI

def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# https://github.com/sunchit17/Snake-Game-Tkinter/blob/master/snake_game.py which heavily inspired my work here
# https://gist.github.com/bluemyria/23860eefeb6490bab5955c61147b299d this helped me with errors I was having at the end