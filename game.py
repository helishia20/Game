
import curses
import random
import time
food_num = 10
food_age = 500
player_char = '☹'
enemy_char = '☠'
food_emoji = "♡"
happ_gage = "☘"
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)
curses.curs_set(False)

maxl = curses.LINES - 1
maxc = curses.COLS - 1

world = []
player_l = player_c = 0
food = []
enemy = []
score = 0


def random_palce():
    a = random.randint(0, maxl)
    b = random.randint(0, maxc)
    while world[a][b] != ' ':
        a = random.randint(0, maxl)
        b = random.randint(0, maxc)
    return a, b


def check_food():
    global score
    for i in range(len(food)):
        fl, fc, fa = food[i]
        fa -= 1
        if fl == player_l and fc == player_c:
            score += 10
            fl, fc = random_palce()
            fa = random.randint(food_age, food_age*3)
        if fa <= 0:
            fl, fc = random_palce()
            fa = random.randint(food_age, food_age*3)
        food[i] = (fl, fc, fa)


def move_enemy():
    global playing
    for i in range(len(enemy)):
        el, ec = enemy[i]
        if random.random() > 0.7:
            if el > player_l:
                el -= 1
        if random.random() > 0.7:
            if ec > player_c:
                ec -= 1
        if random.random() > 0.7:
            if el < player_l:
                el += 1
        if random.random() > 0.7:
            if ec < player_c:
                ec += 1
            el = in_range(el, 0, maxl)
            ec = in_range(ec, 0, maxc)
            enemy[i] = (el, ec)
            time.sleep(0.07)
        if el == player_l and ec == player_c:
            stdscr.addstr(maxl//2, maxc//2, "YOU DIED!")
            stdscr.refresh()
            time.sleep(3)
            playing = False


def init():
    global player_c, player_l
    for i in range(-1, maxl + 1):
        world.append([])
        for j in range(-1, maxc + 1):
            world[i].append(' ' if random.random() > 0.03 else '.')
    for i in range(10):
        fl, fc = random_palce()
        fa = random.randint(1000, 10000)
        food.append((fl, fc, fa))
    for i in range(3):
        el, ec = random_palce()
        enemy.append((el, ec))
    player_l, player_c = random_palce()


def in_range(a, min, max):
    if a > max:
        return max
    if a < min:
        return min
    return a


def draw():
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i, j, world[i][j])
    stdscr.addstr(1, 1, f"Score: {happ_gage}  {score}  {happ_gage}  ")
    # showing food
    for f in food:
        fl, fc, fa = f
        stdscr.addch(fl, fc, food_emoji)
    # showing enemy
    for e in enemy:
        el, ec = e
        stdscr.addch(el, ec, enemy_char)
    # showing palyer
    stdscr.addch(player_l, player_c, player_char)
    stdscr.refresh()


def move(c):
    global player_l, player_c
    if c == 'w' and world[player_l - 1][player_c] != '.':
        player_l -= 1
    elif c == 's' and world[player_l + 1][player_c] != '.':
        player_l += 1
    elif c == 'd' and world[player_l][player_c + 1] != '.':
        player_c += 1
    elif c == 'a' and world[player_l][player_c - 1] != '.':
        player_c -= 1
    player_l = in_range(player_l, 0, maxl - 1)
    player_c = in_range(player_c, 0, maxc - 1)


init()
playing = True
while playing:
    try:
        c = stdscr.getkey()
    except:
        c = ''
    if c in ['a', 's', 'd', 'w']:
        move(c)
    elif c == 'q':
        playing = False
    check_food()
    move_enemy()
    draw()
stdscr.addstr(maxl//2, maxc//2, "THANKS FOR PLAYING!")
stdscr.refresh()
time.sleep(2)
stdscr.clear()
stdscr.refresh()
