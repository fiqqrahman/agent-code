# SECURE - Automated Cybersecurity Code Review Engine

SECURE adalah mesin audit keamanan kode sumber berkinerja tinggi berbasis Artificial Intelligence. Alat ini dirancang untuk mendeteksi kerentanan keamanan secara otomatis pada berkas yang mengalami perubahan (`git diff`) maupun file baru (`untracked files`) sebelum atau sesudah proses commit.

Engine ini mengintegrasikan standar keamanan global seperti OWASP Top 10, OWASP ASVS v5.0, OWASP CheatSheet Series, serta Aturan SOP Internal secara otomatis ke dalam konteks analisis Large Language Model (LLM).

Pengembang: fiqq.rahman

---

## Lisensi

Proyek ini dilindungi di bawah **Educational & AI Research License**. Hak Cipta (C) 2026 **fiqq.rahman**. Hak Cipta Dilindungi Undang-Undang (*All Rights Reserved*).

### Rincian Ketentuan Lisensi:
1. **Khusus Edukasi & Riset AI**: Kode sumber ini disediakan secara bebas hanya untuk diinspeksi, dipelajari, dijadikan materi pembelajaran, serta digunakan sebagai acuan pengembangan/riset teknologi kecerdasan buatan (*Artificial Intelligence*).
2. **Larangan Komersialisasi (Non-Commercial Only)**: Dilarang keras menjual, memperjualbelikan, menyewakan, memonetisasi, atau memanfaatkan mesin ini (maupun seluruh produk turunannya) untuk tujuan bisnis, profit, atau lingkungan enterprise/produksi tanpa izin tertulis resmi dari pemegang hak cipta (**fiqq.rahman**).
3. **Atribusi Kode (Attribution)**: Setiap karya turunan, adaptasi, riset, atau karya ilmiah yang dibuat berdasarkan proyek ini **wajib** mencantumkan kredit dan atribusi secara jelas kepada pengembang asli (**fiqq.rahman**).
4. **Bebas Tanggung Jawab (No Warranty)**: Perangkat lunak ini disediakan *"AS IS"* (apa adanya) tanpa jaminan apa pun. Pengembang (**fiqq.rahman**) tidak bertanggung jawab atas timbulnya klaim, kerusakan, atau kerugian lain yang diakibatkan oleh penggunaan mesin ini.

## Fitur Utama

- Auto Git Diff Targeting: Hanya memindai file aplikasi yang baru diubah atau file baru yang belum di-commit, tanpa membuang kuota token pada berkas bawaan framework/vendor.
- Smart Framework Filtering: Mengabaikan direktori bawaan secara otomatis seperti `vendor/`, `system/`, `node_modules/`, `public/`, `writable/`, dan `storage/`.
- Multi-Knowledge Base RAG Integration: Menggabungkan pengetahuan dari OWASP Top 10 PDF, OWASP ASVS JSON, OWASP CheatSheets Markdown, dan Custom Rules YAML.
- High-Availability Fallback Mechanism: Dilengkapi dengan Exponential Backoff Retry dan otomatis melakukan cascade fallback ke model alternatif jika terjadi lonjakan trafik API.
- Global Terminal CLI: Dapat dipanggil dari direktori mana saja di dalam terminal menggunakan perintah `audit`.
- Cybersec Terminal Formatter: Format keluaran terminal dengan tata letak bersih (80-character text wrap) serta penyorotan warna kondisional untuk tingkat kerentanan.

---

## Cakupan & Batasan Audit (Scope & Boundaries)

Mesin audit ini difokuskan secara khusus untuk menganalisis ekosistem web backend dan frontend.

### 1. Bahasa Pemrograman & Ekstensi Terdukung
- **PHP** (`.php`) — Fokus utama: Laravel, CodeIgniter 4, & Native PHP.
- **JavaScript / TypeScript** (`.js`, `.ts`) — Web Client-side, Node.js, & AJAX/REST API.
- **Bahasa Lain** (`.py`, `.go`, `.java`, `.c`, `.cpp`).

### 2. Standar OWASP CheatSheet Series yang Diparsing
Mesin secara spesifik memuat modul referensi keamanan berikut ke dalam basis pengetahuan RAG:
- **Autentikasi & Akses**: Access Control, Authentication, Authorization, Session Management, IDOR Prevention, Password Storage, Forgot Password, Mass Assignment.
- **Injeksi & Validasi Input**: SQL Injection Prevention, Query Parameterization, OS Command Injection, LDAP Injection, XML External Entity (XXE), Input Validation, File Upload.
- **Keamanan Web Client & Browser**: Cross-Site Scripting (XSS), DOM-based XSS, XSS Filter Evasion, CSRF Prevention, Content Security Policy (CSP), DOM Clobbering, Clickjacking, HTML5 Security, Securing CSS, Third-Party JS Management, Prototype Pollution, XS-Leaks.
- **API & Protocol Security**: REST Security, GraphQL, JSON Web Token (JWT), HTTP Headers, HSTS, SSRF Prevention, Unvalidated Redirects/Forwards, AJAX Security.
- **Framework & Config Khusus**: Laravel Cheat Sheet, PHP Configuration Cheat Sheet.
- **Operasional & Ketahanan**: Denial of Service (DoS), Logging.

### 3. Standar Tambahan
- **OWASP Top 10**: Pemetaan kerentanan kritis tingkat global (A01 Broke Access Control hingga A10 SSRF).
- **OWASP ASVS v5.0.0**: Verifikasi standar tingkat lanjut untuk arsitektur keamanan aplikasi web.

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
├── LICENSE                  # Lisensi penggunaan proyek
└── .env                     # Konfigurasi rahasia API Key