# request函数，请求body为字典 返回也为字典
import requests

def request(url, body):
    # 请求数据，这里是空的字典
    data = body
    # 发送POST请求，使用json参数
    response = requests.post(url, json=data)
    res = response.json()
    if res["status"] == "success":
        if "card_list" in res:
            return res["card_list"]
        elif "index_list" in res:
            return res["index_list"]
        else:
            return[]
    return []


if __name__ == "__main__":
    address = "http://65d9dbc34e5b.ngrok-free.app"
    url1 = address + "/get_database_list"
    url2 = address + "/get_card_list"
    url3 = address + "/chat"
    url4 = address + "/get_card_recom"
    body1 = {}
    body2 = {"book_id": "1234"}
    body3 = {"pdf_path": "前端下载pdf后的 pdf path", "image_path": "image path", "prompt": "description"}
    body4 = {}
    res = request(url4, body4)
    print(res)
    # print("结果列表为:")
    # for index in res:
    #     print(index)
    #     print(index['book_name'])
    #     print(index['chunk_name'])