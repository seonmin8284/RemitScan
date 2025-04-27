
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import joblib

# (1) 샘플 데이터 생성
# 매우 단순화된 룰 기반 데이터 (진짜 시스템이면 더 풍부하게 해야함)
X = np.array([
    [1, 0, 0, 0, 0, 0],  # 차단된 IP → 위험
    [0, 1, 0, 0, 0, 0],  # 블랙리스트 디바이스 → 위험
    [0, 0, 1, 0, 0, 0],  # 고위험 국가 → 위험
    [0, 0, 0, 1, 0, 0],  # 제재 전화번호 → 위험
    [0, 0, 0, 0, 1, 0],  # VPN → 위험
    [0, 0, 0, 0, 0, 1],  # 루팅 → 위험
    [0, 0, 0, 0, 0, 0],  # 다 없음 → 정상
])

y = np.array([
    1, 1, 1, 1, 1, 1, 0
])

# (2) Decision Tree 훈련
model = DecisionTreeClassifier()
model.fit(X, y)

# (3) 저장 (옵션)
joblib.dump(model, "rule_model.pkl")

# (4) ONNX 변환
initial_type = [('input', FloatTensorType([None, 6]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)

with open("rule_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

print("✅ 룰 기반 모델이 ONNX로 변환되었습니다!")
