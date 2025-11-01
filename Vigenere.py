import streamlit as st

# Bảng chữ cái cho phép: a–z (26 ký tự) và dấu cách (1 ký tự)
bang_chu_cai = "abcdefghijklmnopqrstuvwxyz "

# Tạo bảng ánh xạ ký tự ↔ chỉ số
ky_tu_sang_chi_so = dict(zip(bang_chu_cai, range(len(bang_chu_cai))))
chi_so_sang_ky_tu = dict(zip(range(len(bang_chu_cai)), bang_chu_cai))


def kiem_tra_van_ban_hop_le(van_ban: str) -> bool:
    """Trả về True nếu tất cả ký tự trong văn bản nằm trong bảng chữ cái cho phép."""
    return all(ch in ky_tu_sang_chi_so for ch in van_ban)


def ma_hoa(thong_diep, khoa):
    """Mã hóa thông điệp (cả thông điệp và khóa phải là chữ thường và sử dụng bảng chữ cái cho phép)."""
    van_ban_ma_hoa = ""
    # Chia thông điệp thành các khối có độ dài bằng khóa
    thong_diep_tach_ra = [thong_diep[i:i + len(khoa)] for i in range(0, len(thong_diep), len(khoa))]

    for moi_khoi in thong_diep_tach_ra:
        i = 0
        for ky_tu in moi_khoi:
            # Vigenère: C = (P + K) mod N
            so = (ky_tu_sang_chi_so[ky_tu] + ky_tu_sang_chi_so[khoa[i]]) % len(bang_chu_cai)
            van_ban_ma_hoa += chi_so_sang_ky_tu[so]
            i += 1
    return van_ban_ma_hoa


def giai_ma(van_ban_ma_hoa, khoa):
    """Giải mã văn bản đã mã hóa (cả văn bản đã mã hóa và khóa phải là chữ thường và sử dụng bảng chữ cái cho phép)."""
    van_ban_goc = ""
    # Chia văn bản đã mã hóa thành các khối có độ dài bằng khóa
    van_ban_tach_ra = [van_ban_ma_hoa[i:i + len(khoa)] for i in range(0, len(van_ban_ma_hoa), len(khoa))]

    for moi_khoi in van_ban_tach_ra:
        i = 0
        for ky_tu in moi_khoi:
            # Vigenère: P = (C - K) mod N
            so = (ky_tu_sang_chi_so[ky_tu] - ky_tu_sang_chi_so[khoa[i]]) % len(bang_chu_cai)
            van_ban_goc += chi_so_sang_ky_tu[so]
            i += 1
    return van_ban_goc


# --- Giao diện Streamlit ---

st.title("Vigenère Cipher — Mã hóa / Giải mã")
st.markdown("Nhập **văn bản** và **khóa**. Bảng chữ cái cho phép: a–z và dấu cách.")

# Sử dụng tên biến tiếng Việt cho giao diện
che_do = st.radio("Chọn chế độ:", ("Mã hóa", "Giải mã"))
thong_diep_dau_vao = st.text_area("Văn bản (chỉ chứa a-z, chữ thường và dấu cách):", value="", height=150)
khoa_dau_vao = st.text_input("Khóa (chỉ chứa a-z, chữ thường, không để trống):", value="")

if st.button("Thực hiện"):
    # Chuẩn hóa đầu vào
    m = thong_diep_dau_vao.lower()
    k = khoa_dau_vao.lower().strip() # Dùng strip() để xử lý khóa có khoảng trắng thừa

    if not k:
        st.error("Khóa không được để trống.")
    elif not kiem_tra_van_ban_hop_le(k):
        st.error("Khóa chỉ được chứa chữ thường **a-z** và **dấu cách**.")
    elif not kiem_tra_van_ban_hop_le(m):
        st.error("Văn bản chỉ được chứa chữ thường **a-z** và **dấu cách**.")
    else:
        # Tên biến kết quả cũng được dịch sang tiếng Việt
        if che_do == "Mã hóa":
            ket_qua = ma_hoa(m, k)
            st.success("Đã **Mã hóa** thành công!")
        else:
            ket_qua = giai_ma(m, k)
            st.success("Đã **Giải mã** thành công!")

        st.subheader("Kết quả")
        st.code(ket_qua)

        st.info(f"Bảng chữ cái được sử dụng có {len(bang_chu_cai)} ký tự (bao gồm a-z và dấu cách).")
