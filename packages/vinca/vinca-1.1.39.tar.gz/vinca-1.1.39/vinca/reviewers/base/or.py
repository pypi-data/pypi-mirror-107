import tkinter as Tk
from subprocess import run

TERMINAL_BACKGROUND = '#000000'

class ActiveWindow:
    def __init__(self):
        # use xdotool to query basic information about the active terminal's geometry
        out = run(['xdotool','getactivewindow','getwindowgeometry'], capture_output=True)
        # parse the output
	# and calculate handy references to the
	# active terminal's geometry
        out = str(out.stdout, encoding='utf-8')
        window_id, abs_pos, geometry = out.splitlines()
        self.left, self.top = abs_pos.split()[1].split(',')
        self.left, self.top = int(self.left), int(self.top)
        self.width, self.height = geometry.split()[1].split('x')
        self.width, self.height = int(self.width), int(self.height)
        self.right = self.left + self.width
        self.bottom = self.top + self.height
        self.center_x = self.left + self.width // 2
        self.center_y = self.top + self.height // 2

class DisplayImage:
    '''A simple class to draw an image to the screen.
    There are two methods: show and close.'''
    def __init__(self, image_path):
        self.image_path = image_path

    def show(self):
	# get geometry information about the active terminal
        aw = ActiveWindow()

        self.root = Tk.Tk()

        self.image = Tk.PhotoImage(file=self.image_path)
	# warning: images cannot be stored as local variables
	# of a function or else there is risk of them being
	# destroyed by premature garbage collection.

	# we want to center the image at the bottom of the terminal
	# with a 40 pixel margin on all sides
	# if the image is too big we will only see part of it
	# but the window will fit inside the active terminal
        img_height = self.image.height()
        img_width = self.image.width()
        margin = 40
        left = max(aw.left + margin, aw.center_x - img_width // 2)
        right = min(aw.right - margin, aw.center_x + img_width // 2)
        width = right - left
        bottom = aw.bottom - margin
        top = max(aw.top + margin, bottom - img_height)
        height = bottom - top
        self.root.geometry(f'{width}x{height}+{left}+{top}')

	# we want to draw the window
	# we do not want to let the window manager make decisions
        self.root.overrideredirect(True)

	# draw the image on a canvas
	# place our canvas to occupy the whole window
        self.canvas = Tk.Canvas(self.root, width=width, height=height)
        self.canvas.config(bg=TERMINAL_BACKGROUND)
        self.canvas.create_image(0,0, anchor=Tk.NW, image=self.image)
        self.canvas.place(x=-1,y=-1, height=height+2, width=width+2)

	# draw our window to the screen
        self.root.update()

	# (it is more common to see root.mainloop called
	#  to draw the window, but we choose to do the
	#  update call manually because there is no user
	#  interaction with the window.)

    def close(self):
        assert self.root
        self.root.destroy()

