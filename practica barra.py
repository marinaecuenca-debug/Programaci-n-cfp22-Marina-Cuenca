from tkinter import *

ventana = Tk()
ventana.geometry("400x400")
Label(ventana, text="Hola Mundo").pack()
barra=Listbox()
barra.insert(END,*(f"Elemento {i}"for i in range (20)))
barra.pack()
ventana.mainloop()
