import tkinter as tk
from collections import defaultdict


class LifeGame:
	def __init__(self):

		self.__root = tk.Tk()
		self.__x = 27
		self.__y = 27
		self.color_off = 'SystemButtonFace'
		self.color_on = 'blue'
		self.__buttons = defaultdict(list)
		self.pattern = list()
		self.state = {0: self.color_off, 1: self.color_off, 3: self.color_on}
		self.cell_range = [-1, 0, 1]
		self.start = False

	def init_grid(self):

		main_frame = tk.Frame(self.__root, height=(self.__x + 2))
		frame_grids = tk.Frame(main_frame, height=self.__x, width=(2 * self.__y))
		frame_done = tk.Frame(main_frame)
		tk.Button(frame_done, text='Play Simulation', command=self.live).grid(row=self.__x + 2,
																			  column=int(self.__y / 2))

		tk.Button(frame_done, text='Stop Simulation', command=self.stop).grid(row=self.__x + 2,
																			  column=int(self.__y / 2) + 6)

		frame_grids.grid()
		frame_done.grid()
		main_frame.grid()

		for i in range(self.__x):
			for j in range(self.__y):
				button = tk.Button(frame_grids, height=1, width=2,
								   command=lambda x=i, y=j: self.change_n_update(x, y))

				button.grid(row=i, column=j)
				self.__buttons[i].append(button)

		for i in range(self.__x):
			for j in range(self.__y):
				self.__buttons[i][j].configure(bg='blue')

		self.play_life()

		for i in range(self.__x):
			for j in range(self.__y):
				print(self.__buttons[i][j].cget('bg'))

		frame_grids.mainloop()

	def stop(self):
		self.start = False

	def live(self):
		self.start = True

		while self.start:
			self.__root.update()
			self.play_life()

	def change_n_update(self, x, y):

		self.pattern.append([x, y])
		self.__buttons[x][y].configure(bg=self.color_on)

	def play_life(self):

		checked = {}
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

				checked.update({str(i) + str(j): {'n': neigh, 'x': i, 'y': j}})

		for _ in checked:

			if checked[_]['n'] > 3:
				self.__buttons[checked[_]['x']][checked[_]['y']].configure(bg=self.color_off)

			elif checked[_]['n'] != 2:
				self.__buttons[checked[_]['x']][checked[_]['y']].configure(bg=self.state[checked[_]['n']])

		print(checked)


g = LifeGame()
g.init_grid()
