# Daily Habit Tracker

## Deskripsi
Daily Habit Tracker adalah aplikasi berbasis desktop yang dibuat menggunakan PyQt5 untuk membantu pengguna dalam membentuk dan melacak kebiasaan positif sehari-hari. Aplikasi ini memungkinkan pengguna untuk menambahkan kebiasaan baru, mencatat progres harian, melihat statistik perkembangan, serta menyimpan dan mengelola data kebiasaan dengan mudah.

Aplikasi ini dikembangkan sebagai mini project untuk memenuhi tugas UTS mata kuliah **Pemrograman Visual**.

---

## Fitur Utama
- Menambahkan, mengedit, dan menghapus kebiasaan.
- Mencatat progres kebiasaan secara harian.
- Tampilan statistik jumlah kebiasaan yang selesai dan sedang berlangsung.
- Tema Light dan Dark yang dapat diganti.
- Ekspor data kebiasaan ke file teks.
- Penyimpanan data lokal menggunakan file JSON.
- Progress bar interaktif untuk memantau perkembangan.

---

## Teknologi yang Digunakan
- **Python 3**
- **PyQt5**
- **JSON** (untuk penyimpanan data lokal)

---

## Cara Menjalankan Aplikasi

1. **Clone repository ini:**
    ```bash
    git clone https://github.com/username/daily-habit-tracker.git
    cd daily-habit-tracker
    ```

2. **Install dependency:**
    ```bash
    pip install PyQt5
    ```

3. **Jalankan aplikasi:**
    ```bash
    python DailyHabitTracker.py
    ```

---

## Struktur Folder
```
.
├── DailyHabitTracker.py
├── habits.json
├── styles/
│   ├── light_theme.qss
│   └── dark_theme.qss
```
