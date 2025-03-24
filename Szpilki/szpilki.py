from tkinter import Label, Tk, Canvas, Entry, Button
from random import randint
from PIL import Image, ImageTk
from numpy import array

CZAS_NA_SZPILKE = 0
CZAS_NA_ODPOWIEDZ = 0
global szpilka, odpowiedz, main_timer
remaining_time = CZAS_NA_SZPILKE
COUNTER = 0


def pick_random_image():
    canvas_width, canvas_height = 930, 690

    idx = randint(1, 3)
    # idx = str(idx).zfill(4)
    pill_image = Image.open(f"images/1 ({idx}).jpg")
    # pill_image = array(pill_image)
    # szpilka = pill_image[100:790, 150:1080]
    # odpowiedz = pill_image[915:1625, 150:1080]

    szpilka = pill_image.crop((300, 200, 2200, 1600))
    odpowiedz = pill_image.crop((300, 1800, 2200, 3200))

    szpilka = szpilka.resize((canvas_width, canvas_height), Image.LANCZOS)
    odpowiedz = odpowiedz.resize((canvas_width, canvas_height), Image.LANCZOS)

    szpilka = ImageTk.PhotoImage(szpilka)
    odpowiedz = ImageTk.PhotoImage(odpowiedz)

    # szpilka = ImageTk.PhotoImage(Image.fromarray(szpilka))
    # odpowiedz = ImageTk.PhotoImage(Image.fromarray(odpowiedz))

    return szpilka, odpowiedz


def switch_image():
    global szpilka, odpowiedz, remaining_time, COUNTER
    szpilka, odpowiedz = pick_random_image()
    canvas.itemconfig(canvas_image, image=szpilka)
    remaining_time = CZAS_NA_SZPILKE
    COUNTER += 1
    canvas.itemconfig(counter_text, text=COUNTER)
    try:
        window.after_cancel(main_timer)
    except:
        pass
    update_timer()
    window.after(1000 * CZAS_NA_SZPILKE, switch_image2, odpowiedz)


def switch_image2(image):
    global remaining_time
    canvas.itemconfig(canvas_image, image=image)
    remaining_time = CZAS_NA_ODPOWIEDZ
    window.after_cancel(main_timer)
    update_timer()
    window.after(1000 * CZAS_NA_ODPOWIEDZ, switch_image)


def update_timer():
    global remaining_time, main_timer
    if remaining_time >= 0:
        canvas.itemconfig(timer_text, text=f"{remaining_time}")
        remaining_time -= 1  # Zmniejszaj czas o 1 sekundę
        main_timer = window.after(1000, update_timer)  # Wywołaj ponownie co 1000 ms


def start_function():
    global CZAS_NA_SZPILKE, CZAS_NA_ODPOWIEDZ
    CZAS_NA_SZPILKE = int(entry_szpilka.get())
    CZAS_NA_ODPOWIEDZ = int(entry_odpowiedz.get())
    entry_szpilka.destroy()
    entry_odpowiedz.destroy()
    button_start.destroy()
    switch_image()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Szpilunie Festunie")

entry_szpilka = Entry(bg="white", fg="black", font=('Arial', 25))
entry_szpilka.insert(0, "30")
entry_szpilka.grid(row=1, column=0)
entry_odpowiedz = Entry(bg="white", fg="black", font=('Arial', 25))
entry_odpowiedz.insert(0, "5")
entry_odpowiedz.grid(row=1, column=1)

button_start = Button(text="Start", bg="white", fg="black", command=start_function)
button_start.grid(row=2, column=0, columnspan=2)

canvas = Canvas(window, width=930, height=690, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

canvas_image = canvas.create_image(465, 345)

timer_text = canvas.create_text(
                                465, 40,
                                text=f"{remaining_time}",
                                font=('Arial', 20, "bold"),
                                fill="white")

# Współrzędne tekstu
text_x, text_y = 465, 40

# Tworzenie prostokąta jako tła dla tekstu (kolor np. czarny)
background_rect = canvas.create_rectangle(
    text_x - 50, text_y - 20, text_x + 50, text_y + 20,  # Ustal rozmiar prostokąta odpowiednio do tekstu
    fill="black"
)

counter_text = canvas.create_text(
                                40, 40,
                                text=f"{COUNTER}",
                                font=('Arial', 20, "bold"),
                                fill="white")


canvas.tag_raise(timer_text)

window.mainloop()
