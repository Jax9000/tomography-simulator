import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

from skimage.io import imread

def start():
    root = Tk.Tk()
    root.wm_title("Embedding in TK")

    f = Figure(figsize=(5, 4), dpi=100)
    a = f.add_subplot(122)
    t = arange(0.0, 3.0, 0.01)
    s = sin(2*pi*t)

    image = imread("./test02.png")
    a.imshow(image)


    # a tk.DrawingArea
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    def on_key_event(event):
        print('you pressed %s' % event.key)
        image0 = imread("./test.png")
        a.imshow(image0)
        canvas.draw()

    canvas.mpl_connect('key_press_event', on_key_event)

    def _quit():
        root.quit()  # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    button = Tk.Button(master=root, text='Quit', command=_quit)
    button.pack(side=Tk.BOTTOM)

    w = Tk.Scale(root, from_=0, to=100, orient=Tk.HORIZONTAL)
    w.pack(side="right");

    w = Tk.Scale(root, from_=0, to=100, orient=Tk.HORIZONTAL)
    w.pack(side="left");

    Tk.mainloop()
    # If you put root.destroy() here, it will cause an error if
    # the window is closed with the window manager.
