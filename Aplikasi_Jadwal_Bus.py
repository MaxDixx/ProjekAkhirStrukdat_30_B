import os
import csv
os.system("cls")

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop()


    def size(self):
        return len(self.items)


class BusSchedule:
    def __init__(self):
        self.schedule = Queue()
        self.departed_buses = {}
        self.csv_filename = "bus.csv"  
        self.load_schedule_from_csv()
    def load_schedule_from_csv(self):
        if os.path.exists(self.csv_filename):
            with open(self.csv_filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.add_bus(row["KodeBus"])

    def add_bus(self, bus_number):
        self.schedule.enqueue(bus_number)
        print(f"Bus {bus_number} sudah ditambah ke jadwal.")
        self.update_schedule_to_csv()  

    def update_status_in_csv(self, bus_number):
        with open(self.csv_filename, mode='r') as file:
            rows = list(csv.DictReader(file))
            for row in rows:
                if row["KodeBus"] == bus_number:
                    row["Status"] = "Departed"
        with open(self.csv_filename, mode='w', newline='') as file:
            fieldnames = ["KodeBus", "Status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def update_schedule_to_csv(self):
        with open(self.csv_filename, mode='w', newline='') as file:
            Kodebus = ["KodeBus"]
            writer = csv.DictWriter(file, fieldnames=Kodebus)
            writer.writeheader()
            for bus in self.schedule.items:
                writer.writerow({"KodeBus": bus})

    def remove_bus(self):
        if self.schedule.isEmpty():
            print ("Jadwal kosong, semua bus sudah berangkat.")
        else:
            departed_bus = self.schedule.dequeue()
            self.departed_buses[departed_bus] = "Departed"
            self.update_schedule_to_csv()
            self.write_departed_csv()
            self.update_status_in_csv(departed_bus)  
            return departed_bus
    def write_departed_csv(self):
        with open('berangkat.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['BusNumber', 'Status'])
            for bus, status in self.departed_buses.items():
                writer.writerow([bus, status])

    def show_schedule(self):
        if not self.schedule.isEmpty():
            print("Jadwal bus:")
            for bus in self.schedule.items:
                print(f"-> Bus {bus}")
        else:
            print("Jadwal kosong, semua bus sudah berangkat.")

    def show_departed_buses(self):
        if self.departed_buses:
            print("Bus yang sudah berangkat:")
            for bus, status in self.departed_buses.items():
                print(f"-> Bus {bus}")
        else:
            print("Belum ada bus yang berangkat.")

    def show_departed_buses_from_csv(self):
        departed_file = "berangkat.csv"
        with open(departed_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(', '.join(row))
    def user_input(self):
        while True:
            print("\nApa yang ingin anda lakukan?")
            print("1. Tambahkan bus ke jadwal antrian")
            print("2. Hapus jadwal bus dari antrian")
            print("3. Tunjukkan jadwal bus")
            print("4. Bus yang sudah berangkat")
            print("5. Exit")
            choice = input("Masukan pilihan anda (1-5): ")

            if choice == "1":
                bus_number = input("Masukan nomer bus : ")
                self.add_bus(bus_number)
            elif choice == "2":
                self.remove_bus()
            elif choice == "3":
                self.show_schedule()
            elif choice == "4":
                self.show_departed_buses_from_csv()
            elif choice == "5":
                self.show_departed_buses()
                print("Keluar dari program. Terima kasih sudah memakai layanan kami")
                break
            else:
                print("Pilihan salah. Pilihlah pilihan yang tepat.")


bus_schedule = BusSchedule()
bus_schedule.user_input()
