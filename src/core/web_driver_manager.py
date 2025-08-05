"""
웹드라이버 관리 모듈
Chrome 웹드라이버 설정 및 관리를 담당
"""

import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger


class WebDriverManager:
    """웹드라이버 관리 클래스"""
    
    @staticmethod
    def create_driver(config: dict) -> webdriver.Chrome:
        """웹드라이버 생성"""
        try:
            chrome_options = Options()
            
            # 헤드리스 모드 설정
            if config.get('browser.headless', False):
                chrome_options.add_argument('--headless')
            
            # 브라우저 창 크기 설정
            window_size = config.get('browser.window_size', '1920x1080')
            chrome_options.add_argument(f'--window-size={window_size}')
            
            # User-Agent 설정
            user_agent = config.get('browser.user_agent', 
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # HTTP 사이트 접속을 위한 보안 설정
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--ignore-certificate-errors-spki-list')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-cross-origin-auth-prompt')
            
            # 추가 옵션
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            
            # ARM64 Mac 호환성을 위한 추가 옵션
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            try:
                # webdriver-manager로 자동 설치 시도
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e:
                logger.warning(f"webdriver-manager 자동 설치 실패: {str(e)}")
                
                # 수동으로 ChromeDriver 경로 지정
                if platform.machine() == 'arm64':
                    # M1/M2 Mac용 ChromeDriver 경로
                    chromedriver_path = "/usr/local/bin/chromedriver"
                    if not os.path.exists(chromedriver_path):
                        chromedriver_path = "/opt/homebrew/bin/chromedriver"
                    
                    if os.path.exists(chromedriver_path):
                        service = Service(chromedriver_path)
                        driver = webdriver.Chrome(service=service, options=chrome_options)
                    else:
                        raise Exception("ChromeDriver를 찾을 수 없습니다. 수동으로 설치해주세요.")
                else:
                    raise e
            
            logger.info("웹드라이버 생성 완료")
            return driver
            
        except Exception as e:
            logger.error(f"웹드라이버 생성 오류: {str(e)}")
            raise
    
    @staticmethod
    def create_wait(driver: webdriver.Chrome, timeout: int = 10) -> WebDriverWait:
        """명시적 대기 객체 생성"""
        return WebDriverWait(driver, timeout) 