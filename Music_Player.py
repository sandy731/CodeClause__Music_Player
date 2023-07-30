from tkinter import *
import pygame
import time
from tkinter import filedialog
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("ShriNik")
root.iconbitmap('')
root.geometry("500x450")

# Initialize Pygame Mixer
pygame.mixer.init()


def add_song():
    song = filedialog.askopenfilename(initialdir="C:/Users/sande/Music", title="Choose a Song",
                                      filetypes=(("mp3 Files", "*.mp3"),))
    # Strip out the directory info from the mp3
    song = song.replace("C:/Users/sande/Music/", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)


# Add Many songs to playlist
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir="C:/Users/sande/Music", title="Choose a Song",
                                        filetypes=(("mp3 Files", "*.mp3"),))
    #  Loop through song list and replace directory info and mp3
    for song in songs:
        song = song.replace("C:/Users/sande/Music/", "")
        song = song.replace(".mp3", "")
        # Insert into playlist
        song_box.insert(END, song)


# Creating Play function
def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/sande/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Call the play_time function to get song length
    play_time()

    # Update slider to position
    # slider_position = int(song_len)
    # my_slider.config(to=slider_position, value=0)


# Stop plying current song
global stopped
stopped = False


def stop():
    # Reset Slider and Status bar
    status_bar.config(text=' ')
    my_slider.config(value=0)
    # Stop Song
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # Clear the status bar
    status_bar.config(text=' ')

    global stopped
    stopped = True


# Pause Function
# Create global pause function
global paused
paused = False


def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True


# Play the next song in the Playlist
def next_song():
    # Reset Slider and Status bar
    status_bar.config(text=' ')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    # Add one to the current song number
    next_one = next_one[0] + 1
    # Grab song title from the playlist
    song = song_box.get(next_one)
    # Add directory structure and mp3 to song title
    song = f'C:/Users/sande/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #  Clear active bar in playlist listbox
    song_box.selection_clear(0, END)

    #  Move active bar
    song_box.activate(next_one)

    # Set  active bar to next song
    song_box.select_set(next_one, last=None)


def previous_song():
    # Reset Slider and Status bar
    status_bar.config(text=' ')
    my_slider.config(value=0)

    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)

    song = f'C:/Users/sande/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #  Clear active bar in playlist listbox
    song_box.selection_clear(0, END)

    #  Move active bar
    song_box.activate(next_one)

    # Set  active bar to next song
    song_box.select_set(next_one, last=None)


# Delete A Song
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    # Stop music if it Plays
    pygame.mixer.music.stop()


# Delete All Song
def delete_all_song():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

# Grab Song length time info
#  Play Funtion
def play_time():
    if stopped:
        return

    current_time = pygame.mixer.music.get_pos() / 1000
    # slider_label.config(text=f'Slider: {int(my_slider.get())}  and  Song Pos: {int(current_time)}')
    # Covert to time format
    convert_crnt_time = time.strftime('%M:%S', time.gmtime(current_time))
    # Get Current Playing Song
    # current_song = song_box.curselection()

    song = song_box.get(ACTIVE)
    song = f'C:/Users/sande/Music/{song}.mp3'
    # Load song with Mutagen
    song_mut = MP3(song)
    # Get Song length with Mutagen
    global song_len
    song_len = song_mut.info.length
    convert_song_len = time.strftime('%M:%S', time.gmtime(song_len))

    current_time += 1
    if int(my_slider.get()) == int(song_len):
        status_bar.config(text=f'Time Elapsed : {convert_song_len} ')

    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_len)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        slider_position = int(song_len)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        convert_crnt_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time Elapsed :   {convert_crnt_time}   of   {convert_song_len} ')

        # Move these things along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    # Output time to status bar
    # status_bar.config(text=f'Time Elapsed :   {convert_crnt_time}   of   {convert_song_len} ')

    # Update slider position value to current song
    # my_slider.config(value=current_time)

    status_bar.after(1000, play_time)


# Slider Function
def slider(X):
    # slider_label.config(text=f'{int(my_slider.get())}  of  {int(song_len)}')
    song = song_box.get(ACTIVE)
    song = f'C:/Users/sande/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


# Creating playlist box
song_box = Listbox(root, bg="black", fg="LightGreen", width=60, selectbackground="Red", selectforeground="black")
song_box.pack(pady=20)

# Creating player control buttons

back_button_img = PhotoImage(file="back50.png")
forward_button_img = PhotoImage(file="forward50.png")
play_button_img = PhotoImage(file="play50.png")
pause_button_img = PhotoImage(file="pause50.png")
stop_button_img = PhotoImage(file="stop50.png")

# Create player control frame
control_frame = Frame(root)
control_frame.pack()

# Creating Player control buttons
back_button = Button(control_frame, image=back_button_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_button_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_button_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_button_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_button_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Creating a Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Adding song in menu
add_song_in_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_in_menu)
add_song_in_menu.add_command(label="Add One Song to Playlist", command=add_song)

# Add many songs to playlist
add_song_in_menu.add_command(label="Add Many Songs to Playlist", command=add_many_song)

# Create Delete song menu
remove_song = Menu(my_menu)
my_menu.add_cascade(label="Remove Song", menu=remove_song)
remove_song.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song.add_command(label="Delete All Song From Playlist", command=delete_all_song)

# Create Status Bar
status_bar = Label(root, text=' ', bd=1, relief=GROOVE, anchor=N)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create Music Slider
my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slider, length=360)
my_slider.pack(pady=30)

root.mainloop()
