import datetime
from datetime import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar
import cx_Oracle

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)


# Connecting to the Oracle Database
connector = cx_Oracle.connect('sqlLab/1234@localhost') # 'userName/password@localhost'
cursor = connector.cursor()

# script to create sample table
# create table SINHVIEN (
#     masv varchar(10) not null primary key,
#     ho varchar(15) not null,
#     tenlot varchar(30) not null,
#     ten varchar(30) not null,
#     tenlop varchar(20) not null,
#     sdt varchar(20),
#     diachi varchar(50),
#     ngaysinh date,
#     email varchar(40),
#     nienkhoa number,
#     chuyenganh varchar(40),
#     CONSTRAINT fk_sinhvien_tenlop FOREIGN KEY (tenlop)
#     REFERENCES LOP(TENLOP) ON DELETE SET NULL DEFERRABLE
# );


def studentMana():
    # Creating the functions
    def reset_fields():
        id_var.get()
        first_name.get()
        mid_name.get()
        last_name.get()
        dob.get_date()
        gender.get()
        phone_number.get()
        address.get()
        email.get()
        class_name.get()
        major.get()
        entry_year.get()

        for i in ['id_var', 'first_name', 'mid_name', 'last_name', 'gender', 'phone_number', 'address',
                  'email', 'class_name', 'major', 'entry_year']:
            exec(f"{i}.set('')")
        dob.set_date(datetime.now().date())

    def reset_form():
        global tree
        tree.delete(*tree.get_children())

        reset_fields()

    def display_records():
        tree.delete(*tree.get_children())

        curr = cursor.execute('SELECT * FROM SINHVIEN')
        data = curr.fetchall()

        for records in data:
            tree.insert('', END, values=records)

    def add_record(id_val=None, isEdit=False):
        id = id_var.get()
        fname = first_name.get()
        mname = mid_name.get()
        lname = last_name.get()
        DOB = dob.get_date()
        genderr = gender.get()
        phone = phone_number.get()
        addr = address.get()
        mail = email.get()
        classn = class_name.get()
        maj = major.get()
        entryy = entry_year.get()

        if isEdit:
            if id != id_val:
                mb.showerror("Error!", "Can not change the student id")
            else:
                try:
                    cursor.execute(
                        "UPDATE SINHVIEN SET ho = :ho WHERE masv = :id", {'ho': fname,'id': id}
                    )
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET ho = :ho WHERE masv = :id", {'ho': fname,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET tenlot = :tenlot WHERE masv = :id", {'tenlot': mname,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET ten = :ten WHERE masv = :id", {'ten': lname,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET tenlop = :tenlop WHERE masv = :id", {'tenlop': classn,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET sdt = :sdt WHERE masv = :id", {'sdt': phone,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET diachi = :diachi WHERE masv = :id", {'diachi': addr,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET ngaysinh = :ngaysinh WHERE masv = :id", {'ngaysinh': DOB,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET email = :email WHERE masv = :id", {'email': mail,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET nienkhoa = :nienkhoa WHERE masv = :id", {'nienkhoa': entryy,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET chuyenganh = :chuyenganh WHERE masv = :id", {'chuyenganh': maj,'id': id})
                    connector.commit()
                    cursor.execute("UPDATE SINHVIEN SET gioitinh = :gioitinh WHERE masv = :id", {'gioitinh': genderr,'id': id})
                    connector.commit()
                    mb.showinfo('Record added', f"Record of {id} was successfully edited")
                    reset_fields()
                    display_records()
                except Exception as ex:
                    mb.showerror("Error!", ex)
        else:
            # if not id or not fname or not mname or not lname or not DOB or not genderr:
            if not id:
                mb.showerror('Error!', "Please fill all the missing fields!!")
            else:
                try:
                    cursor.execute(
                        "INSERT INTO SINHVIEN VALUES (:id,:fname,:mname,:lname,:classname,"
                        ":phone,:addr,:dob,:email,:entry,:major,:gender)",
                        {'id': id, 'fname': fname, 'mname': mname, 'lname': lname, 'classname': classn,
                         'phone': phone, 'addr': addr,'dob': DOB,
                         'email': mail, 'entry': entryy, 'major': maj, 'gender': genderr}
                    )
                    connector.commit()
                    mb.showinfo('Record added', f"Record of {id} was successfully added")
                    reset_fields()
                    display_records()
                except Exception as ex:
                    mb.showerror("Error!", ex)

    def remove_record():
        if not tree.selection():
            mb.showerror('Error!', 'Please select an item from the database')
        else:
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]

            tree.delete(current_item)

            cursor.execute('DELETE FROM SINHVIEN WHERE masv=%d' % selection[0])
            connector.commit()

            mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

            display_records()

    def search_record():
        tree.delete(*tree.get_children())
        try:
            search_key = search_val.get()
            search_field = search_var.get()
            search_map = {'MSSV': 'masv','Tên': 'ten','Tên lớp':'tenlop'}
            if search_key == '':
                display_records()
            else:
                if not search_field:
                    search_field = 'MSSV'
                #curr = cursor.execute('select * from sinhvien where %s = %s' % (search_map[search_field], search_key))
                curr = cursor.execute("select * from sinhvien where %s like :val" % search_map[search_field], {'val': search_key})
                data = curr.fetchall()
                for records in data:
                    tree.insert('', END, values=records)
        except Exception as ex:
            mb.showerror("Error!", ex)

    def edit_record():
        curr_item = tree.focus()
        values = tree.item(curr_item)
        selection = values["values"]

        id_var.set(selection[0])
        first_name.set(selection[1])
        mid_name.set(selection[2])
        last_name.set(selection[3])
        class_name.set(selection[4])
        phone_number.set(selection[5])
        address.set(selection[6])
        get_date = datetime.strptime(selection[7], "%Y-%m-%d %H:%M:%S").date()
        email.set(selection[8])
        entry_year.set(selection[9])
        major.set(selection[10])
        gender.set(selection[11])
        createPopupInfor(True, get_date)

    def view_record():
        pass

    def createPopupInfor(isEdit=False, date=None):
        global dob
        top_level = Toplevel()
        top_level.title("Create student infor")
        top_level.geometry('800x480')
        top_level.resizable(0, 0)
        # top_level.attributes('-topmost', False)
        Label(top_level, text="THÊM MỚI THÔNG TIN SINH VIÊN", font=headlabelfont, bg='cyan').pack(side=TOP,
                                                                                                         fill=X)

        Label(top_level, text="Mã số sinh viên", font=labelfont).place(relx=0.05, rely=0.15)
        Label(top_level, text="Họ", font=labelfont).place(relx=0.05, rely=0.25)
        Label(top_level, text="Tên lót", font=labelfont).place(relx=0.05, rely=0.35)
        Label(top_level, text="Tên", font=labelfont).place(relx=0.05, rely=0.45)
        Label(top_level, text="Giới tính", font=labelfont).place(relx=0.05, rely=0.55)
        Label(top_level, text="Ngày sinh", font=labelfont).place(relx=0.05, rely=0.65)
        Label(top_level, text="Số điện thoại", font=labelfont).place(relx=0.57, rely=0.15)
        Label(top_level, text="Địa chỉ", font=labelfont).place(relx=0.57, rely=0.25)
        Label(top_level, text="Email", font=labelfont).place(relx=0.57, rely=0.35)
        Label(top_level, text="Tên lớp", font=labelfont).place(relx=0.57, rely=0.45)
        Label(top_level, text="Chuyên ngành", font=labelfont).place(relx=0.57, rely=0.55)
        Label(top_level, text="Năm nhập học", font=labelfont).place(relx=0.57, rely=0.65)

        Entry(top_level, width=19, textvariable=id_var, font=entryfont).place(relx=0.25, rely=0.15)
        Entry(top_level, width=19, textvariable=first_name, font=entryfont).place(relx=0.25, rely=0.25)
        Entry(top_level, width=19, textvariable=mid_name, font=entryfont).place(relx=0.25, rely=0.35)
        Entry(top_level, width=19, textvariable=last_name, font=entryfont).place(relx=0.25, rely=0.45)
        #
        OptionMenu(top_level, gender, 'Male', "Female").place(relx=0.25, rely=0.55)
        #
        dob = DateEntry(top_level, font=("Arial", 12), width=15)
        dob.place(relx=0.25, rely=0.65)
        Entry(top_level, width=19, textvariable=phone_number, font=entryfont).place(relx=0.75, rely=0.15)
        Entry(top_level, width=19, textvariable=address, font=entryfont).place(relx=0.75, rely=0.25)
        Entry(top_level, width=19, textvariable=email, font=entryfont).place(relx=0.75, rely=0.35)
        Entry(top_level, width=19, textvariable=class_name, font=entryfont).place(relx=0.75, rely=0.45)
        Entry(top_level, width=19, textvariable=major, font=entryfont).place(relx=0.75, rely=0.55)
        Entry(top_level, width=19, textvariable=entry_year, font=entryfont).place(relx=0.75, rely=0.65)
        if isEdit:
            dob.set_date(date)
            id_val = id_var.get()
            Button(top_level, text='Xác nhận', font=labelfont, command= lambda : add_record(id_val, True), width=10).place(relx=0.45, rely=0.8)
        else:
            Button(top_level, text='Đồng ý', font=labelfont, command=add_record, width=10).place(relx=0.35, rely=0.8)
            Button(top_level, text='Nhập lại', font=labelfont, command=reset_fields, width=10).place(relx=0.54,
                                                                                                     rely=0.8)

    # Initializing the GUI window
    student_level = Toplevel()
    student_level.title('Student Management')
    student_level.geometry('1000x600')
    student_level.resizable(0, 0)
    # student_level.attributes('-topmost', True)

    # Creating the background and foreground color variables
    lf_bg = 'MediumSpringGreen'  # bg color for the left_frame
    cf_bg = 'PaleGreen'  # bg color for the center_frame

    # Creating the StringVar or IntVar variables
    id_var = StringVar()
    first_name = StringVar()
    mid_name = StringVar()
    last_name = StringVar()
    gender = StringVar()
    phone_number = StringVar()
    address = StringVar()
    email = StringVar()
    class_name = StringVar()
    major = StringVar()
    entry_year = StringVar()

    # Placing the components in the main window
    Label(student_level, text="STUDENT INFORMATION MANAGEMENT", font=headlabelfont, bg='cyan').pack(side=TOP,
                                                                                                           fill=X)

    left_frame = Frame(student_level, bg='light sky blue')
    left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

    right_frame = Frame(student_level, bg="Gray35")
    right_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.8)

    # Placing components in the left frame
    search_var = StringVar()
    search_val = StringVar()

    # Placing components in the center frame
    Button(left_frame, text='Thêm mới', font=labelfont, command=lambda: createPopupInfor(), width=15).place(relx=0.1,
                                                                                                            rely=0.25)
    Button(left_frame, text='Chỉnh sửa', font=labelfont, command=edit_record, width=15).place(relx=0.1, rely=0.35)
    Button(left_frame, text='Xóa sinh viên', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.45)
    Label(left_frame, text="Tìm theo", font=labelfont, bg='light sky blue').place(relx=0.1, rely=0.55)
    OptionMenu(left_frame, search_var, "MSSV", "Tên", "Tên lớp").place(relx=0.52, rely=0.55)
    Entry(left_frame, width=20, textvariable=search_val, font=entryfont).place(relx=0.1, rely=0.63)
    # Placing components in the right frame
    Label(right_frame, text='Students Records', font=headlabelfont, bg='dodger blue', fg='LightCyan').pack(side=TOP,
                                                                                                         fill=X)
    Button(left_frame, text='Tìm kiếm', font=labelfont, command=search_record, width=10).place(relx=0.35, rely=0.7)


    tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                        columns=(
                        'Student ID', 'First Name', 'Mid Name', 'Last Name', 'Class Name', 'Phone', 'Address', 'Date of Birth',
                        'Email', 'Entry year', 'Major', 'Gender'))


    X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
    Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
    X_scroller.pack(side=BOTTOM, fill=X)
    Y_scroller.pack(side=RIGHT, fill=Y)

    tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

    tree.heading('Student ID', text='MSSV', anchor=CENTER)
    tree.heading('First Name', text='Họ', anchor=CENTER)
    tree.heading('Mid Name', text='Tên lót', anchor=CENTER)
    tree.heading('Last Name', text='Tên', anchor=CENTER)
    tree.heading('Class Name', text='Tên lớp', anchor=CENTER)
    tree.heading('Address', text='Địa chỉ', anchor=CENTER)
    tree.heading('Phone', text='SĐT', anchor=CENTER)
    tree.heading('Date of Birth', text='Ngày sinh', anchor=CENTER)
    tree.heading('Email', text='Email', anchor=CENTER)
    tree.heading('Entry year', text='Năm nhập học', anchor=CENTER)
    tree.heading('Major', text='Chuyên ngành', anchor=CENTER)
    tree.heading('Gender', text='Giới tính', anchor=CENTER)

    tree.column('#0', width=0, stretch=NO)
    tree.column('#1', width=60, stretch=NO)
    tree.column('#2', width=50, stretch=NO)
    tree.column('#3', width=60, stretch=NO)
    tree.column('#4', width=60, stretch=NO)
    tree.column('#5', width=80, stretch=NO)
    tree.column('#6', width=80, stretch=NO)
    tree.column('#7', width=140, stretch=NO)
    tree.column('#8', width=80, stretch=NO)
    tree.column('#9', width=120, stretch=NO)
    tree.column('#10', width=80, stretch=NO)
    tree.column('#11', width=80, stretch=NO)
    tree.column('#12', width=80, stretch=NO)

    tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
    display_records()
