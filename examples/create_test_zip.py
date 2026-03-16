#!/usr/bin/env python3
"""
테스트용 학생 제출물 ZIP 파일 생성 스크립트

이 스크립트는 샘플 학생 노트북들을 ZIP으로 압축합니다.
생성된 students.zip을 업로드 페이지에서 업로드하면 됩니다.
"""

import zipfile
import os
from pathlib import Path

def create_test_zip():
    script_dir = Path(__file__).parent

    # 생성할 파일명
    zip_name = script_dir / "students.zip"

    # 포함할 파일들
    files_to_zip = [
        script_dir / "20210001_홍길동.ipynb",
        script_dir / "20210002_김영희.ipynb",
    ]

    # ZIP 파일 생성
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if file.exists():
                zipf.write(file, arcname=file.name)
                print(f"✓ {file.name} 추가됨")
            else:
                print(f"✗ {file.name} 찾을 수 없음")

    print(f"\n✅ {zip_name.name} 생성 완료!")
    print(f"   위치: {zip_name}")
    print(f"   크기: {zip_name.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    create_test_zip()
