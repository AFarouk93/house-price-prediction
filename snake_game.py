import curses
from random import randint


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh-3, sw-3]]

    # draw border
    for x in range(box[0][1], box[1][1]):
        stdscr.addch(box[0][0], x, '#')
        stdscr.addch(box[1][0], x, '#')
    for y in range(box[0][0], box[1][0]):
        stdscr.addch(y, box[0][1], '#')
        stdscr.addch(y, box[1][1], '#')

    snake = [
        [sh//2, sw//2 + 1],
        [sh//2, sw//2],
        [sh//2, sw//2 - 1],
    ]
    direction = curses.KEY_RIGHT

    food = [randint(box[0][0]+1, box[1][0]-1),
            randint(box[0][1]+1, box[1][1]-1)]
    stdscr.addch(food[0], food[1], '*')

    while True:
        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            direction = key

        head = snake[0].copy()
        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        if (head[0] in [box[0][0], box[1][0]] or
                head[1] in [box[0][1], box[1][1]] or
                head in snake):
            msg = "Game Over! Press any key to exit"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.nodelay(False)
            stdscr.getch()
            break

        snake.insert(0, head)
        if head == food:
            while True:
                food = [randint(box[0][0]+1, box[1][0]-1),
                        randint(box[0][1]+1, box[1][1]-1)]
                if food not in snake:
                    break
            stdscr.addch(food[0], food[1], '*')
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        stdscr.addch(head[0], head[1], '#')
        stdscr.refresh()
        curses.napms(100)


if __name__ == '__main__':
    curses.wrapper(main)

