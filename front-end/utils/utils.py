import streamlit as st
import math
import uuid

# 辅助函数
def rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


# 知识库界面功能函数
def render_database(database, cards, DB_PAGE_SIZE, CARD_PAGE_SIZE):
    st.title("📚 数据库")
    total_pages = math.ceil(len(database) / DB_PAGE_SIZE)
    start = (st.session_state.db_page_num - 1) * DB_PAGE_SIZE
    end = start + DB_PAGE_SIZE
    db_page_data = database[start:end]

    for i in range(0, len(db_page_data), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i+j < len(db_page_data):
                item = db_page_data[i+j]
                with col:
                    st.markdown(f"**库名**: {item['book_name']}")
                    st.markdown(f"**描述**: {item['description']}")
                    if st.button("查看所有卡片", key=f"cards_{item['book_id']}"):
                        st.session_state.page = "cards"
                        st.session_state.selected_book = item['book_id']
                        st.session_state.card_page_num = 1
                        st.rerun()

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.db_page_num > 1:
            if st.button("⬅️ 上一页"):
                st.session_state.db_page_num -= 1
                st.rerun()
    with col2:
        st.write(f"第 {st.session_state.db_page_num} 页 / 共 {total_pages} 页")
    with col3:
        if st.session_state.db_page_num < total_pages:
            if st.button("下一页 ➡️"):
                st.session_state.db_page_num += 1
                st.rerun()


def render_cards(database, cards, DB_PAGE_SIZE, CARD_PAGE_SIZE):
    st.title("📝 卡片列表")
    book_id = st.session_state.selected_book
    book_cards = [c for c in cards if c['book_id'] == book_id]

    total_pages = math.ceil(len(book_cards) / CARD_PAGE_SIZE)
    start = (st.session_state.card_page_num - 1) * CARD_PAGE_SIZE
    end = start + CARD_PAGE_SIZE
    card_page_data = book_cards[start:end]

    for card in card_page_data:
        st.markdown(f"**书名**: {card['book_name']}")
        st.markdown(f"**Chunk**: {card['chunk_name']}")
        if st.button("查看详情", key=f"detail_{card['chunk_id']}"):
            st.session_state.page = "detail"
            st.session_state.selected_card = card
            st.rerun()
        st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.card_page_num > 1:
            if st.button("⬅️ 上一页", key="prev_card"):
                st.session_state.card_page_num -= 1
                st.rerun()
    with col2:
        st.write(f"第 {st.session_state.card_page_num} 页 / 共 {total_pages} 页")
    with col3:
        if st.session_state.card_page_num < total_pages:
            if st.button("下一页 ➡️", key="next_card"):
                st.session_state.card_page_num += 1
                st.rerun()

    if st.button("返回数据库"):
        st.session_state.page = "database"
        st.rerun()


def render_detail(database, cards, DB_PAGE_SIZE, CARD_PAGE_SIZE):
    st.title("🔍 卡片详情")
    card = st.session_state.selected_card
    st.markdown(f"**书名**: {card['book_name']}")
    st.markdown(f"**内容**: {card['content']}")

    st.markdown("**要点:**")
    for p in card['points']:
        st.write(f"- {p['point']} (难度: {p['difficulty']})")

    if st.button("返回卡片列表"):
        st.session_state.page = "cards"
        st.rerun()

# ============ 页面渲染 ============
def render_community(community_posts, POST_PAGE_SIZE, COMMENT_PAGE_SIZE):
    st.title("🌐 社区广场")

    # ------- 发帖功能 -------
    with st.expander("✍️ 发帖"):
        with st.form("new_post_form", clear_on_submit=True):
            title = st.text_input("帖子标题")
            author = st.text_input("作者昵称")
            description = st.text_area("帖子简介（简短描述）")
            content = st.text_area("帖子正文（详细内容）")
            submitted = st.form_submit_button("发布 🚀")

            if submitted:
                if title.strip() == "" or content.strip() == "":
                    st.warning("⚠️ 标题和正文不能为空")
                else:
                    new_post = {
                        "post_id": str(uuid.uuid4()),
                        "title": title,
                        "author": author if author else "匿名用户",
                        "description": description,
                        "content": content,
                        "comments": []
                    }
                    community_posts.insert(0, new_post)  # 新帖插入首页最前
                    st.success("✅ 发帖成功！")
                    st.rerun()

    # ------- 帖子分页展示 -------
    total_pages = math.ceil(len(community_posts) / POST_PAGE_SIZE)
    start = (st.session_state.post_page_num - 1) * POST_PAGE_SIZE
    end = start + POST_PAGE_SIZE
    page_posts = community_posts[start:end]

    for i in range(0, len(page_posts), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i+j < len(page_posts):
                post = page_posts[i+j]
                with col:
                    st.subheader(post["title"])
                    st.caption(f"作者: {post['author']}")
                    st.write(post["description"])
                    if st.button("查看帖子", key=f"post_{post['post_id']}"):
                        st.session_state.page = "post"
                        st.session_state.selected_post = post
                        st.session_state.comment_page_num = 1
                        st.rerun()

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.post_page_num > 1:
            if st.button("⬅️ 上一页"):
                st.session_state.post_page_num -= 1
                st.rerun()
    with col2:
        st.write(f"第 {st.session_state.post_page_num} 页 / 共 {total_pages} 页")
    with col3:
        if st.session_state.post_page_num < total_pages:
            if st.button("下一页 ➡️"):
                st.session_state.post_page_num += 1
                st.rerun()


def render_post(community_posts, POST_PAGE_SIZE, COMMENT_PAGE_SIZE):
    post = st.session_state.selected_post
    st.title(post["title"])
    st.caption(f"作者: {post['author']}")
    st.write(post["content"])

    st.markdown("### 💬 评论区")
    comments = post["comments"]
    total_pages = math.ceil(len(comments) / COMMENT_PAGE_SIZE) if comments else 1
    start = (st.session_state.comment_page_num - 1) * COMMENT_PAGE_SIZE
    end = start + COMMENT_PAGE_SIZE
    page_comments = comments[start:end]

    for c in page_comments:
        st.write(f"**{c['author']}**: {c['content']} 👍 {c['likes']}")
        if st.button("查看详情", key=f"comment_{c['comment_id']}"):
            st.session_state.page = "comment"
            st.session_state.selected_comment = c
            st.rerun()
        st.markdown("---")

    if comments:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.comment_page_num > 1:
                if st.button("⬅️ 上一页", key="prev_comment"):
                    st.session_state.comment_page_num -= 1
                    st.rerun()
        with col2:
            st.write(f"第 {st.session_state.comment_page_num} 页 / 共 {total_pages} 页")
        with col3:
            if st.session_state.comment_page_num < total_pages:
                if st.button("下一页 ➡️", key="next_comment"):
                    st.session_state.comment_page_num += 1
                    st.rerun()

    if st.button("返回社区"):
        st.session_state.page = "community"
        st.rerun()


def render_comment(community_posts, POST_PAGE_SIZE, COMMENT_PAGE_SIZE):
    c = st.session_state.selected_comment
    st.title("📝 评论详情")
    st.write(f"作者: {c['author']}")
    st.write(f"内容: {c['content']}")
    st.write(f"👍 点赞数: {c['likes']}")

    if st.button("返回帖子"):
        st.session_state.page = "post"
        st.rerun()
