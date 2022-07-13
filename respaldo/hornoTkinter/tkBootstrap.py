from ttkbootstrap import Style
from ttkbootstrap.widgets import Meter
from tkinter import Scale

style = Style('cosmo')
root = style.master
root.title('ttkbootstrap')

m1 = Meter(metersize=180, padding=20, amountused=25, metertype='semi', labeltext='miles per hour', interactive=True)
m1.grid(row=0, column=0)

m2 = Scale(root, from_=20, to=100, orient='horizontal', tickinterval=20, length=220,variable=15)
m2.grid(row=0, column=1)

root.mainloop()