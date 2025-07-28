
import pymysql
def get_connection():
    con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student')
    return con
def check_photo(email):
    con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student')
    cur = con.cursor()
    cur.execute("SELECT * FROM photodata where email='" + email + "'")
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo

def course_paid(course_id,stid):
    p=0
    con=get_connection()
    sql="select * from fee where sr_no="+str(stid)+" and course_id="+str(course_id)
    cur=con.cursor()
    cur.execute(sql)
    n=cur.rowcount
    if(n>0):
        data=cur.fetchall()
        for d in data:
            p=p+d[3]
    return p

def student_photo(sr_no):
    con = get_connection()
    cur = con.cursor()
    sql = "select * from student_photo where sr_no='"+sr_no+"'"
    cur.execute(sql)
    n=cur.rowcount
    print(n)
    photo="no"
    if n>0:
        data = cur.fetchone()
        photo=data[1]
        print(photo)
    return photo
