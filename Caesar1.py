import streamlit as st

def ceasar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            result += shifted_char
        else:
            result += char
    return result

st.title("Caesar Cipher - Mã hóa / Giải mã")
mode = st.radio("Chọn chế độ:", ("Mã hóa", "Giải mã"))
text = st.text_area("Văn bản:", value="", height=200)
shift = st.number_input("Số bước dịch (0-25):", min_value=0, max_value=25, value=3, step=1)

if st.button("Thực hiện"):
    actual_shift = shift if mode == "Mã hóa" else -shift
    result = ceasar_cipher(text, actual_shift)
    st.subheader("Kết quả")
    st.code(result)