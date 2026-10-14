import csv
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

    def nilai_kunci(self, kunci):
        if kunci == "oid":
            return self.oid
        if kunci == "harga":
            return self.harga
        if kunci == "selesai":
            return float("inf") if self.t_selesai_detik < 0 else self.t_selesai_detik
        raise ValueError("Kunci tidak dikenal: " + str(kunci))

    def __str__(self):
        selesai = "-" if self.t_selesai_detik < 0 else str(self.t_selesai_detik)
        return (self.oid + " | " + self.pelanggan + " | " + self.resto +
                " | " + self.menu + " | Rp" + format(self.harga, ",").replace(",", ".") +
                " | prioritas=" + str(self.prioritas) +
                " | masuk=" + str(self.t_masuk_detik) +
                " | selesai=" + selesai + " | " + self.status)    



def muat_pesanan():
    data = []
    with open("data/pesanan.csv", "r", encoding="utf-8-sig", newline="") as file:
        pembaca = csv.DictReader(file)

        for baris in pembaca:
            selesai_teks = (baris["t_selesai_detik"] or "").strip()
            selesai = -1 if selesai_teks == "" else int(selesai_teks)
            pesanan = Pesanan(
                baris["oid"].strip(), baris["pelanggan"].strip(),
                baris["resto"].strip(), baris["menu"].strip(),
                int(baris["harga"]), int(baris["prioritas"]),
                int(baris["t_masuk_detik"]), selesai, baris["status"].strip()
            )
            data.append(pesanan)
    return data



def _nilai(item, kunci):
    if hasattr(item, "nilai_kunci"):
        return item.nilai_kunci(kunci)
    # Memudahkan algoritma diuji dengan angka/string sederhana.
    return item



def insertion_sort(larik, kunci="selesai"):
    perbandingan = 0
    geser = 0
    i = 1
    while i < len(larik):
        nilai = larik[i]
        nilai_kunci = _nilai(nilai, kunci)
        j = i - 1
        while j >= 0:
            perbandingan += 1
            if _nilai(larik[j], kunci) > nilai_kunci:
                larik[j + 1] = larik[j]
                geser += 1
                j -= 1
            else:
                break
        larik[j + 1] = nilai
        geser += 1
        i += 1
    return larik, perbandingan, geser



def merge_sort(larik, kunci="selesai"):
    n = len(larik)
    if n <= 1:
        return larik[:], 0, 0

    sumber = larik[:]
    tujuan = [None] * n
    lebar = 1
    perbandingan = 0
    pemindahan = 0

    while lebar < n:
        awal = 0
        while awal < n:
            tengah = awal + lebar
            akhir = awal + 2 * lebar
            if tengah > n:
                tengah = n
            if akhir > n:
                akhir = n
            kiri = awal
            kanan = tengah
            posisi = awal

            while kiri < tengah and kanan < akhir:
                perbandingan += 1
                # <= membuat elemen kiri didahulukan saat kunci sama (stabil).
                if _nilai(sumber[kiri], kunci) <= _nilai(sumber[kanan], kunci):
                    tujuan[posisi] = sumber[kiri]
                    kiri += 1
                else:
                    tujuan[posisi] = sumber[kanan]
                    kanan += 1
                posisi += 1
                pemindahan += 1

            while kiri < tengah:
                tujuan[posisi] = sumber[kiri]
                kiri += 1
                posisi += 1
                pemindahan += 1

            while kanan < akhir:
                tujuan[posisi] = sumber[kanan]
                kanan += 1
                posisi += 1
                pemindahan += 1
            awal += 2 * lebar

        sumber, tujuan = tujuan, sumber
        lebar *= 2

    return sumber, perbandingan, pemindahan



def linear_search(larik, target, kunci="oid"):
    perbandingan = 0
    i = 0
    while i < len(larik):
        perbandingan += 1
        if _nilai(larik[i], kunci) == target:
            return i, perbandingan
        i += 1
    return -1, perbandingan



def binary_search(larik_terurut, target, kunci="oid"):
    kiri = 0
    kanan = len(larik_terurut) - 1
    perbandingan = 0
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        nilai_tengah = _nilai(larik_terurut[tengah], kunci)
        perbandingan += 1
        if nilai_tengah == target:
            return tengah, perbandingan
        if nilai_tengah < target:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return -1, perbandingan



def format_waktu(detik):
    if detik < 0:
        return "-"
    jam = detik // 3600
    menit = (detik % 3600) // 60
    sisa = detik % 60
    return "%02d:%02d:%02d" % (jam, menit, sisa)



def _kunci_valid(kunci):
    return kunci == "oid" or kunci == "harga" or kunci == "selesai"



def _cetak_data(data):
    i = 0
    while i < len(data):
        print("%d. %s" % (i + 1, data[i]))
        i += 1



#cek
def jalankan_uji():
    print("=== PENGECEKAN OTOMATIS M3 ===")
    total_uji = 0
    lulus = 0

    def cek(nama, kondisi, detail=""):
        nonlocal total_uji, lulus
        total_uji += 1
        if kondisi:
            lulus += 1
            print("[LULUS] " + nama + (": " + detail if detail else ""))
        else:
            print("[GAGAL] " + nama + (": " + detail if detail else ""))

    angka = [5, 2, 4, 2, 1]
    hasil_i, banding_i, geser_i = insertion_sort(angka[:], "nilai")
    cek("Insertion sort", hasil_i == [1, 2, 2, 4, 5],
        "hasil=%s, perbandingan=%d" % (hasil_i, banding_i))

    hasil_m, banding_m, pindah_m = merge_sort([5, 2, 4, 2, 1], "nilai")
    cek("Merge sort", hasil_m == [1, 2, 2, 4, 5],
        "hasil=%s, perbandingan=%d" % (hasil_m, banding_m))

    sampel = ["O-000001", "O-000002", "O-000003", "O-000004"]
    idx_l, banding_l = linear_search(sampel, "O-000003", "nilai")
    cek("Linear search ditemukan", idx_l == 2, "indeks=%d, perbandingan=%d" % (idx_l, banding_l))
    idx_t, banding_t = binary_search(sampel, "O-000004", "nilai")
    cek("Binary search ditemukan", idx_t == 3, "indeks=%d, perbandingan=%d" % (idx_t, banding_t))
    idx_k, _ = binary_search(sampel, "O-999999", "nilai")
    cek("Binary search target tidak ada", idx_k == -1)
    cek("Kasus larik kosong", binary_search([], "O-1", "nilai")[0] == -1)

    # Uji stabilitas: dua item berkunci sama mempertahankan urutan asal.
    class ItemUji:
        def __init__(self, kunci, nama):
            self.kunci = kunci
            self.nama = nama
        def nilai_kunci(self, k):
            return self.kunci

    data_stabil = [ItemUji(2, "A"), ItemUji(1, "B"), ItemUji(2, "C")]
    stabil_i, _, _ = insertion_sort(data_stabil[:], "nilai")
    stabil_m, _, _ = merge_sort(data_stabil[:], "nilai")
    cek("Insertion sort stabil", [x.nama for x in stabil_i] == ["B", "A", "C"])
    cek("Merge sort stabil", [x.nama for x in stabil_m] == ["B", "A", "C"])

    print("\nHASIL: %d/%d pengujian lulus." % (lulus, total_uji))
    return lulus == total_uji



def menu_terminal():
    data = muat_pesanan()

    print("Jumlah data pesanan:", len(data))

    while True:
        print("\n=== M3 - LAPORAN, SORT DAN SEARCH ===")
        print("1. Insertion sort")
        print("2. Merge sort")
        print("3. Linear search berdasarkan OID")
        print("4. Binary search berdasarkan OID")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "0":
            print("Program M3 selesai.")
            break

        elif pilihan == "1" or pilihan == "2":

            try:
                jumlah = int(input("Masukkan jumlah data yang ingin diurutkan: "))
            except ValueError:
                print("Jumlah data harus berupa angka.")
                continue

            if jumlah < 1 or jumlah > len(data):
                print("Jumlah data harus antara 1 dan %d." % len(data))
                continue

            if pilihan == "1" and jumlah > 20000:
                print("DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh")
                continue

            print("Pilih kunci: oid / harga / selesai")
            kunci = input("Kunci: ").strip().lower()
            if not _kunci_valid(kunci):
                print("Kunci tidak valid.")
                continue

            salinan = data[:jumlah]
            mulai = time.perf_counter()
            if pilihan == "1":
                hasil, perbandingan, pemindahan = insertion_sort(salinan, kunci)
                nama = "Insertion sort"
            else:
                hasil, perbandingan, pemindahan = merge_sort(salinan, kunci)
                nama = "Merge sort"

            ms = (time.perf_counter() - mulai) * 1000

            print("\n%s selesai." % nama)
            print("Jumlah data: %d | Kunci: %s" % (len(hasil), kunci))
            print("Perbandingan: %d | Pemindahan: %d | Waktu: %.3f ms" % (perbandingan, pemindahan, ms))
            _cetak_data(hasil)

        elif pilihan == "3":
            target = input("Masukkan OID  : ").strip()

            mulai = time.perf_counter()
            indeks, perbandingan = linear_search(data, target, "oid")
            ms = (time.perf_counter() - mulai) * 1000

            if indeks >= 0:
                print("Ditemukan di indeks %d: %s" % (indeks, data[indeks]))
            else:
                print("Pesanan tidak ditemukan.")
            print("Perbandingan: %d | Waktu: %.3f ms" % (perbandingan, ms))

        elif pilihan == "4":
            target = input("Masukkan OID  : ").strip()

            mulai_sort = time.perf_counter()
            terurut, banding_sort, pindah_sort = merge_sort(data[:], "oid")
            ms_sort = (time.perf_counter() - mulai_sort) * 1000
            mulai = time.perf_counter()
            indeks, perbandingan = binary_search(terurut, target, "oid")
            ms = (time.perf_counter() - mulai) * 1000

            if indeks >= 0:
                print("Ditemukan di baris terurut %d: %s" % (indeks, terurut[indeks]))
            else:
                print("Pesanan tidak ditemukan.")

            print("Biaya persiapan merge sort: %d perbandingan, %.3f ms" % (banding_sort, ms_sort))
            print("Binary search: %d perbandingan, %.3f ms" % (perbandingan, ms))

        else:
            print("Pilihan tidak valid. Coba lagi.")



if __name__ == "__main__":
    menu_terminal()