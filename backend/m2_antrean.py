import csv
#import time

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

    def __str__(self):
        return (self.oid + '|' + self.pelanggan + '|' + self.resto + '|' + self.menu + '|' + self.prioritas + '|' + self.status)



def muat_pesanan_antre():
    hasil = []

    with open("data/pesanan.csv", "r", encoding="utf-8-sig", newline="") as file:

        pembaca = csv.reader(file)
        next(pembaca, None)

        for kolom in pembaca:

            if kolom[8].strip().upper() == "ANTRE":
                selesai = kolom[7].strip()
                
                if selesai == "":
                    selesai = -1
                else:
                    selesai = int(selesai)

                p = Pesanan(kolom[0].strip(), kolom[1].strip(), kolom[2].strip(), kolom[3].strip(), int(kolom[4]), int(kolom[5]), int(kolom[6]), selesai, kolom[8].strip())
                hasil.append(p)

    return hasil



class Queue:
    def __init__(self, kapasitas=200000):
        self.data = []
        self.circular = [None] * kapasitas
        self.kapasitas = kapasitas
        self.depan = 0
        self.belakang = 0
        self.jumlah = 0

    def enqueue(self, nilai):
        if len(self.data) >= self.kapasitas:
            return False

        if self.jumlah >= self.kapasitas:
            return False

        self.data.append(nilai)

        self.circular[self.belakang] = nilai
        self.belakang = (
            self.belakang + 1
        ) % self.kapasitas

        self.jumlah += 1

        return True

    def dequeue_naif(self):
        if self.is_empty_naif():
            return None

        hasil = self.data[0]

        i = 0
        while i < len(self.data) - 1:
            self.data[i] = self.data[i + 1]
            i += 1

        self.data.pop()
        return hasil

    def dequeue_circular(self):
        if self.is_empty_circular():
            return None

        hasil = self.circular[self.depan]
        self.circular[self.depan] = None

        self.depan = (self.depan + 1) % self.kapasitas
        self.jumlah -= 1

        if self.jumlah == 0:
            self.depan = 0
            self.belakang = 0

        return hasil

    def peek_naif(self):
        if self.is_empty_naif():
            return None
        return self.data[0]

    def peek_circular(self):
        if self.is_empty_circular():
            return None
        return self.circular[self.depan]

    def is_empty_naif(self):
        return len(self.data) == 0

    def is_empty_circular(self):
        return self.jumlah == 0

    def size_naif(self):
        return len(self.data)

    def size_circular(self):
        return self.jumlah

    def lihat_naif(self):
        hasil = []
        i = 0

        while i < len(self.data):
            hasil.append(self.data[i])
            i += 1

        return hasil

    def lihat_circular(self):
        hasil = []
        i = 0

        while i < self.jumlah:
            indeks = (self.depan + i) % self.kapasitas
            hasil.append(self.circular[indeks])
            i += 1

        return hasil



class Stack:
    def __init__(self):
        self.data = []

    def push(self, nilai):
        self.data.append(nilai)

    def pop(self):
        if self.is_empty():
            return None
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.data[len(self.data) - 1]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def clear(self):
        self.data = []



def pecah_token(ekspresi):
    token = []
    angka = ""

    for karakter in ekspresi:
        if karakter.isdigit():
            angka += karakter
        else:
            if angka != "":
                token.append(angka)
                angka = ""

            if karakter in "+-*/()":
                token.append(karakter)
            elif karakter.isspace():
                continue
            else:
                raise ValueError("Karakter tidak valid: " + karakter)

    if angka != "":
        token.append(angka)

    return token



def prioritas(operator):
    if operator == "+" or operator == "-":
        return 1
    elif operator == "*" or operator == "/":
        return 2
    return 0


def infix_ke_postfix(ekspresi):
    token = pecah_token(ekspresi)

    stack_operator = Stack()
    keluaran = []
    langkah = []
    nomor = 1

    for item in token:
        if item.isdigit():
            keluaran.append(item)

            langkah.append([
                "1." + str(nomor),
                item,
                "operand, langsung ke output",
                " ".join(stack_operator.data) if not stack_operator.is_empty() else "kosong",
                " ".join(keluaran)
            ])

        elif item == "(":
            stack_operator.push(item)

            langkah.append([
                "1." + str(nomor),
                item,
                "push ( ke stack",
                " ".join(stack_operator.data),
                " ".join(keluaran) if keluaran else "kosong"
            ])

        elif item == ")":
            ditemukan = False

            while not stack_operator.is_empty():
                operator = stack_operator.pop()

                if operator == "(":
                    ditemukan = True
                    break

                keluaran.append(operator)

            if not ditemukan:
                raise ValueError("Kurung tidak seimbang.")

            langkah.append([
                "1." + str(nomor),
                item,
                "pop sampai ( lalu buang (",
                " ".join(stack_operator.data) if not stack_operator.is_empty() else "kosong",
                " ".join(keluaran)
            ])

        elif item in "+-*/":
            tindakan = ""

            while not stack_operator.is_empty():
                atas = stack_operator.peek()

                if atas == "(":
                    break

                if prioritas(atas) >= prioritas(item):
                    keluaran.append(stack_operator.pop())
                    tindakan += "pop " + atas + ", "

                else:
                    break

            stack_operator.push(item)
            tindakan += "push " + item

            langkah.append([
                "1." + str(nomor),
                item,
                tindakan,
                " ".join(stack_operator.data),
                " ".join(keluaran) if keluaran else "kosong"
            ])

        nomor += 1

    while not stack_operator.is_empty():
        operator = stack_operator.pop()

        if operator == "(":
            raise ValueError("Kurung tidak seimbang.")

        keluaran.append(operator)

        langkah.append([
            "1.akhir",
            operator,
            "pop sisa stack: " + operator,
            " ".join(stack_operator.data) if not stack_operator.is_empty() else "kosong",
            " ".join(keluaran)
        ])

    postfix = " ".join(keluaran)

    return postfix, langkah



def hitung_postfix(postfix):
    stack_angka = Stack()
    langkah = []
    token = postfix.split()
    nomor = 1

    for item in token:
        if item.isdigit():
            stack_angka.push(int(item))
            tindakan = "operand, push " + item

        else:
            angka2 = stack_angka.pop()
            angka1 = stack_angka.pop()

            if angka1 is None or angka2 is None:
                raise ValueError("Ekspresi tidak valid.")

            if item == "+":
                hasil = angka1 + angka2
            elif item == "-":
                hasil = angka1 - angka2
            elif item == "*":
                hasil = angka1 * angka2
            elif item == "/":
                if angka2 == 0:
                    raise ValueError("Tidak bisa membagi dengan nol.")
                hasil = angka1 / angka2
            else:
                raise ValueError("Operator tidak valid.")

            tindakan = (
                "pop " + str(angka1) +
                " dan " + str(angka2) +
                ", hitung " + str(angka1) +
                " " + item + " " + str(angka2) +
                " = " + str(hasil)
            )

            stack_angka.push(hasil)

        langkah.append([
            "2." + str(nomor),
            item,
            tindakan,
            " ".join(str(x) for x in stack_angka.data)
                if not stack_angka.is_empty() else "kosong",
            item
        ])

        nomor += 1

    if stack_angka.size() != 1:
        raise ValueError("Ekspresi tidak valid.")

    return stack_angka.pop(), langkah



class UndoRedoAntrean:
    def __init__(self, queue):
        self.queue = queue
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def _kondisi(self):
        return (
            self.queue.lihat_naif(),
            self.queue.lihat_circular(),
            self.queue.depan,
            self.queue.belakang,
            self.queue.jumlah
        )

    def _pulihkan(self, kondisi):
        data_naif, data_circular, depan, belakang, jumlah = kondisi

        self.queue.data = data_naif[:]
        self.queue.circular = [None] * self.queue.kapasitas

        i = 0
        while i < jumlah:
            indeks = (depan + i) % self.queue.kapasitas
            self.queue.circular[indeks] = data_circular[i]
            i += 1

        self.queue.depan = depan
        self.queue.belakang = belakang
        self.queue.jumlah = jumlah

    def simpan_sebelum(self):
        self.undo_stack.push(self._kondisi())
        self.redo_stack.clear()

    def batalkan_simpan(self):
        # Digunakan jika operasi ternyata gagal.
        if not self.undo_stack.is_empty():
            self.undo_stack.pop()

    def undo(self):
        if self.undo_stack.is_empty():
            return None

        kondisi_sekarang = self._kondisi()
        kondisi_sebelumnya = self.undo_stack.pop()

        self.redo_stack.push(kondisi_sekarang)
        self._pulihkan(kondisi_sebelumnya)

        return kondisi_sekarang, kondisi_sebelumnya

    def redo(self):
        if self.redo_stack.is_empty():
            return None

        kondisi_sekarang = self._kondisi()
        kondisi_berikutnya = self.redo_stack.pop()

        self.undo_stack.push(kondisi_sekarang)
        self._pulihkan(kondisi_berikutnya)

        return kondisi_sekarang, kondisi_berikutnya



def buat_m2(data_awal, kapasitas_tambahan=1000):
    kapasitas = len(data_awal) + kapasitas_tambahan

    queue = Queue(kapasitas)

    for pesanan in data_awal:
        if not queue.enqueue(pesanan):
            raise OverflowError(
                "Kapasitas antrean tidak mencukupi."
            )

    riwayat = UndoRedoAntrean(queue)

    return queue, riwayat



def cari_pesanan(daftar, oid):
    i = 0

    while i < len(daftar):
        if daftar[i].oid == oid:
            return daftar[i]

        i += 1

    return None



def fitur_enqueue(queue, riwayat):
    print("\n=== QUEUE - ENQUEUE ===")
    print("Masukkan data pesanan baru.")

    oid = input("ID Pesanan      : ").strip()

    # Memeriksa apakah ID sudah digunakan
    i = 0
    while i < len(queue.data):
        if queue.data[i].oid == oid:
            print("ID pesanan sudah ada di antrean naif.")
            return
        i += 1

    i = 0
    while i < queue.jumlah:
        indeks = (queue.depan + i) % queue.kapasitas

        if queue.circular[indeks].oid == oid:
            print("ID pesanan sudah ada di antrean circular.")
            return
        i += 1

    pelanggan = input("Nama Pelanggan  : ").strip()
    resto = input("Nama Restoran   : ").strip()
    menu = input("Nama Menu       : ").strip()

    # Memastikan harga berupa angka
    try:
        harga = int(input("Harga           : "))
        if harga < 0:
            print("Harga tidak boleh negatif.")
            return
    except ValueError:
        print("Harga harus berupa angka.")
        return

    prioritas = input("Prioritas       : ").strip()

    try:
        t_masuk_detik = int(input("Waktu Masuk (detik): "))
        if t_masuk_detik < 0:
            print("Waktu masuk tidak boleh negatif.")
            return
    except ValueError:
        print("Waktu masuk harus berupa angka.")
        return

    pesanan = Pesanan(oid, pelanggan, resto, menu, harga, prioritas, t_masuk_detik, -1, "ANTRE")

    if (len(queue.data) >= queue.kapasitas or queue.jumlah >= queue.kapasitas):
        print("Antrean penuh. Pesanan gagal ditambahkan.")
        return

    # Simpan kondisi sebelum perubahan agar bisa di-undo
    riwayat.simpan_sebelum()

    if queue.enqueue(pesanan):
        print("\nPesanan berhasil ditambahkan!")
        print(pesanan)
    else:
        print("Antrean penuh. Pesanan gagal ditambahkan.")



def fitur_dequeue_naif(queue, riwayat):
    print("\n=== QUEUE - DEQUEUE NAIF ===")

    if queue.is_empty_naif():
        print("Antrean naif kosong.")
        return

    try:
        jumlah = int(input("Jumlah pesanan yang ingin dikeluarkan: "))

        if jumlah <= 0:
            print("Jumlah pesanan harus lebih dari 0.")
            return
    except ValueError:
        print("Jumlah harus berupa angka.")
        return

    tersedia = queue.size_naif()

    if jumlah > tersedia:
        print("Jumlah melebihi antrean.")
        print("Pesanan tersedia:", tersedia)
        return

    riwayat.simpan_sebelum()

    print("\nPesanan yang dikeluarkan:")
    i = 0

    while i < jumlah:
        pesanan = queue.dequeue_naif()
        print(str(i + 1) + ". " + str(pesanan))
        i += 1

    print("Total pesanan dikeluarkan:", jumlah)



def fitur_dequeue_circular(queue, riwayat):
    print("\n=== QUEUE - DEQUEUE CIRCULAR ===")

    if queue.is_empty_circular():
        print("Antrean circular kosong.")
        return

    try:
        jumlah = int(input("Jumlah pesanan yang ingin dikeluarkan: "))

        if jumlah <= 0:
            print("Jumlah pesanan harus lebih dari 0.")
            return
    except ValueError:
        print("Jumlah harus berupa angka.")
        return

    tersedia = queue.size_circular()

    if jumlah > tersedia:
        print("Jumlah melebihi antrean.")
        print("Pesanan tersedia:", tersedia)
        return

    riwayat.simpan_sebelum()

    print("\nPesanan yang dikeluarkan:")
    i = 0

    while i < jumlah:
        pesanan = queue.dequeue_circular()
        print(str(i + 1) + ". " + str(pesanan))
        i += 1

    print("Total pesanan dikeluarkan:", jumlah)



def tampilkan_antrean(queue):
    print("\n=== ANTREAN NAIF ===")
    data_naif = queue.lihat_naif()

    if len(data_naif) == 0:
        print("Antrean kosong.")
    else:
        i = 0
        while i < len(data_naif):
            print(str(i + 1) + ". " + str(data_naif[i]))
            i += 1

    print("\n=== ANTREAN CIRCULAR ===")
    data_circular = queue.lihat_circular()

    if len(data_circular) == 0:
        print("Antrean kosong.")
    else:
        i = 0
        while i < len(data_circular):
            print(str(i + 1) + ". " + str(data_circular[i]))
            i += 1



def tampilkan_perubahan(kondisi_sebelum, kondisi_sesudah, jenis):
    naif_sebelum = kondisi_sebelum[0]
    naif_sesudah = kondisi_sesudah[0]

    circular_sebelum = kondisi_sebelum[1]
    circular_sesudah = kondisi_sesudah[1]

    ada_perubahan = False

    # Periksa perubahan pada antrean naif.
    i = 0
    while i < len(naif_sebelum):
        pesanan = naif_sebelum[i]
        ditemukan = False

        j = 0
        while j < len(naif_sesudah):
            if naif_sesudah[j].oid == pesanan.oid:
                ditemukan = True
                break
            j += 1

        if not ditemukan:
            ada_perubahan = True

            if jenis == "UNDO":
                print("Undo: penambahan dibatalkan atau pesanan dikeluarkan:", pesanan)
            else:
                print("Redo: pesanan dikeluarkan atau penambahan dibatalkan:", pesanan)

        i += 1

    i = 0
    while i < len(naif_sesudah):
        pesanan = naif_sesudah[i]
        ditemukan = False

        j = 0
        while j < len(naif_sebelum):
            if naif_sebelum[j].oid == pesanan.oid:
                ditemukan = True
                break
            j += 1

        if not ditemukan:
            ada_perubahan = True

            if jenis == "UNDO":
                print("Undo: pesanan dikembalikan atau penambahan dibatalkan:", pesanan)
            else:
                print("Redo: pesanan ditambahkan atau dikembalikan:", pesanan)

        i += 1

    # Periksa perubahan yang hanya terjadi pada antrean circular.
    i = 0
    while i < len(circular_sebelum):
        pesanan = circular_sebelum[i]
        ditemukan = False

        j = 0
        while j < len(circular_sesudah):
            if circular_sesudah[j].oid == pesanan.oid:
                ditemukan = True
                break
            j += 1

        if not ditemukan:
            ada_perubahan = True
            sudah_di_naif = False

            j = 0
            while j < len(naif_sebelum):
                if naif_sebelum[j].oid == pesanan.oid:
                    sudah_di_naif = True
                    break
                j += 1

            if not sudah_di_naif:
                if jenis == "UNDO":
                    print("Undo: perubahan antrean circular:", pesanan)
                else:
                    print("Redo: perubahan antrean circular:", pesanan)

        i += 1

    i = 0
    while i < len(circular_sesudah):
        pesanan = circular_sesudah[i]
        ditemukan = False

        j = 0
        while j < len(circular_sebelum):
            if circular_sebelum[j].oid == pesanan.oid:
                ditemukan = True
                break
            j += 1

        if not ditemukan:
            sudah_di_naif = False

            j = 0
            while j < len(naif_sesudah):
                if naif_sesudah[j].oid == pesanan.oid:
                    sudah_di_naif = True
                    break
                j += 1

            if not sudah_di_naif:
                ada_perubahan = True

                if jenis == "UNDO":
                    print("Undo: pesanan kembali pada antrean circular:", pesanan)
                else:
                    print("Redo: pesanan kembali pada antrean circular:", pesanan)

        i += 1

    if not ada_perubahan:
        print("Keadaan antrean berhasil dipulihkan.")



#cek
'''if __name__ == "__main__":
    print("=" * 50)
    print("STACK: HITUNG STRUK LEWAT POSTFIX")
    print("=" * 50)

    ekspresi = input("Masukkan ekspresi infix: ")

    try:
        postfix, langkah_konversi = infix_ke_postfix(ekspresi)
        total, langkah_hitung = hitung_postfix(postfix)

        print("\nStruk  :", ekspresi)
        print("Postfix:", postfix)
        print("TOTAL  : Rp {:,.0f}".format(total).replace(",", "."))

        print("\nLANGKAH KONVERSI INFIX KE POSTFIX")
        print("-" * 90)
        print("{:<10} {:<10} {:<35} {:<15} {}".format(
            "Langkah", "Token", "Tindakan", "Stack", "Output"
        ))

        for baris in langkah_konversi:
            print("{:<10} {:<10} {:<35} {:<15} {}".format(
                baris[0], baris[1], baris[2],
                baris[3], baris[4]
            ))

        print("\nLANGKAH EVALUASI POSTFIX")
        print("-" * 90)
        print("{:<10} {:<10} {:<45} {}".format(
            "Langkah", "Token", "Tindakan", "Stack"
        ))

        for baris in langkah_hitung:
            print("{:<10} {:<10} {:<45} {}".format(
                baris[0], baris[1], baris[2], baris[3]
            ))

    except ValueError as error:
        print("Error:", error)'''



def main():
    data_awal = muat_pesanan_antre()

    queue, riwayat = buat_m2(data_awal)

    print("====================================")
    print("       PENGUJIAN BACKEND M2")
    print("====================================")
    print("Jumlah data awal :", len(data_awal))
    print("Antrean naif     :", queue.size_naif())
    print("Antrean circular :", queue.size_circular())

    while True:
        print("\n========== MENU M2 ==========")
        print("1. Stack - Postfix")
        print("2. Stack - Undo")
        print("3. Stack - Redo")
        print("4. Queue - Enqueue")
        print("5. Queue - Dequeue Naif")
        print("6. Queue - Dequeue Circular")
        print("7. Lihat Antrean (untuk pengujian)")
        print("0. Keluar")
        print("=============================")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            ekspresi = input(
                "Masukkan ekspresi infix: "
            )

            try:
                postfix, langkah = infix_ke_postfix(ekspresi)

                print("\nLangkah konversi:")
                i = 0
                while i < len(langkah):
                    print(langkah[i])
                    i += 1

                print("\nHasil postfix:", postfix)

                hasil = hitung_postfix(postfix)
                print("Hasil perhitungan:", hasil)

            except (ValueError, ZeroDivisionError) as error:
                print("Ekspresi tidak valid:", error)

        elif pilihan == "2":
            hasil = riwayat.undo()
            if hasil is not None:
                print("\nUndo berhasil.")
            else:
                print("Tidak ada perubahan yang bisa di-undo.")

        elif pilihan == "3":
            hasil = riwayat.redo()
            if hasil is not None:
                print("\nRedo berhasil.")
            else:
                print("Tidak ada perubahan yang bisa di-redo.")

        elif pilihan == "4":
            fitur_enqueue(queue, riwayat)

        elif pilihan == "5":
            fitur_dequeue_naif(queue, riwayat)

        elif pilihan == "6":
            fitur_dequeue_circular(queue, riwayat)

        elif pilihan == "7":
            tampilkan_antrean(queue)

        elif pilihan == "0":
            print("Program M2 selesai.")
            break

        else:
            print("Pilihan tidak valid. Masukkan angka 0 sampai 7.")


if __name__ == "__main__":
    main()