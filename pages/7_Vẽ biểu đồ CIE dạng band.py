import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import colour

st.set_page_config(layout="wide")
st.write('## Biểu đồ CIE dạng band (400 - 700 nm)')

cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']

wl_min, wl_max = st.sidebar.slider('Khoảng bước sóng (nm)', 400, 700, (400, 700), step=10)
buoc = st.sidebar.selectbox('Bước nhảy bước sóng (nm)', [1, 2, 5, 10], index=0)
hien_cmfs = st.sidebar.checkbox('Hiển thị thêm đường cong x̄(λ), ȳ(λ), z̄(λ)', value=True)


def wavelength_to_srgb(wl):
    """Màu đơn sắc của bước sóng wl (nm) hiển thị trên màn hình sRGB."""
    XYZ = colour.wavelength_to_XYZ(wl, cmfs)
    # RGB tuyến tính, chưa mã hoá gamma
    rgb = colour.XYZ_to_sRGB(XYZ, apply_cctf_encoding=False)
    # Màu đơn sắc nằm ngoài gamut sRGB -> có giá trị âm, cắt về 0
    rgb = np.clip(rgb, 0, None)
    m = rgb.max()
    if m > 0:
        rgb = rgb / m          # chuẩn hoá độ sáng để dải màu rõ ràng
    return np.clip(colour.cctf_encoding(rgb), 0, 1)   # mã hoá gamma sRGB


wavelengths = np.arange(wl_min, wl_max + 1, buoc)
colors = np.array([wavelength_to_srgb(w) for w in wavelengths])   # (N, 3)

CAO = 60
band = np.tile(colors[np.newaxis, :, :], (CAO, 1, 1))              # (CAO, N, 3)

fig, ax = plt.subplots(figsize=(10, 2.2))
ax.imshow(band, extent=[wavelengths[0], wavelengths[-1], 0, 1], aspect='auto')
ax.set_yticks([])
ax.set_xticks(np.arange(wl_min, wl_max + 1, 50 if wl_max - wl_min >= 200 else 10))
ax.set_xlabel('Bước sóng (nm)')
ax.set_title('CIE band: màu đơn sắc từ %d nm đến %d nm' % (wl_min, wl_max))
st.pyplot(fig, clear_figure=True)

if hien_cmfs:
    wl_ve = np.arange(wl_min, wl_max + 1, 1)
    xyz_bar = np.array([cmfs[w] for w in wl_ve])
    fig2, ax2 = plt.subplots(figsize=(10, 3.5))
    ax2.plot(wl_ve, xyz_bar[:, 0], 'r', label='x̄(λ)')
    ax2.plot(wl_ve, xyz_bar[:, 1], 'g', label='ȳ(λ)')
    ax2.plot(wl_ve, xyz_bar[:, 2], 'b', label='z̄(λ)')
    ax2.set_xlim(wl_min, wl_max)
    ax2.set_xlabel('Bước sóng (nm)')
    ax2.set_ylabel('Giá trị CMFs')
    ax2.set_title('Hàm màu CIE 1931 2° Standard Observer')
    ax2.legend()
    ax2.grid(alpha=0.3)
    st.pyplot(fig2, clear_figure=True)

st.caption(
    "Lưu ý: màu đơn sắc nằm ngoài gamut sRGB nên màu hiển thị chỉ là gần đúng "
    "(giá trị âm được cắt về 0 và chuẩn hoá độ sáng)."
)
