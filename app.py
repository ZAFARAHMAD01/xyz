from flask import Flask, request,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import math
import random
from random import randint
from trycourier import Courier
import re
from tkinter import messagebox
import subprocess
# import subprocess
# subprocess.call(['echo', 'Hello, world!', '|', 'javascript', 'alert(prompt(\'This is an alert box\'))'])


con=mysql.connector.connect(user='root',password='',host='localhost',database='data')
if con.is_connected():
    print('connected succesff')
else:
    print('not succesffully')
con.close()

app=Flask(__name__)
@app.route("/",methods=['POST','GET'])
def gezal():
    global namee
    global pinn2
    global ac
    namee=0
    ac=request.form.get("account_number")
    pinn=request.form.get("pin_code")
    if request.method=='POST':
        if request.form.get("account_number")=='' or request.form.get("pin_code")=='':
            pass
        else:
            try:
                con=mysql.connector.connect(user='root',password='',host='localhost',database='data')
                cur=con.cursor()
            except:
                pass
            query='select * from student3 where ACC_NO=%s'
            cur.execute(query,[ac])
            row=cur.fetchall()
            print(row)
            if row=='' or row==None or row==[]:
                namee=1
            else:
                pinn2=(row[-1][-2])
                print(pinn2)
                if int(pinn)==pinn2:
                    return render_template("BCD.html")
                else:
                    message_from_python = "PINCODE INCORRECT TRY AGAIN"
                    return render_template('logg.html', message=message_from_python)
        ac=request.form.get("account_number")
        pinn=request.form.get("pin_code")
        print(ac)
        print(pinn)
    return render_template("index.html" ,name=namee)

@app.route("/z",methods=['POST','GET'])
def var():
    global otp
    global name
    global pinn
    global email
    global bal
    global pinn3
    global deb 
    global newadd3
    if request.method=='POST':    
        def random_with_N_digits(n):
            range_start = 10**(n-1)
            range_end = (10**n)-1
            return randint(range_start, range_end)
        otp=random_with_N_digits(3)
        print(otp)
        name=request.form.get("name")
        pinn=request.form.get("pincode")
        con_pinn=request.form.get("confirm_pincode")
        email=request.form.get('email')
        bal=request.form.get('bal')
        if pinn==con_pinn:
            client = Courier(auth_token="pk_prod_8N981PNEQC4Q5HPACB24V1RVKAEW")
            resp = client.send_message(message={"to": {"email":"{}".format(email)},
                                                "content": {"title": "ATM VARIFICATION YOUR OTP!",
                                                            "body": "WELCOME TO CODES WARS ATM {{otp}}"},"data":{
                                                                "otp": "YOUR ATM OTP IS: {}".format(otp)}})
            print(name)
            print(pinn)
            print(con_pinn)
            print(bal)
            print(email)
            return render_template("otpverifactions.html")  
        else:
            message_from_python ="password missmatched"
            return render_template('createnew.html', message=message_from_python)
    return render_template("createnew.html")
@app.route("/submit",methods=['POST','GET'])
def getvalue():
    if request.method=='POST':
        x=request.form.get('otp')
        print(otp)
        print(x)
        if int(x)==otp:
            print('True')
            try:
                def random_with_N_digits(n):
                    range_start = 10**(n-1)
                    range_end = (10**n)-1
                    return randint(range_start, range_end)
                acc_no=('7'+str(random_with_N_digits(10)))
                con=mysql.connector.connect(user='root',password='',host='localhost',database='data')
                cur=con.cursor()
                query='insert into student3(NAME,ACC_NO,EMAIL,PINCODE,BALANCE) values(%s,%s,%s,%s,%s)'
                cur.execute(query,[name,acc_no,email,pinn,bal])
                con.commit()
                con.close()
                print('successfull')
                client = Courier(auth_token="pk_prod_8N981PNEQC4Q5HPACB24V1RVKAEW")
                resp = client.send_message(message={"to": {"email":"{}".format(email)},
                                                                "content": {"title": "NEW ACCOUNT CREATED SUCCESSFULLY!",
                                                                "body": "WELCOME TO CODES WARS ATM {{otp}}"},"data":{
                                                                    "otp": "YOUR NAME: {},YOUR ACC NO: {},YOUR PIN: {},YOUR INITIAL AMOUNT: {}".format(name,acc_no,pinn,bal)}})
                return render_template("otpverifactions.html")
            except:
                    pass

        else:
            message_from_python = "INCORRECT OTP MISMATCHED OTP INAVLID"
            return render_template('createnew.html', message=message_from_python)
            print('false')
    return render_template("otpverifactions.html")

@app.route("/zz",methods=['POST','GET'])
def credit():
    if request.method=='POST':
        if request.form.get("credit")=='':
            pass
        else:
            try:
                con=mysql.connector.connect(user='root',password='',host='localhost',database='data')
                cur=con.cursor()
            except:
                pass
            query='select * from student3 where ACC_NO=%s'
            cur.execute(query,[ac])
            row=cur.fetchall()
            print(row)

            ####start
            pinn2=(row[-1][-1])
            crr=request.form.get('credit')
            print(pinn2)
            print(crr)
            newadd=int(crr)+int(pinn2)
            print(float(newadd))
            if crr!='' or crr!=None:
                query = "UPDATE student3 SET BALANCE = '{}' WHERE ACC_NO = %s".format(float(newadd))
                cur.execute(query,[ac])
                con.commit()
                con.close()
                client = Courier(auth_token="pk_prod_8N981PNEQC4Q5HPACB24V1RVKAEW")
                resp = client.send_message(message={"to": {"email":"{}".format(email)},
                                                                "content": {"title": "CREDITED AMOUNT!",
                                                                "body": "CODE WARS ATM TRANSECTION{{otp}}"},"data":{
                                                                    "otp": "CODE WAR ATM: {},DEAR,{} YOUR ACC: {}, AVL BAL :{}".format(crr,name,ac,newadd)}})
                return render_template('index.html')
            else:
                pass ##message
    return render_template('credit.html')

@app.route("/zzz",methods=['POST','GET'])
def debit():
    if request.method=='POST':
        if request.form.get("debit")=='':
            pass
        else:
            try:
                con=mysql.connector.connect(user='root',password='',host='localhost',database='data')
                cur=con.cursor()
            except:
                pass
            query='select * from student3 where ACC_NO=%s'
            cur.execute(query,[ac])
            row=cur.fetchall()
            print(row)

            ####start
            pinn3=(row[-1][-1])
            deb=request.form.get('debit')
            print(pinn3)
            print(deb)
            if int(pinn3)>=int(deb):
                newadd2=int(pinn3)-int(deb)
                print(float(newadd2))
                if deb!='' or deb!=None:
                    query = "UPDATE student3 SET BALANCE = '{}' WHERE ACC_NO = %s".format(float(newadd2))
                    cur.execute(query,[ac])
                    con.commit()
                    con.close()
                    client = Courier(auth_token="pk_prod_8N981PNEQC4Q5HPACB24V1RVKAEW")
                    resp = client.send_message(message={"to": {"email":"{}".format(email)},
                                                                "content": {"title": "DEBITED AMOUNT!",
                                                                "body": "CODE WARS ATM TRANSECTION{{otp}}"},"data":{
                                                                    "otp": "CODE WAR ATM: {},DEAR,{} YOUR ACC: {}, AVL BAL :{}".format(deb,name,ac,newadd2)}})
                    return render_template('index.html')
                else:
                    pass ##message
            else:
                message_from_python = "INSUFFICIENT AMOUNT"
                return render_template('debit.html', message=message_from_python)
                
    return render_template('debit.html')

@app.route("/history",methods=['POST','GET'])
def his():
    if request.method=='POST':
        if request.form.get('credit')=='':
            con=mysql.connector.connect(user='root',password='',host='localhost',database='data')
            cur=con.cursor()
            query='select * from student3 where ACC_NO=%s'
            cur.execute(query,[ac])
            row=cur.fetchall()
            print(row)
    return render_template('history.html')
        


if __name__== "__main__":
    app.run(debug=True)

