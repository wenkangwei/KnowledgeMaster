import streamlit as st

# 自定义CSS样式
def load_css():
    st.markdown("""
    <style>
    /* 全局样式 */
    .main {
        padding: 0;
    }
    
    /* 侧边栏样式 - Kimi风格 */
    .profile-section {
        background: white;
        box-shadow: 0 2px 2px rgba(0, 0, 0, 0.05);
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

    /* 隐藏原始提示文本 */
    [data-testid="stFileUploaderDropzone"] div div span {
        display: none;
    }

    /* 隐藏其他次要文本 */
    [data-testid="stFileUploaderDropzone"] div div small {
        display: none;
    }

    /* 美化上传区域 */
    div[data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #f7fafc, #e9f7f6);
        border-radius: 16px;
        border: 1.5px solid #e0e0e0;
        padding: 15px;
        margin-bottom: 0rem;
        box-shadow: 0 2px 8px rgba(78, 205, 196, 0.06);
        transition: box-shadow 0.2s;
        width: 250px;
        max-width: 100%;
    }

    div[data-testid="stFileUploader"]:hover {
        box-shadow: 0 4px 16px rgba(78, 205, 196, 0.13);
    }

    /* 让整个dropzone区域变为flex居中布局 */
    [data-testid="stFileUploaderDropzone"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 120px; /* 可根据需要调整高度 */
        width: 100%;
        gap: 16px; /* 按钮和文字之间留出空间 */
    }

    /* 美化上传按钮 */
    div[data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 10px 20px;
        font-size: 12px;
        font-weight: 400;
        
        transition: all 0.2s;
        box-shadow: none;
        width: 100%;          /* 让按钮宽度合理 */
        margin: 0 auto;      /* 居中 */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    div[data-testid="stFileUploader"] button:hover {
        background: linear-gradient(135deg, #44a08d, #4ecdc4);
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 4px 14px rgba(78, 205, 196, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)