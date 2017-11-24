# "Stopwatch: The Game"
import simplegui

# define global variables
counter = 0
x = 0
y = 0
timer_running = False


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    mins = str(counter / 600)
    if (counter % 600) / 10 < 10:
        secs = "0" + str((counter % 600) / 10)
    else:
        secs = str((counter % 600) / 10)
    tenths = str(counter % 10)
    format_t = mins + ":" + secs + "." + tenths
    return format_t


# define event handlers for buttons; "Start", "Stop", "Reset"
def Start():
    global counter, timer_running
    timer.start()
    timer_running = True


def Stop():
    global counter, x, y, timer_running
    timer.stop()
    if timer_running == True:
        y += 1
        if (counter % 10) == 0:
            x += 1
    timer_running = False


def Reset():
    global counter, x, y, timer_running
    counter = 0
    timer.stop()
    timer_running = False
    x = 0
    y = 0


# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    counter += 1


# define draw handler
def draw_handler(frame):
    global counter
    frame.draw_text(format(counter), [50, 100], 28, "White")
    frame.draw_text(str(x) + "/" + str(y), [150, 25], 24, "Green")


# create frame
frame = simplegui.create_frame("Timer", 200, 200)
timer = simplegui.create_timer(100, tick)

# register event handlers
frame.add_button("Start", Start)
frame.add_button("Stop", Stop)
frame.add_button("Reset", Reset)

# start frame
frame.start()
frame.set_draw_handler(draw_handler)