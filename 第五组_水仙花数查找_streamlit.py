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

# Streamlit UI
st.set_page_config(page_title="水仙花数查找器", layout="centered")
st.title("水仙花数查找器")

# 输入 n
n = st.number_input("请输入位数 n（7 ≥ n ≥ 3）", min_value=3, max_value=7, value=3)

# 触发计算
if st.button("查找水仙花数"):
    result = find_armstrong_numbers(n)
    if result:
        ans = (", ".join(map(str, result)))
        st.success(f"共找到 {len(result)} 个 {n} 位水仙花数：[{ans}]")
    else:
        st.warning("未找到符合条件的水仙花数")
