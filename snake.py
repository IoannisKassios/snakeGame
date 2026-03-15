import curses
import random

score = 0
high_score = 0

def main(stdscr):
    global score, high_score

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()

    # snake starts in the middle
    snake = [[sh//2, sw//2], [sh//2, sw//2 - 1], [sh//2, sw//2 - 2]]
    direction = curses.KEY_RIGHT

    # place food randomly
    food = [random.randint(2, sh-2), random.randint(2, sw-2)]

    while True:

        if direction in (curses.KEY_UP, curses.KEY_DOWN):
            stdscr.timeout(200)
        else:
            stdscr.timeout(100)

        stdscr.border()
        stdscr.addstr(0, 2, " Score: " + str(score) + "  Best: " + str(high_score) + " ")
        stdscr.addch(food[0], food[1], "*")

        key = stdscr.getch()

        if key == ord('q'):
            break
        if key == curses.KEY_UP and direction != curses.KEY_DOWN:
            direction = key
        if key == curses.KEY_DOWN and direction != curses.KEY_UP:
            direction = key
        if key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
            direction = key
        if key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
            direction = key

        # calculate next head position
        head = snake[0].copy()
        if direction == curses.KEY_UP:    head[0] -= 1
        if direction == curses.KEY_DOWN:  head[0] += 1
        if direction == curses.KEY_LEFT:  head[1] -= 1
        if direction == curses.KEY_RIGHT: head[1] += 1

        # hit wall or yourself = game over
        if head[0] <= 0 or head[0] >= sh-1 or head[1] <= 0 or head[1] >= sw-1:
            break
        if head in snake:
            break

        snake.insert(0, head)

        if head == food:
            score += 10
            if score > high_score:
                high_score = score
            food = [random.randint(2, sh-2), random.randint(2, sw-2)]
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], " ")

        stdscr.addch(snake[0][0], snake[0][1], "#")
        stdscr.refresh()

    # game over
    stdscr.addstr(sh//2,   sw//2 - 4, "GAME OVER")
    stdscr.addstr(sh//2+1, sw//2 - 5, "score: " + str(score))
    stdscr.addstr(sh//2+2, sw//2 - 8, "press any key to exit")
    stdscr.nodelay(0)
    stdscr.getch()

curses.wrapper(main)