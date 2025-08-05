#!/usr/bin/env python3
"""
현재 페이지의 메뉴 구조를 분석하는 스크립트
"""

import sys
from pathlib import Path

# 프로젝트 루트 경로를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.config_manager import ConfigManager
from src.websites.ip_168_itsm.automation import IP168ITSMAutomation
from loguru import logger


def analyze_current_page():
    """현재 페이지의 메뉴 구조 분석"""
    try:
        logger.info("=== 현재 페이지 메뉴 구조 분석 시작 ===")
        
        # 설정 로드
        config_manager = ConfigManager()
        config = config_manager.get_website_config('ip_168_itsm')
        
        if not config:
            logger.error("IP 168 ITSM 설정을 찾을 수 없습니다")
            return False
        
        # 자동화 객체 생성
        automation = IP168ITSMAutomation(config)
        
        # 웹사이트 접속 및 로그인
        if not automation.run_automation(keep_browser=True, select_language=True, navigate_to_target=False):
            logger.error("웹사이트 접속 및 로그인 실패")
            return False
        
        # 현재 페이지 정보 확인
        current_url = automation.driver.current_url
        current_title = automation.driver.title
        logger.info(f"현재 URL: {current_url}")
        logger.info(f"현재 페이지 제목: {current_title}")
        
        # 페이지 소스에서 메뉴 관련 요소 찾기
        logger.info("=== 메뉴 관련 요소 분석 ===")
        
        # 시스템관리 관련 메뉴 찾기
        system_management_keywords = ['시스템관리', '시스템', '관리', 'System', 'Management']
        for keyword in system_management_keywords:
            try:
                elements = automation.driver.find_elements_by_xpath(f"//*[contains(text(), '{keyword}')]")
                if elements:
                    logger.info(f"'{keyword}' 관련 요소 발견: {len(elements)}개")
                    for i, element in enumerate(elements[:5]):  # 최대 5개만 표시
                        try:
                            logger.info(f"  {i+1}. 태그: {element.tag_name}, 텍스트: '{element.text}', 클래스: '{element.get_attribute('class')}'")
                        except:
                            continue
            except:
                continue
        
        # 회원관리 관련 메뉴 찾기
        member_management_keywords = ['회원관리', '회원', 'Member', 'User']
        for keyword in member_management_keywords:
            try:
                elements = automation.driver.find_elements_by_xpath(f"//*[contains(text(), '{keyword}')]")
                if elements:
                    logger.info(f"'{keyword}' 관련 요소 발견: {len(elements)}개")
                    for i, element in enumerate(elements[:5]):
                        try:
                            logger.info(f"  {i+1}. 태그: {element.tag_name}, 텍스트: '{element.text}', 클래스: '{element.get_attribute('class')}'")
                        except:
                            continue
            except:
                continue
        
        # 회원등록 관련 메뉴 찾기
        registration_keywords = ['회원등록', '등록', 'Registration', 'Register']
        for keyword in registration_keywords:
            try:
                elements = automation.driver.find_elements_by_xpath(f"//*[contains(text(), '{keyword}')]")
                if elements:
                    logger.info(f"'{keyword}' 관련 요소 발견: {len(elements)}개")
                    for i, element in enumerate(elements[:5]):
                        try:
                            logger.info(f"  {i+1}. 태그: {element.tag_name}, 텍스트: '{element.text}', 클래스: '{element.get_attribute('class')}'")
                        except:
                            continue
            except:
                continue
        
        # 메타넷 관련 메뉴 찾기
        metanet_keywords = ['메타넷', 'MetaNet', 'Meta']
        for keyword in metanet_keywords:
            try:
                elements = automation.driver.find_elements_by_xpath(f"//*[contains(text(), '{keyword}')]")
                if elements:
                    logger.info(f"'{keyword}' 관련 요소 발견: {len(elements)}개")
                    for i, element in enumerate(elements[:5]):
                        try:
                            logger.info(f"  {i+1}. 태그: {element.tag_name}, 텍스트: '{element.text}', 클래스: '{element.get_attribute('class')}'")
                        except:
                            continue
            except:
                continue
        
        # 모든 클릭 가능한 요소 찾기
        logger.info("=== 클릭 가능한 요소들 ===")
        clickable_selectors = [
            "button",
            "a",
            "input[type='button']",
            "input[type='submit']",
            "[role='button']",
            "[onclick]"
        ]
        
        for selector in clickable_selectors:
            try:
                elements = automation.driver.find_elements_by_css_selector(selector)
                if elements:
                    logger.info(f"{selector} 요소 발견: {len(elements)}개")
                    for i, element in enumerate(elements[:10]):  # 최대 10개만 표시
                        try:
                            text = element.text.strip()
                            if text and len(text) < 50:  # 텍스트가 있고 너무 길지 않은 것만
                                logger.info(f"  {i+1}. 텍스트: '{text}', 태그: {element.tag_name}, 클래스: '{element.get_attribute('class')}'")
                        except:
                            continue
            except:
                continue
        
        # 브라우저 유지
        input("분석 완료. 확인 후 Enter를 눌러주세요...")
        
        return True
        
    except Exception as e:
        logger.error(f"페이지 분석 오류: {e}")
        return False


if __name__ == "__main__":
    success = analyze_current_page()
    if success:
        logger.info("🎉 페이지 분석 완료!")
    else:
        logger.error("❌ 페이지 분석 실패!") 