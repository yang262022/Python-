import streamlit as st
import pandas as pd

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

# 页面配置
st.set_page_config(page_title="找零计算器", page_icon="💰", layout="centered")

# 自定义样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1E88E5;
        margin-bottom: 2rem;
    }
    .input-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .result-section {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .warning-section {
        background-color: #fff3e0;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .btn-container {
        text-align: center;
        margin: 2rem 0;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #0D47A1;
    }
    .denom-section {
        margin-bottom: 2rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #6c757d;
    }
    .stTable th {
        background-color: #1E88E5;
        color: white;
    }
    .stTable tr:nth-child(even) {
        background-color: #f2f2f2;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>💰 找零最优方案计算器</h1>", unsafe_allow_html=True)

# 输入金额区域
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    amount_due = st.number_input("商品金额（元）", min_value=0.01, value=13.75, step=0.01, format="%.2f")
with col2:
    amount_paid = st.number_input("付款金额（元）", min_value=0.01, value=20.00, step=0.01, format="%.2f")
st.markdown("</div>", unsafe_allow_html=True)

# 面额选择区域
st.markdown("<div class='denom-section'>", unsafe_allow_html=True)
# 默认面额选项
default_denoms = [100, 50, 20, 10, 5, 1, 0.5, 0.1]
selected = st.multiselect(
    "选择可用找零面额（单位：元）",
    options=default_denoms,
    default=default_denoms,
    help="可多选，默认包含常用纸币和硬币面额"
)

# 手动输入面额
custom_input = st.text_input(
    "手动输入其他可用面额（用英文逗号分隔，如 2,0.2,0.05）",
    placeholder="例如：2,0.2,0.05"
)
st.markdown("</div>", unsafe_allow_html=True)

# 解析手动输入的面额
custom_denoms = []
if custom_input:
    try:
        custom_denoms = list(set([float(x.strip()) for x in custom_input.split(',') if x.strip() != ""]))
    except ValueError:
        st.error("❌ 输入格式错误，请确保是数字并用英文逗号分隔")

# 合并所有面额并去重
final_denoms = sorted(set(selected + custom_denoms), reverse=True)

# 计算按钮
st.markdown("<div class='btn-container'>", unsafe_allow_html=True)
if st.button("计算找零方案"):
    st.markdown("</div>", unsafe_allow_html=True)
    if amount_paid < amount_due:
        st.error("❌ 付款金额不足！")
    elif not final_denoms:
        st.error("❌ 请选择或输入至少一个可用面额")
    else:
        result, remaining = calculate_change(amount_due, amount_paid, final_denoms)
        if result:
            st.markdown("<div class='result-section'>", unsafe_allow_html=True)
            st.success(f"✅ 找零总额：{round(amount_paid - amount_due, 2):.2f} 元")
            # 表格展示找零方案
            df_result = pd.DataFrame({
                "面额（元）": [f"{denom:.2f}" for denom in result.keys()],
                "张/个数": list(result.values())
            })
            st.table(df_result)
            st.markdown("</div>", unsafe_allow_html=True)
            if remaining > 0:
                st.markdown("<div class='warning-section'>", unsafe_allow_html=True)
                st.warning(f"⚠️ 剩余无法找零：{remaining:.2f} 元（面额不足）")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("无需找零，付款刚好！")
else:
    st.markdown("</div>", unsafe_allow_html=True)

# 页脚
st.markdown("<div class='footer'>💡 提示：选择常用面额或自定义面额，快速计算最优找零方案</div>", unsafe_allow_html=True)
