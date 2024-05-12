import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font

from AiGymTrainer import AIGymTrainer

def execute_exercise(exercise_choice: str) -> None:
    trainer = AIGymTrainer()
    trainer.run(exercise_choice)

root = tk.Tk()
root.configure(bg='grey20')
root.title("AI Gym Trainer")

background_image = Image.open("pictures\\gymBg.jpg")
background_image = ImageTk.PhotoImage(background_image)

root.geometry(f"{background_image.width()}x{background_image.height()}+350+180")

background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label_font = font.Font(family="Helvetica", size=16, weight="bold")
button_font = font.Font(family="Helvetica", size=12, weight="bold")

welcome_label = tk.Label(root, text="Welcome to AI Gym Trainer", bg='black', fg='white', font=("Helvetica", 16))
welcome_label.place(x=20, y=20)

prompt_label = tk.Label(root, text="Select an exercise you would like to train?", bg='black', fg='white', font=("Helvetica", 14))
prompt_label.place(x=20, y=60)

button1 = tk.Button(root, text="Single Dumbbell Curl", command=lambda: execute_exercise("1"), bg='grey20', fg='white', font=button_font, relief=tk.RAISED, bd=5)
button1.place(x=20, y=100, width=200, height=40)

button2 = tk.Button(root, text="Reverse Fly", command=lambda: execute_exercise("2"), bg='grey20', fg='white', font=button_font, relief=tk.RAISED, bd=5)
button2.place(x=20, y=150, width=200, height=40)

button3 = tk.Button(root, text="Barbell Curl", command=lambda: execute_exercise("3"), bg='grey20', fg='white', font=button_font, relief=tk.RAISED, bd=5)
button3.place(x=20, y=200, width=200, height=40)

button4 = tk.Button(root, text="Push-ups", command=lambda: execute_exercise("4"), bg='grey20', fg='white', font=button_font, relief=tk.RAISED, bd=5)
button4.place(x=20, y=250, width=200, height=40)

button5 = tk.Button(root, text="Deadlift", command=lambda: execute_exercise("5"), bg='grey20', fg='white', font=button_font, relief=tk.RAISED, bd=5)
button5.place(x=20, y=300, width=200, height=40)
root.mainloop()