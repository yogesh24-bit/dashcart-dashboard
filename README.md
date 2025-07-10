# 🛒 DashCart – E-Commerce Analytics Dashboard

`DashCart` is a lightweight, data-driven e-commerce analytics tool built with **Flask**, **HTML + CSS**, and popular **Python data-science libraries**.  
It lets you upload raw sales data (CSV), explores key metrics, and even predicts future revenue — all in a single-page dashboard with smooth animated visuals.

---

## ✨ Key Features

| Category | Details |
|----------|---------|
| **Data Upload** | Drag-and-drop (or choose) CSV file, instantly parsed with **pandas** |
| **Core Metrics** | Total Products, Orders, Quantity Sold, Total Revenue, Average Order Value |
| **Visuals** | Bar & line charts (Matplotlib → rendered as PNG) |
| **ML Forecast** | Simple **Linear Regression** projection of next-month revenue |
| **UI Flair** | Gradient backgrounds, glass-card panels, floating/bouncing emoji icons |
| **Session Flow** | Login → Upload → Dashboard (logout supported) |

---

## 📸 Screenshots

### 🔐 Login Page  
![image](https://github.com/user-attachments/assets/a8ca22e9-ffc1-49ca-af4e-99a2ab9ffa00)

### 📤 Upload Page  
![image](https://github.com/user-attachments/assets/410185f6-c162-4638-9d7e-935f6a9d3a02)

### 📊 Dashboard  
![image](https://github.com/user-attachments/assets/2380e274-4a6f-445d-995a-44249d7b449c)
![image](https://github.com/user-attachments/assets/fb46b7f9-165e-4e49-be05-4d736d35e340)

## 📂 Project Structure

```
ECOM_DASHBOARD/
├── app.py                       # Flask app entry-point
├── templates/
│   ├── dashboard.html           # main dashboard view
│   ├── login.html               # login screen
│   └── upload.html              # CSV upload page
├── uploads/
│   └── mock_ecommerce_data.csv  # sample dataset (ignored in production)
├── requirements.txt             # Python deps  ← create with pip freeze
└── README.md                    # <-- you are here
```

> **Note**  
> If you later add images / videos / external CSS or JS, create a `static/` folder and reference files via  
> `{{ url_for('static', filename='path/to/file') }}` inside your HTML.

---

## 🏃‍♂️ Quick Start

```bash
# 1. Clone
git clone https://github.com/your-username/dashcart.git
cd dashcart                     # or ECOM_DASHBOARD

# 2. (Optional) virtual env
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Dependencies
pip install -r requirements.txt

# 4. Run the server
python app.py
```

Visit **http://127.0.0.1:5000** in your browser → log in (default user in `app.py`) → upload a CSV → explore the dashboard!

---

## 📈 Sample CSV Format

```csv
Date,Product,Category,Quantity,Price
2024-01-01,LED Monitor,Electronics,2,199.99
2024-01-02,Laptop Stand,Accessories,3,39.99
...
```

*Columns are flexible, but must include* **Date**, **Product**, **Quantity**, **Price** *(case-insensitive).*

---

## 🧠 Machine Learning Note

A **Scikit-learn Linear Regression** model is (re)trained on every upload:

1. Aggregate revenue per month  
2. Fit linear regression  
3. Forecast next-period revenue (shown beneath metrics)

For production-grade accuracy you can swap in more sophisticated models (ARIMA, Prophet, etc.).

---

## 📌 Roadmap

- [x] CSV ingest & basic charts  
- [x] ML revenue forecast  
- [x] Animated emoji background  
- [ ] Export dashboard to PDF  
- [ ] User registration & roles  
- [ ] Dockerfile + CI/CD  
- [ ] Deploy on Render / Railway

---

## 🛠 Requirements

Add these (and anything else you import) to **`requirements.txt`**:

```
Flask
pandas
matplotlib
scikit-learn
```

Generate automatically:

```bash
pip freeze > requirements.txt
```

---

## 🙋‍♂️ Author

**Yogesh M.** – B.Tech IT, Easwari Engineering College  
📧 yogesh2462006@gmail.com |“🔗 [LinkedIn](https://www.linkedin.com/in/yogesh2406/)”

**Kishore Narayanan S R** - B.E CSE(IoT), Saveetha Engineering College 

📧 kishorenarayanan2627@gmail.com |“🔗 [LinkedIn](https://www.linkedin.com/in/kishorenarayanansr/)” | “💻 [GitHub](https://github.com/KISHORENARAYANANSR/)”

> _“Visualize. Optimize. Profit.” — DashCart_

---

### License

This project is released under the **MIT License** – see `LICENSE` for details.
