from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from pygame import mixer


class GUI(Tk):
    def __init__(self, title="Window", width=200, height=200, bg="white", resizableX=0, resizableY=0):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.config(bg=bg)
        self.resizable(resizableX, resizableY)

    def start(self):
        self.mainloop()


def format2Digit(item):
    if item < 10:
        return str(f"0{item}")
    else:
        return str(item)


def formatTime(time):
    # Format Hour & Zone
    hours = int(time[0])
    minutes = int(time[1])
    seconds = int(time[2])
    my_zone = ""
    if hours > 12:
        hours -= 12
        my_zone = "PM"
    elif hours == 12:
        my_zone = "PM"
    elif hours == 0:
        hours = 12
        my_zone = "AM"
    else:
        my_zone = "AM"

    hours = format2Digit(hours)
    minutes = format2Digit(minutes)
    seconds = format2Digit(seconds)

    return f"{hours} : {minutes} : {seconds} {my_zone}    {time[3]}\n"


def formatDate(event):
    date_set = str(date_selected.get_date())
    date_selected.set_date(f"{int(date_set[5:7])}/{int(date_set[-2:])}/{int(date_set[:4])}")


def setListBox():
    alarms.delete(0, END)
    f = open("alarms.txt", "r")
    items = f.readlines()
    items.reverse()
    for item in items:
        alarms.insert(END, item)


def setFileByList():
    f = open("alarms.txt", "w")
    items = list(alarms.get(0, END))
    items.reverse()
    for item in items:
        f.write(item)
    f.close()
    setListBox()


def addAlarm(set_time):
    items = alarms.get(0, END)
    time_to_set = f"{set_time[0]} : {set_time[1]} : {set_time[2]} {set_time[3]}    {set_time[4]}\n"
    for item in items:
        if time_to_set == item:
            return
    f = open("alarms.txt", "a")
    f.write(time_to_set)
    f.close()
    setListBox()


def getCurTime():
    time_obj = datetime.datetime.now()
    hours = time_obj.hour
    minutes = time_obj.minute
    seconds = time_obj.second
    date_now = datetime.date.today()

    # time_now = f"{hours} : {minutes} : {seconds} {zone}"
    # timeLabel.config(text=time_now)
    # dateLabel.config(text=f"{date_now}")
    # dateLabel.after(500, __showTime)

    return [hours, minutes, seconds, str(date_now)]


def resetClock():
    hour_selected.set("01")
    minute_selected.set("00")
    second_selected.set("00")
    zone_selected.set("AM")
    time_now = getCurTime()
    date_selected.set_date(f"{int(time_now[3][5:7])}/{int(time_now[3][-2:])}/{int(time_now[3][:4])}")


def setAlarm():
    set_time = [hour_selected.get(), minute_selected.get(), second_selected.get(), zone_selected.get(),
                str(date_selected.get_date())]
    addAlarm(set_time)
    resetClock()


def deleteAlarm():
    for i in alarms.curselection():
        alarms.delete(i)
    setFileByList()


def checkAlarmTime():
    cur_time = getCurTime()
    cur_time = formatTime(cur_time)
    items = list(alarms.get(0, END))
    timeVar.set(cur_time[:-1])
    for i in range(len(items)):
        if cur_time == items[i]:
            alarms.delete(i)
            setFileByList()
            return True
    return False


def ringAlarm():
    if checkAlarmTime():
        mixer.music.load("alarm.mp3")
        mixer.music.play()
    root.after(1000, ringAlarm)


def stopAlarm():
    mixer.music.stop()


def resetTotal():
    resetClock()
    alarms.delete(0, END)
    setFileByList()
    setListBox()


if __name__ == '__main__':
    BACKGROUND = "#51eaf0"
    FOREGROUND = "#3bcbd1"
    mixer.init()

    # Making Window
    root = GUI(title="Alarm Clock", width=350, height=460, bg=BACKGROUND)

    # Alarms Frame
    list_frame = Frame(root)
    list_frame.pack(fill=X)
    head_label = Label(list_frame, text="My Alarms", font="lucida 14", bg=BACKGROUND)
    head_label.pack(fill=X)
    scroll = Scrollbar(list_frame)
    scroll.pack(side=RIGHT, fill=Y)
    alarms = Listbox(list_frame, yscrollcommand=scroll.set, bg=FOREGROUND, font="lucida 12")
    alarms.pack(fill=BOTH)
    setListBox()
    scroll.config(command=alarms.yview)

    # Set Alarm
    set_frame = Frame(root, bg=BACKGROUND)
    set_frame.pack(fill=X)

    # Time Frame
    time_frame = Frame(set_frame, bg=BACKGROUND)
    time_frame.grid(row=0, column=0)
    # Hour
    hourLabel = Label(time_frame, text="Hour", bg=BACKGROUND, font="lucida 12")
    hour_selected = StringVar()
    hour_selected.set("01")
    hourList = [f"{format2Digit(i)}" for i in range(1, 13)]
    hourBox = ttk.Combobox(time_frame, textvariable=hour_selected, values=hourList, state="readonly", width=10)
    # Minute
    minuteLabel = Label(time_frame, text="Minute", bg=BACKGROUND, font="lucida 12")
    minute_selected = StringVar()
    minute_selected.set("00")
    minuteList = [f"{format2Digit(i)}" for i in range(60)]
    minuteBox = ttk.Combobox(time_frame, textvariable=minute_selected, values=minuteList, state="readonly", width=10)
    # Second
    secondLabel = Label(time_frame, text="Second", bg=BACKGROUND, font="lucida 12")
    second_selected = StringVar()
    second_selected.set("00")
    secondList = [f"{format2Digit(i)}" for i in range(60)]
    secondBox = ttk.Combobox(time_frame, textvariable=second_selected, values=secondList, state="readonly", width=10)
    # Zone
    zoneLabel = Label(time_frame, text="Format", bg=BACKGROUND, font="lucida 12")
    zone_selected = StringVar()
    zone_selected.set("AM")
    zoneList = ["AM", "PM"]
    zoneBox = ttk.Combobox(time_frame, textvariable=zone_selected, values=zoneList, state="readonly", width=10)
    # Date
    dateLabel = Label(time_frame, text="Date", bg=BACKGROUND, font="lucida 12")
    date_selected = DateEntry(time_frame, selectmode="day", state="readonly")
    resetClock()
    date_selected.config(width=10)
    # Packing
    hourLabel.grid(row=0, column=0, padx=10)
    hourBox.grid(row=0, column=1, pady=10)
    minuteLabel.grid(row=1, column=0, padx=10)
    minuteBox.grid(row=1, column=1, pady=10)
    secondLabel.grid(row=2, column=0, padx=10)
    secondBox.grid(row=2, column=1, pady=10)
    zoneLabel.grid(row=3, column=0, padx=10)
    zoneBox.grid(row=3, column=1, pady=10)
    dateLabel.grid(row=4, column=0, padx=10)
    date_selected.grid(row=4, column=1, pady=10)

    # Button Frame
    btn_frame = Frame(set_frame, bg=BACKGROUND)
    btn_frame.grid(row=0, column=1, padx=40)
    # Set Button
    setAlarm = Button(btn_frame, text="Set Alarm", width=8, command=setAlarm)
    # Delete Button
    delAlarm = Button(btn_frame, text="Delete", width=8, command=deleteAlarm)
    # Reset Button
    resetAlarm = Button(btn_frame, text="Reset", width=8, command=resetTotal)
    # Stop Button
    stopAlarm = Button(btn_frame, text="Stop", width=8, command=stopAlarm)
    # Packing
    setAlarm.pack(pady=10)
    delAlarm.pack(pady=10)
    resetAlarm.pack(pady=10)
    stopAlarm.pack(pady=10)

    # Status Frame
    status_frame = Frame(root, bg=FOREGROUND)
    status_frame.pack(fill=X)
    timeVar = StringVar()
    timeVar.set("Loading...")
    timeBar = Label(status_frame, textvariable=timeVar, font="lucida 14", bg=FOREGROUND, anchor="e")
    timeBar.pack(fill=X, pady=5, padx=10)

    # Binding Events
    date_selected.bind("<<DateEntrySelected>>", formatDate)
    ringAlarm()

    # Starting
    root.start()
