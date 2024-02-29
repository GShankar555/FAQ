from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=DRIVER={SQL Server};Server=GOWRI-SHANKAR\\SQLEXPRESS;Database=mlsc;Trusted_Connection=yes;'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class FormData(db.Model):
    __tablename__ = 'Form_Data'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50))
    l_name = db.Column(db.String(50))
    dept = db.Column(db.String(50))
    std_year = db.Column(db.Integer)
    email = db.Column(db.String(50))
    faq = db.Column(db.String(50))
    mobile_no = db.Column(db.Integer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        mobile_no = int(request.form['mobile_no'])
        dept = request.form['dept']
        year = int(request.form['year'])
        email = request.form['email']
        faq = request.form['faq']
        new_data = FormData(f_name=fname, l_name=lname, mobile_no=mobile_no, dept=dept, std_year=year, email=email, faq=faq)
        try:
            db.session.add(new_data)
            db.session.commit()
            return render_template('index.html')
        except Exception as e:
            db.session.rollback()
            return f"Error: {e}"
        finally:
            db.session.close()
    else:
        return "Unexpected error"
if __name__ == '__main__':
    app.run(debug=True)