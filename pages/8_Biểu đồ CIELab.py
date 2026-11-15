import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import colour

st.set_page_config(layout="wide")
st.write('## Biểu đồ CIELab: chuyển dịch màu từ Lab1 sang Lab2')


def lab_to_srgb(lab):
    """Lab -> (XYZ, xy, sRGB hiển thị, có nằm ngoài gamut sRGB không)."""
    XYZ = colour.Lab_to_XYZ(np.array(lab))
    xy = colour.XYZ_to_xy(XYZ)
    rgb = colour.XYZ_to_sRGB(XYZ)
    ngoai_gamut = bool(np.any(rgb < 0) or np.any(rgb > 1))
    return XYZ, xy, np.clip(rgb, 0, 1), ngoai_gamut


def chroma_hue(lab):
    C = np.hypot(lab[1], lab[2])
    h = np.degrees(np.arctan2(lab[2], lab[1])) % 360
    return C, h


def swatch(rgb, ten):
    r, g, b = [int(round(v * 255)) for v in rgb]
    st.markdown(
        f"<div style='background:rgb({r},{g},{b});height:70px;border:1px solid #888;"
        f"border-radius:6px;text-align:center;line-height:70px;color:#888'>{ten}</div>",
        unsafe_allow_html=True,
    )


# ---------------- Nhập liệu ----------------
c1, c2 = st.columns(2)
with c1:
    st.write("### Màu 1 (Lab1)")
    L1 = st.number_input('L1', 0.0, 100.0, 50.0, key='L1')
    a1 = st.number_input('a1', -128.0, 127.0, 40.0, key='a1')
    b1 = st.number_input('b1', -128.0, 127.0, 20.0, key='b1')
with c2:
    st.write("### Màu 2 (Lab2)")
    L2 = st.number_input('L2', 0.0, 100.0, 60.0, key='L2')
    a2 = st.number_input('a2', -128.0, 127.0, -30.0, key='a2')
    b2 = st.number_input('b2', -128.0, 127.0, 40.0, key='b2')

if st.button('Vẽ biểu đồ và nhận xét'):
    lab1 = np.array([L1, a1, b1])
    lab2 = np.array([L2, a2, b2])

    XYZ1, xy1, rgb1, out1 = lab_to_srgb(lab1)
    XYZ2, xy2, rgb2, out2 = lab_to_srgb(lab2)

    # ---------- Ô màu ----------
    s1, s2 = st.columns(2)
    with s1:
        swatch(rgb1, 'Lab1')
    with s2:
        swatch(rgb2, 'Lab2')
    if out1 or out2:
        st.caption("Màu nằm ngoài gamut sRGB, ô màu hiển thị chỉ là gần đúng.")

    # ---------- Hai biểu đồ ----------
    g1, g2 = st.columns(2)

    with g1:
        fig, ax = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
        ax.set_xlim([-0.1, 0.85])
        ax.set_ylim([-0.1, 0.90])
        ax.set_title('Biểu đồ CIE 1931 xy')
        ax.plot(xy1[0], xy1[1], 'o', color='k', markersize=9, label='Lab1')
        ax.plot(xy2[0], xy2[1], 's', color='w', markeredgecolor='k', markersize=9, label='Lab2')
        ax.annotate('', xy=(xy2[0], xy2[1]), xytext=(xy1[0], xy1[1]),
                    arrowprops=dict(arrowstyle='->', color='k', lw=2))
        ax.legend()
        st.pyplot(fig, clear_figure=True)

    with g2:
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.axhline(0, color='gray', lw=1)
        ax2.axvline(0, color='gray', lw=1)
        ax2.scatter(a1, b1, s=200, color=rgb1, edgecolors='k', zorder=3, label='Lab1')
        ax2.scatter(a2, b2, s=200, color=rgb2, edgecolors='k', marker='s', zorder=3, label='Lab2')
        ax2.annotate('', xy=(a2, b2), xytext=(a1, b1),
                     arrowprops=dict(arrowstyle='->', color='k', lw=2))
        ax2.set_xlim(-128, 128)
        ax2.set_ylim(-128, 128)
        ax2.set_xlabel('a*  (xanh lá  ←  →  đỏ)')
        ax2.set_ylabel('b*  (xanh dương  ←  →  vàng)')
        ax2.set_title('Mặt phẳng a*b* của CIELab')
        ax2.grid(alpha=0.3)
        ax2.legend()
        st.pyplot(fig2, clear_figure=True)

    # ---------- Tính toán ----------
    dL, da, db = lab2 - lab1
    C1, h1 = chroma_hue(lab1)
    C2, h2 = chroma_hue(lab2)
    dC = C2 - C1
    dE76 = colour.delta_E(lab1, lab2, method='CIE 1976')
    dE00 = colour.delta_E(lab1, lab2, method='CIE 2000')

    st.write("### Kết quả tính toán")
    st.table({
        'Đại lượng': ['L*', 'a*', 'b*', 'Chroma C*', 'Hue h (độ)', 'x', 'y'],
        'Lab1': [f'{L1:.2f}', f'{a1:.2f}', f'{b1:.2f}', f'{C1:.2f}', f'{h1:.1f}',
                 f'{xy1[0]:.4f}', f'{xy1[1]:.4f}'],
        'Lab2': [f'{L2:.2f}', f'{a2:.2f}', f'{b2:.2f}', f'{C2:.2f}', f'{h2:.1f}',
                 f'{xy2[0]:.4f}', f'{xy2[1]:.4f}'],
    })
    st.write(f"**ΔL\\* = {dL:.2f}, Δa\\* = {da:.2f}, Δb\\* = {db:.2f}, ΔC\\* = {dC:.2f}**")
    st.write(f"**ΔE\\*ab (CIE76) = {float(dE76):.2f}, ΔE00 (CIEDE2000) = {float(dE00):.2f}**")

    # ---------- Nhận xét tự động ----------
    nx = []
    if abs(dL) < 1:
        nx.append("Độ sáng gần như không đổi.")
    elif dL > 0:
        nx.append(f"Màu 2 **sáng hơn** màu 1 (ΔL\\* = {dL:.1f}).")
    else:
        nx.append(f"Màu 2 **tối hơn** màu 1 (ΔL\\* = {dL:.1f}).")

    if abs(da) >= 1:
        nx.append("Dịch chuyển về phía **đỏ** (a\\* tăng)." if da > 0
                  else "Dịch chuyển về phía **xanh lá** (a\\* giảm).")
    if abs(db) >= 1:
        nx.append("Dịch chuyển về phía **vàng** (b\\* tăng)." if db > 0
                  else "Dịch chuyển về phía **xanh dương** (b\\* giảm).")

    if abs(dC) < 1:
        nx.append("Độ bão hoà (chroma) gần như không đổi.")
    elif dC > 0:
        nx.append(f"Màu 2 **bão hoà hơn** (C\\* tăng {dC:.1f}).")
    else:
        nx.append(f"Màu 2 **nhạt/xỉn hơn** (C\\* giảm {abs(dC):.1f}).")

    dh = (h2 - h1 + 180) % 360 - 180
    if C1 > 5 and C2 > 5:
        nx.append(f"Góc sắc độ (hue) xoay {dh:+.1f}° (từ {h1:.0f}° đến {h2:.0f}°).")

    if dE00 < 1:
        muc = "mắt thường gần như không phân biệt được"
    elif dE00 < 2:
        muc = "chỉ người có kinh nghiệm mới nhận ra"
    elif dE00 < 10:
        muc = "nhận thấy được sự khác biệt"
    elif dE00 < 50:
        muc = "khác biệt rõ rệt"
    else:
        muc = "hai màu gần như đối lập"
    nx.append(f"Với ΔE00 = {float(dE00):.2f}: {muc}.")

    st.write("### Nhận xét sự chuyển dịch màu từ Lab1 sang Lab2")
    for t in nx:
        st.markdown("- " + t)
