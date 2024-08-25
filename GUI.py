import tkinter as tk
from main import Game


def lounch(table: list):
    score: tuple

    game = Game(int(scale_lvl_choose.get()))
    score = game.start()
    score = (name.get(), score[0], score[1])

    sort(table, score)


def sort(table: list, score: tuple):
    for index, player in enumerate(table):
        if player == '':
            table[index] = score
            break
        else:
            if player[2] > score[2]:
                table.insert(index, score)
                break


def write_score(player) -> str:
    ans: str = ''
    if type(player) == tuple:
        try:
            ans = f'{player[0]} lvl:{player[1]} time: {player[2]}'
        except:
            ans = 'Error'

    return ans


def write_table() -> list:
    score_board = []
    for i in range(5):
        score_board.append(tk.Message(win, text=f'{i + 1}', width=200, relief='sunken'))

    for i, p in enumerate(score_board):
        p.grid(row=i + 1, column=3)

    return score_board


# te dwie funkcajie da się ogarnąć bo robią prawie to samo

def update_table():
    for i in range(len(board)):
        board[i].destroy()
        board[i] = tk.Message(win, text=write_score(player=players[i]), width=200, relief='sunken')
    for i, p in enumerate(board):
        p.grid(row=i + 1, column=3)


players: list = []
board: list

for i in range(5):
    players.append('')

win = tk.Tk()
win.title('POP Baloon')
win.geometry('500x220')

button_play = tk.Button(win, text='Play', width=10, height=2, command=lambda: lounch(table=players))
button_refresh = tk.Button(win, text='Refresh', width=5, height=1, command=update_table)  # update_table()
scale_lvl_choose = tk.Scale(win, from_=0, to=4, orient='horizontal', length=150)

name = tk.Entry(win, width=20)

# ustawianie przycisków
msg_easy = tk.Message(win, text='Noob', width=40, font=('Arial', 10))
msg_hard = tk.Message(win, text='God', font=('Arial', 10))
head = tk.Message(win, text='How good are You?', width=150, font=('Arial', 12))
name_msg = tk.Message(win, text='Enter your nick', width=150, font=('Arial', 11))
space = tk.Message(win, text=' ')
board_msg = tk.Message(win, text='Score Table', width=100, font=('Arial', 12))
'''player1 = tk.Message(win, text='Karol lvl.0 time: 2.463 sec', width=200, relief='sunken')
player2 = tk.Message(win, text=write_score(players, 2), width=200, relief='sunken')
player3 = tk.Message(win, text=write_score(players, 3), width=200, relief='sunken')
player4 = tk.Message(win, text=write_score(players, 4), width=200, relief='sunken')
player5 = tk.Message(win, text=write_score(players, 5), width=200, relief='sunken')
'''

# ustanie i alokacja tabeli
board = write_table()

# alokacja przycisków
head.grid(row=0, column=1)
msg_hard.grid(row=1, column=2)
msg_easy.grid(row=1, column=0)
scale_lvl_choose.grid(row=1, column=1)
button_play.grid(row=5, column=1)
name.grid(row=4, column=1)
name_msg.grid(row=3, column=1)
space.grid(row=2, column=0)
board_msg.grid(row=0, column=3, ipadx=90)
button_refresh.grid(row=6, column=3)
'''player1.grid(row=1, column=3)
player2.grid(row=2, column=3)'''

win.mainloop()
