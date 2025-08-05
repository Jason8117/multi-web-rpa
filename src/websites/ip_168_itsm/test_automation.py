"""
IP 168 ITSM 웹사이트 자동화 테스트 스크립트
"""

import yaml
import sys
import os
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.websites.ip_168_itsm.automation import IP168ITSMAutomation
from loguru import logger


def load_config():
    """설정 파일 로드"""
    config_path = Path(__file__).parent / "config.yaml"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        logger.info("설정 파일 로드 완료")
        return config
    except Exception as e:
        logger.error(f"설정 파일 로드 오류: {e}")
        return None


def test_website_access():
    """웹사이트 접속 테스트"""
    logger.info("=== IP 168 ITSM 웹사이트 접속 테스트 ===")
    
    config = load_config()
    if not config:
        return False
    
    try:
        automation = IP168ITSMAutomation(config)
        
        # 웹드라이버 설정
        automation.setup_driver()
        
        # 웹사이트 접속
        success = automation.navigate_to_website()
        
        if success:
            logger.info("✅ 웹사이트 접속 테스트 성공")
            
            # 스크린샷 촬영
            screenshot_path = automation.take_screenshot("test_website_access.png")
            if screenshot_path:
                logger.info(f"스크린샷 저장: {screenshot_path}")
        else:
            logger.error("❌ 웹사이트 접속 테스트 실패")
        
        return success
        
    except Exception as e:
        logger.error(f"웹사이트 접속 테스트 오류: {e}")
        return False


def test_login():
    """로그인 테스트"""
    logger.info("=== IP 168 ITSM 로그인 테스트 ===")
    
    config = load_config()
    if not config:
        return False
    
    try:
        automation = IP168ITSMAutomation(config)
        
        # 전체 자동화 실행 (웹사이트 접속 + 로그인)
        success = automation.run_automation()
        
        if success:
            logger.info("✅ 로그인 테스트 성공")
        else:
            logger.error("❌ 로그인 테스트 실패")
        
        return success
        
    except Exception as e:
        logger.error(f"로그인 테스트 오류: {e}")
        return False


def test_custom_credentials():
    """사용자 정의 로그인 정보 테스트"""
    logger.info("=== 사용자 정의 로그인 정보 테스트 ===")
    
    config = load_config()
    if not config:
        return False
    
    # 사용자 정의 로그인 정보
    custom_credentials = {
        'username': 'ij_itsmadmin',
        'password': '0'
    }
    
    try:
        automation = IP168ITSMAutomation(config)
        
        # 웹드라이버 설정
        automation.setup_driver()
        
        # 웹사이트 접속
        if not automation.navigate_to_website():
            logger.error("웹사이트 접속 실패")
            return False
        
        # 사용자 정의 로그인 정보로 로그인
        success = automation.login(custom_credentials)
        
        if success:
            logger.info("✅ 사용자 정의 로그인 정보 테스트 성공")
            
            # 스크린샷 촬영
            screenshot_path = automation.take_screenshot("test_custom_login.png")
            if screenshot_path:
                logger.info(f"스크린샷 저장: {screenshot_path}")
        else:
            logger.error("❌ 사용자 정의 로그인 정보 테스트 실패")
        
        return success
        
    except Exception as e:
        logger.error(f"사용자 정의 로그인 정보 테스트 오류: {e}")
        return False


def main():
    """메인 테스트 함수"""
    logger.info("IP 168 ITSM 웹사이트 자동화 테스트 시작")
    
    # 테스트 결과 저장
    test_results = {}
    
    # 1. 웹사이트 접속 테스트
    test_results['website_access'] = test_website_access()
    
    # 2. 로그인 테스트
    test_results['login'] = test_login()
    
    # 3. 사용자 정의 로그인 정보 테스트
    test_results['custom_credentials'] = test_custom_credentials()
    
    # 테스트 결과 요약
    logger.info("=== 테스트 결과 요약 ===")
    for test_name, result in test_results.items():
        status = "✅ 성공" if result else "❌ 실패"
        logger.info(f"{test_name}: {status}")
    
    # 전체 성공 여부
    all_passed = all(test_results.values())
    if all_passed:
        logger.info("🎉 모든 테스트가 성공했습니다!")
    else:
        logger.warning("⚠️ 일부 테스트가 실패했습니다.")
    
    return all_passed


if __name__ == "__main__":
    main() 