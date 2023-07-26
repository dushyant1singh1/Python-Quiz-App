from tkinter import *
import sqlite3
import os #os.system(file name)
class  quiz :   
    def __init__(self):
        self.enext=1
        self.mvnext=1
        self.tvnext=1
        self.eli=[]
        self.mli=[]
        self.tli=[]
        
        
        #c.execute('CREATE TABLE first1(name TEXT,reg INT, section INT, )')
        
        self.window=Tk()
        self.window.config(bg='blue')
        self.window.title("quiz module")
        frame1=Frame(self.window)
        frame1.pack()
        self.v1=IntVar()

        menubar=Menu(self.window)
        self.window.config(menu=menubar)

        operationMenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Operation",menu=operationMenu)
        operationMenu.add_command(label='Show Data',command=self.show)
        operationMenu.add_separator()

        
        self.window.geometry("600x400")
        self.name=StringVar()#name entry
        message1=Message(frame1, text="Name", width="100")
        message1.grid(row=1,column=1)
        entryname1= Entry(frame1, textvariable=self.name)
        entryname1.grid(row=1,column=2)
        
        self.registration=StringVar()#registration number
        message2=Message(frame1, text="Registration No." ,width="100")
        entryname2=Entry(frame1, textvariable=self.registration)
        message2.grid(row=2,column=1)
        entryname2.grid(row=2,column=2)

        self.section=StringVar()
        message3=Message(frame1, text="Section: ",width="100")
        entryname3=Entry(frame1, textvariable=self.section)
        message3.grid(row=3,column=1)
        entryname3.grid(row=3,column=2)

        message4=Message(frame1, text="Difficulty:  ",width="100")
        easy = Radiobutton(frame1, text ='Easy', variable=self.v1, value=1)
        midium=Radiobutton(frame1, text='Medium' , variable=self.v1, value=2)
        tough=Radiobutton(frame1, text='Tough' , variable=self.v1, value=3)
        message4.grid(row=4,column=1)
        easy.grid(row=4,column=2)
        midium.grid(row=5,column=2)
        tough.grid(row=6,column=2)

        btgetname=Button(frame1, text='Get Name' ,command=self.upload,fg='white',bg='black')
        btgetname.grid(row=7,column=2)
        self.window.mainloop()
        


    def show(self):
        root1=Tk()
        self.s1=StringVar(root1)
        self.g1=IntVar(root1)
        Entry(root1,textvariable=self.s1).grid(row=2,column=2)  
        Message(root1,text='Enter the registration no.',fg='red').grid(row=2,column=1)
        Message(root1,text='Choose one option',fg='red').grid(row=3,column=2)
        Radiobutton(root1,text='Result',variable=self.g1,value=1,fg='red').grid(row=4,column=2)
        Radiobutton(root1, text='Student record',variable=self.g1,value=2,fg='red').grid(row=5,column=2)
        Button(root1,text='Get',command=self.showdata,bg='green').grid(row=6,column=2)
    def showdata(self):
        s=int(self.s1.get())
        print(s)
        d=sqlite3.connect('project.db')
        if self.g1.get()==1:
            a=d.execute('select * from records where reg=?',(s))
            for i in a:
                print(i)
        else:
            a=d.execute('select * from first where reg=?',(self.s1.get()))
            for i in a:
                print(i)
            
            
            

    def upload(self):
        self.reg=self.registration.get()
        if self.name.get()=='' or self.section.get()=='' or self.registration.get()=='' or self.v1.get()==0 :
            self.window.destroy()
            self.__init__()
            print("you must fill all entries before taking quiz")
        else:
            c=sqlite3.connect('project.db')
            print('database connected succefully')
            c.execute('INSERT INTO first VALUES(?,?,?,?)',(self.name.get(),self.section.get(),self.registration.get(),self.v1.get()))
            c.commit()
            if self.v1.get()==1:
                self.easy(1)
            elif self.v1.get()==2:
                self.medium(1)
            elif self.v1.get()==3:
                self.tough(1)
            c.close()
# easy module
    def easy(self,i):
        if i==1:
            self.window.destroy()
        self.ewindow=Tk()
        self.ewindow.geometry("600x400")
        self.v2=IntVar(self.ewindow)
        d=sqlite3.connect('questions.db')
        #d.execute('CREATE TABLE questions(no INT PRIMARY KEY,ques text,op1 text, op2 text, op3 text)')
        if i==2:
            a=d.execute('SELECT distinct * FROM questions where no=2')
        elif i==1:
            a=d.execute('select distinct * from questions where no=1')
        else:
            a=d.execute('select distinct * from questions where no=3')
        #d.execute('insert into questions values(3,"what type of database python support?","My Sql","sqlite3","all of the above")')
        #d.commit()
        # 1, 'what type of language python is?', 'soft', 'high level', 'hard')
        BO=Button(self.ewindow,text='submit',command=self.efnext)
        for j in a:
            message=Message(self.ewindow,text=j[0])
            message.grid(row=1,column=1)
            message1=Message(self.ewindow,text=j[1],width="300").grid(row=1,column=2)
            op1=Radiobutton(self.ewindow,text=j[2],variable=self.v2,value=1).grid(row=2,column=2)
            op2=Radiobutton(self.ewindow,text=j[3],variable=self.v2,value=2).grid(row=3,column=2)
            op3=Radiobutton(self.ewindow,text=j[4],variable=self.v2,value=3).grid(row=4,column=2)
            if i==3:
                BO.grid(row=5,column=3)
            else:
                b1=Button(self.ewindow,text='Next',command=self.efnext).grid(row=5,column=3)
        
    def efnext(self):
        if self.v2.get()==0:
            self.eli.append(0)
            print(self.v2.get())
        else:
            self.eli.append(self.v2.get())
        self.ewindow.destroy()
        if self.enext==3:
            self.result()
        else:    
            self.enext+=1
            self.easy(self.enext)

    def result(self):
        d=sqlite3.connect('project.db')
        #d.execute('create table records(reg int,no int)')
        self.root=Tk()
        self.root.geometry("600x400")
        count=0
        li=[1,2,3]
        for i in range(0,3,1):
            if self.eli[i]==li[i]:
                count+=1
        self.j=IntVar(self.root)
        d.execute('insert into records values(?,?)',(self.reg,count))
        d.commit()
        message=Message(self.root,text="your result is "+str(count),fg="blue",font="Verdana 25 bold").grid(row=1,column=2)
        bo=Radiobutton(self.root,text='Yes',variable=self.j,value=1).grid(row=3,column=2)
        bu=Radiobutton(self.root,text='No',variable=self.j,value=2).grid(row=3,column=3)
        b=Button(self.root,text="submit",command=self.new).grid(row=4,column=2)


        
# medium module
    def medium(self,i):
        if i==1:
            self.window.destroy()
        self.mwindow=Tk()
        self.v3=IntVar(self.mwindow)
        d=sqlite3.connect('question.db')
        self.mwindow.geometry("600x400")
        #d.execute('CREATE TABLE mediumquestions(no INT PRIMARY KEY, ques text,op1 text,op2 text,op3 text )')
        #d.execute('INSERT INTO mediumquestions values(1,"what are right functions in python from following","get()","setup()","printf()")')
        #d.execute('INSERT INTO mediumquestions values(2,"what are right syntax for taking an integer value in python","eval(input())","int(input())","all above")')
        #d.execute('INSERT INTO mediumquestions values(3,"what type of database we can use in python","sqlite3","mongodb","all of the above")')
        #d.commit()
        if i==1:
            a=d.execute('select * from mediumquestions where no=1')
        elif i==2:
            a=d.execute('select * from mediumquestions where no=2')
        else:
            a=d.execute('select * from mediumquestions where no=3')
        for j in a:
            message=Message(self.mwindow,text=j[0])
            message.grid(row=1,column=1)
            message1=Message(self.mwindow,text=j[1],width='300').grid(row=1,column=2)
            op1=Radiobutton(self.mwindow,text=j[2],variable=self.v3,value=1).grid(row=2,column=2)
            op2=Radiobutton(self.mwindow,text=j[3],variable=self.v3,value=2).grid(row=3,column=2)
            op3=Radiobutton(self.mwindow,text=j[4],variable=self.v3,value=3).grid(row=4,column=2)
            if i==3:
                bu=Button(self.mwindow,text='submit',command=self.mnext).grid(row=5,column=3)
            else:
                b1=Button(self.mwindow,text='Next',command=self.mnext).grid(row=5,column=3)
    def mnext(self):
        self.mli.append(self.v3.get())
        self.mwindow.destroy()
        if self.mvnext==3:
            self.mediumresult()
        else:
            self.mvnext+=1
            self.medium(self.mvnext)
    def mediumresult(self):
        self.root=Tk()
        self.root.geometry("600x400")
        count=0
        li=[1,3,3]
        self.j=IntVar(self.root)
        for i in range(0,3,1):
            if self.mli[i]==li[i]:
                count+=1
        message=Message(self.root,text='your result is '+str(count),fg="blue",font="Verdana 25 bold").grid(row=1,column=2)
        bo=Radiobutton(self.root,text='Yes',variable=self.j,value=1).grid(row=3,column=2)
        bu=Radiobutton(self.root,text='No',variable=self.j,value=2).grid(row=3,column=3)
        b=Button(self.root,text="submit",command=self.new).grid(row=4,column=2)



    def tough(self,i):
        if i==1:
            self.window.destroy()
        self.twindow=Tk()
        self.twindow.geometry("600x400")
        d=sqlite3.connect('question.db')
        self.to=IntVar(self.twindow)
        #d.execute('CREATE TABLE tough(no INT PRIMARY KEY,ques text, op1 text, op2 text, op3 text)')
        #d.execute('INSERT INTO tough values(1,"what symbol you can use to comment one line of code","*","//","#")')
        #d.execute('INSERT INTO tough values(2,"How would you cast the string variable a that is equal to 2 into the integer 2?","int(a)","integer(a)","casttoint(a)")')
        #d.commit()
        if i==1:
            a=d.execute('select * from tough where no=1')
        else:
            a=d.execute('select * from tough where no=2')
        for j in a:
            message=Message(self.twindow,text=j[0]).grid(row=1,column=1)
            message1=Message(self.twindow,text=j[1]).grid(row=1,column=2)
            op1=Radiobutton(self.twindow,text=j[2],variable=self.to,value=1)
            op1.grid(row=2,column=2)
            op2=Radiobutton(self.twindow,text=j[3],variable=self.to,value=2)
            op2.grid(row=3,column=2)
            op3=Radiobutton(self.twindow,text=j[4],variable=self.to,value=3)
            op3.grid(row=4,column=2)
            if i==2:
                bu=Button(self.twindow,text='Submit',command=self.tnext).grid(row=5,column=3)
            else:
                bo=Button(self.twindow,text='Next',command=self.tnext).grid(row=5,column=3)
        
        
    def tnext(self):
        self.tli.append(self.to.get())
        if self.tvnext==2:
            self.twindow.destroy()
            self.toughresult()
        else:
            self.twindow.destroy()
            self.tvnext+=1
            print(self.tli)
            self.tough(self.tvnext)
    def toughresult(self):
        self.root=Tk()
        count=0
        li=[3,1]
        print(self.tli)
        self.root.geometry("400x400")
        for i in range(0,2,1):
            if self.tli[i]==li[i]:
                count+=1
        self.j=IntVar(self.root)
        message=Message(self.root,text='your result is '+str(count),fg="blue",font="Verdana 15 bold").grid(row=1,column=2)
        me=Message(self.root, text="will you want to take another quiz").grid(row=2,column=2)
        
        bo=Radiobutton(self.root,text='Yes',variable=self.j,value=1).grid(row=3,column=2)
        bu=Radiobutton(self.root,text='No',variable=self.j,value=2).grid(row=3,column=3)
        b=Button(self.root,text="submit",command=self.new).grid(row=4,column=2)    
    def new(self):
        if self.j.get()==1:
            self.__init__()
            self.root.destroy()
        elif self.j.get()==2:
            self.root.destroy()
quiz()


