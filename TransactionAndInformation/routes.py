from TransactionAndInformation import tranAndInfo
from Dashboard.routes import getData
from app.models import UserData, BalanceData, Transactions

from flask import render_template
from flask import session
from flask import redirect, url_for


@tranAndInfo.route('/MyInformation', methods=['POST', 'GET'])
def showInfo():

    if 'LoggedIn' in session:
        if session['LoggedIn']:

            id = session['id']
            data = getAllData(id)
            return render_template('MyInformation.html', data = data)


@tranAndInfo.route('/Transactions', methods=['POST', 'GET'])
def showTransaction():

    if 'LoggedIn' in session:
        if session['LoggedIn']:

            id = session['id']
            data = getTransactionData(id)
            return render_template('Transactions.html', data = data)


@tranAndInfo.route('/Logout', methods=['POST'])
def Logout():
    session.clear()
    return redirect(url_for('HomeLogin'))


def getAllData(aid):
    result1 = UserData.query.get(aid)
    result2 = BalanceData.query.get(aid)
    data = {
        'username': result1.username,
        'bdate': result1.bdate,
        'email': result1.email,
        'gender': result1.gender,
        'phoneno': result1.phoneno,
        'address': result1.address,
        'country': result1.country,
        'state': result1.state,
        'city': result1.city,
        'postalCode': result1.postalCode,
        'acc_no': result2.AccNo,
        'amount': result2.amount,
        'acc_type': result2.AccType
    }
    return data


def getTransactionData(aid):
    res = getData(aid)
    data = {
        'adata': res,
        'tdata': {}
    }
    t1 = Transactions.query.filter_by(tfrom=res['acc_no']).all()
    t2 = Transactions.query.filter_by(tto=res['acc_no']).all()
    t = t1 + t2

    for i in t:
        temp = {
            'ttype': i.ttype,
            'tfrom': i.tfrom,
            'tto': i.tto,
            'tamount': i.tamount,
            'tdatetime': i.tdatetime
        }
        data['tdata'][i.id] = temp

    mykeys = list(data['tdata'].keys())
    mykeys.sort()

    data['tdata'] = {i: data['tdata'][i] for i in mykeys}
    return data
