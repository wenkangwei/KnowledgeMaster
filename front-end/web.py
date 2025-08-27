import streamlit as st
import time
from datetime import datetime
import base64

# 页面配置
st.set_page_config(
    page_title="知识卡片应用",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
def load_css():
    st.markdown("""
    <style>
    /* 全局样式 */
    .main {
        padding: 0;
    }
    
    /* 顶部导航栏样式 - 小红书风格 */
    .top-nav {
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
    }
    
    .nav-tabs {
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    
    .nav-tab {
        background: rgba(255, 255, 255, 0.9);
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #333;
        font-size: 16px;
    }
    
    .nav-tab.active {
        background: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    /* 侧边栏样式 - Kimi风格 */
    .sidebar {
        background: linear-gradient(180deg, #f8f9fa, #e9ecef);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .profile-section {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .history-item {
        background: white;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
        border-left: 4px solid #ff6b6b;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .history-item:hover {
        transform: translateX(5px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* 知识卡片网格 - 小红书风格 */
    .card-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        padding: 20px;
    }
    
    .knowledge-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }
    
    .knowledge-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border-color: #ff6b6b;
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #333;
        margin-bottom: 10px;
    }
    
    .card-content {
        color: #666;
        line-height: 1.6;
    }
    
    /* 聊天界面样式 - Kimi风格 */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        max-height: 500px;
        overflow-y: auto;
    }
    
    .chat-message {
        margin-bottom: 15px;
        padding: 12px 16px;
        border-radius: 12px;
        max-width: 80%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background: #f1f3f4;
        color: #333;
        margin-right: auto;
    }
    
    /* 输入区域样式 */
    .input-section {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .upload-buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    
    .upload-btn {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .upload-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
    }
    
    /* 隐藏Streamlit默认元素 */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

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
            'name': '用户名',
            'email': 'user@example.com',
            'bio': '这里是个人简介...'
        }

# 顶部导航栏
def render_top_nav():
    st.markdown("""
    <div class="top-nav">
        <div class="nav-tabs">
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

# 侧边栏
def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        
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
        
        st.markdown('</div>', unsafe_allow_html=True)

# 知识卡片网格
def render_knowledge_cards():
    if st.session_state.current_tab == '个人':
        cards_data = [
            {"title": "Python基础教程", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "机器学习入门", "content": "了解机器学习的基本原理和常用算法"},
            {"title": "数据可视化", "content": "使用Python创建美观的数据图表和可视化"},
            {"title": "Web开发实践", "content": "构建现代化的Web应用程序"}
        ]
    elif st.session_state.current_tab == '知识库':
        cards_data = [
            {"title": "技术文档", "content": "各种编程语言和框架的官方文档"},
            {"title": "学习资源", "content": "精选的在线课程和教程资源"},
            {"title": "代码示例", "content": "实用的代码片段和项目模板"},
            {"title": "最佳实践", "content": "行业标准和开发最佳实践指南"}
        ]
    else:  # 社区
        cards_data = [
            {"title": "热门讨论", "content": "社区中最受关注的技术话题讨论"},
            {"title": "项目分享", "content": "用户分享的优秀开源项目"},
            {"title": "经验交流", "content": "开发者们的实战经验分享"},
            {"title": "问答互助", "content": "技术问题的解答和互助"}
        ]
    
    st.markdown(f"### 📋 {st.session_state.current_tab}推荐")
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    for i, card in enumerate(cards_data):
        with col1 if i % 2 == 0 else col2:
            with st.container():
                st.markdown(f"""
                <div class="knowledge-card">
                    <div class="card-title">{card['title']}</div>
                    <div class="card-content">{card['content']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"查看详情", key=f"card_{i}", use_container_width=True):
                    st.session_state.chat_mode = True
                    st.session_state.chat_history = [
                        {"role": "user", "content": f"告诉我更多关于{card['title']}的信息"},
                        {"role": "assistant", "content": f"关于{card['title']}：{card['content']}。这里是更详细的信息..."}
                    ]

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

# 输入区域
def render_input_section():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # 搜索输入框
    user_input = st.text_input("💭 输入您的问题或搜索内容...", key="user_input", placeholder="请输入您想了解的内容")
    
    # 文件上传区域
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        uploaded_image = st.file_uploader("📷 上传图片", type=['png', 'jpg', 'jpeg'], key="image_upload")
    
    with col2:
        uploaded_file = st.file_uploader("📄 上传文件", type=['pdf', 'txt', 'docx'], key="file_upload")
    
    with col3:
        if st.button("🚀 发送", use_container_width=True, type="primary"):
            if user_input:
                # 切换到聊天模式
                st.session_state.chat_mode = True
                
                # 添加用户消息
                st.session_state.chat_history.append({
                    "role": "user", 
                    "content": user_input
                })
                
                # 模拟AI回复
                time.sleep(1)  # 模拟处理时间
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# 主函数
def main():
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
    
    # 输入区域
    render_input_section()

if __name__ == "__main__":
    main()
