# Linux-Totoro-Pomodoro-Timer

A Totoro-themed Pomodoro Timer application built in Python using the
Tkinter GUI library. This tool follows the Pomodoro technique, helping
users improve productivity by dividing work into focused sessions with
breaks in between. Designed specifically for Linux, it features static Totoro-inspired images and custom session management options.

## Features

- **Work and Break Sessions**: Alternate between focused work intervals and short breaks, with visuals updating based on the session type.
- **Customizable Timer**: Set custom work and break durations, adjusting the timer to fit your preferences.
- **Threaded Execution for Responsive GUI**:
Utilizes Python's threading module to keep the interface responsive, preventing blocking operations during countdowns.
- **Sound and Alerts**: Plays sounds at the start of work or 
  break session to keep you aware of each transition.
- **Start, Pause and Resume Options**: Control your Pomodoro timer with intuitive start, pause and resume functions.
- **Error Handling**: Improved handling for undefined variables and unexpected inputs to ensure smooth functionality.
- **Totoro Theme**: Uses Totoro-themed images as background visuals during work and break sessions.
- **Volume Control**: Volume control is implemented using pygame.mixer for real-time sound management.
- **Responsive Images**: The background image dynamically updates to match the current session type, either work or break.
- **Reset and Skip Functions**: Easily reset the timer or skip to the next session as needed.

## Technologies Used

- **Python**: The core programming language used for the logic and functionality of the Pomodoro timer.
- **Tkinter**: Python’s standard GUI library, used for creating the application's interface and managing user interactions.
- **Pygame**: Specifically pygame.mixer for sound playback and real-time volume control.
- **Static Assets (Images and Sounds)**: Totoro-themed images provide a 
  playful interface, while sound files signal transitions between sessions.

## Prerequisites

Before using Totoro-Pomodoro, ensure you have the following dependencies installed:

~~~
Python 3.10
Tkinter
PIL (Python Imaging Library)
pygame
~~~

## Installation
Clone the repository:

~~~bash
git clone https://github.com/filosoho/Linux-Totoro-Pomodoro-Timer.git
~~~

Navigate to the project directory:

~~~bash
cd Linux-Totoro-Pomodoro-Timer
~~~

Run the totoro-pomodoro.py file using Python:

~~~
totoro-pomodoro.py
~~~
The Totoro-Pomodoro application window will appear.

## Usage

1. **Start Timer**: Click the Start button to begin a work session with 
   default time settings.
2. **Set Custom Time**: Set custom time using input fields for Work, Short 
   and Long Break.
3. **Pause/Resume Timer**: Use the Pause and Resume buttons to manage your 
   session timing.
4. **Adjust Volume**: Control the volume in real-time during the session.
5. **Reset Timer**: Click Reset button to reset the timer, checkmark animations and begin a new cycle.

## Customization Code Level

You can customize various aspects of Totoro-Pomodoro to suit your preferences:

- **Work and Break Durations**: You can adjust the default work and break 
durations by 
modifying the WORK_MIN, SHORT_BREAK_MIN and LONG_BREAK_MIN constants in the code.

- **Sound Notifications**: Replace the sound files (work.wav, break.wav, 2.
  wav) with your preferred audio files to change the notification sounds.

- **Totoro Images**: Replace the Totoro-themed image files with your own 
  images if you wish to customize the animations.

## Code Highlights

- **Countdown Logic**: The count_down() function handles the countdown 
  process for both work and break sessions, updating the timer label and managing session transitions.

- **Threading Implementation**: Using the threading.Thread object allows 
  the countdown to run in a separate thread, keeping the GUI responsive during the timer's operation.

- **Sound Control**: The pygame.mixer is utilized for real-time volume 
  control, allowing users to adjust the sound alert volume as sessions progress.

# Interface

<br>

![Totoro Pomodoro](https://github.com/filosoho/Linux-Totoro-Pomodoro-Timer/blob/4b1252a1a70717aafe6039558458693c10ff71fd/totoro1.png)

![Totoro Pomodoro](https://github.com/filosoho/Linux-Totoro-Pomodoro-Timer/blob/4b1252a1a70717aafe6039558458693c10ff71fd/totoro2.png)

![Totoro Pomodoro](https://github.com/filosoho/Linux-Totoro-Pomodoro-Timer/blob/4b1252a1a70717aafe6039558458693c10ff71fd/totoro3.png)

![Totoro Pomodoro](https://github.com/filosoho/Linux-Totoro-Pomodoro-Timer/blob/4b1252a1a70717aafe6039558458693c10ff71fd/totoro4.png)

![Totoro Pomodoro](https://github.com/filosoho/Linux-Totoro-Pomodoro-Timer/blob/4b1252a1a70717aafe6039558458693c10ff71fd/totoro5.png)

<br>

# Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository. 
2. Clone your forked repository.
    ~~~bash
    git clone https://github.com/your-username/Linux-Totoro-Pomodoro-Timer.git
    ~~~
    ~~~bash
    cd Linux-Totoro-Pomodoro-Timer
    ~~~

3. Create a new branch for your feature or bug fix.  
Replace "feature-branch-name" with a descriptive name for your new feature or bug fix.
    ~~~bash
    git checkout -b feature-branch-name
    ~~~
4. Make your changes and test thoroughly.  
     After making changes, add and commit them.
    ~~~bash
    git add .
    ~~~
    ~~~bash
    git commit -m "Add a clear, concise description of the changes you made"
    ~~~
5. Push your branch to your forked repository on GitHub.
    ~~~bash
    git push origin feature-branch-name
    ~~~
6. Create a pull request with a clear description of your changes.  
    Go to your repository on GitHub, navigate to your new branch, and click "Pull request."

# License

Feel free to use and modify the code as per your requirements.
