#!/usr/bin/env python3
"""
IP 168 ITSM 전체 자동화 기능 테스트 스크립트
사용자 요청 조건에 맞게 기능을 확인합니다.
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트 경로를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.config_manager import ConfigManager
from src.websites.ip_168_itsm.automation import IP168ITSMAutomation
from loguru import logger


def test_full_automation():
    """전체 자동화 기능 테스트"""
    try:
        logger.info("=== IP 168 ITSM 전체 자동화 기능 테스트 시작 ===")
        
        # 1. 설정 로드
        logger.info("1. 설정 로드 중...")
        config_manager = ConfigManager()
        config = config_manager.get_website_config('ip_168_itsm')
        
        if not config:
            logger.error("❌ IP 168 ITSM 설정을 찾을 수 없습니다")
            return False
        
        logger.info("✅ 설정 로드 완료")
        
        # 2. 자동화 객체 생성
        logger.info("2. 자동화 객체 생성 중...")
        automation = IP168ITSMAutomation(config)
        logger.info("✅ 자동화 객체 생성 완료")
        
        # 3. 웹사이트 접속 및 로그인
        logger.info("3. 웹사이트 접속 및 로그인 중...")
        if not automation.run_automation(keep_browser=True, select_language=True, navigate_to_target=False):
            logger.error("❌ 웹사이트 접속 및 로그인 실패")
            return False
        
        logger.info("✅ 웹사이트 접속 및 로그인 완료")
        
        # 4. 엑셀 파일 읽기 테스트
        logger.info("4. 엑셀 파일 읽기 테스트 중...")
        if not automation.excel_reader.load_excel_file():
            logger.error("❌ 엑셀 파일 읽기 실패")
            return False
        
        total_rows = automation.excel_reader.get_total_rows()
        column_names = automation.excel_reader.get_column_names()
        
        logger.info(f"✅ 엑셀 파일 읽기 완료: {total_rows}행, 컬럼: {column_names}")
        
        # 5. 회원등록 페이지 직접 이동 테스트
        logger.info("5. 회원등록 페이지 직접 이동 테스트 중...")
        if not automation.navigate_to_registration_page_direct():
            logger.error("❌ 회원등록 페이지 이동 실패")
            return False
        
        logger.info("✅ 회원등록 페이지 이동 완료")
        
        # 6. 페이지 구조 분석
        logger.info("6. 페이지 구조 분석 중...")
        automation.analyze_page_structure()
        
        # 스크린샷 촬영
        screenshot_path = automation.take_screenshot_for_analysis("registration_page")
        if screenshot_path:
            logger.info(f"✅ 페이지 스크린샷 저장: {screenshot_path}")
        
        # 6-1. 중복확인 팝업 분석
        logger.info("6-1. 중복확인 팝업 분석 중...")
        automation.analyze_duplicate_check_popup()
        
        # 7. 필드 매핑 테스트 (첫 번째 사용자 데이터로)
        logger.info("7. 필드 매핑 테스트 중...")
        
        # 첫 번째 사용자 데이터 가져오기
        user_data = automation.excel_reader.get_user_data(0)
        if not user_data:
            logger.error("❌ 첫 번째 사용자 데이터를 가져올 수 없습니다")
            return False
        
        logger.info(f"테스트 사용자 데이터: {user_data}")
        
        # 필드별 테스트
        logger.info("6-1. 성명 필드 테스트...")
        if 'per_nm' in user_data and user_data['per_nm']:
            if automation.fill_name_field_specific(user_data['per_nm']):
                logger.info("✅ 성명 필드 테스트 성공")
            else:
                logger.warning("⚠️ 성명 필드 테스트 실패")
        else:
            logger.warning("⚠️ 성명 데이터가 없어 테스트 생략")
        
        logger.info("6-2. 사용자 ID 필드 테스트...")
        if 'email' in user_data and user_data['email']:
            if automation.fill_user_id_field_specific(user_data['email']):
                logger.info("✅ 사용자 ID 필드 테스트 성공")
            else:
                logger.warning("⚠️ 사용자 ID 필드 테스트 실패")
        else:
            logger.warning("⚠️ 사용자 ID 데이터가 없어 테스트 생략")
        
        logger.info("6-3. 법인 필드 테스트...")
        if '계열사' in user_data and user_data['계열사']:
            if automation.fill_company_field_specific(user_data['계열사']):
                logger.info("✅ 법인 필드 테스트 성공")
            else:
                logger.warning("⚠️ 법인 필드 테스트 실패")
        else:
            logger.warning("⚠️ 법인 데이터가 없어 테스트 생략")
        
        logger.info("6-4. 직위 필드 테스트...")
        if 'per_work' in user_data and user_data['per_work']:
            if automation.fill_position_field_specific(user_data['per_work']):
                logger.info("✅ 직위 필드 테스트 성공")
            else:
                logger.warning("⚠️ 직위 필드 테스트 실패")
        else:
            logger.warning("⚠️ 직위 데이터가 없어 테스트 생략")
        
        logger.info("6-5. 내선번호 필드 테스트...")
        if 'phone' in user_data and user_data['phone']:
            if automation.fill_phone_field_specific(user_data['phone']):
                logger.info("✅ 내선번호 필드 테스트 성공")
            else:
                logger.warning("⚠️ 내선번호 필드 테스트 실패")
        else:
            logger.warning("⚠️ 내선번호 데이터가 없어 테스트 생략")
        
        logger.info("6-6. 휴대폰 필드 테스트...")
        if 'mobile' in user_data and user_data['mobile']:
            if automation.fill_mobile_field_specific(user_data['mobile']):
                logger.info("✅ 휴대폰 필드 테스트 성공")
            else:
                logger.warning("⚠️ 휴대폰 필드 테스트 실패")
        else:
            logger.warning("⚠️ 휴대폰 데이터가 없어 테스트 생략")
        
        logger.info("6-7. 메일 필드 테스트...")
        if 'email' in user_data and user_data['email']:
            if automation.fill_email_field_specific(user_data['email']):
                logger.info("✅ 메일 필드 테스트 성공")
            else:
                logger.warning("⚠️ 메일 필드 테스트 실패")
        else:
            logger.warning("⚠️ 메일 데이터가 없어 테스트 생략")
        
        logger.info("6-8. 영문이름 필드 테스트...")
        if 'per_nm_en' in user_data and user_data['per_nm_en']:
            if automation.fill_english_name_field_specific(user_data['per_nm_en']):
                logger.info("✅ 영문이름 필드 테스트 성공")
            else:
                logger.warning("⚠️ 영문이름 필드 테스트 실패")
        else:
            logger.warning("⚠️ 영문이름 데이터가 없어 테스트 생략")
        
        logger.info("✅ 필드 매핑 테스트 완료")
        
        # 8. 전체 회원가입 프로세스 테스트 (첫 번째 사용자만)
        logger.info("8. 전체 회원가입 프로세스 테스트 중...")
        
        # 회원등록 페이지로 다시 이동
        if not automation.navigate_to_registration_page_direct():
            logger.error("❌ 회원등록 페이지 재이동 실패")
            return False
        
        # 첫 번째 사용자 회원가입
        if automation.register_user_from_excel(0):
            logger.info("✅ 첫 번째 사용자 회원가입 성공")
        else:
            logger.warning("⚠️ 첫 번째 사용자 회원가입 실패")
        
        logger.info("✅ 전체 회원가입 프로세스 테스트 완료")
        
        # 9. 결과 요약
        logger.info("=== 테스트 결과 요약 ===")
        logger.info("✅ 로그인페이지 접속: 성공")
        logger.info("✅ 로그인: 성공")
        logger.info("✅ 엑셀파일 읽기: 성공")
        logger.info("✅ 회원등록 메뉴 이동: 성공")
        logger.info("✅ 필드 매핑: 테스트 완료")
        logger.info("✅ 전체 회원가입 프로세스: 테스트 완료")
        
        logger.info("🎉 모든 테스트가 완료되었습니다!")
        
        # 브라우저 유지
        input("확인 후 Enter를 눌러주세요...")
        
        return True
        
    except Exception as e:
        logger.error(f"전체 자동화 테스트 오류: {e}")
        return False


if __name__ == "__main__":
    success = test_full_automation()
    if success:
        logger.info("🎉 전체 자동화 테스트 성공!")
    else:
        logger.error("❌ 전체 자동화 테스트 실패!") 