from tkinter import *
import math
import threading
from pydub import AudioSegment
from pydub.playback import play
from PIL import ImageTk
from PIL import Image


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "LightPink1"
RED = "palevioletred3"
GREEN = "LightSteelBlue1"

YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
FONT = ("Arial", 13, "normal")
FONT_TIMER = ("Courier", 50, "bold")
FONT_CHECK = ("Courier", 16, "bold")
FONT_BUTTON = ("Courier", 14, "bold")
FONT_RESET = ("Courier", 50, "bold")
FONT_LONG_BREAK = ("Courier", 35, "bold")

FONT_BUTTONS = ("Courier", 18, "bold")

x_coordinate = 35
check_image_counter = 0
check_images = []
# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global timer
    global x_coordinate
    global check_image_counter

    # Reset x_coordinate and check_image_counter
    x_coordinate = 35
    check_image_counter = 0
    canvas.coords(image_item, 328, 275)

    def reset_sound():
        play_sound('2.wav')

    window.after_cancel(timer)

    new_img = Image.open("bg2.png").resize((1280, 555))
    canvas.new_photo = ImageTk.PhotoImage(new_img)
    canvas.itemconfigure(bg_canvas, image=canvas.new_photo)

    canvas.coords(timer_text, 328, 380)
    canvas.itemconfigure(timer_text, fill="white")
    canvas.itemconfig(timer_text, text="00:00")
    canvas.itemconfig(timer_text, font=FONT_RESET)
    canvas.new_img = PhotoImage(file="green-totoro.png")
    canvas.itemconfig(image_item, image=canvas.new_img)
    canvas.itemconfig(timer_word, text="Timer", fill=GREEN)
    canvas.coords(timer_word, 650, 135)
    check_images.clear()

    t = threading.Thread(target=reset_sound)
    t.start()

    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def play_sound(sound_file):
    audio = AudioSegment.from_file(sound_file, format='wav')
    play(audio)


def start_timer():
    def break_sound():
        play_sound('break.wav')

    def work_sound():
        play_sound('work.wav')

    global reps

    if reps == 0:
        add_image()
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    canvas.itemconfig(timer_text, font=FONT_TIMER)

    if reps % 8 == 0:
        new_img = Image.open("long-break-bg.png").resize((1280, 555))
        canvas.new_photo = ImageTk.PhotoImage(new_img)
        canvas.itemconfigure(bg_canvas, image=canvas.new_photo)

        canvas.new_img = PhotoImage(file="Totoro-break1.png")
        canvas.coords(timer_text, 430, 330)
        canvas.itemconfig(image_item, image=canvas.new_img)
        canvas.coords(image_item, 390, 280)
        canvas.itemconfig(timer_text, font=FONT_LONG_BREAK)
        canvas.itemconfigure(timer_text, fill="white")

        t = threading.Thread(target=break_sound)
        t.start()

        count_down(long_break_sec)

        canvas.itemconfig(timer_word, text="Break", fill=RED, font=FONT_TIMER)
        canvas.coords(timer_word, 750, 120)
    elif reps % 2 == 0:
        new_img = Image.open("short-break-bg.png").resize((1280, 555))
        canvas.new_photo = ImageTk.PhotoImage(new_img)
        canvas.itemconfigure(bg_canvas, image=canvas.new_photo)

        canvas.coords(timer_text, 360, 240)
        canvas.itemconfigure(timer_text, fill=PINK)
        canvas.new_img = PhotoImage(file="break-totoro.png")
        canvas.itemconfig(image_item, image=canvas.new_img)

        t = threading.Thread(target=break_sound)
        t.start()

        count_down(short_break_sec)

        canvas.itemconfig(timer_word, text="Break", fill=PINK, font=FONT_TIMER)
        canvas.coords(timer_word, 650, 135)

    else:
        t = threading.Thread(target=work_sound)
        t.start()

        new_img = Image.open("bg.png").resize((1280, 555))
        canvas.new_photo = ImageTk.PhotoImage(new_img)
        canvas.itemconfigure(bg_canvas, image=canvas.new_photo)

        canvas.coords(image_item, 328, 275)
        canvas.coords(timer_text, 328, 400)
        canvas.itemconfigure(timer_text, fill="white")
        canvas.new_img = PhotoImage(file="Totoro.png")
        canvas.itemconfig(timer_text, font=FONT_TIMER)
        canvas.itemconfig(image_item, image=canvas.new_img)
        count_down(work_sec)
        canvas.itemconfig(timer_word, text="Work", fill=GREEN, font=FONT_TIMER)
        canvas.coords(timer_word, 560, 80)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def add_image():
    global x_coordinate
    global check_images
    global check_image_counter

    check_img = PhotoImage(file="check-totoro.png").subsample(3)
    # Create the PhotoImage object and add it to the list
    check_images.append(check_img)

    # Increment the counter
    check_image_counter += 1
    # Check if the counter is greater than 0 before adding a new image
    if check_image_counter > 1:
        return

    # Create a new image and position it to the right of the previous one
    check_image_item = canvas.create_image(x_coordinate, 595, image=check_img)
    x_coordinate += 30

    # Return the image item ID
    return check_image_item


def count_down(count):
    global check_image_counter

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        if canvas.itemcget(timer_word, "text") == "Work":
            work_sessions = math.floor(reps / 2)
            for i in range(work_sessions):
                add_image()
        start_timer()

        # Reset the check_image_counter
        check_image_counter = 0


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Totoro-Pomodoro")
window.geometry("1055x755")

bg_image = Image.open("bg1.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label with the background image
bg_label = Label(image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0)

canvas = Canvas(window, width=955, height=650, highlightthickness=0,  bd=0)

# -------------------------- Canvas BG ---------------------------------------------------------------------
img1 = (Image.open("check-path.jpg"))
resized_image1 = img1.resize((1380, 1000))
new_image1 = ImageTk.PhotoImage(resized_image1)
bg_bottom_canvas = canvas.create_image(0, -340, anchor=NW, image=new_image1)

img = (Image.open("bg.jpg"))
resized_image = img.resize((1280, 555))
new_image = ImageTk.PhotoImage(resized_image)
bg_canvas = canvas.create_image(0, 0, anchor=NW, image=new_image)

# -------------------------------------------------------------------------------------------------------------

totoro_img = PhotoImage(file="Totoro.png")
image_item = canvas.create_image(328, 275, image=totoro_img)
canvas.place(x=50, y=50)

timer_word = canvas.create_text(560, 80, text="Timer", fill=GREEN, font=FONT_TIMER)
timer_text = canvas.create_text(328, 400, text="00:00", fill="white", font=(FONT_NAME, 45, "bold"))

start_img = PhotoImage(file="start-button.png")
start_img = start_img.subsample(4)

start_button = Button(window, image=start_img, highlightthickness=0, bd=0,   command=start_timer, anchor='n',
                      activebackground="green", bg="yellow green")

start_button_window = canvas.create_window(660, 640, anchor='sw', window=start_button)

reset_img = PhotoImage(file="reset-button.png")
reset_img = reset_img.subsample(4)
reset_button = Button(image=reset_img, highlightthickness=0, bd=0, command=reset_timer, anchor='n',
                      activebackground="green", bg="yellow green")

reset_button_window = canvas.create_window(935, 640, anchor='se', window=reset_button)

window.mainloop()
