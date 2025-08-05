"""
IP 168 ITSM 고급 자동화 스크립트
로그인 후 추가 작업을 수행하는 예제
"""

import yaml
import sys
import time
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


def example_form_filling():
    """폼 입력 예제"""
    logger.info("=== 폼 입력 예제 ===")
    
    config = load_config()
    if not config:
        return False
    
    try:
        # 자동화 인스턴스 생성
        automation = IP168ITSMAutomation(config)
        
        # 1. 로그인 (브라우저 유지)
        success = automation.run_automation(keep_browser=True)
        if not success:
            logger.error("로그인 실패")
            return False
        
        # 2. 현재 페이지 정보 확인
        page_info = automation.get_current_page_info()
        logger.info(f"현재 페이지: {page_info}")
        
        # 3. 예제 폼 데이터
        form_data = {
            'title': '테스트 제목',
            'description': '테스트 설명입니다.',
            'assignee': '테스트 담당자',
            'due_date': '2024-12-31'
        }
        
        # 4. 폼 데이터 입력
        if automation.fill_form_data(form_data):
            logger.info("✅ 폼 데이터 입력 성공")
        else:
            logger.warning("⚠️ 폼 데이터 입력 실패")
        
        # 5. 버튼 클릭 예제
        if automation.click_button('save'):
            logger.info("✅ 저장 버튼 클릭 성공")
        else:
            logger.warning("⚠️ 저장 버튼 클릭 실패")
        
        # 6. 셀렉트 옵션 선택 예제
        if automation.select_option('priority', 'high'):
            logger.info("✅ 우선순위 선택 성공")
        else:
            logger.warning("⚠️ 우선순위 선택 실패")
        
        # 7. 스크린샷 촬영
        screenshot_path = automation.take_screenshot("advanced_automation.png")
        if screenshot_path:
            logger.info(f"스크린샷 저장: {screenshot_path}")
        
        # 8. 사용자 입력 대기
        logger.info("추가 작업을 위해 브라우저가 열린 상태로 유지됩니다.")
        automation.wait_for_user_input()
        
        return True
        
    except Exception as e:
        logger.error(f"고급 자동화 오류: {e}")
        return False


def example_menu_navigation():
    """메뉴 네비게이션 예제"""
    logger.info("=== 메뉴 네비게이션 예제 ===")
    
    config = load_config()
    if not config:
        return False
    
    try:
        # 자동화 인스턴스 생성
        automation = IP168ITSMAutomation(config)
        
        # 1. 로그인
        success = automation.run_automation(keep_browser=True)
        if not success:
            logger.error("로그인 실패")
            return False
        
        # 2. 메뉴 네비게이션 예제
        menu_paths = [
            "서비스 데스크 > 티켓 관리",
            "서비스 데스크 > 티켓 생성",
            "관리 > 사용자 관리"
        ]
        
        for menu_path in menu_paths:
            if automation.navigate_to_menu(menu_path):
                logger.info(f"✅ 메뉴 이동 성공: {menu_path}")
                time.sleep(2)  # 페이지 로딩 대기
            else:
                logger.warning(f"⚠️ 메뉴 이동 실패: {menu_path}")
        
        # 3. 사용자 입력 대기
        automation.wait_for_user_input()
        
        return True
        
    except Exception as e:
        logger.error(f"메뉴 네비게이션 오류: {e}")
        return False


def interactive_automation():
    """대화형 자동화"""
    logger.info("=== 대화형 자동화 ===")
    
    config = load_config()
    if not config:
        return False
    
    try:
        # 자동화 인스턴스 생성
        automation = IP168ITSMAutomation(config)
        
        # 1. 로그인
        success = automation.run_automation(keep_browser=True)
        if not success:
            logger.error("로그인 실패")
            return False
        
        # 2. 대화형 작업
        while True:
            print("\n=== 사용 가능한 작업 ===")
            print("1. 현재 페이지 정보 확인")
            print("2. 스크린샷 촬영")
            print("3. 폼 데이터 입력")
            print("4. 버튼 클릭")
            print("5. 셀렉트 옵션 선택")
            print("6. 로그인 페이지 언어 선택 요소 분석")
            print("7. 로그인 페이지에서 한국어 선택")
            print("8. 목표 페이지로 이동 (시스템관리 > 회원관리 > 회원등록(메타넷))")
            print("9. 회원등록 폼 분석")
            print("10. 회원등록 페이지로 직접 이동")
            print("11. 성명 필드 테스트")
            print("12. 엑셀에서 사용자 회원등록 (1명)")
            print("13. 엑셀에서 모든 사용자 회원등록")
            print("14. 종료")
            
            choice = input("\n작업을 선택하세요 (1-14): ").strip()
            
            if choice == '1':
                page_info = automation.get_current_page_info()
                print(f"현재 페이지 정보: {page_info}")
                
            elif choice == '2':
                filename = input("스크린샷 파일명 (기본값: screenshot.png): ").strip()
                if not filename:
                    filename = "screenshot.png"
                screenshot_path = automation.take_screenshot(filename)
                if screenshot_path:
                    print(f"스크린샷 저장: {screenshot_path}")
                    
            elif choice == '3':
                field_name = input("필드 이름: ").strip()
                value = input("입력할 값: ").strip()
                if automation.fill_field(field_name, value):
                    print(f"✅ 필드 '{field_name}'에 값 '{value}' 입력 성공")
                else:
                    print(f"❌ 필드 '{field_name}' 입력 실패")
                    
            elif choice == '4':
                button_name = input("버튼 이름: ").strip()
                if automation.click_button(button_name):
                    print(f"✅ 버튼 '{button_name}' 클릭 성공")
                else:
                    print(f"❌ 버튼 '{button_name}' 클릭 실패")
                    
            elif choice == '5':
                select_name = input("셀렉트 이름: ").strip()
                option_value = input("옵션 값: ").strip()
                if automation.select_option(select_name, option_value):
                    print(f"✅ 셀렉트 '{select_name}'에서 옵션 '{option_value}' 선택 성공")
                else:
                    print(f"❌ 셀렉트 '{select_name}' 옵션 선택 실패")
                    
            elif choice == '6':
                analysis = automation.analyze_login_page_language_selector()
                if analysis:
                    print("✅ 언어 선택 요소 분석 완료")
                    print(f"발견된 요소 수: {len(analysis.get('found_elements', []))}")
                    print(f"언어 옵션: {analysis.get('language_options', [])}")
                    print(f"추천 선택자: {analysis.get('recommended_selector', '없음')}")
                else:
                    print("❌ 언어 선택 요소 분석 실패")
                    
            elif choice == '7':
                if automation.select_language_on_login_page('한국어'):
                    print("✅ 로그인 페이지에서 한국어 선택 성공")
                else:
                    print("❌ 로그인 페이지에서 한국어 선택 실패")
                
            elif choice == '8':
                if automation.navigate_to_target_page():
                    print("✅ 목표 페이지로 이동 성공")
                else:
                    print("❌ 목표 페이지로 이동 실패")
                
            elif choice == '9':
                analysis = automation.analyze_registration_form()
                if analysis:
                    print("✅ 회원등록 폼 분석 완료")
                    print(f"발견된 필드 수: {len(analysis.get('found_fields', []))}")
                    print(f"발견된 버튼 수: {len(analysis.get('found_buttons', []))}")
                else:
                    print("❌ 회원등록 폼 분석 실패")
                    
            elif choice == '10':
                user_index = input("사용자 인덱스 (0부터 시작): ").strip()
                try:
                    user_index = int(user_index)
                    if automation.register_user_from_excel(user_index):
                        print("✅ 사용자 회원등록 성공")
                    else:
                        print("❌ 사용자 회원등록 실패")
                except ValueError:
                    print("❌ 잘못된 인덱스입니다. 숫자를 입력해주세요.")
                    
            elif choice == '10':
                if automation.navigate_to_registration_page_direct():
                    print("✅ 회원등록 페이지로 직접 이동 성공")
                else:
                    print("❌ 회원등록 페이지로 직접 이동 실패")
                    
            elif choice == '11':
                test_value = input("테스트할 성명 값 (기본값: 테스트성명): ").strip()
                if not test_value:
                    test_value = "테스트성명"
                if automation.test_name_field(test_value):
                    print("✅ 성명 필드 테스트 성공")
                else:
                    print("❌ 성명 필드 테스트 실패")
                    
            elif choice == '12':
                user_index = input("사용자 인덱스 (0부터 시작): ").strip()
                try:
                    user_index = int(user_index)
                    if automation.register_user_from_excel(user_index):
                        print("✅ 사용자 회원등록 성공")
                    else:
                        print("❌ 사용자 회원등록 실패")
                except ValueError:
                    print("❌ 잘못된 인덱스입니다. 숫자를 입력해주세요.")
                    
            elif choice == '13':
                result = automation.register_all_users_from_excel()
                if result.get('success'):
                    results = result.get('results', {})
                    print(f"✅ 전체 회원등록 완료")
                    print(f"총 사용자: {results.get('total_users', 0)}명")
                    print(f"성공: {results.get('success_count', 0)}명")
                    print(f"실패: {results.get('failed_count', 0)}명")
                else:
                    print(f"❌ 전체 회원등록 실패: {result.get('message', '알 수 없는 오류')}")
                
            elif choice == '14':
                print("자동화를 종료합니다.")
                break
                
            else:
                print("잘못된 선택입니다. 1-14 중에서 선택해주세요.")
        
        return True
        
    except Exception as e:
        logger.error(f"대화형 자동화 오류: {e}")
        return False


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='IP 168 ITSM 고급 자동화')
    parser.add_argument('--mode', '-m', choices=['form', 'menu', 'interactive'], 
                       default='interactive', help='자동화 모드')
    
    args = parser.parse_args()
    
    if args.mode == 'form':
        success = example_form_filling()
    elif args.mode == 'menu':
        success = example_menu_navigation()
    else:
        success = interactive_automation()
    
    if success:
        logger.info("🎉 고급 자동화가 성공적으로 완료되었습니다!")
        return 0
    else:
        logger.error("❌ 고급 자동화가 실패했습니다.")
        return 1


if __name__ == "__main__":
    import argparse
    exit_code = main()
    sys.exit(exit_code) 