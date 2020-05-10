import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.title("Plotting Charts with Plotly in Streamlit....")
encounter = pd.read_csv(
    "https://raw.githubusercontent.com/vedashree29296/healthcare-eda/master/consolidated.csv"
)
# I - How has the year wise trend been with the Insurance companies ?
encounter.head()

st.header("HOW MANY CASES DID EACH PAYER HANDLE IN EACH YEAR?")
st.subheader("I - How has the year wise trend been with the Insurance companies ?")

with st.echo():
    counts = encounter.groupby(["PAYER_NAME", "YEAR"]).count().reset_index()
    fig = px.bar(counts, x="PAYER_NAME", y="Id", animation_frame="YEAR")
    st.plotly_chart(fig)

with st.echo():
    counts = encounter.groupby(["YEAR", "PAYER_NAME"]).count().reset_index()
    fig = px.bar(counts, x="YEAR", y="Id", color="PAYER_NAME", barmode="group")
    st.plotly_chart(fig)

df = encounter[encounter["ORG_NAME"] == "HALLMARK HEALTH SYSTEM"]

# group by year and payer name and take a count.
payer_distribution = df.groupby(["YEAR", "PAYER_NAME"]).count().reset_index()
fig = px.bar(
    payer_distribution,
    x="YEAR",
    y="Id",
    hover_data=["PAYER_NAME"],
    labels={"Id": "num_visits"},
)
st.plotly_chart(fig)

st.header("COMMON REASONS FOR VISITS EVERY YEAR")
st.subheader("Why did patients visit hallmark every year?")
with st.echo():
    cols = 1
    rows = len(range(df["YEAR"].min(), df["YEAR"].max() + 1))
    specs = [[{"type": "pie"}] for i in range(rows)]
    column_widths = [0.9]
    fig = make_subplots(rows=rows, cols=cols, specs=specs, column_widths=column_widths)
    row = 1
    # first group by year and then for each group we're going to take the value counts for the reason
    for year, group in df.groupby(["YEAR"]):
        counts = group["REASON"].value_counts()
        fig.append_trace(
            go.Pie(
                title=year, labels=counts.index, values=counts.values, textinfo="none"
            ),
            row=row,
            col=1,
        )
        row += 1
    fig.update_layout(height=4000, width=1000)
    st.plotly_chart(fig)

st.header("EXTRA: 3D DECK GL CHARTS")
df = pd.read_csv("data/patients.csv")
df = df[["LAT", "LON"]]
df = df.rename(columns={"LAT": "lat", "LON": "lon"})

st.deck_gl_chart(
    viewport={
        "latitude": df["lat"].mean(),
        "longitude": df.lon.mean(),
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        {
            "type": "HexagonLayer",
            "data": df,
            "radius": 200,
            "elevationScale": 5,
            "elevationRange": [0, 1000],
            "pickable": True,
            "extruded": True,
        },
        {"type": "ScatterplotLayer", "data": df},
    ],
)
