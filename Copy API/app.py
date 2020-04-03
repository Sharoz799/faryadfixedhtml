from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
import pymongo

from bson.objectid import ObjectId
from bson.json_util import dumps

from datetime import datetime,timedelta 

import adminportal


app = Flask(__name__)
app.secret_key = 'faryad'
connection = 'mongodb+srv://faryad:faryad@cluster0-hlef6.mongodb.net/test'
myclient = pymongo.MongoClient(connection)

mydb = myclient["Faryad"]
admin = mydb['admin']
users = mydb["users"]
donors = mydb["donors"]
requests = mydb["requests"]

users.create_index("Email",  unique=True)

# requests.create_index('Phone', unique=True)

def getKeys(cursor):
    arr = []
    for i in cursor:
        for j in i:
            arr.append(j)
        return arr[1:]


@app.route("/", methods=['Post', 'Get'])
def index():
    username = request.form.get('Username')
    password = request.form.get('password')
    donor = donors.find_one({'username': username, 'password': password})
    if donor:
        session['logged_in'] = True
        session['DonorID'] = str(donor['_id'])
        return redirect(url_for('home'))
    admin_ = admin.find_one({'username': username, 'password': password})
    if admin_:
        session['logged_in'] = False
        session['admin'] = True
        return redirect(url_for('signup'))
    else:
        flash("Invalid Credentials.!!!", 'ERROR')
    return render_template('Login.html')


@app.route('/signup' , methods=['Post', 'Get'])
def signup():
    if not session.get('admin'):
        return redirect(url_for('home'))
    f = adminportal.DonorsForm()
    if request.form.get('Submitform') == 'Submitform':
        if f.password.data!=f.confirm.data:
            return  '<center><h1>Error</h1></center>'+'\n' + '<center><h1>Passwords do not match</h1></center>'
        if f.towns.data == []:
            return  '<center><h1>Error</h1></center>'+'\n' + '<center><h1>Select Towns Please</h1></center>'
        json = adminportal.getDonorsjson(f.username.data, f.password.data,f.name.data,f.email.data, f.phone.data, f.address.data, f.towns.data)
        try:
            donors.insert_one(json)
        except:
            return '<center><h1>Error</h1></center>'+'\n' + '<center><h1>Username Already Exists</h1></center>'        
        flash('Thank you for helping people out. :)', 'Success')
        form2 = adminportal.DonorsForm()
        return redirect(url_for('signup', form2 = form2))
    
    return render_template('signup.html', form2 = f)

@app.route('/admin/<variable>')
def adminRoute(variable):
    if not session.get('admin'):
        return redirect(url_for('home'))
    if variable=='Users':
        return render_template('view.html', arr = users.find({}), keys = getKeys(users.find({})), variable = variable)
    elif variable=='Requests':
        return render_template('view.html', arr = requests.find({'status': 'Awaiting'}), keys = getKeys(requests.find({'status': 'Awaiting'})), variable = variable)
    elif variable=='Donors':
        return render_template('view.html', arr = donors.find({}), keys = getKeys(donors.find({})), variable = variable)
    elif variable=='Donations':
        cursor = requests.find({'status': {'$in': ['Delivered', 'Accepted']}}).sort([('Date',pymongo.DESCENDING)])
        return render_template('view.html', arr = cursor, keys = getKeys(requests.find({})), variable = variable)
    return render_template('view.html')


@app.route("/home", methods=['Post', 'Get'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    areas = donors.find_one({'_id': ObjectId(session['DonorID'])})
    areas = areas['areas']
    cl = requests.find({'status':'Awaiting', 'Area':{'$in': adminportal.getAreas(areas)}}).sort([('Date',pymongo.DESCENDING)])
    accepts, ignored = requests.count_documents( { 'status':'Accepted', 'DonorID': (session['DonorID']) } ), requests.count_documents({'status':'Awaiting', 'Area':{'$in': adminportal.getAreas(areas)}})
    arr2= requests.find({'status':'Accepted','DonorID': str(session['DonorID'])}).sort([('Date',pymongo.DESCENDING)]).limit(5)
    return render_template('index.html', arr=cl, accepts= accepts, ignored = ignored, arr2 = arr2, keys = getKeys(requests.find({'status':'Accepted','DonorID': str(session['DonorID'])}).sort([('Date',pymongo.DESCENDING)]).limit(5)))

@app.route("/affirmed", methods=['Post', 'Get'])
def affirmed():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    arr2= requests.find({'status':'Accepted','DonorID': str(session['DonorID'])}).sort([('Date',pymongo.DESCENDING)])
    return render_template('requests.html', arr=arr2, keys = getKeys(requests.find({'status':'Accepted','DonorID': str(session['DonorID'])}).sort([('Date',pymongo.DESCENDING)])))

@app.route("/completed", methods=['Post', 'Get'])
def completed():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    arr2= requests.find({'status':'Delivered','DonorID': str(session['DonorID'])}).sort([('Date',pymongo.DESCENDING)])
    return render_template('completed.html', arr=arr2, keys = getKeys(requests.find({'status':'Delivered','DonorID': str(session['DonorID'])}).sort([('Date',pymongo.DESCENDING)])))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['DonorID'] = ''
    session['admin'] = False
    return redirect(url_for('index'))

@app.route("/saveData", methods=['Post'])
def saveData():
    data = request.get_json()
    users.insert_one(data)
    return 'Data Saved'

@app.route("/saveRequest", methods=['Post'])
def saveRequest():
    data = request.get_json()
    data['status'] =  "Awaiting"
    data['Date'] = datetime.today()
    count = requests.count_documents({'Phone': data['Phone'], 'whom': 'self', "Date":{'$lte':datetime.today(), '$gte': datetime.today()-timedelta(30)}})
    count2 = requests.count_documents({'Email': data['Email'], "Date":{'$lte':datetime.today(), '$gte': datetime.today()-timedelta(30)}})
    count3 = requests.count_documents({'CNIC': data['CNIC'], "Date":{'$lte':datetime.today(), '$gte': datetime.today()-timedelta(30)}})

    if count>0:
        data['flag'] = (str(count+1) + ' requests in last 30 days from same number')
    
    elif (count2>5):
        data['flag'] = (str(count2+1) + ' requests in last 30 days from same device')
    
    
    elif count3>0:
        data['flag'] = str(count3+1) + ' requests in last 30 days from same CNIC'
    
    else:
        data['flag'] = 'No Flag'
    
    requests.insert_one(data)
    return 'Data Saved'

@app.route("/changeStatus/<ID>")
def changeStatus(ID):
    requests.update_one({'_id': ObjectId(ID)}, { "$set" :{'status': "Accepted", 'DonorID': str(session['DonorID']), 'Date Accepted': datetime.today()}})
    return ''

@app.route("/changeStatusToDelivered/<ID>")
def changeStatusToDelivered(ID):
    requests.update_one({'_id': ObjectId(ID)}, { "$set" :{'status': "Delivered", 'DonorID': str(session['DonorID']), 'Date Delivered': datetime.today()}})
    return ''

@app.route("/getRequests/<email>", methods = ['POST', 'GET'])
def getRequests(email):
    return dumps(requests.find( {'Email': email}, {'Name': 1, 'Phone': 1, 'Address': 1, 'status': 1, 'Date': 1, '_id': 0} ))

if __name__ == "__main__":  
    app.run(debug=True)


        