import os
import json

# JSON 파일이 있는 폴더 경로
folder_path = ""

# 새로운 JSON 기본 포맷
DEFAULT_FORMAT = {}

def merge_json(existing_data, default_format):
    if isinstance(default_format, dict):
        # 기존 데이터가 딕셔너리라면, 키별로 처리
        merged = {}
        for key, default_value in default_format.items():
            if key in existing_data:
                merged[key] = merge_json(existing_data[key], default_value)  # 재귀적으로 병합
            else:
                merged[key] = default_value  # 기존 데이터에 없으면 기본값 사용
        
        # 기존 데이터 중 새로운 포맷에 없는 키들도 유지
        for key in existing_data:
            if key not in merged:
                merged[key] = existing_data[key]
        
        return merged
    else:
        # 기본값이 단순 값이라면 기존 데이터 유지
        return existing_data if existing_data else default_format

# 폴더 내 JSON 파일 처리
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)

        # JSON 파일 읽기
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ JSON 파일 오류: {filename}")
                continue

        # 새로운 포맷과 병합
        new_data = merge_json(data, DEFAULT_FORMAT)

        # 변환된 JSON을 같은 파일에 덮어쓰기
        with open(file_path, "w") as f:
            json.dump(new_data, f, indent=2)

        print(f"✅ 변환 완료: {filename}")
