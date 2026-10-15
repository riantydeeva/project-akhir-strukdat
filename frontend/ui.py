import os
import time
import tkinter as tk
from tkinter import ttk

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_KANDIDAT_ROOT = (_SCRIPT_DIR, os.path.dirname(_SCRIPT_DIR))
_ROOT_PROYEK = next(
    (p for p in _KANDIDAT_ROOT if os.path.isdir(os.path.join(p, "backend"))),
    os.path.dirname(_SCRIPT_DIR),
)
os.chdir(_ROOT_PROYEK)

from backend import m1_pesanan as m1
from backend import m2_antrean as m2
from backend import m3_laporan as m3

# ---------- warna ----------
BIRU = "#1f3d5c"
BIRU_TEKS = "#5b6f86"
PUTIH = "#ffffff"
ABU_BG = "#f2f2f2"
GARIS = "#c8c8c8"
AKTIF = "#dce9f5"
KUNING = "#fff8e1"

# kolom tabel langkah: nama, lebar, rata, ikut melebar
KOLOM_LANGKAH = (
    ("langkah", 70, "w", False),
    ("token", 70, "center", False),
    ("tindakan", 360, "w", True),
    ("stack", 140, "w", False),
    ("output", 240, "w", True),
)

KOLOM_PESANAN = (               # id, lebar, rata, ikut melebar
    ("no", 50, "center", False),
    ("oid", 110, "w", False),
    ("pelanggan", 200, "w", True),
    ("resto", 150, "w", True),
    ("menu", 150, "w", True),
    ("masuk", 100, "center", False),
)

KOLOM_SORT = (
    ("no", 50, "center", False),
    ("oid", 110, "w", False),
    ("harga", 100, "e", False),
    ("selesai", 100, "center", False),
    ("resto", 150, "w", True),
    ("menu", 150, "w", True),
)

PILIHAN = {"Diurutkan menurut": ("oid", "harga", "selesai")}

TANPA_JUDUL = {"m2_postfix", "m2_naif", "m2_circular", "m3_insertion", "m3_merge"}

# catatan kuning di bawah log, per menu
CATATAN = {
    "m2_postfix": (
        "Baris 1.x adalah tahap konversi, baris 2.x tahap evaluasi. "
        "Tahap 1 menahan operator di stack sampai gilirannya tiba. "
        "Tahap 2 menumpuk angka, dan setiap operator mengambil dua nilai teratas. "
        "Operand kanan selalu keluar lebih dulu."
    ),
}

# ---------- FONT ----------
FONT = "Segoe UI"
FONT_TITLE = (FONT, 17, "bold")
FONT_SUBTITLE = (FONT, 10)
FONT_MENU = (FONT, 10)
FONT_LABEL = (FONT, 10, "bold")
FONT_INPUT = (FONT, 11)
FONT_BUTTON = (FONT, 10, "bold")
FONT_OUTPUT = ("Consolas", 10)
FONT_LOG = ("Consolas", 9)

# ---------- helper format ----------
NAMA_PRIORITAS = {1: "VIP", 2: "PRIORITAS", 3: "REGULER"}


def jenis(p):

    try:

        return NAMA_PRIORITAS.get(int(p.prioritas), str(p.prioritas))

    except (TypeError, ValueError):

        return str(p.prioritas)


def baris(p):

    return "%s | %s | %s | %s | %s | %s" % (
        p.oid,
        p.pelanggan,
        p.resto,
        p.menu,
        jenis(p),
        p.status,
    )


m2.Pesanan.__str__ = baris

def angka(n):

    return format(n, ",").replace(",", ".")

def rupiah(n):

    return "Rp" + format(n, ",").replace(",", ".")


def detail(p):

    if p is None:

        return "Pesanan tidak ditemukan."

    return "\n".join(
        [
            "OID           : " + p.oid,
            "Pelanggan     : " + p.pelanggan,
            "Restoran      : " + p.resto,
            "Menu          : " + p.menu,
            "Harga         : " + rupiah(p.harga),
            "Prioritas     : " + jenis(p),
            "Waktu masuk   : " + m3.format_waktu(p.t_masuk_detik),
            "Waktu selesai : " + m3.format_waktu(p.t_selesai_detik),
            "Status        : " + p.status,
        ]
    )


def tabel(daftar, maks=100):

    out = []

    for i in range(min(len(daftar), maks)):

        out.append("%d. %s" % (i + 1, daftar[i]))

    if len(daftar) > maks:

        out.append("... dan %d lainnya" % (len(daftar) - maks))

    return out


# ---------- konfigurasi menu ----------
KET = {
    "reguler": (
        "REGULER",
        "masuk paling belakang",
        "append: pesanan biasa mengantre di barisan paling belakang.",
    ),
    "prioritas": (
        "PRIORITAS",
        "masuk ke tengah antrean",
        "insert di posisi n // 2: pesanan prioritas menyalip separuh antrean.",
    ),
    "vip": (
        "VIP",
        "masuk paling depan",
        "insert di indeks 0: pesanan VIP langsung di depan, sisanya digeser.",
    ),
}


def _item_m1(struktur, nama):

    s = struktur.upper()

    items = [
        (
            struktur + "_lihat",
            s + " - LIHAT PESANAN",
            nama + ": lihat pesanan",
            "Ambil satu pesanan berdasarkan indeks (ke-i).",
            [("Indeks", "", "mulai dari 0")],
            "LIHAT",
        )
    ]

    for j in ("reguler", "prioritas", "vip"):

        jn, ket, desk = KET[j]

        items.append(
            (
                struktur + "_" + j,
                s + " - TAMBAH PESANAN " + jn,
                "%s: pesanan %s, %s" % (nama, jn, ket),
                desk,
                [
                    ("Nama pelanggan", "", "Nama pelanggan"),
                    ("Restoran", "", "Nama restoran"),
                    ("Menu", "", "Nama makanan atau minuman"),
                    ("Harga", "", "Harga pesanan dalam rupiah"),
                ],
                "TAMBAH",
            )
        )

    items.append(
        (
            struktur + "_hapus",
            s + " - HAPUS PESANAN",
            nama + ": hapus pesanan",
            "Hapus pesanan ke-i, sisanya digeser.",
            [("Indeks", "", "mulai dari 0")],
            "HAPUS",
        )
    )

    return items


MENU = [
    (
        "DATA",
        [
            (
                "load",
                "Load",
                "Load data",
                "Muat data/pesanan.csv ke M1, M2, dan M3.",
                [],
                "LOAD",
            ),
        ],
    ),
    (
        "M1 - DATA PESANAN",
        _item_m1("array", "Array") + _item_m1("linkedlist", "Linked list"),
    ),
    (
        "M2 - ANTREAN DAN UNDO",
        [
            (
                "m2_postfix",
                "STACK - POSTFIX (MESIN KASIR)",
                "Stack: hitung struk lewat postfix",
                "Struk ditulis infix, lalu dihitung dua tahap dengan stack: "
                "tahap 1 infix menjadi postfix, tahap 2 postfix dievaluasi.",
                [
                    (
                        "Struk belanja (infix)",
                        "",
                        "angka, + - * / dan tanda kurung; ",
                    )
                ],
                "HITUNG",
            ),
            (
                "m2_isi",
                "QUEUE - ENQUEUE",
                "Queue: enqueue",
                "Masukkan pesanan ke belakang antrean naif dan circular.",
                [
                    ("Nama pelanggan", "", "Nama pelanggan"),
                    ("Restoran", "", "Nama restoran"),
                    ("Menu", "", "Nama makanan atau minuman"),
                    ("Harga", "", "Harga pesanan dalam rupiah"),
                ],
                "ENQUEUE",
            ),
            (
                "m2_undo",
                "STACK - UNDO",
                "Stack: undo",
                "Batalkan perubahan antrean terakhir.",
                [],
                "UNDO",
            ),
            (
                "m2_redo",
                "STACK - REDO",
                "Stack: redo",
                "Ulangi perubahan yang tadi di-undo.",
                [],
                "REDO",
            ),
            (
                "m2_naif",
                "QUEUE - DEQUEUE NAIF",
                "Queue naif: ambil dari depan dengan menggeser isi",
                "Mengambil indeks 0 lalu menggeser seluruh sisa isi satu petak ke kiri. "
                "Biayanya O(n) setiap kali.",
                [("Berapa kali dequeue", "",
                "sampai panjang antrean; coba 1 lalu 100 untuk melihat bedanya")],
                "DEQUEUE",
            ),
            (
                "m2_circular",
                "QUEUE - DEQUEUE CIRCULAR",
                "Queue circular: ambil dari depan dengan memajukan penunjuk",
                "Hanya menggeser penunjuk depan satu petak, tanpa menggeser isi. "
                "Biayanya O(1) setiap kali.",
                [("Berapa kali dequeue", "",
                "sampai panjang antrean; bandingkan waktunya dengan dequeue naif")],
                "DEQUEUE",
            ),
        ],
    ),
    (
        "M3 - LAPORAN DAN PENCARIAN",
        [
            (
                "m3_insertion",
                "SORT - INSERTION SORT",
                "Sort: insertion sort, O(n²)",
                "Setiap elemen digeser mundur sampai menemukan tempatnya. "
                "Sederhana, tetapi kerjanya tumbuh kuadratik.",
                [
                    ("Jumlah baris diurutkan", "",
                    "diambil dari awal data; coba 1.000 lalu 2.000 lalu 4.000"),
                    ("Diurutkan menurut", "pilih",
                    "oid (abjad), harga (angka), selesai (waktu selesai)"),
                ],
                "URUTKAN",
            ),
            (
                "m3_merge",
                "SORT - MERGE SORT",
                "Sort: merge sort, O(n log n)",
                "Data dibagi dua terus-menerus, lalu digabung kembali secara berurutan.",
                [
                    ("Jumlah baris diurutkan", "",
                    "diambil dari awal data; boleh sampai seluruh data"),
                    ("Diurutkan menurut", "pilih",
                    "oid (abjad), harga (angka), selesai (waktu selesai)"),
                ],
                "URUTKAN",
            ),
            (
                "m3_linear",
                "SEARCH - LINEAR SEARCH",
                "Search: linear search",
                "Cari OID dari indeks pertama sampai ketemu.",
                [("OID", "", "oid yang dicari")],
                "CARI",
            ),
            (
                "m3_binary",
                "SEARCH - BINARY SEARCH",
                "Search: binary search",
                "Data diurutkan per OID dulu (merge sort), lalu dicari dengan binary search.",
                [("OID", "", "oid yang dicari")],
                "CARI",
            ),
        ],
    ),
]

STUB = {"m4_hash", "m4_cari", "m5_menu", "m5_prioritas", "m6_peta"}

BUTUH_LOAD = {
    "m2_isi",
    "m2_undo",
    "m2_redo",
    "m2_naif",
    "m2_circular",
    "m3_insertion",
    "m3_merge",
    "m3_linear",
    "m3_binary",
}

LABEL_M1 = {"array": "M1 - array", "linkedlist": "M1 - linked list"}


class App(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("2EZ4U Food Delivery")

        self.geometry("1100x700")
        self.resizable(True, True)

        self.configure(bg=ABU_BG)

        # ---- state backend ----

        self.m1 = m1.M1Pesanan()

        self.queue = None

        self.riwayat = None

        self.data3 = None

        self.terurut_oid = None

        self.dimuat = False

        self.info_waktu = ""

        self.no_baru = 0

        self.items = {}

        for _, daftar in MENU:

            for it in daftar:

                self.items[it[0]] = it

        self.aksi = {
            "load": self.h_load,
            "m2_postfix": self.h_postfix,
            "m2_isi": self.h_isi,
            "m2_undo": lambda v: self.h_ubah("undo"),
            "m2_redo": lambda v: self.h_ubah("redo"),
            "m2_naif": lambda v: self.h_dequeue("naif", v),
            "m2_circular": lambda v: self.h_dequeue("circular", v),
            "m3_insertion": lambda v: self.h_sort("insertion", v),
            "m3_merge": lambda v: self.h_sort("merge", v),
            "m3_linear": self.h_linear,
            "m3_binary": self.h_binary,
        }

        for s in ("array", "linkedlist"):

            self.aksi[s + "_lihat"] = lambda v, s=s: self.h_lihat(s, v)

            self.aksi[s + "_hapus"] = lambda v, s=s: self.h_hapus(s, v)

            for j in ("reguler", "prioritas", "vip"):

                self.aksi[s + "_" + j] = lambda v, s=s, j=j: self.h_tambah(s, j, v)

        for k in STUB:

            self.aksi[k] = lambda v, k=k: self.h_stub(k, v)

        self.item_btns = {}

        self.entries = []

        self.aktif = None

        self._buat_header()

        self._buat_status()

        self._buat_badan()

        self._buat_sidebar()

        self._buat_konten()

    # ================= kerangka UI =================

    def _buat_header(self):
        h = tk.Frame(self, bg=BIRU, height=48)
        h.pack(fill="x")
        h.pack_propagate(False)
        tk.Label(
            h, text="2EZ4U Food Delivery", bg=BIRU, fg=PUTIH, font=FONT_TITLE
        ).pack(side="left", padx=16)

    def _buat_status(self):
        s = tk.Frame(self, bg=ABU_BG, height=30)
        s.pack(side="bottom", fill="x")
        self.status = tk.Label(
            s, text="Siap", bg=ABU_BG, fg=BIRU_TEKS, font=(FONT, 9, "bold"), anchor="w"
        )
        self.status.pack(side="left", padx=12, pady=5)

    def _buat_badan(self):
        self.badan = tk.Frame(self, bg=ABU_BG)
        self.badan.pack(fill="both", expand=True, padx=10, pady=(8, 4))
        self.badan.columnconfigure(1, weight=1)
        self.badan.rowconfigure(0, weight=1)

    def _buat_sidebar(self):
        wadah = tk.Frame(
            self.badan,
            bg=PUTIH,
            width=320,
            highlightthickness=1,
            highlightbackground=GARIS,
        )
        wadah.grid(row=0, column=0, sticky="ns")
        wadah.grid_propagate(False)
        wadah.rowconfigure(0, weight=1)
        wadah.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(wadah, bg=PUTIH, highlightthickness=0, width=298)
        sb = tk.Scrollbar(wadah, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        dalam = tk.Frame(self.canvas, bg=PUTIH, padx=10, pady=10)
        self.jendela_menu = self.canvas.create_window(
            (0, 0), window=dalam, anchor="nw", width=298
        )
        self.dalam_menu = dalam

        def perbarui_scrollregion(_event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def perbarui_lebar(event):
            self.canvas.itemconfigure(self.jendela_menu, width=event.width)

        dalam.bind("<Configure>", perbarui_scrollregion)
        self.canvas.bind("<Configure>", perbarui_lebar)

        # Roda mouse bekerja ketika kursor berada di area menu.
        def ikat_scroll(widget):
            widget.bind("<MouseWheel>", self._scroll)
            widget.bind("<Button-4>", self._scroll_linux)
            widget.bind("<Button-5>", self._scroll_linux)

        ikat_scroll(self.canvas)
        ikat_scroll(dalam)

        for grup, daftar in MENU:
            lbl_grup = tk.Label(
                dalam,
                text=grup,
                bg=PUTIH,
                fg=BIRU_TEKS,
                font=(FONT, 9, "bold"),
                anchor="w",
                padx=8,
                pady=8,
            )
            lbl_grup.pack(fill="x", pady=(5, 2))
            ikat_scroll(lbl_grup)

            for it in daftar:
                key, label = it[0], it[1]
                btn = tk.Button(
                    dalam,
                    text=label,
                    command=lambda k=key: self.pilih(k),
                    font=FONT_MENU,
                    bg=PUTIH,
                    fg="#243447",
                    activebackground=AKTIF,
                    activeforeground=BIRU,
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=12,
                    pady=7,
                    cursor="hand2",
                    wraplength=260,
                    justify="left",
                    highlightthickness=0,
                )
                btn.pack(fill="x", pady=1)
                self.item_btns[key] = btn
                ikat_scroll(btn)

    def _scroll(self, event):
        if event.delta:
            # Windows: delta biasanya kelipatan 120; tetap gulir satu langkah.
            langkah = -1 if event.delta > 0 else 1
            self.canvas.yview_scroll(langkah, "units")
        return "break"

    def _scroll_linux(self, event):
        self.canvas.yview_scroll(-1 if event.num == 4 else 1, "units")
        return "break"

    def _buat_konten(self):

        kanan = tk.Frame(self.badan, bg=ABU_BG)

        kanan.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        kanan.rowconfigure(1, weight=1)

        kanan.columnconfigure(0, weight=1)

        self.panel = tk.Frame(
            kanan, bg=PUTIH, highlightthickness=1, highlightbackground=GARIS
        )

        self.panel.grid(row=0, column=0, sticky="ew")

        self.lbl_judul = tk.Label(
            self.panel,
            text="Pilih menu di sebelah kiri",
            bg=PUTIH,
            font=(FONT, 13, "bold"),
            anchor="w",
        )

        self.lbl_judul.pack(fill="x", padx=14, pady=(12, 0))

        self.lbl_desk = tk.Label(
            self.panel, text="", bg=PUTIH, fg=BIRU_TEKS, font=(FONT, 9), anchor="w"
        )

        self.lbl_desk.pack(fill="x", padx=14, pady=(2, 8))

        self.form = tk.Frame(self.panel, bg=PUTIH)

        self.form.pack(fill="x", padx=14, pady=(0, 14))

        out = tk.Frame(kanan, bg=PUTIH, highlightthickness=1, highlightbackground=GARIS)

        self.out = out

        out.grid(row=1, column=0, sticky="nsew", pady=(10, 6))

        out.rowconfigure(0, weight=1)

        out.columnconfigure(0, weight=1)

        self.output = tk.Text(
            out,
            bg=PUTIH,
            relief="flat",
            wrap="none",
            font=FONT_OUTPUT,
            state="disabled",
        )

        ys = tk.Scrollbar(out, orient="vertical", command=self.output.yview)

        xs = tk.Scrollbar(out, orient="horizontal", command=self.output.xview)

        self.output.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)

        self.output.grid(row=0, column=0, sticky="nsew")

        ys.grid(row=0, column=1, sticky="ns")

        xs.grid(row=1, column=0, sticky="ew")

        self.xs_output = xs

        # ---- tabel langkah (dipakai menu postfix) ----

        self.wadah_tabel = tk.Frame(out, bg=PUTIH)

        self.wadah_tabel.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.wadah_tabel.rowconfigure(0, weight=1)

        self.wadah_tabel.columnconfigure(0, weight=1)

        gaya = ttk.Style(self)

        gaya.theme_use("clam")

        gaya.configure(
            "Langkah.Treeview",
            font=FONT_OUTPUT,
            rowheight=20,
            background=PUTIH,
            fieldbackground=PUTIH,
            borderwidth=0,
        )

        gaya.configure(
            "Langkah.Treeview.Heading",
            font=(FONT, 10, "bold"),
            background=PUTIH,
            relief="solid",
            borderwidth=1,
        )

        self.tabel = ttk.Treeview(
            self.wadah_tabel,
            columns=[k[0] for k in KOLOM_LANGKAH],
            show="headings",
            style="Langkah.Treeview",
        )

        for nama, lebar, rata, melebar in KOLOM_LANGKAH:

            self.tabel.heading(nama, text=nama, anchor="center")

            self.tabel.column(nama, width=lebar, anchor=rata, stretch=melebar)

        ty = tk.Scrollbar(self.wadah_tabel, orient="vertical", command=self.tabel.yview)

        tx = tk.Scrollbar(
            self.wadah_tabel, orient="horizontal", command=self.tabel.xview
        )

        self.tabel.configure(yscrollcommand=ty.set, xscrollcommand=tx.set)

        self.tabel.grid(row=0, column=0, sticky="nsew")

        ty.grid(row=0, column=1, sticky="ns")

        tx.grid(row=1, column=0, sticky="ew")

        self.wadah_tabel.grid_remove()

        tk.Label(
            kanan,
            text="COMMAND",
            bg=ABU_BG,
            fg=BIRU_TEKS,
            anchor="w",
            font=(FONT, 9, "bold"),
        ).grid(row=2, column=0, sticky="w")

        logf = tk.Frame(
            kanan, bg=PUTIH, highlightthickness=1, highlightbackground=GARIS
        )

        logf.grid(row=3, column=0, sticky="ew", pady=(2, 6))

        logf.columnconfigure(0, weight=1)

        self.log = tk.Text(
            logf, height=2, bg=PUTIH, relief="flat", font=FONT_LOG, state="disabled"
        )

        ls = tk.Scrollbar(logf, orient="vertical", command=self.log.yview)

        self.log.configure(yscrollcommand=ls.set)

        self.log.grid(row=0, column=0, sticky="ew")

        ls.grid(row=0, column=1, sticky="ns")

        # ---- kotak catatan kuning ----

        self.lbl_catatan = tk.Label(
            kanan,
            text="",
            bg=KUNING,
            fg=BIRU_TEKS,
            font=(FONT, 9),
            anchor="w",
            justify="left",
            padx=12,
            pady=8,
        )

        self.lbl_catatan.grid(row=4, column=0, sticky="ew")

        self.lbl_catatan.grid_remove()

        kanan.bind(
            "<Configure>",
            lambda e: self.lbl_catatan.configure(wraplength=max(200, e.width - 40)),
        )

    # ================= interaksi =================

    def pilih(self, key):

        # Kosongkan kotak hasil setiap kali pindah menu

        self.bersihkan()

        _, label, judul, desk, fields, tombol = self.items[key]

        if self.aktif:

            self.item_btns[self.aktif].configure(bg=PUTIH)

        self.aktif = key

        self.item_btns[key].configure(bg=AKTIF)

        self.lbl_judul.configure(text=judul)

        self.lbl_desk.configure(text=desk)

        catatan = CATATAN.get(key, "")

        self.lbl_catatan.configure(text=catatan)

        if catatan:

            self.lbl_catatan.grid()

        else:

            self.lbl_catatan.grid_remove()

        for w in self.form.winfo_children():

            w.destroy()

        self.entries = []

        kol = tk.Frame(self.form, bg=PUTIH)

        kol.pack(side="left", anchor="n")

        for lbl, default, hint in fields:

            tk.Label(kol, text=lbl, bg=PUTIH, anchor="w", font=FONT_LABEL).pack(
                fill="x", pady=(4, 0)
            )

            if lbl in PILIHAN:
                e = ttk.Combobox(kol, values=PILIHAN[lbl], state="readonly",
                                width=37, font=FONT_INPUT)
                e.set(default)
            else:
                e = tk.Entry(kol, width=40, relief="solid", bd=1, font=FONT_INPUT)
                e.insert(0, default)

            e.pack(anchor="w")

            tk.Label(
                kol, text=hint, bg=PUTIH, fg=BIRU_TEKS, anchor="w", font=(FONT, 9)
            ).pack(fill="x")

            self.entries.append(e)

        btn = tk.Button(
            self.form,
            text=tombol,
            command=lambda: self.eksekusi(key),
            bg=BIRU,
            fg=PUTIH,
            activebackground="#2d557d",
            activeforeground=PUTIH,
            cursor="hand2",
            font=FONT_BUTTON,
            padx=24,
            pady=8,
            relief="flat",
            bd=0,
        )
        btn.pack(side="left", padx=24, pady=(8, 0), anchor="center")

        self.set_status("siap")

    def eksekusi(self, key):

        if key in BUTUH_LOAD and not self.dimuat:

            self.tulis("Data belum dimuat. Klik menu Load dulu.")

            self.set_status("siap")

            return

        nilai = [e.get().strip() for e in self.entries]

        self.set_status("memproses...")

        self.update_idletasks()

        self.info_waktu = ""

        try:

            self.tulis(self.aksi[key](nilai), judul=key not in TANPA_JUDUL)

            self.set_status(self.info_waktu or "selesai")

        except Exception as ex:

            self.tulis("ERROR: %s" % ex)

            self.set_status("error")

    # ================= util =================

    def ukur(self, perintah, modul, fn):

        mulai = time.perf_counter()

        hasil = fn()

        ms = (time.perf_counter() - mulai) * 1000

        self.info_waktu = "[%s] %.2f ms" % (modul, ms)

        self.catat("%-22s -> %-18s %9.2f ms" % (perintah, modul, ms))

        return hasil

    @staticmethod
    def ke_int(teks, nama, minimum=None):

        try:

            n = int(teks)

        except ValueError:

            raise ValueError("%s harus berupa angka." % nama)

        if minimum is not None and n < minimum:

            raise ValueError("%s minimal %d." % (nama, minimum))

        return n

    def tulis(self, teks, judul=True):

        self.output.configure(state="normal")

        awal = self.output.index("end-1c")

        if judul:

            nama = self.items[self.aktif][2].upper() if self.aktif else ""

            self.output.insert("end", "=== %s ===\n%s\n\n" % (nama, teks))

        else:

            self.output.insert("end", teks + "\n")

        self.output.configure(state="disabled")

        self.output.yview(awal)  # scroll ke awal hasil terbaru

    def bersihkan(self):

        self.output.configure(state="normal")

        self.output.delete("1.0", "end")

        self.output.configure(state="disabled")

        self.tabel.delete(*self.tabel.get_children())

        self._mode_tabel(False)

    def _mode_tabel(self, aktif):

        if aktif:

            self.output.configure(height=4)

            self.xs_output.grid_remove()

            self.out.rowconfigure(0, weight=0)

            self.out.rowconfigure(2, weight=1)

            self.wadah_tabel.grid()

        else:

            self.output.configure(height=24)

            self.xs_output.grid()

            self.out.rowconfigure(0, weight=1)

            self.out.rowconfigure(2, weight=0)

            self.wadah_tabel.grid_remove()

    def _isi_tabel(self, kolom, daftar_baris):

        self.tabel.delete(*self.tabel.get_children())

        nama = [k[0] for k in kolom]

        self.tabel.configure(columns=nama, displaycolumns=nama)

        for n, lebar, rata, melebar in kolom:

            self.tabel.heading(n, text="#" if n == "no" else n, anchor="center")

            self.tabel.column(n, width=lebar, anchor=rata, stretch=melebar)

        for r in daftar_baris:

            self.tabel.insert("", "end", values=[str(x) for x in r])

        self._mode_tabel(True)

    def _catatan(self, teks):

        self.lbl_catatan.configure(text=teks)

        self.lbl_catatan.grid()

    def catat(self, teks):

        self.log.configure(state="normal")

        self.log.insert("end", teks + "\n")

        self.log.see("end")

        self.log.configure(state="disabled")

    def set_status(self, teks):

        # capitalize() akan mengecilkan "M2" jadi "m2", jadi huruf pertama saja
        self.status.configure(text=teks[:1].upper() + teks[1:])

    def _wadah(self, s):

        return self.m1.array if s == "array" else self.m1.linked_list

    # ================= LOAD =================

    def h_load(self, v):

        self.ukur("load", "M1 - larik", lambda: self.m1.load("data/pesanan.csv"))

        antre = self.ukur("load", "M2 - muat ANTRE", m2.muat_pesanan_antre)

        self.queue, self.riwayat = self.ukur(
            "load", "M2 - antrean", lambda: m2.buat_m2(antre)
        )

        self.data3 = self.ukur("load", "M3 - laporan", m3.muat_pesanan)

        self.terurut_oid = None

        self.dimuat = True

        return "\n".join(
            [
                "Data berhasil dimuat.",
                "M1 array         : %d pesanan" % self.m1.array.size(),
                "M1 linked list   : %d pesanan" % self.m1.linked_list.size(),
                "M2 antrean naif  : %d pesanan" % self.queue.size_naif(),
                "M2 antrean circ. : %d pesanan" % self.queue.size_circular(),
                "M3 laporan       : %d pesanan" % len(self.data3),
            ]
        )

    # ================= M1 =================

    def h_lihat(self, s, v):

        i = self.ke_int(v[0], "Indeks")

        wadah = self._wadah(s)

        log = "array_get" if s == "array" else "linkedlist_get"

        fn = (
            self.m1.array_lihat_pesanan
            if s == "array"
            else self.m1.linkedlist_lihat_pesanan
        )

        p = self.ukur(log, LABEL_M1[s], lambda: fn(i))

        if p is None:

            return "Indeks tidak valid. Isi 0 sampai %d." % (wadah.size() - 1)

        return "Pesanan ke-%d dari %d\n\n%s" % (i, wadah.size(), detail(p))

    def h_tambah(self, s, j, v):

        if not v[0] or not v[1] or not v[2]:

            raise ValueError("Nama pelanggan, restoran, dan menu wajib diisi.")

        harga = self.ke_int(v[3], "Harga", 0)

        self.no_baru += 1

        prioritas = {"vip": 1, "prioritas": 2, "reguler": 3}[j]

        p = m1.Pesanan(
            "N-%06d" % self.no_baru,
            v[0],
            v[1],
            v[2],
            harga,
            prioritas,
            int(time.time()) % 86400,
            -1,
            "ANTRE",
        )

        wadah = self._wadah(s)

        n = wadah.size()

        pos = {"reguler": n, "prioritas": n // 2, "vip": 0}[j]

        kode = {
            "reguler": "append",
            "prioritas": "insert_prioritas",
            "vip": "insert_vip",
        }[j]

        fn = getattr(self.m1, "%s_tambah_%s" % (s, j))

        self.ukur("%s_%s" % (s, kode), LABEL_M1[s], lambda: fn(p))

        out = [
            "Pesanan %s berhasil ditambahkan di indeks %d." % (j.upper(), pos),
            "Jumlah sekarang: %d" % wadah.size(),
            "",
            "Sekitar posisi baru:",
        ]

        for i in range(max(0, pos - 1), min(wadah.size(), pos + 2)):

            tanda = ">>" if i == pos else "  "

            out.append("%s %d: %s" % (tanda, i, baris(wadah.get(i))))

        return "\n".join(out)

    def h_hapus(self, s, v):

        i = self.ke_int(v[0], "Indeks")

        wadah = self._wadah(s)

        log = "array_remove" if s == "array" else "linkedlist_remove"

        fn = (
            self.m1.array_hapus_pesanan
            if s == "array"
            else self.m1.linkedlist_hapus_pesanan
        )

        p = self.ukur(log, LABEL_M1[s], lambda: fn(i))

        if p is None:

            return "Indeks tidak valid."

        return "Pesanan berhasil dihapus:\n\n%s\n\nJumlah sekarang: %d" % (
            detail(p),
            wadah.size(),
        )

    # ================= M2 =================

    def h_isi(self, v):

        if not v[0] or not v[1] or not v[2]:

            raise ValueError("Nama pelanggan, restoran, dan menu wajib diisi.")

        harga = self.ke_int(v[3], "Harga", 0)

        jumlah = 1

        q = self.queue

        if q.jumlah + jumlah > q.kapasitas:

            raise ValueError(
                "Antrean penuh. Sisa kapasitas: %d" % (q.kapasitas - q.jumlah)
            )

        baru = []

        for _ in range(jumlah):

            self.no_baru += 1

            baru.append(
                m2.Pesanan(
                    "N-%06d" % self.no_baru,
                    v[0],
                    v[1],
                    v[2],
                    harga,
                    3,
                    int(time.time()) % 86400,
                    -1,
                    "ANTRE",
                )
            )

        self.riwayat.simpan_sebelum()

        def isi():

            for p in baru:

                if not q.enqueue(p):

                    return False

            return True

        if not self.ukur("enqueue x%d" % jumlah, "M2 - antrean", isi):

            self.riwayat.batalkan_simpan()

            raise ValueError("Antrean penuh. Pesanan gagal ditambahkan.")

        out = [
            "%d pesanan ditambahkan ke belakang antrean." % jumlah,
            "Antrean naif     : %d" % q.size_naif(),
            "Antrean circular : %d" % q.size_circular(),
            "",
            "Pesanan yang masuk:",
        ]

        out += tabel(baru, len(baru))

        return "\n".join(out)

    def h_dequeue(self, mode, v):

        self.bersihkan()

        jumlah = self.ke_int(v[0], "Jumlah", 1)

        q = self.queue

        if mode == "naif":

            tersedia, fn = q.size_naif(), q.dequeue_naif

        else:

            tersedia, fn = q.size_circular(), q.dequeue_circular

        if tersedia == 0:

            return "Antrean %s kosong." % mode

        if jumlah > tersedia:

            raise ValueError("Jumlah melebihi antrean. Pesanan tersedia: %d" % tersedia)

        self.riwayat.simpan_sebelum()

        keluar = []

        def jalan():

            for _ in range(jumlah):

                keluar.append(fn())

        kode = "naive" if mode == "naif" else "circular"

        self.ukur("queue_dequeue_" + kode, "M2 - queue " + mode, jalan)

        self._isi_tabel(
            KOLOM_PESANAN,
            [
                [i + 1, p.oid, p.pelanggan, p.resto, p.menu,
                m3.format_waktu(p.t_masuk_detik)]
                for i, p in enumerate(keluar)
            ],
        )

        if mode == "naif":

            # dequeue ke-i menggeser (n - 1 - i) elemen
            geser = jumlah * (tersedia - 1) - jumlah * (jumlah - 1) // 2

            return "\n".join(
                [
                    "%d pesanan keluar dari depan antrean naif." % jumlah,
                    "Total %s elemen digeser, rata-rata %s geseran per dequeue."
                    % (angka(geser), angka(geser // jumlah)),
                    "Sisa antrean naif %s." % angka(q.size_naif()),
                ]
            )

        return "\n".join(
            [
                "%d pesanan keluar dari depan antrean circular." % jumlah,
                "Penunjuk depan maju %d petak, tidak ada elemen yang digeser." % jumlah,
                "Sisa antrean circular %s." % angka(q.size_circular()),
            ]
        )

    def h_ubah(self, jenis_aksi):

        fn = self.riwayat.undo if jenis_aksi == "undo" else self.riwayat.redo

        hasil = self.ukur(jenis_aksi, "M2 - stack", fn)

        if hasil is None:

            return "Tidak ada perubahan yang bisa di-%s." % jenis_aksi

        sekarang, target = hasil

        a = {p.oid: p for p in sekarang[0]}  # sebelum aksi

        b = {p.oid: p for p in target[0]}  # sesudah aksi

        keluar = [a[o] for o in a if o not in b]

        masuk = [b[o] for o in b if o not in a]

        out = ["%s berhasil." % jenis_aksi.capitalize()]

        if keluar:

            out += ["", "Keluar dari antrean (%d):" % len(keluar)] + tabel(keluar, len(keluar))

        if masuk:

            out += ["", "Kembali ke antrean (%d):" % len(masuk)] + tabel(masuk, len(masuk))

        if not keluar and not masuk:

            out.append("Keadaan antrean berhasil dipulihkan.")

        out += [
            "",
            "Antrean naif     : %d" % self.queue.size_naif(),
            "Antrean circular : %d" % self.queue.size_circular(),
        ]

        return "\n".join(out)

    def h_postfix(self, v):

        self.bersihkan()

        ekspresi = v[0]

        def hitung():

            postfix, lk = m2.infix_ke_postfix(ekspresi)

            total, lh = m2.hitung_postfix(postfix)

            return postfix, total, lk + lh

        postfix, total, langkah = self.ukur("stack_postfix", "M2 - stack", hitung)

        self._isi_tabel(KOLOM_LANGKAH, langkah)

        return "\n".join(
            [
                "Struk  : " + ekspresi,
                "Postfix: " + postfix,
                "TOTAL  : Rp {:,.0f}".format(total).replace(",", "."),
            ]
        )

    # ================= M3 =================

    def h_sort(self, algo, v):

        self.bersihkan()

        jumlah = self.ke_int(v[0], "Jumlah data", 1)

        if jumlah > len(self.data3):

            raise ValueError("Jumlah data harus antara 1 dan %d." % len(self.data3))

        if algo == "insertion" and jumlah > 200000:

            raise ValueError(
                "DITOLAK: batasnya 200.000 baris, pakai merge sort untuk data penuh."
            )

        kunci = v[1].lower()

        if not m3._kunci_valid(kunci):

            raise ValueError("Kunci tidak valid. Pilih oid / harga / selesai.")

        salinan = self.data3[:jumlah]

        if algo == "insertion":

            hasil, banding, pindah = self.ukur(
                "insertion_sort",
                "M3 - insertion sort",
                lambda: m3.insertion_sort(salinan, kunci),
            )

        else:

            hasil, banding, pindah = self.ukur(
                "merge_sort",
                "M3 - merge sort",
                lambda: m3.merge_sort(salinan, kunci),
            )

        baris_tabel = [
            [i + 1, p.oid, angka(p.harga), m3.format_waktu(p.t_selesai_detik),
            p.resto, p.menu]
            for i, p in enumerate(hasil[:])
        ]

        self._isi_tabel(KOLOM_SORT, baris_tabel)

        return "\n".join(
            [
                "%s pesanan diurutkan menurut %s." % (angka(len(hasil)), kunci),
                "%s perbandingan, %s pemindahan." % (angka(banding), angka(pindah)),
            ]
        )

    def h_linear(self, v):

        target = v[0]

        idx, banding = self.ukur(
            "linear_search",
            "M3 - search",
            lambda: m3.linear_search(self.data3, target, "oid"),
        )

        if idx >= 0:

            hasil = "Ditemukan di indeks %d:\n%s" % (idx, self.data3[idx])

        else:

            hasil = "Pesanan tidak ditemukan."

        return "%s\n\nLinear search: %d perbandingan" % (hasil, banding)

    def h_binary(self, v):

        target = v[0]

        terurut, bs, ps = self.ukur(
            "merge_sort(oid)",
            "M3 - persiapan",
            lambda: m3.merge_sort(self.data3[:], "oid"),
        )

        idx, banding = self.ukur(
            "binary_search",
            "M3 - search",
            lambda: m3.binary_search(terurut, target, "oid"),
        )

        if idx >= 0:

            hasil = "Ditemukan di baris terurut %d:\n%s" % (idx, terurut[idx])

        else:

            hasil = "Pesanan tidak ditemukan."

        return (
            "%s\n\nBiaya persiapan merge sort: %d perbandingan, %d pemindahan\n"
            "Binary search: %d perbandingan" % (hasil, bs, ps, banding)
        )

    # ================= belum ada backend =================

    def h_stub(self, key, v):

        return "[%s]\ninput: %s\n\nBackend-nya belum ada. Sambungkan di h_stub()." % (
            self.items[key][2],
            v,
        )


if __name__ == "__main__":

    App().mainloop()