from MoneyTransaction import moneyTran
from Dashboard.routes import getData

import datetime

from flask import render_template
from flask import session
from flask import redirect, url_for
from flask import request
from flask import flash

from app.models import db, BalanceData, Transactions, UserData


@moneyTran.route('/SendMoney', methods=['GET', 'POST'])
def showSendMoney():

    if 'LoggedIn' in session:
        if session['LoggedIn']:
            id = session['id']

            if request.method == 'GET':
                data = getData(id)
                return render_template('SendMoney.html', data=data)

            if request.method == 'POST':
                if not verifySendMoney(request.form):
                    if DoSendMoney(id, request.form):
                        flash("Money Sent.", "success")
                return redirect(url_for('MoneyTransaction.showSendMoney'))

        else:
            return redirect(url_for('HomeLogin'))
    else:
        return redirect(url_for('HomeLogin'))


@moneyTran.route('/DepositMoney', methods=['GET', 'POST'])
def showDepositMoney():
    if 'LoggedIn' in session:
        if session['LoggedIn']:
            id = session['id']
            if request.method == 'GET':
                data = getData(id)
                return render_template('DepositMoney.html', data = data)

            if request.method == 'POST':
                if not verifyDepositMoney(request.form):
                    if DoDepositMoney(id, request.form):
                        flash("Money Deposited", "success")
                return redirect(url_for('MoneyTransaction.showDepositMoney'))

        else:
            return redirect(url_for('HomeLogin'))
    else:
        return redirect(url_for('HomeLogin'))


@moneyTran.route('/WithdrawMoney', methods=['GET', 'POST'])
def showWithdrawMoney():
    if 'LoggedIn' in session:
        if session['LoggedIn']:
            id = session['id']
            if request.method == 'GET':
                data = getData(id)
                return render_template('WithdrawMoney.html', data=data)

            if request.method == 'POST':
                if not verifyWithdrawMoney(request.form):
                    if DoWithdrawMoney(id, request.form):
                        flash("Money Withdrawed.", "success")

                return redirect(url_for('MoneyTransaction.showWithdrawMoney'))

        else:
            return redirect(url_for('HomeLogin'))
    else:
        return redirect(url_for('HomeLogin'))


@moneyTran.route('/Logout', methods=['POST'])
def Logout():
    session.clear()
    return redirect(url_for('HomeLogin'))


def verifySendMoney(data):
    error = False

    if len(data['racc_no']) != 12 or " " in data['racc_no']:
        flash("Please Enter valid Account Number.", "error")
        error = True

    if data['racc_name'] == " ":
        flash("Please Enter valid Account Holders Name.", "error")
        error = True

    if int(data['amount']) < 1:
        flash("Please Enter valid amount.", "error")
        error = True

    if len(data['pin1']) == 4 and " " not in data['pin1']:
        if data['pin1'] != data['pin2']:
            flash("Pine does not match.", "error")
            error = True
    else:
        flash("Please enter valid pin.", "error")
        error = True

    return error


def verifyDepositMoney(data):
    error = False
    if int(data['amount']) < 1:
        flash("Please enter valid amount.", "error")
        error = True

    if len(data['pin1']) == 4 and " " not in data['pin1']:
        if data['pin1'] != data['pin2']:
            flash("Pine does not match.", "error")
            error = True
    else:
        flash("Please enter valid pin.", "error")
        error = True

    return error


def verifyWithdrawMoney(data):
    error = False
    if int(data['amount']) < 1:
        flash("Please enter valid amount.", "error")
        error = True

    if len(data['pin1']) == 4 and " " not in data['pin1']:
        if data['pin1'] != data['pin2']:
            flash("Pine does not match.", "error")
            error = True
    else:
        flash("Please enter valid pin.", "error")
        error = True

    return error


def DoSendMoney(aid, rdata):
    error = True
    data = getData(aid)
    if int(data['amount']) < int(rdata['amount']):
        flash("Insufficient Balance.", "error")
        error = False

    b = BalanceData.query.filter_by(AccNo = rdata['racc_no']).first()
    if b is None:
        flash("Account does not exist.", "error")
        error = False

    if error:
        u = UserData.query.filter_by(id = aid).first()
        if u.AccPin == int(rdata['pin1']):
            b.amount = str(int(b.amount) + int(rdata['amount']))
            temp = BalanceData.query.get(aid)
            temp.amount = str(int(temp.amount) - int(rdata['amount']))


            data = getData(aid)
            t = Transactions(ttype='Send Money', tfrom = data['acc_no'], tto = rdata['racc_no'],
                             tamount = int(rdata['amount']), tdatetime=datetime.datetime.now())
            db.session.add(t)
            db.session.commit()

        else:
            flash("Invalid Pin", "error")
            error = False

    return error


def DoDepositMoney(aid, rdata):
    error = True
    u = UserData.query.filter_by(id = aid).first()

    if u.AccPin == int(rdata['pin1']):
        b = BalanceData.query.filter_by(id = aid).first()
        b.amount = str(int(rdata['amount']) + int(b.amount))

        data = getData(aid)
        t = Transactions(ttype='Deposit Money', tfrom="None", tto=data['acc_no'],
                         tamount=int(rdata['amount']), tdatetime=datetime.datetime.now())
        db.session.add(t)
        db.session.commit()

    else:
        flash("Invalid Pin", "error")
        error = False

    return error


def DoWithdrawMoney(aid, rdata):
    error = True
    u = UserData.query.filter_by(id=aid).first()

    if u.AccPin == int(rdata['pin1']):
        b = BalanceData.query.filter_by(id=aid).first()
        b.amount = str(int(b.amount) - int(rdata['amount']))

        data = getData(aid)
        t = Transactions(ttype='Withdraw Money', tfrom=data['acc_no'], tto="None",
                         tamount=int(rdata['amount']), tdatetime=datetime.datetime.now())
        db.session.add(t)
        db.session.commit()

    else:
        flash("Invalid Pin", "error")
        error = False

    return error
