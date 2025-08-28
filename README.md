# 项目： KnowledgeMaster
## 框架架构

## 前端功能描述

## 后端接口描述
假设当前本地运行： http://localhost:8000
1. 请求用户历史上传的书籍/文本列表 (对应知识库列表)
- 接口:  ```http://localhost:8000/get_database_list```
- 请求格式: 任意json格式请求
- 返回结果: ``` {"status":"success", "msg":"", "index_list":[book_id1, book_id2,book_id3]} ```


2. 请求大模型对用户pdf/文本解析拆分后的知识卡片列表
- 接口:  ```http://localhost:8000/get_card_list```
- 请求格式:  book_id是知识库id
```json
    {
        "book_id":"640507"
    }
```
- 返回结果: 
    ```json
    {"status":"success", msg:"" ,
                "card_list": [{"book_id":"id","chunk_id":"chunk_id", "content": "content" ,"points":[{"point":"", "difficulty"},{"point":"", "difficulty"}]},
                ]}
    ```
- 解释: status返回success或者failed状态。 msg：错误信息。 card_list 返回请求的知识库的所有知识卡片json格式的信息。 每个知识卡片json里有 book_id(知识库id)， chunk_id(把用户的知识库拆分成多个内容块后的内容块id), content( 内容块的文本)， points: 当前内容块的知识点列表。 每个知识点有point(内容)和difficulty(难度)2个字段.



3. 请求大模型对话接口
- 接口:  ```http://localhost:8000/chat```
- 请求格式: 
```json
        {
            "pdf_path": "前端下载pdf后的 pdf path",
            "image_path": "image path",
            "prompt": "description",
        }
```
- 返回结果: ``` {"status":"success", "response":""} ```
- 解释: 返回状态和大模型返回的文本内容


## 例子
- 查看KnowledgeMaster/utils/test_ollama.sh 里面的curl请求例子