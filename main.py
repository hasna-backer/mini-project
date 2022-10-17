from flask import *
from DBConnection import Db

app=Flask(__name__)
app.secret_key="200ghj"
db = Db()

@app.route("/logout")
def logout():
    session['lid']=""
    return redirect('/')

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
def login():
    return render_template("landingpage.html")


@app.route("/login")
def home():
    return render_template("lnlogin.html")



@app.route("/login_post",methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['pwd']
    db = Db()
    qry = " SELECT * FROM `login` WHERE `email`='" + username + "' and `password`='" + password + "'"
    res = db.selectOne(qry)
    if res !=None:
        session["lid"]=res["login_id"]
        print(session['lid'])

        if res['user type'] == "admin":
            return '''<script>alert("vaild");window.location="/admin"</script>'''
        elif res['user type'] == "student":

            return '''<script>alert("vaild");window.location="student"</script>'''
        elif res['user type'] == "staff":
            return '''<script>alert("vaild");window.location="staff"</script>'''
        else:
            return '''<scrpit>alert("invaild");window.location="/"</scrpit>'''
    else:
        return '''<script>alert("invaild");window.location="/"</script>'''

@app.route("/admin")
def admin_home():
    return render_template("admin/adminindex.html")



@app.route("/admin_course_mngt")
def admin_course_mngt():
    db = Db()
    qry = "select *from course"
    res = db.select(qry)
    return render_template("admin/course mngt.html",data=res)


@app.route('/admin_add_course')
def admin_add_course():
    qry="select * from category"
    db = Db()
    res = db.select(qry)
    return render_template("admin/add course.html",data=res)

@app.route('/admin_add_course_post', methods=['POST'])
def admin_add_course_post():
    category=request.form['select']
    course=request.form['textfield']

    eligibility=request.files['eligibility']
    path="/Users/hasna/PycharmProjects/LEVEL UP/static/eligibility/"
    from datetime import  datetime
    fname= datetime.now().strftime("%Y%m%d%H%M%S")+".pdf"
    s=path+fname
    eligibility.save(s)
    epath="/static/eligibility/"+fname

    syllabus=request.files['syllabus']
    path="/Users/hasna/PycharmProjects/LEVEL UP/static/syllabus/"
    from datetime import datetime
    sname= datetime.now().strftime("%Y%m%d%H%M%S")+".pdf"
    syl=path+sname
    syllabus.save(syl)
    spath="/static/syllabus/"+sname
    duration=request.form['textfield2']

    fees=request.form['textfield3']
    exam=request.form['textfield4']
    db = Db()
    qry = "insert into course(cat_id,course_name,eligibility,duration,syllabus,fees,exam_type)VALUES ('"+category+"','"+course+"','"+epath+"','"+duration+"','"+spath+"','"+fees+"','"+exam+"')"
    print(qry)
    res=db.insert(qry)
    return '''<script>alert('successfully added');window.location="/admin_course_mngt#why-us"</script>'''


@app.route('/admin_update_course/<id>')
def admin_update_course(id):
    qry = "select * from category"
    db = Db()
    res = db.select(qry)


    qry1="select * from course where course_id='"+id+"'"
    ress=db.selectOne(qry1)
    return render_template("admin/update course.html",data=res,data1=ress)

@app.route('/admin_update_course_post', methods=['POST'])
def admin_update_course_post():
    id = request.form['id']
    category = request.form['select']
    course = request.form['textfield']
    eligibility = request.files['eligibility']
    syllabus = request.files['syllabus']
    duration = request.form['textfield2']
    fees = request.form['textfield3']
    exam = request.form['textfield4']
    db = Db()

    paths = "/Users/hasna/PycharmProjects/LEVEL UP/static/syllabus/"
    pathe = "/Users/hasna/PycharmProjects/LEVEL UP/static/eligibility/"

    from datetime import datetime
    sname = datetime.now().strftime("%Y%m%d%H%M%S") + ".pdf"
    fname = datetime.now().strftime("%Y%m%d%H%M%S") + ".pdf"

    if eligibility and syllabus:

        s = pathe + fname
        eligibility.save(s)
        epath = "/static/eligibility/" + fname


        syl = paths + sname
        syllabus.save(syl)
        spath = "/static/syllabus/" + sname
        duration = request.form['textfield2']

        qry="update course set cat_id'"+category+"',course_name='"+course+"',eligibility='"+epath+"',syllabus='"+spath+"',duration='"+duration+"',fees='"+fees+"',exam_type='"+exam+"' where course_id='"+id+"' "
        res=db.update(qry)
        return '''<script>alert('successfully updated');window.location="/admin_course_mngt#why-us"</script>'''
    elif eligibility:

        s = pathe + fname
        eligibility.save(s)
        epath = "/static/eligibility/" + fname

        qry="update course set cat_id='"+category+"',course_name='"+course+"',eligibility='"+epath+"',duration='"+duration+"',fees='"+fees+"',exam_type='"+exam+"' where course_id='"+id+"'"
        res=db.update(qry)
        return '''<script>alert('successfully updated');window.location="/admin_course_mngt#why-us"</script>'''
    elif syllabus:

        syl = paths + sname
        syllabus.save(syl)
        spath = "/static/syllabus/" + sname
        duration = request.form['textfield2']

        qry = "update course set cat_id='" + category + "',course_name='" + course + "',syllabus='" + spath + "',duration='" + duration + "',fees='" + fees + "',exam_type='" + exam + "' where course_id='" + id + "'"
        res = db.update(qry)
        return '''<script>alert('successfully updated');window.location="/admin_course_mngt#why-us"</script>'''

    else:
        qry = "update course set cat_id='"+category+"',course_name='"+course+"',duration='"+duration+"',fees='"+fees+"',exam_type='"+exam+"' where course_id='"+id+"'"

        res = db.update(qry)
        return '''<script>alert('successfully updated');window.location="/admin_course_mngt#why-us"</script>'''




@app.route('/admin_view_category')
def admin_view_category():
    db = Db()
    qry="select *from category"
    res=db.select(qry)

    return render_template("admin/view category.html",data=res)

@app.route('/admin_delete_course/<id>')
def admin_delete_course(id):
    db = Db()
    qry="delete from course where course_id='"+id+"'"
    res=db.delete(qry)

    return admin_course_mngt()

@app.route('/admin_delete_category/<id>')
def admin_delete_category(id):
    db = Db()
    qry="delete from category where cat_id='"+id+"'"
    res=db.delete(qry)

    return admin_view_category()


@app.route('/admin_add_category')
def admin_add_category():
    return render_template("admin/category mngt.html")

@app.route('/admin_add_category_post', methods=['POST'])
def admin_add_category_post():
    category=request.form['textfield']
    db=Db()
    qry="insert into category(cname)VALUES ('"+category+"')"
    res = db.insert(qry)
    return admin_view_category()

@app.route("/admin_student")
def admin_student():
    db = Db()
    qry = "select *from student"
    res = db.select(qry)
    return render_template("admin/student.html",data=res)

@app.route("/admin_notification")
def admin_notification():
    db = Db()
    qry = "select *from notification"
    res = db.select(qry)
    return render_template("admin/notification.html", data=res)

@app.route('/admin_delete_notification/<id>')
def admin_delete_notification(id):
    db = Db()
    qry="delete from notification where noti_id='"+id+"'"
    res=db.delete(qry)

    return '''<script>alert('successfully deleted');window.location="/admin_notification#why-us"</script>'''


@app.route('/admin_send_notification')
def admin_send_notification():
    return render_template("admin/send notification.html")

@app.route('/admin_send_notification_post', methods=['POST'])
def admin_send_notification_post():
    type=request.form['textfield2']
    notification=request.form['textfield']
    db = Db()
    qry = "insert into notification(type,notification,date)VALUES ('" + type + "','"+notification+"',curdate())"
    res = db.insert(qry)
    return admin_notification()


@app.route("/admin_payment")
def admin_payment():
    return render_template("admin/payment.html")











@app.route("/student")
def student_home():
    return render_template("student/student_index.html")



@app.route('/student_registration')
def student_registration():
    qry="select * from student"
    db = Db()
    res = db.select(qry)
    return render_template("signin.html",data=res)

@app.route('/student_registration_post', methods=['POST'])
def student_registration_post():
    fn=request.form['textfield6']
    ln = request.form['textfield']
    house = request.form['textfield55']
    place = request.form['textfield5']
    post = request.form['textfield2']
    city=request.form['textfield3']
    pin=request.form['textfield4']
    gender = request.form['radio']
    dob = request.form['textfield8']
    email=request.form['mail']
    phno = request.form['textfield7']
    nationality = request.form['select']
    photo = request.files['pic']
    qualification=request.form['qual']


    photo.save("/Users/hasna/PycharmProjects/LEVEL UP/static/photo/"+photo.filename)
    pathlibs="/static/photo/"+photo.filename
    pwd=request.form["password"]
    pwd2=request.form["pwd2"]
    db = Db()
    qry1="select * from student where email='"+email+"'"
    res1=db.selectOne(qry1)
    if res1 is not None:
        return '''<script>alert('data already exist');window.location="/student_registration#why-us"</script>'''
    else:
        qry2="insert into login(email,password,`user type`)values('"+email+"','"+pwd+"','student')"
        res2=db.insert(qry2)
        qry = "insert into student(login_id,first_name,last_name,house,place,post,city,pin,nationality,photo,gender,dob,email,phone,qualification)VALUES ('"+str(res2)+"','"+fn+"','"+ln+"','"+house+"','"+place+"','"+post+"','"+city+"','"+pin+"','"+nationality+"','"+pathlibs+"','"+gender+"','"+dob+"','"+email+"','"+phno+"','"+qualification+"')"
        print(qry)
        res=db.insert(qry)
        return '''<script>alert('successfully added');window.location="/login"</script>'''


@app.route('/student_view_course')
def student_view_course():
    db = Db()
    qry="select *from course"
    res=db.select(qry)

    return render_template("student/view course.html",data=res)

@app.route('/student_view_profile')
def student_view_profile():
    db = Db()
    qry="select *from student where login_id='"+str(session['lid'])+"'"
    print(session['lid'])
    res=db.selectOne(qry)

    return render_template("student/profile.html",data=res)



@app.route('/update_user_profile')
def update_user_profile():
    db = Db()
    qry="select * from student where login_id='"+str(session["lid"])+"'"
    res=db.selectOne(qry)

    return render_template("student/profile_update.html",data=res)


@app.route('/update_user_profile_post', methods=['POST'])
def update_user_profile_post():


    fn = request.form['textfield6']
    ln = request.form['textfield']
    house = request.form['textfield55']
    place = request.form['textfield5']
    post = request.form['textfield2']
    city = request.form['textfield3']
    pin = request.form['textfield4']
    gender = request.form['radio']

    dob = request.form['textfield8']
    email = request.form['mail']
    phno = request.form['textfield7']
    nationality = request.form['select']
    photo = request.files['pic']
    qualification = request.form['qual']

    db = Db()
    if photo:
        photo.save("/Users/hasna/PycharmProjects/LEVEL UP/static/photo/" + photo.filename)
        pathlibs = "/static/photo/" + photo.filename
        qry="update student set first_name='"+fn+"',last_name='"+ln+"',house='"+house+"',place='"+place+"',post='"+post+"',city='"+city+"',pin='"+pin+"',gender='"+gender+"',dob='"+dob+"',email='"+email+"',phone='"+phno+"',nationality='"+nationality+"',photo='"+pathlibs+"',qualification='"+qualification+"' where login_id='"+str(session['lid'])+"'"
        res=db.update(qry)
        qry1 = "update login set email='" + email + "' where login_id='"+str(session['lid'])+"'"
        res1 = db.update(qry1)
        return '''<script>alert('successfully updated');window.location="/student_view_profile#why-us"</script>'''
    else:
        qry = "update student set first_name='" + fn + "',last_name='" + ln + "',house='"+house+"',place='" + place + "',post='" + post + "',city='" + city + "',pin='" + pin + "',gender='" + gender + "',dob='" + dob + "',email='" + email + "',phone='" + phno + "',nationality='" + nationality + "',qualification='" + qualification + "' where login_id='" + str(
            session['lid']) + "'"
        res = db.update(qry)
        qry1="update login set email='"+email+"' where login_id='"+str(session['lid'])+"'"
        res1=db.update(qry1)
        return '''<script>alert('successfully updated');window.location="/student_view_profile#why-us"</script>'''



















@app.route("/staff")
def staff_home():
    return render_template("staff/staff_index.html")
    # return render_template("staff.html")


@app.route('/staff_view_course')
def staff_view_course():
    qry="select * from course"
    db = Db()
    res = db.select(qry)
    return render_template("staff/view course.html",data=res)

#
#


@app.route('/staff_update_course/<id>')
def staff_update_course(id):
    qry = "select * from category"
    db = Db()
    res = db.select(qry)


    qry1="select * from course where course_id='"+id+"'"
    ress=db.selectOne(qry1)
    return render_template("staff/update course.html",data=res,data1=ress)

@app.route('/staff_update_course_post', methods=['POST'])
def staff_update_course_post():
    id = request.form['id']
    category = request.form['select']
    course = request.form['textfield']
    eligibility = request.files['eligibility']
    syllabus = request.files['syllabus']
    duration = request.form['textfield2']
    fees = request.form['textfield3']
    exam = request.form['textfield4']
    db = Db()

    paths = "/Users/hasna/PycharmProjects/LEVEL UP/static/syllabus/"
    pathe = "/Users/hasna/PycharmProjects/LEVEL UP/static/eligibility/"

    from datetime import datetime
    sname = datetime.now().strftime("%Y%m%d%H%M%S") + ".pdf"
    fname = datetime.now().strftime("%Y%m%d%H%M%S") + ".pdf"

    if eligibility and syllabus:

        s = pathe + fname
        eligibility.save(s)
        epath = "/static/eligibility/" + fname


        syl = paths + sname
        syllabus.save(syl)
        spath = "/static/syllabus/" + sname
        duration = request.form['textfield2']

        qry="update course set cat_id'"+category+"',course_name='"+course+"',eligibility='"+epath+"',syllabus='"+spath+"',duration='"+duration+"',fees='"+fees+"',exam_type='"+exam+"' where course_id='"+id+"' "
        res=db.update(qry)
        return '''<script>alert('successfully updated');window.location="/staff_view_course#why-us"</script>'''
    elif eligibility:

        s = pathe + fname
        eligibility.save(s)
        epath = "/static/eligibility/" + fname

        qry="update course set cat_id='"+category+"',course_name='"+course+"',eligibility='"+epath+"',duration='"+duration+"',fees='"+fees+"',exam_type='"+exam+"' where course_id='"+id+"'"
        res=db.update(qry)
        return '''<script>alert('successfully updated');window.location="/staff_view_course#why-us"</script>'''
    elif syllabus:

        syl = paths + sname
        syllabus.save(syl)
        spath = "/static/syllabus/" + sname
        duration = request.form['textfield2']

        qry = "update course set cat_id='" + category + "',course_name='" + course + "',syllabus='" + spath + "',duration='" + duration + "',fees='" + fees + "',exam_type='" + exam + "' where course_id='" + id + "'"
        res = db.update(qry)
        return '''<script>alert('successfully updated');window.location="/staff_view_course#why-us"</script>'''

    else:
        qry = "update course set cat_id='"+category+"',course_name='"+course+"',duration='"+duration+"',fees='"+fees+"',exam_type='"+exam+"' where course_id='"+id+"'"

        res = db.update(qry)
        return '''<script>alert('successfully updated');window.location="/staff_view_course#why-us"</script>'''


@app.route("/staff_student")
def staff_student():
    db = Db()
    qry = "select *from student"
    res = db.select(qry)
    return render_template("staff/student.html",data=res)






if __name__ == '__main__':
    app.run(debug=True)
