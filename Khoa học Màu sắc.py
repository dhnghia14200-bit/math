import os
import streamlit as st

st.set_page_config(page_title="Khoa học Màu sắc", layout="wide")

# ---- Logo trường và khoa (đặt ảnh vào thư mục images/) ----
LOGO_TRUONG = "images/logo_truong.png"
LOGO_KHOA = "images/logo_khoa.png"

col_a, col_b, col_c = st.columns([1, 4, 1])
with col_a:
    if os.path.exists(LOGO_TRUONG):
        st.image(LOGO_TRUONG, width=120)
    else:
        st.caption("Chưa có images/logo_truong.png")
with col_c:
    if os.path.exists(LOGO_KHOA):
        st.image(LOGO_KHOA, width=120)
    else:
        st.caption("Chưa có images/logo_khoa.png")
with col_b:
    st.markdown(
        "<h3 style='text-align:center;'>TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP.HCM<br>"
        "KHOA CÔNG NGHỆ IN VÀ TRUYỀN THÔNG</h3>",
        unsafe_allow_html=True,
    )

st.write("### Chào mừng bạn đến với project Khoa học Màu sắc của mình!")
st.write("# Mình tên là Võ Tự Thanh, MaSV 22158139")

st.markdown(
    """
**Nội dung project (chọn ở thanh bên trái):**
1. Chuyển đổi không gian màu sRGB ↔ XYZ
2. Tính giá trị 3 thành phần X, Y, Z từ file phổ
3. Biểu đồ CIE hình móng ngựa
4. Gamut màu của thiết bị RGB
5. Gamut màu của máy in
6. Đặc tính hoá máy in nửa tông
7. **Biểu đồ CIE dạng band (400–700 nm)**
8. **Biểu đồ CIELab: chuyển dịch màu Lab1 → Lab2**
"""
)
