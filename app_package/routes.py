from flask import render_template, flash, redirect, url_for
from app_package import app, db,mongo
from flask_login import current_user, login_user, logout_user, login_required
from app_package.forms import LoginForm, RegistrationForm
from app_package.forms import AddCustomerForm, DeleteCustomerForm, WithdrawAmountForm
from app_package.forms import ModifyCustomerForm
from app_package.models import User

cus_id=0
tbal=[]
nbal=[]
sbal=[]
@app.route("/", methods=["GET","POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid user")
                return redirect(url_for("index"))
            else:
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for("menu"))
        else:
            return render_template("login.html",form=form)

@app.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:
        form=RegistrationForm()
        if form.validate_on_submit():
            user=User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("User registered. You may login now")
            return redirect(url_for("index"))
        else:
            return render_template("register.html",form=form)
            
@app.route("/menu")
@login_required
def menu():
    return render_template("menu.html")
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/add_customer", methods=["GET","POST"])
@login_required
def add_customer():
    global cus_id
    form=AddCustomerForm()
    if form.validate_on_submit():
        fields=["_id","name","age","type","account_num","balance"]
        cus_id+=1
        values=[cus_id,form.name.data,form.age.data,form.type.data,form.account_num.data,form.balance.data]
        customer=dict(zip(fields,values))
        cus_col=mongo.db.customers
        tmp=cus_col.insert_one(customer)
        if tmp.inserted_id==cus_id:
            flash("Customer added")
            return redirect(url_for("menu"))
        else:
            flash("Problem adding customer")
            return redirect(url_for("logout"))
    else:
        return render_template("add_customer.html",form=form)
        
@app.route("/delete_employee", methods=["GET","POST"])
@login_required
def delete_customer():
    form=DeleteCustomerForm()
    if form.validate_on_submit():
        cus_col=mongo.db.customers
        query={"_id":form.id.data}
        cus_col.delete_one(query)
        flash("Customer deleted")
        return redirect(url_for("menu"))
    else:
        return render_template("delete_customer.html",form=form)
        
@app.route("/modify_customer", methods=["GET","POST"])
@login_required
def modify_customer():
    form=ModifyCustomerForm()
    if form.validate_on_submit():
        values=dict()
        if form.name.data!="":values["name"]=form.name.data
        if form.balance.data!="":values["balance"]=form.balance.data
        new_data={"$set":values}
        query={"_id":form.id.data}
        cus_col=mongo.db.customers
        cus_col.update_one(query,new_data)
        flash("Customers modified")
        return redirect(url_for("menu"))
    else:
        return render_template("modify_customer.html",form=form)
        
@app.route("/display_customers")
@login_required
def display_customers():
    cus_col=mongo.db.customers
    customers=cus_col.find()
    return render_template("display_customers.html",customers=customers)
    
    
@app.route("/withdraw_amount", methods=["GET","POST"])
@login_required
def withdraw_amount():
    form=WithdrawAmountForm()
    if form.validate_on_submit():
        
        query={"account_num":form.account_num.data}
        cus_col=mongo.db.customers
        cust=cus_col.find_one(query)
        bal=cust["balance"]
        new_bal=bal+form.balance.data
        new_bal={"$set":{"balance":new_bal}}
        cus_col.update_one(query,new_bal)
        flash("Amount withdrawed")
        return redirect(url_for("menu"))      
    else:
        return render_template("withdraw_amount.html",form=form)
