# Laptop Price Predictor

An end-to-end machine learning web application that estimates laptop market prices from hardware specifications and displays the predicted valuation in Sri Lankan Rupees (LKR).

---

## Overview

This project combines a supervised regression pipeline built in Jupyter Notebook with a Flask web application (**Laptop Valuation Desk**). Users configure a laptop's specifications—RAM, weight, display features, manufacturer, form factor, operating system, processor, and graphics—and receive an instant price estimate powered by a tuned Random Forest model.

---

## Project Structure

```text
Laptop_Price_Predictor/
├── Model/
│   ├── laptop_price.csv          # Raw dataset (1,303 laptop records)
│   ├── Model Building.ipynb      # Data cleaning, feature engineering, model training & tuning
│   └── predictor.pickle          # Serialized best-performing model
├── Web site/
│   ├── Model/
│   │   └── predictor.pickle      # Model artifact used by the Flask app
│   ├── templates/
│   │   ├── index.html            # Frontend UI (Laptop Valuation Desk)
│   │   └── styles.css            # Application styling
│   ├── app.py                    # Flask backend and /predict API endpoint
│   └── Procfile                  # Gunicorn entry point for deployment
├── requirments.txt               # Python dependencies
└── README.md
```

---

## Dataset & Feature Engineering

The model is trained on `Model/laptop_price.csv` (1,303 rows), predicting `Price_euros` from 30 engineered features:

| Category | Features |
| :--- | :--- |
| **Numeric** | `Ram` (GB), `Weight` (kg) |
| **Display (Binary)** | `Touchscreen`, `IPS` |
| **Company (One-Hot)** | `Acer`, `Apple`, `Asus`, `Dell`, `HP`, `Lenovo`, `MSI`, `Toshiba`, `Other` |
| **Type (One-Hot)** | `2 in 1 Convertible`, `Gaming`, `Netbook`, `Notebook`, `Ultrabook`, `Workstation` |
| **OS (One-Hot)** | `Linux`, `Mac`, `Windows`, `Other` |
| **CPU (One-Hot)** | `Intel Core i3`, `Intel Core i5`, `Intel Core i7`, `Other` |
| **GPU (One-Hot)** | `AMD`, `Intel`, `Nvidia` |

On the web interface, the predicted EUR price is converted to LKR (`1 EUR = 449.50 LKR`).

---

## Model Training & Evaluation

Four regression algorithms were compared on a 75/25 train-test split, followed by hyperparameter tuning with `GridSearchCV` on the top candidate:

| Model | Test $R^2$ Score |
| :--- | :---: |
| Linear Regression | `0.7022` |
| Lasso Regression | `0.7008` |
| Decision Tree Regressor | `0.6267` |
| Random Forest Regressor (default) | `0.7375` |
| **Random Forest Regressor (tuned: `criterion='absolute_error'`)** | **`0.7475`** |

The tuned `RandomForestRegressor` is exported via `pickle` to `predictor.pickle` and loaded lazily by the Flask backend.

---

## Getting Started

### Prerequisites

- Python 3.10+
- `pip`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RavinduPathirana28/Laptop_Price_Predictor.git
   cd Laptop_Price_Predictor
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirments.txt
   pip install flask
   ```

### Running the Web App Locally

```bash
cd "Web site"
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.

---

## API Reference

### `POST /predict`

Returns the predicted laptop price (in EUR) for a 30-element feature vector matching the training column order.

**Request Body (`application/json`)**
```json
{
  "features": [8, 1.37, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
}
```

**Response (`200 OK`)**
```json
{
  "price": 1345.25
}
```

---

## Tech Stack

- **Machine Learning:** Python, Pandas, NumPy, scikit-learn, Jupyter Notebook
- **Backend:** Flask, Gunicorn
- **Frontend:** HTML5, CSS3, Vanilla JavaScript

---

## Author

**Ravindu Pathirana** — [@RavinduPathirana28](https://github.com/RavinduPathirana28)
