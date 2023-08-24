import json
import random
from tkinter import NW, Button, Canvas, Label, Tk

from PIL import Image, ImageTk
from pygame import mixer

from brains import playInstrument


def change_bg():
    if main_menu_running:
        main_menu.bind("<Button-1>", play)
        count = 50
        prev_bg_color = random.choice(bg_colors)
        bg_color = random.choice(bg_colors)
        for i in range(count):
            while bg_color == prev_bg_color:
                bg_color = random.choice(bg_colors)
            main_menu.create_rectangle(
                (i * w / count, 0), ((i + 1) * w / 5, h), fill=bg_color, width=0
            )
            prev_bg_color = bg_color
        setting_button = Button(
            root,
            image=setting_img,
            borderwidth=0,
            command=setting,
            bg="black",
            activebackground="white",
        )
        setting_button.place(x=560, y=410)
        main_menu.create_image(140, 120, image=logo_img, anchor=NW)
        main_menu.place(x=0, y=0)
        close_button = Button(
            root,
            image=close_img,
            borderwidth=0,
            command=close,
            bg="black",
            activebackground="white",
        )
        close_button.place(x=560, y=20)
        root.after(500, change_bg)
    global master_initialized
    if not master_initialized:
        global master
        master = playInstrument()
        master_initialized = True


def close():
    root.quit()


def setting():
    pass


def play(e):
    global main_menu_running
    main_menu_running = False
    selection_menu(current_item)


def back():
    global master_running
    master_running = False
    selection_menu(current_item)
    mixer.music.unpause()


def start(e, instrument):
    mixer.music.pause()
    global current_item
    current_item = instrument
    global master_running
    master_running = True
    for ele in root.winfo_children():
        ele.destroy()
    vid_label = Label(root, height=h, width=w)
    close_button = Button(
        root,
        image=close_img,
        borderwidth=0,
        command=close,
        bg="#3b3b3b",
        activebackground="white",
    )
    close_button.place(x=560, y=20)
    back_button = Button(
        root,
        image=back_img,
        borderwidth=0,
        command=back,
        bg="#3b3b3b",
        activebackground="white",
    )
    back_button.place(x=30, y=20)
    vid_label.pack()
    master.instrument_init(instrument)

    def show_frame():
        if master_running:
            frame = master.play()
            image_fa = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image=image_fa)
            vid_label.photo_image = image
            vid_label.configure(image=image)
            vid_label.after(1, show_frame)

    show_frame()


def menu_change(k, e=0):
    selection_menu(k)


def back_main():
    global main_menu_running
    main_menu_running = True
    for ele in root.winfo_children():
        ele.destroy()
    global main_menu
    main_menu = Canvas(root, border=0, height=h, width=w)
    change_bg()


def selection_menu(instrument):
    instrument_idx = instruments.index(instrument)
    if instrument_idx == len(instruments) - 1:
        next_idx = 0
    else:
        next_idx = instrument_idx + 1
    if instrument_idx == 0:
        prev_idx = len(instruments) - 1
    else:
        prev_idx = instrument_idx - 1
    bg_color = random.choice(bg_colors)
    s_menu = Canvas(root, height=h, width=w, bg=bg_color)
    s_menu.create_image(
        460, 215, image=instruments_img[instruments[next_idx]]["small"], anchor=NW
    )
    s_menu.create_image(
        100, 215, image=instruments_img[instruments[prev_idx]]["small"], anchor=NW
    )
    s_menu.create_image(
        w / 2 - instruments_img[instrument]["title"].width() / 2,
        90,
        image=instruments_img[instrument]["title"],
        anchor=NW,
    )
    s_menu.create_image(250, 190, image=instruments_img[instrument]["big"], anchor=NW)
    prev_button = Button(
        s_menu,
        image=prev_img,
        borderwidth=0,
        command=lambda: selection_menu(instruments[prev_idx]),
        bg=bg_color,
        activebackground=bg_color,
    )
    root.bind("<Left>", lambda x: menu_change(instruments[prev_idx], x))
    root.bind("<Right>", lambda x: menu_change(instruments[next_idx], x))
    next_button = Button(
        s_menu,
        image=next_img,
        borderwidth=0,
        command=lambda: selection_menu(instruments[next_idx]),
        bg=bg_color,
        activebackground=bg_color,
    )
    close_button = Button(
        s_menu,
        image=close_img,
        borderwidth=0,
        command=close,
        bg=bg_color,
        activebackground=bg_color,
    )
    prev_button.place(x=30, y=230)
    next_button.place(x=570, y=230)
    close_button.place(x=560, y=20)
    back_button = Button(
        root,
        image=back_img,
        borderwidth=0,
        command=back_main,
        bg=bg_color,
        activebackground=bg_color,
    )
    back_button.place(x=30, y=20)
    play_button = Button(
        root,
        image=next_img,
        borderwidth=0,
        command=lambda: start(0, instrument),
        bg=bg_color,
        activebackground=bg_color,
    )
    play_button.place(x=300, y=360)
    root.bind("<space>", lambda e: start(e, instrument))
    # root.bind("<Button-1>", lambda e: start(e, instrument))
    s_menu.place(x=0, y=0)


w = 640
h = 480
bg_colors = ["#01afda", "#fee471", "#fe9fab", "#f7f4d4", "#6fdfd1", "#39d4c0"]

root = Tk()
root.geometry("640x480+300+100")
root.attributes("-topmost", True)
root.overrideredirect(True)
main_menu_running = True
master_initialized = False
master_running = True

mixer.init()
mixer.music.load(
    "/home/haseeb/Downloads/VR_tones/assets/background_music/still_Dre.mp3"
)
mixer.music.play()

main_menu = Canvas(root, border=0, height=h, width=w)

logo_img = ImageTk.PhotoImage(
    file="/home/haseeb/Downloads/VR_tones/assets/icons/logo.png", format="RGBA"
)
close_img = ImageTk.PhotoImage(
    file="/home/haseeb/Downloads/VR_tones/assets/icons/close.png", format="RGBA"
)
setting_img = ImageTk.PhotoImage(
    file="/home/haseeb/Downloads/VR_tones/assets/icons/setting.png", format="RGBA"
)
prev_img = ImageTk.PhotoImage(
    file="/home/haseeb/Downloads/VR_tones/assets/icons/prev.png", format="RGBA"
)
next_img = ImageTk.PhotoImage(
    file="/home/haseeb/Downloads/VR_tones/assets/icons/next.png", format="RGBA"
)
back_img = ImageTk.PhotoImage(
    file="/home/haseeb/Downloads/VR_tones/assets/icons/back.png", format="RGBA"
)
tap_img = ImageTk.PhotoImage(
    file="/home/haseeb/Downloads/VR_tones/assets/icons/back.png", format="RGBA"
)

file = open("data.json")
instrument_data = json.load(file)
instruments = []
for item in instrument_data:
    instruments.append(item)

current_item = instruments[0]
instrument_img_labels = ["big", "small", "title"]
instruments_img = {}
for instrument in instruments:
    instruments_img[instrument] = {}
    for label in instrument_img_labels:
        instruments_img[instrument][label] = ImageTk.PhotoImage(
            file=f"./assets/icons/{instrument}_{label}.png", format="RGBA"
        )
change_bg()
root.mainloop()
