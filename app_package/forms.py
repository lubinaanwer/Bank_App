from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import IntegerField
from wtforms.validators import DataRequired, EqualTo
from app_package.models import User

class LoginForm(FlaskForm):
    username=StringField("Username: ",validators=[DataRequired()])
    password=PasswordField("Password: ", validators=[DataRequired()])
    remember_me=BooleanField("Remember Me")
    submit=SubmitField("Sign in")
    
class RegistrationForm(FlaskForm):
    username=StringField("Username: ",validators=[DataRequired()])
    password=PasswordField("Password: ", validators=[DataRequired()])
    password2=PasswordField("Repeat password: ",validators=[DataRequired(),EqualTo("password")])
    submit=SubmitField("Register")
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username exists, choose another one")
            
class AddCustomerForm(FlaskForm):
    name=StringField("Name: ",validators=[DataRequired()])
    age=IntegerField("Age: ",validators=[DataRequired()])
    type=StringField("Type : ",validators=[DataRequired()])
    account_num=IntegerField("Account Number: ",validators=[DataRequired()])
    balance=IntegerField("Balance: ",validators=[DataRequired()])
    submit=SubmitField("Add Customer")
    
class DeleteCustomerForm(FlaskForm):
    id=IntegerField("Id of the customer to be deleted: ",validators=[DataRequired()])
    submit=SubmitField("Delete Customer")
    
class ModifyCustomerForm(FlaskForm):
    id=IntegerField("Id of employee to be modified: ",validators=[DataRequired()])
    name=StringField("Name: ")
    balance=StringField("Balance: ")
    submit=SubmitField("Modify Customer")
    
    
class WithdrawAmountForm(FlaskForm):
    id=IntegerField("Id of employee: ",validators=[DataRequired()])
    account_num=IntegerField("Account Number: ",validators=[DataRequired()])
    balance=IntegerField("Amount: ",validators=[DataRequired()])
    submit=SubmitField("Withdraw")
    
