import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# KONFIGURASI HALAMAN
# -------------------------
st.set_page_config(
    page_title="NYC Taxi Big Data Dashboard",
    layout="wide"
)

st.title("🚖 NYC Yellow Taxi Big Data Analytics Dashboard")
st.caption(
    "Analisis Big Data menggunakan Hadoop & MapReduce, "
    "dengan visualisasi interaktif berbasis Streamlit"
)

st.markdown("---")

# -------------------------
# LOAD DATA
# -------------------------
try:
    df_raw = pd.read_csv(
        "hasil_full.csv",
        sep=";",
        names=["Key", "Val"]
    )

    # -------------------------
    # PREPROCESSING DATA
    # -------------------------

    # 1️⃣ INSIGHT WAKTU (T_HOUR)
    df_hour = df_raw[df_raw["Key"].str.contains("T_HOUR")].copy()
    df_hour["Jam"] = df_hour["Key"].str.replace("T_HOUR_", "").astype(int)
    df_hour = df_hour.sort_values("Jam")

    # 2️⃣ INSIGHT SPASIAL (S_PICKUP)
    df_geo = df_raw[df_raw["Key"].str.contains("S_PICKUP")].copy()
    df_geo[["Lat", "Lon"]] = (
        df_geo["Key"]
        .str.replace("S_PICKUP_", "")
        .str.split(",", expand=True)
    )
    df_geo["Lat"] = pd.to_numeric(df_geo["Lat"])
    df_geo["Lon"] = pd.to_numeric(df_geo["Lon"])

    # 3️⃣ INSIGHT KINERJA (P_SPEED)
    df_speed = df_raw[df_raw["Key"].str.contains("P_SPEED")].copy()
    df_speed["Jam"] = df_speed["Key"].str.replace("P_SPEED_", "").astype(int)
    df_speed = df_speed.sort_values("Jam")

    # -------------------------
    # TABS DASHBOARD
    # -------------------------
    tab1, tab2, tab3 = st.tabs([
        "📊 Pola Permintaan Waktu",
        "📍 Hotspot Lokasi Pickup",
        "🚦 Kinerja Perjalanan"
    ])

    # =====================================================
    # TAB 1 — POLA WAKTU
    # =====================================================
    with tab1:
        st.header("Pola Permintaan Berdasarkan Waktu")

        fig_time = px.line(
            df_hour,
            x="Jam",
            y="Val",
            markers=True,
            title="Jumlah Perjalanan per Jam"
        )
        fig_time.update_layout(
            xaxis_title="Jam",
            yaxis_title="Jumlah Trip"
        )

        st.plotly_chart(fig_time, use_container_width=True)

        peak_hour = df_hour.loc[df_hour["Val"].idxmax(), "Jam"]
        peak_value = df_hour["Val"].max()

        st.success(
            f"📌 **Jam tersibuk terjadi pada pukul {peak_hour}:00** "
            f"dengan total {peak_value:,} perjalanan."
        )

        st.markdown(
            """
            **Insight:**  
            Terlihat pola permintaan yang meningkat pada jam-jam tertentu, 
            yang umumnya berkaitan dengan jam berangkat dan pulang kerja.
            """
        )

    # =====================================================
    # TAB 2 — HOTSPOT LOKASI
    # =====================================================
    with tab2:
        st.header("Hotspot Lokasi Pickup Taksi")

        fig_density = px.density_mapbox(
            df_geo,
            lat="Lat",
            lon="Lon",
            z="Val",
            radius=25,
            center=dict(lat=40.73, lon=-73.93),
            zoom=10,
            mapbox_style="carto-positron",
            title="Kepadatan Lokasi Pickup Taksi (Density Map)"
        )

        st.plotly_chart(fig_density, use_container_width=True)

        st.info(
            "Area dengan intensitas warna lebih terang menunjukkan "
            "lokasi dengan konsentrasi pickup yang tinggi, "
            "yang mengindikasikan hotspot aktivitas taksi."
        )

        st.markdown(
            """
            **Insight:**  
            Hotspot pickup cenderung terkonsentrasi di pusat aktivitas kota,
            seperti area bisnis dan transportasi utama.
            """
        )

    # =====================================================
    # TAB 3 — KINERJA PERJALANAN
    # =====================================================
    with tab3:
        st.header("Kinerja Perjalanan & Indikasi Kemacetan")

        fig_speed = px.line(
            df_speed,
            x="Jam",
            y="Val",
            markers=True,
            title="Kecepatan Rata-rata per Jam (Speed Proxy)"
        )
        fig_speed.update_layout(
            xaxis_title="Jam",
            yaxis_title="Kecepatan (mph)"
        )

        st.plotly_chart(fig_speed, use_container_width=True)

        slowest_hour = df_speed.loc[df_speed["Val"].idxmin(), "Jam"]
        slowest_speed = df_speed["Val"].min()

        st.warning(
            f"🚦 **Kemacetan tertinggi terjadi pada pukul {slowest_hour}:00** "
            f"dengan kecepatan rata-rata {slowest_speed:.2f} mph."
        )

        st.markdown(
            """
            **Insight:**  
            Penurunan kecepatan rata-rata pada jam sibuk mengindikasikan
            terjadinya kemacetan, yang berkorelasi dengan tingginya
            permintaan perjalanan.
            """
        )

    # -------------------------
    # FOOTER
    # -------------------------
    st.markdown("---")
    st.caption(
        "Dashboard ini menggunakan hasil pemrosesan Big Data berbasis "
        "Hadoop dan MapReduce sebagai fondasi analisis."
    )

except Exception as e:
    st.error("Terjadi kesalahan saat memuat data.")
    st.exception(e)
