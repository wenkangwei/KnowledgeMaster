import streamlit as st

# 获取数据库的数据
def get_data_from_es():
    if st.session_state.get('current_tab', '个人') == '个人':
        cards_data = [
            {"title": "Python基础教程", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "机器学习入门", "content": "了解机器学习的基本原理和常用算法"},
            {"title": "数据可视化", "content": "使用Python创建美观的数据图表和可视化"},
            {"title": "Web开发实践", "content": "构建现代化的Web应用程序"},
            {"title": "个人A", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "个人B", "content": "了解机器学习的基本原理和常用算法"},
            {"title": "个人C", "content": "使用Python创建美观的数据图表和可视化"},
            {"title": "个人D", "content": "构建现代化的Web应用程序"},
            {"title": "个人E", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "个人F", "content": "了解机器学习的基本原理和常用算法"},
            {"title": "个人G", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "个人H", "content": "了解机器学习的基本原理和常用算法"}
        ]
    elif st.session_state.current_tab == '知识库':
        cards_data = [
            {"title": "技术文档", "content": "各种编程语言和框架的官方文档"},
            {"title": "学习资源", "content": "精选的在线课程和教程资源"},
            {"title": "代码示例", "content": "实用的代码片段和项目模板"},
            {"title": "最佳实践", "content": "行业标准和开发最佳实践指南"},
            {"title": "知识库A", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "知识库B", "content": "了解机器学习的基本原理和常用算法"},
            {"title": "知识库C", "content": "使用Python创建美观的数据图表和可视化"},
            {"title": "知识库D", "content": "构建现代化的Web应用程序"},
            {"title": "知识库E", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "知识库F", "content": "了解机器学习的基本原理和常用算法"},
            {"title": "知识库G", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "知识库H", "content": "了解机器学习的基本原理和常用算法"}
        ]
    else:  # 社区
        cards_data = [
            {"title": "热门讨论", "content": "社区中最受关注的技术话题讨论"},
            {"title": "项目分享", "content": "用户分享的优秀开源项目"},
            {"title": "经验交流", "content": "开发者们的实战经验分享"},
            {"title": "问答互助", "content": "技术问题的解答和互助"},
            {"title": "社区A", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "社区B", "content": "了解机器学习的基本原理和常用算法"},
            {"title": "社区C", "content": "使用Python创建美观的数据图表和可视化"},
            {"title": "社区D", "content": "构建现代化的Web应用程序"},
            {"title": "社区E", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "社区F", "content": "了解机器学习的基本原理和常用算法"},
            {"title": "社区G", "content": "从零开始学习Python编程语言的基础知识和核心概念"},
            {"title": "社区H", "content": "了解机器学习的基本原理和常用算法"}
        ]
    return cards_data