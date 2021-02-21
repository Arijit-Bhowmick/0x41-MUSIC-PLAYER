from tkinter import *  
  
def select(sel):  
  #sel = "Value = " + str(v.get())  
  label.config(text = sel)  
 
top = Tk()  
top.geometry("200x100")  
v = DoubleVar()  
scale = Scale( top, variable = v, from_ = 1, to = 50, orient = HORIZONTAL, command=select)  
scale.pack(anchor=CENTER)  
  
btn = Button(top, text="Value", command=select)  
btn.pack(anchor=CENTER)  
  
label = Label(top)  
label.pack()  
  
top.mainloop()