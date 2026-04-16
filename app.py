import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Page Config
st.set_page_config(page_title="MediFind", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

# --- DATASET ---
HOSPITALS = {
    "Mumbai": [
        {
            "name": "Kokilaben Dhirubhai Ambani Hospital",
            "address": "Four Bungalows, Andheri West, Mumbai – 400053",
            "lat": 19.1197, "lon": 72.8346,
            "rating": 4.8,
            "specialities": ["Cardiology", "Oncology", "Neurology", "Orthopedics", "Gastroenterology"],
            "emergency_no": "022-30999999", "ambulance_no": "022-30999911",
            "about": "NABH & JCI accredited 750-bed super-specialty hospital.",
            "rooms": {"General": 2500, "SemiPrivate": 5000, "Private": 9000, "ICU": 18000},
            "treatments": ["Robotic Surgery", "Bone Marrow Transplant", "CyberKnife"],
            "beds": 750,
            "doctors": [
                {"name": "Dr. Santosh Shetty", "speciality": "Cardiology", "timing": "Mon–Fri 10am–2pm", "contact": "+91-9820000001"},
                {"name": "Dr. Priya Mehta", "speciality": "Oncology", "timing": "Mon–Sat 9am–1pm", "contact": "+91-9820000002"}
            ]
        },
        {
            "name": "Lilavati Hospital & Research Centre",
            "address": "Bandra Reclamation, Bandra West, Mumbai – 400050",
            "lat": 19.0596, "lon": 72.8295,
            "rating": 4.6,
            "specialities": ["Nephrology", "Urology", "Dermatology", "Pediatrics", "Gynecology"],
            "emergency_no": "022-26751000", "ambulance_no": "022-26751099",
            "about": "Premier multi-specialty hospital with over 1,000 beds.",
            "rooms": {"General": 2000, "SemiPrivate": 4500, "Private": 8000, "ICU": 15000},
            "treatments": ["Kidney Transplant", "In-vitro Fertilisation", "Renal Dialysis"],
            "beds": 1000,
            "doctors": [
                {"name": "Dr. Sanjay Kulkarni", "speciality": "Nephrology", "timing": "Mon–Fri 11am–3pm", "contact": "+91-9870000011"}
            ]
        }
    ],
    "Pune": [
        {
            "name": "Ruby Hall Clinic",
            "address": "40, Sassoon Road, Pune – 411001",
            "lat": 18.5282, "lon": 73.8741,
            "rating": 4.7,
            "specialities": ["Cardiology", "Neurology", "Oncology", "Organ Transplant"],
            "emergency_no": "020-66455100", "ambulance_no": "020-66455200",
            "about": "One of Pune's oldest and most renowned multi-specialty hospitals.",
            "rooms": {"General": 1800, "SemiPrivate": 3500, "Private": 6000, "ICU": 14000},
            "treatments": ["Liver Transplant", "Cardiac Bypass", "Neuro Surgery"],
            "beds": 850,
            "doctors": [
                {"name": "Dr. P.K. Grant", "speciality": "Cardiology", "timing": "Mon–Fri 10am–1pm", "contact": "+91-9822000001"},
                {"name": "Dr. Sunil Agarwal", "speciality": "Neurology", "timing": "Tue–Sat 11am–3pm", "contact": "+91-9822000002"}
            ]
        }
    ],
    "Nagpur": [
        {
            "name": "Kingsway Hospital",
            "address": "68, Kingsway Road, Nagpur – 440001",
            "lat": 21.1458, "lon": 79.0882,
            "rating": 4.5,
            "specialities": ["General Medicine", "Orthopedics", "Cardiology", "Pediatrics"],
            "emergency_no": "0712-2524444", "ambulance_no": "0712-2524400",
            "about": "Leading multi-specialty hospital in central India.",
            "rooms": {"General": 1200, "SemiPrivate": 2800, "Private": 5500, "ICU": 12000},
            "treatments": ["Cardiac Angioplasty", "Joint Replacement", "Laparoscopic Procedures"],
            "beds": 450,
            "doctors": [
                {"name": "Dr. Abhijit Deshmukh", "speciality": "Cardiology", "timing": "Mon–Sat 10am–1pm", "contact": "+91-9890000041"}
            ]
        },
        {
            "name": "Orange City Hospital & Research Institute",
            "address": "Wadi, Nagpur – 440023",
            "lat": 21.0867, "lon": 79.0495,
            "rating": 4.6,
            "specialities": ["Oncology", "Neurology", "Urology", "Nephrology"],
            "emergency_no": "0712-6630000", "ambulance_no": "0712-6630099",
            "about": "NABH-accredited 500-bed hospital with advanced cancer care.",
            "rooms": {"General": 1500, "SemiPrivate": 3500, "Private": 6500, "ICU": 14000},
            "treatments": ["Robotic Prostatectomy", "Chemotherapy", "Dialysis"],
            "beds": 500,
            "doctors": [
                {"name": "Dr. Sudhir Paunikar", "speciality": "Oncology", "timing": "Mon–Fri 10am–2pm", "contact": "+91-9860000051"}
            ]
        }
    ],
    "Wardha": [
        {
            "name": "Acharya Vinoba Bhave Rural Hospital (AVBRH)",
            "address": "Sawangi (Meghe), Wardha – 442107",
            "lat": 20.7289, "lon": 78.5833,
            "rating": 4.3,
            "specialities": ["General Surgery", "Obstetrics", "Pediatrics", "Internal Medicine"],
            "emergency_no": "07152-287701", "ambulance_no": "07152-287702",
            "about": "1525-bed teaching hospital attached to JNMC providing comprehensive care.",
            "rooms": {"General": 500, "SemiPrivate": 1500, "Private": 3000, "ICU": 8000},
            "treatments": ["General Surgery", "Maternity Care", "Trauma Care"],
            "beds": 1525,
            "doctors": [
                {"name": "Dr. R. Singh", "speciality": "General Surgery", "timing": "Mon–Sat 9am–4pm", "contact": "+91-9422000011"}
            ]
        }
    ],
    "Delhi": [
        {
            "name": "AIIMS New Delhi",
            "address": "Sri Aurobindo Marg, Ansari Nagar, New Delhi – 110029",
            "lat": 28.5672, "lon": 77.2100,
            "rating": 4.9,
            "specialities": ["Cardiology", "Oncology", "Neurology", "Transplant Surgery"],
            "emergency_no": "011-26588500", "ambulance_no": "011-26588444",
            "about": "India's premier government medical institute.",
            "rooms": {"General": 500, "SemiPrivate": 2000, "Private": 5000, "ICU": 12000},
            "treatments": ["Multiorgan Transplant", "CAR-T Cell Therapy", "Deep Brain Stimulation"],
            "beds": 2000,
            "doctors": [
                {"name": "Dr. Anand Kumar", "speciality": "Cardiothoracic", "timing": "Mon–Wed 9am–1pm", "contact": "+91-9910000021"}
            ]
        }
    ],
    "Bengaluru": [
        {
            "name": "Manipal Hospital",
            "address": "HAL Airport Road, Bengaluru – 560017",
            "lat": 12.9576, "lon": 77.6428,
            "rating": 4.7,
            "specialities": ["Cardiology", "Orthopedics", "Nephrology", "Spine Surgery"],
            "emergency_no": "080-25024444", "ambulance_no": "080-25024400",
            "about": "600-bed multi-specialty hospital with Level 1 Trauma Centre.",
            "rooms": {"General": 1800, "SemiPrivate": 4000, "Private": 7500, "ICU": 16000},
            "treatments": ["Joint Replacement", "Spine Surgery", "Renal Transplant"],
            "beds": 600,
            "doctors": [
                {"name": "Dr. Rajeev Sood", "speciality": "Orthopedic Surgery", "timing": "Mon–Fri 9am–1pm", "contact": "+91-9845000031"}
            ]
        }
    ],
    "Chennai": [
        {
            "name": "Apollo Hospitals",
            "address": "Greams Road, Chennai – 600006",
            "lat": 13.0569, "lon": 80.2409,
            "rating": 4.8,
            "specialities": ["Cardiology", "Oncology", "Transplant", "Neurology"],
            "emergency_no": "044-28290200", "ambulance_no": "1066",
            "about": "Asia's first JCI-accredited hospital with 700 beds.",
            "rooms": {"General": 2200, "SemiPrivate": 4800, "Private": 9500, "ICU": 20000},
            "treatments": ["Heart Transplant", "Stem Cell Therapy", "IMRT Cancer Treatment"],
            "beds": 700,
            "doctors": [
                {"name": "Dr. K. Harishkumar", "speciality": "Cardiac Surgery", "timing": "Mon–Fri 9am–1pm", "contact": "+91-9444000061"}
            ]
        }
    ]
}

# --- SIDEBAR & STATE ---
st.sidebar.title("🏥 MediFind")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", ["Search", "Analytics", "Map", "Emergency", "Appointments", "About"])

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

cities = sorted(list(HOSPITALS.keys()))
selected_city = st.sidebar.selectbox("Select City", cities, index=cities.index("Nagpur") if "Nagpur" in cities else 0)

# Get all specialities for selected city
all_specs = set()
for h in HOSPITALS.get(selected_city, []):
    for s in h["specialities"]:
        all_specs.add(s)
all_specs = ["All"] + sorted(list(all_specs))

selected_spec = st.sidebar.selectbox("Speciality", all_specs)
min_rating = st.sidebar.slider("Minimum Rating ⭐", 1.0, 5.0, 4.0, 0.1)

# Filter Hospitals
filtered_hospitals = []
for h in HOSPITALS.get(selected_city, []):
    if h["rating"] >= min_rating and (selected_spec == "All" or selected_spec in h["specialities"]):
        filtered_hospitals.append(h)

# Emergency Quick Links in Sidebar
st.sidebar.markdown("---")
st.sidebar.error("🆘 **Emergency Calls**\n\n📞 **112** – Universal\n\n📞 **108** – Ambulance")


# --- PAGES ---

if page == "Search":
    st.title(f"🏥 Hospitals in {selected_city}")
    
    # Stats row
    col1, col2, col3 = st.columns(3)
    col1.metric("Hospitals Found", len(filtered_hospitals))
    col2.metric("Total Beds", sum(h["beds"] for h in filtered_hospitals))
    col3.metric("Avg Rating", round(sum(h["rating"] for h in filtered_hospitals)/len(filtered_hospitals), 1) if filtered_hospitals else 0)
    
    st.markdown("---")
    
    if not filtered_hospitals:
        st.warning("⚠️ No hospitals match your filters. Try adjusting your criteria.")
    else:
        for h in filtered_hospitals:
            st.subheader(f"{h['name']}")
            st.caption(f"📍 {h['address']} | ⭐ {h['rating']}/5")
            
            # Badges for specialities
            st.markdown("**Specialities:** " + ", ".join([f"`{s}`" for s in h["specialities"]]))
            
            # Expanders for details
            with st.expander("Show Details"):
                tabs = st.tabs(["Overview", "Doctors", "Rooms", "Emergency"])
                
                with tabs[0]:
                    st.write(f"**About:** {h['about']}")
                    st.write(f"**Total Beds:** {h['beds']}")
                    st.write("**Top Treatments:** " + ", ".join(h["treatments"]))
                
                with tabs[1]:
                    for doc in h["doctors"]:
                        st.markdown(f"**👨‍⚕️ {doc['name']}** ({doc['speciality']})  \n🕐 {doc['timing']} | 📞 {doc['contact']}")
                
                with tabs[2]:
                    st.table(pd.DataFrame([h["rooms"]]).T.rename(columns={0: "Charge (₹)"}))
                
                with tabs[3]:
                    st.error(f"📞 Emergency: **{h['emergency_no']}** \n🚑 Ambulance: **{h['ambulance_no']}**")
            st.markdown("---")

elif page == "Analytics":
    st.title("📊 Analytics Dashboard")
    if not filtered_hospitals:
        st.warning("No data to show based on current filters.")
    else:
        df = pd.DataFrame(filtered_hospitals)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⭐ Hospital Ratings")
            fig1 = px.bar(df, x="name", y="rating", color="rating", color_continuous_scale="Viridis", range_y=[0, 5])
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            st.subheader("🛏️ Bed Distribution")
            fig2 = px.pie(df, names="name", values="beds", hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)
            
        st.subheader("💰 Room Charges (ICU)")
        icu_data = [{"Name": h["name"], "ICU Charge": h["rooms"]["ICU"]} for h in filtered_hospitals]
        fig3 = px.line(pd.DataFrame(icu_data), x="Name", y="ICU Charge", markers=True)
        st.plotly_chart(fig3, use_container_width=True)
        
        st.subheader("📋 Hospital Data Table")
        display_df = df[["name", "rating", "beds", "emergency_no"]]
        st.dataframe(display_df, use_container_width=True)

elif page == "Map":
    st.title(f"🗺️ Hospital Map - {selected_city}")
    
    if not filtered_hospitals:
        st.warning("No hospitals to map.")
    else:
        # Calculate center
        avg_lat = sum(h["lat"] for h in filtered_hospitals) / len(filtered_hospitals)
        avg_lon = sum(h["lon"] for h in filtered_hospitals) / len(filtered_hospitals)
        
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
        
        for h in filtered_hospitals:
            popup_html = f"<b>{h['name']}</b><br>⭐ {h['rating']}<br>🛏️ {h['beds']} beds<br>📞 {h['emergency_no']}"
            folium.Marker(
                [h["lat"], h["lon"]], 
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=h["name"]
            ).add_to(m)
            
            # Service radius circle
            folium.Circle(
                [h["lat"], h["lon"]],
                radius=1000, # 1km radius
                color="blue",
                fill=True,
                fill_opacity=0.1
            ).add_to(m)
            
        st_folium(m, width=800, height=500)

elif page == "Emergency":
    st.title("🚨 Emergency Dashboard")
    st.error("⚠️ For life-threatening emergencies, call **112** immediately!")
    
    col1, col2, col3 = st.columns(3)
    col1.error("🚑 **National Ambulance**\n# 108")
    col2.warning("🚒 **Police / Fire**\n# 112")
    col3.success("🤱 **Maternal Ambulance**\n# 102")
    
    st.markdown("---")
    st.subheader(f"🏥 Direct Hospital Lines in {selected_city}")
    
    for h in filtered_hospitals:
        with st.container():
            st.markdown(f"### {h['name']}")
            c1, c2 = st.columns(2)
            c1.button(f"📞 Call Emergency: {h['emergency_no']}", key=f"e_{h['name']}")
            c2.button(f"🚑 Call Ambulance: {h['ambulance_no']}", key=f"a_{h['name']}")
            st.write("")

elif page == "Appointments":
    st.title("📅 Book Appointment")
    
    with st.form("appointment_form"):
        st.subheader("Patient Details")
        col1, col2 = st.columns(2)
        name = col1.text_input("Full Name *")
        phone = col2.text_input("Mobile Number *")
        
        st.subheader("Consultation Details")
        if not filtered_hospitals:
            st.error("Select a different city/filter.")
            hosp_list = []
        else:
            hosp_list = [h["name"] for h in filtered_hospitals]
            
        selected_hosp_name = st.selectbox("Select Hospital *", hosp_list)
        
        # Get doctors for selected hospital
        doc_list = []
        if selected_hosp_name:
            hosp_data = next((item for item in filtered_hospitals if item["name"] == selected_hosp_name), None)
            if hosp_data:
                doc_list = [f"{d['name']} ({d['speciality']})" for d in hosp_data["doctors"]]
                
        selected_doc = st.selectbox("Select Doctor *", doc_list)
        date = st.date_input("Preferred Date")
        symptoms = st.text_area("Reason for Visit / Symptoms")
        
        submitted = st.form_submit_button("✅ Request Appointment", use_container_width=True)
        if submitted:
            if name and phone and selected_hosp_name and selected_doc:
                st.success(f"Appointment request sent for {name} with {selected_doc} at {selected_hosp_name} on {date}.")
            else:
                st.error("Please fill all required fields (*)")

elif page == "About":
    st.title("ℹ️ About MediFind")
    st.write("Your trusted healthcare companion across India.")
    
    st.markdown("""
    ### Features
    * 🔍 Find top-rated multispecialty hospitals nearby
    * 👨‍⚕️ View doctor profiles and timings
    * 🛏️ Compare room charges and facilities
    * 🚑 Direct emergency connections
    
    ### Cities Covered
    """ + ", ".join(cities) + """
    
    ### Disclaimer
    This application provides information for guidance only. In a life-threatening emergency always call **112** immediately.
    """)
