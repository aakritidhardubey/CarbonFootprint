import streamlit as st
import os 
import requests
from dotenv import load_dotenv
import matplotlib.pyplot as plt


load_dotenv()

API_KEY =os.getenv("API_KEY")
DEPLOYMENT_URL=os.getenv("DEPLOYMENT_URL")

if not API_KEY or not DEPLOYMENT_URL:
    st.error("Missing API configuration. Check your .env file.")
    st.stop()

st.set_page_config(
    page_title="Carbon Coach", 
    layout="wide", 
    page_icon="🌍",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    footer {visibility: hidden !important;}
    .main .block-container {
        padding: 2rem 1rem !important;
        background: #f0fdf4 !important;
        max-width: 1200px !important;
    }
    .main-header {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border-radius: 20px !important;
        text-align: center !important;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.3) !important;
        border: 3px solid #34d399 !important;
        animation: slideDown 0.8s ease-out !important;
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    .main-header p {
        font-size: 1.3rem !important;
        margin: 1rem 0 0 0 !important;
        color: #d1fae5 !important;
        opacity: 0.95 !important;
    }
            
    .stForm {
        border: 3px solid #22c55e !important;
        border-radius: 20px !important;
    }
    
    .stSelectbox > div > div > div {
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div > div:hover {
        transform: translateY(-1px) !important;
    }
    .stButton> button{
            background:linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    }
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
            
    .stButton > button:hover {
        background:light red  !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.4) !important;
        border-color: #10b981 !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-container_value"] {
        color: #065f46 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-container_label"] {
        color: #047857 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
    }
            
</style>
""", unsafe_allow_html=True)

def get_ibm_token(api_key):
    try:
        url = "https://iam.cloud.ibm.com/identity/token"
        data = {"apikey": api_key, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"}
        response = requests.post(url, data=data, timeout=30)
        
        if response.status_code != 200:
            st.error(f"Authentication failed: {response.status_code}")
            return None
            
        return response.json()["access_token"]
    except requests.exceptions.RequestException:
        st.error("Network error during authentication")
        return None
    except KeyError:
        st.error("Invalid API key")
        return None


def calculate_pie_chart_data(distance, grocery, tv_hours, bag_count):
    transport = distance * 0.21 * 12  
    food = grocery * 0.002 * 12        
    energy = tv_hours * 0.5 * 365     
    waste = bag_count * 2.5 * 52      
    
    return [transport, food, energy, waste]

def calculate_eco_score(footprint):
    return max(0, 100 - footprint / 100)

st.markdown("""
<div class="main-header">
    <h1>🌍 Carbon Coach</h1>
    <p style="font-size: 1.2rem; margin: 0;">Discover your carbon footprint and get personalized climate tips</p>
    <p style="font-size: 1rem; opacity: 0.9; margin: 0.5rem 0 0 0;">Powered by IBM Watson ML 🚀</p>
</div>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "form"

if  st.session_state.page=="form":
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    with st.form("carbon_form"):
            st.markdown("### 📋 Tell us about your lifestyle")
            st.markdown("---")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**👤 Personal Info**")
                body_type = st.selectbox("Body Type", ["Thin", "Average", "Overweight"])
                sex = st.selectbox("Sex", ["Male", "Female"])
                diet = st.selectbox("Diet", ["Meat Eater", "Vegetarian", "Vegan"])
                shower = st.selectbox("How Often You Shower", ["Daily", "Few Times a Week", "Rarely"])
                social = st.selectbox("Social Activity", ["Low", "Medium", "High"])
                
                st.markdown("**♻️ Sustainability**")
                energy_eff = st.selectbox("Energy Efficient Appliances?", ["Yes", "No"])
                recycling = st.selectbox("Do You Recycle?", ["Yes", "No"])

            with col2:
                st.markdown("**🏠 Home & Energy**")
                heating = st.selectbox("Heating Energy Source", ["Electricity", "Gas", "Wood", "None"])
                cooking = st.selectbox("Cooking With", ["Gas", "Electric"])
                tv_hours = st.number_input("TV/PC Hours per Day", 0, 24, 4)
                internet = st.number_input("Internet Hours per Day", 0, 24, 6)
                
                st.markdown("**🛍️ Consumption**")
                grocery = st.number_input("Monthly Grocery Bill (₹)", 100, 50000, 5000)
                clothes = st.number_input("New Clothes per Month", 0, 100, 5)

            with col3:
                st.markdown("**🚗 Transportation**")
                transport = st.selectbox("Transport Type", ["Car", "Public Transport", "Cycle", "Walk"])
                vehicle = st.selectbox("Vehicle Type", ["None", "Petrol", "Diesel", "Electric"])
                distance = st.number_input("Monthly Vehicle Distance (km)", 0, 10000, 500)
                flights = st.selectbox("Air Travel Frequency", ["Never", "Rarely", "Often"])
                
                st.markdown("**🗑️ Waste**")
                bag_size = st.selectbox("Waste Bag Size", ["Small", "Medium", "Large"])
                bag_count = st.number_input("Bags per Week", 0, 50, 3)

            st.markdown("---")
            submit = st.form_submit_button("🔍 Calculate My Carbon Footprint")

    st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if grocery > 50000:
            st.error("Monthly grocery bill seems unrealistic")
            st.stop()
        if distance > 10000:
            st.error("Monthly vehicle distance seems unrealistic")
            st.stop()
        if bag_count > 50:
            st.error("Waste bags per week seems unrealistic")
            st.stop()
            
        with st.spinner("🔄 Calculating your carbon footprint..."):
            token = get_ibm_token(API_KEY)
            
            if not token:
                st.stop()
                
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
            
            payload = {
                "input_data": [
                    {
                        "fields": [
                            "Body Type", "Sex", "Diet", "How Often Shower", "Heating Energy Source",
                            "Transport", "Vehicle Type", "Social Activity", "Monthly Grocery Bill",
                            "Frequency of Traveling by Air", "Vehicle Monthly Distance Km", "Waste Bag Size",
                            "Waste Bag Weekly Count", "How Long TV PC Daily Hour", "How Many New Clothes Monthly",
                            "How Long Internet Daily Hour", "Energy efficiency", "Recycling", "Cooking_With"
                        ],
                        "values": [[
                            body_type, sex, diet, shower, heating, transport, vehicle,
                            social, grocery, flights, distance, bag_size, bag_count,
                            tv_hours, clothes, internet, energy_eff, recycling, cooking
                        ]]
                    }
                ]
            }

            try:
                response = requests.post(DEPLOYMENT_URL, json=payload, headers=headers, timeout=60)
                
                if response.status_code != 200:
                    st.error(f"Prediction failed with status: {response.status_code}")
                    st.stop()
                    
                result_data = response.json()
                
                if 'predictions' not in result_data:
                    st.error("Invalid response format from API")
                    st.stop()
                    
                predictions = result_data['predictions']
                if not predictions or 'values' not in predictions[0]:
                    st.error("No prediction values in response")
                    st.stop()
                    
                result = predictions[0]['values'][0][0]
                
                if not isinstance(result, (int, float)) or result < 0 or result > 100000:
                    st.error("Invalid prediction result received")
                    st.stop()

                st.session_state.result = result
                st.session_state.distance = distance
                st.session_state.grocery = grocery
                st.session_state.tv_hours = tv_hours
                st.session_state.bag_count = bag_count
                st.session_state.page ="resultP"
                st.rerun()

            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except requests.exceptions.RequestException:
                st.error("Network error during prediction")
            except (KeyError, IndexError, TypeError):
                st.error("Invalid response format from prediction API")
            except Exception as e:
                st.error(f"Unexpected error occurred during prediction: {str(e)}")
                st.text(f"Error details: {type(e).__name__}")


elif st.session_state.page =="resultP":
    st.markdown("""
    <script>
        window.scrollTo({top: 0, behavior: 'smooth'});
    </script>
""", unsafe_allow_html=True)
    result = st.session_state.result
    distance = st.session_state.distance
    grocery = st.session_state.grocery
    tv_hours = st.session_state.tv_hours
    bag_count = st.session_state.bag_count
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: white; border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <h2 style="color: #2E8B57; margin-bottom: 1rem;">🌱 Your Carbon Footprint Results</h2>
        <h1 style="color: #FF6B35; font-size: 3rem; margin: 0;">{result:.0f} kg CO₂</h1>
        <p style="color: #666; font-size: 1.2rem;">per year</p>
    </div>
    """, unsafe_allow_html=True)

    EXCELLENT_THRESHOLD = 3000
    AVERAGE_THRESHOLD = 7000

    if result < EXCELLENT_THRESHOLD:
        tip = "✅ Excellent! You're a climate hero. Keep it up!"
        tip_color = "#28a745"
    elif result < AVERAGE_THRESHOLD:
        tip = "⚠️ Average. Consider biking, saving energy, or reducing waste."
        tip_color = "#ffc107"
    else:
        tip = "❌ High impact. Time to take action: diet, travel, energy use."
        tip_color = "#dc3545"

    st.markdown(f"""
    <div style="background: {tip_color}20; border-left: 5px solid {tip_color}; padding: 1.5rem; border-radius: 10px; margin: 2rem 0;">
        <h3 style="color: {tip_color};">{tip}</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        score = calculate_eco_score(result)
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("💚 Eco Score", f"{score:.1f}/100")
        st.progress(min(max(score / 100, 0), 1))
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 🥧 Footprint Breakdown")
        
        labels = ['Transport', 'Food', 'Energy', 'Waste']
        data = calculate_pie_chart_data(distance, grocery, tv_hours, bag_count)
        
        if sum(data) > 0:
            fig, ax = plt.subplots(figsize=(8, 6))
            colors = ["#FA3B3B", "#6391EC", "#58D6F3", "#93F0C5"]
            wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            ax.set_title('Your Carbon Footprint by Category', fontsize=14, fontweight='bold', pad=20)
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("No significant emissions detected in breakdown categories.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🔄 Calculate Again", type="primary"):
        st.session_state.page = "form"
        st.rerun()