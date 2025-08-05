"""
IP 168 ITSM 웹사이트 자동화 실행 스크립트
"""

import yaml
import sys
import argparse
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


def run_automation(credentials=None, take_screenshot=False, keep_browser=True, select_language=True, navigate_to_target=True):
    """자동화 실행"""
    logger.info("IP 168 ITSM 웹사이트 자동화 시작")
    
    config = load_config()
    if not config:
        logger.error("설정 파일을 로드할 수 없습니다")
        return False
    
    try:
        # 자동화 인스턴스 생성
        automation = IP168ITSMAutomation(config)
        
        # 자동화 실행
        success = automation.run_automation(credentials, keep_browser, select_language, navigate_to_target)
        
        if success:
            logger.info("✅ IP 168 ITSM 자동화 성공")
            
            # 스크린샷 촬영 (옵션)
            if take_screenshot:
                screenshot_path = automation.take_screenshot()
                if screenshot_path:
                    logger.info(f"스크린샷 저장: {screenshot_path}")
            
            # 브라우저 유지 시 사용자 입력 대기
            if keep_browser:
                logger.info("브라우저가 열린 상태로 유지됩니다.")
                logger.info("추가 작업을 위해 대기 중... (Ctrl+C로 종료)")
                try:
                    automation.wait_for_user_input()
                except KeyboardInterrupt:
                    logger.info("사용자가 중단했습니다.")
        else:
            logger.error("❌ IP 168 ITSM 자동화 실패")
        
        return success
        
    except Exception as e:
        logger.error(f"자동화 실행 오류: {e}")
        return False


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='IP 168 ITSM 웹사이트 자동화')
    parser.add_argument('--username', '-u', help='사용자명 (기본값: ij_itsmadmin)')
    parser.add_argument('--password', '-p', help='비밀번호 (기본값: 0)')
    parser.add_argument('--screenshot', '-s', action='store_true', help='스크린샷 촬영')
    parser.add_argument('--test', '-t', action='store_true', help='테스트 모드 실행')
    parser.add_argument('--close-browser', '-c', action='store_true', help='자동화 완료 후 브라우저 닫기')
    parser.add_argument('--no-language-select', '-n', action='store_true', help='로그인 페이지 언어 선택 비활성화')
    parser.add_argument('--no-navigate', '-nn', action='store_true', help='목표 페이지 이동 비활성화')
    
    args = parser.parse_args()
    
    # 테스트 모드인 경우
    if args.test:
        logger.info("테스트 모드로 실행합니다")
        from test_automation import main as test_main
        return test_main()
    
    # 사용자 정의 로그인 정보
    credentials = None
    if args.username or args.password:
        credentials = {
            'username': args.username or 'ij_itsmadmin',
            'password': args.password or '0'
        }
        logger.info(f"사용자 정의 로그인 정보 사용: {credentials['username']}")
    
    # 브라우저 유지 여부 결정
    keep_browser = not args.close_browser
    
    # 언어 선택 여부 결정
    select_language = not args.no_language_select
    
    # 목표 페이지 이동 여부 결정
    navigate_to_target = not args.no_navigate
    
    # 자동화 실행
    success = run_automation(credentials, args.screenshot, keep_browser, select_language, navigate_to_target)
    
    if success:
        logger.info("🎉 자동화가 성공적으로 완료되었습니다!")
        return 0
    else:
        logger.error("❌ 자동화가 실패했습니다.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 