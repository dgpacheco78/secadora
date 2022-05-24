from mainFrame import MainFrame
from tkinter import Tk
from ttkbootstrap import Style

def main():
    root = Tk()
    #style = Style('cosmo')
    #root = style.master
    root.wm_title("Secadora de Alimentos - UTIM")
    root.iconbitmap('icono.jpg')
    app = MainFrame(root)
    app.mainloop()

    #style = Style('cosmo')
    #root = style.master

if __name__=="__main__":
    main()