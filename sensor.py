# Simulasi Pembacaan Sensor
nilai_sensor = 40

print("---Sistem Aktif---")
print("Membaca intensitas cahaya...")

if nilai_sensor < 50:
    print("Status: Kondisi gelap. Lampu otomatis MENYALA.")
else:
    print("Status: Kondisi terang. Lampu otomatis MATI.")
    