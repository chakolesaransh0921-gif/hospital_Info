import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

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
            "lat": 19.1197, "lon": 72.8346,
            "rating": 4.8,
            "specialities": ["Cardiology", "Oncology", "Neurology", "Orthopedics", "Gastroenterology"],
            "emergency_no": "022-30999999", "ambulance_no": "022-30999911",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "NABH & JCI accredited 750-bed super-specialty hospital with state-of-the-art OT suites, robotic surgery, and 24×7 emergency services.",
            "rooms": {"General": 2500, "SemiPrivate": 5000, "Private": 9000, "ICU": 18000},
            "treatments": ["Robotic Surgery", "Bone Marrow Transplant", "TAVI Procedure", "CyberKnife Radiosurgery", "Liver Transplant"],
            "ambulance": True,
            "beds": 750,
            "doctors": [
                {"name": "Dr. Santosh Shetty", "speciality": "Cardiology", "qualification": "MD, DM (Cardiology) – AIIMS Delhi", "timing": "Mon–Fri 10am–2pm", "contact": "+91-9820000001"},
                {"name": "Dr. Priya Mehta", "speciality": "Oncology", "qualification": "MS, MCh (Onco) – Tata Memorial", "timing": "Mon–Sat 9am–1pm", "contact": "+91-9820000002"},
                {"name": "Dr. Ramesh Gupta", "speciality": "Neurology", "qualification": "MD, DM (Neurology) – KEM Mumbai", "timing": "Tue–Thu 3pm–6pm", "contact": "+91-9820000003"}
            ]
        },
        {
            "name": "Lilavati Hospital & Research Centre",
            "address": "A-791, Bandra Reclamation, Bandra West, Mumbai – 400050",
            "lat": 19.0596, "lon": 72.8295,
            "rating": 4.6,
            "specialities": ["Nephrology", "Urology", "Dermatology", "Pediatrics", "Gynecology"],
            "emergency_no": "022-26751000", "ambulance_no": "022-26751099",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
            "about": "One of South Asia's premier multi-specialty hospitals with over 1,000 beds, advanced diagnostic imaging, and renowned surgical teams.",
            "rooms": {"General": 2000, "SemiPrivate": 4500, "Private": 8000, "ICU": 15000},
            "treatments": ["Kidney Transplant", "In-vitro Fertilisation", "Paediatric Cardiac Surgery", "Renal Dialysis", "Laparoscopic Surgery"],
            "ambulance": True,
            "beds": 1000,
            "doctors": [
                {"name": "Dr. Sanjay Kulkarni", "speciality": "Nephrology", "qualification": "MD, DM (Nephrology) – Grant Medical College", "timing": "Mon–Fri 11am–3pm", "contact": "+91-9870000011"},
                {"name": "Dr. Meena Joshi", "speciality": "Gynecology", "qualification": "MS (Obs & Gynae) – Mumbai University", "timing": "Mon–Sat 9am–12pm", "contact": "+91-9870000012"}
            ]
        }
    ],
    "Delhi": [
        {
            "name": "All India Institute of Medical Sciences (AIIMS)",
            "address": "Sri Aurobindo Marg, Ansari Nagar, New Delhi – 110029",
            "lat": 28.5672, "lon": 77.2100,
            "rating": 4.9,
            "specialities": ["Cardiology", "Oncology", "Neurology", "Endocrinology", "Transplant Surgery"],
            "emergency_no": "011-26588500", "ambulance_no": "011-26588444",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80",
            "about": "India's premier government medical institute with globally recognised research, 2,000+ beds and 24-hour trauma centre.",
            "rooms": {"General": 500, "SemiPrivate": 2000, "Private": 5000, "ICU": 12000},
            "treatments": ["Multiorgan Transplant", "Proton Beam Therapy", "Deep Brain Stimulation", "CAR-T Cell Therapy", "Paediatric Oncology"],
            "ambulance": True,
            "beds": 2000,
            "doctors": [
                {"name": "Dr. Anand Kumar", "speciality": "Cardiothoracic Surgery", "qualification": "MS, MCh – AIIMS Delhi", "timing": "Mon–Wed 9am–1pm", "contact": "+91-9910000021"},
                {"name": "Dr. Sunita Sharma", "speciality": "Endocrinology", "qualification": "MD, DM – PGI Chandigarh", "timing": "Tue–Sat 10am–2pm", "contact": "+91-9910000022"},
                {"name": "Dr. Vikram Nair", "speciality": "Neurosurgery", "qualification": "MS, MCh (Neurosurgery) – AIIMS Delhi", "timing": "Thu–Fri 2pm–5pm", "contact": "+91-9910000023"}
            ]
        }
    ],
    "Bengaluru": [
        {
            "name": "Manipal Hospital (Old Airport Road)",
            "address": "98, HAL Airport Road, Bengaluru – 560017",
            "lat": 12.9576, "lon": 77.6428,
            "rating": 4.7,
            "specialities": ["Cardiology", "Orthopedics", "Nephrology", "Oncology", "Spine Surgery"],
            "emergency_no": "080-25024444", "ambulance_no": "080-25024400",
            "image_url": "https://images.unsplash.com/photo-1551190822-a9333d879b1f?w=800&q=80",
            "about": "600-bed multi-specialty hospital with Level 1 Trauma Centre, internationally trained surgeons and cutting-edge medical technology.",
            "rooms": {"General": 1800, "SemiPrivate": 4000, "Private": 7500, "ICU": 16000},
            "treatments": ["Total Joint Replacement", "Spine Surgery", "Renal Transplant", "Coronary Bypass", "Minimally Invasive Surgery"],
            "ambulance": True,
            "beds": 600,
            "doctors": [
                {"name": "Dr. Rajeev Sood", "speciality": "Orthopedic Surgery", "qualification": "MS (Ortho) – Kasturba Medical College", "timing": "Mon–Fri 9am–1pm", "contact": "+91-9845000031"},
                {"name": "Dr. Kavitha Reddy", "speciality": "Cardiology", "qualification": "MD, DM – Sri Jayadeva Institute", "timing": "Mon–Sat 11am–3pm", "contact": "+91-9845000032"}
            ]
        }
    ],
    "Nagpur": [
        {
            "name": "Kingsway Hospital",
            "address": "68, Kingsway Road, Nagpur – 440001",
            "lat": 21.1458, "lon": 79.0882,
            "rating": 4.5,
            "specialities": ["General Medicine", "Orthopedics", "Cardiology", "Pediatrics", "Gynecology"],
            "emergency_no": "0712-2524444", "ambulance_no": "0712-2524400",
            "image_url": "https://images.unsplash.com/photo-1516841273335-e39b37888115?w=800&q=80",
            "about": "Leading multi-specialty hospital in central India with 450+ beds and a dedicated trauma care unit serving Vidarbha region.",
            "rooms": {"General": 1200, "SemiPrivate": 2800, "Private": 5500, "ICU": 12000},
            "treatments": ["Cardiac Angioplasty", "Joint Replacement", "Normal & C-Section Delivery", "Paediatric Surgery", "Laparoscopic Procedures"],
            "ambulance": True,
            "beds": 450,
            "doctors": [
                {"name": "Dr. Abhijit Deshmukh", "speciality": "Cardiology", "qualification": "MD, DM (Cardiology) – Nagpur University", "timing": "Mon–Sat 10am–1pm", "contact": "+91-9890000041"},
                {"name": "Dr. Preeti Shende", "speciality": "Gynecology", "qualification": "MS (Obs & Gynae) – NKP Salve Medical College", "timing": "Mon–Fri 9am–12pm", "contact": "+91-9890000042"},
                {"name": "Dr. Nishant Bakde", "speciality": "Orthopedics", "qualification": "MS (Ortho) – GMCH Nagpur", "timing": "Tue–Sat 4pm–7pm", "contact": "+91-9890000043"}
            ]
        },
        {
            "name": "Orange City Hospital & Research Institute",
            "address": "Wadi, Nagpur – 440023",
            "lat": 21.0867, "lon": 79.0495,
            "rating": 4.6,
            "specialities": ["Oncology", "Neurology", "Urology", "Nephrology", "Dermatology"],
            "emergency_no": "0712-6630000", "ambulance_no": "0712-6630099",
            "image_url": "https://images.unsplash.com/photo-1632833239869-a37e3a5806d2?w=800&q=80",
            "about": "NABH-accredited 500-bed hospital with advanced cancer care, robotic-assisted surgery and 24×7 emergency & trauma services.",
            "rooms": {"General": 1500, "SemiPrivate": 3500, "Private": 6500, "ICU": 14000},
            "treatments": ["Robotic Prostatectomy", "Chemotherapy", "Neuro Endovascular", "Dialysis", "PET-CT Guided Biopsy"],
            "ambulance": True,
            "beds": 500,
            "doctors": [
                {"name": "Dr. Sudhir Paunikar", "speciality": "Oncology", "qualification": "MD, DM – Tata Memorial Centre", "timing": "Mon–Fri 10am–2pm", "contact": "+91-9860000051"},
                {"name": "Dr. Archana Wankhede", "speciality": "Neurology", "qualification": "MD, DM (Neurology) – AIIMS Nagpur", "timing": "Mon–Sat 9am–12pm", "contact": "+91-9860000052"}
            ]
        }
    ],
    "Chennai": [
        {
            "name": "Apollo Hospitals (Greams Road)",
            "address": "21, Greams Lane, Off Greams Road, Chennai – 600006",
            "lat": 13.0569, "lon": 80.2409,
            "rating": 4.8,
            "specialities": ["Cardiology", "Oncology", "Transplant", "Neurology", "Orthopedics"],
            "emergency_no": "044-28290200", "ambulance_no": "1066",
            "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
            "about": "Asia's first JCI-accredited hospital with 700 beds. Pioneer in cardiac and organ transplant surgeries with internationally trained faculty.",
            "rooms": {"General": 2200, "SemiPrivate": 4800, "Private": 9500, "ICU": 20000},
            "treatments": ["Heart Transplant", "Liver Transplant", "Stem Cell Therapy", "IMRT Cancer Treatment", "Spinal Fusion"],
            "ambulance": True,
            "beds": 700,
            "doctors": [
                {"name": "Dr. K. Harishkumar", "speciality": "Cardiac Surgery", "qualification": "MS, MCh – JIPMER Puducherry", "timing": "Mon–Fri 9am–1pm", "contact": "+91-9444000061"},
                {"name": "Dr. Malathi Srinivasan", "speciality": "Oncology", "qualification": "MD, DM – Adyar Cancer Institute", "timing": "Tue–Sat 10am–2pm", "contact": "+91-9444000062"}
            ]
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
                st.image(h['image_url'], use_container_width=True)
                
            with col_info:
                st.markdown(f"<h2>🏥 {h['name']}</h2>", unsafe_allow_html=True)
                st.markdown(f"📍 {h['address']}")
                st.markdown(f"**Rating:** ⭐ <span style='color: #d97706; font-weight: bold;'>{h['rating']}/5</span>", unsafe_allow_html=True)
                
                specs_html = " ".join([f"<span style='background:#dbeafe; color:#1e40af; padding:4px 10px; border-radius:20px; font-size:14px; font-weight:600; margin-right:5px;'>{s}</span>" for s in h["specialities"]])
                st.markdown(f"<div style='margin-top:10px; margin-bottom:15px;'>{specs_html}</div>", unsafe_allow_html=True)
                
                tabs = st.tabs(["Overview", "Doctors", "Rooms", "Treatments", "Contact"])
                
                with tabs[0]:
                    st.write(f"**About:** {h['about']}")
                    st.write(f"**🛏️ Total Beds:** {h['beds']}")
                
                with tabs[1]:
                    for doc in h["doctors"]:
                        st.info(f"**👨‍⚕️ {doc['name']}** \n🩺 {doc['speciality']} | 🎓 {doc['qualification']}  \n🕐 {doc['timing']} | 📞 {doc['contact']}")
                
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
    st.markdown(f"*Visual insights into hospital data across {selectedCity}*")
    
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
                radar_data.append({"hospital": h["name"][:15], "metric": "Beds/100", "value": h["beds"]/100})
            
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
            
        st_folium(m, width=1200, height=600)
        
        st.markdown("### 📍 Locations")
        cols = st.columns(2)
        for i, h in enumerate(filtered_hospitals):
            with cols[i % 2]:
                st.markdown(f"""
                <div class='stat-card' style='margin-bottom: 10px;'>
                    <h4>{h['name']}</h4>
                    <p>📍 {h['address']}<br>
                    ⭐ {h['rating']}/5 | 🛏️ {h['beds']} beds<br>
                    <b>Coordinates:</b> {h['lat']:.4f}, {h['lon']:.4f}</p>
                    <a href='https://www.google.com/maps?q=${h['lat']},{h['lon']}' target='_blank'>🗺️ Open in Google Maps</a>
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
    
    with st.form("appointment_form"):
        st.subheader("📝 Appointment Request Form")
        
        c1, c2 = st.columns(2)
        hosp_names = [h["name"] for h in filtered_hospitals]
        selected_hosp = c1.selectbox("Select Hospital *", ["Choose a hospital..."] + hosp_names)
        
        doc_list = ["Choose a doctor..."]
        if selected_hosp != "Choose a hospital...":
            hdata = next((item for item in filtered_hospitals if item["name"] == selected_hosp), None)
            if hdata:
                doc_list += [f"{d['name']} – {d['speciality']}" for d in hdata["doctors"]]
                
        selected_doc = c2.selectbox("Select Doctor *", doc_list)
        
        c3, c4 = st.columns(2)
        name = c3.text_input("Patient Name *", placeholder="Enter full name")
        age = c4.number_input("Age", min_value=0, max_value=120, step=1)
        
        c5, c6 = st.columns(2)
        phone = c5.text_input("Mobile Number *", placeholder="+91-XXXXXXXXXX")
        email = c6.text_input("Email (optional)", placeholder="email@example.com")
        
        c7, c8 = st.columns(2)
        gender = c7.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
        date = c8.date_input("Preferred Date")
        
        symptoms = st.text_area("Reason for Visit / Symptoms", placeholder="Describe your symptoms or reason for consultation...")
        
        submitted = st.form_submit_button("✅ Request Appointment", type="primary", use_container_width=True)
        
        if submitted:
            if name and phone and selected_hosp != "Choose a hospital..." and selected_doc != "Choose a doctor...":
                st.success(f"Appointment request submitted successfully for {name} with {selected_doc} at {selected_hosp} on {date}.")
            else:
                st.error("Please fill all required fields (*).")

    st.markdown("### 🕐 All Doctor Timings")
    for h in filtered_hospitals:
        with st.expander(f"🏥 {h['name']}"):
            for doc in h["doctors"]:
                st.info(f"**{doc['name']}** (🩺 {doc['speciality']} | 🎓 {doc['qualification']})\n\n🕐 {doc['timing']} | 📞 {doc['contact']}")

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
