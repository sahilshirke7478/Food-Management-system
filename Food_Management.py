# Food Management System
import prettytable
import mysql.connector
import re
import maskpass
import datetime

x=datetime.datetime.now()
class Food:
    # list of users
    # users=["sahil","sameer","kamble","shinde","Aman","Atul"]
    # users={"sahil":"123"}
    mydb=mysql.connector.connect(host="localhost",user="root" ,database="food" ,password="root",buffered=True)
    cursor= mydb.cursor()
    def create_table(self):
        self.cursor.execute("create table if not exists register(id int auto_increment primary key,name varchar(125),password int(125),email varchar(100),mobile bigint,date_and_time datetime)")
        self.cursor.execute("create table if not exists foodlist(fid int auto_increment primary key,fname varchar(100),fprice int(255));")
        self.cursor.execute("create table if not exists Admin(id int,Name varchar(100),password int(50))")
        self.cursor.execute("create table if not exists orders(id int(40) auto_increment primary key,user varchar(50),fname varchar(50))")
        self.cursor.execute("select * from Admin")
        self.check = self.cursor.fetchall()
        # print(self.check)
        if self.check==[]:
            self.cursor.execute("insert ignore into Admin values(%s,%s,%s)",(1,"Sahil",1234))
            self.mydb.commit()
    # cursor.execute("select * from Admin;")

    # method for adding new user
    def regi(self):
        while True:
            # id1=int(input("Enter your id:"))
            name=input("Enter your name to register : ")
            if name.isdigit()!= True:
                password = input("Create password : ")
                if password.isdigit():
                    email=input("Enter Your E-mail: ")
                    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                    if (re.fullmatch(regex, email)):
                        number = input("Enter Your Mobile Number")
                        if len(number) == 10 and number.isdigit():
                            print("                     Welcome",name)
                            db = "insert into register(name,password,email,mobile,date_and_time) values('{}','{}','{}','{}','{}')".format(name, int(password),email,int(number),x)
                            self.cursor.execute(db)
                            self.mydb.commit()
                            break
                        else:
                            print("Please Enter Valid 10 digit mobile number.And try again")
                            print()
                    else:
                        print("Please enter valid email. And try again")
                        print()
                else:
                    print("Please Enter Numbers Only. And try again.")
                    print()
            else:
                print("Enter Valid Name (Don't Include Numbers). And try again")
                print()

    # login method for Hotel
    def hotel_login(self):
        self.id=input("Enter your ID:    ")
        self.Name2 = input("Enter your name :   ")
        self.password2 = input("Enter your password :    ")
        self.cursor.execute("select * from Admin where id=%s",(self.id,))
        var = self.cursor.fetchone()
        try:
            if int(self.password2) == var[2] and self.Name2 == var[1] and int(self.id)==var[0]:
                print("*"*20,"Welcome","*"*20)

                while(True):
                    print("\n1.DisplayDish \n2.AddMenu \n3.DeleteMenu  \n4.Orderdish \n5.Users  \n6:exit \n")
                    choice2=(input("Enter your choice : "))
                    if choice2=="1":
                        self.displayDish()
                    elif choice2=="2":
                        # self.Ad=input("Enter Dish name :  ")
                        # self.fid=input("Enter Dish Id: ")
                        self.addMenu()
                    elif choice2=="3":
                        # self.dish=input("Enter Dish name : ")
                        self.deleteMenu()
                    elif choice2=="4":
                        self.orderdish_list()

                    elif choice2=="5":
                        self.cursor.execute("select * from register")
                        print(prettytable.from_db_cursor(self.cursor))

                    elif choice2=="6":
                        self.home()
                    else:
                        print("Enter valid choice")
            else:
                print("Enter valid Name or Password")
        except:
            print("Enter valid input")

    # login method for users
    def user_login(self):
        self.Name1=input("Enter your name : ")
        self.password1=input("Enter password : ")
        self.cursor.execute("select * from register where name=%s and password=%s",(self.Name1,int(self.password1)))
        var=self.cursor.fetchone()
        # print(self.Name1==var[1])
        # print(self.password1 == var[2])
        # try:
        if self.Name1 == var[1] and int(self.password1) == var[2]:
            while(True):
                print("\n1:DisplayDish  \n2:Orderdish  \n3:exit \n")
                choice1=(input("Enter your choice : "))
                if choice1=="1":
                    self.displayDish()
                elif choice1=="2":
                    self.Orderdish()
                elif choice1=="3":
                    print("Thank you for visiting the restaurnt ")
                    break
                else:
                    print("Enter valid choice ")
        # except:
        #     print('invalid name and password')



    def displayDish(self):
        print("We have following dish in our hotel")
        self.cursor.execute("select * from foodlist")
        # self.cursor.fetchall()
        print(prettytable.from_db_cursor(self.cursor))
    # def orderdish(self,dish):
    #     self.cursor.execute("create table if not exists orderdish(user_name varchar(125),foodlist varchar(125));")
    #     query6="insert into orderdish('{}','{}')".format(self.Name1,dish)
    #     self.cursor.execute(query6)
    #     self.mydb.commit()
    def orderdish_list(self):
        self.cursor.execute("select * from orders")
        print(prettytable.from_db_cursor(self.cursor))

    def Orderdish(self):
        total = 0
        while True:
            dish = input("Enter Dish name to order   :     ")
            # query2="delete from foodlist where fname='{}'".format(dish)
            self.cursor.execute("select Fname from foodlist")
            fname = self.cursor.fetchall()
            lst=[x[0] for x in fname]
            if dish in lst:
                query3="insert into orders(user,fname) values('{}','{}')".format(self.Name1,dish)
                self.cursor.execute("select Fprice from foodlist where Fname=%s",(dish,))
                # self.cursor.execute(query2)
                bill=self.cursor.fetchone()
                self.cursor.execute(query3)
                self.mydb.commit()
                yn= input("Do you want to order more (y/n):       ")
                total += bill[0]
                # print(total)
                # print("You can take your order after some minutes. And your total bill is:", total)
                if yn == "y":
                    # total += bill[0]
                    pass
                elif yn=="n":
                    print("You can take your order after some minutes. And your total bill is:", total)
                    break
                else:
                    print("Please Enter Valid choice")
            else:
                print()
                print("This Dish is not available right now. Try something else.")
                print()



    # def canceldish(self, dish):
    #         print("your dish has been cancel suucefully ")
    #         # print(self.lendDict)
    #     else:
    #         print("There is no dish with these name ")

    def addMenu(self):
        s.displayDish()
        fname=input("Enter Food Name to Add on Menu   :     ")
        fprice = input("Enter Food price to Add on Menu   :     ")
        if fname.isalpha() and fprice.isdigit():
            bd = "insert into foodlist(fname,fprice) values('{}','{}')".format(fname,int(fprice))
            self.cursor.execute(bd)
            self.mydb.commit()
            print()
            print("*-"*10,"Dish has been added to the dish list","-*"*10)
        else:
            print()
            print("x-"*10,"Invalid Food Name or Price","-x"*10)

    def deleteMenu(self):
        s.displayDish()
        fid = input("Enter Food ID to Delete   :    ")
        self.cursor.execute("select fid from foodlist where fid=%s",(fid,))
        check=self.cursor.fetchone()
        if check != None:
            if check[0] == int(fid):
                if fid.isdigit():
                    query1 = "delete from foodlist where fid='{}'".format(int(fid))
                    self.cursor.execute(query1)
                    self.mydb.commit()
                    print("*-"*10,"The Food has been removed from the menu","-*"*10)
                else:
                    print("x-"*10,"Please Enter Valid ID","-x"*10)
            else:
                print("This ID doesn't Exists")
        else:
            print("This ID doesn't Exists")

    def home(self):
        print("\n Welcome to Madhuram  Restaurant")
        while(True):
            print("\n1:hotel_Login \n2:User_login \n3:Register \n4.exit \n")
            choice=(input("Enter your choice : "))
            if choice=="1":
                self.hotel_login()
            elif choice=="2":
                self.user_login()
            elif choice=="3":
                self.regi()
            elif choice=="4":
                exit()
            else:
                print("Enter valid choice ")

s=Food()
s.create_table()
s.home()
# s.orderdish_list()
# s.drop()

