"""
웹사이트 자동화 기본 클래스
모든 웹사이트 자동화 클래스의 기본이 되는 추상 클래스
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from loguru import logger


class BaseAutomation(ABC):
    """웹사이트 자동화 기본 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.logger = logger
        self.keep_browser = True  # 기본적으로 브라우저 유지
        
    @abstractmethod
    def setup_driver(self) -> None:
        """웹드라이버 설정"""
        pass
        
    @abstractmethod
    def navigate_to_website(self) -> bool:
        """웹사이트 접속"""
        pass
        
    @abstractmethod
    def login(self, credentials: Dict[str, str]) -> bool:
        """로그인 (필요시)"""
        pass
        
    def fill_form(self, data: Dict[str, Any]) -> bool:
        """폼 작성 (기본 구현)"""
        self.logger.warning("fill_form 메서드가 구현되지 않았습니다")
        return True
        
    @abstractmethod
    def submit_form(self) -> bool:
        """폼 제출"""
        pass
        
    @abstractmethod
    def validate_result(self) -> bool:
        """결과 검증"""
        pass
        
    def cleanup(self) -> None:
        """리소스 정리"""
        if self.driver and not self.keep_browser:
            self.driver.quit()
            self.logger.info("웹드라이버 종료")
        elif self.keep_browser:
            self.logger.info("브라우저를 열린 상태로 유지합니다")
            
    def set_keep_browser(self, keep_browser: bool) -> None:
        """브라우저 유지 여부 설정"""
        self.keep_browser = keep_browser
        self.logger.info(f"브라우저 유지 설정: {keep_browser}")
            
    def run_automation(self, data: Dict[str, Any], keep_browser: bool = True) -> bool:
        """자동화 실행"""
        try:
            self.keep_browser = keep_browser
            self.logger.info("자동화 시작")
            
            # 1. 웹드라이버 설정
            self.setup_driver()
            
            # 2. 웹사이트 접속
            if not self.navigate_to_website():
                return False
                
            # 3. 로그인 (필요시)
            if self.config.get('requires_login', False):
                credentials = self.config.get('credentials', {})
                if not self.login(credentials):
                    return False
                    
            # 4. 폼 작성
            if not self.fill_form(data):
                return False
                
            # 5. 폼 제출
            if not self.submit_form():
                return False
                
            # 6. 결과 검증
            if not self.validate_result():
                return False
                
            self.logger.info("자동화 완료")
            
            # 브라우저 유지 여부에 따른 처리
            if self.keep_browser:
                self.logger.info("브라우저가 열린 상태로 유지됩니다. 웹에서 다음 작업을 진행할 수 있습니다.")
            else:
                self.logger.info("브라우저를 닫습니다.")
                self.cleanup()
                
            return True
            
        except Exception as e:
            self.logger.error(f"자동화 실행 중 오류: {e}")
            return False
        finally:
            # 리소스 정리는 keep_browser 설정에 따라 결정
            if not self.keep_browser:
                self.cleanup() 