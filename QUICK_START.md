# 🚀 Quick Start Guide

Panduan cepat untuk menjalankan aplikasi Model SIR COVID-19.

## ⚡ Menjalankan Lokal (Cepat)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Jalankan aplikasi:**
```bash
streamlit run app.py
```

3. **Buka browser:**
   - Aplikasi akan otomatis terbuka di `http://localhost:8501`
   - Atau buka manual di browser

## 📋 File yang Diperlukan

- ✅ `app.py` - Aplikasi utama
- ✅ `covid_data.csv` - Dataset (atau upload via aplikasi)
- ✅ `requirements.txt` - Dependencies

## 🎯 Fitur Utama

1. **Pilih Negara** dari dropdown
2. **Pilih Mode**:
   - ✅ Optimasi Otomatis (disarankan)
   - ⚙️ Manual (atur beta & gamma sendiri)
3. **Klik "Jalankan Simulasi"**
4. **Lihat Hasil** di 4 tab:
   - 📊 Visualisasi
   - 📈 Grafik SIR
   - 📋 Interpretasi
   - 💾 Download

## 🌐 Deploy ke Web

### Streamlit Cloud (Paling Mudah)
1. Push ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Deploy dari GitHub
4. Selesai!

Lihat `DEPLOYMENT.md` untuk detail lengkap.

## ❓ Troubleshooting

**Error: File tidak ditemukan**
- Pastikan `covid_data.csv` ada di folder yang sama
- Atau upload file via aplikasi

**Error: Module not found**
- Install dependencies: `pip install -r requirements.txt`

**Port sudah digunakan**
- Gunakan port lain: `streamlit run app.py --server.port 8502`

## 📚 Dokumentasi Lengkap

- `README.md` - Dokumentasi lengkap
- `DEPLOYMENT.md` - Panduan deployment
- `model.ipynb` - Analisis dan development

---

**Selamat menggunakan! 🎉**

