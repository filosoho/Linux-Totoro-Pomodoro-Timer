import os
import sys
from tkinter import *
import math
import threading
from PIL import ImageTk
from PIL import Image
import pygame

# Determine if we’re in a PyInstaller environment
if getattr(sys, 'frozen', False):
    # If we are, get the base directory using _MEIPASS
    base_dir = sys._MEIPASS
else:
    # If not, use the script’s directory (for development)
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize Pygame mixer
pygame.mixer.init()

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
volume_level = 1.0

is_timer_running = False
paused_time = 0
remaining_time = 0

current_session_type = "work"


# ---------------------------- TIMER CONTROL ------------------------------- #
def pause_timer():
    global is_timer_running, paused_time, remaining_time, current_session_type

    if is_timer_running:
        window.after_cancel(timer)
        paused_time = int(canvas.itemcget(timer_text, "text").split(':')[0]) * 60 + int(canvas.itemcget(timer_text, "text").split(':')[1])  # Store remaining time
        remaining_time = paused_time
        is_timer_running = False


def resume_timer():
    global is_timer_running, remaining_time
    if not is_timer_running:
        is_timer_running = True
        count_down(remaining_time)


def reset_timer_only():
    global timer
    if timer:  # Check if timer has a valid value before cancelling
        window.after_cancel(timer)  # Cancel the existing timer
    canvas.itemconfig(timer_text, text="00:00")  # Reset timer display
    timer = None


def reset_timer():
    global reps, timer, x_coordinate, check_image_counter, is_timer_running, current_session_type

    current_session_type = "reset"

    start_button.config(state=NORMAL)
    resume_timer_button.config(state=DISABLED)

    # Reset timer running status
    is_timer_running = False

    reps = 0
    x_coordinate = 35
    check_image_counter = 0
    canvas.coords(image_item, 328, 275)

    def reset_sound():
        play_sound(os.path.join(base_dir, "assets", "2.wav"))

    window.after_cancel(timer)

    new_img = Image.open(os.path.join(base_dir, "assets","bg2.png")).resize((
        1280,
                                                                     555))
    canvas.new_photo = ImageTk.PhotoImage(new_img)
    canvas.itemconfigure(bg_canvas, image=canvas.new_photo)
    canvas.coords(timer_text, 328, 380)
    canvas.itemconfigure(timer_text, fill="white")
    canvas.itemconfig(timer_text, text="00:00", font=FONT_RESET)
    canvas.new_img = PhotoImage(file=os.path.join(base_dir, "assets", "green-totoro.png"))
    canvas.itemconfig(image_item, image=canvas.new_img)
    canvas.itemconfig(timer_word, text="Timer", fill=GREEN)
    canvas.coords(timer_word, 650, 135)
    check_images.clear()

    t = threading.Thread(target=reset_sound)
    t.start()


# ---------------------------- SOUND CONTROLS ------------------------------- #
def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.set_volume(volume_level)
    pygame.mixer.music.play()


def pause_sound():
    pygame.mixer.music.pause()

def resume_sound():
    pygame.mixer.music.unpause()

def stop_sound():
    pygame.mixer.music.stop()


# ---------------------------- ADD IMAGE CHECK ------------------------------- #
def add_image():
    global x_coordinate, check_images, check_image_counter
    check_img = PhotoImage(file=os.path.join(base_dir, "assets", "check-totoro.png")).subsample(3)
    check_images.append(check_img)
    check_image_counter += 1
    if check_image_counter > 1:
        return
    check_image_item = canvas.create_image(x_coordinate, 595, image=check_img)
    x_coordinate += 30
    return check_image_item


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global check_image_counter, is_timer_running, remaining_time

    if count < 0:
        count = 0

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0 and is_timer_running:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        if is_timer_running:
            is_timer_running = False
            # Ensure it only runs if the timer was running
            if canvas.itemcget(timer_word, "text") == "Work":
                add_image()
            start_timer(count)
            check_image_counter = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer(work_duration):
    global reps, is_timer_running, current_session_type

    def work_sound():
        play_sound(os.path.join(base_dir, "assets", "work.wav"))

    start_button.config(state=DISABLED)
    resume_timer_button.config(state=NORMAL)

    try:
        work_duration = int(work_input.get()) if work_input.get() else WORK_MIN  # Use WORK_MIN if no input
        short_break_duration = int(
            short_break_input.get()) if short_break_input.get() else SHORT_BREAK_MIN  # Use SHORT_BREAK_MIN if no input
        long_break_duration = int(
            long_break_input.get()) if long_break_input.get() else LONG_BREAK_MIN  # Use LONG_BREAK_MIN if no input
    except ValueError:
        # If invalid input, use the default global values
        work_duration = WORK_MIN
        short_break_duration = SHORT_BREAK_MIN
        long_break_duration = LONG_BREAK_MIN

    # If the timer is currently on break, reset and start work session
    if current_session_type in ["short break", "long break", "break", "reset"]:
        reset_timer_only()
        if current_session_type == "reset":
            reps += 1
        current_session_type = "work"
        if reps == 0:
            add_image()
        is_timer_running = True
        work_sec = work_duration * 60
        t = threading.Thread(target=work_sound)
        t.start()

        new_img = Image.open(os.path.join(base_dir, "assets", "bg.png")).resize((1280, 555))
        canvas.new_photo = ImageTk.PhotoImage(new_img)
        canvas.itemconfigure(bg_canvas, image=canvas.new_photo)

        # Update UI elements for the work session
        canvas.coords(image_item, 328, 275)
        canvas.coords(timer_text, 328, 400)
        canvas.itemconfig(timer_text, fill="white", font=FONT_TIMER)
        canvas.new_img = PhotoImage(file=os.path.join(base_dir, "assets", "Totoro.png"))
        canvas.itemconfig(image_item, image=canvas.new_img)
        canvas.itemconfig(timer_word, text="Work", fill=GREEN, font=FONT_TIMER)
        canvas.coords(timer_word, 560, 80)
        count_down(work_sec)
        return

    if is_timer_running:
        return

    reset_timer_only()

    t = threading.Thread(target=work_sound)
    t.start()

    if current_session_type == "work":
        add_image()

    is_timer_running = True
    reps += 1
    work_sec = work_duration * 60
    count_down(work_sec)

    # When work session is done, decide on break
    if reps % 5 == 0 and reps > 1:  # Long break after every 4th work session
        start_long_break(long_break_duration)
    elif reps > 1: # Short break after each work session
        start_short_break(short_break_duration)

    return


# ---------------------------- BREAK FUNCTIONS ------------------------------- #
def start_short_break(duration_time):
    global reps, is_timer_running, current_session_type
    reset_timer_only()
    is_timer_running = False
    current_session_type = "short break"
    duration_time = duration_time * 60
    (start_break(duration_time, "Break", PINK, os.path.join(base_dir, "assets", "short-break-bg.png"),
            os.path.join(base_dir, "assets", "break-totoro.png"),
     FONT_TIMER, 360, 240, 650, 135))

def start_long_break(duration_time):
    global reps, is_timer_running, current_session_type
    reset_timer_only()
    is_timer_running = False
    current_session_type = "long break"
    duration_time = duration_time  * 60
    start_break(duration_time, "Break", RED, os.path.join(base_dir, "assets", "long-break-bg.png"),
            os.path.join(base_dir, "assets", "Totoro-break1.png"), FONT_LONG_BREAK,375, 320, 750, 120)

def start_break(duration, break_name, color, break_bg_image, totoro_image, font_break, coords_text_x, coords_text_y, coords_word_x, coords_word_y):
    global reps, timer, is_timer_running, current_session_type

    start_button.config(state=NORMAL)
    resume_timer_button.config(state=NORMAL)
    is_timer_running = True
    canvas.itemconfig(timer_text, font=font_break)

    current_session_type = "break"

    def break_sound():
        play_sound(os.path.join(base_dir, "assets", "break.wav"))

    t = threading.Thread(target=break_sound)
    t.start()

    # Update background and image
    new_img = Image.open(break_bg_image).resize((1280, 555))
    canvas.new_photo = ImageTk.PhotoImage(new_img)
    canvas.itemconfigure(bg_canvas, image=canvas.new_photo)
    canvas.coords(timer_text, coords_text_x, coords_text_y)
    canvas.itemconfig(timer_text, fill=color)
    canvas.new_img = PhotoImage(file=totoro_image)
    canvas.itemconfig(image_item, image=canvas.new_img)

    count_down(duration)
    canvas.itemconfig(timer_word, text=break_name, fill=color, font=FONT_TIMER)
    canvas.coords(timer_word, coords_word_x, coords_word_y)


# ---------------------------- VOLUME CONTROL ------------------------------- #
def on_volume_change(val):
    global volume_level
    volume_level = float(val) / 100
    pygame.mixer.music.set_volume(volume_level)


# ----------------------------- VALID INPUT --------------------------------- #
# Function to get valid input or use default values
def get_valid_input(input_field, default_value):
    try:
        value = input_field.get().strip()
        if value == "":  # If input is empty, return the default value
            return default_value
        return int(value)
    except ValueError:  # Catch non-numeric input
        return default_value  # Return the default value if input is invalid


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Totoro-Pomodoro")
window.geometry("1055x755")

# Global variables for entry widgets
work_input = Entry(window)
short_break_input = Entry(window)
long_break_input = Entry(window)

# Set up the duration inputs (work, short break, long break)
def setup_duration_inputs():
    global work_input, short_break_input, long_break_input

    # Create the work input field with placeholder
    work_input = Entry(window, width=10)
    work_input.insert(0, "Work (min)")  # Placeholder text
    work_input.grid(row=0, column=0, pady=15, padx=(50, 5))
    work_input.config(fg="#949292")

    # Function to handle the placeholder behavior for the work input
    def on_work_input_click(event):
        if work_input.get() == "Work (min)":  # Placeholder text
            work_input.delete(0, "end")  # Clear the placeholder
            work_input.config(fg="black")  # Set the text color to black

    # Bind the click event to remove placeholder
    work_input.bind("<FocusIn>", on_work_input_click)

    # Function to reset placeholder if the input is empty
    def on_work_input_focus_out(event):
        if work_input.get() == "":  # If no input is provided
            work_input.insert(0, "Work (min)")  # Reapply placeholder text

    # Bind the focus out event to reset the placeholder if needed
    work_input.bind("<FocusOut>", on_work_input_focus_out)

    # Create the short break input field with placeholder
    short_break_input = Entry(window, width=15)
    short_break_input.insert(0, "Short Break (min)")  # Placeholder text
    short_break_input.grid(row=0, column=1, pady=5, padx=0)
    short_break_input.config(fg="#949292")

    # Function to handle the placeholder behavior for the short break input
    def on_short_break_input_click(event):
        if short_break_input.get() == "Short Break (min)":
            short_break_input.delete(0, "end")
            short_break_input.config(fg="black")

    short_break_input.bind("<FocusIn>", on_short_break_input_click)

    def on_short_break_input_focus_out(event):
        if short_break_input.get() == "":
            short_break_input.insert(0, "Short Break (min)")

    short_break_input.bind("<FocusOut>", on_short_break_input_focus_out)

    # Create the long break input field with placeholder
    long_break_input = Entry(window, width=15)
    long_break_input.insert(0, "Long Break (min)")  # Placeholder text
    long_break_input.grid(row=0, column=2, pady=5, padx=5)
    long_break_input.config(fg="#949292")

    # Function to handle the placeholder behavior for the long break input
    def on_long_break_input_click(event):
        if long_break_input.get() == "Long Break (min)":
            long_break_input.delete(0, "end")
            long_break_input.config(fg="black")

    long_break_input.bind("<FocusIn>", on_long_break_input_click)

    def on_long_break_input_focus_out(event):
        if long_break_input.get() == "":
            long_break_input.insert(0, "Long Break (min)")

    long_break_input.bind("<FocusOut>", on_long_break_input_focus_out)

    # Function to remove focus when clicking outside
    def remove_focus(event):
        # Remove focus from all entry widgets by clicking outside
        if (event.widget != work_input and
                event.widget != short_break_input and
                event.widget != long_break_input):
            window.focus_set()  # This removes focus from all input fields

    # Bind the click event to remove focus when clicking anywhere outside the input fields
    window.bind("<Button-1>", remove_focus)


bg_image = Image.open(os.path.join(base_dir, "assets", "bg1.jpg"))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0)

canvas = Canvas(window, width=955, height=650, highlightthickness=0, bd=0)

setup_duration_inputs()
# Canvas Background Setup
img1 = Image.open(os.path.join(base_dir, "assets", "check-path.jpg"))
resized_image1 = img1.resize((1380, 1000))
new_image1 = ImageTk.PhotoImage(resized_image1)
bg_bottom_canvas = canvas.create_image(0, -340, anchor=NW, image=new_image1)

img = Image.open(os.path.join(base_dir, "assets", "bg.jpg"))
resized_image = img.resize((1280, 555))
new_image = ImageTk.PhotoImage(resized_image)
bg_canvas = canvas.create_image(0, 0, anchor=NW, image=new_image)

# Totoro Image Setup
totoro_img = PhotoImage(file=os.path.join(base_dir, "assets", "Totoro.png"))
image_item = canvas.create_image(328, 275, image=totoro_img)
canvas.place(x=50, y=50)

timer_word = canvas.create_text(560, 80, text="Timer", fill=GREEN, font=FONT_TIMER)
timer_text = canvas.create_text(328, 400, text="00:00", fill="white", font=(FONT_NAME, 45, "bold"))

# Volume Control Slider
volume_slider = Scale(
    window,
    from_=0,
    to=100,
    orient=HORIZONTAL,
    command=on_volume_change,
    bg="LightSteelBlue1",  # Background color of the slider
    fg="black",             # Color of the slider indicator
    activebackground="palevioletred3",  # Color when hovered
    sliderlength=30,        # Length of the slider knob
    length=300,             # Length of the slider
    highlightbackground="yellow",  # Color of the highlight around the slider
    font=("Courier", 12)    # Font of the text
)
volume_slider.set(100)  # Set default volume to 100%
volume_slider.place(x=700, y=5)


# Function to overlay a color while preserving icon shape
def overlay_image(icon, color):
    # Create a new image with the same size and an empty (transparent) background
    overlay = Image.new("RGBA", icon.size, (0, 0, 0, 0))

    # Create an overlay layer filled with the specified color
    colored_overlay = Image.new("RGBA", icon.size, color)

    # Use the icon's own transparency (alpha channel) as a mask
    overlay = Image.composite(colored_overlay, overlay, icon)

    # Composite the overlay with the icon
    return Image.alpha_composite(icon, overlay)

# Define hover overlay color (Light Steel Blue with transparency)
hover_color = (176, 224, 230, 128)

# Load and scale icons as PIL images
resume_icon_pil = Image.open(os.path.join(base_dir, "assets", "resume_icon.png")).resize((50, 50), Image.Resampling.LANCZOS).convert("RGBA")
pause_icon_pil = Image.open(os.path.join(base_dir, "assets", "pause_icon.png")).resize((50, 50), Image.Resampling.LANCZOS).convert("RGBA")
stop_icon_pil = Image.open(os.path.join(base_dir, "assets", "stop_icon.png")).resize((50, 50), Image.Resampling.LANCZOS).convert("RGBA")

# Convert PIL images to Tkinter-compatible PhotoImage
resume_icon = ImageTk.PhotoImage(resume_icon_pil)
pause_icon = ImageTk.PhotoImage(pause_icon_pil)
stop_icon = ImageTk.PhotoImage(stop_icon_pil)

# Add images to canvas
resume_image = canvas.create_image(730, 55, anchor='sw', image=resume_icon)
canvas.tag_bind(resume_image, "<Button-1>", lambda event: resume_sound())
pause_image = canvas.create_image(780, 55, anchor='sw', image=pause_icon)
canvas.tag_bind(pause_image, "<Button-1>", lambda event: pause_sound())
stop_image = canvas.create_image(880, 55, anchor='se', image=stop_icon)
canvas.tag_bind(stop_image, "<Button-1>", lambda event: stop_sound())

resume_overlayed_image = None
pause_overlayed_image = None
stop_overlayed_image = None

# Hover functions to apply overlay matching the icon's shape
def on_resume_image_enter(event):
    global resume_overlayed_image
    overlayed_image = overlay_image(resume_icon_pil, hover_color)
    resume_overlayed_image = ImageTk.PhotoImage(overlayed_image)
    canvas.itemconfig(resume_image, image=resume_overlayed_image)

def on_resume_image_leave(event):
    canvas.itemconfig(resume_image, image=resume_icon)

def on_pause_image_enter(event):
    global pause_overlayed_image
    overlayed_image = overlay_image(pause_icon_pil, hover_color)
    pause_overlayed_image = ImageTk.PhotoImage(overlayed_image)
    canvas.itemconfig(pause_image, image=pause_overlayed_image)

def on_pause_image_leave(event):
    canvas.itemconfig(pause_image, image=pause_icon)

def on_stop_image_enter(event):
    global stop_overlayed_image
    overlayed_image = overlay_image(stop_icon_pil, hover_color)
    stop_overlayed_image = ImageTk.PhotoImage(overlayed_image)
    canvas.itemconfig(stop_image, image=stop_overlayed_image)

def on_stop_image_leave(event):
    canvas.itemconfig(stop_image, image=stop_icon)

# Bind hover events for each image
canvas.tag_bind(resume_image, "<Enter>", on_resume_image_enter)
canvas.tag_bind(resume_image, "<Leave>", on_resume_image_leave)
canvas.tag_bind(pause_image, "<Enter>", on_pause_image_enter)
canvas.tag_bind(pause_image, "<Leave>", on_pause_image_leave)
canvas.tag_bind(stop_image, "<Enter>", on_stop_image_enter)
canvas.tag_bind(stop_image, "<Leave>", on_stop_image_leave)

start_img = PhotoImage(file=os.path.join(base_dir, "assets", "start-button.png"))
start_img = start_img.subsample(4)
start_button = Button(window, image=start_img, highlightthickness=0, bd=0,   command=lambda: start_timer(get_valid_input(work_input, WORK_MIN)), anchor='n',
                      activebackground="green", bg="yellow green")
start_button_window = canvas.create_window(660, 640, anchor='sw', window=start_button)

reset_img = PhotoImage(file=os.path.join(base_dir, "assets", "reset-button.png"))
reset_img = reset_img.subsample(4)
reset_button = Button(image=reset_img, highlightthickness=0, bd=0, command=reset_timer, anchor='n',
                      activebackground="green", bg="yellow green")
reset_button_window = canvas.create_window(935, 640, anchor='se', window=reset_button)


# Pause Timer Button
pause_timer_button = Button(window, text="Pause Timer", command=pause_timer, font=("Courier", 12, "bold"), bg="LightSteelBlue1")
pause_timer_window = canvas.create_window(320, 680, anchor='sw', window=pause_timer_button)

# Resume Timer Button
resume_timer_button = Button(window, text="Resume Timer", command=resume_timer, font=("Courier", 12, "bold"), bg="LightSteelBlue1")
resume_timer_window = canvas.create_window(620, 680, anchor='se', window=resume_timer_button)

# Short Break Button
short_break_button = Button(window, text="Short Break", command=lambda: start_short_break(get_valid_input(short_break_input, SHORT_BREAK_MIN)), font=("Courier", 12, "bold"), bg="LightSteelBlue1")
short_break_button_window = canvas.create_window(1, 680, anchor='sw', window=short_break_button)

# Long Break Button
long_break_button = Button(window, text="Long Break", command=lambda: start_long_break(get_valid_input(long_break_input, LONG_BREAK_MIN)), font=("Courier", 12, "bold"), bg="LightSteelBlue1")
long_break_button_window = canvas.create_window(280, 680, anchor='se', window=long_break_button)

# ---------------------------- MAINLOOP ------------------------------- #
window.mainloop()