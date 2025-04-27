import requests

# Triton 서버 주소
url = "http://localhost:8000/v2/models/rule_model/infer"
headers = {"Content-Type": "application/json"}

# 예시 입력 데이터
payload = {
    "inputs": [
        {
            "name": "input",
            "shape": [1, 6],
            "datatype": "FP32",
            "data": [[0.0, 1.0, 0.0, 0.0, 1.0, 0.0]]  # 예시 입력값 (6개 feature)
        }
    ]
}

# 요청 보내기
response = requests.post(url, headers=headers, json=payload)

# 결과 출력
if response.status_code == 200:
    result = response.json()
    print("✅ Inference 결과:", result["outputs"][0]["data"])
else:
    print("❌ Inference 실패:", response.status_code, response.text)
