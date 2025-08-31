import streamlit as st
from request.request import request

class Get_data:
    def __init__(self):
        self.cards_data1 = [
                {'book_id': '48602', 'chunk_id': 'chunk1', 'emb_id': '48602_chunk1',
                'points': [
                    {'point': '2025年特别报告发布背景', 'difficulty': '1', 'point_id': '48602_chunk1'},
                    {'point': '2025年特别报告主要目标', 'difficulty': '2', 'point_id': '48602_chunk1'},
                    {'point': '2025年特别报告数据分析结果', 'difficulty': '3', 'point_id': '48602_chunk1'},
                ],
                'content': '###chunk1: \n2025 年度特别报告',
                'book_name': 'china_trends.pdf',
                'chunk_name': 'china_trends.pdf:罗兰贝格中国行业趋势报告'
                },
                {'book_id': '995975', 'chunk_id': 'chunk1', 'emb_id': '995975_chunk1',
                'points': [{'point': '模态相互作用提供新的信息', 'difficulty': '4', 'point_id': '995975_chunk1'}],
                'content': '###chunk1: \nALBEF 模态交互研究',
                'book_name': 'MMOE_paper.pdf',
                'chunk_name': 'MMOE_paper.pdf:Abstract'
                },
                {'book_id': '995975', 'chunk_id': 'chunk5', 'emb_id': '995975_chunk5',
                'points': [
                    {'point': '回顾了之前研究中的多模态相互作用量化和学习方法', 'difficulty': 1, 'point_id': '995975_chunk5'},
                    {'point': 'MMOE框架允许在各种类型的模型上应用', 'difficulty': 3, 'point_id': '995975_chunk5'},
                    {'point': '提供了代码复现指导', 'difficulty': 1, 'point_id': '995975_chunk5'},
                ],
                'content': '###chunk5: \nWe cover related work...',
                'book_name': 'MMOE_paper.pdf',
                'chunk_name': 'MMOE_paper.pdf:2Related Work'
                },
                {'book_id': '995975', 'chunk_id': 'chunk6', 'emb_id': '995975_chunk5',
                'points': [
                    {'point': '回顾了之前研究中的多模态相互作用量化和学习方法', 'difficulty': 1, 'point_id': '995975_chunk5'},
                    {'point': 'MMOE框架允许在各种类型的模型上应用', 'difficulty': 3, 'point_id': '995975_chunk5'},
                    {'point': '提供了代码复现指导', 'difficulty': 1, 'point_id': '995975_chunk5'},
                ],
                'content': '###chunk5: \nWe cover related work...',
                'book_name': 'MMOE_paper.pdf',
                'chunk_name': 'MMOE_paper.pdf:2Related Work'
                },
                {'book_id': '2', 'chunk_id': 'chunk4', 'emb_id': '995975_chunk5',
                'points': [
                    {'point': '回顾了之前研究中的多模态相互作用量化和学习方法', 'difficulty': 1, 'point_id': '995975_chunk5'},
                    {'point': 'MMOE框架允许在各种类型的模型上应用', 'difficulty': 3, 'point_id': '995975_chunk5'},
                    {'point': '提供了代码复现指导', 'difficulty': 1, 'point_id': '995975_chunk5'},
                ],
                'content': '###chunk5: \nWe cover related work...',
                'book_name': '2.pdf',
                'chunk_name': 'MMOE_paper.pdf:2Related Work'
                },
                {'book_id': '2', 'chunk_id': 'chunk5', 'emb_id': '995975_chunk5',
                'points': [
                    {'point': '回顾了之前研究中的多模态相互作用量化和学习方法', 'difficulty': 1, 'point_id': '995975_chunk5'},
                    {'point': 'MMOE框架允许在各种类型的模型上应用', 'difficulty': 3, 'point_id': '995975_chunk5'},
                    {'point': '提供了代码复现指导', 'difficulty': 1, 'point_id': '995975_chunk5'},
                ],
                'content': '###chunk5: \nWe cover related work...',
                'book_name': '2.pdf',
                'chunk_name': 'MMOE_paper.pdf:2Related Work'
                },
                {'book_id': '2', 'chunk_id': 'chunk6', 'emb_id': '995975_chunk5',
                'points': [
                    {'point': '回顾了之前研究中的多模态相互作用量化和学习方法', 'difficulty': 1, 'point_id': '995975_chunk5'},
                    {'point': 'MMOE框架允许在各种类型的模型上应用', 'difficulty': 3, 'point_id': '995975_chunk5'},
                    {'point': '提供了代码复现指导', 'difficulty': 1, 'point_id': '995975_chunk5'},
                ],
                'content': '###chunk5: \nWe cover related work...',
                'book_name': '2.pdf',
                'chunk_name': 'MMOE_paper.pdf:2Related Work'
                },
                {'book_id': '5', 'chunk_id': 'chunk5', 'emb_id': '995975_chunk5',
                'points': [
                    {'point': '回顾了之前研究中的多模态相互作用量化和学习方法', 'difficulty': 1, 'point_id': '995975_chunk5'},
                    {'point': 'MMOE框架允许在各种类型的模型上应用', 'difficulty': 3, 'point_id': '995975_chunk5'},
                    {'point': '提供了代码复现指导', 'difficulty': 1, 'point_id': '995975_chunk5'},
                ],
                'content': '###chunk5: \nWe cover related work...',
                'book_name': '5.pdf',
                'chunk_name': 'MMOE_paper.pdf:2Related Work'
                },
                {'book_id': '5', 'chunk_id': 'chunk6', 'emb_id': '995975_chunk5',
                'points': [
                    {'point': '回顾了之前研究中的多模态相互作用量化和学习方法', 'difficulty': 1, 'point_id': '995975_chunk5'},
                    {'point': 'MMOE框架允许在各种类型的模型上应用', 'difficulty': 3, 'point_id': '995975_chunk5'},
                    {'point': '提供了代码复现指导', 'difficulty': 1, 'point_id': '995975_chunk5'},
                ],
                'content': '###chunk5: \nWe cover related work...',
                'book_name': '5.pdf',
                'chunk_name': 'MMOE_paper.pdf:2Related Work'
                },
                {'book_id': '7', 'chunk_id': 'chunk5', 'emb_id': '995975_chunk5',
                'points': [
                    {'point': '回顾了之前研究中的多模态相互作用量化和学习方法', 'difficulty': 1, 'point_id': '995975_chunk5'},
                    {'point': 'MMOE框架允许在各种类型的模型上应用', 'difficulty': 3, 'point_id': '995975_chunk5'},
                    {'point': '提供了代码复现指导', 'difficulty': 1, 'point_id': '995975_chunk5'},
                ],
                'content': '###chunk5: \nWe cover related work...',
                'book_name': '7.pdf',
                'chunk_name': 'MMOE_paper.pdf:2Related Work'
                },
                {'book_id': '7', 'chunk_id': 'chunk6', 'emb_id': '995975_chunk5',
                'points': [
                    {'point': '回顾了之前研究中的多模态相互作用量化和学习方法', 'difficulty': 1, 'point_id': '995975_chunk5'},
                    {'point': 'MMOE框架允许在各种类型的模型上应用', 'difficulty': 3, 'point_id': '995975_chunk5'},
                    {'point': '提供了代码复现指导', 'difficulty': 1, 'point_id': '995975_chunk5'},
                ],
                'content': '###chunk5: \nWe cover related work...',
                'book_name': '7.pdf',
                'chunk_name': 'MMOE_paper.pdf:2Related Work'
                }
            ]

        self.cards_data2 = [
                {'book_id': '48602', 'book_name': 'china_trends.pdf', 'description': '2025 年度特别报告'},
                {'book_id': '647931', 'book_name': 'spectral-based-graph-neural-networks.pdf', 'description': 'SComGNN 模型研究...'},
                {'book_id': '995975', 'book_name': 'MMOE_paper.pdf', 'description': '多模态交互研究论文'},
                {'book_id': '2', 'book_name': '2.pdf', 'description': '2025 年度特别报告'},
                {'book_id': '3', 'book_name': '3.pdf', 'description': 'SComGNN 模型研究...'},
                {'book_id': '4', 'book_name': '4.pdf', 'description': '多模态交互研究论文'},
                {'book_id': '5', 'book_name': '5.pdf', 'description': '2025 年度特别报告'},
                {'book_id': '6', 'book_name': '6.pdf', 'description': 'SComGNN 模型研究...'},
                {'book_id': '7', 'book_name': '7.pdf', 'description': '多模态交互研究论文'}
            ]

        self.cards_data3 = [
                {
                    "post_id": "p1",
                    "title": "如何快速上手Streamlit？",
                    "author": "Alice",
                    "description": "分享一下我学习Streamlit的经验和心得。",
                    "content": "这里是完整的帖子内容，包含了详细的Streamlit使用经验和代码示例……",
                    "comments": [
                        {"comment_id": "c1", "author": "Bob", "content": "写得太详细了，受益匪浅！", "likes": 5},
                        {"comment_id": "c2", "author": "Charlie", "content": "能不能再分享一下部署的方法？", "likes": 2},
                        {"comment_id": "c3", "author": "Daisy", "content": "支持一下，正好最近要做可视化！", "likes": 4},
                    ]
                },
                {
                    "post_id": "p2",
                    "title": "深度学习中的正则化技巧",
                    "author": "Eve",
                    "description": "总结一些常用的正则化方法，比如L2、Dropout等。",
                    "content": "完整内容：详细介绍了深度学习模型中过拟合问题的应对方式，包括数学推导与实验结果……",
                    "comments": [
                        {"comment_id": "c4", "author": "Frank", "content": "Dropout 真的很有效！", "likes": 3},
                        {"comment_id": "c5", "author": "Grace", "content": "能不能再对比一下L1和L2？", "likes": 1},
                    ]
                },
                # 心灵鸡汤和恋爱技巧
                {
                    "post_id": "p3",
                    "title": "如何找到内心的平静？",
                    "author": "Lily",
                    "description": "每个人都想找个属于自己的平静，你也可以。",
                    "content": "生活太忙碌，心情难以平复，但记得，你的情绪，最终由你自己掌控。🌿 不要让外界的喧嚣影响到你内心的声音。找到你的宁静区，无论是散步、阅读，还是静坐五分钟，给自己一些温柔的独处时光。",
                    "comments": []
                },
                {
                    "post_id": "p4",
                    "title": "恋爱中的小技巧——如何让对方更爱你",
                    "author": "James",
                    "description": "提高恋爱质量的小贴士。",
                    "content": "爱情不是一场追逐游戏，而是一种陪伴与成长。在感情中，我们要学会倾听、理解、并给予足够的空间。🕊️ 互相尊重，做自己，但也要在对方面前展示真正的自己。每天多一句关心的话，温暖一下对方的心。",
                    "comments": []
                },
                {
                    "post_id": "p5",
                    "title": "如何成为一个更有魅力的人？",
                    "author": "Emma",
                    "description": "每个人都有自己独特的魅力，发现它，展现它。",
                    "content": "魅力不仅仅来自外貌，更多的是内在的自信和智慧。📚 无论是通过提升自己的知识面，还是加强内在的情感表达，都能让你在人群中更有光彩。保持微笑，真诚待人，你的气质会感染周围的人。",
                    "comments": []
                },
                {
                    "post_id": "p6",
                    "title": "成功的秘诀，往往在于坚持",
                    "author": "Tim",
                    "description": "每一次的坚持，都会改变你的未来。",
                    "content": "许多人都渴望成功，但成功不是一蹴而就的。🌟 每天一点点的努力，都会在日积月累中产生巨大的变化。不放弃，走下去，成功的终点线会越来越近。",
                    "comments": []
                },
                {
                    "post_id": "p7",
                    "title": "如何保持一段健康的恋情？",
                    "author": "Sarah",
                    "description": "给情侣的一些小建议。",
                    "content": "健康的恋爱关系建立在信任、尊重和沟通之上。💌 经常沟通，哪怕是简单的问候，都会让感情更加稳固。尊重对方的独立性，并且在彼此需要的时候，毫不犹豫地站出来支持对方。",
                    "comments": []
                },
                {
                    "post_id": "p8",
                    "title": "学会在孤独中找到自我",
                    "author": "Natalie",
                    "description": "孤独并不等于寂寞，它是自我成长的契机。",
                    "content": "孤独的时光，不必害怕，它给了你时间去思考、去审视自己。🌙 学会享受独处，去做自己想做的事，这样你会发现，其实孤独是最好的自我陪伴。",
                    "comments": []
                },
                {
                    "post_id": "p9",
                    "title": "恋爱中的独立，才是最美的依赖",
                    "author": "Sophie",
                    "description": "在恋爱中要学会独立。",
                    "content": "在一段关系中，独立并不意味着分开，而是你有能力面对生活的挑战，而不是把所有压力都放在对方身上。🌺 保持自我成长，不依赖对方来完成你自己的生活，这样才能在彼此的世界中找到真正的平衡。",
                    "comments": []
                },
                {
                    "post_id": "p10",
                    "title": "如何正确处理感情中的争吵？",
                    "author": "Ben",
                    "description": "爱情中不可能没有争吵，学会如何处理它。",
                    "content": "争吵是感情中的一部分，关键在于如何沟通。💬 保持冷静，不要让情绪决定你的反应。争吵时试着站在对方的角度看问题，学会妥协和理解。争吵之后，主动道歉和恢复关系，让感情更加稳固。",
                    "comments": []
                }
            ]


    # 获取数据库的数据
    def get_data_from_sql(self, which_card):
        if which_card == "card1":
            return self.cards_data1
        elif which_card == "card2":
            return self.cards_data2
        else:  # 社区
            return self.cards_data3
        return self.cards_data1
    
    # 检查数据格式
    def check_valid(self, datas):
        valid_data = []
        for data in datas:
            if ("book_name" not in data) or ("chunk_name" not in data) or ("points" not in data) \
                 or (not isinstance(data["points"],list)) or (len(data["points"]) != 3):
                 continue
            valid_data.append(data)
        return(valid_data)

    # 设置数据库数据
    def set_data(self, which_card):
        if which_card == "card1":
            # tmp = request("http://65d9dbc34e5b.ngrok-free.app/get_card_recom", {})
            tmp = request("http://localhost:8000/get_card_recom", {})
            self.cards_data1 = self.check_valid(tmp)
        if which_card == "card2":
            pass
        if which_card == "card3":
            pass

all_data = Get_data()