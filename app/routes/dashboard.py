from app.routes import app
from flask import render_template, session, request, redirect, flash
from app.Forms import GiveForm
from app.Data import Transaction, User
import requests
from datetime import datetime
from mongoengine.queryset.visitor import Q

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = GiveForm.new()
    currUser = User.objects.get(googleid=session['googleID'])
    given = Transaction.objects(giver=currUser.id).sum('amount')
    received = Transaction.objects(recipient=currUser.id).sum('amount')
    myWallet = received-given

    #if request.method == 'POST' and form.validate():
    if request.method == 'POST' and form.validate():
        validTransaction = False

        # check that giver isn't giving money to themselves
        if (currUser.name != form.recipient.data):
            validTransaction = True
        else:
            flash("You can't give it to yourself, " +
                  giver.name[0:giver.name.find(" ")])
            return redirect("/dashboard")

        # check if giver has enough money
        if (int(myWallet) >= int(form.amount.data)):
            validTransaction = True
        else:
            flash(f"You can't send {form.amount.data} when you only have {myWallet}")
            return redirect("/dashboard")

        if int(form.amount.data < 6):
            validTransaction = True
        else:
            flash('The maximum you can give is 5')
            return redirect("/dashboard")

        if currUser.gaveto != form.recipient.data:
            validTransaction = True
        else:
            flash("You can't give to the same person twice in a row.")
            return redirect("/dashboard")

    # if valid
        if validTransaction:
            # get giver data
            currUser.reload()

            # get recipient data
            recipientUser = User.objects.get(name=form.recipient.data)

            # create the transaction
            newTransaction = Transaction()
            newTransaction.giver = currUser
            newTransaction.recipient = recipientUser
            newTransaction.amount = form.amount.data
            newTransaction.reason = form.reason.data
            newTransaction.category = form.category.data
            newTransaction.createdate = datetime.now()
            newTransaction.save()

            currUser.update(gaveto=form.recipient.data)

            flash(f"You successfully sent {form.amount.data} currency to {form.recipient.data}")
            return redirect("/dashboard")

    # Update session and other variables
    currUser.reload()
    userTransactions = Transaction.objects(Q(giver=currUser.id) | Q(recipient=currUser.id))
    received = Transaction.objects(recipient=currUser.id).sum('amount')
    given = Transaction.objects(giver=currUser.id).sum('amount')
    countTrans = Transaction.objects.count()
    myWallet = received-given
    currUser.update(wallet=myWallet,reputation=given)
    session["wallet"] = myWallet
    session["reputation"] = given

    #form.recipient.choices = [(row.name, row.name) for row in User.objects()]

    return render_template('dashboard.html', wallet=myWallet, reputation=given,
                            form=form, totalTransactions = countTrans, userTransactions = userTransactions,
                            user=currUser)
