"""
엑셀 파일 테스트 스크립트
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.websites.ip_168_itsm.excel_reader import ITSMExcelReader
from loguru import logger


def test_excel_file():
    """엑셀 파일 테스트"""
    try:
        logger.info("=== 엑셀 파일 테스트 시작 ===")
        
        # 더미 설정 (실제로는 사용되지 않음)
        config = {}
        
        # 엑셀 리더 생성
        excel_reader = ITSMExcelReader(config)
        
        # 엑셀 파일 로드
        if excel_reader.load_excel_file():
            logger.info("✅ 엑셀 파일 로드 성공")
            
            # 데이터 정보 출력
            total_rows = excel_reader.get_total_rows()
            columns = excel_reader.get_column_names()
            
            logger.info(f"총 행 수: {total_rows}")
            logger.info(f"컬럼 목록: {columns}")
            
            # 데이터 미리보기
            excel_reader.preview_data(3)
            
            # 첫 번째 사용자 데이터 테스트
            if total_rows > 0:
                user_data = excel_reader.get_user_data(0)
                if user_data:
                    logger.info(f"✅ 첫 번째 사용자 데이터: {user_data}")
                else:
                    logger.warning("⚠️ 첫 번째 사용자 데이터 로드 실패")
            
            # 두 번째 사용자 데이터 테스트 (있는 경우)
            if total_rows > 1:
                user_data2 = excel_reader.get_user_data(1)
                if user_data2:
                    logger.info(f"✅ 두 번째 사용자 데이터: {user_data2}")
                else:
                    logger.warning("⚠️ 두 번째 사용자 데이터 로드 실패")
            
            logger.info("=== 엑셀 파일 테스트 완료 ===")
            return True
            
        else:
            logger.error("❌ 엑셀 파일 로드 실패")
            return False
            
    except Exception as e:
        logger.error(f"엑셀 파일 테스트 오류: {e}")
        return False


if __name__ == "__main__":
    success = test_excel_file()
    if success:
        logger.info("🎉 엑셀 파일 테스트 성공!")
    else:
        logger.error("❌ 엑셀 파일 테스트 실패!") 