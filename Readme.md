# 📈 Recurrent Investment Simulator

A Streamlit app to simulate how a recurring monthly investment would have performed in various global stock market indices (e.g., S&P 500, MSCI World, Nikkei 225) over a custom time period.  
It helps visualize the power of compound interest and compare investment strategies across different regions and timeframes.

---

## 🚀 Features

- Choose from major global indices:
  - S&P 500 (SPY / ^GSPC)
  - MSCI World (URTH)
  - MSCI Japan (EWJ)
  - Nikkei 225 (^N225)
  - Europe (VGK)
  - Emerging Markets (EEM)
- Define your investment strategy:
  - Initial lump sum
  - Monthly recurring contribution
  - Start year and end year
- Visual simulation includes:
  - 📊 Stacked bar chart (contributions vs interest)
  - 📈 Line chart showing normalized index performance
  - 📋 Interest percentage annotation (% over total contribution)

---

## 📷 Example Output

*An example figure will be shown here after running the app locally.*  
It includes:
- Cumulative investment bars
- Red line for index evolution
- Annotated box with total interest earned in %

---

## 🛠 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/recurrent-investment-simulator.git
cd recurrent-investment-simulator
```

2. **Install the required Python packages**:

```bash
pip install -r requirements.txt
```

3. **Run the Streamlit app**:

```bash
streamlit run app.py
```

---

## 📦 Requirements

- Python ≥ 3.8
- `streamlit`
- `yfinance`
- `pandas`
- `numpy`
- `matplotlib`

You can generate `requirements.txt` with:

```bash
pip freeze > requirements.txt
```

---

## ⚠️ Disclaimer

This simulator is for **educational and illustrative purposes only**.  
It does **not** constitute financial advice. Past performance is not indicative of future results.

---

## 🧠 Future Ideas

- Add inflation-adjusted returns
- Allow CSV download of simulation data
- Compare multiple indices side-by-side
- Support for custom ETFs or stocks

---

## 🤝 Contributions

Pull requests and suggestions are welcome.  
Please open an issue to discuss any major changes before submitting.

---

## 📬 Contact

For feedback or collaboration, feel free to reach out via GitHub Issues.
