# 📦 Panduan Deployment Aplikasi

Panduan lengkap untuk deploy aplikasi Model SIR COVID-19 ke berbagai platform.

## 🚀 Opsi Deployment

### 1. Streamlit Cloud (Paling Mudah - GRATIS)

**Keuntungan:**
- Gratis
- Mudah digunakan
- Auto-deploy dari GitHub
- URL publik otomatis

**Langkah-langkah:**

1. **Push ke GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo-name.git
git push -u origin main
```

2. **Deploy di Streamlit Cloud:**
   - Buka [share.streamlit.io](https://share.streamlit.io)
   - Login dengan GitHub
   - Klik "New app"
   - Pilih repository
   - Pilih branch (biasanya `main`)
   - Main file path: `app.py`
   - Klik "Deploy"

3. **Selesai!** Aplikasi akan tersedia di URL: `https://username-repo-name.streamlit.app`

**Catatan:** 
- Pastikan file `covid_data.csv` sudah di-commit ke GitHub (atau gunakan upload file di aplikasi)
- Jika ada error dengan Python 3.13, Streamlit Cloud akan otomatis menggunakan versi yang kompatibel
- Pastikan `requirements.txt` menggunakan versi fleksibel (>=) untuk kompatibilitas lebih baik

---

### 2. Heroku

**Keuntungan:**
- Gratis tier tersedia
- Custom domain
- Auto-scaling

**Langkah-langkah:**

1. **Install Heroku CLI:**
   - Download dari [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login:**
```bash
heroku login
```

3. **Buat aplikasi:**
```bash
heroku create nama-aplikasi-sir
```

4. **Set buildpack:**
```bash
heroku buildpacks:set heroku/python
```

5. **Deploy:**
```bash
git push heroku main
```

6. **Buka aplikasi:**
```bash
heroku open
```

**File yang diperlukan:**
- `Procfile` (sudah ada)
- `requirements.txt` (sudah ada)
- `runtime.txt` (opsional, untuk Python version)

**Buat `runtime.txt`:**
```
python-3.9.16
```

---

### 3. Docker

**Keuntungan:**
- Portable
- Konsisten di semua environment
- Mudah untuk production

**Langkah-langkah:**

1. **Build image:**
```bash
docker build -t sir-model-app .
```

2. **Run container:**
```bash
docker run -p 8501:8501 sir-model-app
```

3. **Akses di browser:**
   - Buka `http://localhost:8501`

**Deploy ke Docker Hub:**

1. **Login:**
```bash
docker login
```

2. **Tag image:**
```bash
docker tag sir-model-app username/sir-model-app:latest
```

3. **Push:**
```bash
docker push username/sir-model-app:latest
```

4. **Run dari Docker Hub:**
```bash
docker run -p 8501:8501 username/sir-model-app:latest
```

---

### 4. VPS/Cloud Server (AWS, DigitalOcean, dll)

**Langkah-langkah:**

1. **SSH ke server:**
```bash
ssh user@your-server-ip
```

2. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

3. **Install Nginx (reverse proxy):**
```bash
sudo apt install nginx
```

4. **Setup systemd service:**
Buat file `/etc/systemd/system/sir-app.service`:
```ini
[Unit]
Description=Streamlit SIR Model App
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Start service:**
```bash
sudo systemctl start sir-app
sudo systemctl enable sir-app
```

6. **Setup Nginx:**
Edit `/etc/nginx/sites-available/default`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

7. **Restart Nginx:**
```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

### 5. Google Cloud Run

**Langkah-langkah:**

1. **Install gcloud CLI:**
   - Download dari [cloud.google.com](https://cloud.google.com/sdk/docs/install)

2. **Login:**
```bash
gcloud auth login
```

3. **Set project:**
```bash
gcloud config set project YOUR_PROJECT_ID
```

4. **Build dan deploy:**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/sir-model
gcloud run deploy sir-model --image gcr.io/YOUR_PROJECT_ID/sir-model --platform managed
```

---

## 📝 Checklist Sebelum Deploy

- [ ] File `requirements.txt` sudah lengkap
- [ ] File `covid_data.csv` sudah ada (atau siapkan upload)
- [ ] Test aplikasi lokal dengan `streamlit run app.py`
- [ ] Semua dependencies terinstall
- [ ] Tidak ada error saat running

## 🔧 Troubleshooting

### Port sudah digunakan
```bash
# Cari process yang menggunakan port 8501
lsof -i :8501
# Kill process
kill -9 PID
```

### Memory error
- Kurangi ukuran dataset
- Gunakan sampling data
- Upgrade server/RAM

### Import error
- Pastikan semua dependencies di `requirements.txt`
- Install ulang: `pip install -r requirements.txt`

## 📞 Support

Jika ada masalah saat deployment, cek:
1. Log aplikasi
2. Error message di console
3. Dokumentasi platform yang digunakan

---

**Selamat deploy! 🎉**

