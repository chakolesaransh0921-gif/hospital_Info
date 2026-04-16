# ===============================
# MEDIFIND PRO — PREMIUM HOSPITAL FINDER
# ===============================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
import folium
from streamlit_folium import st_folium
import pydeck as pdk
from faker import Faker
from geopy.distance import geodesic

fake = Faker("en_IN")

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="MediFind Pro",
    page_icon="🏥",
    layout="wide"
)

# ===============================
# PREMIUM CSS
# ===============================

st.markdown("""
<style>

.main {
    background: linear-gradient(to right,#eef2ff,#f8fafc);
}

.hero {
    background: linear-gradient(135deg,#1e3a8a,#2563eb);
    padding:35px;
    border-radius:18px;
    color:white;
    margin-bottom:25px;
}

.card {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 6px 18px rgba(0,0,0,0.08);
    margin-bottom:15px;
}

.badge {
    background:#dbeafe;
    color:#1e40af;
    padding:4px 10px;
    border-radius:12px;
    margin:2px;
    font-size:12px;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# REAL MAJOR METRO DATA
# ===============================

cities_data = {

"Mumbai":[
("Kokilaben Dhirubhai Ambani Hospital",19.1197,72.8346),
("Lilavati Hospital",19.0596,72.8295),
("Nanavati Max Hospital",19.0988,72.8402)
],

"Delhi":[
("AIIMS Delhi",28.5672,77.2100),
("Max Super Speciality Hospital",28.5675,77.2105),
("Fortis Escorts Heart Institute",28.5601,77.2732)
],

"Bengaluru":[
("Manipal Hospital",12.9576,77.6428),
("Apollo Hospital Bannerghatta",12.8950,77.5960),
("Fortis Hospital Bannerghatta",12.8962,77.5971)
],

"Chennai":[
("Apollo Hospitals Greams Road",13.0569,80.2409),
("Fortis Malar Hospital",13.0400,80.2500),
("MIOT International Hospital",13.0250,80.2000)
],

"Hyderabad":[
("Apollo Hospitals Jubilee Hills",17.4176,78.4347),
("Yashoda Hospital",17.4300,78.4100),
("Care Hospital",17.4250,78.4500)
],

"Pune":[
("Ruby Hall Clinic",18.5362,73.8767),
("Jehangir Hospital",18.5308,73.8797),
("Sahyadri Hospital",18.5000,73.8600)
],

"Nagpur":[
("Kingsway Hospital",21.1458,79.0882),
("Orange City Hospital",21.0867,79.0495),
("Wockhardt Hospital",21.1250,79.0900)
]

}

specialities = [
"Cardiology",
"Orthopedics",
"Neurology",
"Pediatrics",
"Oncology",
"Dermatology"
]

# ===============================
# BUILD HOSPITAL DATA
# ===============================

hospital_list = []

for city, hospitals in cities_data.items():

    for name,lat,lon in hospitals:

        doctors=[]

        for i in range(3):
            doctors.append({
                "name":fake.name(),
                "speciality":random.choice(specialities),
                "experience":random.randint(5,25)
            })

        hospital_list.append({

            "city":city,
            "name":name,
            "lat":lat,
            "lon":lon,
            "rating":round(random.uniform(4.0,4.9),1),
            "beds_total":random.randint(200,900),
            "beds_available":random.randint(20,200),
            "specialities":random.sample(specialities,3),
            "doctors":doctors

        })

df = pd.DataFrame(hospital_list)

# ===============================
# SIDEBAR
# ===============================

with st.sidebar:

    st.title("🏥 MediFind Pro")

    city = st.selectbox(
        "Select City",
        sorted(df["city"].unique())
    )

    speciality_filter = st.selectbox(
        "Filter Speciality",
        ["All"]+specialities
    )

    rating_filter = st.slider(
        "Minimum Rating",
        4.0,
        5.0,
        4.0
    )

    page = st.radio(
        "Navigation",
        [
        "🏥 Hospital Finder",
        "📊 Dashboard",
        "🗺️ Map",
        "🚨 Emergency"
        ]
    )

# ===============================
# FILTER DATA
# ===============================

filtered_df = df[df["city"]==city]

if speciality_filter!="All":

    filtered_df = filtered_df[
        filtered_df["specialities"].apply(
            lambda x: speciality_filter in x
        )
    ]

filtered_df = filtered_df[
    filtered_df["rating"]>=rating_filter
]

# ===============================
# PAGE 1 — HOSPITAL FINDER
# ===============================

if page=="🏥 Hospital Finder":

    st.markdown(f"""
    <div class='hero'>
    <h1>🏥 MediFind Pro — {city}</h1>
    <p>Find top hospitals with live availability</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics

    col1,col2,col3=st.columns(3)

    col1.metric(
        "Hospitals",
        len(filtered_df)
    )

    col2.metric(
        "Total Beds",
        int(filtered_df["beds_total"].sum())
    )

    col3.metric(
        "Available Beds",
        int(filtered_df["beds_available"].sum())
    )

    st.divider()

    # Hospital Cards

    for i,row in filtered_df.iterrows():

        with st.container():

            st.markdown(f"""
            <div class='card'>
            <h3>🏥 {row['name']}</h3>
            ⭐ {row['rating']}/5
            <br>
            🛏️ Available Beds:
            {row['beds_available']} / {row['beds_total']}
            <br>
            {" ".join([f"<span class='badge'>{s}</span>" for s in row['specialities']])}
            </div>
            """, unsafe_allow_html=True)

            tab1,tab2=st.tabs(
                ["👨‍⚕️ Doctors","📊 Bed Availability"]
            )

            with tab1:

                for d in row["doctors"]:

                    st.write(
                        f"👨‍⚕️ {d['name']} — {d['speciality']} ({d['experience']} yrs)"
                    )

            with tab2:

                beds=row["beds_available"]
                used=row["beds_total"]-beds

                pie_df=pd.DataFrame({
                    "Status":["Available","Occupied"],
                    "Beds":[beds,used]
                })

                fig=px.pie(
                    pie_df,
                    values="Beds",
                    names="Status",
                    title="Bed Status"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

# ===============================
# PAGE 2 — DASHBOARD
# ===============================

elif page=="📊 Dashboard":

    st.title("📊 Analytics Dashboard")

    fig1=px.bar(
        filtered_df,
        x="name",
        y="rating",
        title="Hospital Ratings"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2=px.scatter(
        filtered_df,
        x="beds_total",
        y="beds_available",
        size="rating",
        hover_name="name",
        title="Beds vs Availability"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ===============================
# PAGE 3 — MAP
# ===============================

elif page=="🗺️ Map":

    st.title("🗺️ Hospital Map")

    center_lat=filtered_df["lat"].mean()
    center_lon=filtered_df["lon"].mean()

    m=folium.Map(
        location=[center_lat,center_lon],
        zoom_start=12
    )

    for _,row in filtered_df.iterrows():

        folium.Marker(
            [row["lat"],row["lon"]],
            popup=row["name"]
        ).add_to(m)

    st_folium(
        m,
        width=1000,
        height=500
    )

# ===============================
# PAGE 4 — EMERGENCY
# ===============================

elif page=="🚨 Emergency":

    st.error(
        "🚨 In case of emergency call 112 immediately"
    )

    st.markdown("### 🚑 Emergency Numbers")

    st.write("🚑 Ambulance — 108")
    st.write("🚓 Police — 100")
    st.write("🚒 Fire — 101")

# ===============================
# NEAREST HOSPITAL FINDER
# ===============================

st.sidebar.markdown("---")

st.sidebar.subheader(
"📍 Nearest Hospital Finder"
)

user_lat=st.sidebar.number_input(
"Your Latitude",
value=21.1458
)

user_lon=st.sidebar.number_input(
"Your Longitude",
value=79.0882
)

if st.sidebar.button("Find Nearest"):

    distances=[]

    for _,row in filtered_df.iterrows():

        dist=geodesic(
            (user_lat,user_lon),
            (row["lat"],row["lon"])
        ).km

        distances.append(dist)

    filtered_df["distance_km"]=distances

    nearest=filtered_df.sort_values(
        "distance_km"
    ).iloc[0]

    st.sidebar.success(
        f"Nearest: {nearest['name']} ({nearest['distance_km']:.2f} km)"
    )
