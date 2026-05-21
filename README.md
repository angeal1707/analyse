# Aplikasi Analisis Emiten BEI

Aplikasi Python untuk menganalisis saham yang terdaftar di Bursa Efek Indonesia (BEI) dan memberikan rekomendasi beli/jual.

## Fitur

- **Analisis Fundamental**: Menampilkan P/E Ratio, P/B Ratio, Dividend Yield, Market Cap, dan EPS
- **Analisis Teknikal**: Menggunakan Moving Averages (SMA 20, 50, 200) untuk mengidentifikasi tren
- **Analisis Momentum**: Menggunakan RSI dan MACD untuk menganalisis momentum pasar
- **Rekomendasi Otomatis**: Memberikan skor dan rekomendasi BELI/PERTIMBANGKAN/JANGAN BELI
- **Visualisasi Grafik**: Menampilkan grafik harga dan indikator teknikal

## Instalasi

1. Pastikan Python 3.7+ sudah terinstal
2. Buat virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Cara Menggunakan

1. Aktifkan virtual environment:
```bash
source venv/bin/activate
```

2. Jalankan aplikasi:
```bash
python app.py
```

3. Buka browser dan akses: `http://localhost:5000`
4. Masukkan kode emiten BEI (contoh: BBCA, BMRI, TLKM, ASII, dll)
5. Klik tombol "Analisis"
6. Tunggu hasil analisis muncul dengan grafik dan rekomendasi

## Kode Emiten Populer BEI

- **BBCA**: Bank Central Asia
- **BMRI**: Bank Mandiri
- **BRI**: Bank Rakyat Indonesia
- **TLKM**: Telekomunikasi Indonesia
- **ASII**: Astra International
- **UNVR**: Unilever Indonesia
- **INDF**: Indofood Sukses Makmur
- **GGRM**: Gudang Garam
- **SMGR**: Semen Indonesia
- **ADRO**: Adaro Energy

## Indikator Teknikal

### Moving Averages (SMA)
- **SMA 20**: Rata-rata harga 20 hari (tren jangka pendek)
- **SMA 50**: Rata-rata harga 50 hari (tren jangka menengah)
- **SMA 200**: Rata-rata harga 200 hari (tren jangka panjang)

### RSI (Relative Strength Index)
- **> 70**: Overbought (kemungkinan harga akan turun)
- **< 30**: Oversold (kemungkinan harga akan naik)
- **30-70**: Normal

### MACD (Moving Average Convergence Divergence)
- **MACD > Signal Line**: Bullish (sinyal beli)
- **MACD < Signal Line**: Bearish (sinyal jual)

## Interpretasi Rekomendasi

### BELI (BUY) - Skor ≥ 70%
Sinyal positif kuat untuk membeli saham

### PERTIMBANGKAN (HOLD) - Skor 50-70%
Sinyal netral, pertimbangkan dengan riset lebih lanjut

### JANGAN BELI (SELL) - Skor < 50%
Sinyal negatif, hindari membeli atau pertimbangkan menjual

## Disclaimer

⚠️ **PENTING**: Aplikasi ini hanya untuk tujuan edukasi dan analisis. Bukan merupakan saran investasi profesional. Selalu lakukan riset mendalam dan konsultasi dengan ahli keuangan sebelum membuat keputusan investasi.

## Catatan Penting

- Data diambil dari Yahoo Finance dengan periode 1 tahun terakhir
- Analisis berbasis data historis dan tidak menjamin hasil di masa depan
- Pasar saham sangat dinamis dan dipengaruhi banyak faktor eksternal
- Gunakan aplikasi ini sebagai alat bantu, bukan satu-satunya acuan keputusan

## Troubleshooting

### Saham tidak ditemukan
- Pastikan kode emiten benar (gunakan huruf besar)
- Periksa koneksi internet
- Beberapa saham mungkin tidak tersedia di Yahoo Finance

### Error saat mengambil data
- Tunggu beberapa saat dan coba lagi
- Periksa koneksi internet Anda
- Restart aplikasi jika masalah berlanjut

## Lisensi

MIT License
