"""
로그인 페이지 언어 선택 요소 디버그 스크립트
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


def debug_login_page():
    """로그인 페이지 디버그"""
    logger.info("=== 로그인 페이지 언어 선택 요소 디버그 ===")
    
    config = load_config()
    if not config:
        return False
    
    try:
        # 자동화 인스턴스 생성
        automation = IP168ITSMAutomation(config)
        
        # 웹드라이버 설정
        automation.setup_driver()
        
        # 웹사이트 접속
        if not automation.navigate_to_website():
            logger.error("웹사이트 접속 실패")
            return False
        
        # 페이지 소스 분석
        page_source = automation.driver.page_source
        
        print("\n=== 페이지 제목 ===")
        print(f"제목: {automation.driver.title}")
        
        print("\n=== 모든 select 요소 ===")
        select_elements = automation.driver.find_elements("css selector", "select")
        for i, select in enumerate(select_elements):
            print(f"Select {i+1}:")
            print(f"  - name: {select.get_attribute('name')}")
            print(f"  - id: {select.get_attribute('id')}")
            print(f"  - class: {select.get_attribute('class')}")
            print(f"  - visible: {select.is_displayed()}")
            
            # 옵션들 확인
            try:
                from selenium.webdriver.support.ui import Select
                select_obj = Select(select)
                options = select_obj.options
                print(f"  - 옵션들:")
                for j, option in enumerate(options):
                    print(f"    {j+1}. {option.text} (value: {option.get_attribute('value')})")
            except:
                print(f"  - 옵션 읽기 실패")
        
        print("\n=== 모든 button 요소 ===")
        button_elements = automation.driver.find_elements("css selector", "button")
        for i, button in enumerate(button_elements):
            if button.is_displayed():
                print(f"Button {i+1}:")
                print(f"  - text: {button.text}")
                print(f"  - onclick: {button.get_attribute('onclick')}")
                print(f"  - class: {button.get_attribute('class')}")
                print(f"  - id: {button.get_attribute('id')}")
        
        print("\n=== 모든 a 요소 ===")
        a_elements = automation.driver.find_elements("css selector", "a")
        for i, a in enumerate(a_elements):
            if a.is_displayed():
                print(f"Link {i+1}:")
                print(f"  - text: {a.text}")
                print(f"  - href: {a.get_attribute('href')}")
                print(f"  - onclick: {a.get_attribute('onclick')}")
                print(f"  - class: {a.get_attribute('class')}")
        
        print("\n=== 언어 관련 키워드 검색 ===")
        language_keywords = [
            '한국어', 'Korean', 'ko', 'ko-KR',
            '영어', 'English', 'en', 'en-US',
            'language', 'lang', 'locale',
            '언어', '선택', 'select'
        ]
        
        for keyword in language_keywords:
            if keyword in page_source:
                print(f"✅ '{keyword}' 발견")
                
                # 해당 키워드 주변 텍스트 찾기
                import re
                pattern = f'.{{0,50}}{re.escape(keyword)}.{{0,50}}'
                matches = re.findall(pattern, page_source)
                for match in matches[:3]:  # 처음 3개만 출력
                    print(f"  - {match.strip()}")
        
        print("\n=== JavaScript 코드에서 언어 관련 부분 ===")
        script_elements = automation.driver.find_elements("css selector", "script")
        for i, script in enumerate(script_elements):
            script_content = script.get_attribute('innerHTML')
            if script_content and any(keyword in script_content for keyword in ['lang', 'language', 'ko', 'en']):
                print(f"Script {i+1}에서 언어 관련 코드 발견:")
                lines = script_content.split('\n')
                for line in lines:
                    if any(keyword in line for keyword in ['lang', 'language', 'ko', 'en']):
                        print(f"  {line.strip()}")
        
        # 스크린샷 촬영
        screenshot_path = automation.take_screenshot("debug_login_page.png")
        if screenshot_path:
            print(f"\n스크린샷 저장: {screenshot_path}")
        
        # 사용자 입력 대기
        input("\n엔터 키를 누르면 브라우저가 닫힙니다...")
        automation.cleanup()
        
        return True
        
    except Exception as e:
        logger.error(f"디버그 오류: {e}")
        return False


def main():
    """메인 함수"""
    success = debug_login_page()
    
    if success:
        logger.info("🎉 디버그가 성공적으로 완료되었습니다!")
        return 0
    else:
        logger.error("❌ 디버그가 실패했습니다.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 