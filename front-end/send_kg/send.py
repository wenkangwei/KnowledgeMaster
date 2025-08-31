# # send to llm
# import requests

# def send_kg(text, picture_path, file_path):
#     # URL of the API endpoint
#     url = 'https://1a8071138f26.ngrok-free.app/chat_v2'  # 替换为你的API URL

#     print(text)
#     print(picture_path)
#     print(file_path)

#     # Prepare the files and data for the POST request
#     files = {
#         'pdf_path': open(file_path, 'rb'),  # Open the PDF file in binary mode
#         'image_path': open(picture_path, 'rb'),  # Open the WAV file in binary mode (note: parameter name might not be accurate)
#         'prompt': (None, text)  # The prompt text is sent as a field without a file
#     }

#     # Send the POST request
#     try:
#         response = requests.post(url, files=files, timeout=(30, 60))
#         print(response.status_code)
#         print(response.text)
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")

#     # # Check the response status and content
#     # if response.status_code == 200:
#     #     print('Request successful!')
#     #     print(response.json())  # Assuming the server returns JSON, adjust as necessary
#     # else:
#     #     print(f'Request failed with status code: {response.status_code}')
#     #     print(response.text)  # Print the error message or other response content

#     # Close the file handles (they will be closed automatically when the script ends, but it's good practice to close them explicitly)
#     files['pdf_path'].close()
#     files['image_path'].close()

# if __name__ == "__main__":
#     send_kg("test", "/Users/zhuzhenwei/Desktop/zzw_code/MasterKnowledge/KnowledgeMaster/data/3.jpg", "/Users/zhuzhenwei/Desktop/zzw_code/MasterKnowledge/KnowledgeMaster/data/2025新生手册.pdf")


import subprocess

def send_kg(text, picture_path, file_path):
    # 定义变量
    # curl_url = "https://3bca4fdab4d1.ngrok-free.app/chat_v2"

    curl_url = "http://localhost:8000"
    # 构建 curl 命令
    curl_command = [
        "curl", "-X", "POST", curl_url,
        "-F", f"pdf_path=@{file_path}",
        "-F", f"prompt={text}",
        "-F", f"image_path=@{picture_path}",
        "--connect-timeout", "120",
        "--max-time", "120"
    ]
    print(curl_command)

    # 执行命令并捕获输出
    result = subprocess.run(curl_command, capture_output=True, text=True)

    # 打印命令的返回码、标准输出和错误输出
    print("Return code:", result.returncode)
    print("Standard Output:", result.stdout)
    print("Error Output:", result.stderr)

