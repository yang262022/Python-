import streamlit as st

# 找零计算函数
def calculate_change(amount_due, amount_paid, denominations):
    change = round(amount_paid - amount_due, 2)
    if change < 0:
        return None, change

    result = {}
    for denom in sorted(denominations, reverse=True):
        count = int((change * 100) // (denom * 100))
        if count > 0:
            result[denom] = count
            change = round(change - denom * count, 2)
    return result, change

# Streamlit UI
st.set_page_config(page_title="找零计算器", layout="centered")
st.title("找零最优方案计算器")

# 输入金额
col1, col2 = st.columns(2)
with col1:
    amount_due = st.number_input("商品金额", min_value=0.01, value=13.75)
with col2:
    amount_paid = st.number_input("付款金额", min_value=0.01, value=20.00)

# 默认面额选项
default_denoms = [100, 50, 20, 10, 5, 1, 0.5, 0.1]
selected = st.multiselect("选择可用找零面额（单位：元）", default=default_denoms, options=default_denoms)

# 手动输入面额
custom_input = st.text_input("手动输入其他可用面额（用英文逗号分隔，如 2,0.2,0.05）")

# 解析手动输入的面额
custom_denoms = []
if custom_input:
    try:
        custom_denoms = list(set([float(x.strip()) for x in custom_input.split(',') if x.strip() != ""]))
    except ValueError:
        st.error("❌ 输入格式错误，请确保是数字并用英文逗号分隔")

# 合并所有面额并去重
final_denoms = sorted(set(selected + custom_denoms), reverse=True)

# 按钮
if st.button("计算找零方案"):
    if amount_paid < amount_due:
        st.error("❌ 付款金额不足！")
    elif not final_denoms:
        st.error("❌ 请选择或输入至少一个可用面额")
    else:
        result, remaining = calculate_change(amount_due, amount_paid, final_denoms)
        if result:
            st.success("✅ 找零方案如下：")
            for denom, count in result.items():
                st.markdown(f"- {denom:.2f} 元 × {count} 张/个")
            if remaining > 0:
                st.warning(f"⚠️ 剩余无法找零：{remaining:.2f} 元（面额不足）")
        else:
            st.info("无需找零，付款刚好！")
