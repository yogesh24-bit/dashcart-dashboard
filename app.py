from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username']=='admin' and request.form['password']=='admin':
            session['logged_in'] = True
            return redirect(url_for('upload'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(path)
        session['csv_file'] = filename
        return redirect(url_for('dashboard'))
    return render_template('upload.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    filename = session.get('csv_file')
    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    df.columns = df.columns.str.lower()
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['quantity_ordered'] = pd.to_numeric(df['quantity_ordered'], errors='coerce')
    df['price_each'] = pd.to_numeric(df['price_each'], errors='coerce')
    df.dropna(subset=['order_id','product','quantity_ordered','price_each','order_date'], inplace=True)
    df['revenue'] = df['quantity_ordered'] * df['price_each']
    df['month'] = df['order_date'].dt.month_name()

    # Filters
    prod_filter = request.values.get('product_filter', 'All')
    mon_filter = request.values.get('month_filter', 'All')
    if 'category' in df.columns:
        cat_filter = request.values.get('category_filter','All')
    else:
        cat_filter = None

    df_f = df.copy()
    if prod_filter!='All':
        df_f = df_f[df_f['product']==prod_filter]
    if mon_filter!='All':
        df_f = df_f[df_f['month']==mon_filter]
    if cat_filter and cat_filter!='All':
        df_f = df_f[df_f['category']==cat_filter]

    # Metrics post-filter
    total_orders = df_f['order_id'].nunique()
    total_quantity = int(df_f['quantity_ordered'].sum())
    total_revenue = round(df_f['revenue'].sum(),2)
    total_products = df_f['product'].nunique()

    # Product table
    product_table = df_f.groupby('product').agg({
        'quantity_ordered':'sum','revenue':'sum'
    }).reset_index().sort_values(by='revenue',ascending=False).to_dict('records')

    # Chart data
    top = pd.DataFrame(product_table).head(5)
    top_labels = top['product'].tolist()
    top_values = [int(x) for x in top['quantity_ordered']]

    monthly_tot = df_f.groupby('month')['revenue'].sum()
    months = list(monthly_tot.index)
    month_values = monthly_tot.round(2).tolist()

    # Prediction
    df_pred = df.groupby(df['order_date'].dt.to_period('M'))[['quantity_ordered', 'revenue']].sum().reset_index()
    df_pred['month_num'] = df_pred['order_date'].dt.to_timestamp().map(lambda x: x.year*12+x.month)
    # train
    X = df_pred[['month_num']]
    y = df_pred['revenue']
    model = LinearRegression().fit(X, y)
    future = []
    last = df_pred['month_num'].max()
    for i in range(1,4): future.append([last+i])
    preds = model.predict(np.array(future))
    pred_months = [ (df_pred['order_date'].dt.to_timestamp().iloc[-1] + pd.DateOffset(months=i)).strftime('%b %Y') for i in range(1,4) ]
    predicted = dict(zip(pred_months, [round(p,2) for p in preds]))

    # Dropdown options
    prods = ['All'] + sorted(df['product'].unique().tolist())
    months_opts = ['All'] + sorted(df['month'].unique().tolist())
    if cat_filter is not None:
        cats = ['All'] + sorted(df['category'].unique().tolist())
    else:
        cats = None

    return render_template('dashboard.html',
        total_orders=total_orders, total_quantity=total_quantity, total_revenue=total_revenue,
        total_products=total_products, product_table=product_table,
        top_labels=top_labels, top_values=top_values,
        months=months, month_values=month_values,
        predicted=predicted,
        products=prods, months_opts=months_opts, categories=cats,
        sel_prod=prod_filter, sel_mon=mon_filter, sel_cat=cat_filter
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)
