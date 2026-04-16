import streamlit as st
import pandas as pd
import numpy as np
import random
import math
import plotly.express as px
import folium
from streamlit_folium import st_folium

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="MediFind India",
    page_icon="🏥",
    layout="wide"
)

# -------------------------
# METRO HOSPITAL DATA
# -------------------------

CITIES = {

"Nagpur": [
"Kingsway Hospital",
"Orange City Hospital",
"Alexis Multispeciality Hospital",
"Wockhardt Hospital Nagpur",
"SevenStar Hospital"
],

"Mumbai": [
"Kokilaben Hospital",
"Lilavati Hospital",
"Nanavati Hospital",
"Jaslok Hospital",
"Fortis Mulund"
],

"Delhi": [
"AIIMS Delhi",
"Max Hospital",
"Apollo Delhi",
"Safdarjung Hospital",
"Ganga Ram Hospital"
],

"Bengaluru": [
"Manipal Hospital",
"Apollo Bengaluru",
"Narayana Health",
"Victoria Hospital",
"Sakra World Hospital"
],

"Chennai": [
"Apollo Chennai",
"MIOT Hospital",
"Kauvery Hospital",
"SIMS Hospital",
"Fortis Malar"
]

}

SPECIALITIES = [
"General Medicine",
"Surgery",
"Pediatrics",
"Gynecology",
"Orthopedics",
"Cardiology",
"Neurology",
"Dermatology",
"Dentistry",
"Physiotherapy"
]

DOCTOR_NAMES = [
"Dr. Amit Sharma",
"Dr. Priya Mehta",
"Dr. Rajesh Gupta",
"Dr. Neha Kulkarni",
"Dr. Rohit Verma",
"Dr. Sneha Patil",
"Dr. Rahul Joshi",
"Dr. Meena Iyer"
]

SCHEMES = [
"Ayushman Bharat",
"CGHS",
"ESIC"
]

# -------------------------
# GENERATE HOSPITAL DATA
# -------------------------

def generate_hospital(city, name):

    beds = random.randint(200, 800)

    hospital = {

        "name": name,

        "type":
        "Government"
        if "Hospital" in name
        else "Private",

        "address":
        f"Main Road, {city}",

        "lat":
        round(random.uniform(18, 28), 4),

        "lon":
        round(random.uniform(72, 88), 4),

        "rating":
        round(random.uniform(4.0, 4.9), 1),

        "beds": beds,

        "vacant_beds":
        random.randint(20, beds//2),

        "specialities":
        random.sample(
            SPECIALITIES,
            6
        ),

        "schemes":
        random.sample(
            SCHEMES,
            2
        ),

        "patient_stats": {

            "monthly":
            [random.randint(2000,5000)
             for _ in range(6)]

        },

        "doctors": [

            {

                "name":
                random.choice(
                    DOCTOR_NAMES
                ),

                "speciality":
                random.choice(
                    SPECIALITIES
                ),

                "timing":
                "Mon–Sat 9am–2pm",

                "contact":
                f"+91-98{random.randint(10000000,99999999)}"

            }

            for _ in range(6)

        ]

    }

    return hospital


# Build dataset
HOSPITALS = {}

for city, names in CITIES.items():

    HOSPITALS[city] = [

        generate_hospital(
            city,
            name
        )

        for name in names

    ]


# -------------------------
# LIVE BED SIMULATION
# -------------------------

def update_beds():

    for city in HOSPITALS:

        for h in HOSPITALS[city]:

            h["vacant_beds"] = random.randint(
                10,
                h["beds"]//2
            )

update_beds()


# -------------------------
# DISTANCE FUNCTION
# -------------------------

def calculate_distance(
lat1, lon1,
lat2, lon2):

    R = 6371

    d_lat = math.radians(lat2-lat1)
    d_lon = math.radians(lon2-lon1)

    a = (
        math.sin(d_lat/2)**2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(d_lon/2)**2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1-a)
    )

    return R * c


# -------------------------
# RANKING FUNCTION
# -------------------------

def calculate_score(h):

    rating_score = h["rating"] * 20

    bed_score = (
        h["vacant_beds"]
        / h["beds"]
    ) * 100

    doctor_score = len(
        h["doctors"]
    ) * 5

    speciality_score = len(
        h["specialities"]
    ) * 3

    return round(

        rating_score +
        bed_score +
        doctor_score +
        speciality_score,

        2

    )


# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    st.title("🏥 MediFind")

    selected_city = st.selectbox(
        "Select City",
        list(HOSPITALS.keys())
    )

    hospital_type = st.selectbox(
        "Hospital Type",
        ["All","Government","Private"]
    )

    speciality_filter = st.selectbox(
        "Speciality",
        ["All"] + SPECIALITIES
    )

    page = st.radio(

        "Navigation",

        [

        "🏥 Hospitals",

        "📍 Nearest",

        "🏆 Rankings",

        "📊 Analytics",

        "🗺️ Map",

        "📅 Appointment"

        ]

    )

# -------------------------
# FILTER DATA
# -------------------------

filtered = []

for h in HOSPITALS[selected_city]:

    if hospital_type != "All":

        if h["type"] != hospital_type:
            continue

    if speciality_filter != "All":

        if speciality_filter not in h["specialities"]:
            continue

    filtered.append(h)


# -------------------------
# PAGE 1 — HOSPITALS
# -------------------------

if page == "🏥 Hospitals":

    st.title("🏥 Hospitals")

    for h in filtered:

        with st.container():

            st.subheader(h["name"])

            col1,col2,col3 = st.columns(3)

            col1.metric(
                "⭐ Rating",
                h["rating"]
            )

            col2.metric(
                "🛏️ Vacant Beds",
                h["vacant_beds"]
            )

            col3.metric(
                "🏥 Total Beds",
                h["beds"]
            )

            st.write("📍",h["address"])

            st.write(
                "🩺 Specialities:",
                ", ".join(
                    h["specialities"]
                )
            )

            st.write(
                "🏥 Schemes:",
                ", ".join(
                    h["schemes"]
                )
            )

            with st.expander("👨‍⚕️ Doctors"):

                for doc in h["doctors"]:

                    st.write(
                        doc["name"],
                        "-",
                        doc["speciality"]
                    )


# -------------------------
# PAGE 2 — NEAREST
# -------------------------

elif page == "📍 Nearest":

    st.title("📍 Nearest Hospitals")

    user_lat = st.number_input(
        "Latitude",
        value=21.1458
    )

    user_lon = st.number_input(
        "Longitude",
        value=79.0882
    )

    distances = []

    for h in filtered:

        d = calculate_distance(
            user_lat,
            user_lon,
            h["lat"],
            h["lon"]
        )

        distances.append((h,d))

    distances.sort(
        key=lambda x:x[1]
    )

    for h,d in distances[:5]:

        st.write(

            h["name"],
            " — ",
            round(d,2),
            "km"

        )


# -------------------------
# PAGE 3 — RANKINGS
# -------------------------

elif page == "🏆 Rankings":

    st.title("🏆 Hospital Rankings")

    ranked = []

    for h in filtered:

        score = calculate_score(h)

        ranked.append(
            (h,score)
        )

    ranked.sort(
        key=lambda x:x[1],
        reverse=True
    )

    rank_data=[]

    for i,(h,s) in enumerate(ranked):

        rank_data.append({

            "Rank":i+1,
            "Hospital":h["name"],
            "Score":s

        })

    df = pd.DataFrame(rank_data)

    st.dataframe(df)

    fig = px.bar(
        df,
        x="Hospital",
        y="Score",
        color="Score"
    )

    st.plotly_chart(fig)


# -------------------------
# PAGE 4 — ANALYTICS
# -------------------------

elif page == "📊 Analytics":

    st.title("📊 Patient Analytics")

    for h in filtered:

        monthly = h["patient_stats"]["monthly"]

        fig = px.line(

            y=monthly,

            title=h["name"]

        )

        st.plotly_chart(fig)


# -------------------------
# PAGE 5 — MAP
# -------------------------

elif page == "🗺️ Map":

    st.title("🗺️ Hospital Map")

    m = folium.Map(
        location=[21.1458,79.0882],
        zoom_start=5
    )

    for h in filtered:

        folium.Marker(

            [h["lat"],h["lon"]],

            popup=h["name"]

        ).add_to(m)

    st_folium(
        m,
        width=900,
        height=500
    )


# -------------------------
# PAGE 6 — APPOINTMENT
# -------------------------

elif page == "📅 Appointment":

    st.title("📅 Book Appointment")

    hospital_names = [
        h["name"]
        for h in filtered
    ]

    selected_hospital = st.selectbox(
        "Hospital",
        hospital_names
    )

    hospital = next(
        h for h in filtered
        if h["name"] ==
        selected_hospital
    )

    doctor_names = [

        doc["name"]
        for doc in hospital["doctors"]

    ]

    selected_doctor = st.selectbox(
        "Doctor",
        doctor_names
    )

    name = st.text_input(
        "Patient Name"
    )

    phone = st.text_input(
        "Phone Number"
    )

    date = st.date_input(
        "Date"
    )

    if st.button(
        "Book Appointment"
    ):

        if name and phone:

            st.success(
                f"Appointment booked with {selected_doctor}"
            )

        else:

            st.error(
                "Enter required details"
            )
