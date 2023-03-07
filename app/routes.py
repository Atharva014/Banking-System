from app import app
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import session, flash
from app.models import db, LoginTable, UserData, BalanceData


@app.route('/', methods=['POST', 'GET'])
def HomeLogin():
    session.clear()
    return render_template('HomeLogin.html', error=False)


@app.route('/Register', methods=['POST', 'GET'])
def RegisterPage():
    session.clear()
    return render_template('RegisterPage.html', error="None")


@app.route('/Process', methods=['POST'])
def Process():

    val = request.form['hiddenValue']

    if val == '0':
        error = check(request.form)
        if len(error) == 0:
            addInfo(request.form)
            return redirect(url_for('HomeLogin'))
        else:
            return render_template('RegisterPage.html', error=error)

    elif val == '1':
        data = request.form
        if isPresent(data):
            return redirect(url_for('Dashboard.Dashboard'))
        else:
            return render_template('HomeLogin.html', error=True)


def check(data):
    error = []
    if data['uname'] == " ":
        error.append("Enter valid Name.")

    if data['pno'] == " ":
        error.append("Enter valid Phone number.")

    if data['address'] == " ":
        error.append("Enter valid Address.")

    if data['country'] == " ":
        error.append("Enter valid Country.")

    if data['state'] == " ":
        error.append("Enter valid State.")

    if data['city'] == " ":
        error.append("Enter valid City.")

    if data['pcode'] == " ":
        error.append("Enter valid Postal Code.")

    if len(data['pin1']) == 4 and " " not in data['pin1']:
        if data['pin1'] != data['pin2']:
            error.append("Pin does not match.")

    else:
        error.append("Enter valid pin.")

    if len(data['pass1']) >= 8 and " " not in data['pass1']:
        if data['pass1'] != data['pass2']:
            error.append("Password does not match.")

    else:
        error.append("Enter valid Password.")

    return error

def isPresent(data):
    user = LoginTable.query.filter_by(phone_no=data['phno']).first()
    if user is not None:
        if user.phone_no == data['phno'] and user.password == data['pass']:
            session['id'] = user.id
            session['LoggedIn'] = True
            return True
        else:
            return False
    else:
        return False

def addInfo(data):
    account_no = "00" + data['pno']
    u = UserData(username = data['uname'], bdate = data['bdate'], email = data['email'], gender = data['gender'],
                 phoneno = data['pno'], address = data['address'], country = data['country'],state = data['state'],
                 city = data['city'], postalCode = data['pcode'], AccNo = account_no, AccType = data['atype'],
                 AccPin = data['pin1'], password = data['pass1'])
    db.session.add(u)


    l = LoginTable(phone_no = data['pno'], password = data['pass1'])
    db.session.add(l)

    b = BalanceData(AccNo = account_no, amount = "0", AccType = data['atype'])
    db.session.add(b)
    db.session.commit()
