'''import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import time


class FoodDeliveryUI:
    BG = "#eef1f5"
    NAVY = "#254866"
    NAVY_DARK = "#203d58"
    TEXT = "#252b32"
    MUTED = "#667484"
    BORDER = "#c8cdd3"
    WHITE = "#ffffff"

    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        # Data contoh untuk membuat UI bisa langsung dicoba.
        self.array_orders = []
        self.linked_orders = []
        self.order_counter = 1
        self.current_page = None

        self._setup_style()
        self._build_window()
        self.show_page("ARRAY - LIHAT PESANAN")

    def _setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Sidebar.TButton",
            font=("Arial", 9),
            padding=(7, 5),
            anchor="w",
            background="#fbfbfb",
            foreground="#20252a",
            bordercolor="#b9bec4",
        )
        style.map(
            "Sidebar.TButton",
            background=[("active", "#dce6ef"), ("pressed", "#cbd9e6")],
        )
        style.configure(
            "Selected.TButton",
            font=("Arial", 9, "bold"),
            padding=(7, 5),
            anchor="w",
            background="#c8d8e7",
            foreground="#172b3c",
            bordercolor="#7892a8",
        )
        style.configure(
            "Action.TButton",
            font=("Arial", 10, "bold"),
            padding=(18, 7),
            background=self.NAVY,
            foreground="white",
            bordercolor="#17344d",
        )
        style.map(
            "Action.TButton",
            background=[("active", "#315b7d"), ("pressed", "#18344b")],
        )
        style.configure(
            "Small.TButton",
            font=("Arial", 9),
            padding=(8, 4),
        )

    def _build_window(self):

        header = tk.Frame(self.root, bg=self.NAVY, height=40)
        header.pack(fill="x", padx=12)
        header.pack_propagate(False)
        tk.Label(
            header, text="2EZ4U Food Delivery",
            bg=self.NAVY, fg="white",
            font=("Arial", 15, "bold")
        ).pack(side="left", padx=10)

        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True, padx=12, pady=(0, 0))

        # Panel kiri: daftar menu yang dapat digulir.
        self.sidebar = tk.Frame(body, bg=self.BG, width=300)
        self.sidebar.pack(side="left", fill="y", padx=(0, 7), pady=7)
        self.sidebar.pack_propagate(False)

        self.side_canvas = tk.Canvas(
            self.sidebar, bg=self.BG, highlightthickness=0, width=285
        )
        self.side_scroll = ttk.Scrollbar(
            self.sidebar, orient="vertical", command=self.side_canvas.yview
        )
        self.side_canvas.configure(yscrollcommand=self.side_scroll.set)
        self.side_scroll.pack(side="right", fill="y")
        self.side_canvas.pack(side="left", fill="both", expand=True)

        self.menu_frame = tk.Frame(self.side_canvas, bg=self.BG)
        self.menu_window = self.side_canvas.create_window(
            (0, 0), window=self.menu_frame, anchor="nw", width=280
        )
        self.menu_frame.bind(
            "<Configure>",
            lambda event: self.side_canvas.configure(
                scrollregion=self.side_canvas.bbox("all")
            )
        )
        self.side_canvas.bind(
            "<Configure>",
            lambda event: self.side_canvas.itemconfigure(
                self.menu_window, width=event.width
            )
        )

        self.menu_buttons = {}
        self._add_menu_group("DATA", [
            ("Load", self.load_csv),
        ])
        self._add_menu_group("M1 - DATA PESANAN", [
            ("ARRAY - LIHAT PESANAN", self.view_array),
            ("ARRAY - TAMBAH PESANAN REGULER", None),
            ("ARRAY - TAMBAH PESANAN PRIORITAS", None),
            ("ARRAY - TAMBAH PESANAN VIP", None),
            ("ARRAY - HAPUS PESANAN", None),
            ("LINKEDLIST - LIHAT PESANAN", self.view_linked),
            ("LINKEDLIST - TAMBAH PESANAN REGULER", None),
            ("LINKEDLIST - TAMBAH PESANAN PRIORITAS", None),
            ("LINKEDLIST - TAMBAH PESANAN VIP", None),
            ("LINKEDLIST - HAPUS PESANAN", None),
        ])
        self._add_menu_group("M2 - ANTREAN DAN UNDO", [
            ("Isi antrean FIFO", None),
            ("Layani berikutnya", None),
            ("Undo", None),
        ])
        self._add_menu_group("M3 DAN M4 - LAPORAN DAN PENCARIAN", [
            ("Laporan harian", None),
            ("Cari di laporan", None),
            ("Bangun indeks hash", None),
            ("Cari pesanan (oid)", None),
        ])
        self._add_menu_group("M5 - KATALOG DAN PRIORITAS", [
            ("Menu per rentang harga", None),
            ("Isi antrean prioritas", None),
        ])
        self._add_menu_group("M6 - PETA DAN RUTE", [
            ("Muat peta", None),
        ])

        bottom = tk.Frame(self.sidebar, bg=self.BG)
        bottom.pack(side="bottom", fill="x", pady=(6, 0))
        ttk.Button(bottom, text="siap", style="Action.TButton",
                   command=lambda: self.log_command("status", "UI siap")).pack(
                       side="left", padx=2, pady=2
                   )

        # Panel kanan.
        self.main_panel = tk.Frame(body, bg=self.WHITE, highlightbackground=self.BORDER,
                                   highlightthickness=1)
        self.main_panel.pack(side="left", fill="both", expand=True, pady=7)

        self.page_top = tk.Frame(self.main_panel, bg="#fafbfc")
        self.page_top.pack(fill="x")

        self.page_title = tk.Label(
            self.page_top, text="", bg="#fafbfc", fg=self.TEXT,
            font=("Arial", 13, "bold"), anchor="w"
        )
        self.page_title.pack(fill="x", padx=14, pady=(12, 4))

        self.page_description = tk.Label(
            self.page_top, text="", bg="#fafbfc", fg="#4d5c6b",
            font=("Arial", 9), anchor="w"
        )
        self.page_description.pack(fill="x", padx=14, pady=(0, 10))

        self.form = tk.Frame(self.page_top, bg="#fafbfc")
        self.form.pack(fill="x", padx=14, pady=(0, 12))

        separator = ttk.Separator(self.main_panel, orient="horizontal")
        separator.pack(fill="x")

        output_frame = tk.Frame(self.main_panel, bg=self.WHITE)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output = tk.Text(
            output_frame, wrap="none", font=("Consolas", 10),
            bg="white", fg="#222222", relief="solid", bd=1,
            padx=7, pady=7
        )
        output_y = ttk.Scrollbar(output_frame, orient="vertical",
                                 command=self.output.yview)
        output_x = ttk.Scrollbar(output_frame, orient="horizontal",
                                 command=self.output.xview)
        self.output.configure(yscrollcommand=output_y.set,
                              xscrollcommand=output_x.set)
        output_y.pack(side="right", fill="y")
        output_x.pack(side="bottom", fill="x")
        self.output.pack(side="left", fill="both", expand=True)

        # Log command di bagian bawah.
        log_label = tk.Label(
            self.main_panel, text="COMMAND", bg=self.WHITE, fg=self.MUTED,
            font=("Arial", 9, "bold"), anchor="w"
        )
        log_label.pack(fill="x", padx=10)

        log_frame = tk.Frame(self.main_panel, bg=self.WHITE)
        log_frame.pack(fill="x", padx=10, pady=(0, 8))
        self.command_log = tk.Text(
            log_frame, height=4, wrap="none", font=("Consolas", 9),
            bg="white", fg="#33404c", relief="solid", bd=1,
            padx=5, pady=4
        )
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical",
                                   command=self.command_log.yview)
        self.command_log.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side="right", fill="y")
        self.command_log.pack(side="left", fill="x", expand=True)
        self.log_command("startup", "UI siap")

    def _add_menu_group(self, heading, items):
        tk.Label(
            self.menu_frame, text=heading, bg=self.BG, fg="#687584",
            font=("Arial", 9, "bold"), anchor="w"
        ).pack(fill="x", padx=5, pady=(8, 3))

        for label, callback in items:
            command = callback if callback is not None else (
                lambda page=label: self.show_page(page)
            )
            button = ttk.Button(
                self.menu_frame, text=label, style="Sidebar.TButton",
                command=command
            )
            button.pack(fill="x", padx=4, pady=1)
            self.menu_buttons[label] = button

    def log_command(self, name, message):
        timestamp = time.strftime("%H:%M:%S")
        self.command_log.insert("end", f"{name:<24} -> {message}  [{timestamp}]\n")
        self.command_log.see("end")

    def _clear_form(self):
        for widget in self.form.winfo_children():
            widget.destroy()

    def show_page(self, page):
        self.current_page = page
        for label, button in self.menu_buttons.items():
            button.configure(
                style="Selected.TButton" if label == page else "Sidebar.TButton"
            )

        self._clear_form()
        descriptions = {
            "ARRAY - LIHAT PESANAN": (
                "Array: tampilkan semua pesanan yang tersimpan."
            ),
            "ARRAY - TAMBAH PESANAN REGULER": (
                "append: pesanan biasa mengantre di barisan paling belakang."
            ),
            "ARRAY - TAMBAH PESANAN PRIORITAS": (
                "insert tengah: pesanan prioritas dimasukkan ke bagian tengah."
            ),
            "ARRAY - TAMBAH PESANAN VIP": (
                "insert depan: pesanan VIP berada di posisi paling depan."
            ),
            "ARRAY - HAPUS PESANAN": (
                "Hapus pesanan dari Array berdasarkan nomor pesanan (OID)."
            ),
            "LINKEDLIST - LIHAT PESANAN": (
                "Linked List: tampilkan semua pesanan yang tersimpan."
            ),
            "LINKEDLIST - TAMBAH PESANAN REGULER": (
                "append: tambahkan pesanan reguler di bagian belakang Linked List."
            ),
            "LINKEDLIST - TAMBAH PESANAN PRIORITAS": (
                "Tambahkan pesanan prioritas ke bagian tengah Linked List."
            ),
            "LINKEDLIST - TAMBAH PESANAN VIP": (
                "Tambahkan pesanan VIP ke posisi pertama Linked List."
            ),
            "LINKEDLIST - HAPUS PESANAN": (
                "Hapus pesanan dari Linked List berdasarkan nomor pesanan (OID)."
            ),
        }

        self.page_title.configure(text=page)
        self.page_description.configure(
            text=descriptions.get(page, "Pilih aksi untuk menjalankan fitur ini.")
        )

        if page.endswith("LIHAT PESANAN"):
            ttk.Button(
                self.form, text="TAMPILKAN", style="Action.TButton",
                command=self._view_current
            ).pack(side="left")
            self._write_output("Klik TAMPILKAN untuk melihat daftar pesanan.")
        elif "TAMBAH PESANAN" in page:
            tk.Label(
                self.form, text="Nama pelanggan", bg="#fafbfc", fg=self.TEXT,
                font=("Arial", 9, "bold")
            ).grid(row=0, column=0, sticky="w", padx=(0, 60))
            self.name_entry = ttk.Entry(self.form, width=24)
            self.name_entry.insert(0, "Pelanggan Baru")
            self.name_entry.grid(row=1, column=0, sticky="w", padx=(0, 60))
            tk.Label(
                self.form, text="nama untuk pesanan yang akan dibuat",
                bg="#fafbfc", fg="#7b8794", font=("Arial", 8)
            ).grid(row=2, column=0, sticky="w", pady=(3, 0))
            ttk.Button(
                self.form, text="TAMBAH", style="Action.TButton",
                command=self._add_order
            ).grid(row=1, column=1, sticky="w")
            self._write_output("")
        elif "HAPUS PESANAN" in page:
            tk.Label(
                self.form, text="Nomor pesanan (OID)", bg="#fafbfc",
                fg=self.TEXT, font=("Arial", 9, "bold")
            ).pack(side="left", padx=(0, 10))
            self.oid_entry = ttk.Entry(self.form, width=22)
            self.oid_entry.pack(side="left", padx=(0, 10))
            ttk.Button(
                self.form, text="HAPUS", style="Action.TButton",
                command=self._delete_order
            ).pack(side="left")
            self._write_output("Masukkan OID pesanan yang ingin dihapus.")
        else:
            ttk.Button(
                self.form, text="JALANKAN", style="Action.TButton",
                command=lambda: self._placeholder_action(page)
            ).pack(side="left")
            self._write_output(
                "Fitur ini disiapkan sebagai tempat integrasi backend berikutnya."
            )

    def _write_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        if text:
            self.output.insert("1.0", text)
        self.output.configure(state="normal")

    def _current_structure(self):
        if self.current_page.startswith("LINKEDLIST"):
            return self.linked_orders, "Linked List"
        return self.array_orders, "Array"

    def _add_order(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input belum lengkap", "Nama pelanggan harus diisi.")
            return

        orders, structure_name = self._current_structure()
        if "REGULER" in self.current_page:
            priority = "REGULER"
            orders.append({"oid": f"O-{self.order_counter:06d}",
                           "nama": name, "prioritas": priority})
        elif "PRIORITAS" in self.current_page:
            priority = "PRIORITAS"
            order = {"oid": f"O-{self.order_counter:06d}",
                     "nama": name, "prioritas": priority}
            orders.insert(len(orders) // 2, order)
        else:
            priority = "VIP"
            order = {"oid": f"O-{self.order_counter:06d}",
                     "nama": name, "prioritas": priority}
            orders.insert(0, order)

        oid = f"O-{self.order_counter:06d}"
        self.order_counter += 1
        self._write_output(
            f"Pesanan berhasil ditambahkan!\n\n"
            f"OID       : {oid}\n"
            f"Pelanggan : {name}\n"
            f"Prioritas : {priority}\n"
            f"Struktur  : {structure_name}\n"
            f"Jumlah    : {len(orders)} pesanan"
        )
        self.log_command("add_order", f"{structure_name} | {oid} | {priority}")
        self.name_entry.delete(0, "end")

    def _view_current(self):
        orders, structure_name = self._current_structure()
        lines = [f"DAFTAR PESANAN - {structure_name}",
                 f"Jumlah pesanan: {len(orders)}", "-" * 65]
        if not orders:
            lines.append("Belum ada pesanan. Tambahkan pesanan terlebih dahulu.")
        else:
            for index, order in enumerate(orders, start=1):
                lines.append(
                    f"{index:>4}. {order['oid']} | {order['nama']} | "
                    f"{order['prioritas']}"
                )
        self._write_output("\n".join(lines))
        self.log_command("view_orders", f"{structure_name} | {len(orders)} data")

    def view_array(self):
        self.show_page("ARRAY - LIHAT PESANAN")

    def view_linked(self):
        self.show_page("LINKEDLIST - LIHAT PESANAN")

    def _delete_order(self):
        oid = self.oid_entry.get().strip()
        orders, structure_name = self._current_structure()
        index_found = -1
        for index, order in enumerate(orders):
            if order["oid"] == oid:
                index_found = index
                break

        if index_found == -1:
            messagebox.showinfo("Pesanan tidak ditemukan",
                                f"OID {oid!r} tidak ditemukan di {structure_name}.")
            self.log_command("delete_order", f"{oid} tidak ditemukan")
            return

        del orders[index_found]
        self._write_output(
            f"Pesanan {oid} berhasil dihapus dari {structure_name}.\n"
            f"Sisa pesanan: {len(orders)}"
        )
        self.log_command("delete_order", f"{structure_name} | {oid}")

    def load_csv(self):
        path = filedialog.askopenfilename(
            title="Pilih file CSV pesanan",
            filetypes=[("CSV files", "*.csv"), ("Semua file", "*.*")]
        )
        if not path:
            return

        loaded = []
        try:
            with open(path, "r", encoding="utf-8-sig", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Mendukung beberapa variasi nama kolom CSV.
                    oid = row.get("oid") or row.get("OID") or row.get("id") or ""
                    name = (row.get("pelanggan") or row.get("nama_pelanggan")
                            or row.get("nama") or "Pelanggan")
                    priority = (row.get("prioritas") or row.get("jenis_prioritas")
                                or "REGULER").upper()
                    loaded.append({
                        "oid": oid if oid else f"O-{self.order_counter:06d}",
                        "nama": name,
                        "prioritas": priority
                    })
                    if not oid:
                        self.order_counter += 1
        except (OSError, csv.Error) as error:
            messagebox.showerror("Gagal memuat CSV", str(error))
            self.log_command("load_csv", f"GAGAL: {error}")
            return

        self.array_orders = loaded[:]
        self.linked_orders = loaded[:]
        self._write_output(
            f"File berhasil dimuat:\n{path}\n\n"
            f"Jumlah data CSV : {len(loaded)}\n"
            f"Array           : {len(self.array_orders)} data\n"
            f"Linked List     : {len(self.linked_orders)} data\n\n"
            "Catatan: ini adalah contoh pemuatan data untuk UI. "
            "Sesuaikan pemetaan kolom dengan backend/proyek Anda."
        )
        self.log_command("load_csv", f"{len(loaded)} data dimuat")

    def _placeholder_action(self, page):
        self._write_output(
            f"Menu: {page}\n\n"
            "Tampilan UI sudah tersedia, tetapi fungsi ini belum dihubungkan "
            "ke modul backend terkait."
        )
        self.log_command("open_feature", page)


def main():
    root = tk.Tk()
    app = FoodDeliveryUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()'''