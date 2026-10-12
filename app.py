import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Quản lý điểm sinh viên", page_icon="🎓", layout="wide")
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 1. Tạo DataFrame gồm 10 sinh viên
student_data = {
    "Ho_ten": ["Nguyễn Văn An", "Trần Thị Bình", "Lê Minh Châu", "Phạm Quốc Dũng", "Hoàng Thu Hà", "Võ Thanh Hùng", "Đặng Ngọc Lan", "Bùi Gia Minh", "Đỗ Hải Nam", "Lê Thảo Vy"],
    "Chuyen_can": [9, 8, 10, 7, 9, 6, 8, 10, 5, 9],
    "Giua_ky": [8, 7, 9, 6, 8, 5, 7, 9, 4, 8],
    "Cuoi_ky": [9, 8, 9, 7, 8, 4, 7, 9, 3, 9],
}
df = pd.DataFrame(student_data)

# 2. Tính điểm tổng kết
df["Tong_ket"] = (df["Chuyen_can"] * 0.2 + df["Giua_ky"] * 0.3 + df["Cuoi_ky"] * 0.5).round(2)

# 3. Xếp loại sinh viên
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 4. Hiển thị bảng điểm
st.subheader("Bảng điểm của 10 sinh viên")
st.dataframe(df.rename(columns={"Ho_ten": "Họ tên", "Chuyen_can": "Chuyên cần", "Giua_ky": "Giữa kỳ", "Cuoi_ky": "Cuối kỳ", "Tong_ket": "Tổng kết", "Xep_loai": "Xếp loại"}), use_container_width=True, hide_index=True)

# 5. Thống kê lớp
diem_tb = df["Tong_ket"].mean()
diem_max = df["Tong_ket"].max()
diem_min = df["Tong_ket"].min()
so_dat = int((df["Tong_ket"] >= 5).sum())

st.subheader("Thống kê điểm lớp")
c1, c2, c3 = st.columns(3)
c1.metric("Điểm trung bình", f"{diem_tb:.2f}")
c2.metric("Điểm cao nhất", f"{diem_max:.2f}")
c3.metric("Số sinh viên đạt", f"{so_dat}/{len(df)}")

cao_nhat = df.loc[df["Tong_ket"] == diem_max, "Ho_ten"].tolist()
thap_nhat = df.loc[df["Tong_ket"] == diem_min, "Ho_ten"].tolist()
st.write(f"**Sinh viên có điểm cao nhất:** {', '.join(cao_nhat)} ({diem_max:.2f} điểm)")
st.write(f"**Sinh viên có điểm thấp nhất:** {', '.join(thap_nhat)} ({diem_min:.2f} điểm)")

# 6. Tra cứu điểm sinh viên
st.subheader("Tra cứu điểm sinh viên")
ten_chon = st.selectbox("Chọn một sinh viên", df["Ho_ten"].tolist())
sv = df.loc[df["Ho_ten"] == ten_chon].iloc[0]
st.write(f"**Họ tên:** {sv['Ho_ten']}")
st.write(f"**Điểm chuyên cần:** {sv['Chuyen_can']}")
st.write(f"**Điểm giữa kỳ:** {sv['Giua_ky']}")
st.write(f"**Điểm cuối kỳ:** {sv['Cuoi_ky']}")
st.write(f"**Điểm tổng kết:** {sv['Tong_ket']:.2f}")
st.write(f"**Xếp loại:** {sv['Xep_loai']}")

# 7. Biểu đồ cột điểm tổng kết
st.subheader("Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(range(len(df)), df["Tong_ket"], color="skyblue", edgecolor="black")
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.1, f"{h:.2f}", ha="center", fontsize=9)
ax.set_title("Biểu đồ điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Họ và tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.set_xticks(range(len(df)))
ax.set_xticklabels(df["Ho_ten"], rotation=45, ha="right")
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# 8. Thông tin người thực hiện
st.divider()
st.caption("Người thực hiện: Lê Tiến | MSSV: 038208029836")
