import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import datetime

# ==========================================================
# 1. PAGE CONFIG & CUSTOM CSS (From Edit Snippet + Enhancements)
# ==========================================================
st.set_page_config(
    page_title="Medifind - Hospital Finder",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling combining both snippets
st.markdown("""
<style>
    /* Global Background */
    .main { background-color: #f7fbff; }
    
    /* Typography */
    h1, h2, h3 { color: #1f77b4; }
    
    /* Cards */
    .card {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px grey;
    }
    
    /* Hospital Card Specifics */
    .hospital-card-wrapper {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        border: 1px solid #e2e8f0;
    }
    
    /* Header */
    .main-header {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(to right, #1e3a8a, #312e81);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    /* Stat Cards */
    .stat-card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
    }
    
    /* Sidebar Styling */
    .sidebar-header {
        text-align: center;
        color: #3b82f6;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. DATA SET (Comprehensive Data from First Snippet)
# ==========================================================
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
        }
    ]
}

# ==========================================================
# 3. HELPER FUNCTIONS
# ==========================================================

# FIX 1 & 2: Unique keys for tabs and modern image handling
def render_hospital_card(h):
    st.markdown(f"""
    <div class="hospital-card-wrapper">
        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 250px;">
                <img src="{h['image_url']}" style="width: 100%; border-radius: 12px; object-fit: cover; height: 200px;">
            </div>
            <div style="flex: 2; min-width: 300px;">
                <h2 style="margin-top: 0;">🏥 {h['name']}</h2>
                <p style="color: #666;">📍 {h['address']}</p>
                <p><b>Rating:</b> ⭐ {h['rating']}/5 | <b>Beds:</b> 🛏️ {h['beds']}</p>
                
                <div style="margin: 10px 0;">
                    {' '.join([f'<span style="background:#dbeafe; color:#1e40af; padding:4px 10px; border-radius:20px; font-size:14px; font-weight:600; margin-right:5px;">{s}</span>' for s in h['specialities']])}
                </div>
                
                <p><b>🚑 Ambulance:</b> {'✅ Available' if h['ambulance'] else '❌ Not Available'} | <b>📞 Emergency:</b> {h['emergency_no']}</p>
            </div>
        </div>
        
        <hr style="margin: 15px 0; border: none; border-top: 1px solid #eee;">
        
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <details style="flex: 1; min-width: 200px; background: #f9fafb; padding: 10px; border-radius: 8px;">
                <summary style="cursor: pointer; font-weight: bold;">👨‍⚕️ Doctors</summary>
                <ul style="padding-left: 20px; margin-top: 5px;">
                    {''.join([f'<li style="margin-bottom: 5px;">{d["name"]}<br><small>{d["speciality"]} | {d["timing"]} | {d["contact"]}</small></li>' for d in h["doctors"]])}
                </ul>
            </details>
            
            <details style="flex: 1; min-width: 200px; background: #f9fafb; padding: 10px; border-radius: 8px;">
                <summary style="cursor: pointer; font-weight: bold;">💰 Room Charges</summary>
                <table style="width: 100%; margin-top: 5px; font-size: 14px;">
                    <tr><td>General</td><td>₹{h['rooms']['General']}</td></tr>
                    <tr><td>Semi-Private</td><td>₹{h['rooms']['SemiPrivate']}</td></tr>
                    <tr><td>Private</td><td>₹{h['rooms']['Private']}</td></tr>
                    <tr><td>ICU</td><td>₹{h['rooms']['ICU']}</td></tr>
                </table>
            </details>
            
            <details style="flex: 1; min-width: 200px; background: #f9fafb; padding: 10px; border-radius: 8px;">
                <summary style="cursor: pointer; font-weight: bold;">✅ Treatments</summary>
                <ul style="padding-left: 20px; margin-top: 5px;">
                    {''.join([f'<li>{t}</li>' for t in h['treatments']])}
                </ul>
            </details>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# 4. SIDEBAR & NAVIGATION
# ==========================================================

st.sidebar.markdown('<p class="sidebar-header">🏥 Medifind</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")

# Menu selection based on Edit Snippet structure, but keeping advanced pages
page_selection = st.sidebar.radio(
    "📌 Navigation",
    ["Home", "Find Hospital", "Hospital Map", "Analytics", "Emergency", "Appointments", "About"]
)

# Filters (Global)
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Search & Filters")
cities = sorted(list(HOSPITALS.keys()))
selected_city = st.sidebar.selectbox("Select City", cities, index=cities.index("Nagpur") if "Nagpur" in cities else 0)

all_specs = set()
for h in HOSPITALS.get(selected_city, []):
    for s in h["specialities"]:
        all_specs.add(s)
all_specs = ["All"] + sorted(list(all_specs))
selected_spec = st.sidebar.selectbox("Speciality", all_specs)
min_rating = st.sidebar.slider("Minimum Rating ⭐", 1.0, 5.0, 4.0, 0.1)

# Filter Logic
filtered_hospitals = [
    h for h in HOSPITALS.get(selected_city, [])
    if h["rating"] >= min_rating and (selected_spec == "All" or selected_spec in h["specialities"])
]

# Stats for sidebar
total_docs = sum(len(h["doctors"]) for h in filtered_hospitals)
avg_rtg = sum(h["rating"] for h in filtered_hospitals) / len(filtered_hospitals) if filtered_hospitals else 0
amb_ready = sum(1 for h in filtered_hospitals if h.get("ambulance", False))

st.sidebar.markdown("---")
st.sidebar.metric("🏥 Hospitals", len(filtered_hospitals))
st.sidebar.metric("👨‍⚕️ Doctors", total_docs)
st.sidebar.metric("⭐ Avg Rating", f"{avg_rtg:.1f}")
st.sidebar.markdown("---")
st.sidebar.error("🆘 **Emergency**\n\n📞 **112** (Universal)\n🚑 **108** (Ambulance)")

# ==========================================================
# 5. PAGE RENDERING LOGIC
# ==========================================================

# -- HOME PAGE --
if page_selection == "Home":
    st.markdown("<h1 class='main-header'>🏥 Medifind</h1>", unsafe_allow_html=True)
    st.markdown("### *Discover top-rated multispecialty hospitals near you • Instant doctor connect • 24×7 ambulance*")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("""
        **Medifind** helps users quickly find nearby hospitals along with their facilities, doctors, and emergency services. 
        Whether you need a routine checkup or urgent care, we are here to guide you.
        """)
        st.success("""
        ✅ **Fast Hospital Search** by City & Speciality  
        ✅ **Interactive Map** for directions  
        ✅ **Detailed Profiles** of Doctors & Rooms  
        ✅ **Direct Ambulance** & Emergency Calling  
        ✅ **Online Appointment** Booking  
        """)
    with col2:
        st.image("https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?w=600&q=80", use_container_width=True)

# -- FIND HOSPITAL PAGE --
elif page_selection == "Find Hospital":
    st.markdown("<h1 class='main-header'>🔍 Find Nearby Hospitals</h1>", unsafe_allow_html=True)
    st.markdown(f"### 🏥 Available Hospitals in **{selected_city}**")
    
    if not filtered_hospitals:
        st.warning(f"⚠️ No hospitals found in {selected_city} matching your criteria.")
    else:
        for h in filtered_hospitals:
            render_hospital_card(h)

# -- HOSPITAL MAP PAGE --
elif page_selection == "Hospital Map":
    st.markdown("<h1 class='main-header'>🗺️ Hospital Map</h1>", unsafe_allow_html=True)
    
    if not filtered_hospitals:
        st.warning("No hospitals to map for the current selection.")
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
        
        # FIX 3: Use container width
        st_folium(m, use_container_width=True, height=600)
        
        st.markdown("### 📍 Quick Links")
        cols = st.columns(2)
        for i, h in enumerate(filtered_hospitals):
            with cols[i % 2]:
                # FIX 4: Corrected Google Maps URL syntax
                maps_url = f"https://www.google.com/maps?q={h['lat']},{h['lon']}"
                st.markdown(f"""
                <div class="stat-card" style="margin-bottom: 10px;">
                    <h4>{h['name']}</h4>
                    <p style="font-size: 0.9em;">📍 {h['address']}<br>
                    ⭐ {h['rating']}/5 | 🛏️ {h['beds']} beds</p>
                    <a href="{maps_url}" target="_blank">🗺️ Open in Maps</a>
                </div>
                """, unsafe_allow_html=True)

# -- ANALYTICS PAGE --
elif page_selection == "Analytics":
    st.markdown("<h1 class='main-header'>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    if not filtered_hospitals:
        st.warning("No data to show based on current filters.")
    else:
        df = pd.DataFrame(filtered_hospitals)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Hospitals 🏥", len(filtered_hospitals))
        c2.metric("Total Beds 🛏️", sum(h["beds"] for h in filtered_hospitals))
        c3.metric("Avg Rating ⭐", f"{avg_rtg:.1f}")
        c4.metric("Total Doctors 👨‍&", total_docs)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ⭐ Hospital Ratings")
            fig1 = px.bar(df, x="name", y="rating", color_discrete_sequence=["#3b82f6"], range_y=[0, 5])
            fig1.update_layout(xaxis_title="", yaxis_title="Rating", xaxis_tickangle=-45)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("### 🛏️ Bed Distribution")
            fig2 = px.pie(df, names="name", values="beds", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown("### 💰 Room Charges Comparison")
        icu_data = [{"name": h["name"], "icu": h["rooms"]["ICU"], "general": h["rooms"]["General"]} for h in filtered_hospitals]
        fig3 = px.line(pd.DataFrame(icu_data), x="name", y=["icu", "general"], markers=True)
        fig3.update_layout(xaxis_title="", yaxis_title="Charge (₹)", xaxis_tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)

# -- EMERGENCY PAGE --
elif page_selection == "Emergency":
    st.markdown("<h1 class='main-header'>🚨 Emergency Dashboard</h1>", unsafe_allow_html=True)
    st.error("⚠️ **For life-threatening emergencies, call 112 immediately!**")
    
    col1, col2, col3 = st.columns(3)
    col1.error("🚑 **National Ambulance**\n# 108")
    col2.warning("🚒 **Police / Fire**\n# 100 / # 101")
    col3.info("☎ **General Emergency**\n# 112")
    
    st.markdown("---")
    st.markdown(f"### 🏥 Emergency Contacts – {selected_city}")
    
    for h in filtered_hospitals:
        with st.expander(f"🏥 {h['name']} - ⭐{h['rating']} | 🛏️ {h['beds']} beds"):
            c1, c2 = st.columns(2)
            c1.warning(f"📞 **Emergency**: {h['emergency_no']}")
            c2.error(f"🚑 **Ambulance**: {h['ambulance_no']}")
            
            st.markdown("**👨‍⚕️ On-call Doctors**:")
            for doc in h["doctors"]:
                st.info(f"**{doc['name']}** (🩺 {doc['speciality']}) • 🕐 {doc['timing']} • 📞 {doc['contact']}")

# -- APPOINTMENTS PAGE --
elif page_selection == "Appointments":
    st.markdown("<h1 class='main-header'>📅 Book Appointment</h1>", unsafe_allow_html=True)
    
    hosp_names = [h["name"] for h in filtered_hospitals]
    selected_hosp_name = st.selectbox("Select Hospital *", ["Choose a hospital..."] + hosp_names)
    
    doc_list = ["Choose a doctor..."]
    if selected_hosp_name != "Choose a hospital...":
        hdata = next((item for item in filtered_hospitals if item["name"] == selected_hosp_name), None)
        if hdata:
            doc_list += [f"{d['name']} – {d['speciality']}" for d in hdata["doctors"]]
    
    selected_doc = st.selectbox("Select Doctor *", doc_list)
    
    with st.form("appointment_form"):
        st.markdown("### 📝 Patient Details")
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name *", placeholder="Enter full name")
        age = c2.number_input("Age", min_value=0, max_value=120, step=1)
        
        c3, c4 = st.columns(2)
        phone = c3.text_input("Mobile Number *", placeholder="+91-XXXXXXXXXX")
        email = c4.text_input("Email (optional)", placeholder="email@example.com")
        
        # FIX 6: Added min_value
        date = st.date_input("Preferred Date", min_value=datetime.date.today())
        symptoms = st.text_area("Reason for Visit / Symptoms", placeholder="Describe your symptoms...")
        
        submitted = st.form_submit_button("✅ Request Appointment", type="primary", use_container_width=True)
        
        if submitted:
            if name and phone and selected_hosp_name != "Choose a hospital..." and selected_doc != "Choose a doctor...":
                st.success(f"✅ Appointment request submitted for **{name}** with **{selected_doc}** at **{selected_hosp_name}** on **{date}**. We will call you shortly to confirm.")
            else:
                st.error("Please fill all required fields (*).")

# -- ABOUT PAGE --
elif page_selection == "About":
    st.markdown("<h1 class='main-header'>ℹ️ About Medifind</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    **Medifind** is a smart hospital discovery and emergency response platform designed to help patients across India find the right healthcare facility quickly.
    
    ### 🚀 Features
    * 🔍 **Smart Search:** Filter hospitals by city, speciality, and rating.
    * 🗺️ **Interactive Maps:** Visualize hospital locations and get directions.
    * 📊 **Data Analytics:** Compare bed availability, room charges, and doctor ratings.
    * 🚑 **Emergency Ready:** One-click access to ambulance and emergency numbers.
    * 📅 **Online Booking:** Request appointments with top specialists.
    """)
    
    st.markdown("### 🏙️ Cities Covered")
    st.write(" • ".join([f"**{c}**" for c in cities]))
    
    st.markdown("### 🚨 Emergency Numbers")
    st.table(pd.DataFrame([
        {"Service": "Universal Emergency", "Number": "112"},
        {"Service": "Ambulance", "Number": "108"},
        {"Service": "Police", "Number": "100"},
        {"Service": "Fire Service", "Number": "101"},
        {"Service": "Maternal Ambulance", "Number": "102"}
    ]))
    
    st.warning("⚠️ **Disclaimer:** This app provides information for guidance only. In a life-threatening emergency, always call **112** immediately.")

# ==========================================================
# 6. FOOTER
# ==========================================================
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #666;'>
Developed by <b>Saransh Chakole</b> | MCA Project 2026<br>
<small>Medifind &copy; 2024</small>
</p>
""", unsafe_allow_html=True)

