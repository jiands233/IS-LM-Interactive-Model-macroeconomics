import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 页面全局配置：设置标题和宽屏布局，保障视觉开阔
st.set_page_config(page_title="IS-LM 宏观经济模拟器", layout="wide")
st.title("📈 IS-LM 宏观经济政策动态模拟器")
st.markdown("通过左侧面板调节参数，直观观察财政政策与货币政策对国民收入(Y)和利率(r)的综合影响。")

# 2. 侧边栏：丝滑的参数调节控制台
st.sidebar.header("🕹️ 宏观经济参数调节")

st.sidebar.subheader("财政政策与微观消费")
G = st.sidebar.slider("政府购买 (G)", 100, 1000, 500, step=10)
T = st.sidebar.slider("税收 (T)", 100, 1000, 500, step=10)
c = st.sidebar.slider("边际消费倾向 (c)", 0.1, 0.9, 0.8, step=0.05)
d = st.sidebar.slider("投资对利率的敏感度 (d)", 10, 200, 50, step=5)
A = st.sidebar.slider("自发性支出总和 (A)", 100, 2000, 1000, step=50)

st.sidebar.subheader("货币政策与流动性偏好")
M = st.sidebar.slider("名义货币供给 (M)", 500, 3000, 1500, step=50)
P = st.sidebar.slider("价格水平 (P)", 0.5, 3.0, 1.0, step=0.1)
k = st.sidebar.slider("货币需求的收入敏感度 (k)", 0.1, 1.0, 0.5, step=0.05)
h = st.sidebar.slider("货币需求的利率敏感度 (h)", 10, 200, 50, step=5)

# 3. 核心代数逻辑（依据曼昆宏观经济学原理推导）
# IS方程: r = (A + G - c*T)/d - (1-c)/d * Y
# LM方程: r = (k/h)*Y - M/(P*h)

# 计算均衡点 (Y*, r*)
term1 = (1 - c) / d
term2 = k / h
term3 = (A + G - c * T) / d
term4 = M / (P * h)

Y_star = (term3 + term4) / (term1 + term2)
r_star = term2 * Y_star - term4

# 生成X轴范围数据，确保交点始终在视野中心附近
Y = np.linspace(max(0, Y_star - 1500), Y_star + 1500, 500)

# 计算对应的Y轴(利率)数据
IS_r = (A + G - c * T) / d - ((1 - c) / d) * Y
LM_r = (k / h) * Y - M / (P * h)

# 4. 界面绘制：使用 Plotly 构建精致的动态交互图表
fig = go.Figure()

# 绘制IS曲线
fig.add_trace(go.Scatter(
    x=Y, y=IS_r, mode='lines', name='IS 曲线 (产品市场)', 
    line=dict(color='#FF6B6B', width=4, shape='spline')
))

# 绘制LM曲线
fig.add_trace(go.Scatter(
    x=Y, y=LM_r, mode='lines', name='LM 曲线 (货币市场)', 
    line=dict(color='#4ECDC4', width=4, shape='spline')
))

# 标记高光交点
fig.add_trace(go.Scatter(
    x=[Y_star], y=[r_star], mode='markers+text', 
    name='均衡点 (Y*, r*)',
    text=[f'均衡点<br>Y*={Y_star:.1f}<br>r*={r_star:.2f}'],
    textposition="top center",
    textfont=dict(size=14),
    marker=dict(color='#FFE66D', size=14, line=dict(width=2, color='white'))
))

# 设定图表美学排版
fig.update_layout(
    xaxis_title="国民收入 (Y)",
    yaxis_title="利率 (r)",
    yaxis=dict(range=[max(0, r_star - 15), r_star + 15]),
    template="plotly_dark", # 现代感暗色主题
    hovermode="x unified",  # 丝滑的鼠标悬停提示
    legend=dict(yanchor="top", y=0.95, xanchor="right", x=0.95),
    margin=dict(l=40, r=40, t=40, b=40)
)

# 渲染图表到页面
st.plotly_chart(fig, use_container_width=True)

# 5. 底部数据看板
st.markdown("### 📊 实时经济指标")
col1, col2 = st.columns(2)
col1.metric("当前均衡国民收入 (Y*)", f"{Y_star:.2f}")
col2.metric("当前均衡利率 (r*)", f"{r_star:.2f}%")