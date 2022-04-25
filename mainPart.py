from student import *
from PIL import Image, ImageTk

headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)


# main UI
main = Tk()
main.title('SIM System')
main.geometry('700x400')
main.resizable(0, 0)

left_frame = Frame(main, bg='azure')
left_frame.place(x=0, relheight=1, relwidth=0.7)

right_frame = Frame(main, bg="snow2")
right_frame.place(relx=0.7, relheight=1, relwidth=0.3)

Label(left_frame, text="School Management \nSystem", font=('Jokerman',25),fg='DarkOrchid3',bg='azure').place(relx=0.15, rely=0.05)

image1 = Image.open("icon.png")
image1 = image1.resize((250, 250), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(image1)
panel = Label(left_frame, image=image1, bg='azure')
panel.image = image1
panel.place(x=120,y=120)


#Label(main, text="SCHOOL MANAGEMENT INFORMATION SYSTEM", font=headlabelfont, bg='cyan').pack(side=TOP, fill=X)

Button(right_frame, text='Quản lý sinh viên', font=labelfont, command=studentMana, width=15, bg="light sky blue").place(relx=0.1, rely=0.4)
Button(right_frame, text='Quản lý giảng viên', font=labelfont, command=studentMana, width=15, bg="light sky blue").place(relx=0.1, rely=0.55)


# Finalizing the GUI window
main.update()
main.mainloop()


