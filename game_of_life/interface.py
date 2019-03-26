import tkinter as tk
from collections import defaultdict
import time


class LifeGame:
	def __init__(self, dim_x=25, dim_y=25):

		self.x = dim_x
		self.y = dim_y
		self.color_off = 'SystemButtonFace'
		self.color_on = 'blue'
		self.root = tk.Tk()
		self.buttons = defaultdict(list)
		self.pattern = list()
		self.state = {0: self.color_off, 1: self.color_off, 2: self.color_on, 3: self.color_on}
		self.cell_range = [-1, 0, 1]

	def init_grid(self):
		main_frame = tk.Frame(self.root, width=25, height=25)
		frame_grids = tk.Frame(main_frame)
		frame_done = tk.Frame(main_frame)

		main_frame.pack()
		frame_grids.pack()
		frame_done.pack()

		for i in range(self.x):
			for j in range(self.y):
				button = tk.Button(frame_grids, height=1, width=2,
								   command=lambda x=i, y=j: self.change_n_update(x, y))

				button.grid(row=i, column=j)
				self.buttons[i].append(button)

		tk.Button(frame_done, text='Play Simulation', command=self.play_life).grid(row=self.x + 2,
																				   column=int(self.x / 2))

		main_frame.mainloop()

	def change_n_update(self, x, y):

		self.pattern.append([x, y])
		self.buttons[x][y].configure(bg=self.color_on)

	def play_life(self):

		checked = {}

		for i in range(self.x):

			for j in range(self.y):
				neigh = 0

				for x in self.cell_range:

					if 0 <= (i + x) < self.x:
						row = i + x
					else:
						continue

					for y in self.cell_range:

						if 0 <= (j + y) < self.y:
							column = j + y
						else:
							continue

						if row == i and column == j:
							continue

						if self.buttons[row][column]['bg'] == self.color_on:
							neigh += 1

				checked.update({str(i) + str(j): {'n': neigh, 'x': i, 'y': j}})

			for _ in checked:
				if checked[_]['n'] not in list(self.state):
					self.buttons[checked[_]['x']][checked[_]['y']].configure(bg=self.color_off)
				else:
					print(checked[_])

					self.buttons[checked[_]['x']][checked[_]['y']].configure(bg=self.state[checked[_]['n']])


g = LifeGame(25, 25)
g.init_grid()
