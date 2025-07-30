# 🌍  Lifestyle Carbon Footprint Estimator

An intelligent web app that predicts your **annual carbon footprint (in kg CO₂e)** based on your daily lifestyle habits. Built using **IBM Watson AutoAI** for automatic model training and **Streamlit** for a fast, interactive frontend.

---

## 📌 Features

- ♻️ Predicts personal carbon footprint using 19 lifestyle-related inputs
- 📊 Categorizes users into:
  - **Climate Hero** 🌱
  - **Moderate Impact** ⚖️
  - **High Carbon Lifestyle** 🔥
- 💡 Offers climate-friendly tips for reducing carbon footprint
- ⚙️ Powered by **IBM Watson AutoAI** and deployed via **Watson Machine Learning**
- 🔐 Secure API usage with `.env` environment variables
- 🧠 Uses RMSE as model evaluation metric

---

## 🖥️ Tech Stack

- **IBM Watson AutoAI**
- **Streamlit**
- **Python 3.10+**
- **Requests** – for API communication
- **python-dotenv** – for environment variable management

---

## 📂 Project Structure

carbon_calci/
│
├── main.py # Streamlit app
├── .env # Stores API key and URL securely
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── assets/ # (Optional) images/icons used

---

## 🚀 How to Run the App Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/carbon-footprint-estimator.git
cd carbon-footprint-estimator
```
### 2️⃣ Install required dependencies
``` bash
Copy code
pip install -r requirements.txt
```
### 3️⃣ Create .env file with your IBM credentials
<pre> ```ini # .env file API_KEY=your_ibm_cloud_api_key 
DEPLOYMENT_URL=your_ibm_model_deployment_url ``` </pre>
### 4️⃣ Run the app using Streamlit
```bash
Copy code
streamlit run main.py
```
--- 

### 🔢 Sample Input Fields
These 19 fields are collected from the user to predict their carbon footprint:

- Body Type
- Sex
- Diet
- How Often Shower
- Heating Energy Source
- Transport
- Vehicle Type
- Social Activity
- Monthly Grocery Bill
- Frequency of Traveling by Air
- Vehicle Monthly Distance (Km)
- Waste Bag Size
- Waste Bag Weekly Count
- Hours on TV/PC Daily
- New Clothes Bought Monthly
- Hours on Internet Daily
- Energy Efficiency
- Recycling
- Cooking With

---

### 📈 Model Information
-   🔍 AutoAI selected the best regression model using RMSE
-   🧪 Trained on lifestyle-based carbon emission dataset from Kaggle
-    🔄 Real-time predictions via IBM Watson Machine Learning API

---

### ✅ Future Improvements
- 📢 Add TTS-based climate tips (optional)
- 📊 Charts and comparison visualizations
- 📝 Export personalized carbon report
- 🔗 Social media share options

---

### 💡 Inspiration
This app was built as an awareness-driven innovation to help  users understand their carbon footprint based on common lifestyle choices — and take actionable steps to reduce it!

---

### 🤝 Acknowledgements
-   IBM Watson Studio AutoAI
-   Kaggle Carbon Footprint Dataset
-   Streamlit Open Source

---

### 📜 License
This project is open-source and free to use under the MIT License.
---