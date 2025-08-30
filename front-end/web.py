import streamlit as st
import time
from datetime import datetime
import base64
from streamlit_autorefresh import st_autorefresh

from css.css import load_css
from get_data.get_data import get_data_from_es
from utils.utils import rerun

# 页面配置
st.set_page_config(
    page_title="KnowledgeMaster",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 每隔5秒自动刷新一次页面（10000毫秒）
st_autorefresh(interval=5000, key="auto_refresh")

# 初始化会话状态
def init_session_state():
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = '个人'
    if 'chat_mode' not in st.session_state:
        st.session_state.chat_mode = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'search_history' not in st.session_state:
        st.session_state.search_history = [
            "Python机器学习基础",
            "深度学习入门指南",
            "数据科学工具箱",
            "AI应用开发实践"
        ]
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': 'KnowledgeMaster',
            'email': 'KnowledgeMaster@example.com',
            'bio': '你好呀，我是KnowledgeMaster，一款让知识库”主动““讨好”您的AI Agent。'
        }

# 顶部导航栏
def render_top_nav():
    st.markdown("""
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("个人", key="tab_personal", use_container_width=True):
            st.session_state.current_tab = '个人'
            st.session_state.chat_mode = False
    
    with col2:
        if st.button("知识库", key="tab_knowledge", use_container_width=True):
            st.session_state.current_tab = '知识库'
            st.session_state.chat_mode = False
    
    with col3:
        if st.button("社区", key="tab_community", use_container_width=True):
            st.session_state.current_tab = '社区'
            st.session_state.chat_mode = False
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# 用户上传知识功能
def render_input_section():
    st.markdown('', unsafe_allow_html=True)
    st.subheader("💭 输入您的收藏")
    user_input = st.text_input("注: 文字/图片/文件", key="user_input", placeholder="请输入...")
    uploader_container = st.container()
    with uploader_container:
        col = st.columns(1)[0]  # 或者直接使用 st.beta_expander 或不使用列
        # 图片上传
        with col:  # 如果不使用列，则直接放在 uploader_container 下
            uploaded_image = st.file_uploader("📷图片", type=['png', 'jpg', 'jpeg'], key="image_upload")
            st.markdown('''<style>
                /* 直接在这里应用针对 file_uploader 的样式调整，如果必要的话 */
                div[data-testid="stFileUploaderDropzone"] {
                    min-height: 60px; /* 减少高度 */
                    padding: 5px; /* 减少内边距 */
                }
            </style>''', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("📄文件", type=['pdf', 'txt', 'docx'], key="file_upload")
            st.markdown('''<style>
                /* 直接在这里应用针对 file_uploader 的样式调整，如果必要的话 */
                div[data-testid="stFileUploaderDropzone"] {
                    min-height: 60px; /* 减少高度 */
                    padding: 5px; /* 减少内边距 */
                }
            </style>''', unsafe_allow_html=True)
        # upload_button_col = st.column(width=0.3)  # 可选：限制按钮列宽
        if st.button("⬆", use_container_width=True, type="primary"):
            if user_input or uploaded_image or uploaded_file:
                # 上传到后端逻辑
                print("你输入的文字为：", user_input)
                print("你输入的图片为：", uploaded_image)
                print("你输入的文件为：", uploaded_file)
                st.rerun()

# 侧边栏
def render_sidebar():
    st.markdown("""
    <style>
    .st-emotion-cache-1xgtwnd {
        padding-top: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)
    with st.sidebar:        
        # 个人信息编辑
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.subheader("👤 个人信息")
        
        with st.expander("编辑个人信息", expanded=False):
            new_name = st.text_input("姓名", value=st.session_state.user_profile['name'])
            new_email = st.text_input("邮箱", value=st.session_state.user_profile['email'])
            new_bio = st.text_area("个人简介", value=st.session_state.user_profile['bio'])
            
            if st.button("保存信息"):
                st.session_state.user_profile = {
                    'name': new_name,
                    'email': new_email,
                    'bio': new_bio
                }
                st.success("信息已保存！")
        
        # 显示当前个人信息
        st.write(f"**姓名:** {st.session_state.user_profile['name']}")
        st.write(f"**邮箱:** {st.session_state.user_profile['email']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 搜索历史
        st.subheader("📚 回顾列表")
        for i, item in enumerate(st.session_state.search_history):
            if st.button(f"📖 {item}", key=f"history_{i}", use_container_width=True):
                st.session_state.chat_mode = True
                # 模拟加载历史对话
                st.session_state.chat_history = [
                    {"role": "user", "content": f"告诉我关于{item}的信息"},
                    {"role": "assistant", "content": f"这是关于{item}的详细信息..."}
                ]
        # 输入区域
        render_input_section()
        st.markdown('</div>', unsafe_allow_html=True)

def search_input_section():
    st.markdown('', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([4, 3, 1])

    with col1:
        st.markdown(f"### 📋 {st.session_state.current_tab}推荐")
    with col2:
        search_input = st.text_input("test",placeholder="请模糊输入关键词",key="search_box",label_visibility="collapsed")
    with col3:
        search_clicked = st.button("🔍搜索", use_container_width=True)
    if search_clicked and search_input:
        # 执行搜索 并返回数据
        print("你搜索的关键字为: ", search_input)
        st.rerun()

# 知识卡片网格
def render_knowledge_cards():
    cards_data = get_data_from_es()
    search_input_section()
    cards_per_page = 4
    total_cards = len(cards_data)
    total_pages = (total_cards + cards_per_page - 1) // cards_per_page

    # 初始化分页和计时
    if 'card_page_idx' not in st.session_state:
        st.session_state.card_page_idx = 0
    if 'last_cards_refresh' not in st.session_state:
        st.session_state.last_cards_refresh = time.time()

    # 自动翻页（每10秒）
    now = time.time()
    if now - st.session_state.last_cards_refresh > 5:
        st.session_state.card_page_idx = (st.session_state.card_page_idx + 1) % total_pages
        st.session_state.last_cards_refresh = now
        rerun()

    # 展示当前页的卡片
    start = st.session_state.card_page_idx * cards_per_page
    end = start + cards_per_page
    cards_to_show = cards_data[start:end]

    # 用自定义grid美化
    st.markdown('<div class="card-grid">', unsafe_allow_html=True)
    # 两列布局
    col1, col2 = st.columns(2)
    for i, card in enumerate(cards_to_show):
        with col1 if i % 2 == 0 else col2:
            with st.container():
                st.markdown(f"""
                <div class="knowledge-card">
                    <div class="card-title">{card['title']}</div>
                    <div class="card-content">{card['content']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"查看详情", key=f"card_{start + i}", use_container_width=True):
                    st.session_state.chat_mode = True
                    st.session_state.chat_history = [
                        {"role": "user", "content": f"告诉我更多关于{card['title']}的信息"},
                        {"role": "assistant", "content": f"关于{card['title']}：{card['content']}。这里是更详细的信息..."}
                    ]
    
    # 上一页/下一页按钮 + 页码
    prev_col, page_col, next_col = st.columns([1,3,1])
    with prev_col:
        if st.button("上一页", key="prev_page"):
            st.session_state.card_page_idx = (st.session_state.card_page_idx - 1) % total_pages
            st.session_state.last_cards_refresh = time.time()
            rerun()
    with next_col:
        if st.button("下一页", key="next_page"):
            st.session_state.card_page_idx = (st.session_state.card_page_idx + 1) % total_pages
            st.session_state.last_cards_refresh = time.time()
            rerun()
    with page_col:
        st.markdown(
            f"<div style='text-align:center; font-size:16px; margin-top:10px;'>"
            f"第 <b>{st.session_state.card_page_idx + 1}</b> / <b>{total_pages}</b> 页"
            f"</div>",
            unsafe_allow_html=True
        )


# 聊天界面
def render_chat_interface():
    st.markdown("### 💬 智能对话")
    
    # 返回按钮
    if st.button("⬅️ 返回卡片视图"):
        st.session_state.chat_mode = False
        st.rerun()
    
    # 聊天历史
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)

def chat_input_section():
    st.markdown('', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])  # 左宽右窄

    with col1:
        user_input = st.text_input(
            "💭 输入您的问题或搜索内容...",
            key="chat_input",
            placeholder="请输入您想了解的内容",
            label_visibility="collapsed"  # 隐藏label
        )
    with col2:
        send_clicked = st.button("🚀 发送", use_container_width=True)
    # 仅在点击按钮且有输入时触发
    if send_clicked and user_input:
        # 切换到聊天模式
        st.session_state.chat_mode = True
        # 添加用户消息
        st.session_state.chat_history.append({
            "role": "user", 
            "content": user_input
        })

        # 模拟AI回复
        time.sleep(1)
        ai_response = f"我理解您想了解关于'{user_input}'的信息。这是一个很好的问题！让我为您详细解答..."

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_response
        })

        # 添加到搜索历史
        if user_input not in st.session_state.search_history:
            st.session_state.search_history.insert(0, user_input)
            if len(st.session_state.search_history) > 10:
                st.session_state.search_history.pop()
        st.rerun()

# 主函数
def main():
    st.markdown("""
    <style>
    /* 隐藏 Streamlit 默认的菜单和页脚 */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    /* 去除主内容区的 padding 顶部间距 */
    .block-container {
        padding-top: 0rem !important;  /* 你可以调成0rem或1rem，看需求 */
    }
    </style>
    """, unsafe_allow_html=True)
    load_css()
    init_session_state()
    # 渲染顶部导航
    render_top_nav()
    # 渲染侧边栏
    render_sidebar()
    # 主内容区域
    if st.session_state.chat_mode:
        render_chat_interface()
    else:
        render_knowledge_cards()
    # 聊天输入区域
    chat_input_section()
    
if __name__ == "__main__":
    main()
