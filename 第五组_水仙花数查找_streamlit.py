import streamlit as st

# 判断一个数是否为水仙花数
def is_armstrong(num):
    digits = list(map(int, str(num)))
    n = len(digits)
    return num == sum([d ** n for d in digits])

# 查找所有 n 位水仙花数
def find_armstrong_numbers(n_digits):
    start = 10 ** (n_digits - 1)
    end = 10 ** n_digits
    return [i for i in range(start, end) if is_armstrong(i)]

# 设置页面信息
st.set_page_config(page_title="水仙花数查找器", layout="centered")

# 页面标题与说明
st.markdown("<h1 style='text-align: center;'>🌸 水仙花数查找器</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>自动查找 n 位的所有水仙花数（阿姆斯特朗数）</p>", unsafe_allow_html=True)
st.markdown("---")

# 滑动条选择位数（3~7）
n = st.slider("🔢 请选择位数 n", min_value=3, max_value=10, value=3, step=1)

# 按钮触发
if st.button("🚀 查找水仙花数"):
    with st.spinner("计算中，请稍候..."):
        result = find_armstrong_numbers(n)
    st.markdown("---")
    if result:
        st.success(f"✅ 共找到 {len(result)} 个 {n} 位水仙花数！")
        st.code(", ".join(map(str, result)), language="python")
    else:
        st.warning("⚠️ 未找到符合条件的水仙花数。")

# 页脚说明
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #999;'>Made with ❤️ using Streamlit</p>",
    unsafe_allow_html=True
)
