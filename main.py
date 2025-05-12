import os
import asyncio
import json
from dotenv import load_dotenv
import classification
import search  

# 환경 변수 로드
load_dotenv()

async def run_pipeline():
    print("=== 이미지 위치 식별 파이프라인 시작 ===")

    # 1. 이미지 분류 (사람/비사람) - 선택적
    print("\n=== 1단계: 이미지 분류 ===")
    classification_results = classification.main()
    if not classification_results:
        print("이미지 분류에 실패했습니다. 모든 이미지를 분석합니다.")
        classification_results = {}

    # 2. 멀티모달 AI를 사용한 이미지 위치 분석
    print("\n=== 2단계: 이미지 위치 분석 ===")
    location_results = await search.main()
    if not location_results:
        print("이미지 위치 분석에 실패했습니다. 프로세스를 종료합니다.")
        return

    print("\n=== 이미지 위치 식별 파이프라인 완료 ===")

    # 최종 결과 출력
    try:
        print("\n=== 최종 위치 식별 결과 ===")
        for img_idx, location in location_results.items():
            img_idx_str = str(img_idx)
            is_person = (classification_results.get(img_idx_str, False) or 
                         classification_results.get(int(img_idx_str), False) or
                         location.lower() == "person")
            status = "사람 이미지" if is_person else "풍경 이미지"
            print(f"이미지 {img_idx}: {location} ({status})")
    except Exception as e:
        print(f"최종 결과 출력 중 오류 발생: {e}")

if __name__ == "__main__":
    asyncio.run(run_pipeline())