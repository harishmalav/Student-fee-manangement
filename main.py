from flask import Flask ,render_template,redirect,url_for,session,request
import pymysql
import time
import os




from mylib import *

app=Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER']='./static/photos'

@app.route('/')
def index():
    return render_template("home.html")

@app.route("/autherror")
def autherror():
    return render_template("autherror.html")


@app.route("/Contant_us")
def Contant_us():
    return render_template("Contant_us.html")


@app.route("/About_us")
def About_us():
    return render_template("About_us.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    if 'email' in session:
        session.pop('email',None)
        session.pop('usertype',None)
        return redirect('login')
    else:
        return redirect('login')



@app.route("/login",methods=['GET','POST'])
def login ():
    if request.method=="POST":
        cn=pymysql.connect(host="localhost",user="root",port=3306,db="student",password="",autocommit=True)
        cur=cn.cursor()
        email=request.form['T1']
        password=request.form['T2']
        sql="select * from logindata where email='"+email+"' and password='"+password+"'"
        cur.execute(sql)
        n=cur.rowcount
        if n==1:
            data=cur.fetchone()
            usertype=data[2]
            sr_no=data[0]

            session["usertype"]=usertype
            session['email']=email
            if usertype=='student':
                session['email']=email
            if usertype=='admin':
                return redirect(url_for("Admin_home"))
            elif usertype=='accountant':
                return redirect(url_for("Accountant_home"))
            elif usertype=='student':
                return redirect(url_for("Student_dashboard"))
            else:
                return redirect(url_for('autherror'))
        else:
            return render_template("login.html",msg="data not matched")
    else:
        return render_template("login.html")

@app.route('/Admin_home')
def Admin_home():
    if "email" in session:
        usertype = session['usertype']
        email = session['email']
        if usertype=='admin':
            photo = check_photo(email)
            cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
            cur=cn.cursor()
            sql="select * from admin where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount

            if n==1:
                data=cur.fetchall()
                return render_template("Adminhome.html",data=data,photo=photo)
            else:
                return render_template("Adminhome.html",msg="data not found")
        else:
            return redirect("autherror")
    else:
        return redirect("autherror")


@app.route("/Accountant_home")
def Accountant_home():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='accountant':
            photo=check_photo(email)
            cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
            cur = cn.cursor()
            sql = "select * from accountant where email='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n == 1:
                data = cur.fetchall()
                return render_template("AccountantHome.html",data=data,photo=photo)
            else:
                return render_template("AccountantHome.html",msg="data not found")
        else:
            return redirect('autherror')
    else:
        return redirect('login')



@app.route("/admin_reg",methods=['GET','POST'])
def admin_reg():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                ut='admin'
                cn=pymysql.connect(host="localhost",user="root",port=3306,db="student",password="",autocommit=True)
                cur1= cn.cursor()
                cur2 = cn.cursor()

                name = request.form['T1']
                contact = request.form['T2']
                address = request.form['T3']
                email = request.form['T4']
                password = request.form['T5']
                confirm_password = request.form['T6']
                sql1 = "insert into admin values ('"+name+"','"+contact+"','"+address+"','"+email+"')"
                sql2 = "insert into logindata values ('"+email+"','"+password+"','"+ut+"')"

                cur1.execute(sql1)
                cur2.execute(sql2)
                n1 = cur1.rowcount
                n2 = cur2.rowcount
                if n1 == 1 and n2 == 1:
                    return render_template("Admin_Reg.html", msg="Admin Registration successfull")
                else:
                    return render_template("Admin_Reg.html", msg="Admin Registration unsuccessfull")
            else:
                return render_template("Admin_Reg.html")
        else:
            return redirect(url_for('login'))





@app.route('/Admin_show')
def Admin_show():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=="admin":
            cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
            cur = cn.cursor()
            sql = "select * from admin"
            cur.execute(sql)
            n = cur.rowcount
            if n > 0:
                record= cur.fetchall()
                return render_template("Admin_show.html", data=record)
            else:
                return render_template("Admin_show.html", msd="data not found")
        else:
            return redirect(url_for('Admin_home'))
    else:
        return redirect('login')



@app.route("/Edit_Admin_profile")
def Edit_Admin_proflie():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="",autocommit=True)
                cur = cn.cursor()
                sql = "select * from admin where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    records = cur.fetchall()
                    return render_template("Edit_Admin_profile.html", data=records)
                else:
                    return render_template("Edit_Admin_profile.html", msg="data not found")
        else:
           return redirect('autherror')
    else:
         return redirect('login')

@app.route("/Edit_Admin1_profile",methods=['GET','POST'])
def Edit_Admin1_profile():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="",autocommit=True)
                cur = cn.cursor()
                name=request.form['T1']
                contact=request.form['T2']
                address=request.form['T3']
                sql="update admin set name='"+name+"',contact='"+contact+"',address='"+address+"' where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template("Edit_Admin_profile.html",msg="data Edited")
                else:
                    return render_template("Edit_Admin_profile.html",msg="Data not Edited")
            else:
                return render_template("Edit_Admin_profile.html")
        else:
            return redirect('Admin_home')
    else:
        return redirect('login')



@app.route("/Accountant_Reg",methods=['GET','POST'])
def Accountant_Reg():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method == "POST":
                try:
                    cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
                    cur1 = cn.cursor()
                    cur2=cn.cursor()
                    ut='accountant'
                    em_id=request.form['T1']
                    name=request.form['T2']
                    contact=request.form['T3']
                    address=request.form['T4']
                    gender=request.form['T5']
                    email=request.form['T6']
                    password=request.form['T7']
                    confirm_pass=request.form['T8']
                    sql1="insert into accountant values('"+em_id+"','"+name+"','"+contact+"','"+address+"','"+gender+"','"+email+"')"
                    sql2="insert into logindata values('"+email+"','"+password+"','"+ut+"')"

                    cur1.execute(sql1)
                    cur2.execute(sql2)

                    n1=cur1.rowcount
                    n2=cur2.rowcount

                    if n1==1 and n2==1:
                        return render_template("Accountant_Reg.html",msg="data saved")
                    else:
                        return render_template("Accountant_Reg.html",mag="data not saved")
                except pymysql.err.IntegrityError:
                    return render_template("Accountant_Reg.html",msg="User Already exist")
            else:
                return render_template("Accountant_Reg.html")
        else:
            return redirect('Admin_home')
    else:
        return redirect('login')


@app.route("/ManageAccountant",methods=['GET','POST'])
def ManageAccountant():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
            cur = cn.cursor()
            sql="select * from accountant"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                records=cur.fetchall()
                return render_template("Manage_Accountant.html",data=records)
            else:
                return render_template("Manage_Accountant.html",msg="data not found")
        else:
            return redirect('Admin_home')
    else:
        return redirect('login')



@app.route("/Edit_Accountant",methods=['GET','POST'])
def Edit_Accountant():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
                cur = cn.cursor()
                em=request.form['T1']
                sql="select * from accountant where email='"+em+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    records=cur.fetchall()
                    return render_template("Edit_Accountant.html",data=records)
                else:
                    return render_template("Edit_Accountant.html",msg="data not found")
            else:
                return redirect('ManageAccountant')
        else:
            return redirect('autherror')
    else:
        return redirect('login')



@app.route("/Edit_Accountant1",methods=['GET','POST'])
def Edit_Accountant1():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
                cur = cn.cursor()
                em_id=request.form['T1']
                name=request.form['T2']
                contact=request.form['T3']
                address=request.form['T4']
                gender=request.form['T5']
                em=request.form['T6']
                sql="update accountant set em_id='"+em_id+"',name='"+name+"',contact='"+contact+"',address='"+address+"',gender='"+gender+"' where email='"+em+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template("Edit_Accountant.html",msg="data Edited")
                else:
                    return render_template("Edit_Accountant.html",msg="data not Edited")
            else:
                return redirect('ManageAccountant')
        else:
            return redirect('autherror')
    else:
        return redirect('login')



@app.route("/Delete_accountant",methods=['GET','POST'])
def Delete_accountant():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
                cur = cn.cursor()
                em=request.form['T2']
                sql="select * from accountant where email='"+em+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    records=cur.fetchall()
                    return render_template("Delete_accountant.html",data=records)
                else:
                    return render_template("Delete_accountant.html",msg="data not found")
            else:
                return redirect('ManageAccountant')
        else:
            return redirect('Admin_home')
    else:
        return redirect('login')



@app.route("/Delete_Accountant1",methods=['GET','POST'])
def Delete_Accountant1():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="",autocommit=True)
                cur = cn.cursor()
                em_id=request.form['T1']
                name=request.form['T2']
                em=request.form['T6']
                sql="delete from accountant where email='"+em+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template("Delete_accountant.html",msg="data deleted")
                else:
                    return render_template("Delete_accountant.html",msg="data not delete")
            else:
                return redirect('ManageAccountant')
        else:
            return redirect('Admin_home')
    else:
        return redirect('login')


@app.route("/Student_Reg",methods=['GET','POST'])
def Student_Reg():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='accountant':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
                cur = cn.cursor()
                cur1 = cn.cursor()
                sr_no=request.form['T1']
                name=request.form['T2']
                father_name=request.form['T3']
                mother_name=request.form['T4']
                gender=request.form['T5']
                address = request.form['T6']
                contact=request.form['T7']
                dob=request.form['T8']
                category=request.form['T9']
                state=request.form['T10']
                em=request.form['T11']
                password=request.form['T12']
                confirm_password=request.form['T13']
                usertype='student'
                sql="insert into studentdata values('"+sr_no+"','"+name+"','"+father_name+"','"+mother_name+"','"+gender+"','"+address+"','"+contact+"','"+dob+"','"+category+"','"+state+"','"+em+"')"
                sql1="insert into logindata values('"+sr_no+"','"+password+"','"+usertype+"')"
                cur.execute(sql)
                cur1.execute(sql1)
                n=cur.rowcount
                n1=cur1.rowcount
                if n==1 and n1==1:
                    return render_template("Student_Reg.html",msg="data saved")
                else:
                    return render_template("Student_Reg.html",msg="data not saved")
            else:
                return render_template("Student_Reg.html")
        else:
            return redirect("Accountant_home")


@app.route("/Manage_Student",methods=['GET','POST'])
def Manage_Student():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='accountant':
            cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password='', autocommit=True)
            cur = cn.cursor()
            sql="select * from studentdata"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                records=cur.fetchall()
                return render_template("Manage_Student.html",data=records)
                print("data")
            else:
                return render_template("Manage_Student.html",msg="data not found")
        else:
            return redirect('Accountant_home')
    else:
        return redirect('login')


@app.route('/Edit_student',methods=['GET','POST'])
def Edit_student():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='accountant':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
                cur = cn.cursor()
                sr_no=request.form['T1']
                sql="select * from studentdata where sr_no='"+sr_no+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchall()
                    return render_template("Edit_Student.html",data=data)
                else:
                    return render_template("Edit_Student.html",msg="data not found")
            else:
                return redirect('Manage_Student')
        else:
            return redirect('Accountant_home')
    else:
        return redirect('login')


@app.route("/Edit_Student1",methods=['GET','POST'])
def Edit_Student1():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='accountant':
            if request.method == "POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="",autocommit=True)
                cur = cn.cursor()
                sr_no=request.form['T1']
                name=request.form['T2']
                address=request.form['T3']
                contact=request.form['T4']
                em=request.form['T5']
                sql="update studentdata set sr_no='"+sr_no+"',name='"+name+"',address='"+address+"',contact='"+contact+"' where email='"+em+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template("Edit_Student.html",msg="data Edited")
                else:
                    return render_template("Edit_Student.html",mag="data not Edited")
            else:
                return redirect('Manage_Student')
        else:
            return redirect('Accountant_home')
    else:
        return redirect('login')


@app.route("/Change_Password",methods=['GET','POST'])
def Change_Password():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='accountant':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="",autocommit=True)
                cur = cn.cursor()

                old_password=request.form['T1']
                new_password=request.form['T2']

                sql = "update logindata set password='"+new_password+"' where email='"+email+"'and password='"+old_password+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template("Change_Password.html",msg="password changed")
                else:
                    return render_template("Change_Password.html",msg="password not changed")
            else:
                return render_template("Change_Password.html")
        else:
            return redirect('Accountant_home')
    else:
        return redirect('login')





@app.route("/Show_Student",methods=['GET','POST'])
def Show_Student():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
            cur = cn.cursor()
            sql="select * from studentdata"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                records=cur.fetchall()
                return render_template("Show_Student.html",data=records)
            else:
                return render_template("Show_Student.html",msg="data not found")
        else:
            return redirect('admin_home')
    else:
        return redirect('login')

@app.route("/Edit_student2",methods=['GET','POST'])
def Edit_student2():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
                cur = cn.cursor()
                sr_no=request.form['T1']
                sql = "select * from studentdata where sr_no='" + sr_no + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    data = cur.fetchall()
                    return render_template("Edit_Student1.html", data=data)
                else:
                    return render_template("Edit_Student1.html", msg="data not found")
            else:
                return redirect('Show_Student')
        else:
            return redirect('Admin_home')
    else:
         return redirect('login')




@app.route("/Edit_Student3",methods=['GET','POST'])
def Edit_Student3():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method == "POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="",autocommit=True)
                cur = cn.cursor()
                sr_no=request.form['T1']
                name=request.form['T2']
                address=request.form['T3']
                contact=request.form['T4']
                em=request.form['T5']
                sql="update studentdata set sr_no='"+sr_no+"',name='"+name+"',address='"+address+"',contact='"+contact+"' where email='"+em+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template("Edit_Student1.html",msg="data Edited")
                else:
                    return render_template("Edit_Student1.html",mag="data not Edited")
            else:
                return redirect('Show_Student')
        else:
            return redirect('Admin_home')
    else:
        return redirect('login')



@app.route("/Delete_Student",methods=['GET','POST'])
def Delete_Student():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="", autocommit=True)
                cur = cn.cursor()
                sr_no=request.form['T1']
                sql="select * from studentdata where sr_no='"+sr_no+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    records=cur.fetchall()
                    return render_template("Delete_Student.html",data=records)
                else:
                    return render_template("Delete_Student.html",msg="data not found")
            else:
                return redirect('Show_Student')
        else:
            return redirect('Admin_home')
    else:
        return redirect('login')



@app.route("/Delete_Student1",methods=['GET','POST'])
def Delete_Student1():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="",autocommit=True)
                cur = cn.cursor()
                sr_no = request.form['T1']
                name = request.form['T2']
                em = request.form['T5']
                sql = "delete from studentdata where sr_no='"+sr_no+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    return render_template("Delete_Student.html",msg="data deleted")
                else:
                    return render_template("Delete_Student.html",msg="data not delete")
            else:
                return redirect('Show_Student')
        else:
            return redirect('Admin_home')
    else:
        return redirect('login')



@app.route("/Accountant_photo")
def Accountant_photo():
    return render_template("Photo_upload_accountant.html")


@app.route("/Accountant_photo1",methods=['GET','POST'])
def Accountant_photo1():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='accountant':
            if request.method=="POST":
                file=request.files['AC1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cn=pymysql.connect(host='localhost',port=3306,user='root',password='',db='student',autocommit=True)
                    cur=cn.cursor()
                    sql="insert into photodata values('"+email+"','"+filename+"')"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                        return render_template("Photo_upload_accountant1.html",result="success")
                    else:
                        return render_template("Photo_upload_accountant1.html",result="failure")
                else:
                    return redirect(url_for('autherror'))
            else:
                return redirect(url_for('autherror'))





@app.route('/Change_Accountant_Photo')
def Change_Accountant_Photo():
    if 'email' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='accountant':
            photo = check_photo(email)
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student', autocommit=True)
            cur = conn.cursor()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                os.remove("./static/photos/"+photo)
                return render_template('Change_Accountant_Photo.html',data="success")
            else:
                return render_template('Change_Accountant_Photo.html', data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))



@app.route("/Student_dashboard",methods=['GET','POST'])
def Student_dashboard():
    if 'email' in session:
        sr_no=session['email']
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                sr_no=request.form['T1']
                sql = "select * from studentdata where sr_no='"+sr_no+"'"
                cur.execute(sql)
                n=cur.rowcount
                print(n)
                if n==1:
                    data=cur.fetchall()
                    photo = student_photo(sr_no)
                    cur2 = conn.cursor()
                    sql2 = "SELECT * FROM course WHERE sr_no='" + sr_no + "'"
                    cur2.execute(sql2)
                    n=cur2.rowcount
                    j="d"
                    print(j)
                    data1 = cur2.fetchall()
                    if n>0:
                        courses=[]
                        for d in data1:
                            paid=course_paid(d[0],d[4])
                            due=int(d[2])-int(paid)
                            aa=[d[0],d[1],d[2],d[3],d[4],paid,due]
                            courses.append(aa)
                        cur3=conn.cursor()
                        sql3 = "SELECT * FROM fee WHERE sr_no='" + sr_no + "'"
                        cur3.execute(sql3)
                        n4=cur3.rowcount
                        print(n4)
                        if n>0:
                            data4=cur3.fetchall()
                            fee=0
                            for d in data1:
                                fee=fee + d[2]
                            print(fee)
                            deposit=0
                            for i in data4:
                                deposit=deposit + i[3]
                            print(deposit)
                            due=fee-deposit
                            print(due)
                            return render_template("Student_deshboard.html",data=data,fee=fee,deposit=deposit,due=due, data1=courses,data4=data4,j="k",photo=photo)
                        else:
                            return render_template("Student_deshboard.html",data=data,j="k",data1=courses,photo=photo)
                    else:
                        return render_template("Student_deshboard.html",data=data,j="k",l="l",photo=photo)
                else:
                    return render_template("Student_deshboard.html",j="k")
            else:
                return redirect(url_for("autherror"))
        elif usertype=='accountant':
            if request.method=="POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                sr_no=request.form['T1']
                sql = "select * from studentdata where sr_no='"+sr_no+"'"

                cur.execute(sql)
                n=cur.rowcount

                if n==1:
                    data=cur.fetchall()
                    print(data)
                    photo = student_photo(sr_no)

                    cur2=conn.cursor()
                    sql2="SELECT * FROM course WHERE sr_no='"+sr_no+"'"
                    cur2.execute(sql2)
                    n=cur2.rowcount

                    print(n)
                    if n>0:
                        data1=cur2.fetchall()
                        courses=[]
                        for d in data1:
                            paid=course_paid(d[0],d[4])
                            due=int(d[2])-int(paid)
                            aa=[d[0],d[1],d[2],d[3],d[4],paid,due]
                            courses.append(aa)
                        cur3=conn.cursor()
                        sql3 = "SELECT * FROM fee WHERE sr_no='" + sr_no + "'"
                        cur3.execute(sql3)
                        n4=cur3.rowcount
                        print(n4)
                        if n>0:
                            data4=cur3.fetchall()
                            return render_template("Student_deshboard.html",data=data,data1=courses,data4=data4,j="j",photo=photo)
                        else:
                            return render_template("Student_deshboard.html",data=data,j="j",photo=photo)
                    else:
                        return render_template("Student_deshboard.html",data=data,j="j",photo=photo)
                else:
                    return render_template("Student_deshboard.html",j="j")
        elif usertype=="student":
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',
                                   autocommit=True)
            cur = conn.cursor()
            print(sr_no)
            print(sr_no)
            print(sr_no)

            sql = "select * from studentdata where sr_no='" + sr_no + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n == 1:
                data = cur.fetchall()
                print(data)
                photo = student_photo(sr_no)

                cur2 = conn.cursor()
                sql2 = "SELECT * FROM course WHERE sr_no='" + sr_no + "'"
                cur2.execute(sql2)
                n = cur2.rowcount

                print(n)
                if n > 0:
                    data1 = cur2.fetchall()
                    courses = []
                    for d in data1:
                        paid = course_paid(d[0], d[4])
                        due = int(d[2]) - int(paid)
                        aa = [d[0], d[1], d[2], d[3], d[4], paid, due]
                        courses.append(aa)
                    cur3 = conn.cursor()
                    sql3 = "SELECT * FROM fee WHERE sr_no='" + sr_no + "'"
                    cur3.execute(sql3)
                    n4 = cur3.rowcount
                    print(n4)
                    if n > 0:
                        data4 = cur3.fetchall()
                        return render_template("Student_deshboard.html", data=data, data1=courses, j="u", data4=data4,
                                               photo=photo)
                    else:
                        return render_template("Student_deshboard.html", data=data, j="u", photo=photo)
                else:
                    return render_template("Student_deshboard.html", data=data, j="u", photo=photo)
            else:
                return render_template("Student_deshboard.html", j="u")
        else:
            return redirect('autherror')
    else:
        return redirect('login')



@app.route("/Add_course",methods=['GET','Post'])
def Add_course():
    if 'email' in session:
        usertype=session['usertype']
        if usertype == 'admin':

            if request.method == "POST":

                sr_no = request.form['T3']
                print(sr_no)
                return render_template("Add_course.html", sid=sr_no,j="k")
            else:
                return redirect('Student_deshboard')

        elif usertype=='accountant':
            if request.method == "POST":
                sr_no = request.form['T5']
                print(sr_no)
                return render_template("Add_course.html", sid=sr_no,j="j")
            else:
                return redirect('Student_deshboard')
        else:
            return redirect('autherror')
    else:
        return redirect('login')



@app.route("/Add_course1",methods=['GET','Post'])
def Add_course1():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                course_id=0
                sr_no=request.form['T1']
                course_name=request.form['T2']
                fee=request.form['T3']
                start_date=request.form['T4']
                sql="insert into course value('"+str(course_id)+"','"+course_name+"','"+fee+"','"+start_date+"','"+sr_no+"')"
                cur.execute(sql)
                n=cur.rowcount
                print(n)
                if n==1:
                    return render_template("Add_course.html",msg="data saved",j="k")
            else:
                return render_template("Add_course.html",msg="data not saved",j="k")
        elif usertype=='accountant':
            if request.method=="POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                course_id=0
                sr_no=request.form['T1']
                course_name=request.form['T2']
                fee=request.form['T3']
                start_date=request.form['T4']
                sql="insert into course value('"+str(course_id)+"','"+course_name+"','"+fee+"','"+start_date+"','"+sr_no+"')"
                cur.execute(sql)
                n=cur.rowcount
                print(n)
                if n==1:
                    return render_template("Add_course.html",msg="data saved",j="j")
            else:
                return render_template("Add_course.html",msg="data not saved",j="j")
        else:
            return redirect('autherror')
    else:
        return redirect('login')



@app.route("/fee_deposit",methods=['GET','POST'])
def fee_deposit():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()

                course_id=request.form['T2']
                sql="select * from course where course_id='"+course_id+"'"
                cur.execute(sql)
                data=cur.fetchone()
                sr_no = data[4]
                return render_template("fee_deposit.html" ,course_id=course_id,sr_no=sr_no,d="d",j="k")
            else:
                return render_template("fee_deposit.html",j="k")
        elif usertype=='accountant':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()

                course_id=request.form['T2']
                sql="select * from course where course_id='"+course_id+"'"
                cur.execute(sql)
                data=cur.fetchone()
                sr_no = data[4]
                return render_template("fee_deposit.html" ,course_id=course_id,sr_no=sr_no,d="d",j="j")
            else:
                return render_template("fee_deposit.html",j="j")

        else:
            return redirect('autherror')
    else:
        return redirect('login')


@app.route("/fee_deposit1",methods=['GET','POST'])
def fee_deposit1():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student', autocommit=True)
                cur = conn.cursor()
                t_no=0
                st_id=request.form['T2']
                course_id = request.form['T3']
                amount = request.form['T4']
                deposit_date = request.form['T5']
                remark = request.form['T6']
                sql="insert into fee values('"+str(t_no)+"','"+str(st_id)+"','"+str(course_id)+"','"+str(amount)+"','"+str(deposit_date)+"','"+str(remark)+"' )"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template("fee_deposit.html",msg="data save",j="k" )
                else:
                    return render_template("fee_deposit.html",msg="data not saved",j="k")
            else:
                return render_template("fee_deposit.html",j="k")
        elif usertype=='accountant':
            if request.method=="POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student', autocommit=True)
                cur = conn.cursor()
                t_no=0
                st_id=request.form['T2']
                course_id = request.form['T3']
                amount = request.form['T4']
                deposit_date = request.form['T5']
                remark = request.form['T6']
                sql="insert into fee values('"+str(t_no)+"','"+str(st_id)+"','"+str(course_id)+"','"+str(amount)+"','"+str(deposit_date)+"','"+str(remark)+"' )"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template("fee_deposit.html",msg="data save",j="j" )
                else:
                    return render_template("fee_deposit.html",msg="data not saved",j="j")
            else:
                return render_template("fee_deposit.html",j="j")
        else:
            return redirect('autherror')
    else:
        return redirect('login')


@app.route("/Edit_course",methods=['GET','POST'])
def Edit_course():
    if 'email' in session:
        email = session['email']
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                course_id=request.form['T2']
                sql="select * from course where course_id='"+course_id+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template("Edit_course.html",data=data)
                else:
                    return render_template("Edit_course.html",msg="data not found")
            else:
                return render_template("Student_deshboard.html")
        else:
            return redirect('autherror')
    else:
        return redirect('login')


@app.route("/Edit_course1",methods=['GET','POST'])
def Edit_course1():
    if 'email' in session:
        email = session['email']
        usertype =  session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                course_id = request.form['T1']
                course_name = request.form['T2']
                fee = request.form['T3']
                start_date = request.form['T4']
                sr_no = request.form['T5']
                sql = "update course set course_name='"+course_name+"',fee='"+fee+"',start_date='"+start_date+"',sr_no='"+sr_no+"' where course_id='"+course_id+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    return render_template("Edit_course.html",msg="data edit")
                else:
                    return render_template("Edit_course.html",msg="data not edit")
            else:
                return render_template("Student_deshboard.html")
        else:
            return redirect('autherror')
    else:
        return redirect('login')

@app.route("/Delete_course",methods=['GET','POST'])
def Delete_course():
    if 'email' in session:
        email = session['email']
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()

                course_id = request.form['T2']

                sql="select * from course where course_id='"+course_id+"'"

                cur.execute(sql)
                n=cur.rowcount

                if n==1:

                    records = cur.fetchall()
                    return render_template("Delete_course.html",data=records)
                else:
                    return render_template("Delete_course.html",msg="data not found")
            else:
                return render_template("Student_deshboard.html")
        else:
            return redirect('autherror')
    else:
        return redirect('login')

@app.route("/Delete_course1",methods=['GET','POST'])
def Delete_course1():
    if 'email' in session:
        email = session['email']
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                course_id = request.form['T1']
                course_name = request.form['T2']
                fee = request.form['T3']
                start_date = request.form['T4']
                sr_no = request.form['T5']
                sql = "delete from course where course_id='"+course_id+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    return render_template("Delete_course.html",msg="data deleted")
                else:
                    return render_template("Delete_course.html",msg="data not delete")
            else:
                return render_template("Student_deshboard.html")
        else:
            return redirect("autherror")
    else:
        return redirect('login')






@app.route("/Edit_transaction",methods=['GET','POST'])
def Edit_transaction():
    if 'email' in session:
        email = session['email']
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                t_no=request.form['T1']
                sql="select * from fee where t_no='"+t_no+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template("Edit_transaction.html",data=data)
                else:
                    return render_template("Edit_transaction.html",msg="data not found")
            else:
                return render_template("Student_deshboard.html")
        else:
            return redirect('autherror')
    else:
        return redirect('login')


@app.route("/Edit_transaction1",methods=['GET','POST'])
def Edit_transaction1():
    if 'email' in session:
        email = session['email']
        usertype =  session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                t_no = request.form['T1']
                sr_no = request.form['T2']
                course_id = request.form['T3']
                amount = request.form['T4']
                deposit_date = request.form['T5']
                remark = request.form['T6']
                sql = "update fee set sr_no='"+sr_no+"',course_id='"+course_id+"',amount='"+amount+"',deposit_date='"+deposit_date+"',remark='"+remark+"' where t_no='"+t_no+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    return render_template("Edit_transaction.html",msg="data edit")
                else:
                    return render_template("Edit_transaction.html",msg="data not edit")
            else:
                return render_template("Student_deshboard.html")
        else:
            return redirect('autherror')
    else:
        return redirect('login')




@app.route("/Delete_transaction",methods=['GET','POST'])
def Delete_transaction():
    if 'email' in session:
        email = session['email']
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()

                t_no = request.form['T1']

                sql="select * from fee where t_no='"+t_no+"'"

                cur.execute(sql)
                n=cur.rowcount

                if n==1:

                    records = cur.fetchall()
                    return render_template("Delete_transaction.html",data=records)
                else:
                    return render_template("Delete_transaction.html",msg="data not found")
            else:
                return render_template("Student_deshboard.html")
        else:
            return redirect('autherror')
    else:
        return redirect('login')


@app.route("/Delete_transaction1",methods=['GET','POST'])
def Delete_transaction1():
    if 'email' in session:
        email = session['email']
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                t_id = request.form['T1']
                sr_no = request.form['T2']
                course_id = request.form['T3']
                amount = request.form['T4']
                deposit_date = request.form['T5']
                remark = request.form['T6']

                sql = "delete from fee where t_no='"+t_id+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    return render_template("Delete_transaction.html",msg="data deleted")
                else:
                    return render_template("Delete_transaction.html",msg="data not delete")
            else:
                return render_template("Student_deshboard.html")
        else:
            return redirect("autherror")
    else:
        return redirect('login')


@app.route("/photo_upload_student",methods=['POST','GET'])
def photo_upload_student():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method == "POST":
                sr_no = request.form['T5']
                return render_template("photo_upload_student.html",sr_no=sr_no)
            else:
                return redirect("autherror")
        elif usertype=='accountant':
            if request.method == "POST":
                sr_no = request.form['T5']
                return render_template("photo_upload_student.html", sr_no=sr_no)
            else:
                return redirect("autherror")
        else:
            return redirect("autherror")
    else:
        return redirect("autherror")

@app.route("/photo_upload_student1",methods=['GET','POST'])
def photo_upload_student1():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                file=request.files['S1']
                sr_no = request.form['T5']
                print(sr_no)
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cn=pymysql.connect(host='localhost',port=3306,user='root',password='',db='student',autocommit=True)
                    cur=cn.cursor()
                    sql="insert into student_photo values('"+sr_no+"','"+filename+"')"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                        return render_template("photo_upload_student1.html",result="success")
                    else:
                        return render_template("photo_upload_student1.html",result="failure")
                else:
                    return redirect(url_for('autherror'))
            else:
                return redirect(url_for('autherror'))
        elif usertype=='accountant':
            if request.method=="POST":
                file=request.files['S1']
                sr_no = request.form['T5']
                print(sr_no)
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cn=pymysql.connect(host='localhost',port=3306,user='root',password='',db='student',autocommit=True)
                    cur=cn.cursor()
                    sql="insert into student_photo values('"+sr_no+"','"+filename+"')"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                        return render_template("photo_upload_student1.html",result="success")
                    else:
                        return render_template("photo_upload_student1.html",result="failure")
                else:
                    return redirect(url_for('autherror'))
            else:
                return redirect(url_for('autherror'))
        else:
            return redirect('autherror')
    else:
        return redirect('login')

@app.route("/Change_student_Photo",methods=['GET','POST'])
def Change_student_Photo():
    if 'email' in session:
        email = session['email']
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method=="POST":
                sr_no = request.form['T5']
                photo = student_photo(sr_no)
                os.remove("./static/photos/"+photo)
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                sql = "delete from student_photo where sr_no='" + sr_no + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    return render_template('photo_upload_student.html', sr_no=sr_no)
                else:
                    return render_template('photo_upload_student.html', msg="failure")
            else:
                return redirect("autherror")
        elif usertype=='accountant':
            if request.method=="POST":
                sr_no = request.form['T5']
                photo = student_photo(sr_no)
                os.remove("./static/photos/"+photo)
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                sql = "delete from student_photo where sr_no='" + sr_no + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    return render_template('photo_upload_student.html', sr_no=sr_no)
                else:
                    return render_template('photo_upload_student.html', msg="failure")
            else:
                return redirect("autherror")

        else:
            return redirect("autherror")
    else:
        return redirect("login")



@app.route("/Change_admin_password",methods=['GET','POST'])
def Change_admin_password():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                cn = pymysql.connect(host="localhost", user="root", port=3306, db="student", password="",autocommit=True)
                cur = cn.cursor()

                old_password=request.form['T1']
                new_password=request.form['T2']

                sql = "update logindata set password='"+new_password+"' where email='"+email+"'and password='"+old_password+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template("Change_admin_password.html",msg="password changed")
                else:
                    return render_template("Change_admin_password.html",msg="password not changed")
            else:
                return render_template("Change_admin_password.html")
        else:
            return redirect('Accountant_home')
    else:
        return redirect('login')



@app.route("/Admin_photo")
def Admin_photo():
    return render_template("Photo_upload_admin.html")


@app.route("/Admin_photo1",methods=['GET','POST'])
def Admin_photo1():
    if 'email' in session:
        email=session['email']
        usertype=session['usertype']
        if usertype=='admin':
            if request.method=="POST":
                file=request.files['A1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cn=pymysql.connect(host='localhost',port=3306,user='root',password='',db='student',autocommit=True)
                    cur=cn.cursor()
                    sql="insert into photodata values('"+email+"','"+filename+"')"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                        return render_template("Photo_upload_admin1.html",result="success")
                    else:
                        return render_template("Photo_upload_admin1.html",result="failure")
                else:
                    return redirect(url_for('autherror'))
            else:
                return redirect(url_for('autherror'))



@app.route('/Change_Admin_Photo')
def Change_Admin_Photo():
    if 'email' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            photo = check_photo(email)
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student', autocommit=True)
            cur = conn.cursor()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                os.remove("./static/photos/"+photo)
                return render_template('Change_Admin_Photo.html',data="success")
            else:
                return render_template('Change_Admin_Photo.html', data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('lohin'))


@app.route("/Edit_accountant2",methods=['GET','POST'])
def Edit_accountant2():
    if 'email' in session:
        email = session['email']
        usertype = session['usertype']
        if usertype == "accountant":
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                em= request.form['T1']
                sql = "select * from accountant where email='" + em + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    data= cur.fetchall()
                    return render_template("Edit_accountant_pro.html", data=data)
                else:
                    return render_template("Edit_accountant_pro.html", msg="data not found")
            else:
                return render_template("Accountant_home.html")
        else:
            return redirect('autherror')
    else:
        return redirect(url_for("login"))



@app.route("/Edit_accountant3", methods=['GET', 'POST'])
def Edit_accountant3():
    if 'email' in session:
        email = session['email']
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student',autocommit=True)
                cur = conn.cursor()
                name = request.form['T2']
                contact = request.form['T3']
                address = request.form['T4']
                gender = request.form['T5']
                email = request.form['T6']
                sql = "update accountant set  name='" + name + "', contact='" + contact + "', address='" + address + "', gender='"+gender+"' where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                print(n)
                if n == 1:
                    return render_template("Edit_accountant_pro.html", msg="data edit")
                else:
                    return render_template("Edit_accountant_pro.html", msg="data not edit")
            else:
                return render_template("Accountant_home.html")
        else:
            return redirect('autherror')
    else:
        return redirect('login')








if (__name__) == '__main__':
    app.run(debug=True)
