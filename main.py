from tkinter import *
import time
import random
from functools import partial

root = Tk()
root.title('MinerThing')
root.geometry("269x45+669+420")
root.resizable(False, False)

start_Button = Button(root, text="►Start")
back_Button = Button(root, text="Back")
redderButton = Button(root, width=0, height=0, bg='red')


def StartEasy():
    try:
        global GameOver
        GameOver.destroy()
    except:
        pass
    try:
        global YouWon
        YouWon.destroy()
    except:
        pass
    GameOver = Label(root, text='GameOver', font='50')
    YouWon = Label(root, text='YouWon!!', font='50')
    root.geometry("269x310")
    start_Button.configure(text='restart')
    back_Button.place(x=220, y=5)
    root.update()
    time.sleep(0.05)



    # settings
    global failed
    global redding_on
    redding_on = False
    red_buttons = []
    failed = False
    won = False
    x_gameBttn_pos = 10
    y_gameBttn_pos = 50
    buttons_per_row = 10
    number_of_buttons = 100
    plus_or_square = True   # True for Square, False for Plus

    # makes random values for the game
    # makes dicts
    button_values = []
    already_done = []
    for v in range(0, int(number_of_buttons/buttons_per_row)):
        button_values.append([])
    q = buttons_per_row
    t = 0
    for v in range(0, number_of_buttons):
        if v == q:
            q = q + buttons_per_row
            t = t + 1
        button_values[t].append('')
        already_done.append('')
    # makes Bombs
    alreadydone = []
    for v in range(0, 10):
        t = 0
        x = random.randrange(0, number_of_buttons)
        exist = True
        while exist:
            if x in alreadydone:
                x = random.random(0, number_of_buttons)
                exist = True
            else:
                alreadydone.append(str(x))
                while x >= buttons_per_row:
                    x = x - buttons_per_row
                    t = t + 1
                exist = False

        button_values[t][x] = '💣'
    # sets value based on Bombs
    num_of_neighbor_bombs = 0
    value = ''
    q = buttons_per_row
    t = 0
    r = buttons_per_row
    j = 0
    for v in range(0, number_of_buttons):
        if v == r:
            t = t + 1
            r = r + buttons_per_row
            j = j + buttons_per_row
        value = '💣'
        if not button_values[t][v-j] == '💣':
            num_of_neighbor_bombs = 0
            try:
                if button_values[t][v-1-j] == '💣' and v-1-j >= 0:
                    num_of_neighbor_bombs = num_of_neighbor_bombs + 1
            except:
                pass
            try:
                if button_values[t][v+1-j] == '💣' and v+1-j >= 0:
                    num_of_neighbor_bombs = num_of_neighbor_bombs + 1
            except:
                pass
            try:
                if button_values[t-1][v-j] == '💣' and v-j >= 0 and t-1 >= 0:
                    num_of_neighbor_bombs = num_of_neighbor_bombs + 1
            except:
                pass
            try:
                if button_values[t+1][v-j] == '💣' and v-j >= 0 and t+1 <= number_of_buttons/buttons_per_row:
                    num_of_neighbor_bombs = num_of_neighbor_bombs + 1
            except:
                pass
            if plus_or_square:
                try:
                    if button_values[t+1][v+1-j] == '💣' and v+1-j >= 0 and t+1 <= number_of_buttons/buttons_per_row:
                        num_of_neighbor_bombs = num_of_neighbor_bombs + 1
                except:
                    pass
                try:
                    if button_values[t+1][v-1-j] == '💣' and v-1-j >= 0 and t+1 <= number_of_buttons/buttons_per_row:
                        num_of_neighbor_bombs = num_of_neighbor_bombs + 1
                except:
                    pass
                try:
                    if button_values[t-1][v+1-j] == '💣' and v+1-j >= 0 and t-1 >= 0:
                        num_of_neighbor_bombs = num_of_neighbor_bombs + 1
                except:
                    pass
                try:
                    if button_values[t-1][v-1-j] == '💣' and v-1-j >= 0 and t-1 >= 0:
                        num_of_neighbor_bombs = num_of_neighbor_bombs + 1
                except:
                    pass
            if v - 1 == q:
                q = q + buttons_per_row
            value = str(num_of_neighbor_bombs)
            if value == '0':
                value = '•'
        button_values[t][v-j] = value

    swi = []
    alreadydone = set(alreadydone)
    alreadydone = list(alreadydone)

    for v in range(0, number_of_buttons):
        swi.append('')
    for v in range(0, len(alreadydone)):
        swi[int(alreadydone[v])] = '💣'
    already_done = swi

    # Pressing event!
    def press(button):
        r = button
        t = 0
        while r >= buttons_per_row:
            r = r - buttons_per_row
            t = t + 1

        global redding_on

        if redding_on:
            if str(button) in red_buttons:
                gameBttnsDict[button].configure(bg='#d0d0d0')
                red_buttons.remove(str(button))
                root.configure(cursor='')
                redding_on = False
            else:
                red_buttons.append(str(button))
                gameBttnsDict[button].configure(bg='red')
                root.configure(cursor='')
                redding_on = False

        elif str(button) not in red_buttons:
            global failed
            if not failed:
                gameBttnsDict[button].configure(text=button_values[t][r],  height=1, width=2)
            if button_values[t][r] == '💣':
                GameOver.place(x=buttons_per_row*20/2, y=15)
                failed = True
            else:
                already_done[button] = 'done'
                if len(set(already_done)) == 2 and not failed:
                    YouWon.place(x=buttons_per_row*20/2, y=15)
                    global won
                    won = True


    # make all the buttons!!
    gameBttnsDict = {}
    Mekadem = 0
    for b in range(0, number_of_buttons):
        gameBttnsDict[b] = Button(root, text="", height=1, width=2, bg='#d0d0d0', command=partial(press, b))
        gameBttnsDict[b].place(x=x_gameBttn_pos, y=y_gameBttn_pos)
        x_gameBttn_pos = x_gameBttn_pos + 25
        if b == buttons_per_row - 1 + buttons_per_row * Mekadem:
            Mekadem = Mekadem + 1
            x_gameBttn_pos = 10
            y_gameBttn_pos = y_gameBttn_pos + 25

    def redding():
        root.configure(cursor='fleur')
        global redding_on
        redding_on = True

    redderButton.config(command=redding)
    redderButton.place(x=205, y=5)

def back():
    root.geometry("269x45+669+420")
    start_Button.configure(text="►Start")
    back_Button.place_forget()
    redderButton.place_forget()
    try:
        GameOver.destroy()
        YouWon.destroy()
    except:
        pass


start_Button.configure(command=StartEasy)
back_Button.configure(command=back)
start_Button.place(x=5, y=5)

root.mainloop()



# things to add - a button that makes all UnClear buttons Yellow, help section before start, custom size.
# a button that reveals all tiles but makes you lose