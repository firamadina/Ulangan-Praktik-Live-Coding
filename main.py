import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

DATA_FILE = 'study_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Ensure structure
            if isinstance(data, list):
                # Migrate old data
                return {'study_data': data, 'schedules': []}
            return data
    return {'study_data': [], 'schedules': []}

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
    data['study_data'].append({'date': date_str, 'duration': duration, 'subject': subject})
    save_data(data)
    print("Data belajar berhasil disimpan.")

def calculate_consistency():
    data = load_data()
    study_data = data['study_data']
    if not study_data:
        print("Belum ada data belajar.")
        return
    total_days = len(set(entry['date'] for entry in study_data))
    total_hours = sum(entry['duration'] for entry in study_data)
    avg_hours_per_day = total_hours / total_days if total_days > 0 else 0
    print(f"Total hari belajar: {total_days}")
    print(f"Total jam belajar: {total_hours:.2f}")
    print(f"Rata-rata jam per hari: {avg_hours_per_day:.2f}")
    # Konsistensi: hitung hari dalam 7 hari terakhir
    last_week = datetime.now() - timedelta(days=7)
    recent_data = [entry for entry in study_data if datetime.strptime(entry['date'], '%Y-%m-%d') >= last_week]
    recent_days = len(set(entry['date'] for entry in recent_data))
    print(f"Hari belajar dalam 7 hari terakhir: {recent_days}/7")

def recommend_schedule():
    data = load_data()
    study_data = data['study_data']
    if not study_data:
        print("Belum ada data untuk rekomendasi.")
        return
    # Hitung pola waktu belajar
    day_counts = defaultdict(float)
    for entry in study_data:
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
    study_data = data['study_data']
    subjects = set(entry.get('subject', 'Unknown') for entry in study_data)
    if subjects:
        print("Mapel yang telah dipelajari:")
        for subj in sorted(subjects):
            print(f"- {subj}")
    else:
        print("Belum ada mapel yang dicatat.")

def input_schedule():
    day = input("Masukkan hari (e.g., Monday): ")
    start_time = input("Masukkan waktu mulai (HH:MM): ")
    end_time = input("Masukkan waktu selesai (HH:MM): ")
    subject = input("Masukkan nama mapel: ")
    data = load_data()
    data['schedules'].append({'day': day, 'start_time': start_time, 'end_time': end_time, 'subject': subject})
    save_data(data)
    print("Jadwal belajar berhasil disimpan.")

def view_schedule():
    data = load_data()
    schedules = data['schedules']
    if not schedules:
        print("Belum ada jadwal belajar yang dicatat.")
        return
    print("Jadwal Belajar Anda:")
    for i, sched in enumerate(schedules, 1):
        print(f"{i}. {sched['day']}: {sched['start_time']} - {sched['end_time']} ({sched['subject']})")

def edit_schedule():
    data = load_data()
    schedules = data['schedules']
    if not schedules:
        print("Belum ada jadwal belajar untuk diedit.")
        return
    view_schedule()  # Tampilkan list
    try:
        idx = int(input("Pilih nomor jadwal yang ingin diedit: ")) - 1
        if 0 <= idx < len(schedules):
            sched = schedules[idx]
            print(f"Mengedit: {sched['day']}: {sched['start_time']} - {sched['end_time']} ({sched['subject']})")
            day = input(f"Hari ({sched['day']}): ") or sched['day']
            start_time = input(f"Waktu mulai ({sched['start_time']}): ") or sched['start_time']
            end_time = input(f"Waktu selesai ({sched['end_time']}): ") or sched['end_time']
            subject = input(f"Mapel ({sched['subject']}): ") or sched['subject']
            schedules[idx] = {'day': day, 'start_time': start_time, 'end_time': end_time, 'subject': subject}
            save_data(data)
            print("Jadwal berhasil diedit.")
        else:
            print("Nomor tidak valid.")
    except ValueError:
        print("Input tidak valid.")

def delete_schedule():
    data = load_data()
    schedules = data['schedules']
    if not schedules:
        print("Belum ada jadwal belajar untuk dihapus.")
        return
    view_schedule()  # Tampilkan list
    try:
        idx = int(input("Pilih nomor jadwal yang ingin dihapus: ")) - 1
        if 0 <= idx < len(schedules):
            deleted = schedules.pop(idx)
            save_data(data)
            print(f"Jadwal {deleted['day']}: {deleted['start_time']} - {deleted['end_time']} ({deleted['subject']}) berhasil dihapus.")
        else:
            print("Nomor tidak valid.")
    except ValueError:
        print("Input tidak valid.")

def main():
    print("🌟 Selamat Datang di Study Tracker! 🌟")
    print("Mari kita jadikan belajar sebagai kebiasaan yang menyenangkan dan produktif!")
    print("Dengan aplikasi ini, Anda dapat melacak waktu belajar, melihat konsistensi,")
    print("mendapatkan rekomendasi jadwal, dan tips belajar yang berguna.")
    print("Semangat belajar dan capai tujuan Anda! 📚✨")
    print("\n" + "="*50)
    while True:
        print("\n\033[96m=== Study Tracker ===\033[0m")
        print("\033[92m1. 📝 Input Waktu Belajar\033[0m")
        print("\033[92m2. 📊 Lihat Konsistensi\033[0m")
        print("\033[92m3. 📅 Rekomendasi Jadwal\033[0m")
        print("\033[92m4. 💡 Tips Belajar\033[0m")
        print("\033[92m5. 📋 List Mapel\033[0m")
        print("\033[92m6. 🕒 Input Jadwal Belajar\033[0m")
        print("\033[92m7. 👀 Lihat Jadwal Belajar\033[0m")
        print("\033[92m8. ✏️ Edit Jadwal Belajar\033[0m")
        print("\033[92m9. 🗑️ Hapus Jadwal Belajar\033[0m")
        print("\033[92m10. 🚪 Keluar\033[0m")
        choice = input("\033[93mPilih opsi: \033[0m")
        if choice == '1':
            input_study_time()
        elif choice == '2':
            calculate_consistency()
        elif choice == '3':
            recommend_schedule()
        elif choice == '4':
            study_tips()
        elif choice == '5':
            list_subjects()
        elif choice == '6':
            input_schedule()
        elif choice == '7':
            view_schedule()
        elif choice == '8':
            edit_schedule()
        elif choice == '9':
            delete_schedule()
        elif choice == '10':
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()