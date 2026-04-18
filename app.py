import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import datetime


# ✅ ADD THIS (Fix)
menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "Home",
        "Find Hospital",
        "Emergency Numbers"
    ]
)

# Your hospital data
HOSPITALS = {
    "Mumbai": [
        {
            "name": "Kokilaben Dhirubhai Ambani Hospital"
        }
    ]
}

# PART 1 (Keep as it is)
# Home Page
if menu == "Home":

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏠 Welcome to Medifind")

        st.info("""
        Medifind helps users quickly find nearby hospitals
        along with their facilities and services.
        """)

    with col2:
        st.success("""
        ✅ Fast Hospital Search  
        ✅ Easy to Use  
        ✅ Emergency Ready  
        """)

# Find Hospital Page
elif menu == "Find Hospital":

    st.header("🔍 Find Nearby Hospitals")

    city_list = list(set([h["city"] for h in hospitals]))

    selected_city = st.selectbox(
        "📍 Select City",
        city_list
    )

    st.markdown("### 🏥 Available Hospitals")

    found = False

    for h in hospitals:
        if h["city"] == selected_city:

            hospital_card(
                h["name"],
                h["beds"],
                h["ambulance"],
                h["treatments"]
            )

            found = True

    if not found:
        st.warning("⚠ No hospitals found in selected city.")

# Emergency Numbers Page
elif menu == "Emergency Numbers":

    st.header("🚑 Emergency Numbers (National)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📞 Emergency Contacts

        🚑 Ambulance: **108**  
        🚓 Police: **100**  
        🔥 Fire: **101**  
        ☎ General Emergency: **112**
        """)

    with col2:
        st.info("""
        In case of emergency, contact the nearest
        available service immediately.
        """)

# Footer
st.markdown("---")

st.markdown("""
<p style='text-align: center;'>
Developed by <b>Saransh Chakole</b> | MCA Project 2026
</p>
""", unsafe_allow_html=True)

# --- PAGE CONFIG & CUSTOM CSS ---
st.set_page_config(page_title="MediFind", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .hospital-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        border: 1px solid #e2e8f0;
    }
    .main-header {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(to right, #1e3a8a, #312e81);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .stat-card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# --- DATASET ---
HOSPITALS = {
    "Mumbai": [
        {
            "name": "Kokilaben Dhirubhai Ambani Hospital",
            "address": "Rao Saheb, Achutrao Patwardhan Marg, Four Bungalows, Andheri West, Mumbai – 400053",
            "lat": 19.1197, "lon": 72.8346, "rating": 4.8,
            "specialities": ["Cardiology", "Oncology", "Neurology", "Orthopedics", "Gastroenterology"],
            "emergency_no": "022-30999999", "ambulance_no": "022-30999911",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "NABH & JCI accredited 750-bed super-specialty hospital with state-of-the-art OT suites.",
            "rooms": {"General": 2500, "SemiPrivate": 5000, "Private": 9000, "ICU": 18000},
            "treatments": ["Robotic Surgery", "Bone Marrow Transplant", "CyberKnife Radiosurgery"],
            "ambulance": True, "beds": 750,
            "doctors": [{"name": "Dr. Santosh Shetty", "speciality": "Cardiology", "qualification": "MD, DM", "timing": "Mon–Fri 10am–2pm", "contact": "+91-9820000001"}]
        },
        {
            "name": "Lilavati Hospital & Research Centre",
            "address": "A-791, Bandra Reclamation, Bandra West, Mumbai – 400050",
            "lat": 19.0596, "lon": 72.8295, "rating": 4.6,
            "specialities": ["Nephrology", "Urology", "Dermatology", "Pediatrics", "Gynecology"],
            "emergency_no": "022-26751000", "ambulance_no": "022-26751099",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "Premier multi-specialty hospital with over 1,000 beds and renowned surgical teams.",
            "rooms": {"General": 2000, "SemiPrivate": 4500, "Private": 8000, "ICU": 15000},
            "treatments": ["Kidney Transplant", "In-vitro Fertilisation", "Paediatric Cardiac Surgery"],
            "ambulance": True, "beds": 1000,
            "doctors": [{"name": "Dr. Sanjay Kulkarni", "speciality": "Nephrology", "qualification": "MD, DM", "timing": "Mon–Fri 11am–3pm", "contact": "+91-9870000011"}]
        },
        {
            "name": "P. D. Hinduja Hospital",
            "address": "Veer Savarkar Marg, Mahim West, Mumbai – 400016",
            "lat": 19.0330, "lon": 72.8384, "rating": 4.7,
            "specialities": ["Neurology", "Oncology", "Endocrinology", "Orthopedics"],
            "emergency_no": "022-24452222", "ambulance_no": "022-24451111",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "Ultra-modern tertiary care hospital highly recognized for neurology and oncology.",
            "rooms": {"General": 2200, "SemiPrivate": 4800, "Private": 8500, "ICU": 16000},
            "treatments": ["Deep Brain Stimulation", "Joint Replacement", "Radiation Oncology"],
            "ambulance": True, "beds": 400,
            "doctors": [{"name": "Dr. Milind Nadkar", "speciality": "Endocrinology", "qualification": "MD, DNB", "timing": "Mon-Sat 9am-1pm", "contact": "+91-9811122233"}]
        },
        {
            "name": "Breach Candy Hospital",
            "address": "60 A, Bhulabhai Desai Marg, Breach Candy, Mumbai – 400026",
            "lat": 18.9730, "lon": 72.8055, "rating": 4.8,
            "specialities": ["Cardiology", "General Medicine", "Gastroenterology"],
            "emergency_no": "022-23667788", "ambulance_no": "022-23667799",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "A prestigious hospital in South Mumbai known for excellent patient care and elite doctors.",
            "rooms": {"General": 3000, "SemiPrivate": 6000, "Private": 12000, "ICU": 22000},
            "treatments": ["Coronary Angiography", "Endoscopy", "Minimally Invasive Surgeries"],
            "ambulance": True, "beds": 250,
            "doctors": [{"name": "Dr. Hemant Thacker", "speciality": "General Medicine", "qualification": "MD", "timing": "Tue-Fri 10am-4pm", "contact": "+91-9922334455"}]
        },
        {
            "name": "Dr L H Hiranandani Hospital",
            "address": "Hillside Avenue, Hiranandani Gardens, Powai, Mumbai – 400076",
            "lat": 19.1232, "lon": 72.9067, "rating": 4.5,
            "specialities": ["Orthopedics", "Gynecology", "Pediatrics"],
            "emergency_no": "022-25763333", "ambulance_no": "022-25763344",
            "image_url": "https://images.unsplash.com/photo-1516841273335-e39b37888115?w=800&q=80",
            "about": "Multi-specialty hospital in Powai focused on personalized healthcare.",
            "rooms": {"General": 1800, "SemiPrivate": 3500, "Private": 7000, "ICU": 14000},
            "treatments": ["High-Risk Pregnancy Care", "Pediatric Surgery", "Knee Replacement"],
            "ambulance": True, "beds": 240,
            "doctors": [{"name": "Dr. Anita Soni", "speciality": "Gynecology", "qualification": "MD, DGO", "timing": "Mon-Sat 11am-5pm", "contact": "+91-9833445566"}]
        },
        {
            "name": "Fortis Hospital, Mulund",
            "address": "Mulund Goregaon Link Road, Mulund West, Mumbai – 400078",
            "lat": 19.1654, "lon": 72.9416, "rating": 4.6,
            "specialities": ["Cardiology", "Neurology", "Transplant Surgery"],
            "emergency_no": "022-43654365", "ambulance_no": "022-43654444",
            "image_url": "https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?w=800&q=80",
            "about": "JCI accredited hospital renowned for heart transplants and complex cardiac care.",
            "rooms": {"General": 2000, "SemiPrivate": 4000, "Private": 8000, "ICU": 16000},
            "treatments": ["Heart Transplant", "Brain Tumor Surgery", "Pacemaker Implantation"],
            "ambulance": True, "beds": 315,
            "doctors": [{"name": "Dr. Anvay Mulay", "speciality": "Cardiology", "qualification": "MS, MCh", "timing": "Mon-Wed 9am-1pm", "contact": "+91-9844556677"}]
        },
        {
            "name": "Nanavati Max Super Speciality Hospital",
            "address": "SV Road, Vile Parle West, Mumbai – 400056",
            "lat": 19.0962, "lon": 72.8397, "rating": 4.7,
            "specialities": ["Gastroenterology", "Oncology", "Orthopedics", "Urology"],
            "emergency_no": "022-26267777", "ambulance_no": "022-26267788",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "A historic, iconic healthcare institution of Mumbai recently upgraded to Max network.",
            "rooms": {"General": 2300, "SemiPrivate": 4800, "Private": 8500, "ICU": 17000},
            "treatments": ["Liver Transplant", "Hip Replacement", "Prostate Surgery"],
            "ambulance": True, "beds": 350,
            "doctors": [{"name": "Dr. Sanjay Dudhat", "speciality": "Oncology", "qualification": "MS (Surgery)", "timing": "Tue-Sat 10am-3pm", "contact": "+91-9855667788"}]
        },
        {
            "name": "Jaslok Hospital & Research Centre",
            "address": "15, Dr. Deshmukh Marg, Pedder Road, Mumbai – 400026",
            "lat": 18.9717, "lon": 72.8099, "rating": 4.6,
            "specialities": ["Nephrology", "Neurology", "Endocrinology"],
            "emergency_no": "022-66573333", "ambulance_no": "022-66573344",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "One of the oldest tertiary care trust hospitals in the city with cutting-edge tech.",
            "rooms": {"General": 2100, "SemiPrivate": 4500, "Private": 8000, "ICU": 16000},
            "treatments": ["Dialysis", "Neuro Rehabilitation", "Hormonal Therapy"],
            "ambulance": True, "beds": 350,
            "doctors": [{"name": "Dr. Rupa Dalal", "speciality": "Endocrinology", "qualification": "MD, DNB", "timing": "Mon-Fri 12pm-4pm", "contact": "+91-9866778899"}]
        },
        {
            "name": "Tata Memorial Hospital",
            "address": "Dr. E Borges Road, Parel, Mumbai – 400012",
            "lat": 19.0044, "lon": 72.8426, "rating": 4.9,
            "specialities": ["Oncology", "Radiology", "Hematology"],
            "emergency_no": "022-24177000", "ambulance_no": "022-24177011",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "India's premier cancer treatment and research centre offering subsidized and free treatments.",
            "rooms": {"General": 500, "SemiPrivate": 2000, "Private": 5000, "ICU": 10000},
            "treatments": ["Chemotherapy", "Bone Marrow Transplant", "Surgical Oncology"],
            "ambulance": True, "beds": 700,
            "doctors": [{"name": "Dr. Rajendra Badwe", "speciality": "Oncology", "qualification": "MS, FACS", "timing": "Mon-Thu 9am-1pm", "contact": "+91-9877889900"}]
        },
        {
            "name": "Sir H. N. Reliance Foundation Hospital",
            "address": "Prarthana Samaj, Raja Rammohan Roy Road, Girgaon, Mumbai – 400004",
            "lat": 18.9587, "lon": 72.8193, "rating": 4.8,
            "specialities": ["Cardiology", "Orthopedics", "Robotic Surgery", "Oncology"],
            "emergency_no": "022-61305000", "ambulance_no": "1066",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "Highly advanced healthcare facility in South Mumbai with international standards.",
            "rooms": {"General": 2800, "SemiPrivate": 5500, "Private": 10000, "ICU": 20000},
            "treatments": ["Robotic Joint Replacement", "Minimally Invasive Cardiac Surgery", "Onco-Surgery"],
            "ambulance": True, "beds": 345,
            "doctors": [{"name": "Dr. Ashwin Mehta", "speciality": "Cardiology", "qualification": "MD, FACC", "timing": "Mon-Sat 10am-2pm", "contact": "+91-9888990011"}]
        }
    ],
    "Delhi": [
        {
            "name": "All India Institute of Medical Sciences (AIIMS)",
            "address": "Sri Aurobindo Marg, Ansari Nagar, New Delhi – 110029",
            "lat": 28.5672, "lon": 77.2100, "rating": 4.9,
            "specialities": ["Cardiology", "Oncology", "Neurology", "Endocrinology", "Transplant Surgery"],
            "emergency_no": "011-26588500", "ambulance_no": "011-26588444",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "India's premier government medical institute with globally recognised research and 24-hour trauma centre.",
            "rooms": {"General": 500, "SemiPrivate": 2000, "Private": 5000, "ICU": 12000},
            "treatments": ["Multiorgan Transplant", "Proton Beam Therapy", "Deep Brain Stimulation"],
            "ambulance": True, "beds": 2000,
            "doctors": [{"name": "Dr. Anand Kumar", "speciality": "Cardiothoracic Surgery", "qualification": "MS, MCh", "timing": "Mon–Wed 9am–1pm", "contact": "+91-9910000021"}]
        },
        {
            "name": "Sir Ganga Ram Hospital",
            "address": "Sarhadi Gandhi Marg, Old Rajinder Nagar, New Delhi – 110060",
            "lat": 28.6384, "lon": 77.1894, "rating": 4.8,
            "specialities": ["Gastroenterology", "Nephrology", "General Surgery"],
            "emergency_no": "011-42254000", "ambulance_no": "011-42253333",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "A multi-speciality state-of-the-art Hospital in India, providing comprehensive healthcare.",
            "rooms": {"General": 1800, "SemiPrivate": 3800, "Private": 7500, "ICU": 15000},
            "treatments": ["Laparoscopic Surgery", "Dialysis", "Liver Resection"],
            "ambulance": True, "beds": 675,
            "doctors": [{"name": "Dr. D.S. Rana", "speciality": "Nephrology", "qualification": "MD, DM", "timing": "Mon-Sat 10am-2pm", "contact": "+91-9911223344"}]
        },
        {
            "name": "Indraprastha Apollo Hospitals",
            "address": "Sarita Vihar, Delhi Mathura Road, New Delhi – 110076",
            "lat": 28.5273, "lon": 77.2842, "rating": 4.7,
            "specialities": ["Cardiology", "Neurology", "Transplant Surgery", "Orthopedics"],
            "emergency_no": "011-29871066", "ambulance_no": "1066",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "First JCI accredited hospital in India with excellent multi-organ transplant facility.",
            "rooms": {"General": 2200, "SemiPrivate": 4800, "Private": 9000, "ICU": 18000},
            "treatments": ["Liver Transplant", "Robotic Knee Replacement", "Advanced Neurosurgery"],
            "ambulance": True, "beds": 718,
            "doctors": [{"name": "Dr. Anupam Sibal", "speciality": "Pediatrics", "qualification": "MD, FRCP", "timing": "Tue-Fri 11am-4pm", "contact": "+91-9922334455"}]
        },
        {
            "name": "Max Super Speciality Hospital, Saket",
            "address": "1, 2, Press Enclave Road, Saket, New Delhi – 110017",
            "lat": 28.5283, "lon": 77.2120, "rating": 4.6,
            "specialities": ["Oncology", "Cardiology", "Urology"],
            "emergency_no": "011-26515050", "ambulance_no": "011-26515050",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "Premier hospital offering integrated comprehensive care with advanced technology.",
            "rooms": {"General": 2500, "SemiPrivate": 5500, "Private": 9500, "ICU": 19000},
            "treatments": ["Chemotherapy", "Cardiac Ablation", "Kidney Stone Removal"],
            "ambulance": True, "beds": 500,
            "doctors": [{"name": "Dr. Harit Chaturvedi", "speciality": "Oncology", "qualification": "MS, MCh", "timing": "Mon-Thu 9am-1pm", "contact": "+91-9933445566"}]
        },
        {
            "name": "BLK-Max Super Speciality Hospital",
            "address": "Pusa Road, Radha Soami Satsang, Rajinder Nagar, New Delhi – 110005",
            "lat": 28.6433, "lon": 77.1812, "rating": 4.5,
            "specialities": ["Hematology", "Bone Marrow Transplant", "Gastroenterology"],
            "emergency_no": "011-30403040", "ambulance_no": "011-30403040",
            "image_url": "https://images.unsplash.com/photo-1516841273335-e39b37888115?w=800&q=80",
            "about": "Known for one of the largest Bone Marrow Transplant units in Asia.",
            "rooms": {"General": 2000, "SemiPrivate": 4000, "Private": 8000, "ICU": 15000},
            "treatments": ["Bone Marrow Transplant", "Bariatric Surgery", "Endoscopy"],
            "ambulance": True, "beds": 650,
            "doctors": [{"name": "Dr. Dharma Choudhary", "speciality": "Hematology", "qualification": "MD, DM", "timing": "Mon-Sat 10am-3pm", "contact": "+91-9944556677"}]
        },
        {
            "name": "Fortis Escorts Heart Institute",
            "address": "Okhla Road, New Friends Colony, New Delhi – 110025",
            "lat": 28.5630, "lon": 77.2750, "rating": 4.8,
            "specialities": ["Cardiology", "Cardiothoracic Surgery", "Vascular Surgery"],
            "emergency_no": "011-47134444", "ambulance_no": "011-47135000",
            "image_url": "https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?w=800&q=80",
            "about": "Globally acclaimed for advanced cardiac care and surgeries.",
            "rooms": {"General": 2300, "SemiPrivate": 5000, "Private": 9000, "ICU": 18500},
            "treatments": ["CABG", "TAVI", "Pacemaker Implantation"],
            "ambulance": True, "beds": 310,
            "doctors": [{"name": "Dr. Ashok Seth", "speciality": "Cardiology", "qualification": "MD, FRCP", "timing": "Tue-Fri 9am-2pm", "contact": "+91-9955667788"}]
        },
        {
            "name": "Safdarjung Hospital",
            "address": "Ansari Nagar East, near AIIMS Metro Station, New Delhi – 110029",
            "lat": 28.5683, "lon": 77.2064, "rating": 4.3,
            "specialities": ["Trauma", "Burns", "General Medicine", "Orthopedics"],
            "emergency_no": "011-26165060", "ambulance_no": "011-26165060",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "One of the largest government hospitals in India, renowned for its Burns and Plastic Surgery unit.",
            "rooms": {"General": 200, "SemiPrivate": 1000, "Private": 3000, "ICU": 6000},
            "treatments": ["Skin Grafting", "Trauma Care", "Complex Fracture Fixing"],
            "ambulance": True, "beds": 1500,
            "doctors": [{"name": "Dr. R. K. Sharma", "speciality": "Orthopedics", "qualification": "MS (Ortho)", "timing": "Mon-Fri 8am-1pm", "contact": "+91-9966778899"}]
        },
        {
            "name": "Rajiv Gandhi Cancer Institute",
            "address": "Sir Chotu Ram Marg, Sector 5, Rohini, New Delhi – 110085",
            "lat": 28.7277, "lon": 77.0988, "rating": 4.7,
            "specialities": ["Oncology", "Radiotherapy", "Hematology"],
            "emergency_no": "011-47022222", "ambulance_no": "011-47022000",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "Exclusive comprehensive cancer care centre providing state-of-the-art diagnostics and treatment.",
            "rooms": {"General": 1500, "SemiPrivate": 3500, "Private": 7000, "ICU": 14000},
            "treatments": ["Immunotherapy", "Targeted Therapy", "Radiation Oncology"],
            "ambulance": True, "beds": 300,
            "doctors": [{"name": "Dr. Sudhir Rawal", "speciality": "Uro-Oncology", "qualification": "MS, MCh", "timing": "Mon-Wed 10am-4pm", "contact": "+91-9977889900"}]
        },
        {
            "name": "Dr. Ram Manohar Lohia (RML) Hospital",
            "address": "Baba Kharak Singh Marg, Connaught Place, New Delhi – 110001",
            "lat": 28.6258, "lon": 77.2001, "rating": 4.4,
            "specialities": ["Cardiology", "Neurology", "Psychiatry"],
            "emergency_no": "011-23365525", "ambulance_no": "011-23365525",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "Central government funded hospital providing multi-disciplinary care.",
            "rooms": {"General": 300, "SemiPrivate": 1200, "Private": 3500, "ICU": 6500},
            "treatments": ["Psychiatric Rehab", "Neuro Angiography", "Cardiac Stenting"],
            "ambulance": True, "beds": 1420,
            "doctors": [{"name": "Dr. Neeraj Jain", "speciality": "Cardiology", "qualification": "MD, DM", "timing": "Tue-Sat 9am-1pm", "contact": "+91-9988990011"}]
        },
        {
            "name": "Moolchand Medcity",
            "address": "Lajpat Nagar III, New Delhi – 110024",
            "lat": 28.5658, "lon": 77.2341, "rating": 4.5,
            "specialities": ["Gynecology", "Orthopedics", "Ayurveda"],
            "emergency_no": "011-42000000", "ambulance_no": "011-42000000",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "A trusted hospital legacy in Delhi providing both modern and ayurvedic healthcare.",
            "rooms": {"General": 1900, "SemiPrivate": 4000, "Private": 7500, "ICU": 14500},
            "treatments": ["High Risk Obstetrics", "Joint Replacement", "Panchakarma"],
            "ambulance": True, "beds": 300,
            "doctors": [{"name": "Dr. Sadhna Desai", "speciality": "Gynecology", "qualification": "MD", "timing": "Mon-Fri 10am-2pm", "contact": "+91-9999001122"}]
        }
    ],
    "Bengaluru": [
        {
            "name": "Manipal Hospital (Old Airport Road)",
            "address": "98, HAL Airport Road, Bengaluru – 560017",
            "lat": 12.9576, "lon": 77.6428, "rating": 4.7,
            "specialities": ["Cardiology", "Orthopedics", "Nephrology", "Oncology", "Spine Surgery"],
            "emergency_no": "080-25024444", "ambulance_no": "080-25024400",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "600-bed multi-specialty hospital with Level 1 Trauma Centre and cutting-edge tech.",
            "rooms": {"General": 1800, "SemiPrivate": 4000, "Private": 7500, "ICU": 16000},
            "treatments": ["Total Joint Replacement", "Renal Transplant", "Coronary Bypass"],
            "ambulance": True, "beds": 600,
            "doctors": [{"name": "Dr. Rajeev Sood", "speciality": "Orthopedic Surgery", "qualification": "MS (Ortho)", "timing": "Mon–Fri 9am–1pm", "contact": "+91-9845000031"}]
        },
        {
            "name": "Fortis Hospital, Bannerghatta Road",
            "address": "154/9, Bannerghatta Road, Opposite IIM-B, Bengaluru – 560076",
            "lat": 12.8953, "lon": 77.5991, "rating": 4.6,
            "specialities": ["Cardiology", "Neurology", "Urology"],
            "emergency_no": "080-66214444", "ambulance_no": "080-66214000",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "Top-tier facility widely known for excellence in cardiac sciences and brain surgery.",
            "rooms": {"General": 2000, "SemiPrivate": 4200, "Private": 8000, "ICU": 16500},
            "treatments": ["Minimally Invasive Cardiac Surgery", "Craniotomy", "Prostate Laser Surgery"],
            "ambulance": True, "beds": 276,
            "doctors": [{"name": "Dr. Vivek Jawali", "speciality": "Cardiology", "qualification": "MS, MCh", "timing": "Mon-Wed 10am-2pm", "contact": "+91-9845112233"}]
        },
        {
            "name": "Apollo Hospitals, Jayanagar",
            "address": "212, 14th Cross Rd, Jayanagar 3rd Block, Bengaluru – 560011",
            "lat": 12.9304, "lon": 77.5838, "rating": 4.5,
            "specialities": ["General Medicine", "Gastroenterology", "Pulmonology"],
            "emergency_no": "080-26304050", "ambulance_no": "1066",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "Premium neighborhood hospital offering holistic multi-specialty healthcare.",
            "rooms": {"General": 1900, "SemiPrivate": 3900, "Private": 7200, "ICU": 15000},
            "treatments": ["Bronchoscopy", "Endoscopy", "Dialysis"],
            "ambulance": True, "beds": 150,
            "doctors": [{"name": "Dr. Ravindra N", "speciality": "Gastroenterology", "qualification": "MD, DM", "timing": "Tue-Sat 11am-4pm", "contact": "+91-9845223344"}]
        },
        {
            "name": "Aster CMI Hospital",
            "address": "43/2, New Airport Road, NH 44, Hebbal, Bengaluru – 560092",
            "lat": 13.0402, "lon": 77.5935, "rating": 4.8,
            "specialities": ["Pediatrics", "Oncology", "Neurology", "Transplant"],
            "emergency_no": "080-43420100", "ambulance_no": "080-43420100",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "One of the most advanced healthcare hubs in North Bengaluru with robotic tech.",
            "rooms": {"General": 2500, "SemiPrivate": 5500, "Private": 9500, "ICU": 19000},
            "treatments": ["Pediatric Liver Transplant", "Robotic Uro-Surgery", "Brain Tumor Excisions"],
            "ambulance": True, "beds": 500,
            "doctors": [{"name": "Dr. Sonal Asthana", "speciality": "Transplant Surgery", "qualification": "MS, MRCS", "timing": "Mon-Fri 9am-3pm", "contact": "+91-9845334455"}]
        },
        {
            "name": "Narayana Health City",
            "address": "258/A, Bommasandra Industrial Area, Hosur Road, Bengaluru – 560099",
            "lat": 12.8159, "lon": 77.6946, "rating": 4.7,
            "specialities": ["Cardiology", "Oncology", "Nephrology", "Ophthalmology"],
            "emergency_no": "080-71222222", "ambulance_no": "080-71222222",
            "image_url": "https://images.unsplash.com/photo-1516841273335-e39b37888115?w=800&q=80",
            "about": "Massive healthcare campus known for highly affordable cardiac surgeries globally.",
            "rooms": {"General": 1200, "SemiPrivate": 3000, "Private": 6000, "ICU": 13000},
            "treatments": ["Pediatric Heart Surgery", "Bone Marrow Transplant", "Cataract Surgery"],
            "ambulance": True, "beds": 1000,
            "doctors": [{"name": "Dr. Devi Shetty", "speciality": "Cardiac Surgery", "qualification": "MS, FRCS", "timing": "Mon-Wed 10am-1pm", "contact": "+91-9845445566"}]
        },
        {
            "name": "St. John's Medical College Hospital",
            "address": "Sarjapur Road, John Nagar, Koramangala, Bengaluru – 560034",
            "lat": 12.9298, "lon": 77.6186, "rating": 4.5,
            "specialities": ["General Medicine", "Dermatology", "Orthopedics"],
            "emergency_no": "080-22065000", "ambulance_no": "080-22065000",
            "image_url": "https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?w=800&q=80",
            "about": "Reputed non-profit institution offering excellent multidisciplinary medical care.",
            "rooms": {"General": 600, "SemiPrivate": 1800, "Private": 4000, "ICU": 9000},
            "treatments": ["Joint Reconstruction", "Skin Grafting", "Infectious Disease Care"],
            "ambulance": True, "beds": 1350,
            "doctors": [{"name": "Dr. Sanjiv Ramachandran", "speciality": "General Medicine", "qualification": "MD", "timing": "Mon-Sat 8am-1pm", "contact": "+91-9845556677"}]
        },
        {
            "name": "Sakra World Hospital",
            "address": "Devarabeesanahalli, Varthur Hobli, Bellandur, Bengaluru – 560103",
            "lat": 12.9348, "lon": 77.6833, "rating": 4.6,
            "specialities": ["Orthopedics", "Neurology", "Gastroenterology"],
            "emergency_no": "080-49694969", "ambulance_no": "080-49694969",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "Indo-Japanese collaborative hospital ensuring advanced precision treatments.",
            "rooms": {"General": 2400, "SemiPrivate": 5000, "Private": 9000, "ICU": 18000},
            "treatments": ["Spine Fusion", "Stroke Management", "GI Oncology"],
            "ambulance": True, "beds": 350,
            "doctors": [{"name": "Dr. Maheshwara Reddy", "speciality": "Orthopedics", "qualification": "MS (Ortho)", "timing": "Mon-Fri 10am-4pm", "contact": "+91-9845667788"}]
        },
        {
            "name": "Sparsh Hospital",
            "address": "Tumkur Road, Yeshwanthpur, Bengaluru – 560022",
            "lat": 13.0245, "lon": 77.5401, "rating": 4.5,
            "specialities": ["Orthopedics", "Plastic Surgery", "Pediatrics"],
            "emergency_no": "080-61222000", "ambulance_no": "080-61222000",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "Pioneers in complex trauma, orthopedic reconstruction, and plastic surgeries.",
            "rooms": {"General": 1800, "SemiPrivate": 3500, "Private": 7000, "ICU": 15000},
            "treatments": ["Complex Limb Reconstruction", "Cleft Lip Surgery", "Pediatric Care"],
            "ambulance": True, "beds": 250,
            "doctors": [{"name": "Dr. Sharan Patil", "speciality": "Orthopedics", "qualification": "MS (Ortho)", "timing": "Wed-Sat 9am-2pm", "contact": "+91-9845778899"}]
        },
        {
            "name": "Fortis Hospital, Cunningham Road",
            "address": "14, Cunningham Road, Vasanth Nagar, Bengaluru – 560052",
            "lat": 12.9868, "lon": 77.5936, "rating": 4.6,
            "specialities": ["Cardiology", "Urology", "Internal Medicine"],
            "emergency_no": "080-41994444", "ambulance_no": "080-41994444",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "Boutique tertiary care hospital situated in the heart of the city.",
            "rooms": {"General": 2200, "SemiPrivate": 4800, "Private": 8500, "ICU": 16000},
            "treatments": ["Angioplasty", "Laser Stone Removal", "Comprehensive Health Check"],
            "ambulance": True, "beds": 150,
            "doctors": [{"name": "Dr. Rajpal Singh", "speciality": "Cardiology", "qualification": "MD, DM", "timing": "Mon-Fri 10am-2pm", "contact": "+91-9845889900"}]
        },
        {
            "name": "BGS Gleneagles Global Hospital",
            "address": "67, Uttarahalli Road, Kengeri, Bengaluru – 560060",
            "lat": 12.9054, "lon": 77.4981, "rating": 4.7,
            "specialities": ["Hepatology", "Oncology", "Nephrology", "Transplant"],
            "emergency_no": "080-26255555", "ambulance_no": "080-26255555",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "Renowned for multi-organ transplant procedures and comprehensive gastro care.",
            "rooms": {"General": 2000, "SemiPrivate": 4500, "Private": 8000, "ICU": 16500},
            "treatments": ["Liver Transplant", "Pancreas Transplant", "Medical Oncology"],
            "ambulance": True, "beds": 500,
            "doctors": [{"name": "Dr. Rajiv Lochan", "speciality": "Transplant Surgery", "qualification": "MS, FRCS", "timing": "Tue-Sat 9am-4pm", "contact": "+91-9845990011"}]
        }
    ],
    "Nagpur": [
        {
            "name": "Kingsway Hospital",
            "address": "68, Kingsway Road, Nagpur – 440001",
            "lat": 21.1458, "lon": 79.0882, "rating": 4.5,
            "specialities": ["General Medicine", "Orthopedics", "Cardiology", "Pediatrics", "Gynecology"],
            "emergency_no": "0712-2524444", "ambulance_no": "0712-2524400",
            "image_url": "https://images.unsplash.com/photo-1516841273335-e39b37888115?w=800&q=80",
            "about": "Leading multi-specialty hospital in central India with 450+ beds and a dedicated trauma care unit.",
            "rooms": {"General": 1200, "SemiPrivate": 2800, "Private": 5500, "ICU": 12000},
            "treatments": ["Cardiac Angioplasty", "Joint Replacement", "Laparoscopic Procedures"],
            "ambulance": True, "beds": 450,
            "doctors": [{"name": "Dr. Abhijit Deshmukh", "speciality": "Cardiology", "qualification": "MD, DM", "timing": "Mon–Sat 10am–1pm", "contact": "+91-9890000041"}]
        },
        {
            "name": "Orange City Hospital & Research Institute",
            "address": "Wadi, Nagpur – 440023",
            "lat": 21.0867, "lon": 79.0495, "rating": 4.6,
            "specialities": ["Oncology", "Neurology", "Urology", "Nephrology", "Dermatology"],
            "emergency_no": "0712-6630000", "ambulance_no": "0712-6630099",
            "image_url": "https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?w=800&q=80",
            "about": "NABH-accredited 500-bed hospital with advanced cancer care and 24×7 emergency.",
            "rooms": {"General": 1500, "SemiPrivate": 3500, "Private": 6500, "ICU": 14000},
            "treatments": ["Robotic Prostatectomy", "Chemotherapy", "Neuro Endovascular"],
            "ambulance": True, "beds": 500,
            "doctors": [{"name": "Dr. Sudhir Paunikar", "speciality": "Oncology", "qualification": "MD, DM", "timing": "Mon–Fri 10am–2pm", "contact": "+91-9860000051"}]
        },
        {
            "name": "Wockhardt Super Speciality Hospital",
            "address": "1644, North Ambazari Road, Shankar Nagar, Nagpur – 440033",
            "lat": 21.1344, "lon": 79.0592, "rating": 4.7,
            "specialities": ["Cardiology", "Neurology", "Nephrology"],
            "emergency_no": "0712-6624444", "ambulance_no": "0712-6624444",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "Pioneer in central India for world-class neuro, cardiac, and renal treatments.",
            "rooms": {"General": 1800, "SemiPrivate": 3500, "Private": 6500, "ICU": 14500},
            "treatments": ["Coronary Bypass", "Stroke Rehabilitation", "Renal Dialysis"],
            "ambulance": True, "beds": 200,
            "doctors": [{"name": "Dr. Nitin Tiwari", "speciality": "Cardiology", "qualification": "MD, DM", "timing": "Mon-Sat 10am-4pm", "contact": "+91-9890112233"}]
        },
        {
            "name": "Care Hospital",
            "address": "3, Farmland, Panchsheel Square, Ramdaspeth, Nagpur – 440010",
            "lat": 21.1378, "lon": 79.0734, "rating": 4.4,
            "specialities": ["General Medicine", "Gastroenterology", "Pulmonology"],
            "emergency_no": "0712-3982222", "ambulance_no": "0712-3982222",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "A trusted healthcare institution providing high-quality comprehensive medical care.",
            "rooms": {"General": 1300, "SemiPrivate": 2900, "Private": 5500, "ICU": 12500},
            "treatments": ["Endoscopy", "Asthma Clinic", "Hernia Repair"],
            "ambulance": True, "beds": 105,
            "doctors": [{"name": "Dr. Prakash Khetan", "speciality": "Gastroenterology", "qualification": "MD, DM", "timing": "Tue-Fri 11am-5pm", "contact": "+91-9890223344"}]
        },
        {
            "name": "Alexis Multispeciality Hospital",
            "address": "Survey No 232, Mankapur, Koradi Road, Nagpur – 440030",
            "lat": 21.1963, "lon": 79.0768, "rating": 4.8,
            "specialities": ["Oncology", "Orthopedics", "Cardiology"],
            "emergency_no": "0712-7120000", "ambulance_no": "0712-7120000",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "Ultra-modern hospital delivering comprehensive care with Zulekha Healthcare Group.",
            "rooms": {"General": 1600, "SemiPrivate": 3200, "Private": 6000, "ICU": 13500},
            "treatments": ["Radiation Oncology", "Joint Replacement", "Cath Lab Services"],
            "ambulance": True, "beds": 200,
            "doctors": [{"name": "Dr. Amol Dongre", "speciality": "Medical Oncology", "qualification": "MD, DM", "timing": "Mon-Sat 9am-2pm", "contact": "+91-9890334455"}]
        },
        {
            "name": "Aureus Hospital",
            "address": "Wathoda Layout, Near Symbiosis International University, Nagpur – 440008",
            "lat": 21.1341, "lon": 79.1360, "rating": 4.5,
            "specialities": ["Nephrology", "Urology", "General Surgery"],
            "emergency_no": "0712-6603030", "ambulance_no": "0712-6603030",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "Fast-emerging medical facility focused on minimally invasive and renal sciences.",
            "rooms": {"General": 1200, "SemiPrivate": 2500, "Private": 5000, "ICU": 11000},
            "treatments": ["Kidney Transplant Prep", "Laser Prostatectomy", "Appendectomy"],
            "ambulance": True, "beds": 120,
            "doctors": [{"name": "Dr. Vikas Jain", "speciality": "Urology", "qualification": "MS, MCh", "timing": "Mon-Fri 10am-4pm", "contact": "+91-9890445566"}]
        },
        {
            "name": "National Cancer Institute (NCI)",
            "address": "Khasra No. 25, Outer Ring Road, Jamtha, Nagpur – 441108",
            "lat": 21.0313, "lon": 79.0346, "rating": 4.9,
            "specialities": ["Oncology", "Radiology", "Palliative Care"],
            "emergency_no": "0712-2800400", "ambulance_no": "0712-2800400",
            "image_url": "https://images.unsplash.com/photo-1516841273335-e39b37888115?w=800&q=80",
            "about": "World-class, large scale comprehensive cancer care and research institute.",
            "rooms": {"General": 1000, "SemiPrivate": 2500, "Private": 5000, "ICU": 12000},
            "treatments": ["TrueBeam Radiotherapy", "Surgical Oncology", "Chemotherapy"],
            "ambulance": True, "beds": 470,
            "doctors": [{"name": "Dr. Anand Pathak", "speciality": "Oncology", "qualification": "MD", "timing": "Mon-Sat 9am-5pm", "contact": "+91-9890556677"}]
        },
        {
            "name": "KIMS-Viveka Hospitals",
            "address": "Subhash Nagar, South Ambazari Road, Nagpur – 440022",
            "lat": 21.1278, "lon": 79.0435, "rating": 4.6,
            "specialities": ["Gastroenterology", "Neurology", "Orthopedics"],
            "emergency_no": "0712-6789000", "ambulance_no": "0712-6789000",
            "image_url": "https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?w=800&q=80",
            "about": "Part of the KIMS group, offering specialized quaternary care in central India.",
            "rooms": {"General": 1500, "SemiPrivate": 3000, "Private": 6000, "ICU": 13000},
            "treatments": ["Spine Surgery", "Liver Clinic", "Neuro Critical Care"],
            "ambulance": True, "beds": 250,
            "doctors": [{"name": "Dr. Sameer Paltewar", "speciality": "Neuro Surgery", "qualification": "MS, MCh", "timing": "Tue-Sat 10am-2pm", "contact": "+91-9890667788"}]
        },
        {
            "name": "SevenStar Hospital",
            "address": "Jagnade Square, Nandanvan, Nagpur – 440009",
            "lat": 21.1275, "lon": 79.1170, "rating": 4.4,
            "specialities": ["Cardiology", "Trauma", "General Medicine"],
            "emergency_no": "0712-6699999", "ambulance_no": "0712-6699999",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "Modern multi-specialty facility catering to East Nagpur and surrounding areas.",
            "rooms": {"General": 1100, "SemiPrivate": 2600, "Private": 5000, "ICU": 11500},
            "treatments": ["Angiography", "Accident Care", "Fever & Infection Clinic"],
            "ambulance": True, "beds": 150,
            "doctors": [{"name": "Dr. Prashant Rahate", "speciality": "General Surgery", "qualification": "MS", "timing": "Mon-Fri 11am-3pm", "contact": "+91-9890778899"}]
        },
        {
            "name": "Meditrina Institute of Medical Sciences",
            "address": "278, Central Bazar Road, Ramdaspeth, Nagpur – 440010",
            "lat": 21.1350, "lon": 79.0700, "rating": 4.5,
            "specialities": ["Cardiology", "Nephrology", "Ophthalmology"],
            "emergency_no": "0712-6669666", "ambulance_no": "0712-6669666",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "Well-equipped healthcare centre focusing on cardiac and critical care.",
            "rooms": {"General": 1400, "SemiPrivate": 2800, "Private": 5500, "ICU": 12500},
            "treatments": ["Echocardiography", "Hemodialysis", "Phacoemulsification"],
            "ambulance": True, "beds": 110,
            "doctors": [{"name": "Dr. Sameer Dani", "speciality": "Cardiology", "qualification": "MD, DM", "timing": "Mon-Sat 10am-4pm", "contact": "+91-9890889900"}]
        }
    ],
    "Chennai": [
        {
            "name": "Apollo Hospitals (Greams Road)",
            "address": "21, Greams Lane, Off Greams Road, Chennai – 600006",
            "lat": 13.0569, "lon": 80.2409, "rating": 4.8,
            "specialities": ["Cardiology", "Oncology", "Transplant", "Neurology", "Orthopedics"],
            "emergency_no": "044-28290200", "ambulance_no": "1066",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "Asia's first JCI-accredited hospital. Pioneer in cardiac and organ transplant surgeries.",
            "rooms": {"General": 2200, "SemiPrivate": 4800, "Private": 9500, "ICU": 20000},
            "treatments": ["Heart Transplant", "Stem Cell Therapy", "IMRT Cancer Treatment"],
            "ambulance": True, "beds": 700,
            "doctors": [{"name": "Dr. K. Harishkumar", "speciality": "Cardiac Surgery", "qualification": "MS, MCh", "timing": "Mon–Fri 9am–1pm", "contact": "+91-9444000061"}]
        },
        {
            "name": "MIOT International",
            "address": "4/112, Mount Poonamallee Road, Manapakkam, Chennai – 600089",
            "lat": 13.0163, "lon": 80.1802, "rating": 4.6,
            "specialities": ["Orthopedics", "Cardiology", "Gastroenterology", "Nephrology"],
            "emergency_no": "044-42002288", "ambulance_no": "044-42002288",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "Renowned globally for joint replacements, orthopedics, and multi-specialty care.",
            "rooms": {"General": 2000, "SemiPrivate": 4000, "Private": 8000, "ICU": 16000},
            "treatments": ["Hip Replacement", "Liver Care", "Kidney Transplant"],
            "ambulance": True, "beds": 1000,
            "doctors": [{"name": "Dr. P. V. A. Mohandas", "speciality": "Orthopedics", "qualification": "MS (Ortho)", "timing": "Mon-Sat 10am-1pm", "contact": "+91-9444112233"}]
        },
        {
            "name": "Fortis Malar Hospital",
            "address": "52, 1st Main Road, Gandhi Nagar, Adyar, Chennai – 600020",
            "lat": 13.0116, "lon": 80.2565, "rating": 4.5,
            "specialities": ["Cardiology", "Neurology", "Pediatrics"],
            "emergency_no": "044-42892222", "ambulance_no": "044-42892222",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "Pioneers in advanced medical care including heart failure and transplant programs.",
            "rooms": {"General": 1800, "SemiPrivate": 3800, "Private": 7500, "ICU": 15000},
            "treatments": ["ECMO", "Heart Transplant", "Pediatric ICU"],
            "ambulance": True, "beds": 180,
            "doctors": [{"name": "Dr. K. R. Balakrishnan", "speciality": "Cardiothoracic Surgery", "qualification": "MS, MCh", "timing": "Mon-Fri 9am-4pm", "contact": "+91-9444223344"}]
        },
        {
            "name": "Gleneagles Global Health City",
            "address": "439, Cheran Nagar, Perumbakkam, Chennai – 600100",
            "lat": 12.9023, "lon": 80.1983, "rating": 4.7,
            "specialities": ["Hepatology", "Oncology", "Urology", "Transplant"],
            "emergency_no": "044-44777000", "ambulance_no": "044-44777000",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "Asia's most trusted multi-organ transplant center and tertiary care hospital.",
            "rooms": {"General": 2200, "SemiPrivate": 4500, "Private": 8500, "ICU": 18000},
            "treatments": ["Liver Transplant", "Robotic Uro-Surgery", "Radiation Oncology"],
            "ambulance": True, "beds": 1000,
            "doctors": [{"name": "Dr. Joy Varghese", "speciality": "Hepatology", "qualification": "MD, DM", "timing": "Tue-Sat 10am-3pm", "contact": "+91-9444334455"}]
        },
        {
            "name": "Kauvery Hospital",
            "address": "81, TTK Road, Alwarpet, Chennai – 600018",
            "lat": 13.0305, "lon": 80.2520, "rating": 4.6,
            "specialities": ["Geriatrics", "Orthopedics", "Cardiology"],
            "emergency_no": "044-40006000", "ambulance_no": "044-40006000",
            "image_url": "https://images.unsplash.com/photo-1516841273335-e39b37888115?w=800&q=80",
            "about": "Multi-specialty hospital well-known for exceptional geriatric and cardiac care.",
            "rooms": {"General": 1900, "SemiPrivate": 4200, "Private": 7800, "ICU": 15500},
            "treatments": ["Geriatric Care", "Knee Replacement", "Coronary Stenting"],
            "ambulance": True, "beds": 250,
            "doctors": [{"name": "Dr. V. N. Muralidharan", "speciality": "Orthopedics", "qualification": "MS (Ortho)", "timing": "Mon-Fri 11am-2pm", "contact": "+91-9444445566"}]
        },
        {
            "name": "Sri Ramachandra Medical Centre (SRMC)",
            "address": "1, Ramachandra Nagar, Porur, Chennai – 600116",
            "lat": 13.0392, "lon": 80.1485, "rating": 4.7,
            "specialities": ["Sports Medicine", "Cardiology", "Neurology", "Pediatrics"],
            "emergency_no": "044-45928500", "ambulance_no": "044-45928500",
            "image_url": "https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?w=800&q=80",
            "about": "Massive academic medical centre offering quaternary care and excellent sports medicine.",
            "rooms": {"General": 1500, "SemiPrivate": 3500, "Private": 7000, "ICU": 14000},
            "treatments": ["Arthroscopy", "Pediatric Cardiology", "Stroke Management"],
            "ambulance": True, "beds": 1800,
            "doctors": [{"name": "Dr. S. Arumugam", "speciality": "Sports Medicine", "qualification": "MD", "timing": "Mon-Sat 9am-1pm", "contact": "+91-9444556677"}]
        },
        {
            "name": "Vijaya Hospital",
            "address": "323, NSK Salai, Vadapalani, Chennai – 600026",
            "lat": 13.0515, "lon": 80.2110, "rating": 4.4,
            "specialities": ["Maternity", "General Surgery", "Orthopedics"],
            "emergency_no": "044-23651234", "ambulance_no": "044-23651234",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "One of Chennai's oldest and most trusted trust hospitals with affordable care.",
            "rooms": {"General": 1200, "SemiPrivate": 2500, "Private": 5500, "ICU": 11000},
            "treatments": ["Normal/C-Section Delivery", "Appendectomy", "Fracture Care"],
            "ambulance": True, "beds": 750,
            "doctors": [{"name": "Dr. Saraswathi", "speciality": "Gynecology", "qualification": "MD, DGO", "timing": "Mon-Sat 10am-2pm", "contact": "+91-9444667788"}]
        },
        {
            "name": "SIMS Hospital",
            "address": "1, Jawaharlal Nehru Salai, Vadapalani, Chennai – 600026",
            "lat": 13.0530, "lon": 80.2093, "rating": 4.6,
            "specialities": ["Gastroenterology", "Cardiology", "Trauma Care"],
            "emergency_no": "044-20002001", "ambulance_no": "044-20002001",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "State-of-the-art multi-super specialty hospital with a dedicated advanced trauma center.",
            "rooms": {"General": 2000, "SemiPrivate": 4200, "Private": 8000, "ICU": 16000},
            "treatments": ["Bariatric Surgery", "Cardiac Bypass", "Polytrauma Care"],
            "ambulance": True, "beds": 345,
            "doctors": [{"name": "Dr. V. V. Bashi", "speciality": "Cardiothoracic Surgery", "qualification": "MS, MCh", "timing": "Tue-Fri 9am-4pm", "contact": "+91-9444778899"}]
        },
        {
            "name": "Chettinad Health City",
            "address": "Rajiv Gandhi Salai, Kelambakkam, Chennai – 603103",
            "lat": 12.7886, "lon": 80.2190, "rating": 4.5,
            "specialities": ["General Medicine", "Pulmonology", "Dermatology"],
            "emergency_no": "044-47411000", "ambulance_no": "044-47411000",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "A massive health city offering quality education and widespread multispecialty patient care.",
            "rooms": {"General": 1000, "SemiPrivate": 2500, "Private": 5000, "ICU": 12000},
            "treatments": ["Respiratory Therapy", "Skin Grafting", "Infectious Diseases"],
            "ambulance": True, "beds": 1150,
            "doctors": [{"name": "Dr. R. Rajasekar", "speciality": "General Medicine", "qualification": "MD", "timing": "Mon-Sat 8am-1pm", "contact": "+91-9444889900"}]
        },
        {
            "name": "Billroth Hospitals",
            "address": "43, Lakshmi Talkies Road, Shenoy Nagar, Chennai – 600030",
            "lat": 13.0768, "lon": 80.2263, "rating": 4.4,
            "specialities": ["Oncology", "Gastroenterology", "Gynecology"],
            "emergency_no": "044-26641777", "ambulance_no": "044-26641777",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "Pioneers in advanced gastroenterology and oncology setups since 1990.",
            "rooms": {"General": 1600, "SemiPrivate": 3200, "Private": 6500, "ICU": 13500},
            "treatments": ["Chemotherapy", "GI Endoscopy", "Minimally Invasive Gynecology"],
            "ambulance": True, "beds": 600,
            "doctors": [{"name": "Dr. V. Jeganathan", "speciality": "Gastroenterology", "qualification": "MD, DM", "timing": "Mon-Fri 10am-2pm", "contact": "+91-9444990011"}]
        }
    ]
}

# --- SIDEBAR ---
st.sidebar.markdown("<h2 style='text-align: center; color: #3b82f6;'>🏥 MediFind</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", ["Hospital Search", "Analytics", "Hospital Map", "Emergency", "Appointments", "About"])

st.sidebar.markdown("---")
st.sidebar.markdown("**Search & Filters**")

cities = sorted(list(HOSPITALS.keys()))
selected_city = st.sidebar.selectbox("Select City", cities, index=cities.index("Nagpur") if "Nagpur" in cities else 0)

all_specs = set()
for h in HOSPITALS.get(selected_city, []):
    for s in h["specialities"]:
        all_specs.add(s)
all_specs = ["All"] + sorted(list(all_specs))

selected_spec = st.sidebar.selectbox("Speciality", all_specs)
min_rating = st.sidebar.slider("Minimum Rating ⭐", 1.0, 5.0, 4.0, 0.1)

# Filter Hospitals
filtered_hospitals = [
    h for h in HOSPITALS.get(selected_city, [])
    if h["rating"] >= min_rating and (selected_spec == "All" or selected_spec in h["specialities"])
]

total_docs = sum(len(h["doctors"]) for h in filtered_hospitals)
avg_rtg = sum(h["rating"] for h in filtered_hospitals) / len(filtered_hospitals) if filtered_hospitals else 0
amb_ready = sum(1 for h in filtered_hospitals if h.get("ambulance", False))

st.sidebar.markdown("---")
st.sidebar.error("🆘 **Emergency Contacts**\n\n📞 **112** – Universal\n\n📞 **108** – Ambulance\n\n📞 **102** – Maternal")

# --- PAGES ---

if page == "Hospital Search":
    st.markdown("<h1 class='main-header'>🏥 MediFind</h1>", unsafe_allow_html=True)
    st.markdown("*Discover top-rated multispecialty hospitals near you • Instant doctor connect • 24×7 ambulance*")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Hospitals Found 🏥", len(filtered_hospitals))
    col2.metric("Doctors Available 👨‍⚕️", total_docs)
    col3.metric("Avg Rating ⭐", f"{avg_rtg:.1f}")
    col4.metric("Ambulance Ready 🚑", amb_ready)

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered_hospitals:
        st.warning("⚠️ No hospitals match your filters. Try adjusting your criteria.")
    else:
        for idx, h in enumerate(filtered_hospitals):
            st.markdown("<div class='hospital-card'>", unsafe_allow_html=True)
            col_img, col_info = st.columns([1, 2])

            with col_img:
                # FIX 1: use_column_width deprecated → use_container_width
                st.image(h['image_url'], use_container_width=True)

            with col_info:
                st.markdown(f"<h2>🏥 {h['name']}</h2>", unsafe_allow_html=True)
                st.markdown(f"📍 {h['address']}")
                st.markdown(f"**Rating:** ⭐ <span style='color: #d97706; font-weight: bold;'>{h['rating']}/5</span>", unsafe_allow_html=True)

                specs_html = " ".join([
                    f"<span style='background:#dbeafe; color:#1e40af; padding:4px 10px; border-radius:20px; "
                    f"font-size:14px; font-weight:600; margin-right:5px;'>{s}</span>"
                    for s in h["specialities"]
                ])
                st.markdown(f"<div style='margin-top:10px; margin-bottom:15px;'>{specs_html}</div>", unsafe_allow_html=True)

                # FIX 2: unique key for each st.tabs call to avoid widget ID collisions
                tabs = st.tabs([f"Overview##{idx}", f"Doctors##{idx}", f"Rooms##{idx}", f"Treatments##{idx}", f"Contact##{idx}"])

                with tabs[0]:
                    st.write(f"**About:** {h['about']}")
                    st.write(f"**🛏️ Total Beds:** {h['beds']}")

                with tabs[1]:
                    for doc in h["doctors"]:
                        st.info(
                            f"**👨‍⚕️ {doc['name']}** \n"
                            f"🩺 {doc['speciality']} | 🎓 {doc['qualification']}  \n"
                            f"🕐 {doc['timing']} | 📞 {doc['contact']}"
                        )

                with tabs[2]:
                    df_rooms = pd.DataFrame(list(h["rooms"].items()), columns=["Room Type", "Charges (₹/day)"])
                    st.dataframe(df_rooms, hide_index=True, use_container_width=True)

                with tabs[3]:
                    st.success("**Available Treatments:** \n" + "  \n".join([f"✔️ {t}" for t in h["treatments"]]))

                with tabs[4]:
                    e_col1, e_col2 = st.columns(2)
                    e_col1.warning(f"📞 **Emergency Helpline**\n### {h['emergency_no']}")
                    e_col2.error(f"🚑 **Ambulance Service**\n### {h['ambulance_no']}")

            st.markdown("</div>", unsafe_allow_html=True)

elif page == "Analytics":
    st.markdown("<h1 class='main-header'>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"*Visual insights into hospital data across {selected_city}*")

    if not filtered_hospitals:
        st.warning("No data to show based on current filters.")
    else:
        df = pd.DataFrame(filtered_hospitals)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Hospitals 🏥", len(filtered_hospitals))
        c2.metric("Total Beds 🛏️", sum(h["beds"] for h in filtered_hospitals))
        c3.metric("Avg Rating ⭐", f"{avg_rtg:.1f}")
        c4.metric("Total Doctors 👨‍⚕️", total_docs)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ⭐ Hospital Ratings")
            fig1 = px.bar(df, x="name", y="rating", color_discrete_sequence=["#3b82f6"], range_y=[0, 5])
            fig1.update_layout(xaxis_title="", yaxis_title="Rating")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("### 🛏️ Bed Distribution")
            fig2 = px.pie(df, names="name", values="beds", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("### 💰 Room Charges (ICU)")
            icu_data = [{"name": h["name"], "icu": h["rooms"]["ICU"]} for h in filtered_hospitals]
            fig3 = px.line(pd.DataFrame(icu_data), x="name", y="icu", markers=True, color_discrete_sequence=["#f59e0b"])
            fig3.update_traces(line=dict(width=3))
            fig3.update_layout(xaxis_title="", yaxis_title="Charge (₹)")
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.markdown("### 👨‍⚕️ Doctors vs Beds (Scaled)")
            radar_data = []
            for h in filtered_hospitals:
                radar_data.append({"hospital": h["name"][:15], "metric": "Doctors", "value": len(h["doctors"])})
                radar_data.append({"hospital": h["name"][:15], "metric": "Beds/100", "value": h["beds"] / 100})
            fig4 = px.line_polar(pd.DataFrame(radar_data), r="value", theta="hospital", color="metric", line_close=True)
            fig4.update_traces(fill='toself')
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("### 📋 Hospital Data Table")
        table_data = []
        for h in filtered_hospitals:
            table_data.append({
                "Hospital": h["name"],
                "Rating": h["rating"],
                "Beds": h["beds"],
                "Doctors": len(h["doctors"]),
                "General Ward (₹)": h["rooms"]["General"],
                "ICU (₹)": h["rooms"]["ICU"]
            })
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

elif page == "Hospital Map":
    st.markdown(f"<h1 class='main-header'>🗺️ Hospital Map</h1>", unsafe_allow_html=True)
    st.markdown(f"*Interactive map showing hospital locations in {selected_city}*")

    if not filtered_hospitals:
        st.warning("No hospitals to map.")
    else:
        avg_lat = sum(h["lat"] for h in filtered_hospitals) / len(filtered_hospitals)
        avg_lon = sum(h["lon"] for h in filtered_hospitals) / len(filtered_hospitals)

        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

        for h in filtered_hospitals:
            popup_html = f"""
            <div style='width:200px'>
                <b>{h['name']}</b><br>
                ⭐ Rating: {h['rating']}/5<br>
                🛏️ Beds: {h['beds']}<br>
                📞 {h['emergency_no']}
            </div>
            """
            folium.Marker(
                [h["lat"], h["lon"]],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=h["name"],
                icon=folium.Icon(color="blue", icon="plus")
            ).add_to(m)

            folium.Circle(
                [h["lat"], h["lon"]],
                radius=500,
                color="blue",
                fill=True,
                fill_opacity=0.2
            ).add_to(m)

        # FIX 3: removed fixed width=1200 to prevent overflow; use_container_width handles it
        st_folium(m, use_container_width=True, height=600)

        st.markdown("### 📍 Locations")
        cols = st.columns(2)
        for i, h in enumerate(filtered_hospitals):
            with cols[i % 2]:
                # FIX 4: corrected Google Maps URL – was using JS ${} syntax instead of Python f-string {}
                maps_url = f"https://www.google.com/maps?q={h['lat']},{h['lon']}"
                st.markdown(f"""
                <div class='stat-card' style='margin-bottom: 10px;'>
                    <h4>{h['name']}</h4>
                    <p>📍 {h['address']}<br>
                    ⭐ {h['rating']}/5 | 🛏️ {h['beds']} beds<br>
                    <b>Coordinates:</b> {h['lat']:.4f}, {h['lon']:.4f}</p>
                    <a href='{maps_url}' target='_blank'>🗺️ Open in Google Maps</a>
                </div>
                """, unsafe_allow_html=True)

elif page == "Emergency":
    st.markdown("<h1 class='main-header'>🚨 Emergency Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("*One-click direct connect to doctors & ambulance • 24×7 Active*")

    st.error("⚠️ **For life-threatening emergencies, call 112 immediately!**")

    col1, col2, col3 = st.columns(3)
    col1.error("🚑 **National Ambulance**\n# 108")
    col2.warning("🚒 **Police / Fire / Rescue**\n# 112")
    col3.success("🤱 **Maternal Ambulance**\n# 102")

    st.markdown("---")
    st.markdown(f"### 🏥 Emergency Contacts – {selected_city} Hospitals")

    for h in filtered_hospitals:
        st.markdown(f"#### 🏥 {h['name']}")
        c1, c2 = st.columns(2)
        c1.warning(f"📞 **Emergency:** {h['emergency_no']}")
        c2.error(f"🚑 **Ambulance:** {h['ambulance_no']}")

        st.markdown("**👨‍⚕️ On-call Doctors:**")
        for doc in h["doctors"]:
            st.info(f"**{doc['name']}** (🩺 {doc['speciality']} • 🕐 {doc['timing']}) 📞 {doc['contact']}")
        st.markdown("---")

elif page == "Appointments":
    st.markdown("<h1 class='main-header'>📅 Book Appointment</h1>", unsafe_allow_html=True)
    st.markdown(f"*Schedule your visit with top doctors in {selected_city}*")

    # FIX 5: moved hospital selector outside the form so doctor list updates reactively
    st.subheader("📝 Appointment Request Form")
    hosp_names = [h["name"] for h in filtered_hospitals]
    selected_hosp = st.selectbox("Select Hospital *", ["Choose a hospital..."] + hosp_names)

    doc_list = ["Choose a doctor..."]
    if selected_hosp != "Choose a hospital...":
        hdata = next((item for item in filtered_hospitals if item["name"] == selected_hosp), None)
        if hdata:
            doc_list += [f"{d['name']} – {d['speciality']}" for d in hdata["doctors"]]

    selected_doc = st.selectbox("Select Doctor *", doc_list)

    with st.form("appointment_form"):
        c3, c4 = st.columns(2)
        name = c3.text_input("Patient Name *", placeholder="Enter full name")
        age = c4.number_input("Age", min_value=0, max_value=120, step=1)

        c5, c6 = st.columns(2)
        phone = c5.text_input("Mobile Number *", placeholder="+91-XXXXXXXXXX")
        email = c6.text_input("Email (optional)", placeholder="email@example.com")

        c7, c8 = st.columns(2)
        gender = c7.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
        # FIX 6: added min_value to date_input to suppress deprecation warning
        date = c8.date_input("Preferred Date", min_value=datetime.date.today())

        symptoms = st.text_area("Reason for Visit / Symptoms", placeholder="Describe your symptoms or reason for consultation...")

        submitted = st.form_submit_button("✅ Request Appointment", type="primary", use_container_width=True)

        if submitted:
            if name and phone and selected_hosp != "Choose a hospital..." and selected_doc != "Choose a doctor...":
                st.success(
                    f"Appointment request submitted successfully for **{name}** with **{selected_doc}** "
                    f"at **{selected_hosp}** on **{date}**."
                )
            else:
                st.error("Please fill all required fields (*).")

    st.markdown("### 🕐 All Doctor Timings")
    for h in filtered_hospitals:
        with st.expander(f"🏥 {h['name']}"):
            for doc in h["doctors"]:
                st.info(
                    f"**{doc['name']}** (🩺 {doc['speciality']} | 🎓 {doc['qualification']})\n\n"
                    f"🕐 {doc['timing']} | 📞 {doc['contact']}"
                )

elif page == "About":
    st.markdown("<h1 class='main-header'>ℹ️ About MediFind</h1>", unsafe_allow_html=True)
    st.markdown("*Your trusted healthcare companion across India*")

    st.markdown("""
    **MediFind** is a smart hospital discovery and emergency response platform designed to help patients:

    * 🔍 Find top-rated multispecialty hospitals nearby
    * 👨‍⚕️ View doctor profiles, qualifications & specialities
    * 🛏️ Compare room charges and available treatments
    * 🚑 Connect with ambulance services instantly
    * 📞 One-click call to doctors and emergency units
    * 📅 Book appointments seamlessly
    * 📊 Visualize hospital data with advanced analytics
    * 🗺️ Interactive maps for easy navigation
    """)

    st.markdown("### 🏙️ Cities Covered")
    st.write(" • ".join([f"**{c}**" for c in cities]))

    st.markdown("### 🚨 Emergency Numbers (National)")
    st.table(pd.DataFrame([
        {"Service": "Universal Emergency", "Number": "112"},
        {"Service": "Ambulance", "Number": "108"},
        {"Service": "Maternal Ambulance", "Number": "102"},
        {"Service": "Police", "Number": "100"},
        {"Service": "Fire", "Number": "101"}
    ]))

    st.warning("⚠️ **Disclaimer:** This app provides information for guidance only. In a life-threatening emergency always call **112** immediately.")
