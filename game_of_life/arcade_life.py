import tkinter as tk
from collections import defaultdict

try:
	from tkinter import messagebox
except ImportError:
	from tkinter import tkMessageBox as messagebox


# clean the list when new uni : NO need?
class LifeGame:
	def __init__(self):

		self.__root = tk.Tk()
		self.__x = 27
		self.__y = 57
		self.__x_fixed = 27
		self.__y_fixed = 57
		self.color_off = 'SystemButtonFace'
		self.color_on = 'blue'
		self.__buttons = defaultdict(list)
		self.state = {0: self.color_off, 1: self.color_off, 3: self.color_on}
		self.cell_range = [-1, 0, 1]
		self.start = False
		self.universe_init = False
		self.__root.protocol('WM_DELETE_WINDOW', self.close_window)
		self.frame_grids = tk.Frame(self.__root, height=self.__x, width=(2 * self.__y))
		self.frame_grids.grid()
		self.frame_props = tk.Frame(self.__root)
		self.frame_props.grid()
		self.button_status = {True: 'green', False: 'red'}
		self.pause_play = tk.Button(self.frame_props, text='Play/Pause Simulation', bg='red', command=self.live)
		self.pause_play.grid(row=0, column=10)
		tk.Button(self.frame_props, text='Adjust Grid', bg='yellow', command=lambda: self.make_universe(True)).grid(
			row=0, column=15)
		self.config_universe = tk.Toplevel()
		self.config_universe.lift()

	def init_grid(self):

		for i in range(self.__x):
			for j in range(self.__y):
				button = tk.Button(self.frame_grids, height=1, width=2,
								   command=lambda x=i, y=j: self.change_n_update(x, y))

				button.grid(row=i, column=j)
				self.__buttons[i].append(button)

		self.__root.update()

	def make_universe(self, new_universe=False):

		if not self.universe_init:
			self.__root.withdraw()
			dialog = tk.Frame(self.config_universe)

			tk.Label(dialog, text='rows').grid(row=0, column=0)
			row = tk.Entry(dialog)
			row.grid(row=0, column=1)

			tk.Label(dialog, text='columns').grid(row=1, column=0)
			col = tk.Entry(dialog)
			col.grid(row=1, column=1)

			tk.Button(dialog, text='submit', command=lambda: self.update_grid(row.get(), col.get())).grid(row=2,
																										  column=0)

			dialog.grid()

		if new_universe:
			self.show_config()

	def update_grid(self, x, y):

		if x == '':
			x = self.__x

		if y == '':
			y = self.__y

		elif x == '' and y == '':
			y = self.__y
			x = self.__x

		x = int(x)
		y = int(y)

		if x < 1 or y < 1:
			messagebox.showerror('really?', 'The Size Must Be Atleast 1X1')
		elif x > self.__x_fixed or y > self.__y_fixed:
			messagebox.showerror('really??', f'The Size Must Be less than {self.__x_fixed}X{self.__y_fixed}')

		elif self.universe_init:

			self.pause_play.invoke()

			for i in range(self.__x):
				for j in range(self.__y):
					self.__buttons[i][j].destroy()

					self.frame_grids.update()

			self.__buttons = defaultdict(list)
			self.__x = x
			self.__y = y
			self.init_grid()

		else:

			self.__x = x
			self.__y = y
			self.show_root()
			self.init_grid()
			self.universe_init = True

		self.config_universe.withdraw()

	def show_root(self):

		self.__root.update()
		self.__root.deiconify()

	def show_config(self):
		self.config_universe.update()
		self.config_universe.deiconify()

	def check_clear(self):
		if self.frame_grids:
			self.pause_play.invoke()

	def play_life(self):

		checked = {}
		nums = 0
		for i in range(self.__x):

			for j in range(self.__y):
				neigh = 0

				for x in self.cell_range:

					if 0 <= (i + x) < self.__x:
						row = i + x
					else:
						continue

					for y in self.cell_range:

						if 0 <= (j + y) < self.__y:
							column = j + y
						else:
							continue

						if row == i and column == j:
							continue

						if self.__buttons[row][column]['bg'] == self.color_on:
							neigh += 1

				checked.update({nums: {'n': neigh, 'x': i, 'y': j}})
				nums += 1

		for _ in checked:

			if self.start is True:
				if checked[_]['n'] > 3:

					self.__buttons[checked[_]['x']][checked[_]['y']].configure(bg=self.color_off)

				elif checked[_]['n'] != 2:
					self.__buttons[checked[_]['x']][checked[_]['y']].configure(bg=self.state[checked[_]['n']])

	def close_window(self):

		self.pause_play.invoke()
		self.__root.destroy()

	def play(self):
		self.make_universe()
		self.__root.mainloop()

	def live(self):

		self.start = not self.start

		self.pause_play['bg'] = self.button_status[self.start]

		while self.start:
			self.play_life()
			self.frame_grids.update()

	def change_n_update(self, x, y):
		if self.__buttons[x][y]['bg'] == self.color_off:
			self.__buttons[x][y].configure(bg=self.color_on)
		else:
			self.__buttons[x][y].configure(bg=self.color_off)


g = LifeGame()
g.play()
