import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

DATA_FILE = 'study_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def input_study_time():
    date_str = input("Masukkan tanggal (YYYY-MM-DD) atau tekan Enter untuk hari ini: ")
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("Format tanggal salah. Gunakan YYYY-MM-DD.")
        return
    subject = input("Masukkan nama mapel: ")
    duration = float(input("Masukkan durasi belajar dalam jam: "))
    data = load_data()
    data.append({'date': date_str, 'duration': duration, 'subject': subject})
    save_data(data)
    print("Data belajar berhasil disimpan.")

def calculate_consistency():
    data = load_data()
    if not data:
        print("Belum ada data belajar.")
        return
    total_days = len(set(entry['date'] for entry in data))
    total_hours = sum(entry['duration'] for entry in data)
    avg_hours_per_day = total_hours / total_days if total_days > 0 else 0
    print(f"Total hari belajar: {total_days}")
    print(f"Total jam belajar: {total_hours:.2f}")
    print(f"Rata-rata jam per hari: {avg_hours_per_day:.2f}")
    # Konsistensi: hitung hari dalam 7 hari terakhir
    last_week = datetime.now() - timedelta(days=7)
    recent_data = [entry for entry in data if datetime.strptime(entry['date'], '%Y-%m-%d') >= last_week]
    recent_days = len(set(entry['date'] for entry in recent_data))
    print(f"Hari belajar dalam 7 hari terakhir: {recent_days}/7")

def recommend_schedule():
    data = load_data()
    if not data:
        print("Belum ada data untuk rekomendasi.")
        return
    # Hitung pola waktu belajar
    day_counts = defaultdict(float)
    for entry in data:
        day = datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%A')
        day_counts[day] += entry['duration']
    if day_counts:
        best_day = max(day_counts, key=day_counts.get)
        print(f"Hari favorit belajar: {best_day} dengan total {day_counts[best_day]:.2f} jam.")
        print("Rekomendasi: Jadwalkan belajar di hari favorit Anda untuk konsistensi.")
    else:
        print("Rekomendasi umum: Belajar 1-2 jam per hari, 5 hari seminggu.")

def study_tips():
    tips = [
        "Gunakan teknik Pomodoro: Belajar 25 menit, istirahat 5 menit.",
        "Aktif recall: Coba ingat materi tanpa melihat catatan.",
        "Spaced repetition: Ulangi materi pada interval yang meningkat.",
        "Tetapkan tujuan harian dan mingguan.",
        "Jaga kesehatan: Tidur cukup, makan sehat, olahraga."
    ]
    print("Saran Teknik Belajar:")
    for tip in tips:
        print(f"- {tip}")

def list_subjects():
    data = load_data()
    subjects = set(entry.get('subject', 'Unknown') for entry in data)
    if subjects:
        print("Mapel yang telah dipelajari:")
        for subj in sorted(subjects):
            print(f"- {subj}")
    else:
        print("Belum ada mapel yang dicatat.")

def main():
    print("🌟 Selamat Datang di Study Tracker! 🌟")
    print("Mari kita jadikan belajar sebagai kebiasaan yang menyenangkan dan produktif!")
    print("Dengan aplikasi ini, Anda dapat melacak waktu belajar, melihat konsistensi,")
    print("mendapatkan rekomendasi jadwal, dan tips belajar yang berguna.")
    print("Semangat belajar dan capai tujuan Anda! 📚✨")
    print("\n" + "="*50)
    while True:
        print("\n=== Study Tracker ===")
        print("1. Input Waktu Belajar")
        print("2. Lihat Konsistensi")
        print("3. Rekomendasi Jadwal")
        print("4. Saran Teknik Belajar")
        print("5. Keluar")
        choice = input("Pilih opsi: ")
        if choice == '1':
            input_study_time()
        elif choice == '2':
            calculate_consistency()
        elif choice == '3':
            recommend_schedule()
        elif choice == '4':
            study_tips()
        elif choice == '5':
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()