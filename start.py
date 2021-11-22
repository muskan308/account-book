import tkinter
from cryptography.fernet import Fernet
import string
from tkinter import *
from tkinter import messagebox
from tkinter import font
from tkinter.ttk import*
from PIL import Image, ImageTk
from tkinter import PhotoImage
import pymysql

# cryptography of password
key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
k = Fernet(key)

# ***********sign in page**************


def open_a(bank):
    global var1, var2, var3, var4, var5, var6, var7, root,var8  # will be used globally
    root = Tk(className="Sign In")
    root.geometry("450x500")
    var1, var2, var3, var5, var6,var8 = StringVar(
    ), StringVar(), StringVar(), StringVar(), StringVar(),StringVar()
    var4 = StringVar()
    var7 = bank
    l1 = Label(root, text="Enter your details to Sign - In", font="Algerian")
    l1.place(x=63, y=20)
    l7 = Label(root, text="Enter Name", font=('serif', 10)).place(x=30, y=100)
    en6 = Entry(root, width=30, textvariable=var6)
    en6.place(x=200, y=100)
    l2 = Label(root, text="Enter UserId", font=(
        'serif', 10)).place(x=30, y=150)
    en1 = Entry(root, width=30, textvariable=var1)
    en1.place(x=200, y=150)
    l3 = Label(root, text="Enter Password",
               font=('serif', 10)).place(x=30, y=200)
    en2 = Entry(root, width=30, textvariable=var2)
    en2.place(x=200, y=200)
    l4 = Label(root, text="Confirm Password",
               font=('serif', 10)).place(x=30, y=250)
    en3 = Entry(root, width=30, textvariable=var3)
    en3.place(x=200, y=250)
    l5 = Label(root, text="Enter Account Number",
               font=('serif', 10)).place(x=30, y=300)
    en4 = Entry(root, width=30, textvariable=var4)
    en4.place(x=200, y=300)
    l6 = Label(root, text="Enter IFSC code",
               font=('serif', 10)).place(x=30, y=350)
    en5 = Entry(root, width=30, textvariable=var5)
    en5.place(x=200, y=350)
    l7 = Label(root, text="Enter Mobile number",
               font=('serif', 10)).place(x=30, y=400)
    en6 = Entry(root, width=30, textvariable=var8)
    en6.place(x=200, y=400)
    bu1 = Button(root, text="Sign In", command=do_entry).place(x=190, y=450)
    root.mainloop()

    # ***********signing in details to mysql************


def do_entry():

    n = bytes(var2.get(), 'utf-8')
    tok = k.encrypt(n)
    if(var1.get() == "" or var2.get() == "" or var3.get() == "" or var4.get() == "" or var5.get() == "" or var6.get() == "" or var8.get()==""):
        messagebox.showerror("Error", "Fill all the details")
    else:
        if(not(len(var4.get()) <= 18 and len(var4.get()) >= 9)):
            messagebox.showerror("Error", "Invalid Account Number")
        elif(var2.get() != var3.get()):
            messagebox.showerror("Error", "Password should match")
        elif(len(var8.get()) != 10 ):
            messagebox.showerror("Error","Enter valid mobile number")
        elif(len(var5.get()) !=11):
            messagebox.showerror("Error","Enter valid ifsc code")
        else:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='M1s2k3n4@',
                db='db'
            )
            cur = conn.cursor()
            sql1 = 'select * from login'
            cur.execute(sql1)
            out = cur.fetchall()
            for i in out:
                if(i[2] == var4.get()):
                    messagebox.showerror("Error","Account number already used")
                    break
            else:
                sql = 'insert into login values(%s,%s,%s,%s,%s,%s,%s)'
                val = (var1.get(), tok, var4.get(), var5.get(), var6.get(), var7,var8.get())
                cur.execute(sql, val)
                conn.commit()
                global m
                m = 'm'+var4.get()

                sql2 = 'create table ' + m + \
                '(date date,time time, type varchar(10),amount int,balance int)'

                cur.execute(sql2)
                conn.close()
                if(var7 == "SBI"):
                    sbi()
                elif(var7 == "PNB"):
                    pnb()
                elif(var7 == "HDFC"):
                    hdfc()
                elif(var7 == "COOP"):
                    coop()
                elif(var7 == "ICIC"):
                    icic()

                messagebox.showinfo("Confirmation", "Signed In successfully")
                root.destroy()
                open_b(var6.get())



            #***********change mobile number***********
def change():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='M1s2k3n4@',
        db='db',
    )
    cur = conn.cursor()
    sql = 'select * from login'
    cur.execute(sql)
    output = cur.fetchall()
    # print(output)
    for i in output:
        if vnum1.get() == i[6]:
            sql2 = 'update login set mobile = %s where mobile = %s'
            val = (vnum2.get(), vnum1.get())
            cur.execute(sql2,val)
            conn.commit()
            messagebox.showinfo("Confirmation","Number successfully updated")
            break
    else:
        print(vnum1.get())
        messagebox.showerror("Error","Wrong mobile number entered")
    conn.close()
           
           #************display mobile number change frame************

def num():
    global vnum1, vnum2
    vnum1 , vnum2 = StringVar(), StringVar()
    f = tkinter.Frame(home,bg = '#F36142')
    f.place(x =  130, y = 330)
    lb1 = tkinter.Label(f, text = "Old number",bg = '#F36142').grid(row = 0, column=0)
    en1  = tkinter.Entry(f,bg = '#fff',textvariable = vnum1).grid(row = 0, column=1)
    lb2 = tkinter.Label(f, text = "New number",bg = '#F36142').grid(row = 1,column=0)
    en2 = tkinter.Entry(f,bg = '#fff',textvariable = vnum2).grid(row = 1, column=1)
    f1 = tkinter.Frame(home, bg = '#F36142')
    f1.place(x = 205, y = 380)
    but = tkinter.Button(f1, text ="Change",bg = '#fff',command=change).pack(side=TOP)

    
            # *************home page*************


def main():
    v = messagebox.askokcancel(
        "Confirmation", "Do you really want to log out ?")
    if(v):
        home.destroy()
        main_p()
    else:
        pass

def open_b(name):
    global home
    home = Tk(className=" Account Book")
    home.geometry("450x450")
    home['background'] = '#F36142'
    lo1 = tkinter.Label(home, text="Welcome " + name.capitalize(),
                        font=('MS Serif', 15), bg='#fff', width=41, height=3).place(x=0, y=8)
    but3 = tkinter.Button(home, text="Display balance",
                          width=30, height=2, bg="#fff", command=balance)
    but3.place(x=120, y=140)
    but4 = tkinter.Button(home, text="Show transaction",
                          width=30, height=2, bg="#fff", command=transaction)
    but4.place(x=120, y=200)
    but5 = tkinter.Button(home, text="Update Phone number",
                          width=30, height=2, bg="#fff",command=num)
    but5.place(x=120, y=260)
    
    but6 = tkinter.Button(home, text="Log out", bg='white',
                          width=10, height=1, command=main).place(x=360, y=400)

    home.mainloop()


   # ************display balance****************


def balance():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='M1s2k3n4@',
        db='db',
    )
    cur = conn.cursor()
    sql = 'select * from '+m
    cur.execute(sql)
    output = cur.fetchall()
    if(not(output)):
        messagebox.showinfo("Message","No information to display")
    else:
        messagebox.showinfo("Balance", "Account balance is " + str(output[-1][4]))
    conn.close()

    # *************show transaction***************


def transaction():
    tran = Tk("Transactions")
    tran.geometry("450x450")
    lt1 = tkinter.Label(tran, text="Last 10 transactions are displayed ", font=(
        'algerian', 12)).place(x=65, y=20)
    # heading
    lb = tkinter.Label(tran, text="Date").place(x=50, y=70)
    lb = tkinter.Label(tran, text="Time").place(x=120, y=70)
    lb = tkinter.Label(tran, text="Type").place(x=190, y=70)
    lb = tkinter.Label(tran, text="Ammount").place(x=250, y=70)
    lb = tkinter.Label(tran, text="Balance").place(x=330, y=70)

    # connecting sql
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='M1s2k3n4@',
        db='db',
    )
    cur = conn.cursor()
    sql = 'select * from '+m
    cur.execute(sql)
    output = cur.fetchall()
    if(not(output)):
        messagebox.showinfo("Message","No transaction to display")
        tran.destroy()
    else:
    # fetching transactions using loop
        count = 100  # y dimension to display label
        for i in output[-1::-1]:
            # if(count > 370):
            #     break
            lb1 = tkinter.Label(tran, width=8, text=str(i[0])).place(x=30, y=count)
            lb1 = tkinter.Label(tran, width=6, text=str(
                i[1])).place(x=120, y=count)
            lb1 = tkinter.Label(tran, width=6, text=str(
                i[2])).place(x=190, y=count)
            lb1 = tkinter.Label(tran, width=6, text=str(
                i[3])).place(x=260, y=count)
            lb1 = tkinter.Label(tran, width=6, text=str(
                i[4])).place(x=330, y=count)
            count += 30

    conn.close()
    tran.mainloop()
    # ************checking for the login credentials************


def check():
    global m
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='M1s2k3n4@',
        db='db',
    )
    cur = conn.cursor()
    sql = 'select * from login'
    cur.execute(sql)
    output = cur.fetchall()
    for i in output:
        if(i[0] == v1.get()):
            n = bytes(i[1], 'utf-8')
            print()
            if(v2.get() == (k.decrypt(n)).decode('UTF-8')):
                top.destroy()
                n = i[2]
                m = 'm' + n
                open_b(i[4])
                break
            else:
                messagebox.showerror("Error", "Wrong password")
                break
    else:
        messagebox.showerror("Error", "UserId does not exists")

    conn.close()

    # **************** sbi*******************


def sbi():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='M1s2k3n4@',
        db='db',
    )
    cur = conn.cursor()
    fetch = 'select * from banks'
    cur.execute(fetch)
    output = cur.fetchall()
    acc = output[1][2]
    acc += 1
    sql = 'update banks set no_of_accounts = ' + str(acc)+' where sno = 2'
    cur.execute(sql)
    conn.commit()
    conn.close()

    # **************** pnb*******************


def pnb():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='M1s2k3n4@',
        db='db',
    )
    cur = conn.cursor()
    fetch = 'select * from banks'
    cur.execute(fetch)
    output = cur.fetchall()
    acc = output[0][2]
    acc += 1
    sql = 'update banks set no_of_accounts = ' + str(acc)+' where sno = 1'
    cur.execute(sql)
    conn.commit()
    conn.close()

    # **************** hdfc*******************


def hdfc():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='M1s2k3n4@',
        db='db',
    )
    cur = conn.cursor()
    fetch = 'select * from banks'
    cur.execute(fetch)
    output = cur.fetchall()
    acc = output[3][2]
    acc += 1
    sql = 'update banks set no_of_accounts = ' + str(acc)+' where sno = 4'
    cur.execute(sql)
    conn.commit()
    conn.close()

    # **************** coop*******************


def coop():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='M1s2k3n4@',
        db='db',
    )
    cur = conn.cursor()
    fetch = 'select * from banks'
    cur.execute(fetch)
    output = cur.fetchall()
    acc = output[2][2]
    acc += 1
    sql = 'update banks set no_of_accounts = ' + str(acc)+' where sno = 3'
    cur.execute(sql)
    conn.commit()
    conn.close()

    # **************** icic*******************


def icic():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='M1s2k3n4@',
        db='db',
    )
    cur = conn.cursor()
    fetch = 'select * from banks'
    cur.execute(fetch)
    output = cur.fetchall()
    acc = output[4][2]
    acc += 1
    sql = 'update banks set no_of_accounts = ' + str(acc)+' where sno = 5'
    cur.execute(sql)
    conn.commit()
    conn.close()

    # **************connector*************


def connect_sbi():
    banktk.destroy()
    open_a("SBI")


def connect_pnb():
    banktk.destroy()
    open_a("PNB")


def connect_hdfc():
    banktk.destroy()
    open_a("HDFC")


def connect_coop():
    banktk.destroy()
    open_a("COOP")


def connect_icic():
    banktk.destroy()
    open_a("ICIC")

    # **************select bank************


def bank():
    top.destroy()
    global banktk
    banktk = Tk(className="Select Bank")
    banktk.geometry("650x650")
    banktk['background'] = '#F36142'
    bl1 = tkinter.Label(banktk, text="Select your Bank",
                        font=('algerian', 25), bg='#F36142')
    bl1.place(x=170, y=20)

    bim1 = (Image.open("D:\python\project\images\sbi.png"))
    resize1 = bim1.resize((50, 50), Image.ANTIALIAS)
    bimg1 = ImageTk.PhotoImage(resize1)
    bb1 = tkinter.Button(banktk, text="  State Bank of India ", image=bimg1, compound=LEFT, width=300, font=(
        'Helvetica', 15), bg='#fff', height=50, bd=0, command=connect_sbi)
    bb1.place(x=170, y=100)

    bim2 = (Image.open("D:\python\project\images\pnb.png"))
    resize2 = bim2.resize((40, 40), Image.ANTIALIAS)
    bimg2 = ImageTk.PhotoImage(resize2)
    bb2 = tkinter.Button(banktk, text="  Punjab National Bank", image=bimg2, compound=LEFT, width=300, font=(
        'Helvetica', 15), bg='#fff', height=50, bd=0, command=connect_pnb)
    bb2.place(x=170, y=200)

    bim3 = (Image.open("D:\python\project\images\hdfc.png"))
    resize3 = bim3.resize((50, 50), Image.ANTIALIAS)
    bimg3 = ImageTk.PhotoImage(resize3)
    bb3 = tkinter.Button(banktk, text="            HDFC Bank  ", image=bimg3, compound=LEFT, width=300, font=(
        'Helvetica', 15), bg='#fff', height=50, bd=0, command=connect_hdfc)
    bb3.place(x=170, y=300)

    bim4 = (Image.open("D:\python\project\images\coop.png"))
    resize4 = bim4.resize((70, 30), Image.ANTIALIAS)
    bimg4 = ImageTk.PhotoImage(resize4)
    bb4 = tkinter.Button(banktk, text="  Cooperative Bank ", image=bimg4, compound=LEFT, width=300, font=(
        'Helvetica', 15), bg='#fff', height=50, bd=0, command=connect_coop)
    bb4.place(x=170, y=400)

    bim5 = (Image.open("D:\python\project\images\icic.png"))
    resize5 = bim5.resize((50, 50), Image.ANTIALIAS)
    bimg5 = ImageTk.PhotoImage(resize5)
    bb5 = tkinter.Button(banktk, text="           ICIC Bank  ", image=bimg5, compound=LEFT, width=300, font=(
        'Helvetica', 15), bg='#fff', height=50, bd=0, command=connect_icic)
    bb5.place(x=170, y=500)

    banktk.mainloop()

    # ***************main window*************


def main_p():

    global v1, v2, top
    top = Tk(className=" MULTIBANK SUPPORTIVE ACCOUNT BOOK")
    top.geometry("650x450")
    top['background'] = '#fff'
    canvas = tkinter.Canvas(top, width=550, height=550, bg='#fff')
    canvas.pack(fill="both", expand=True)
    im = (Image.open("D:\python\project\images\Multibank.jpg"))
    resize = im.resize((650, 450), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resize)
    canvas.create_image(0, 0, anchor="nw", image=img)
    # labels
    canvas.create_text(330, 60, text="Welcome to the Account Book",
                       font=("Algerian", 20), fill="black")

    v1, v2 = StringVar(), StringVar()  # variables to store data
    # first entry
    e1 = tkinter.Entry(top, textvariable=v1, width=30)
    e1.insert(0, "   Enter UserID")
    canvas.create_window(120, 150, window=e1)
    # second entry
    e2 = tkinter.Entry(top, textvariable=v2, width=30)
    e2.insert(0, "   Enter Password")
    canvas.create_window(120, 200, window=e2)
    button1 = tkinter.Button(top, text="Log in", command=check)
    button_window = canvas.create_window(80, 250, anchor="nw", window=button1)
    button2 = tkinter.Button(top, text="Sign in", command=bank)
    button_window = canvas.create_window(80, 300, anchor="nw", window=button2)
    top.mainloop()


main_p()
