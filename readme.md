# SECURE - Automated Cybersecurity Code Review Engine

SECURE adalah mesin audit keamanan kode sumber berkinerja tinggi berbasis Artificial Intelligence. Alat ini dirancang untuk mendeteksi kerentanan keamanan secara otomatis pada berkas yang mengalami perubahan (`git diff`) maupun file baru (`untracked files`) sebelum atau sesudah proses commit.

Engine ini mengintegrasikan standar keamanan global seperti OWASP Top 10, OWASP ASVS v5.0, OWASP CheatSheet Series, serta Aturan SOP Internal secara otomatis ke dalam konteks analisis Large Language Model (LLM).

Pengembang: fiqq.rahman

---

## Fitur Utama

- Auto Git Diff Targeting: Hanya memindai file aplikasi yang baru diubah atau file baru yang belum di-commit, tanpa membuang kuota token pada berkas bawaan framework/vendor.
- Smart Framework Filtering: Mengabaikan direktori bawaan secara otomatis seperti `vendor/`, `system/`, `node_modules/`, `public/`, `writable/`, dan `storage/`.
- Multi-Knowledge Base RAG Integration: Menggabungkan pengetahuan dari OWASP Top 10 PDF, OWASP ASVS JSON, OWASP CheatSheets Markdown, dan Custom Rules YAML.
- High-Availability Fallback Mechanism: Dilengkapi dengan Exponential Backoff Retry dan otomatis melakukan cascade fallback ke model alternatif jika terjadi lonjakan trafik API.
- Global Terminal CLI: Dapat dipanggil dari direktori mana saja di dalam terminal menggunakan perintah `audit`.
- Cybersec Terminal Formatter: Format keluaran terminal dengan tata letak bersih (80-character text wrap) serta penyorotan warna kondisional untuk tingkat kerentanan.

---

## Arsitektur Sistem

Mesin bekerja dengan alur kerja berikut:

1. Target Scanning: Membaca status direktori kerja Git di mana perintah dipanggil.
2. Filter & Parsing: Memfilter ekstensi berkas yang didukung (`.php`, `.py`, `.js`, `.ts`, `.go`, `.java`, `.c`, `.cpp`) dan mengabaikan pustaka pihak ketiga.
3. Patch Extraction: Mengambil perubahan baris kode (patch diff) atau konten penuh jika berkas baru dibuat.
4. Knowledge Aggregation: Memuat standar OWASP dan SOP internal ke dalam konteks instruksi sistem.
5. AI Analysis: Mengirimkan konteks dan patch kode ke model Gemini untuk dianalisis secara forensik.
6. Console Output Rendering: Menampilkan hasil laporan audit yang sudah dibungkus rapi ke layar terminal.

---

## Prasyarat System

- Python 3.10 atau versi lebih baru
- Git CLI
- Google Gemini API Key

---

## Struktur Proyek

```text
audit-code/
├── config/
│   └── settings.py          # Konfigurasi path knowledge base dan LLM
├── core/
│   ├── auditor.py           # Core engine komunikasi LLM & fallback logic
│   ├── git_handler.py       # Handler ekstraksi git diff & untracked files
│   └── rule_parser.py       # Parser aturan internal SOP
├── knowledge/
│   ├── asps_parser.py       # Parser OWASP ASVS JSON
│   ├── owasp_parser.py      # Parser OWASP CheatSheets
│   └── top10_parser.py      # Parser OWASP Top 10 PDF
├── utils/
│   └── formatter.py         # Formatter terminal & penyorot warna ANSI
├── audit.bat                # Wrapper CLI executable untuk Windows
├── main.py                  # Entry point aplikasi
├── requirements.txt         # Daftar dependensi Python
└── .env                     # Konfigurasi rahasia API Key

---

## Lisensi

Proyek ini dilindungi di bawah **Educational & AI Research License**. Hak Cipta (C) 2026 **fiqq.rahman**.

- **Izin Penggunaan**: Kode sumber ini terbuka secara khusus untuk dipelajari, dijadikan bahan edukasi, serta digunakan sebagai acuan pengembangan/riset teknologi kecerdasan buatan (Artificial Intelligence).
- **Larangan Komersialisasi**: Dilara