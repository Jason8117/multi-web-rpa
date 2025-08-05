#!/usr/bin/env python3
"""
회원등록 페이지의 버튼들을 분석하는 디버그 스크립트
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트 경로를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.config_manager import ConfigManager
from src.websites.ip_168_itsm.automation import IP168ITSMAutomation
from selenium.webdriver.common.by import By
from loguru import logger

def debug_buttons():
    """현재 페이지의 모든 버튼을 분석"""
    try:
        # 설정 로드
        config_manager = ConfigManager()
        config_manager.load_configs()
        website_config = config_manager.get_website_config('ip_168_itsm')
        
        # 자동화 객체 생성
        automation = IP168ITSMAutomation(website_config)
        
        # 웹드라이버 설정
        automation.setup_driver()
        
        # 웹사이트 접속 및 로그인
        automation.navigate_to_website()
        automation.select_language_on_login_page('한국어')
        automation.login()
        
        # 회원등록 페이지로 이동
        automation.navigate_to_registration_page_direct()
        
        # 현재 페이지의 모든 버튼 찾기
        logger.info("=== 현재 페이지의 모든 버튼 분석 ===")
        
        # 모든 button 요소 찾기
        buttons = automation.driver.find_elements(By.TAG_NAME, "button")
        logger.info(f"총 {len(buttons)}개의 button 요소 발견")
        
        for i, button in enumerate(buttons):
            try:
                text = button.text.strip()
                tag_name = button.tag_name
                button_type = button.get_attribute('type')
                button_class = button.get_attribute('class')
                button_id = button.get_attribute('id')
                button_name = button.get_attribute('name')
                is_displayed = button.is_displayed()
                is_enabled = button.is_enabled()
                
                logger.info(f"버튼 {i+1}:")
                logger.info(f"  텍스트: '{text}'")
                logger.info(f"  태그: {tag_name}")
                logger.info(f"  타입: {button_type}")
                logger.info(f"  클래스: {button_class}")
                logger.info(f"  ID: {button_id}")
                logger.info(f"  이름: {button_name}")
                logger.info(f"  표시됨: {is_displayed}")
                logger.info(f"  활성화됨: {is_enabled}")
                logger.info("  ---")
                
            except Exception as e:
                logger.error(f"버튼 {i+1} 분석 오류: {e}")
        
        # 모든 input 요소도 확인
        inputs = automation.driver.find_elements(By.TAG_NAME, "input")
        logger.info(f"\n=== 현재 페이지의 모든 input 요소 분석 ===")
        logger.info(f"총 {len(inputs)}개의 input 요소 발견")
        
        for i, input_elem in enumerate(inputs):
            try:
                input_type = input_elem.get_attribute('type')
                input_value = input_elem.get_attribute('value')
                input_class = input_elem.get_attribute('class')
                input_id = input_elem.get_attribute('id')
                input_name = input_elem.get_attribute('name')
                is_displayed = input_elem.is_displayed()
                
                # submit 타입만 상세 분석
                if input_type == 'submit':
                    logger.info(f"Submit Input {i+1}:")
                    logger.info(f"  타입: {input_type}")
                    logger.info(f"  값: '{input_value}'")
                    logger.info(f"  클래스: {input_class}")
                    logger.info(f"  ID: {input_id}")
                    logger.info(f"  이름: {input_name}")
                    logger.info(f"  표시됨: {is_displayed}")
                    logger.info("  ---")
                
            except Exception as e:
                logger.error(f"Input {i+1} 분석 오류: {e}")
        
        # 브라우저 유지
        input("분석 완료. Enter를 눌러 브라우저를 닫으세요...")
        automation.cleanup()
        
    except Exception as e:
        logger.error(f"디버그 스크립트 오류: {e}")

if __name__ == "__main__":
    debug_buttons() 