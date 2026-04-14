import streamlit as st
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import pydeck as pdk

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MediFind – Hospital Finder",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS (keeping your original styles)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.main { background: #f0f4ff; }
section[data-testid="stSidebar"] { background: #0a0f2e !important; }
section[data-testid="stSidebar"] * { color: #e0e6ff !important; }
header { visibility: hidden; }

.hero-banner {
    background: linear-gradient(135deg, #0a0f2e 0%, #1a2560 50%, #0d3b7a 100%);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(10,15,46,0.3);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(99,179,237,0.08);
}
.hero-banner h1 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 8px 0;
}
.hero-banner p {
    color: #93c5fd;
    font-size: 1.05rem;
    margin: 0;
}

.hospital-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(10,15,46,0.08);
    border: 1px solid #e2e8f0;
    transition: transform 0.2s, box-shadow 0.2s;
}
.hospital-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 40px rgba(10,15,46,0.14);
}
.hospital-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #0a0f2e;
    margin-bottom: 4px;
}
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin: 2px 3px;
}
.badge-blue  { background:#dbeafe; color:#1d4ed8; }
.badge-green { background:#dcfce7; color:#15803d; }
.badge-red   { background:#fee2e2; color:#b91c1c; }
.badge-amber { background:#fef3c7; color:#b45309; }

.doctor-card {
    background: #f8faff;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 8px 0;
    border-left: 4px solid #3b82f6;
}
.doctor-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    color: #1e3a8a;
    font-size: 1.05rem;
}

.emergency-dash {
    background: linear-gradient(135deg, #7f1d1d, #991b1b);
    border-radius: 18px;
    padding: 28px 32px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(153,27,27,0.35);
}
.emergency-dash h2 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    margin: 0 0 6px 0;
}
.pulse-dot {
    display: inline-block;
    width: 10px; height: 10px;
    background: #f87171;
    border-radius: 50%;
    animation: pulse 1.2s infinite;
    margin-right: 8px;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.5; transform:scale(1.4); }
}

.room-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.room-table th {
    background: #1e3a8a;
    color: white;
    padding: 10px 14px;
    text-align: left;
    font-size: 0.84rem;
    font-weight: 600;
    letter-spacing: 0.4px;
}
.room-table td {
    padding: 9px 14px;
    font-size: 0.88rem;
    border-bottom: 1px solid #e2e8f0;
}
.room-table tr:nth-child(even) td { background: #f8faff; }

.stars { color: #f59e0b; font-size: 1.1rem; }

.call-btn {
    display: inline-block;
    background: linear-gradient(90deg,#16a34a,#15803d);
    color: white !important;
    border: none;
    padding: 10px 22px;
    border-radius: 30px;
    font-weight: 700;
    font-size: 0.92rem;
    text-decoration: none;
    cursor: pointer;
    margin: 4px 4px 4px 0;
    box-shadow: 0 4px 12px rgba(22,163,74,0.3);
}
.call-btn-red {
    background: linear-gradient(90deg,#dc2626,#b91c1c);
    box-shadow: 0 4px 12px rgba(220,38,38,0.3);
}

.appt-block {
    background: #eff6ff;
    border-radius: 12px;
    padding: 14px 18px;
    border: 1px solid #bfdbfe;
    margin-top: 10px;
}

.section-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #1e3a8a;
    margin: 18px 0 8px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.sidebar-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #94a3b8;
    margin: 18px 0 6px 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA WITH COORDINATES
# ─────────────────────────────────────────────
HOSPITALS = {
    "Mumbai": [
        {
            "name": "Kokilaben Dhirubhai Ambani Hospital",
            "address": "Rao Saheb, Achutrao Patwardhan Marg, Four Bungalows, Andheri West, Mumbai – 400053",
            "lat": 19.1197, "lon": 72.8346,
            "rating": 4.8,
            "specialities": ["Cardiology", "Oncology", "Neurology", "Orthopedics", "Gastroenterology"],
            "emergency_no": "022-30999999",
            "ambulance_no": "022-30999911",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "NABH & JCI accredited 750-bed super-specialty hospital with state-of-the-art OT suites, robotic surgery, and 24×7 emergency services.",
            "rooms": {"General Ward": 2500, "Semi-Private": 5000, "Private Room": 9000, "ICU": 18000},
            "treatments": ["Robotic Surgery", "Bone Marrow Transplant", "TAVI Procedure", "CyberKnife Radiosurgery", "Liver Transplant"],
            "ambulance": True,
            "beds": 750,
            "doctors": [
                {"name": "Dr. Santosh Shetty", "speciality": "Cardiology", "qualification": "MD, DM (Cardiology) – AIIMS Delhi", "timing": "Mon–Fri 10am–2pm", "contact": "+91-9820000001"},
                {"name": "Dr. Priya Mehta", "speciality": "Oncology", "qualification": "MS, MCh (Onco) – Tata Memorial", "timing": "Mon–Sat 9am–1pm", "contact": "+91-9820000002"},
                {"name": "Dr. Ramesh Gupta", "speciality": "Neurology", "qualification": "MD, DM (Neurology) – KEM Mumbai", "timing": "Tue–Thu 3pm–6pm", "contact": "+91-9820000003"},
            ],
        },
        {
            "name": "Lilavati Hospital & Research Centre",
            "address": "A-791, Bandra Reclamation, Bandra West, Mumbai – 400050",
            "lat": 19.0596, "lon": 72.8295,
            "rating": 4.6,
            "specialities": ["Nephrology", "Urology", "Dermatology", "Pediatrics", "Gynecology"],
            "emergency_no": "022-26751000",
            "ambulance_no": "022-26751099",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "One of South Asia's premier multi-specialty hospitals with over 1,000 beds, advanced diagnostic imaging, and renowned surgical teams.",
            "rooms": {"General Ward": 2000, "Semi-Private": 4500, "Private Room": 8000, "ICU": 15000},
            "treatments": ["Kidney Transplant", "In-vitro Fertilisation", "Paediatric Cardiac Surgery", "Renal Dialysis", "Laparoscopic Surgery"],
            "ambulance": True,
            "beds": 1000,
            "doctors": [
                {"name": "Dr. Sanjay Kulkarni", "speciality": "Nephrology", "qualification": "MD, DM (Nephrology) – Grant Medical College", "timing": "Mon–Fri 11am–3pm", "contact": "+91-9870000011"},
                {"name": "Dr. Meena Joshi", "speciality": "Gynecology", "qualification": "MS (Obs & Gynae) – Mumbai University", "timing": "Mon–Sat 9am–12pm", "contact": "+91-9870000012"},
            ],
        },
    ],
    "Delhi": [
        {
            "name": "All India Institute of Medical Sciences (AIIMS)",
            "address": "Sri Aurobindo Marg, Ansari Nagar, New Delhi – 110029",
            "lat": 28.5672, "lon": 77.2100,
            "rating": 4.9,
            "specialities": ["Cardiology", "Oncology", "Neurology", "Endocrinology", "Transplant Surgery"],
            "emergency_no": "011-26588500",
            "ambulance_no": "011-26588444",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "India's premier government medical institute with globally recognised research, 2,000+ beds and 24-hour trauma centre.",
            "rooms": {"General Ward": 500, "Semi-Private": 2000, "Private Room": 5000, "ICU": 12000},
            "treatments": ["Multiorgan Transplant", "Proton Beam Therapy", "Deep Brain Stimulation", "CAR-T Cell Therapy", "Paediatric Oncology"],
            "ambulance": True,
            "beds": 2000,
            "doctors": [
                {"name": "Dr. Anand Kumar", "speciality": "Cardiothoracic Surgery", "qualification": "MS, MCh – AIIMS Delhi", "timing": "Mon–Wed 9am–1pm", "contact": "+91-9910000021"},
                {"name": "Dr. Sunita Sharma", "speciality": "Endocrinology", "qualification": "MD, DM – PGI Chandigarh", "timing": "Tue–Sat 10am–2pm", "contact": "+91-9910000022"},
                {"name": "Dr. Vikram Nair", "speciality": "Neurosurgery", "qualification": "MS, MCh (Neurosurgery) – AIIMS Delhi", "timing": "Thu–Fri 2pm–5pm", "contact": "+91-9910000023"},
            ],
        },
    ],
    "Bengaluru": [
        {
            "name": "Manipal Hospital (Old Airport Road)",
            "address": "98, HAL Airport Road, Bengaluru – 560017",
            "lat": 12.9576, "lon": 77.6428,
            "rating": 4.7,
            "specialities": ["Cardiology", "Orthopedics", "Nephrology", "Oncology", "Spine Surgery"],
            "emergency_no": "080-25024444",
            "ambulance_no": "080-25024400",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "600-bed multi-specialty hospital with Level 1 Trauma Centre, internationally trained surgeons and cutting-edge medical technology.",
            "rooms": {"General Ward": 1800, "Semi-Private": 4000, "Private Room": 7500, "ICU": 16000},
            "treatments": ["Total Joint Replacement", "Spine Surgery", "Renal Transplant", "Coronary Bypass", "Minimally Invasive Surgery"],
            "ambulance": True,
            "beds": 600,
            "doctors": [
                {"name": "Dr. Rajeev Sood", "speciality": "Orthopedic Surgery", "qualification": "MS (Ortho) – Kasturba Medical College", "timing": "Mon–Fri 9am–1pm", "contact": "+91-9845000031"},
                {"name": "Dr. Kavitha Reddy", "speciality": "Cardiology", "qualification": "MD, DM – Sri Jayadeva Institute", "timing": "Mon–Sat 11am–3pm", "contact": "+91-9845000032"},
            ],
        },
    ],
    "Nagpur": [
        {
            "name": "Kingsway Hospital",
            "address": "68, Kingsway Road, Nagpur – 440001",
            "lat": 21.1458, "lon": 79.0882,
            "rating": 4.5,
            "specialities": ["General Medicine", "Orthopedics", "Cardiology", "Pediatrics", "Gynecology"],
            "emergency_no": "0712-2524444",
            "ambulance_no": "0712-2524400",
            "image_url": "https://images.unsplash.com/photo-1516841273335-e39b37888115?w=800&q=80",
            "about": "Leading multi-specialty hospital in central India with 450+ beds and a dedicated trauma care unit serving Vidarbha region.",
            "rooms": {"General Ward": 1200, "Semi-Private": 2800, "Private Room": 5500, "ICU": 12000},
            "treatments": ["Cardiac Angioplasty", "Joint Replacement", "Normal & C-Section Delivery", "Paediatric Surgery", "Laparoscopic Procedures"],
            "ambulance": True,
            "beds": 450,
            "doctors": [
                {"name": "Dr. Abhijit Deshmukh", "speciality": "Cardiology", "qualification": "MD, DM (Cardiology) – Nagpur University", "timing": "Mon–Sat 10am–1pm", "contact": "+91-9890000041"},
                {"name": "Dr. Preeti Shende", "speciality": "Gynecology", "qualification": "MS (Obs & Gynae) – NKP Salve Medical College", "timing": "Mon–Fri 9am–12pm", "contact": "+91-9890000042"},
                {"name": "Dr. Nishant Bakde", "speciality": "Orthopedics", "qualification": "MS (Ortho) – GMCH Nagpur", "timing": "Tue–Sat 4pm–7pm", "contact": "+91-9890000043"},
            ],
        },
        {
            "name": "Orange City Hospital & Research Institute",
            "address": "Wadi, Nagpur – 440023",
            "lat": 21.0867, "lon": 79.0495,
            "rating": 4.6,
            "specialities": ["Oncology", "Neurology", "Urology", "Nephrology", "Dermatology"],
            "emergency_no": "0712-6630000",
            "ambulance_no": "0712-6630099",
            "image_url": "https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?w=800&q=80",
            "about": "NABH-accredited 500-bed hospital with advanced cancer care, robotic-assisted surgery and 24×7 emergency & trauma services.",
            "rooms": {"General Ward": 1500, "Semi-Private": 3500, "Private Room": 6500, "ICU": 14000},
            "treatments": ["Robotic Prostatectomy", "Chemotherapy", "Neuro Endovascular", "Dialysis", "PET-CT Guided Biopsy"],
            "ambulance": True,
            "beds": 500,
            "doctors": [
                {"name": "Dr. Sudhir Paunikar", "speciality": "Oncology", "qualification": "MD, DM – Tata Memorial Centre", "timing": "Mon–Fri 10am–2pm", "contact": "+91-9860000051"},
                {"name": "Dr. Archana Wankhede", "speciality": "Neurology", "qualification": "MD, DM (Neurology) – AIIMS Nagpur", "timing": "Mon–Sat 9am–12pm", "contact": "+91-9860000052"},
            ],
        },
    ],
    "Chennai": [
        {
            "name": "Apollo Hospitals (Greams Road)",
            "address": "21, Greams Lane, Off Greams Road, Chennai – 600006",
            "lat": 13.0569, "lon": 80.2409,
            "rating": 4.8,
            "specialities": ["Cardiology", "Oncology", "Transplant", "Neurology", "Orthopedics"],
            "emergency_no": "044-28290200",
            "ambulance_no": "1066",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "Asia's first JCI-accredited hospital with 700 beds. Pioneer in cardiac and organ transplant surgeries with internationally trained faculty.",
            "rooms": {"General Ward": 2200, "Semi-Private": 4800, "Private Room": 9500, "ICU": 20000},
            "treatments": ["Heart Transplant", "Liver Transplant", "Stem Cell Therapy", "IMRT Cancer Treatment", "Spinal Fusion"],
            "ambulance": True,
            "beds": 700,
            "doctors": [
                {"name": "Dr. K. Harishkumar", "speciality": "Cardiac Surgery", "qualification": "MS, MCh – JIPMER Puducherry", "timing": "Mon–Fri 9am–1pm", "contact": "+91-9444000061"},
                {"name": "Dr. Malathi Srinivasan", "speciality": "Oncology", "qualification": "MD, DM – Adyar Cancer Institute", "timing": "Tue–Sat 10am–2pm", "contact": "+91-9444000062"},
            ],
        },
    ],
}

CITIES = sorted(HOSPITALS.keys())

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 MediFind")
    st.markdown("---")
    st.markdown('<p class="sidebar-label">Search</p>', unsafe_allow_html=True)
    selected_city = st.selectbox("Select City", CITIES, index=CITIES.index("Nagpur") if "Nagpur" in CITIES else 0)

    all_specs = sorted({s for h in HOSPITALS[selected_city] for s in h["specialities"]})
    selected_spec = st.selectbox("Filter by Speciality", ["All"] + all_specs)

    min_rating = st.slider("Minimum Rating ⭐", 1.0, 5.0, 4.0, 0.1)
    st.markdown("---")
    st.markdown('<p class="sidebar-label">Navigation</p>', unsafe_allow_html=True)
    page = st.radio("", [
        "🏥 Hospital Search", 
        "📊 Analytics Dashboard",
        "🗺️ Hospital Map", 
        "🚨 Emergency Dashboard", 
        "📅 Appointments", 
        "ℹ️ About"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**🆘 National Emergency**")
    st.markdown("📞 **112** – Police / Fire / Ambulance")
    st.markdown("📞 **108** – Ambulance (free)")
    st.markdown("📞 **102** – Maternal Ambulance")

# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
filtered = [
    h for h in HOSPITALS[selected_city]
    if h["rating"] >= min_rating and (selected_spec == "All" or selected_spec in h["specialities"])
]

# ─────────────────────────────────────────────
# PAGE: HOSPITAL SEARCH
# ─────────────────────────────────────────────
if page == "🏥 Hospital Search":
    st.markdown(f"""
    <div class="hero-banner">
        <h1>🏥 MediFind</h1>
        <p>Discover top-rated multispecialty hospitals near you • Instant doctor connect • 24×7 ambulance</p>
    </div>
    """, unsafe_allow_html=True)

    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.metric("🏥 Hospitals Found", len(filtered))
    with col_stat2:
        st.metric("👨‍⚕️ Doctors Available", sum(len(h["doctors"]) for h in filtered))
    with col_stat3:
        st.metric("⭐ Avg Rating", f"{sum(h['rating'] for h in filtered)/max(len(filtered),1):.1f}" if filtered else "—")
    with col_stat4:
        st.metric("🚑 Ambulance Ready", sum(1 for h in filtered if h["ambulance"]))

    st.markdown("---")

    if not filtered:
        st.warning("No hospitals match your filters. Try lowering the minimum rating or selecting 'All' specialities.")
    else:
        for h in filtered:
            with st.container():
                st.markdown(f"""
                <div class="hospital-card">
                    <div class="hospital-name">🏥 {h['name']}</div>
                    <div style="color:#64748b;font-size:0.88rem;margin-bottom:8px;">📍 {h['address']}</div>
                    <div class="stars">{'★' * int(h['rating'])}{'☆' * (5-int(h['rating']))}</div>
                    <span style="font-weight:700;color:#f59e0b;margin-left:6px;">{h['rating']}/5</span>
                    <div style="margin-top:10px;">
                        {''.join(f'<span class="badge badge-blue">{s}</span>' for s in h['specialities'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏨 Overview", "👨‍⚕️ Doctors", "🛏️ Room Charges", "💊 Treatments", "📞 Contact & Ambulance"])

                with tab1:
                    img_col, info_col = st.columns([1, 2])
                    with img_col:
                        st.image(h["image_url"], use_container_width=True, caption=h["name"])
                    with info_col:
                        st.markdown(f"**About:** {h['about']}")
                        st.markdown(f"**📍 Address:** {h['address']}")
                        st.markdown(f"**⭐ Rating:** {h['rating']} / 5.0")
                        st.markdown(f"**🛏️ Total Beds:** {h['beds']}")
                        st.markdown("**🔬 Specialities:**")
                        st.markdown(" | ".join(f"`{s}`" for s in h["specialities"]))

                with tab2:
                    for doc in h["doctors"]:
                        st.markdown(f"""
                        <div class="doctor-card">
                            <div class="doctor-name">👨‍⚕️ {doc['name']}</div>
                            <div style="font-size:0.88rem;color:#1d4ed8;margin:2px 0;">🩺 {doc['speciality']}</div>
                            <div style="font-size:0.85rem;color:#374151;">🎓 {doc['qualification']}</div>
                            <div style="font-size:0.85rem;color:#374151;margin-top:4px;">🕐 {doc['timing']}</div>
                            <div style="margin-top:10px;">
                                <a href="tel:{doc['contact']}" class="call-btn">📞 Call Dr. {doc['name'].split()[-1]}</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                with tab3:
                    st.markdown('<div class="section-header">🛏️ Room Charges & Tariff</div>', unsafe_allow_html=True)
                    
                    # Display as table
                    room_html = """
                    <table class="room-table">
                        <tr><th>Room Type</th><th>Charges</th></tr>
                    """
                    for rtype, charge in h["rooms"].items():
                        room_html += f"<tr><td>{rtype}</td><td><strong>₹{charge:,}/day</strong></td></tr>"
                    room_html += "</table>"
                    st.markdown(room_html, unsafe_allow_html=True)
                    
                    # Plotly bar chart
                    st.markdown("#### 📊 Visual Comparison")
                    room_df = pd.DataFrame(list(h["rooms"].items()), columns=["Room Type", "Charge"])
                    fig = px.bar(room_df, x="Room Type", y="Charge", 
                                color="Charge",
                                color_continuous_scale="Blues",
                                title="Room Charges Comparison")
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)

                with tab4:
                    st.markdown('<div class="section-header">💊 Best Treatments Available</div>', unsafe_allow_html=True)
                    for t in h["treatments"]:
                        st.markdown(f'<span class="badge badge-green">✔ {t}</span>', unsafe_allow_html=True)

                with tab5:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"""
                        <div style="background:#fef3c7;border-radius:12px;padding:16px 20px;border:1px solid #fcd34d;">
                            <div style="font-weight:700;font-size:1rem;color:#92400e;">📞 Emergency Helpline</div>
                            <div style="font-size:1.4rem;font-weight:800;color:#b45309;margin-top:4px;">{h['emergency_no']}</div>
                            <a href="tel:{h['emergency_no']}" class="call-btn" style="margin-top:10px;display:inline-block;">📞 Call Emergency</a>
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        if h["ambulance"]:
                            st.markdown(f"""
                            <div style="background:#fee2e2;border-radius:12px;padding:16px 20px;border:1px solid #fca5a5;">
                                <div style="font-weight:700;font-size:1rem;color:#991b1b;">🚑 Ambulance Service</div>
                                <div style="font-size:1.4rem;font-weight:800;color:#b91c1c;margin-top:4px;">{h['ambulance_no']}</div>
                                <a href="tel:{h['ambulance_no']}" class="call-btn call-btn-red" style="margin-top:10px;display:inline-block;">🚑 Call Ambulance</a>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("<hr style='border:1px solid #e2e8f0;margin:4px 0 12px;'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: ANALYTICS DASHBOARD
# ─────────────────────────────────────────────
elif page == "📊 Analytics Dashboard":
    st.markdown(f"""
    <div class="hero-banner">
        <h1>📊 Analytics Dashboard</h1>
        <p>Visual insights into hospital data across {selected_city}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create DataFrame for analysis
    data_list = []
    for h in HOSPITALS[selected_city]:
        data_list.append({
            "Hospital": h["name"],
            "Rating": h["rating"],
            "Beds": h["beds"],
            "Doctors": len(h["doctors"]),
            "Specialities": len(h["specialities"]),
            "General Ward": h["rooms"]["General Ward"],
            "ICU": h["rooms"]["ICU"],
            "Latitude": h["lat"],
            "Longitude": h["lon"]
        })
    
    df = pd.DataFrame(data_list)
    
    # Summary Statistics
    st.subheader("📈 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Hospitals", len(df))
        st.metric("Total Beds", int(df["Beds"].sum()))
    with col2:
        st.metric("Avg Rating", f"{df['Rating'].mean():.2f}")
        st.metric("Total Doctors", int(df["Doctors"].sum()))
    with col3:
        st.metric("Highest Rating", f"{df['Rating'].max():.1f}")
        st.metric("Lowest Ward Cost", f"₹{int(df['General Ward'].min()):,}")
    with col4:
        st.metric("Avg Specialities", f"{df['Specialities'].mean():.1f}")
        st.metric("Avg ICU Cost", f"₹{int(df['ICU'].mean()):,}")
    
    st.markdown("---")
    
    # Plotly Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("⭐ Hospital Ratings Comparison")
        fig1 = px.bar(df, x="Hospital", y="Rating", 
                     color="Rating",
                     color_continuous_scale="RdYlGn",
                     title="Hospital Ratings")
        fig1.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_chart2:
        st.subheader("🛏️ Bed Capacity Analysis")
        fig2 = px.pie(df, values="Beds", names="Hospital", 
                     title="Bed Distribution",
                     hole=0.4)
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Matplotlib + Seaborn Charts
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.subheader("💰 Room Charges Comparison (Matplotlib)")
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.arange(len(df))
        width = 0.35
        ax.bar(x - width/2, df["General Ward"], width, label='General Ward', color='#60a5fa')
        ax.bar(x + width/2, df["ICU"], width, label='ICU', color='#f87171')
        ax.set_xlabel('Hospitals')
        ax.set_ylabel('Cost (₹)')
        ax.set_title('Room Charges Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels([h[:15] + "..." if len(h) > 15 else h for h in df["Hospital"]], rotation=45, ha='right')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
    
    with col_chart4:
        st.subheader("👨‍⚕️ Doctors vs Beds (Seaborn)")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=df, x="Beds", y="Doctors", size="Rating", 
                       hue="Rating", palette="viridis", sizes=(100, 400), ax=ax)
        ax.set_title("Doctors vs Bed Capacity")
        plt.tight_layout()
        st.pyplot(fig)
    
    # Correlation Heatmap
    st.subheader("🔥 Correlation Heatmap (Seaborn)")
    fig, ax = plt.subplots(figsize=(10, 6))
    numeric_df = df[["Rating", "Beds", "Doctors", "Specialities", "General Ward", "ICU"]]
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", center=0, ax=ax, fmt=".2f")
    ax.set_title("Feature Correlation Matrix")
    plt.tight_layout()
    st.pyplot(fig)
    
    # Plotly 3D Scatter
    st.subheader("🌐 3D Analysis: Rating × Beds × Doctors")
    fig3d = px.scatter_3d(df, x="Beds", y="Doctors", z="Rating",
                         color="Rating", size="Beds",
                         hover_name="Hospital",
                         color_continuous_scale="Viridis",
                         title="3D Hospital Metrics")
    fig3d.update_layout(height=600)
    st.plotly_chart(fig3d, use_container_width=True)
    
    # Raw Data Table
    st.subheader("📋 Raw Data Table (Pandas)")
    st.dataframe(df.style.highlight_max(axis=0, color='lightgreen').format({
        "Rating": "{:.1f}",
        "General Ward": "₹{:,.0f}",
        "ICU": "₹{:,.0f}"
    }))
    
    # Download CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f'medifind_{selected_city}_data.csv',
        mime='text/csv',
    )

# ─────────────────────────────────────────────
# PAGE: HOSPITAL MAP
# ─────────────────────────────────────────────
elif page == "🗺️ Hospital Map":
    st.markdown(f"""
    <div class="hero-banner">
        <h1>🗺️ Hospital Map</h1>
        <p>Interactive map showing hospital locations in {selected_city}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare data
    map_data = []
    for h in HOSPITALS[selected_city]:
        map_data.append({
            "name": h["name"],
            "lat": h["lat"],
            "lon": h["lon"],
            "rating": h["rating"],
            "beds": h["beds"],
            "emergency": h["emergency_no"]
        })
    
    map_df = pd.DataFrame(map_data)
    
    # Folium Map
    st.subheader("🗺️ Interactive Map (Folium)")
    
    center_lat = map_df["lat"].mean()
    center_lon = map_df["lon"].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    
    for idx, row in map_df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"""
            <b>{row['name']}</b><br>
            ⭐ Rating: {row['rating']}/5<br>
            🛏️ Beds: {row['beds']}<br>
            📞 Emergency: {row['emergency']}
            """,
            tooltip=row["name"],
            icon=folium.Icon(color="red", icon="plus", prefix='fa')
        ).add_to(m)
    
    st_folium(m, width=1200, height=500)
    
    # PyDeck 3D Map
    st.subheader("🌆 3D Hospital Visualization (PyDeck)")
    
    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=11,
        pitch=50,
    )
    
    layer = pdk.Layer(
        "ColumnLayer",
        data=map_df,
        get_position=["lon", "lat"],
        get_elevation="beds",
        elevation_scale=2,
        radius=200,
        get_fill_color=["rating * 50", "100", "rating * 30", 200],
        pickable=True,
        auto_highlight=True,
    )
    
    tooltip = {
        "html": "<b>{name}</b><br>Rating: {rating}/5<br>Beds: {beds}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }
    
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9"
    )
    
    st.pydeck_chart(r)
    
    # Plotly Map
    st.subheader("📍 Hospital Scatter Map (Plotly)")
    fig_map = px.scatter_mapbox(
        map_df, 
        lat="lat", 
        lon="lon",
        hover_name="name",
        hover_data={"rating": True, "beds": True, "lat": False, "lon": False},
        color="rating",
        size="beds",
        color_continuous_scale="Viridis",
        size_max=20,
        zoom=11,
        height=500
    )
    fig_map.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig_map, use_container_width=True)

# ─────────────────────────────────────────────
# PAGE: EMERGENCY DASHBOARD
# ─────────────────────────────────────────────
elif page == "🚨 Emergency Dashboard":
    st.markdown("""
    <div class="emergency-dash">
        <h2><span class="pulse-dot"></span>Emergency Dashboard</h2>
        <p style="color:#fca5a5;font-size:0.95rem;margin:0;">One-click direct connect to doctors & ambulance • 24×7 Active</p>
    </div>
    """, unsafe_allow_html=True)

    st.error("⚠️ For life-threatening emergencies, call **112** immediately!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#fee2e2;border-radius:16px;padding:24px;text-align:center;border:2px solid #f87171;">
            <div style="font-size:2.5rem;">🚑</div>
            <div style="font-weight:800;font-size:1.1rem;color:#991b1b;">National Ambulance</div>
            <div style="font-size:2rem;font-weight:900;color:#dc2626;margin:8px 0;">108</div>
            <a href="tel:108" class="call-btn call-btn-red">🚑 Call 108 Now</a>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#fef3c7;border-radius:16px;padding:24px;text-align:center;border:2px solid #fcd34d;">
            <div style="font-size:2.5rem;">🚒</div>
            <div style="font-weight:800;font-size:1.1rem;color:#92400e;">Police / Fire / Rescue</div>
            <div style="font-size:2rem;font-weight:900;color:#b45309;margin:8px 0;">112</div>
            <a href="tel:112" class="call-btn" style="background:linear-gradient(90deg,#d97706,#b45309);">📞 Call 112 Now</a>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#dcfce7;border-radius:16px;padding:24px;text-align:center;border:2px solid #86efac;">
            <div style="font-size:2.5rem;">🤱</div>
            <div style="font-weight:800;font-size:1.1rem;color:#14532d;">Maternal Ambulance</div>
            <div style="font-size:2rem;font-weight:900;color:#16a34a;margin:8px 0;">102</div>
            <a href="tel:102" class="call-btn">📞 Call 102 Now</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(f"🏥 Emergency Contacts – {selected_city} Hospitals")

    for h in HOSPITALS[selected_city]:
        with st.expander(f"🏥 {h['name']} — Emergency: {h['emergency_no']}"):
            ec1, ec2 = st.columns(2)
            with ec1:
                st.markdown(f"**📞 Emergency:** {h['emergency_no']}")
                st.markdown(f'<a href="tel:{h["emergency_no"]}" class="call-btn">📞 Emergency Call</a>', unsafe_allow_html=True)
            with ec2:
                st.markdown(f"**🚑 Ambulance:** {h['ambulance_no']}")
                st.markdown(f'<a href="tel:{h["ambulance_no"]}" class="call-btn call-btn-red">🚑 Ambulance Call</a>', unsafe_allow_html=True)

            st.markdown("**👨‍⚕️ On-call Doctors:**")
            for doc in h["doctors"]:
                dc1, dc2, dc3, dc4 = st.columns([2, 2, 2, 1])
                with dc1: st.markdown(f"**{doc['name']}**")
                with dc2: st.markdown(f"🩺 {doc['speciality']}")
                with dc3: st.markdown(f"🕐 {doc['timing']}")
                with dc4: st.markdown(f'<a href="tel:{doc["contact"]}" class="call-btn" style="padding:6px 14px;font-size:0.8rem;">📞 Call</a>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: APPOINTMENTS
# ─────────────────────────────────────────────
elif page == "📅 Appointments":
    st.markdown(f"""
    <div class="hero-banner">
        <h1>📅 Book Appointment</h1>
        <p>Schedule your visit with top doctors in {selected_city}</p>
    </div>
    """, unsafe_allow_html=True)

    hosp_names = [h["name"] for h in HOSPITALS[selected_city]]
    sel_hosp_name = st.selectbox("Select Hospital", hosp_names)
    sel_hosp = next(h for h in HOSPITALS[selected_city] if h["name"] == sel_hosp_name)

    doc_names = [f"{d['name']} – {d['speciality']}" for d in sel_hosp["doctors"]]
    sel_doc_str = st.selectbox("Select Doctor", doc_names)
    sel_doc = sel_hosp["doctors"][doc_names.index(sel_doc_str)]

    st.markdown(f"""
    <div class="appt-block">
        <div class="section-header">👨‍⚕️ {sel_doc['name']}</div>
        <div><strong>🩺 Speciality:</strong> {sel_doc['speciality']}</div>
        <div><strong>🎓 Qualification:</strong> {sel_doc['qualification']}</div>
        <div><strong>🕐 Appointment Timing:</strong> {sel_doc['timing']}</div>
        <div><strong>📞 Direct Contact:</strong> {sel_doc['contact']}</div>
        <div style="margin-top:12px;">
            <a href="tel:{sel_doc['contact']}" class="call-btn">📞 Call to Book Appointment</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📝 Appointment Request Form")
    with st.form("appt_form"):
        fc1, fc2 = st.columns(2)
        with fc1:
            p_name = st.text_input("Patient Name *")
            p_age  = st.number_input("Age", min_value=0, max_value=120, value=30)
            p_gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
        with fc2:
            p_phone = st.text_input("Mobile Number *")
            p_email = st.text_input("Email (optional)")
            p_date  = st.date_input("Preferred Date")

        p_reason = st.text_area("Reason for Visit / Symptoms")
        submitted = st.form_submit_button("✅ Request Appointment")
        if submitted:
            if p_name and p_phone:
                st.success(f"✅ Appointment request submitted for **{p_name}** with **{sel_doc['name']}** on **{p_date}**. The hospital will call you on **{p_phone}** to confirm.")
                st.info(f"📞 You can also directly call: **{sel_doc['contact']}**")
            else:
                st.error("Please enter your name and mobile number.")

    st.markdown("---")
    st.subheader("🕐 All Doctor Timings")
    for h in HOSPITALS[selected_city]:
        with st.expander(f"🏥 {h['name']}"):
            for doc in h["doctors"]:
                st.markdown(f"""
                <div class="doctor-card">
                    <div class="doctor-name">{doc['name']}</div>
                    <div style="font-size:0.85rem;color:#1d4ed8;">🩺 {doc['speciality']} &nbsp;|&nbsp; 🎓 {doc['qualification']}</div>
                    <div style="font-size:0.85rem;color:#374151;margin-top:3px;">🕐 {doc['timing']} &nbsp;|&nbsp; 📞 {doc['contact']}</div>
                    <a href="tel:{doc['contact']}" class="call-btn" style="margin-top:8px;display:inline-block;padding:7px 16px;font-size:0.82rem;">📞 Call Now</a>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: ABOUT
# ─────────────────────────────────────────────
elif page == "ℹ️ About":
    st.markdown(f"""
    <div class="hero-banner">
        <h1>ℹ️ About MediFind</h1>
        <p>Your trusted healthcare companion across India</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **MediFind** is a smart hospital discovery and emergency response platform designed to help patients:
    - 🔍 Find top-rated multispecialty hospitals nearby
    - 👨‍⚕️ View doctor profiles, qualifications & specialities
    - 🛏️ Compare room charges and available treatments
    - 🚑 Connect with ambulance services instantly
    - 📞 One-click call to doctors and emergency units
    - 📅 Book appointments seamlessly
    - 📊 Visualize hospital data with advanced analytics
    - 🗺️ Interactive maps with Folium & PyDeck

    ### 🏙️ Cities Covered
    """ + ", ".join(f"**{c}**" for c in CITIES) + """

    ### 📚 Technologies Used
    - **Streamlit** – Web framework
    - **Pandas** – Data manipulation
    - **NumPy** – Numerical operations
    - **Matplotlib** – Static visualizations
    - **Seaborn** – Statistical plotting
    - **Plotly** – Interactive charts & 3D graphs
    - **Folium** – Interactive maps
    - **PyDeck** – 3D geospatial visualization

    ### 🚨 Emergency Numbers (National)
    | Service | Number |
    |---------|--------|
    | Universal Emergency | 112 |
    | Ambulance | 108 |
    | Maternal Ambulance | 102 |
    | Police | 100 |
    | Fire | 101 |

    ---
    > ⚠️ *This app provides information for guidance only. In a life-threatening emergency always call 112 immediately.*
    """)
