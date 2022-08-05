
import json
import re
from flask import Flask,request,render_template,redirect,session,jsonify
import requests
import sqlite3



con = sqlite3.connect('users4.db')
cursor = con.cursor()

cursor.execute('create table if not exists REG(username varchar, password varchar)')
cursor.execute('create table if not exists FriendsReq(sender varchar,tof varchar)')
cursor.execute('create table if not exists Friends(me varchar,you varchar)')
cursor.execute('create table if not exists SLAMS(tof varchar,sender varchar,q1 varchar,q2 varchar,q3 varchar,q4 varchar,q5 varchar,q6 varchar,q7 varchar)')


con.close()

def getU():
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()

    cursor.execute('create table if not exists USERS(dname varchar, username varchar, email varchar, hostel varchar, branch varchar)')
    # cursor.execute('create table if not exists POSTS1(name varchar, email varchar, text varchar, senderemail varchar, sendername varchar)')

    cursor.execute('select username from USERS')
    User = []
    for i in cursor:
        User.append(i[0])
    print(User)

    con.close()
    return User

User = getU()

app = Flask(__name__)
app.secret_key = 'harrish07'

@app.route('/auth')
def auth():
    return redirect('https://auth.delta.nitt.edu/authorize?client_id=SXlKVDxrzf9dXwUN&redirect_uri=http://127.0.0.1:5000/log&response_type=code&grant_type=authorization_code&scope=user')


@app.route('/',methods = ['POST','GET'])
def home():
    return render_template('index.html')

@app.route('/log')
def log():
    session['authcode']  = request.args['code']
    d = session['authcode']
    url = f'https://auth.delta.nitt.edu/api/oauth/token'
    print(url)
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    params = {'client_id' : 'SXlKVDxrzf9dXwUN','client_secret':'nZvL2jfZV3tggKSioPOQum6lTQ~QSbUR','grant_type':'authorization_code','code':d,'redirect_uri':'http://127.0.0.1:5000/log'}
    r = requests.post(url,headers = headers,data = params)
    s = r.json()
    print(s)
    session['token']  = s['access_token']
    
    url2 = 'https://auth.delta.nitt.edu/api/resources/user'
    headers2 = {'Authorization' : "Bearer " + s['access_token'],'Content-type': 'application/x-www-form-urlencoded'}
    print(headers2['Authorization'])
    params = {'client_id' : 'SXlKVDxrzf9dXwUN','client_secret':'nZvL2jfZV3tggKSioPOQum6lTQ~QSbUR','grant_type':'authorization_code','code':d,'redirect_uri':'http://127.0.0.1:5000/log'}
    r = requests.post(url2,headers = headers2,data = params)
    print(r.content)
    dat = r.json()
    session['data'] = dat
    n = dat['name']
    t1 = n.split(" ")
    n = "_".join(t1)
    if ("D-" + n) not in User:
        print('UUUUUUUUUUUUUU')
        return redirect('/register')
    else:
        con = sqlite3.connect('users4.db')
        cursor = con.cursor()
        d = "D-" + n
        cursor.execute(f'select * from USERS where username = "{d}"')
        for i in cursor:
            dname = i[0]
            branch = i[4]
            hostel = i[3]
            break 
        dat['hostel'] = hostel
        dat['branch'] = branch
        dat['dname'] = dname
        session['cuser'] = "D-" + n;
        return render_template('home.html',data = dat)

@app.route('/register')
def reg():
    
    return render_template('register.html')


@app.route('/reg',methods = ['POST','GET'])
def regi():
    global User
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    dn = request.form.get('dname')
    h = request.form.get('hostel')
    b = request.form.get('branch')
    
    d1 = session['data']['email']
    
    n = session['data']['name']
    t1 = n.split(" ")
    n = "_".join(t1)
    n = "D-" + n
    cursor.execute('insert into USERS values("' + str(dn) +'","'+ str(n) +'","' + str(d1) +'","' + str(h) + '","' + str(b) + '")')
    con.commit()
    User = getU()

    con.close()
    return render_template('home.html',data = session['data'])


@app.route('/search',methods = ['POST','GET'])
def search():
    s = request.form['st']
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    h = request.form['ht']
    b = request.form['bt']
    u = session['cuser']
    plus1 = []
    cursor.execute(f'select you from Friends where me = "{u}"')
    for i in cursor:
        plus1.append(i[0])
    cursor.execute(f'select me from Friends where you = "{u}"')
    for i in cursor:
        plus1.append(i[0])
    t3 = set(plus1)
    plus1 = list(t3)
    plus2 = []
    for f1 in plus1:
        cursor.execute(f'select you from Friends where me = "{f1}"')
        for i in cursor:
            plus2.append(i[0])
        cursor.execute(f'select me from Friends where you = "{f1}"')
        for i in cursor:
            plus2.append(i[0])
    t3 = set(plus2)
    plus2 = list(t3)
    plus3 = []
    for f1 in plus2:
        cursor.execute(f'select you from Friends where me = "{f1}"')
        for i in cursor:
            plus3.append(i[0])
        cursor.execute(f'select me from Friends where you = "{f1}"')
        for i in cursor:
            plus3.append(i[0])
    t4 = set(plus3)
    plus3 = list(t4)

    cursor.execute('select * from USERS')
    l = []
    s = s.lower()
    for i in cursor:
        if s in i[1].lower():
            if i[1] == session['cuser']:
                continue
            if h == 'ALL':
                if b == 'ALL':
                    l.append(i)
                else:
                    if b == i[4]:
                        l.append(i)
            else:
                if h == i[3]:
                    if b == 'ALL':
                        l.append(i)
                    else:
                        if b == i[4]:
                            l.append(i)
        elif s in i[0].lower():
            if h == 'ALL':
                if b == 'ALL':
                    l.append(i)
                else:
                    if b == i[4]:
                        l.append(i)
            else:
                if h == i[3]:
                    if b == 'ALL':
                        l.append(i)
                    else:
                        if b == i[4]:
                            l.append(i)
    t1 = session['cuser']
    cursor.execute(f'select tof from FriendsReq where sender = "{t1}"')
    l1 = [] 
    for i in cursor:
        l1.append(i[0])
    print(l)
    c = session['cuser']
    return jsonify({'data' : l,'sent' : l1,'user' : c,'con':[plus1,plus2,plus3]})

@app.route('/nlog', methods = ['POST'])
def nlog():
    
    n = request.form['nt']
    
    passi = request.form['passt']
    
    User = getU()
    
    if n in User:
        con = sqlite3.connect('users4.db')
        cursor = con.cursor()
        cursor.execute('create table if not exists REG(username varchar, password varchar)')
        cursor.execute(f'select * from REG where username = "{n}"')
        passit = None
        for i in cursor:
            passit = i[1]
            break 
        if passit != None and passit == passi:
            cursor.execute(f'select * from USERS where username = "{n}"')
            dt = {}
            for i in cursor:
                dt['dname'] = i[0]
                dt['name'] = i[1]
                dt['email'] = i[2]
                dt['hostel'] = i[3]
                dt['branch'] = i[4]
            session['dt'] = dt
            session['cuser'] = dt['name'];
            return jsonify({'info' : 'correct'})
            
    return jsonify({'info' :  'Username or password is incorrect'})


@app.route('/nlog2', methods = ['POST','GET'])
def nlog2():
    return render_template('home.html',data = session['dt'])


@app.route('/regform')
def regform():
    return render_template('nregister.html')

@app.route('/nreg',methods = ['POST'])
def nreg():
    dn = request.form['dnt']
    n = request.form['nt']
    passt =request.form['passt']
    cpass =request.form['cpasst']
    e = request.form['et']
    h = request.form['ht']
    b = request.form['bt']
    User = getU()
    if n in User:
        return jsonify({'info':'Username already registered/taken'})
    
    capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smallalphabets="abcdefghijklmnopqrstuvwxyz"
    specialchar="$@_"
    digits="0123456789"

    Ca = 0
    Sm = 0
    Sc = 0
    Di = 0
    for i in passt:
        if i in capitalalphabets:
            Ca+=1 
        if i in smallalphabets:
            Sm+=1 
        if i in specialchar:
            Sc+=1 
        if i in digits:
            Di+=1 
    
    if not Ca:
        return jsonify({'info' : 'The password should contain a uppercase letter'})
    
    if not Sm:
        return jsonify({'info' : 'The password should contain a lowercase letter'})

    if not Sc:
        return jsonify({'info' : 'The password should contain a one of the special character ($,@,_)'})

    if not Di:
        return jsonify({'info' : 'The password should contain a digit'})
    
    if len(passt) < 8:
        return jsonify({'info' : "The password should atleast have 8 characters"})


    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    
    if passt == cpass:
        cursor.execute('insert into USERS values("' + str(dn) +'","'+ str(n) +'","' + str(e) +'","' + str(h) + '","' + str(b) + '")')
        con.commit()
        cursor.execute('insert into REG values("' + str(n) + '","' + str(passt) + '")')
        con.commit()
        con.close()
        return jsonify({'info' : 'User registered successfully' })
        
    else:
        con.close()
        return jsonify({'info' : 'Password and confirm password do not match'})



@app.route('/dum', methods = ['POST'])
def dum():
    return jsonify({'info':'Success'})


@app.route('/sfr', methods = ['POST'])
def friendreq():
    name = request.form['st']
    sender = session['cuser']
    print('sdsd')
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists FriendsReq(sender varchar,tof varchar)')

    cursor.execute(f'insert into FriendsReq values("{sender}","{name}")')
    con.commit()

    R = []
    cursor.execute('select * from FriendsReq')
    for i in cursor:
        R.append(i)
    print(R)
    con.close()
    return jsonify({'info':1})

@app.route('/frr', methods = ['POST'])
def frr():
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists FriendsReq(sender varchar,tof varchar)')
    u = session['cuser']
    cursor.execute(f'select sender from FriendsReq where tof = "{u}"')
    L = []
    for i in cursor:
        L.append(i[0])

    return jsonify({'data' : L})

@app.route('/afr', methods = ['POST'])
def afr():
    name = request.form['st']
    sender = session['cuser']
    print('sdsd')
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists Friends(me varchar,you varchar)')

    cursor.execute(f'insert into Friends values("{sender}","{name}")')
    con.commit()
    cursor.execute(f'delete from FriendsReq where tof = "{sender}" and sender = "{name}"')
    con.commit()
    R = []
    # cursor.execute('select * from FriendsReq')
    # for i in cursor:
    #     R.append(i)
    # print(R)
    con.close()
    return jsonify({'info':1})

@app.route('/fr', methods = ['POST'])
def fr():
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists Friends(me varchar,you varchar)')
    u = session['cuser']
    cursor.execute(f'select you from Friends where me = "{u}"')
    L = []
    for i in cursor:
        L.append(i[0])
    cursor.execute(f'select me from Friends where you = "{u}"')
    for i in cursor:
        L.append(i[0])
    t1 = set(L)
    t2 = list(t1)
    return jsonify({'data' : t2})

@app.route('/viewp', methods = ['POST'])
def viewp():
    u = request.form['st']
    print(u)
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute(f'select * from USERS where username = "{u}"')
    L = []
    for i in cursor:
        L.append(i)
    
    t1 = session['cuser']
    cursor.execute(f'select tof from FriendsReq where sender = "{t1}"')
    l1 = [] 
    for i in cursor:
        l1.append(i[0])

    cursor.execute(f'select you from Friends where me = "{t1}"')
    l2 = []
    for i in cursor:
        l2.append(i[0])
    cursor.execute(f'select me from Friends where you = "{t1}"')
    for i in cursor:
        l2.append(i[0])
    print(l2)
    t1 = set(l2)
    l2 = list(t1)
    return jsonify({'data' : L, 'sent' : l1,'friends' : l2})


@app.route('/fs', methods = ['POST'])
def fs():
    t2 = session['cuser']
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute(f'select you from Friends where me = "{t2}"')
    l2 = []
    for i in cursor:
        l2.append(i[0])
    cursor.execute(f'select me from Friends where you = "{t2}"')
    for i in cursor:
        l2.append(i[0])
    print(l2)

    t1 = set(l2)
    l2 = list(t1)
    l3 = []
    cursor.execute(f'select tof from SLAMS where sender = "{t2}"')
    for i in cursor:
        l3.append(i[0])
    return jsonify({'data' : l2,'sent':l3})



@app.route('/sendslam', methods = ['POST'])
def sendslam():
    q1 = request.form['q1t']
    q2 = request.form['q2t']
    q3 = request.form['q3t']
    q4 = request.form['q4t']
    q5 = request.form['q5t']
    q6 = request.form['q6t']
    q7 = request.form['q7t']
    tof = request.form['st']
    u = session['cuser']
    s = [u,tof,q1,q2,q3,q4,q5,q6,q7]
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists SLAMS(tof varchar,sender varchar,q1 varchar,q2 varchar,q3 varchar,q4 varchar,q5 varchar,q6 varchar,q7 varchar)')
    cursor.execute(f'insert into SLAMS values("{tof}","{u}","{q1}","{q2}","{q3}","{q4}","{q5}","{q6}","{q7}")')
    con.commit()
    con.close()
    session['touser'] = tof
    return jsonify({'data' : 'success'})

@app.route('/ys', methods = ['POST'])
def ys():
    u = session['cuser']
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists SLAMS(tof varchar,sender varchar,q1 varchar,q2 varchar,q3 varchar,q4 varchar,q5 varchar,q6 varchar,q7 varchar)')
    cursor.execute(f'select sender from SLAMS where tof = "{u}"')
    L = []
    
    for i in cursor:
        L.append(i[0])

    s = set(L)
    L = list(s) 
    
    u1 = session['cuser']
    return jsonify({'data' : L,'user' : u1})

@app.route('/showys', methods = ['POST'])
def showys():
    u = session['cuser']
    s = request.form['st']
    print(s)
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists SLAMS(tof varchar,sender varchar,q1 varchar,q2 varchar,q3 varchar,q4 varchar,q5 varchar,q6 varchar,q7 varchar)')
    cursor.execute(f'select * from SLAMS where tof = "{u}" and sender = "{s}"')
    L = []
    for i in cursor:
        L = list(i) 
    print(L)

    l2 = ['na','na','Birthday','Motto','Hobbies','Likes','Dislikes','First thing you notice in me','BestFriend']

    return jsonify({'data':L,'Q' : l2,'user' : u})

@app.route('/dsl', methods = ['POST'])
def dsl():
    s = request.form['st']
    c = session['cuser']
    con = sqlite3.connect('users4.db')
    cursor = con.cursor()
    cursor.execute(f'delete from SLAMS where sender = "{c}" and tof = "{s}"')
    print(f'delete from SLAMS where sender = "{c}" and tof = "{s}"')
    con.commit()
    cursor.execute('select * from SLAMS')
    for i in cursor:
        print(i)
    return jsonify({'data':1})

@app.route('/pred',methods = ['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'data' : 'nofile'})
        file = request.files['file']
        tof = session['touser']
        u = session['cuser']
        f = tof + "-" + u
        file.save(f"static/images/{f}.jpg")
        return jsonify({'data':1})
    except:
        return jsonify({'error':'Unexpected error (check the file, only jpg allowed)'})


if __name__ == '__main__':
    app.run(debug = True)