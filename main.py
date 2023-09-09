import tkinter as tk
import random, time, asyncio

from tkinter import messagebox

class Memorizer:
	def __init__(self, master):
		self.master = master
		self.rows = 4
		self.cols = 5
		self.player1 = 0
		self.player2 = 0
		self.turn = "Player 1"
		self.selection = False
		self.selected = []
		self.board = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
		self.board_satus = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

		self.create_cards_order()
		self.create_widgets()

	def create_cards_order(self):
		cards = ["♩", "♪", "♫", "♬", "♭", "♮", "♯", "ø", "≠", "≭"]
		cards = cards+cards
		cards = random.sample(cards, len(cards))

		card = 0
		for i in range(self.rows):
			for j in range(self.cols):
				self.board[i][j] = cards[card]
				card = card+1

	def create_widgets(self):
		self.frame = tk.Frame(self.master)
		self.frame.pack()

		self.buttons = []
		
		for i in range(self.rows):
			row = []
			for j in range(self.cols):
				btn = tk.Button(
					self.frame, width=4, height=2,
					command=lambda x=i, y=j: self.on_button_click(x, y)
				)
				btn.grid(row=i, column=j)
				row.append(btn)
			self.buttons.append(row)

		self.show_turn = tk.Label(self.frame, text="Turn of: Player 1", font = ('default', 10, 'bold'))
		self.show_turn.grid(row=4, column=0, columnspan=5, sticky='we')

		self.player1_hits = tk.Label(self.frame, text="Player 1: 0")
		self.player1_hits.grid(row=5, column=0, columnspan=2, sticky='we')

		self.player2_hits = tk.Label(self.frame, text="Player 2: 0")
		self.player2_hits.grid(row=5, column=3, columnspan=2, sticky='we')

	def on_button_click(self, row, col):
		if self.board_satus[row][col] == 0:
			self.board_satus[row][col] = 2
			self.buttons[row][col].config(text=self.board[row][col])
			
			if self.selection:
				for i in range(self.rows):
					card1 = self.board_satus[i].index(2) if 2 in self.board_satus[i] else None
					card2 = self.board_satus[i].index(3) if 3 in self.board_satus[i] else None
					
					if card1 or card1 == 0:
						self.selected.append([i, card1, self.board[i][card1]])

					if card2 or card2 == 0:
						self.selected.append([i, card2, self.board[i][card2]])

				self.analyze_selections()
			else:
				self.board_satus[row][col] = 3
				self.selection = True

		if self.check_win():
			if self.player1 == self.player2:
				self.show_message('Losers! There was a draw!')
			elif self.player1 >= self.player2:
				self.show_message('Congratulations! The winner is Player 1!')
			else:
				self.show_message('Congratulations! The winner is Player 2!')
			self.restart_game()

	def analyze_selections(self):
		if self.selected[0][2] == self.selected[1][2]:
			for item in self.selected:
				self.board_satus[item[0]][item[1]] = 1

			if self.turn == "Player 1":
				self.player1 = self.player1+1
				self.player1_hits.config(text=f"Player 1: {self.player1}")
			else:
				self.player2 = self.player2+1
				self.player2_hits.config(text=f"Player 2: {self.player2}")

			self.selection = False
			self.selected = []
		else:
			if self.turn == "Player 1":
				self.turn = "Player 2"
			else:
				self.turn = "Player 1"

			self.show_turn.config(text=f"Turn of: {self.turn}")
			self.master.after(750, self.remove_elements)

	def remove_elements(self):
		for item in self.selected:
			self.board_satus[item[0]][item[1]] = 0
			self.buttons[item[0]][item[1]].config(text=" ")
		self.selection = False
		self.selected = []

	def check_win(self):
		for row in range(self.rows):
			for col in range(self.cols):
				if self.board_satus[row][col] != 1:
					return False
		return True

	def restart_game(self):
		self.player1 = 0
		self.player2 = 0
		self.turn = "Player 1"
		self.selection = False
		self.selected = []
		self.create_cards_order()
		self.board_satus = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

		for row in range(self.rows):
			for col in range(self.cols):
				self.buttons[row][col].config(text=" ")

		self.show_turn.config(text="Turn of: Player 1")
		self.player1_hits.config(text="Player 1: 0")
		self.player2_hits.config(text="Player 2: 0")

	def show_message(self, message):
		messagebox.showinfo('Game Over', message)


if __name__ == '__main__':
	root = tk.Tk()
	root.title('Memorizer')
	root.resizable(False, False)
	game = Memorizer(root)
	root.mainloop()