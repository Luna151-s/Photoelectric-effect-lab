import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Planck's Constant Lab Manual Tool", page_icon="⚛️", layout="wide")

st.title("⚛️ Planck's Constant Lab Manual Assistant")
st.write("Enter experimental observations below to automate slope calculations, graphing, and percentage error.")

st.markdown("---")

c = 3.0e8          # Speed of light (m/s)
e = 1.602e-19      # Elementary charge (C)
h_actual = 6.626e-34 # Accepted h (J*s)

st.subheader("📋 Experimental Data Table")

default_data = pd.DataFrame({
    "Filter / Color": ["Ultraviolet", "Violet", "Blue", "Green", "Yellow"],
    "Wavelength λ (nm)": [365.0, 405.0, 436.0, 546.0, 577.0],
    "Stopping Voltage V₀ (V)": [1.52, 1.15, 0.92, 0.41, 0.28]
})

edited_df = st.data_editor(
    default_data, 
    num_rows="dynamic", 
    use_container_width=True,
    column_config={
        "Wavelength λ (nm)": st.column_config.NumberColumn(format="%.1f nm"),
        "Stopping Voltage V₀ (V)": st.column_config.NumberColumn(format="%.2f V")
    }
)

st.markdown("---")

if st.button("🚀 Calculate & Generate Graph"):
    # Clean data & drop missing/empty values
    df_clean = edited_df.dropna().copy()
    
    df_clean["Wavelength λ (nm)"] = pd.to_numeric(df_clean["Wavelength λ (nm)"], errors='coerce')
    df_clean["Stopping Voltage V₀ (V)"] = pd.to_numeric(df_clean["Stopping Voltage V₀ (V)"], errors='coerce')
    df_clean = df_clean.dropna()

    if len(df_clean) < 2:
        st.error("Please enter at least 2 valid data rows to fit a line.")
    else:
        wavelengths_nm = df_clean["Wavelength λ (nm)"].to_numpy(dtype=float)
        voltages = df_clean["Stopping Voltage V₀ (V)"].to_numpy(dtype=float)
        colors = df_clean["Filter / Color"].astype(str).to_list()
        
        # Calculate Frequency
        wavelengths_m = wavelengths_nm * 1e-9
        frequencies = c / wavelengths_m
        
        # Linear Regression
        slope, intercept = np.polyfit(frequencies, voltages, 1)
        h_exp = e * slope
        percentage_error = abs((h_exp - h_actual) / h_actual) * 100

        # Display Metrics
        st.subheader("📊 Output Results")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Calculated Slope (dV/dν)", value=f"{slope:.4e} V·s")
        m2.metric(label="Experimental Planck's Constant (h)", value=f"{h_exp:.4e} J·s")
        m3.metric(label="Percentage Error", value=f"{percentage_error:.2f}%")

        st.markdown("---")

        # Plot
        st.subheader("📈 Stopping Voltage (V₀) vs. Frequency (ν) Graph")
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(9, 5))
        
        ax.scatter(frequencies, voltages, color='#00FFC8', s=80, label='Lab Data Points', zorder=5)
        for i, txt in enumerate(colors):
            ax.annotate(f" {txt}", (frequencies[i], voltages[i]), fontsize=9, color='#00FFC8')
        
        freq_line = np.linspace(min(frequencies)*0.95, max(frequencies)*1.05, 100)
        voltage_line = slope * freq_line + intercept
        ax.plot(freq_line, voltage_line, color='#FF5733', linestyle='--', linewidth=2, label='Best-Fit Line')
        
        ax.set_xlabel("Frequency ν (Hz)", fontsize=11, color='white')
        ax.set_ylabel("Stopping Voltage V₀ (V)", fontsize=11, color='white')
        ax.set_title("Photoelectric Effect Graph", fontsize=13, color='white')
        ax.grid(True, linestyle=':', alpha=0.4)
        ax.legend()
        
        st.pyplot(fig)
