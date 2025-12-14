import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import io

# Konfigurasi halaman
st.set_page_config(
    page_title="Model SIR COVID-19 - Simulator RK4",
    page_icon="🦠",
    layout="wide"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🦠 Model SIR COVID-19 - Simulator RK4</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar untuk input
st.sidebar.header("⚙️ Pengaturan Parameter")

# Upload file atau gunakan default
uploaded_file = st.sidebar.file_uploader("Upload File CSV (opsional)", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.sidebar.success("File berhasil diupload!")
else:
    try:
        data = pd.read_csv("covid_data.csv")
    except:
        st.error("⚠️ File 'covid_data.csv' tidak ditemukan. Silakan upload file CSV.")
        st.stop()

# Pilih negara
available_locations = sorted(data['location'].unique())
location = st.sidebar.selectbox(
    "Pilih Negara",
    options=available_locations,
    index=available_locations.index("Indonesia") if "Indonesia" in available_locations else 0
)

# Parameter tuning
st.sidebar.subheader("Parameter Model")
use_optimization = st.sidebar.checkbox("Gunakan Optimasi Otomatis", value=True)

# Inisialisasi parameter manual (akan digunakan jika optimasi tidak dipilih)
beta_manual = 0.5
gamma_manual = 0.1

if not use_optimization:
    beta_manual = st.sidebar.slider("Beta (β) - Laju Penularan", 0.1, 2.0, 0.5, 0.01)
    gamma_manual = st.sidebar.slider("Gamma (γ) - Laju Recovery", 0.05, 1.0, 0.1, 0.01)
else:
    st.sidebar.info("Parameter akan dioptimalkan secara otomatis")

# Fungsi model SIR
def model_sir(t, y, beta, gamma):
    S, I, R = y
    N = S + I + R
    dS_dt = -beta * S * I / N
    dI_dt = beta * S * I / N - gamma * I
    dR_dt = gamma * I
    return np.array([dS_dt, dI_dt, dR_dt])

# Fungsi RK4 solver
def rk4_solver(f, t0, y0, h, n_steps, beta, gamma):
    t = t0
    y = y0
    t_values = [t]
    y_values = [y]
    
    for _ in range(n_steps):
        k1 = f(t, y, beta, gamma)
        k2 = f(t + h/2, y + h/2 * k1, beta, gamma)
        k3 = f(t + h/2, y + h/2 * k2, beta, gamma)
        k4 = f(t + h, y + h * k3, beta, gamma)
        
        y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        t = t + h
        
        t_values.append(t)
        y_values.append(y)
    
    return np.array(t_values), np.array(y_values)

# Fungsi optimasi
def objective_function(params, I_data, y0, h, n_steps):
    beta_opt, gamma_opt = params
    if beta_opt < 0 or gamma_opt < 0 or beta_opt > 2 or gamma_opt > 1:
        return 1e10
    
    t_sim_opt, y_sim_opt = rk4_solver(
        model_sir, 0, y0, h, n_steps, beta_opt, gamma_opt
    )
    I_sim_opt = y_sim_opt[:, 1]
    rmse_opt = np.sqrt(np.mean((I_data - I_sim_opt)**2))
    return rmse_opt

# Tombol untuk menjalankan simulasi
if st.sidebar.button("🚀 Jalankan Simulasi", type="primary"):
    with st.spinner("Memproses data..."):
        # Filter data
        data_filtered = data[data['location'] == location].copy()
        data_filtered = data_filtered[data_filtered['total_cases'].notna()]
        data_filtered = data_filtered[data_filtered['total_cases'] > 0]
        data_filtered = data_filtered.sort_values('date').reset_index(drop=True)
        
        if len(data_filtered) == 0:
            st.error(f"Tidak ada data valid untuk {location}!")
            st.stop()
        
        # Konversi tanggal
        data_filtered['date'] = pd.to_datetime(data_filtered['date'])
        data_filtered['day'] = (data_filtered['date'] - data_filtered['date'].min()).dt.days + 1
        
        time = data_filtered["day"].values
        infected_data = data_filtered["total_cases"].values
        
        # Normalisasi
        if 'population' in data_filtered.columns and data_filtered['population'].notna().any():
            N = data_filtered['population'].iloc[0]
        else:
            N = infected_data.max() * 20
        
        I_data = infected_data / N
        
        # Kondisi awal
        S0 = 0.99
        I0 = I_data[0] if I_data[0] > 0 else 0.000001
        R0 = 0.01
        y0 = np.array([S0, I0, R0])
        
        h = 1
        n_steps = len(time) - 1
        
        # Optimasi atau manual
        if use_optimization:
            with st.spinner("Mengoptimalkan parameter..."):
                initial_params = [0.5, 0.1]
                result = minimize(
                    objective_function,
                    initial_params,
                    args=(I_data, y0, h, n_steps),
                    method='Nelder-Mead',
                    options={'maxiter': 100}
                )
                beta = result.x[0]
                gamma = result.x[1]
                st.success(f"✓ Optimasi selesai! β={beta:.4f}, γ={gamma:.4f}")
        else:
            # Gunakan nilai dari slider
            beta = beta_manual
            gamma = gamma_manual
            st.info(f"✓ Menggunakan parameter manual: β={beta:.4f}, γ={gamma:.4f}")
        
        # Simulasi
        with st.spinner("Menjalankan simulasi RK4..."):
            t_sim, y_sim = rk4_solver(
                model_sir, 0, y0, h, n_steps, beta, gamma
            )
            I_sim = y_sim[:, 1]
            S_sim = y_sim[:, 0]
            R_sim = y_sim[:, 2]
        
        # Hitung RMSE
        rmse = np.sqrt(np.mean((I_data - I_sim)**2))
        R0 = beta / gamma
        
        # Simpan ke session state
        st.session_state['location'] = location
        st.session_state['time'] = time
        st.session_state['I_data'] = I_data
        st.session_state['t_sim'] = t_sim
        st.session_state['I_sim'] = I_sim
        st.session_state['S_sim'] = S_sim
        st.session_state['R_sim'] = R_sim
        st.session_state['beta'] = beta
        st.session_state['gamma'] = gamma
        st.session_state['rmse'] = rmse
        st.session_state['R0'] = R0
        st.session_state['infected_data'] = infected_data
        st.session_state['N'] = N

# Tampilkan hasil jika sudah ada simulasi
if 'I_sim' in st.session_state:
    location = st.session_state['location']
    time = st.session_state['time']
    I_data = st.session_state['I_data']
    t_sim = st.session_state['t_sim']
    I_sim = st.session_state['I_sim']
    S_sim = st.session_state['S_sim']
    R_sim = st.session_state['R_sim']
    beta = st.session_state['beta']
    gamma = st.session_state['gamma']
    rmse = st.session_state['rmse']
    R0 = st.session_state['R0']
    infected_data = st.session_state['infected_data']
    N = st.session_state['N']
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualisasi", "📈 Grafik SIR", "📋 Interpretasi", "💾 Download"])
    
    with tab1:
        st.subheader(f"📊 Perbandingan Data Asli vs Simulasi - {location}")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Beta (β)", f"{beta:.4f}", "Laju Penularan")
        with col2:
            st.metric("Gamma (γ)", f"{gamma:.4f}", "Laju Recovery")
        with col3:
            st.metric("R₀", f"{R0:.4f}", "Reproduction Number")
        with col4:
            st.metric("RMSE", f"{rmse:.6f}", f"{rmse*100:.2f}%")
        
        # Grafik perbandingan
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.scatter(time, I_data, label="Data Asli", color="red", s=15, alpha=0.5, zorder=3)
        ax.plot(t_sim, I_sim, label=f"Simulasi RK4 (β={beta:.4f}, γ={gamma:.4f})", 
                color="blue", linewidth=2.5, zorder=2)
        ax.set_xlabel("Hari", fontsize=12, fontweight='bold')
        ax.set_ylabel("Proporsi Terinfeksi", fontsize=12, fontweight='bold')
        ax.set_title(f"Model SIR - {location} | RMSE = {rmse:.6f}", fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        x_min = min(time.min(), t_sim.min())
        x_max = max(time.max(), t_sim.max())
        y_min = min(I_data.min(), I_sim.min())
        y_max = max(I_data.max(), I_sim.max())
        
        x_margin = (x_max - x_min) * 0.02
        y_margin = (y_max - y_min) * 0.1 if y_max > y_min else 0.01
        
        ax.set_xlim(x_min - x_margin, x_max + x_margin)
        ax.set_ylim(max(0, y_min - y_margin), y_max + y_margin)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab2:
        st.subheader("📈 Grafik Komponen SIR Lengkap")
        
        fig2, ax2 = plt.subplots(figsize=(14, 7))
        ax2.plot(t_sim, S_sim, label="Susceptible (S)", color="green", linewidth=2)
        ax2.plot(t_sim, I_sim, label="Infected (I)", color="red", linewidth=2)
        ax2.plot(t_sim, R_sim, label="Recovered (R)", color="blue", linewidth=2)
        ax2.set_xlabel("Hari", fontsize=12, fontweight='bold')
        ax2.set_ylabel("Proporsi Populasi", fontsize=12, fontweight='bold')
        ax2.set_title(f"Model SIR - {location} (Komponen Lengkap)", fontsize=14, fontweight='bold')
        ax2.legend(fontsize=11)
        ax2.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
        st.pyplot(fig2)
    
    with tab3:
        st.subheader("📋 Interpretasi Parameter")
        
        st.markdown("### 1. Parameter Beta (β)")
        st.info(f"""
        **Nilai: {beta:.6f}**
        
        - **Laju Penularan (Transmission Rate)**
        - Setiap hari, setiap orang terinfeksi dapat menularkan penyakit ke **{beta:.2f}** orang lain
        - Semakin besar β, semakin cepat penyebaran penyakit
        """)
        
        st.markdown("### 2. Parameter Gamma (γ)")
        st.info(f"""
        **Nilai: {gamma:.6f}**
        
        - **Laju Recovery (Recovery Rate)**
        - Setiap hari, **{gamma*100:.2f}%** dari populasi terinfeksi akan sembuh atau diisolasi
        - Waktu rata-rata recovery: **{1/gamma:.2f} hari**
        - Semakin besar γ, semakin cepat pasien sembuh
        """)
        
        st.markdown("### 3. Reproduction Number (R₀)")
        if R0 > 1:
            st.warning(f"""
            **Nilai: {R0:.4f}**
            
            - **R₀ > 1**: Penyakit akan menyebar (epidemi)
            - Setiap 1 orang terinfeksi akan menularkan ke **{R0:.2f}** orang lain
            - Penyakit akan terus berkembang
            """)
        else:
            st.success(f"""
            **Nilai: {R0:.4f}**
            
            - **R₀ < 1**: Penyakit akan menurun
            - Setiap 1 orang terinfeksi akan menularkan ke kurang dari 1 orang
            - Penyakit akan berangsur-angsur hilang
            """)
        
        st.markdown("### 4. Analisis Data")
        st.markdown(f"""
        - **Total hari pengamatan**: {len(time)} hari ({len(time)/30:.1f} bulan)
        - **Proporsi maksimum terinfeksi**: {I_data.max()*100:.2f}%
        - **Proporsi akhir terinfeksi**: {I_data[-1]*100:.2f}%
        - **Jumlah maksimum kasus**: {infected_data.max():,.0f} orang
        - **Jumlah akhir kasus**: {infected_data[-1]:,.0f} orang
        - **Populasi**: {N:,.0f} orang
        """)
        
        st.markdown("### 5. Kualitas Model")
        if rmse < 0.01:
            st.success(f"**RMSE: {rmse:.6f} ({rmse*100:.2f}%)** - Model sangat akurat!")
        elif rmse < 0.05:
            st.info(f"**RMSE: {rmse:.6f} ({rmse*100:.2f}%)** - Model akurat")
        elif rmse < 0.1:
            st.warning(f"**RMSE: {rmse:.6f} ({rmse*100:.2f}%)** - Model cukup akurat")
        else:
            st.error(f"**RMSE: {rmse:.6f} ({rmse*100:.2f}%)** - Model perlu perbaikan")
    
    with tab4:
        st.subheader("💾 Download Hasil")
        
        # Download data hasil simulasi
        results_df = pd.DataFrame({
            'Hari': t_sim,
            'Susceptible': S_sim,
            'Infected': I_sim,
            'Recovered': R_sim,
            'Data_Asli': np.interp(t_sim, time, I_data)
        })
        
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data Simulasi (CSV)",
            data=csv,
            file_name=f"sir_simulation_{location.replace(' ', '_')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Preview Data")
        st.dataframe(results_df.head(20))
        
        # Download parameter
        params_text = f"""
Parameter Model SIR - {location}
================================
Beta (β): {beta:.6f}
Gamma (γ): {gamma:.6f}
R0: {R0:.6f}
RMSE: {rmse:.6f} ({rmse*100:.2f}%)

Kondisi Awal:
- S0: {S_sim[0]:.6f}
- I0: {I_sim[0]:.6f}
- R0: {R_sim[0]:.6f}

Data:
- Total Hari: {len(time)}
- Populasi: {N:,.0f}
- Max Kasus: {infected_data.max():,.0f}
        """
        
        st.download_button(
            label="📥 Download Parameter (TXT)",
            data=params_text,
            file_name=f"parameters_{location.replace(' ', '_')}.txt",
            mime="text/plain"
        )

else:
    st.info("👈 Pilih negara dan parameter di sidebar, lalu klik 'Jalankan Simulasi' untuk memulai!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Model SIR COVID-19 - Simulator dengan Metode Runge-Kutta Orde 4 (RK4)</p>
    <p>Dibuat untuk Tugas Akhir Pemodelan Matematika</p>
</div>
""", unsafe_allow_html=True)

