from flask import Flask, request, redirect, render_template
import ibm_db


connection = ibm_db.connect("DATABASE=bludb; HOSTNAME = 8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud; PORT=30120; SECURITY=SSL; SSLServerCertificate= DigiCertGlobalRootCA.crt;UID=mpb71923;PWD=kkEChAbOHtoXvmQN",'','')
print(connection)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/student')
def student():
    return render_template("login.html")

@app.route('/prof')
def prof():
    return render_template("login.html")

@app.route('/admin')
def admin():
    return render_template("login.html")

@app.route('/adminprofile')
def adminprofile():
    return render_template("adminprofile.html")


@app.route('/login1', methods=['GET', 'POST'])
def login1():
    USERNAME = request.form['USERNAME']
    PASSWORD = request.form['PASSWORD']
    sql = "SELECT * FROM REG WHERE NAME = ? AND PASSWORD = ?"
    stmt = ibm_db.prepare(connection, sql)
    ibm_db.bind_param(stmt,1,USERNAME)
    ibm_db.bind_param(stmt,2,PASSWORD)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
         return redirect("/adminprofile")
    else:
        return render_template("reg.html", pred="Login Unsuccessful")

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    NAME = request.form.get('NAME')
    EMAIL = request.form.get('EMAIL')
    PASSWORD = request.form.get('PASSWORD')

    sql = "SELECT * FROM REG WHERE EMAIL = ?"
    stmt = ibm_db.prepare(connection, sql)
    ibm_db.bind_param(stmt,1,NAME)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    
    if account:
        return render_template("login.html", pred="Already registered. Please Login.!")
        
    else:
        insert = "INSERT INTO REG VALUES (?, ?, ?)"
        prep_stmt = ibm_db.prepare(connection, insert)
        ibm_db.bind_param(prep_stmt,1,NAME)
        ibm_db.bind_param(prep_stmt,2,EMAIL)
        ibm_db.bind_param(prep_stmt,3,PASSWORD)
        ibm_db.execute(prep_stmt)
        return render_template("login.html", pred="Registration successful. Please Login.!")

if __name__ == '__main__':
    app.run(debug=True, port = 5000)