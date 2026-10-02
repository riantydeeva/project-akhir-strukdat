import time

class Pesanan:
    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas, t_masuk_detik, t_selesai_detik, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = harga
        self.prioritas = prioritas
        self.t_masuk_detik = t_masuk_detik
        self.t_selesai_detik = t_selesai_detik
        self.status = status

    def jenis_prioritas(self):
        if self.prioritas == 1:
            return "VIP"
        elif self.prioritas == 2:
            return "PRIORITAS"
        else:
            return "REGULER"

    def __str__(self):
        return (self.oid + '|' + self.pelanggan + '|' + self.resto + '|' + self.menu + '|' + self.jenis_prioritas())

    

class Array:
    def __init__(self):
        self.data = []
        self.n = 0
        self.capacity = 0

    def _resize(self):
        if self.capacity == 0:
            self.capacity = 1
        else:
            self.capacity = self.capacity * 2

    def append(self, v):
        if self.n == self.capacity:
            self._resize()

        self.data.append(v)
        self.n += 1

    #tambah
    def insert(self, i, v):
        if i < 0 or i > self.n:
            return False

        if self.n == self.capacity:
            self._resize()

        self.data.append(None)
        
        j = self.n
        while j > i:
            self.data[j] = self.data[j - 1]
            j -= 1

        self.data[i] = v
        self.n += 1

        return True

    def get(self, i):
        if i < 0 or i >= self.n:
            return None
        return self.data[i]

    def remove(self, i):
        if i < 0 or i >= self.n:
            return None

        result = self.data[i]

        j = i
        while j < self.n - 1:
            self.data[j] = self.data[j + 1]
            j += 1

        self.data[self.n - 1] = None
        self.n -= 1

        return result

    def size(self):
        return self.n

    def is_empty(self):
        return self.n == 0

    def clear(self):
        self.data = []
        self.n = 0
        self.capacity = 0



class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.n = 0

    def append(self, v):
        node = Node(v)

        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

        self.n += 1

    def insert(self, i, v):
        if i < 0 or i > self.n:
            return False

        # insert depan
        if i == 0:
            node = Node(v)

            node.next = self.head
            self.head = node

            if self.tail is None:
                self.tail = node

            self.n += 1
            return True

        # insert belakang
        if i == self.n:
            self.append(v)
            return True

        prev = self.head
        j = 0
        while j < i - 1:
            prev = prev.next
            j += 1

        node = Node(v)
        node.next = prev.next
        prev.next = node

        self.n += 1
        return True

    def get(self, i):
        if i < 0 or i >= self.n:
            return None

        now = self.head
        j = 0
        while j < i:
            now = now.next
            j += 1

        return now.data

    def remove(self, i):
        if i < 0 or i >= self.n:
            return None

        # hapus depan
        if i == 0:
            result = self.head.data
            self.head = self.head.next
            self.n -= 1
            if self.n == 0:
                self.tail = None
            return result

        prev = self.head
        j = 0
        while j < i - 1:
            prev = prev.next
            j += 1

        target = prev.next
        result = target.data
        prev.next = target.next

        if target is self.tail:
            self.tail = prev

        self.n -= 1

        return result

    def size(self):
        return self.n

    def is_empty(self):
        return self.n == 0

    def clear(self):
        self.head = None
        self.tail = None
        self.n = 0
    


# backend m1 (yang dipanggil ui)
class M1Pesanan:

    def __init__(self):
        self.array = Array()
        self.linked_list = LinkedList()

    def load(self, file_path):
        self.array.clear()
        self.linked_list.clear()

        file = open("data/pesanan.csv", "r")
        file.readline()  # skip baris pertama

        for line in file:
        
            line = line.strip()

            column = self.parse_csv(line)

            oid = column[0]
            pelanggan = column[1]
            resto = column[2]
            menu = column[3]
            harga = int(column[4])
            prioritas = int(column[5])
            t_masuk_detik = int(column[6])

            if column[7] == "":
                t_selesai_detik = -1
            else:
                t_selesai_detik = int(column[7])

            status = column[8]

            pesanan = Pesanan(oid, pelanggan, resto, menu, harga, prioritas, t_masuk_detik, t_selesai_detik, status)

            self.array.append(pesanan)
            self.linked_list.append(pesanan)

        file.close()

    def parse_csv(self, line):
        result = []

        part = ""
        in_quotes = False

        i = 0
        while i < len(line):
            char = line[i]

            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                result.append(part)
                part = ""
            else:
                part += char

            i += 1

        result.append(part)

        return result

    #array

    # Lihat pesanan ke-i
    def array_lihat_pesanan(self, i):
        return self.array.get(i)

    # REGULER -> paling belakang
    def array_tambah_reguler(self, pesanan):
        pesanan.prioritas = 3
        self.array.append(pesanan)

    # PRIORITAS -> tengah (n // 2)
    def array_tambah_prioritas(self, pesanan):
        pesanan.prioritas = 2
        posisi = self.array.size() // 2
        self.array.insert(posisi, pesanan)

    # VIP -> paling depan
    def array_tambah_vip(self, pesanan):
        pesanan.prioritas = 1
        self.array.insert(0, pesanan)

    # Hapus pesanan ke-i
    def array_hapus_pesanan(self, i):
        return self.array.remove(i)

    #linked list

    # Lihat pesanan ke-i
    def linkedlist_lihat_pesanan(self, i):
        return self.linked_list.get(i)

    # REGULER -> paling belakang
    def linkedlist_tambah_reguler(self, pesanan):
        pesanan.prioritas = 3
        self.linked_list.append(pesanan)

    # PRIORITAS -> tengah (n // 2)
    def linkedlist_tambah_prioritas(self, pesanan):
        pesanan.prioritas = 2
        posisi = self.linked_list.size() // 2
        self.linked_list.insert(posisi, pesanan)

    # VIP -> paling depan
    def linkedlist_tambah_vip(self, pesanan):
        pesanan.prioritas = 1
        self.linked_list.insert(0, pesanan)

    # Hapus pesanan ke-i
    def linkedlist_hapus_pesanan(self, i):
        return self.linked_list.remove(i)



#operasi
def tampilkan_pesanan(pesanan):
    if pesanan is None:
        print("Pesanan tidak ditemukan.")
        return

    print("OID             :", pesanan.oid)
    print("Pelanggan       :", pesanan.pelanggan)
    print("Restoran        :", pesanan.resto)
    print("Menu            :", pesanan.menu)
    print("Harga           :", pesanan.harga)
    print("Prioritas       :", pesanan.jenis_prioritas())
    print("Waktu masuk     :", pesanan.t_masuk_detik)
    print("Waktu selesai   :", pesanan.t_selesai_detik)
    print("Status          :", pesanan.status)


def buat_pesanan_baru():
    print()
    print("=== PESANAN BARU ===")

    oid = input("OID             : ")
    pelanggan = input("Pelanggan       : ")
    resto = input("Restoran        : ")
    menu = input("Menu            : ")
    harga = int(input("Harga           : "))
    waktu_masuk = int(input("Waktu masuk     : "))

    return Pesanan(oid, pelanggan, resto, menu, harga, 3, waktu_masuk, -1, "ANTRE")

def ukur_operasi(nama, fungsi):
    mulai = time.perf_counter()
    hasil = fungsi()
    selesai = time.perf_counter()

    waktu_ms = (selesai - mulai) * 1000

    print()
    print("Perintah :", nama)
    print("Waktu    :", format(waktu_ms, ".4f"), "ms")

    return hasil



#cek
if __name__ == "__main__":

    m1 = M1Pesanan()
    sudah_load = False

    while True:
        print()
        print("==================================================")
        print("              TEST BACKEND M1")
        print("==================================================")
        print("Data loaded :", sudah_load)
        print("Jumlah Array:", m1.array.size())
        print("Jumlah List :", m1.linked_list.size())
        print("--------------------------------------------------")
        print("1. Load / reset data dari CSV")
        print()
        print("2. Array - lihat pesanan ke-i")
        print("3. Array - tambah REGULER")
        print("4. Array - tambah PRIORITAS")
        print("5. Array - tambah VIP")
        print("6. Array - hapus pesanan ke-i")
        print()
        print("7. Linked List - lihat pesanan ke-i")
        print("8. Linked List - tambah REGULER")
        print("9. Linked List - tambah PRIORITAS")
        print("10. Linked List - tambah VIP")
        print("11. Linked List - hapus pesanan ke-i")
        print()
        print("12. Tampilkan beberapa data awal")
        print("0. Keluar")
        print("==================================================")

        pilihan = input("Pilih menu: ")

        #load
        if pilihan == "1":
            path = input("Lokasi CSV [data/pesanan.csv]: ")

            if path == "":
                path = "data/pesanan.csv"

            mulai = time.perf_counter()
            m1.load(path)
            selesai = time.perf_counter()

            sudah_load = True

            print()
            print("Data berhasil di-load.")
            print("Jumlah Array       :", m1.array.size())
            print("Jumlah Linked List :", m1.linked_list.size())
            print(
                "Waktu load         :",
                format((selesai - mulai) * 1000, ".4f"),
                "ms"
            )

        #aray lihat
        elif pilihan == "2":
            if not sudah_load:
                print("Silakan Load data terlebih dahulu.")
                continue

            i = int(input("Index pesanan: "))

            hasil = ukur_operasi(
                "array_get",
                lambda: m1.array_lihat_pesanan(i)
            )

            print()
            tampilkan_pesanan(hasil)

        #array reguler
        elif pilihan == "3":
            pesanan = buat_pesanan_baru()

            ukur_operasi(
                "array_append",
                lambda: m1.array_tambah_reguler(pesanan)
            )

            print("Pesanan REGULER masuk paling belakang.")
            print("Jumlah Array:", m1.array.size())

        #array prioritas
        elif pilihan == "4":
            pesanan = buat_pesanan_baru()

            ukur_operasi(
                "array_insert_prioritas",
                lambda: m1.array_tambah_prioritas(pesanan)
            )

            print("Pesanan PRIORITAS masuk ke posisi tengah.")
            print("Jumlah Array:", m1.array.size())

        #array vip
        elif pilihan == "5":
            pesanan = buat_pesanan_baru()

            ukur_operasi(
                "array_insert_vip",
                lambda: m1.array_tambah_vip(pesanan)
            )

            print("Pesanan VIP masuk ke posisi pertama.")
            print("Jumlah Array:", m1.array.size())

        #array hapus
        elif pilihan == "6":
            i = int(input("Index pesanan yang dihapus: "))

            hasil = ukur_operasi(
                "array_remove",
                lambda: m1.array_hapus_pesanan(i)
            )

            if hasil is None:
                print("Index tidak valid.")
            else:
                print("Pesanan berhasil dihapus:")
                print(hasil)

        #linked list lihat
        elif pilihan == "7":
            if not sudah_load:
                print("Silakan Load data terlebih dahulu.")
                continue

            i = int(input("Index pesanan: "))

            hasil = ukur_operasi(
                "linkedlist_get",
                lambda: m1.linkedlist_lihat_pesanan(i)
            )

            print()
            tampilkan_pesanan(hasil)

        #linked list reguler
        elif pilihan == "8":
            pesanan = buat_pesanan_baru()

            ukur_operasi(
                "linkedlist_append",
                lambda: m1.linkedlist_tambah_reguler(pesanan)
            )

            print("Pesanan REGULER masuk paling belakang.")
            print("Jumlah Linked List:", m1.linked_list.size())

        #linked list prioritas
        elif pilihan == "9":
            pesanan = buat_pesanan_baru()

            ukur_operasi(
                "linkedlist_insert_prioritas",
                lambda: m1.linkedlist_tambah_prioritas(pesanan)
            )

            print("Pesanan PRIORITAS masuk ke posisi tengah.")
            print("Jumlah Linked List:", m1.linked_list.size())

        #linked list vip
        elif pilihan == "10":
            pesanan = buat_pesanan_baru()

            ukur_operasi(
                "linkedlist_insert_vip",
                lambda: m1.linkedlist_tambah_vip(pesanan)
            )

            print("Pesanan VIP masuk ke posisi pertama.")
            print("Jumlah Linked List:", m1.linked_list.size())

        #linked list hapus
        elif pilihan == "11":
            i = int(input("Index pesanan yang dihapus: "))

            hasil = ukur_operasi(
                "linkedlist_remove",
                lambda: m1.linkedlist_hapus_pesanan(i)
            )

            if hasil is None:
                print("Index tidak valid.")
            else:
                print("Pesanan berhasil dihapus:")
                print(hasil)

        #tampilkan data awal
        elif pilihan == "12":
            print()
            print("=== 10 DATA PERTAMA ARRAY ===")

            jumlah = m1.array.size()

            if jumlah == 0:
                print("Belum ada data.")
            else:
                batas = 10
                if jumlah < batas:
                    batas = jumlah

                i = 0
                while i < batas:
                    print(i, ":", m1.array.get(i))
                    i += 1

            print()
            print("=== 10 DATA PERTAMA LINKED LIST ===")

            jumlah = m1.linked_list.size()

            if jumlah == 0:
                print("Belum ada data.")
            else:
                batas = 10
                if jumlah < batas:
                    batas = jumlah

                i = 0
                sekarang = m1.linked_list.head

                while i < batas:
                    print(i, ":", sekarang.data)
                    sekarang = sekarang.next
                    i += 1

        elif pilihan == "0":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid.")