from Dashboard import dboard
from flask import render_template
from flask import session
from flask import redirect, url_for
from app.models import BalanceData

@dboard.route('/')
def Dashboard():

    if 'LoggedIn' in session:
        if session['LoggedIn']:

            id = session['id']
            data = getData(id)
            return render_template('DashboardPage.html', data = data)

        else:
            return redirect(url_for('HomeLogin'))
    else:
        return redirect(url_for('HomeLogin'))

@dboard.route('/<name>')
def DProcess(name):
    if name == 'SendMoney':
        return redirect(url_for('MoneyTransaction.showSendMoney'))

    if name == 'DepositMoney':
        return redirect(url_for('MoneyTransaction.showDepositMoney'))

    if name == 'WithdrawMoney':
        return redirect(url_for('MoneyTransaction.showWithdrawMoney'))

    if name == 'TransactionHistory':
        return redirect(url_for('TransactionAndInformation.showTransaction'))

    if name == 'MyInformation':
        return redirect(url_for('TransactionAndInformation.showInfo'))

    return render_template('DashboardPage.html')

@dboard.route('/Logout', methods=['POST'])
def Logout():
    session.clear()
    return redirect(url_for('HomeLogin'))

def getData(aid):
    result = BalanceData.query.get(aid)
    data = {
        'acc_no': result.AccNo,
        'amount': result.amount,
        'acc_type':result.AccType
    }
    return data
