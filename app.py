import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Page setup
st.set_page_config(page_title="Planck's Constant Lab Assistant", page_icon="⚛️", layout="wide")

st.title("⚛️ Planck's Constant Lab Assistant")
st.write("Enter your experimental observations to calculate slope, Planck's constant, percentage error, and display the graph.")

st.markdown("---")

# Constants
c = 3.0e8          # Speed of light (m/s)
e = 1.602e-19      # Elementary charge (C)
h_actual = 6.626e-34 # Accepted Planck's constant (J*s)

st.subheader("📋 Experimental Data Input")

# Editable Data Table
default_data = pd.DataFrame({
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
    # Clean data & remove empty rows
    df_clean = edited_df.dropna().copy()
    df_clean["Wavelength λ (nm)"] = pd.to_numeric(df_clean["Wavelength λ (nm)"], errors='coerce')
    df_clean["Stopping Voltage V₀ (V)"] = pd.to_numeric(df_clean["Stopping Voltage V₀ (V)"], errors='coerce')
    df_clean = df_clean.dropna()

    if len(df_clean) < 2:
        st.error("Please enter at least 2 valid data rows to calculate slope.")
    else:
        wavelengths = df_clean["Wavelength λ (nm)"].to_list()
        voltages = df_clean["Stopping Voltage V₀ (V)"].to_list()

        # Calculate Frequencies
        frequencies = [c / (w * 1e-9) for w in wavelengths]

        # --- ENDPOINT SLOPE METHOD (Matches your ~1.4% error logic) ---
        min_idx = wavelengths.index(min(wavelengths)) # Shortest wavelength -> Highest Frequency
        max_idx = wavelengths.index(max(wavelengths)) # Longest wavelength -> Lowest Frequency

        change_in_y = voltages[min_idx] - voltages[max_idx]
        change_in_x = frequencies[min_idx] - frequencies[max_idx]

        slope = change_in_y / change_in_x
        Experimental_h = slope * e
        percentage_error = (abs(Experimental_h - h_actual) / h_actual) * 100

        # Output Cards
        st.subheader("📊 Output Results")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="Calculated Slope", value=f"{slope:.4e} V·s")
        m2.metric(label="Experimental h", value=f"{Experimental_h:.4e} J·s")
        m3.metric(label="Actual h", value=f"{h_actual:.4e} J·s")
        m4.metric(label="Percentage Error", value=f"{percentage_error:.2f}%")

        st.markdown("---")

        # Plot Graph
        st.subheader("📈 Stopping Voltage (V₀) vs. Frequency (ν) Graph")
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(9, 5))

        # Data points
        ax.scatter(frequencies, voltages, color='#00FFC8', s=80, label='Lab Data Points', zorder=5)

        # Plot line passing through endpoint slope
        intercept = voltages[min_idx] - (slope * frequencies[min_idx])
        freq_line = np.linspace(min(frequencies) * 0.95, max(frequencies) * 1.05, 100)
        voltage_line = slope * freq_line + intercept

        ax.plot(freq_line, voltage_line, color='#FF5733', linestyle='--', linewidth=2, label='Endpoint Slope Line')

        ax.set_xlabel("Frequency ν (Hz)", fontsize=11, color='white')
        ax.set_ylabel("Stopping Voltage V₀ (V)", fontsize=11, color='white')
        ax.set_title("Photoelectric Effect Graph", fontsize=13, color='white')
        ax.grid(True, linestyle=':', alpha=0.4)
        ax.legend()

        st.pyplot(fig)
