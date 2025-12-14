# 🔧 Troubleshooting Deployment

## Error: ModuleNotFoundError: No module named 'distutils'

**Penyebab:** Python 3.13+ tidak lagi menyertakan `distutils`. Package lama seperti `numpy==1.24.3` memerlukan distutils untuk build dari source.

**Solusi PENTING:**

1. **Update requirements.txt** - Gunakan numpy versi >= 1.26.0:
   ```
   streamlit>=1.28.0
   numpy>=1.26.0    # ← PENTING: Versi ini support Python 3.13
   pandas>=2.0.0
   matplotlib>=3.7.0
   scipy>=1.11.0
   ```

2. **Jika masih error di Streamlit Cloud:**
   - Buka Settings di Streamlit Cloud
   - Pilih Python version: 3.11 (jika tersedia)
   - Atau gunakan `requirements-lock.txt` yang sudah disediakan

3. **Alternatif - Gunakan versi locked:**
   - Rename `requirements-lock.txt` menjadi `requirements.txt`
   - Versi ini sudah diuji kompatibel dengan Python 3.13

## Error: BackendUnavailable

**Penyebab:** Build backend tidak tersedia atau tidak kompatibel.

**Solusi:**
- Pastikan menggunakan Python 3.9-3.12
- Update pip: `pip install --upgrade pip setuptools wheel`
- Install build tools: `pip install build`

## Error: Port already in use

**Solusi:**
```bash
# Cari process
lsof -i :8501
# Kill process
kill -9 PID
```

## Error: File not found (covid_data.csv)

**Solusi:**
1. Pastikan file ada di root folder
2. Atau gunakan fitur upload di aplikasi
3. Untuk deployment, commit file ke GitHub (jika < 100MB)

## Error: Memory limit exceeded

**Solusi:**
- Kurangi ukuran dataset
- Gunakan sampling data
- Upgrade tier hosting

## Tips Deployment Streamlit Cloud

1. **Pastikan requirements.txt tidak terlalu ketat**
   - Gunakan `>=` bukan `==` untuk fleksibilitas
   - Jangan pin versi terlalu spesifik

2. **File size limit**
   - Streamlit Cloud: 1GB total
   - Jika `covid_data.csv` terlalu besar, gunakan upload feature

3. **Python version**
   - Streamlit Cloud otomatis pilih versi kompatibel
   - Biasanya Python 3.11

4. **Build time**
   - Build pertama mungkin lama (5-10 menit)
   - Sabar dan tunggu proses selesai

## Test Lokal Sebelum Deploy

```bash
# Install dependencies
pip install -r requirements.txt

# Test aplikasi
streamlit run app.py

# Jika berhasil, baru deploy
```

## Kontak Support

Jika masih ada masalah:
1. Cek log deployment di Streamlit Cloud
2. Test lokal dulu
3. Pastikan semua file sudah di-commit

