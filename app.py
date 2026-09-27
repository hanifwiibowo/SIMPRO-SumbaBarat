"""
SIMPRO — Dashboard Pengajuan Pendampingan Probity (versi Streamlit)
Inspektorat Kabupaten Sumba Barat

Dashboard non-web-HTML untuk OPD mengajukan permohonan pendampingan Probity
langsung, tanpa perlu login ke aplikasi utama SIMPRO. Data yang ditampilkan
masih dummy/contoh (belum tersambung ke database sungguhan SIMPRO).
"""

import streamlit as st
from datetime import datetime

# ---------------------------------------------------------------------------
# KONFIGURASI HALAMAN
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SIMPRO — Pengajuan Pendampingan Probity",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# TEMA / STYLING
# Catatan: tema warna (terang, tidak ikut dark mode perangkat) dikunci lewat
# .streamlit/config.toml, supaya tampilannya konsisten untuk semua orang yang
# membuka link ini. CSS di bawah hanya untuk elemen dekoratif kecil yang
# SELALU dibuka & ditutup dalam satu pemanggilan st.markdown yang sama —
# tidak ada <div> yang dibuka di satu tempat lalu ditutup jauh di baris lain,
# karena Streamlit merender tiap elemen sebagai blok terpisah dan trik itu
# menghasilkan HTML yang rusak.
# ---------------------------------------------------------------------------
PRIMARY = "#4F46E5"
PRIMARY_2 = "#7C3AED"
BORDER = "rgba(67,56,202,0.15)"

st.markdown(
    """
    <style>
    .block-container { padding-top: 1rem; max-width: 980px; }
    .simpro-topstripe {
        height: 6px; width: 100%; background: #DC2626;
        margin: -1rem 0 1.2rem 0;
    }
    .simpro-cta {
        background: linear-gradient(135deg, #4F46E5, #7C3AED);
        color: #fff; padding: 20px 24px; border-radius: 14px;
        margin-bottom: 22px;
    }
    .simpro-cta h3 { margin: 0 0 4px 0; color: #fff; }
    .simpro-cta p { margin: 0; color: rgba(255,255,255,.92); font-size: 0.92rem; }

    .status-badge {
        display: inline-block; padding: 4px 12px; border-radius: 999px;
        font-size: 0.78rem; font-weight: 700; white-space: nowrap;
    }
    .badge-baru { background:#EEF2FF; color:#4338CA; }
    .badge-verifikasi { background:#FEF3C7; color:#B45309; }
    .badge-disetujui { background:#DCFCE7; color:#15803D; }
    .badge-revisi { background:#FEE2E2; color:#B91C1C; }
    .badge-selesai { background:#E0E7FF; color:#3730A3; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# DATA DUMMY
# ---------------------------------------------------------------------------
DAFTAR_OPD = [
    "Dinas Pekerjaan Umum",
    "Dinas Pendidikan",
    "Dinas Kesehatan",
    "Badan Perencanaan Pembangunan Daerah",
    "Sekretariat Daerah (Pemda)",
]

DOKUMEN_WAJIB = [
    ("dpa", "DPA (Dokumen Pelaksanaan Anggaran)"),
    ("rup", "RUP (Rencana Umum Pengadaan)"),
    ("kak", "KAK (Kerangka Acuan Kerja)"),
    ("hps", "HPS (Harga Perkiraan Sendiri)"),
    ("spek", "Spesifikasi Teknis"),
    ("jadwal", "Jadwal Pelaksanaan"),
    ("pasar", "Analisis Pasar"),
]

TAHAPAN_OPSI = [
    "Perencanaan",
    "Persiapan Pengadaan",
    "Pemilihan Penyedia",
    "Pelaksanaan Kontrak",
]

STATUS_BADGE_CLASS = {
    "Baru": "badge-baru",
    "Diverifikasi": "badge-verifikasi",
    "Disetujui": "badge-disetujui",
    "Dikembalikan untuk Revisi": "badge-revisi",
    "Selesai": "badge-selesai",
}

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "submissions" not in st.session_state:
    # beberapa contoh data dummy supaya dashboard tidak kosong saat pertama dibuka
    st.session_state.submissions = [
        {
            "opd": "Dinas Pekerjaan Umum",
            "paket": "Pembangunan Jalan Ruas A–B",
            "nilai": 2_500_000_000,
            "tahapan": "Pemilihan Penyedia",
            "status": "Diverifikasi",
            "tanggal": "25 Sep 2026",
        },
        {
            "opd": "Dinas Kesehatan",
            "paket": "Pengadaan Alat Kesehatan Puskesmas",
            "nilai": 1_200_000_000,
            "tahapan": "Persiapan Pengadaan",
            "status": "Disetujui",
            "tanggal": "23 Sep 2026",
        },
    ]

if "extra_docs_count" not in st.session_state:
    st.session_state.extra_docs_count = 0


def format_rupiah(n):
    return f"{n:,.0f}".replace(",", ".")


def reset_form():
    for key in list(st.session_state.keys()):
        if key.startswith("doc_") or key in ("paket_nama", "paket_nilai", "paket_tahapan", "surat_resmi"):
            del st.session_state[key]
    st.session_state.extra_docs_count = 0


def render_status_row(s, show_opd=False):
    badge_class = STATUS_BADGE_CLASS.get(s["status"], "badge-baru")
    subtitle = f"{s['opd']} · " if show_opd else ""
    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;
                    padding:10px 0;border-bottom:1px solid {BORDER};">
            <div>
                <b>{s['paket']}</b><br>
                <span style="color:#6B7280;font-size:0.85rem;">
                    {subtitle}Rp {format_rupiah(s['nilai'])} · {s['tahapan']} · {s['tanggal']}
                </span>
            </div>
            <span class="status-badge {badge_class}">{s['status']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# SIDEBAR — pilih "login sebagai" (dummy, tanpa autentikasi sungguhan)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ SIMPRO")
    st.caption("Inspektorat Kab. Sumba Barat")
    st.divider()
    opd_aktif = st.selectbox("Masuk sebagai OPD", DAFTAR_OPD)
    st.divider()
    menu = st.radio("Menu", ["📝 Ajukan Pendampingan", "📊 Rekap Permohonan"])
    st.divider()
    st.caption("Dashboard ini memakai data contoh (dummy) — belum tersambung ke database SIMPRO yang sesungguhnya.")

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown('<div class="simpro-topstripe"></div>', unsafe_allow_html=True)
st.title("Sistem Informasi Pendampingan Probity")
st.caption(f"Dashboard pengajuan pendampingan APIP — {opd_aktif}")
st.write("")

# ---------------------------------------------------------------------------
# HALAMAN: AJUKAN PENDAMPINGAN
# ---------------------------------------------------------------------------
if menu == "📝 Ajukan Pendampingan":

    st.markdown(
        """
        <div class="simpro-cta">
            <h3>Siap mengajukan pendampingan Probity?</h3>
            <p>Lengkapi checklist dokumen tahap Perencanaan di bawah, lalu isi formulir permohonan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Langkah 1: checklist dokumen wajib ----
    with st.container(border=True):
        st.markdown("**LANGKAH 1**")
        st.subheader("Lengkapi & unggah dokumen tahap Perencanaan")
        st.caption("Setiap dokumen diunggah sebagai bukti kelengkapan. Format PDF, maksimal 50MB per dokumen.")

        uploaded = {}
        for key, label in DOKUMEN_WAJIB:
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(label)
            with col2:
                f = st.file_uploader(label, type=["pdf"], key=f"doc_{key}", label_visibility="collapsed")
                uploaded[key] = f

        jumlah_lengkap = sum(1 for k in uploaded if uploaded[k] is not None)
        st.progress(jumlah_lengkap / len(DOKUMEN_WAJIB))
        semua_lengkap = jumlah_lengkap == len(DOKUMEN_WAJIB)

        if semua_lengkap:
            st.success(f"✔ {jumlah_lengkap}/{len(DOKUMEN_WAJIB)} dokumen wajib terunggah — formulir pengajuan terbuka.")
        else:
            st.info(f"Unggah {len(DOKUMEN_WAJIB) - jumlah_lengkap} dokumen lagi untuk membuka formulir pengajuan ({jumlah_lengkap}/{len(DOKUMEN_WAJIB)}).")

    # ---- Dokumen pendukung lainnya (opsional) ----
    with st.container(border=True):
        st.subheader("Dokumen Pendukung Lainnya")
        st.caption("Opsional — tambahkan dokumen lain di luar 7 dokumen wajib di atas, kalau ada.")

        for i in range(st.session_state.extra_docs_count):
            c1, c2 = st.columns([3, 2])
            with c1:
                st.text_input("Nama dokumen", key=f"extra_name_{i}", placeholder="Contoh: Surat Dukungan Teknis")
            with c2:
                st.file_uploader("Berkas", type=["pdf"], key=f"extra_file_{i}", label_visibility="collapsed")

        if st.button("+ Tambah Dokumen Lain"):
            st.session_state.extra_docs_count += 1
            st.rerun()

    # ---- Langkah 2: formulir permohonan ----
    with st.container(border=True):
        st.markdown("**LANGKAH 2**")
        st.subheader("Formulir permohonan")

        with st.form("form_permohonan", clear_on_submit=False):
            nama_paket = st.text_input("Nama Paket", key="paket_nama")
            nilai_paket = st.number_input("Nilai Paket (Rp)", min_value=0, step=1_000_000, key="paket_nilai")
            tahapan = st.selectbox("Tahapan Pengadaan", TAHAPAN_OPSI, key="paket_tahapan")
            surat = st.file_uploader("Surat Permohonan Resmi (PDF, maks. 50MB)", type=["pdf"], key="surat_resmi")

            submit = st.form_submit_button(
                "Kirim Permohonan",
                disabled=not semua_lengkap,
                use_container_width=True,
            )

            if submit:
                if not nama_paket:
                    st.error("Nama Paket wajib diisi.")
                elif surat is None:
                    st.error("Surat Permohonan Resmi wajib diunggah.")
                else:
                    st.session_state.submissions.insert(0, {
                        "opd": opd_aktif,
                        "paket": nama_paket,
                        "nilai": nilai_paket,
                        "tahapan": tahapan,
                        "status": "Baru",
                        "tanggal": datetime.now().strftime("%d %b %Y"),
                    })
                    st.success(f"Permohonan '{nama_paket}' berhasil diajukan (status: Baru). Admin Inspektorat akan memverifikasi.")
                    reset_form()

        if not semua_lengkap:
            st.caption("Tombol 'Kirim Permohonan' aktif setelah 7 dokumen wajib di atas lengkap.")

    # ---- Status pengajuan milik OPD aktif ----
    punya = [s for s in st.session_state.submissions if s["opd"] == opd_aktif]
    if punya:
        with st.container(border=True):
            st.subheader("Status Pengajuan Saya")
            for s in punya:
                render_status_row(s, show_opd=False)

# ---------------------------------------------------------------------------
# HALAMAN: REKAP PERMOHONAN (ringkas, untuk dilihat K Sida / Admin)
# ---------------------------------------------------------------------------
else:
    with st.container(border=True):
        st.subheader("Rekap Seluruh Permohonan")
        st.caption("Ringkasan status seluruh permohonan pendampingan Probity (data contoh).")

        total = len(st.session_state.submissions)
        baru = sum(1 for s in st.session_state.submissions if s["status"] == "Baru")
        verifikasi = sum(1 for s in st.session_state.submissions if s["status"] == "Diverifikasi")
        disetujui = sum(1 for s in st.session_state.submissions if s["status"] in ("Disetujui", "Selesai"))

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Permohonan", total)
        c2.metric("Baru", baru)
        c3.metric("Sedang Diverifikasi", verifikasi)
        c4.metric("Disetujui / Selesai", disetujui)

    with st.container(border=True):
        st.subheader("Daftar Permohonan")
        if st.session_state.submissions:
            for s in st.session_state.submissions:
                render_status_row(s, show_opd=True)
        else:
            st.write("Belum ada permohonan.")
