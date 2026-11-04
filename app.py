from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key=os.environ.get('SECRET_KEY','dev-secret-change-this')
app.config['UPLOAD_FOLDER']=os.path.join(app.root_path,'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)
DB=os.path.join(app.root_path,'restaurant.db')

def connect():
    con=sqlite3.connect(DB); con.row_factory=sqlite3.Row; con.execute('PRAGMA foreign_keys=ON'); return con
def query_db(sql,args=()):
    with connect() as con: return con.execute(sql,args).fetchall()
def execute_db(sql,args=()):
    with connect() as con: con.execute(sql,args); con.commit()

def init_db():
    with connect() as con:
        con.executescript("\nCREATE TABLE IF NOT EXISTS menu(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL, available INTEGER DEFAULT 1);\nCREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT, customer TEXT NOT NULL, items TEXT NOT NULL, total REAL NOT NULL, status TEXT DEFAULT 'Received', created_at TEXT DEFAULT CURRENT_TIMESTAMP);\nCREATE TABLE IF NOT EXISTS reservations(id INTEGER PRIMARY KEY AUTOINCREMENT, customer TEXT NOT NULL, date TEXT NOT NULL, time TEXT NOT NULL, guests INTEGER NOT NULL, status TEXT DEFAULT 'Confirmed');\n")
        con.executescript("INSERT OR IGNORE INTO menu(id,name,category,price,available) VALUES\n(1,'Margherita Pizza','Pizza',249,1),(2,'Farmhouse Pizza','Pizza',329,1),(3,'Classic Burger','Burgers',159,1),(4,'Paneer Wrap','Wraps',139,1),(5,'Cold Coffee','Drinks',99,1),(6,'Pasta Alfredo','Pasta',229,1);")
        con.commit()


@app.route('/')
def home():
    menu=query_db("SELECT * FROM menu WHERE available=1 ORDER BY category")
    orders=query_db("SELECT * FROM orders ORDER BY id DESC LIMIT 10")
    reservations=query_db("SELECT * FROM reservations ORDER BY id DESC LIMIT 10")
    return render_template('home.html',menu=menu,orders=orders,reservations=reservations)
@app.route('/order',methods=['POST'])
def order():
    names=request.form.getlist('item_name'); prices=request.form.getlist('item_price'); qtys=request.form.getlist('qty')
    chosen=[]; total=0
    for name,price,qty in zip(names,prices,qtys):
        q=max(0,int(qty or 0)); p=float(price)
        if q: chosen.append(f'{name} x{q}'); total+=p*q
    if not chosen: flash('Choose at least one menu item.','warning'); return redirect(url_for('home'))
    execute_db("INSERT INTO orders(customer,items,total) VALUES(?,?,?)",(request.form['customer'],', '.join(chosen),total))
    flash('Order placed successfully!','success'); return redirect(url_for('home'))
@app.route('/orders/<int:oid>/status',methods=['POST'])
def order_status(oid):
    execute_db("UPDATE orders SET status=? WHERE id=?",(request.form['status'],oid)); flash('Order status updated.','success'); return redirect(url_for('home'))
@app.route('/reserve',methods=['POST'])
def reserve():
    execute_db("INSERT INTO reservations(customer,date,time,guests) VALUES(?,?,?,?)",(request.form['customer'],request.form['date'],request.form['time'],int(request.form['guests'])))
    flash('Table reservation received.','success'); return redirect(url_for('home'))
@app.route('/menu/add',methods=['POST'])
def menu_add():
    execute_db("INSERT INTO menu(name,category,price) VALUES(?,?,?)",(request.form['name'],request.form['category'],float(request.form['price'])))
    flash('Menu item added.','success'); return redirect(url_for('home'))


if __name__=='__main__':
    init_db()
    app.run(debug=True,port=5002)
