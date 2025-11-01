import streamlit as st
import base64

# --- Logic XOR Cipher (Đối xứng) ---

def thuc_hien_xor(du_lieu_bytes: bytes, khoa: str) -> bytearray:
    """
    Thực hiện phép mã hóa/giải mã XOR bitwise.
    Đầu vào là bytes (từ Text hoặc Base64 decode), đầu ra là bytearray.
    """
    khoa_bytes = khoa.encode('utf-8')
    len_khoa = len(khoa_bytes)
    ket_qua_bytes = bytearray()
    
    if len_khoa == 0:
        return bytearray(du_lieu_bytes) # Nếu không có khóa, trả về bản gốc

    for i in range(len(du_lieu_bytes)):
        # Lấy byte của dữ liệu đầu vào
        p_byte = du_lieu_bytes[i]
        
        # Lấy byte của khóa (lặp lại)
        k_byte = khoa_bytes[i % len_khoa]
        
        # Phép toán XOR (C = P ^ K hoặc P = C ^ K)
        c_byte = p_byte ^ k_byte
        ket_qua_bytes.append(c_byte)
            
    return ket_qua_bytes


# --- Giao diện Streamlit ---

st.title("XOR Cipher — Mã hóa / Giải mã")
st.markdown("Văn bản mã hóa sẽ được hiển thị dưới dạng **Base64** để đảm bảo an toàn và khả năng in.")

# Sử dụng tên biến tiếng Việt cho giao diện
che_do = st.radio("Chọn chế độ:", ("Mã hóa (Text -> Base64)", "Giải mã (Base64 -> Text)"))
thong_diep_dau_vao = st.text_area("Văn bản/Base64 đầu vào:", value="", height=150)
khoa_dau_vao = st.text_input("Khóa (Không để trống):", value="")


if st.button("Thực hiện"):
    k = khoa_dau_vao.strip()

    if not k:
        st.error("Khóa không được để trống.")
    else:
        try:
            if che_do == "Mã hóa (Text -> Base64)":
                # Mã hóa: Text -> Bytes -> XOR Bytes -> Base64 String
                
                # 1. Chuyển Text đầu vào sang Bytes (UTF-8)
                du_lieu_bytes = thong_diep_dau_vao.encode('utf-8')
                
                # 2. Áp dụng XOR
                ket_qua_xor_bytes = thuc_hien_xor(du_lieu_bytes, k)
                
                # 3. Mã hóa kết quả XOR sang Base64 để hiển thị
                ket_qua_base64 = base64.b64encode(ket_qua_xor_bytes).decode('utf-8')
                
                st.success("Đã **Mã hóa** thành công!")
                st.subheader("Kết quả Base64")
                st.code(ket_qua_base64)
                st.info("Chuỗi Base64 này an toàn để sao chép và chia sẻ.")
            
            else: # Giải mã (Base64 -> Text)
                # Giải mã: Base64 String -> Bytes -> XOR Bytes -> Text
                
                # 1. Giải mã Base64 sang Bytes
                try:
                    van_ban_xor_bytes = base64.b64decode(thong_diep_dau_vao)
                except base64.binascii.Error:
                    st.error("Văn bản đầu vào không phải là chuỗi Base64 hợp lệ.")
                    st.stop()
                
                # 2. Áp dụng XOR (sử dụng cùng hàm XOR vì XOR là đối xứng)
                ket_qua_giai_ma_bytes = thuc_hien_xor(van_ban_xor_bytes, k)

                # 3. Giải mã Bytes sang Text (UTF-8)
                ket_qua_text = ket_qua_giai_ma_bytes.decode('utf-8', errors='replace')
                
                st.success("Đã **Giải mã** thành công!")
                st.subheader("Kết quả Văn bản Gốc")
                st.code(ket_qua_text)
                st.warning("Nếu thấy ký tự thay thế (), nghĩa là khóa có thể không chính xác hoặc văn bản gốc không phải là UTF-8.")

        except Exception as e:
            st.error(f"Đã xảy ra lỗi không mong muốn: {e}")

