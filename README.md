# Model SIR COVID-19 - Simulator RK4

Aplikasi web interaktif untuk simulasi model SIR (Susceptible-Infected-Recovered) menggunakan metode Runge-Kutta Orde 4 (RK4) untuk memodelkan penyebaran COVID-19.

## 🚀 Fitur

- **Simulasi Model SIR**: Implementasi manual metode RK4 untuk menyelesaikan sistem PDB
- **Parameter Tuning**: Optimasi otomatis parameter beta dan gamma menggunakan scipy.optimize
- **Visualisasi Interaktif**: Grafik perbandingan data asli vs simulasi
- **Multi-Negara**: Pilih negara dari dataset COVID-19
- **Interpretasi Parameter**: Analisis lengkap parameter model (β, γ, R₀)
- **Download Hasil**: Export data simulasi dan parameter dalam format CSV/TXT

## 📋 Requirements

```
streamlit==1.28.0
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
scipy==1.11.1
```

## 🔧 Instalasi

1. Clone atau download repository ini
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Pastikan file `covid_data.csv` ada di folder yang sama dengan `app.py`

## ▶️ Menjalankan Aplikasi

Jalankan aplikasi dengan perintah:
```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser pada `http://localhost:8501`

## 📖 Cara Menggunakan

1. **Pilih Negara**: Gunakan dropdown di sidebar untuk memilih negara
2. **Pilih Parameter**:
   - **Optimasi Otomatis**: Centang untuk optimasi parameter secara otomatis (disarankan)
   - **Manual**: Uncheck dan atur beta (β) dan gamma (γ) secara manual
3. **Jalankan Simulasi**: Klik tombol "🚀 Jalankan Simulasi"
4. **Lihat Hasil**: 
   - Tab **Visualisasi**: Grafik perbandingan data asli vs simulasi
   - Tab **Grafik SIR**: Grafik komponen S, I, R lengkap
   - Tab **Interpretasi**: Analisis parameter dan hasil
   - Tab **Download**: Download hasil simulasi

## 📊 Model SIR

Model SIR memodelkan penyebaran penyakit dengan 3 komponen:

- **S (Susceptible)**: Populasi rentan
- **I (Infected)**: Populasi terinfeksi
- **R (Recovered)**: Populasi sembuh/terisolasi

### Persamaan Diferensial:

```
dS/dt = -β * S * I / N
dI/dt = β * S * I / N - γ * I
dR/dt = γ * I
```

Dimana:
- **β (beta)**: Laju penularan (transmission rate)
- **γ (gamma)**: Laju recovery (recovery rate)
- **N**: Total populasi (S + I + R)
- **R₀**: Reproduction number = β/γ

## 🎯 Parameter

- **Beta (β)**: Laju penularan, semakin besar semakin cepat penyebaran
- **Gamma (γ)**: Laju recovery, semakin besar semakin cepat pasien sembuh
- **R₀**: Reproduction number, jika > 1 maka penyakit akan menyebar (epidemi)

## 📁 Struktur File

```
.
├── app.py                 # Aplikasi Streamlit utama
├── model.ipynb           # Notebook Jupyter untuk analisis
├── covid_data.csv        # Dataset COVID-19
├── requirements.txt      # Dependencies Python
└── README.md            # Dokumentasi
```

## 🌐 Deployment

### Streamlit Cloud (Gratis)

1. Push repository ke GitHub
2. Buka [streamlit.io](https://streamlit.io)
3. Login dengan GitHub
4. Pilih repository dan deploy

### Heroku

1. Install Heroku CLI
2. Buat file `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```
3. Deploy:
```bash
heroku create nama-aplikasi
git push heroku main
```

### Docker

1. Buat `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Build dan run:
```bash
docker build -t sir-model .
docker run -p 8501:8501 sir-model
```

## 📝 Lisensi

Project ini dibuat untuk keperluan akademik (Tugas Akhir Pemodelan Matematika).

## 👨‍💻 Author

Dibuat untuk Tugas Akhir Pemodelan Matematika - Implementasi RK4 untuk Model SIR COVID-19

