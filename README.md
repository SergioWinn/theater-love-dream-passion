# 🔴 Theater Love Dream Passion - Live Ticket Monitor

Web aplikasi berbasis **Streamlit** yang dirancang untuk memantau ketersediaan kuota tiket **2-Shot** dan **Meet & Greet** JKT48 secara real-time untuk rangkaian event **Theater Love Dream Passion** di Surabaya dan Yogyakarta. 

Aplikasi ini membantu para fans untuk memantau pergerakan kuota tiket member incaran mereka secara instan dan *sat-set* saat masa penjualan tiket berlangsung.

## ✨ Fitur Utama

*   **📍 Dual-Location Filter:** Beralih dengan mudah antara event di **Surabaya** dan **Yogyakarta** hanya dengan satu klik.
*   **🔄 Stable Auto-Refresh:** Sinkronisasi data otomatis langsung ke API server JKT48 setiap 5 detik tanpa perlu me-refresh halaman manual.
*   **🩷⭐🔥 Dynamic Team Tabs:** Tampilan rapi yang dipisahkan berdasarkan tim (**TEAM LOVE**, **TEAM DREAM**, **TEAM PASSION**) menggunakan sistem *Dynamic Tabs* (tab hanya muncul jika API tim tersebut sudah aktif).
*   **📸 Kabesha Photo Integration:** Menampilkan foto profil resmi (*kabesha*) dari setiap member menggunakan proxy gambar asinkron yang ringan dan cepat.
*   **📊 Smart Progress Button:** Visualisasi kuota premium menggunakan *progress bar* interaktif yang berubah warna sesuai kondisi tiket (Hijau: Tersedia, Kuning: Menipis, Merah: Habis).
*   **🛒 Direct Purchase Link:** Memotong jalur antrean pembelian! Klik tombol **SISA** pada kartu member untuk langsung diarahkan (*auto-direct*) ke halaman pembayaran resmi JKT48 di tab baru.
*   **🔒 Safe Navigation & Sold Out Lock:** Melindungi kenyamanan pengguna dari ketidaksengajaan klik (*accidental touch*) saat melakukan *scrolling* di perangkat mobile, serta mengunci kartu member secara otomatis jika tiket sudah **HABIS**.

## 🛠️ Tech Stack

*   **Python** (Bahasa pemrograman utama)
*   **Streamlit** (Framework UI & Web App)
*   **Requests** (HTTP Library untuk integrasi API JKT48)
*   **Streamlit-Autorefresh** (Komponen pengatur interval refresh otomatis)

## 🚀 Menjalankan Secara Lokal

Jika ingin mencoba menjalankan aplikasi ini di komputer lokal, ikuti langkah-langkah berikut:

### 1. Clone Repositori ini

```bash
git clone [https://github.com/SergioWinn/theater-love-dream-passion.git](https://github.com/SergioWinn/theater-love-dream-passion.git)
cd theater-love-dream-passion
```

### 2. Install Dependencies

Pastikan sudah menginstal Python di komputer, lalu jalankan perintah:

```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi

```bash
streamlit run app.py
```

## 🌐 Deployment

Aplikasi ini sepenuhnya kompatibel dan siap untuk di-hosting secara gratis di **Streamlit Community Cloud** (`share.streamlit.io`) langsung dari branch utama repositori GitHub ini.

## 🤝 Credits & Support

Proyek ini dikembangkan dan dikelola secara mandiri oleh:
*   **X (Twitter):** [@estrellawin19](https://x.com/estrellawin19)

Jika aplikasi ini bermanfaat dan membantu kamu memenangkan *war* tiket member incaranmu, kamu bisa memberikan dukungan atau sekadar memberikan apresiasi melalui:
*   **Tako:** [🐙 Support via Tako](https://tako.id/Sportagame19Win)

---
*Disclaimer: Aplikasi ini adalah alat bantu pihak ketiga (fan-made) yang memanfaatkan API publik JKT48. Seluruh hak cipta data, aset gambar, dan sistem pembayaran adalah milik JKT48 Official Team (JOT).*
