from tkinter import *
import re


# Arguments
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
BACKGROUND = "#030303"
FRAMES = ["Cel2Fah", "Fah2Cel"]
TEMP_REGEX = r"([+-]?\d+(\.\d+)*)\s?°([CcFf])"
FLOAT_REGEX = r"[+-]?\d+\.\d+"

# Check Float
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# Formula Cel2Fah
def cel2fah(cel):
    return (cel * (9/5)) + 32


# Formula Fah2Cel
def fah2cel(fah):
    return (fah - 32) * (5/9)


# Option Frame Switch
def converter(entry, controller):
    if entry == "Cel2Fah":
        controller.show_frame(Cel2Fah)
    else:
        controller.show_frame(Fah2Cel)


# App Setup
class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        X_COORD = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        Y_COORD = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)

        # Setup GUI
        self.title("Cel2Fah - Fah2Cel (by Spimy)")
        # self.resizable(False, False)
        self.geometry("+{0}+{1}".format(X_COORD, Y_COORD))
        self.iconbitmap("icon.ico")
        self.config(cursor="@arrow.cur")

        # Setup Frames
        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Frame Handler
        self.frames = {}

        for F in (Cel2Fah, Fah2Cel):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Set Default Page
        self.show_frame(Cel2Fah)

    # Change Frame of GUI
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Cel2Fah(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background=BACKGROUND)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Setup Selection
        DROPDOWN_ARROW = PhotoImage(file='arrow.png')
        entry = StringVar()
        entry.set(FRAMES[0])

        # Converter Selection
        option = OptionMenu(self, entry, *FRAMES, 
                                 command=lambda ent=entry, cont=controller: converter(ent, cont))

        option.configure(highlightthickness=0, bg="#07049e", fg="#f1f1f1", font=("Consolas", 10),
                       activebackground="#0400d3", activeforeground="#f1f1f1", relief=FLAT)

        option["menu"].configure(bg="#07049e", fg="#f1f1f1", activebackground="#0400d3", 
                                 activeforeground="#f1f1f1", bd=0, relief=FLAT, 
                                 font=("Consolas", 10), activeborderwidth=0)
        
        # Changing Selection Dropdown Arrow
        option.config(compound='right', image=DROPDOWN_ARROW, indicator=0)
        option.image = DROPDOWN_ARROW

        # Setup Celsius Entry
        self.celsius = Entry(self, fg="#f1f1f1", bg="#0c0c0c", insertbackground="#f1f1f1", bd=0, relief=FLAT)
        self.celsius.insert(0, "0°C")
        self.celsius.bind("<FocusIn>", lambda args: self.celsius.delete('0', 'end'))

        # Setup Submit Button
        submit = Button(self, text="Convert", bg="#07049e", fg="#f1f1f1", font=("Consolas", 10),
                        relief=FLAT, activebackground="#0400d3", activeforeground="#f1f1f1",
                        width=25, height=2, command=self.submit)

        # Placing Widgets
        option.grid(row=0, column=0, padx=100, pady=(20, 5), sticky="nsew")
        self.celsius.grid(row=1, column=0, padx=100, pady=(5, 5), sticky="nsew")
        submit.grid(row=2, column=0, padx=100, pady=(5, 20), sticky="nsew")
 
    def submit(self):

        if not str.isnumeric(self.celsius.get() or not isfloat(self.fahrenheit.get())):

            if re.match(TEMP_REGEX, self.celsius.get()):
                if re.match(FLOAT_REGEX, self.celsius.get()):
                    cel = float(re.findall(FLOAT_REGEX, self.celsius.get())[0])
                    ans = cel2fah(cel)
                    self.celsius.delete('0', 'end')
                    return self.celsius.insert(0, "{0}°C = {1}°F".format(cel, ans))

                cel = float(''.join(list(filter(str.isdigit, self.celsius.get()))))
                ans = cel2fah(cel)
                self.celsius.delete('0', 'end')
                return self.celsius.insert(0, "{0}°C = {1}°F".format(cel, ans))

            if re.match(FLOAT_REGEX, self.celsius.get()):
                cel = float(re.findall(FLOAT_REGEX, self.celsius.get())[0])
                ans = cel2fah(cel)
                self.celsius.delete('0', 'end')
                return self.celsius.insert(0, "{0}°C = {1}°F".format(cel, ans))
                
            self.celsius.delete('0', 'end')
            return self.celsius.insert(0, "Please Insert Numbers")
        
        cel = float(self.celsius.get())
        ans = cel2fah(cel)
        self.celsius.delete('0', 'end')
        return self.celsius.insert(0, "{0}°C = {1}°F".format(cel, ans))

class Fah2Cel(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background=BACKGROUND)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Setup Selection
        DROPDOWN_ARROW = PhotoImage(file='arrow.png')
        entry = StringVar()
        entry.set(FRAMES[1])

        # Converter Selection
        option = OptionMenu(self, entry, *FRAMES, 
                                 command=lambda ent=entry, cont=controller: converter(ent, cont))

        option.configure(highlightthickness=0, bg="#07049e", fg="#f1f1f1", font=("Consolas", 10),
                       activebackground="#0400d3", activeforeground="#f1f1f1", relief=FLAT)

        option["menu"].configure(bg="#07049e", fg="#f1f1f1", activebackground="#0400d3", 
                                 activeforeground="#f1f1f1", bd=0, relief=FLAT, 
                                 font=("Consolas", 10), activeborderwidth=0)
        
        # Changing Selection Dropdown Arrow
        option.config(compound='right', image=DROPDOWN_ARROW, indicator=0)
        option.image = DROPDOWN_ARROW

        # Setup Fahrenheit Entry
        self.fahrenheit = Entry(self, fg="#f1f1f1", bg="#0c0c0c", insertbackground="#f1f1f1", bd=0, relief=FLAT)
        self.fahrenheit.insert(0, "32°F")
        self.fahrenheit.bind("<FocusIn>", lambda args: self.fahrenheit.delete('0', 'end'))

        # Setup Submit Button
        submit = Button(self, text="Convert", bg="#07049e", fg="#f1f1f1", font=("Consolas", 10),
                        relief=FLAT, activebackground="#0400d3", activeforeground="#f1f1f1",
                        width=25, height=2, command=self.submit)

        # Placing Widgets
        option.grid(row=0, column=0, padx=100, pady=(20, 5), sticky="nsew")
        self.fahrenheit.grid(row=1, column=0, padx=100, pady=(5, 5), sticky="nsew")
        submit.grid(row=2, column=0, padx=100, pady=(5, 20), sticky="nsew")

    def submit(self):
        if not str.isnumeric(self.fahrenheit.get() or not isfloat(self.fahrenheit.get())):

            if re.match(TEMP_REGEX, self.fahrenheit.get()):
                if re.match(FLOAT_REGEX, self.fahrenheit.get()):
                    fah = float(re.findall(FLOAT_REGEX, self.fahrenheit.get())[0])
                    ans = fah2cel(fah)
                    self.fahrenheit.delete('0', 'end')
                    return self.fahrenheit.insert(0, "{0}°F = {1}°C".format(fah, ans))

                fah = float(''.join(list(filter(str.isdigit, self.fahrenheit.get()))))
                ans = fah2cel(fah)
                self.fahrenheit.delete('0', 'end')
                return self.fahrenheit.insert(0, "{0}°F = {1}°C".format(fah, ans))

            if re.match(FLOAT_REGEX, self.fahrenheit.get()):
                fah = float(re.findall(FLOAT_REGEX, self.fahrenheit.get())[0])
                ans = fah2cel(fah)
                self.fahrenheit.delete('0', 'end')
                return self.fahrenheit.insert(0, "{0}°F = {1}°C".format(fah, ans))

            self.fahrenheit.delete('0', 'end')
            return self.fahrenheit.insert(0, "Please Insert Numbers")
        
        fah = float(self.fahrenheit.get())
        ans = fah2cel(fah)
        self.fahrenheit.delete('0', 'end')
        return self.fahrenheit.insert(0, "{0}°F = {1}°C".format(fah, ans))


def runapp():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    runapp()