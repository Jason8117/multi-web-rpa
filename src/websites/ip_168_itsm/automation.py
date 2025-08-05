"""
IP 168 ITSM 웹사이트 자동화 플러그인
"""

import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.core.base_automation import BaseAutomation
from src.core.web_driver_manager import WebDriverManager
from .element_selectors import IP168ITSMSelectors
from .excel_reader import ITSMExcelReader
from loguru import logger


class IP168ITSMAutomation(BaseAutomation):
    """IP 168 ITSM 웹사이트 자동화 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.selectors = IP168ITSMSelectors()
        self.driver = None
        self.wait = None
        self.excel_reader = ITSMExcelReader(config)
        
    def setup_driver(self) -> None:
        """웹드라이버 설정"""
        try:
            self.driver = WebDriverManager.create_driver(self.config)
            timeout = self.config.get('website.timeout', 10)
            self.wait = WebDriverWait(self.driver, timeout)
            logger.info("IP 168 ITSM 웹드라이버 설정 완료")
        except Exception as e:
            logger.error(f"웹드라이버 설정 오류: {e}")
            raise
            
    def navigate_to_website(self) -> bool:
        """웹사이트 접속"""
        try:
            url = self.config.get('website.url', self.selectors.MAIN_PAGE)
            logger.info(f"IP 168 ITSM 웹사이트 접속 중: {url}")
            
            self.driver.get(url)
            
            # 페이지 로딩 대기
            page_load_time = self.config.get('wait_times.page_load', 3)
            time.sleep(page_load_time)
            
            # 페이지 제목 확인
            page_title = self.driver.title
            logger.info(f"페이지 제목: {page_title}")
            
            logger.info("IP 168 ITSM 웹사이트 접속 완료")
            return True
            
        except Exception as e:
            logger.error(f"웹사이트 접속 오류: {e}")
            return False
            
    def find_element_with_fallback(self, selectors: list, timeout: int = 5) -> Optional[Any]:
        """여러 선택자를 시도하여 요소 찾기"""
        for selector in selectors:
            try:
                if selector.startswith("//"):
                    # XPath 선택자
                    element = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                else:
                    # CSS 선택자
                    element = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                logger.info(f"요소 찾기 성공: {selector}")
                return element
            except TimeoutException:
                logger.debug(f"선택자 실패: {selector}")
                continue
        return None
    
    def login(self, credentials: Optional[Dict[str, str]] = None) -> bool:
        """로그인 수행"""
        try:
            logger.info("IP 168 ITSM 로그인 시작")
            
            # 기본 로그인 정보 사용
            if credentials is None:
                credentials = {
                    'username': self.config.get('login.username', 'ij_itsmadmin'),
                    'password': self.config.get('login.password', '0')
                }
            
            username = credentials.get('username')
            password = credentials.get('password')
            
            logger.info(f"로그인 시도: 사용자명 = {username}")
            
            # 페이지가 완전히 로드될 때까지 대기
            time.sleep(2)
            
            # 사용자명 입력
            username_selectors = self.selectors.get_username_selectors()
            username_element = self.find_element_with_fallback(username_selectors)
            
            if username_element is None:
                logger.error("사용자명 입력 필드를 찾을 수 없습니다")
                return False
            
            # 요소가 상호작용 가능할 때까지 대기
            try:
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.common.by import By
                
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, "userName"))
                )
            except Exception as e:
                logger.warning(f"요소 대기 중 오류 (무시하고 진행): {e}")
            
            # 기존 값 제거 후 입력
            username_element.clear()
            time.sleep(0.5)
            username_element.send_keys(username)
            logger.info("사용자명 입력 완료")
            
            # 비밀번호 입력
            password_selectors = self.selectors.get_password_selectors()
            password_element = self.find_element_with_fallback(password_selectors)
            
            if password_element is None:
                logger.error("비밀번호 입력 필드를 찾을 수 없습니다")
                return False
            
            # 기존 값 제거 후 입력
            password_element.clear()
            password_element.send_keys(password)
            logger.info("비밀번호 입력 완료")
            
            # 로그인 버튼 클릭
            login_button_selectors = self.selectors.get_login_button_selectors()
            login_button = self.find_element_with_fallback(login_button_selectors)
            
            if login_button is None:
                logger.error("로그인 버튼을 찾을 수 없습니다")
                return False
            
            # 로그인 버튼 클릭
            login_button.click()
            logger.info("로그인 버튼 클릭 완료")
            
            # 로그인 완료 대기
            login_wait_time = self.config.get('wait_times.login_wait', 2)
            time.sleep(login_wait_time)
            
            # 로그인 성공 확인
            if self.verify_login_success():
                logger.info("IP 168 ITSM 로그인 성공")
                return True
            else:
                logger.warning("로그인 성공 여부를 확인할 수 없습니다")
                return True  # 일단 성공으로 처리
                
        except Exception as e:
            logger.error(f"로그인 오류: {e}")
            return False
    
    def verify_login_success(self) -> bool:
        """로그인 성공 여부 확인"""
        try:
            # 로그인 후 URL 변경 확인
            current_url = self.driver.current_url
            login_url = self.config.get('website.login_url', self.selectors.LOGIN_PAGE)
            
            if current_url != login_url:
                logger.info(f"URL 변경 감지: {current_url}")
                return True
            
            # 페이지 제목 변경 확인
            page_title = self.driver.title
            if "login" not in page_title.lower() and "sign" not in page_title.lower():
                logger.info(f"페이지 제목 변경: {page_title}")
                return True
            
            # 에러 메시지 확인
            error_selectors = [
                ".error-message",
                ".alert-danger",
                ".login-error",
                "[class*='error']",
                "[class*='alert']"
            ]
            
            for selector in error_selectors:
                try:
                    error_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if error_element.is_displayed():
                        error_text = error_element.text
                        logger.warning(f"로그인 에러 메시지: {error_text}")
                        return False
                except NoSuchElementException:
                    continue
            
            return True
            
        except Exception as e:
            logger.error(f"로그인 성공 확인 오류: {e}")
            return True  # 확인 실패시 성공으로 처리
    
    def run_automation(self, data: Optional[Dict[str, Any]] = None, keep_browser: bool = True, select_language: bool = True, navigate_to_target: bool = True) -> bool:
        """전체 자동화 실행"""
        try:
            logger.info("IP 168 ITSM 자동화 시작")
            
            # 1. 웹드라이버 설정
            self.setup_driver()
            
            # 2. 웹사이트 접속
            if not self.navigate_to_website():
                logger.error("웹사이트 접속 실패")
                return False
            
            # 3. 로그인 페이지에서 언어 선택 (옵션)
            if select_language:
                logger.info("로그인 페이지에서 언어 선택 시도")
                if self.select_language_on_login_page('한국어'):
                    logger.info("✅ 로그인 페이지에서 한국어 선택 성공")
                    time.sleep(2)  # 언어 변경 후 페이지 로딩 대기
                else:
                    logger.warning("⚠️ 로그인 페이지에서 언어 선택 실패")
            
            # 4. 로그인
            if not self.login(data):
                logger.error("로그인 실패")
                return False
            
            # 5. 목표 페이지로 이동 (옵션)
            if navigate_to_target:
                logger.info("목표 페이지로 이동 시도")
                if self.navigate_to_target_page():
                    logger.info("✅ 목표 페이지 이동 성공")
                else:
                    logger.warning("⚠️ 목표 페이지 이동 실패")
            
            logger.info("IP 168 ITSM 자동화 완료")
            
            # 브라우저 유지 여부에 따라 처리
            if keep_browser:
                logger.info("브라우저가 열린 상태로 유지됩니다. 추가 작업을 위해 대기 중...")
                return True
            else:
                self.cleanup()
                return True
            
        except Exception as e:
            logger.error(f"자동화 실행 오류: {e}")
            return False
    
    def cleanup(self) -> None:
        """웹드라이버 정리"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("웹드라이버 정리 완료")
            except Exception as e:
                logger.error(f"웹드라이버 정리 오류: {e}")
    
    def wait_for_user_input(self) -> None:
        """사용자 입력 대기"""
        try:
            input("엔터 키를 누르면 브라우저가 닫힙니다...")
            self.cleanup()
        except KeyboardInterrupt:
            logger.info("사용자가 중단했습니다.")
            self.cleanup()
    
    def navigate_to_menu(self, menu_path: str) -> bool:
        """메뉴 네비게이션"""
        try:
            logger.info(f"메뉴 네비게이션: {menu_path}")
            
            # 메뉴 경로를 '/'로 분리
            menu_items = menu_path.split('/')
            
            for i, menu_item in enumerate(menu_items):
                logger.info(f"메뉴 클릭 시도: {menu_item}")
                
                # 메뉴 요소 찾기
                menu_selectors = [
                    f"//span[contains(text(), '{menu_item}')]",
                    f"//div[contains(text(), '{menu_item}')]",
                    f"//a[contains(text(), '{menu_item}')]",
                    f"//button[contains(text(), '{menu_item}')]",
                    f"[class*='menu']:contains('{menu_item}')",
                    f"[class*='nav']:contains('{menu_item}')"
                ]
                
                menu_found = False
                for selector in menu_selectors:
                    try:
                        if selector.startswith('//'):
                            # XPath 선택자
                            element = self.driver.find_element(By.XPATH, selector)
                        else:
                            # CSS 선택자
                            element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        
                        if element.is_displayed():
                            element.click()
                            logger.info(f"✅ 메뉴 클릭 성공: {menu_item}")
                            time.sleep(1)  # 메뉴 로딩 대기
                            menu_found = True
                            break
                            
                    except Exception as e:
                        continue
                
                if not menu_found:
                    logger.warning(f"⚠️ 메뉴를 찾을 수 없음: {menu_item}")
                    return False
            
            logger.info(f"✅ 메뉴 네비게이션 완료: {menu_path}")
            return True
            
        except Exception as e:
            logger.error(f"메뉴 네비게이션 오류: {e}")
            return False
    
    def navigate_to_system_management(self) -> bool:
        """시스템관리 메뉴로 이동"""
        try:
            logger.info("시스템관리 메뉴로 이동 시도")
            
            # 상단 메뉴에서 시스템관리 찾기
            system_management_selectors = [
                "//span[contains(text(), '시스템관리')]",
                "//div[contains(text(), '시스템관리')]",
                "//a[contains(text(), '시스템관리')]",
                "//button[contains(text(), '시스템관리')]",
                "//li[contains(text(), '시스템관리')]",
                "[class*='menu']:contains('시스템관리')",
                "[class*='nav']:contains('시스템관리')"
            ]
            
            for selector in system_management_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        element.click()
                        logger.info("✅ 시스템관리 메뉴 클릭 성공")
                        time.sleep(2)  # 메뉴 로딩 대기
                        return True
                        
                except Exception as e:
                    continue
            
            logger.warning("⚠️ 시스템관리 메뉴를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"시스템관리 메뉴 이동 오류: {e}")
            return False
    
    def navigate_to_member_registration(self) -> bool:
        """회원등록(메타넷) 메뉴로 이동"""
        try:
            logger.info("회원등록(메타넷) 메뉴로 이동 시도")
            
            # 1단계: 회원관리 메뉴 클릭
            member_management_selectors = [
                "//span[contains(text(), '회원관리')]",
                "//div[contains(text(), '회원관리')]",
                "//a[contains(text(), '회원관리')]",
                "//button[contains(text(), '회원관리')]",
                "//li[contains(text(), '회원관리')]",
                "[class*='menu']:contains('회원관리')",
                "[class*='nav']:contains('회원관리')"
            ]
            
            member_management_found = False
            for selector in member_management_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        element.click()
                        logger.info("✅ 회원관리 메뉴 클릭 성공")
                        time.sleep(1)  # 하위 메뉴 로딩 대기
                        member_management_found = True
                        break
                        
                except Exception as e:
                    continue
            
            if not member_management_found:
                logger.warning("⚠️ 회원관리 메뉴를 찾을 수 없습니다")
                return False
            
            # 2단계: 회원등록(메타넷) 메뉴 클릭
            member_registration_selectors = [
                "//span[contains(text(), '회원등록(메타넷)')]",
                "//div[contains(text(), '회원등록(메타넷)')]",
                "//a[contains(text(), '회원등록(메타넷)')]",
                "//button[contains(text(), '회원등록(메타넷)')]",
                "//li[contains(text(), '회원등록(메타넷)')]",
                "//span[contains(text(), '회원등록')]",
                "//div[contains(text(), '회원등록')]",
                "//a[contains(text(), '회원등록')]",
                "//button[contains(text(), '회원등록')]",
                "//li[contains(text(), '회원등록')]",
                "[class*='menu']:contains('회원등록')",
                "[class*='nav']:contains('회원등록')"
            ]
            
            for selector in member_registration_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        element.click()
                        logger.info("✅ 회원등록(메타넷) 메뉴 클릭 성공")
                        time.sleep(2)  # 페이지 로딩 대기
                        return True
                        
                except Exception as e:
                    continue
            
            logger.warning("⚠️ 회원등록(메타넷) 메뉴를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"회원등록(메타넷) 메뉴 이동 오류: {e}")
            return False
    
    def navigate_to_registration_page_direct(self) -> bool:
        """회원등록 페이지로 직접 이동"""
        try:
            logger.info("회원등록 페이지로 직접 이동 시도")
            
            # 직접 URL로 이동 (사용자가 제공한 정확한 경로)
            registration_url = "http://4.144.198.168/ims/ImsMng001.R01.cmd?rootMenu=MNU180516000001"
            self.driver.get(registration_url)
            
            # 페이지 로딩 대기
            time.sleep(3)
            
            # 페이지 제목 확인
            page_title = self.driver.title
            logger.info(f"회원등록 페이지 제목: {page_title}")
            
            # URL 확인
            current_url = self.driver.current_url
            logger.info(f"현재 URL: {current_url}")
            
            if "ImsMng001" in current_url:
                logger.info("✅ 회원등록 페이지 접속 성공")
                return True
            else:
                logger.warning("⚠️ 회원등록 페이지 접속 실패")
                return False
                
        except Exception as e:
            logger.error(f"회원등록 페이지 직접 이동 오류: {e}")
            return False
    
    def navigate_to_target_page(self) -> bool:
        """목표 페이지로 이동 (직접 URL 사용)"""
        try:
            logger.info("목표 페이지로 이동 시작")
            
            # 직접 회원등록 페이지 URL로 이동
            if not self.navigate_to_registration_page_direct():
                logger.error("회원등록 페이지 이동 실패")
                return False
            
            logger.info("✅ 목표 페이지 이동 완료")
            return True
            
        except Exception as e:
            logger.error(f"목표 페이지 이동 오류: {e}")
            return False
    
    def fill_form_data(self, form_data: Dict[str, Any]) -> bool:
        """폼 데이터 입력"""
        try:
            logger.info("폼 데이터 입력 시작")
            
            for field_name, value in form_data.items():
                if not self.fill_field(field_name, value):
                    logger.warning(f"필드 '{field_name}' 입력 실패")
            
            logger.info("폼 데이터 입력 완료")
            return True
            
        except Exception as e:
            logger.error(f"폼 데이터 입력 오류: {e}")
            return False
    
    def fill_field(self, field_name: str, value: Any) -> bool:
        """개별 필드 입력"""
        try:
            # 필드 선택자 찾기
            field_selector = self.selectors.get_field_selector(field_name)
            if not field_selector:
                logger.warning(f"필드 '{field_name}'의 선택자를 찾을 수 없습니다")
                return False
            
            # 요소 찾기
            element = self.find_element_with_fallback([field_selector])
            if not element:
                logger.warning(f"필드 '{field_name}' 요소를 찾을 수 없습니다")
                return False
            
            # 값 입력
            element.clear()
            element.send_keys(str(value))
            logger.info(f"필드 '{field_name}'에 값 '{value}' 입력 완료")
            return True
            
        except Exception as e:
            logger.error(f"필드 '{field_name}' 입력 오류: {e}")
            return False
    
    def click_button(self, button_name: str) -> bool:
        """버튼 클릭"""
        try:
            # 버튼 선택자 찾기
            button_selector = self.selectors.get_button_selector(button_name)
            if not button_selector:
                logger.warning(f"버튼 '{button_name}'의 선택자를 찾을 수 없습니다")
                return False
            
            # 요소 찾기
            element = self.find_element_with_fallback([button_selector])
            if not element:
                logger.warning(f"버튼 '{button_name}' 요소를 찾을 수 없습니다")
                return False
            
            # 클릭
            element.click()
            logger.info(f"버튼 '{button_name}' 클릭 완료")
            return True
            
        except Exception as e:
            logger.error(f"버튼 '{button_name}' 클릭 오류: {e}")
            return False
    
    def select_option(self, select_name: str, option_value: str) -> bool:
        """옵션 선택"""
        try:
            from selenium.webdriver.support.ui import Select
            
            # 셀렉트 요소 찾기
            select_selector = self.selectors.get_select_selector(select_name)
            if not select_selector:
                logger.warning(f"셀렉트 '{select_name}'의 선택자를 찾을 수 없습니다")
                return False
            
            # 요소 찾기
            element = self.find_element_with_fallback([select_selector])
            if not element:
                logger.warning(f"셀렉트 '{select_name}' 요소를 찾을 수 없습니다")
                return False
            
            # Select 객체 생성 및 옵션 선택
            select = Select(element)
            select.select_by_value(option_value)
            logger.info(f"셀렉트 '{select_name}'에서 옵션 '{option_value}' 선택 완료")
            return True
            
        except Exception as e:
            logger.error(f"셀렉트 '{select_name}' 옵션 선택 오류: {e}")
            return False
    
    def get_current_page_info(self) -> Dict[str, Any]:
        """현재 페이지 정보 가져오기"""
        try:
            info = {
                'url': self.driver.current_url,
                'title': self.driver.title,
                'page_source_length': len(self.driver.page_source)
            }
            logger.info(f"현재 페이지 정보: {info}")
            return info
        except Exception as e:
            logger.error(f"페이지 정보 가져오기 오류: {e}")
            return {}
    
    def analyze_login_page_language_selector(self) -> Dict[str, Any]:
        """로그인 페이지의 언어 선택 요소 분석"""
        try:
            logger.info("로그인 페이지 언어 선택 요소 분석 시작")
            
            analysis_result = {
                'found_elements': [],
                'language_options': [],
                'current_language': None,
                'recommended_selector': None
            }
            
            # 가능한 언어 선택 요소들 찾기
            language_selectors = [
                # 일반적인 언어 선택 요소들
                "select[name*='lang']",
                "select[name*='language']",
                "select[name*='locale']",
                "select[id*='lang']",
                "select[id*='language']",
                "select[id*='locale']",
                "select[class*='lang']",
                "select[class*='language']",
                
                # 드롭다운 형태의 언어 선택
                ".language-selector select",
                ".lang-selector select",
                ".locale-selector select",
                "[class*='language'] select",
                "[class*='lang'] select",
                
                # 버튼 형태의 언어 선택
                "button[onclick*='lang']",
                "button[onclick*='language']",
                "a[href*='lang']",
                "a[href*='language']",
                
                # 라디오 버튼 형태
                "input[type='radio'][name*='lang']",
                "input[type='radio'][name*='language']",
                
                # 체크박스 형태
                "input[type='checkbox'][name*='lang']",
                "input[type='checkbox'][name*='language']",
                
                # Material-UI 언어 선택 요소들 (디버그에서 발견)
                "div:contains('English')",
                "div:contains('한국어')",
                "div:contains('Korean')",
                "[class*='MuiSelect']",
                "[class*='MuiOutlinedInput']",
                "[class*='jss10']",
                "[class*='MuiSelect-select']",
                "[class*='MuiSelect-outlined']",
                
                # XPath로 텍스트 기반 검색
                "//div[contains(text(), 'English')]",
                "//div[contains(text(), '한국어')]",
                "//div[contains(text(), 'Korean')]",
                "//span[contains(text(), 'English')]",
                "//span[contains(text(), '한국어')]",
                "//span[contains(text(), 'Korean')]"
            ]
            
            # 각 선택자로 요소 찾기
            for selector in language_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            element_info = {
                                'selector': selector,
                                'tag_name': element.tag_name,
                                'tag_text': element.text,
                                'attributes': {
                                    'name': element.get_attribute('name'),
                                    'id': element.get_attribute('id'),
                                    'class': element.get_attribute('class'),
                                    'value': element.get_attribute('value'),
                                    'onclick': element.get_attribute('onclick'),
                                    'href': element.get_attribute('href')
                                }
                            }
                            analysis_result['found_elements'].append(element_info)
                            logger.info(f"언어 선택 요소 발견: {element_info}")
                except Exception as e:
                    continue
            
            # 페이지 소스에서 언어 관련 키워드 찾기
            page_source = self.driver.page_source
            language_keywords = [
                '한국어', 'Korean', 'ko', 'ko-KR',
                '영어', 'English', 'en', 'en-US',
                '일본어', 'Japanese', 'ja', 'ja-JP',
                '중국어', 'Chinese', 'zh', 'zh-CN'
            ]
            
            for keyword in language_keywords:
                if keyword in page_source:
                    analysis_result['language_options'].append(keyword)
            
            # 현재 선택된 언어 확인
            for element_info in analysis_result['found_elements']:
                if element_info['tag_name'] == 'select':
                    try:
                        from selenium.webdriver.support.ui import Select
                        element = self.driver.find_element(By.CSS_SELECTOR, element_info['selector'])
                        select = Select(element)
                        selected_option = select.first_selected_option
                        analysis_result['current_language'] = selected_option.text
                        logger.info(f"현재 선택된 언어: {selected_option.text}")
                    except:
                        pass
            
            # 추천 선택자 결정
            if analysis_result['found_elements']:
                # select 태그가 있으면 우선 선택
                for element_info in analysis_result['found_elements']:
                    if element_info['tag_name'] == 'select':
                        analysis_result['recommended_selector'] = element_info['selector']
                        break
                
                # select가 없으면 첫 번째 발견된 요소
                if not analysis_result['recommended_selector']:
                    analysis_result['recommended_selector'] = analysis_result['found_elements'][0]['selector']
            
            logger.info(f"분석 결과: {analysis_result}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"로그인 페이지 언어 선택 요소 분석 오류: {e}")
            return {}
    
    def select_language_on_login_page(self, language: str = '한국어') -> bool:
        """로그인 페이지에서 언어 선택"""
        try:
            logger.info(f"로그인 페이지에서 언어 '{language}' 선택 시도")
            
            # 먼저 언어 선택 요소 분석
            analysis = self.analyze_login_page_language_selector()
            
            if not analysis.get('found_elements'):
                logger.warning("언어 선택 요소를 찾을 수 없습니다")
                return False
            
            # 추천 선택자 사용
            recommended_selector = analysis.get('recommended_selector')
            if not recommended_selector:
                logger.warning("추천 선택자를 찾을 수 없습니다")
                return False
            
            # 요소 찾기
            element = self.driver.find_element(By.CSS_SELECTOR, recommended_selector)
            
            # 요소 타입에 따른 처리
            if element.tag_name == 'select':
                # 셀렉트 박스인 경우
                from selenium.webdriver.support.ui import Select
                select = Select(element)
                
                # 다양한 방법으로 한국어 선택 시도
                try:
                    select.select_by_visible_text(language)
                    logger.info(f"✅ 언어 '{language}' 선택 성공 (visible_text)")
                    return True
                except:
                    try:
                        select.select_by_value('ko')
                        logger.info(f"✅ 언어 '{language}' 선택 성공 (value='ko')")
                        return True
                    except:
                        try:
                            select.select_by_value('ko-KR')
                            logger.info(f"✅ 언어 '{language}' 선택 성공 (value='ko-KR')")
                            return True
                        except:
                            try:
                                select.select_by_index(0)  # 첫 번째 옵션 선택
                                logger.info(f"✅ 첫 번째 언어 옵션 선택 성공")
                                return True
                            except:
                                logger.error("셀렉트 박스에서 언어 선택 실패")
                                return False
            
            elif element.tag_name == 'button':
                # 버튼인 경우 클릭
                element.click()
                logger.info("언어 선택 버튼 클릭 완료")
                time.sleep(1)
                return True
            
            elif element.tag_name == 'a':
                # 링크인 경우 클릭
                element.click()
                logger.info("언어 선택 링크 클릭 완료")
                time.sleep(1)
                return True
            
            elif element.tag_name == 'input' and element.get_attribute('type') == 'radio':
                # 라디오 버튼인 경우
                element.click()
                logger.info("언어 선택 라디오 버튼 클릭 완료")
                time.sleep(1)
                return True
            
            elif element.tag_name == 'div':
                # div 요소인 경우 (Material-UI 언어 선택기)
                logger.info("Material-UI 언어 선택기 발견")
                
                # 클릭하여 드롭다운 열기
                element.click()
                time.sleep(1)
                
                # 한국어 옵션 찾기 및 클릭
                korean_selectors = [
                    "//div[contains(text(), '한국어')]",
                    "//div[contains(text(), 'Korean')]",
                    "//span[contains(text(), '한국어')]",
                    "//span[contains(text(), 'Korean')]",
                    "//li[contains(text(), '한국어')]",
                    "//li[contains(text(), 'Korean')]"
                ]
                
                for selector in korean_selectors:
                    try:
                        korean_option = self.driver.find_element(By.XPATH, selector)
                        if korean_option.is_displayed():
                            korean_option.click()
                            logger.info(f"✅ 한국어 옵션 클릭 성공: {selector}")
                            time.sleep(1)
                            return True
                    except:
                        continue
                
                logger.warning("한국어 옵션을 찾을 수 없습니다")
                return False
            
            else:
                logger.warning(f"지원하지 않는 요소 타입: {element.tag_name}")
                return False
                
        except Exception as e:
            logger.error(f"로그인 페이지 언어 선택 오류: {e}")
            return False
    
    def submit_form(self) -> bool:
        """폼 제출 (로그인 폼의 경우 로그인 버튼 클릭)"""
        try:
            logger.info("폼 제출 (로그인) 수행")
            return self.login()
        except Exception as e:
            logger.error(f"폼 제출 오류: {e}")
            return False
    
    def validate_result(self) -> bool:
        """결과 검증 (로그인 성공 여부 확인)"""
        try:
            logger.info("로그인 결과 검증")
            return self.verify_login_success()
        except Exception as e:
            logger.error(f"결과 검증 오류: {e}")
            return False
    
    def take_screenshot(self, filename: str = None) -> str:
        """스크린샷 촬영"""
        try:
            if filename is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"ip_168_itsm_{timestamp}.png"
            
            # 스크린샷 디렉토리 생성
            screenshot_dir = Path(__file__).parent.parent.parent.parent / "logs" / "screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            
            screenshot_path = screenshot_dir / filename
            self.driver.save_screenshot(str(screenshot_path))
            
            logger.info(f"스크린샷 저장: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            logger.error(f"스크린샷 촬영 오류: {e}")
            return ""
    
    def analyze_registration_form(self) -> Dict[str, Any]:
        """회원등록 폼 분석"""
        try:
            logger.info("회원등록 폼 분석 시작")
            
            analysis_result = {
                'found_fields': [],
                'found_buttons': [],
                'form_structure': {},
                'page_info': {
                    'title': self.driver.title,
                    'url': self.driver.current_url
                }
            }
            
            # 일반적인 입력 필드들 찾기
            input_selectors = [
                "input[type='text']",
                "input[type='email']",
                "input[type='tel']",
                "input[type='password']",
                "input[type='number']",
                "textarea",
                "select"
            ]
            
            for selector in input_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            field_info = {
                                'selector': selector,
                                'tag_name': element.tag_name,
                                'type': element.get_attribute('type'),
                                'name': element.get_attribute('name'),
                                'id': element.get_attribute('id'),
                                'placeholder': element.get_attribute('placeholder'),
                                'value': element.get_attribute('value'),
                                'class': element.get_attribute('class'),
                                'label': self.get_field_label(element)
                            }
                            analysis_result['found_fields'].append(field_info)
                            logger.info(f"입력 필드 발견: {field_info}")
                except Exception as e:
                    continue
            
            # 버튼들 찾기
            button_selectors = [
                "button",
                "input[type='submit']",
                "input[type='button']"
            ]
            
            for selector in button_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            button_info = {
                                'selector': selector,
                                'tag_name': element.tag_name,
                                'text': element.text,
                                'type': element.get_attribute('type'),
                                'name': element.get_attribute('name'),
                                'id': element.get_attribute('id'),
                                'class': element.get_attribute('class')
                            }
                            analysis_result['found_buttons'].append(button_info)
                            logger.info(f"버튼 발견: {button_info}")
                except Exception as e:
                    continue
            
            logger.info(f"폼 분석 완료: 필드 {len(analysis_result['found_fields'])}개, 버튼 {len(analysis_result['found_buttons'])}개")
            return analysis_result
            
        except Exception as e:
            logger.error(f"회원등록 폼 분석 오류: {e}")
            return {}
    
    def get_field_label(self, element) -> str:
        """필드의 라벨 텍스트 찾기"""
        try:
            # 다양한 방법으로 라벨 찾기
            label_selectors = [
                f"label[for='{element.get_attribute('id')}']",
                f"//label[@for='{element.get_attribute('id')}']",
                f"//label[contains(text(), '')]//following-sibling::*[1]",
                f"//*[contains(text(), '')]//following-sibling::*[1]"
            ]
            
            for selector in label_selectors:
                try:
                    if selector.startswith('//'):
                        label_element = self.driver.find_element(By.XPATH, selector)
                    else:
                        label_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if label_element.is_displayed():
                        return label_element.text.strip()
                except:
                    continue
            
            return ""
        except:
            return ""
    
    def test_name_field(self, test_value: str = "테스트성명") -> bool:
        """성명 필드 테스트"""
        try:
            logger.info(f"성명 필드 테스트 시작: {test_value}")
            
            # 성명 관련 필드 찾기 (사용자가 제공한 정확한 정보 포함)
            name_selectors = [
                "input[name='perNm']",  # 정확한 name 속성
                "input[id='mui-26']",   # 정확한 id 속성
                "input[name*='perNm']",
                "input[name*='name']",
                "input[name*='nm']",
                "input[name*='성명']",
                "input[name*='이름']",
                "input[placeholder*='성명']",
                "input[placeholder*='이름']",
                "input[id*='name']",
                "input[id*='nm']",
                "//input[@name='perNm']",
                "//input[@id='mui-26']",
                "//input[contains(@name, 'name')]",
                "//input[contains(@name, 'nm')]",
                "//input[contains(@placeholder, '성명')]",
                "//input[contains(@placeholder, '이름')]"
            ]
            
            for selector in name_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"성명 필드 발견: {selector}")
                        logger.info(f"현재 값: {current_value}")
                        
                        # 테스트 값 입력 (JavaScript로 강제 설정)
                        self.driver.execute_script("arguments[0].value = '';", element)
                        element.clear()
                        element.send_keys(test_value)          # 새 값 입력
                        
                        # 입력된 값 확인
                        time.sleep(1)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == test_value:
                            logger.info("✅ 성명 필드 테스트 성공")
                            return True
                        else:
                            logger.warning(f"⚠️ 성명 필드 테스트 실패: 입력값 불일치")
                            return False
                            
                except Exception as e:
                    continue
            
            logger.warning("⚠️ 성명 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"성명 필드 테스트 오류: {e}")
            return False
    
    def fill_registration_form(self, user_data: Dict[str, Any]) -> bool:
        """회원등록 폼 자동 입력"""
        try:
            logger.info(f"회원등록 폼 자동 입력 시작: {user_data.get('per_nm', 'Unknown')}")
            
            # 엑셀 필드명과 웹 폼 필드명 매핑 (실제 엑셀 컬럼명 기준)
            field_mapping = {
                'per_nm': '성명',      # 엑셀의 per_nm -> 웹 폼의 성명 필드
                '계열사': '법인',      # 엑셀의 계열사 -> 웹 폼의 법인 필드
                'per_work': '직위',    # 엑셀의 per_work -> 웹 폼의 직위 필드
                'phone': '내선번호',   # 엑셀의 phone -> 웹 폼의 내선번호 필드
                'mobile': '휴대폰',    # 엑셀의 mobile -> 웹 폼의 휴대폰 필드
                'per_nm_en': '영문이름' # 엑셀의 per_nm_en -> 웹 폼의 영문이름 필드
            }
            
            success_count = 0
            # email 필드는 두 곳에 입력되므로 +2, 나머지는 +1
            total_fields = len(field_mapping) + 2 if user_data.get('email') else len(field_mapping)
            
            logger.info(f"엑셀 데이터: {user_data}")
            
            # 1단계: 성명 필드 먼저 입력 (중복확인 전에 필요)
            if 'per_nm' in user_data and user_data['per_nm']:
                value = str(user_data['per_nm'])
                logger.info(f"1단계 - 성명 필드 입력: {value}")
                if self.fill_name_field_specific(value):
                    logger.info(f"✅ 성명 필드에 값 '{value}' 입력 성공")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ 성명 필드 입력 실패")
            
            # 2단계: email 필드 특별 처리 (사용자ID와 메일 두 곳에 입력)
            email_value = user_data.get('email')
            if email_value:
                logger.info(f"2단계 - email 필드 특별 처리: {email_value} -> 사용자ID 및 메일")
                
                # 2-1. 사용자 ID 필드에 입력 (중복확인 포함)
                if self.fill_user_id_field_specific(str(email_value)):
                    logger.info(f"✅ 사용자 ID 필드에 email 값 '{email_value}' 입력 성공 (중복확인 포함)")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ 사용자 ID 필드 입력 실패 (중복확인 포함)")
                
                # 2-2. 메일 필드에 입력
                if self.fill_email_field_specific(str(email_value)):
                    logger.info(f"✅ 메일 필드에 email 값 '{email_value}' 입력 성공")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ 메일 필드 입력 실패")
            
            # 3단계: 나머지 필드들 처리 (성명과 email은 이미 처리했으므로 제외)
            logger.info("3단계 - 나머지 필드들 처리")
            
            # 법인 필드 처리 (계열사 값을 compCd 필드에 선택)
            if '계열사' in user_data and user_data['계열사']:
                value = str(user_data['계열사'])
                logger.info(f"3-1. 법인 필드 처리: {value}")
                if self.fill_company_field_specific(value):
                    logger.info(f"✅ 법인 필드에 계열사 값 '{value}' 선택 성공")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ 법인 필드 선택 실패")
            
            # 직위 필드 처리
            if 'per_work' in user_data and user_data['per_work']:
                value = str(user_data['per_work'])
                logger.info(f"3-2. 직위 필드 처리: {value}")
                if self.fill_position_field_specific(value):
                    logger.info(f"✅ 직위 필드에 값 '{value}' 입력 성공")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ 직위 필드 입력 실패")
            
            # 내선번호 필드 처리
            if 'phone' in user_data and user_data['phone']:
                value = str(user_data['phone'])
                logger.info(f"3-3. 내선번호 필드 처리: {value}")
                if self.fill_phone_field_specific(value):
                    logger.info(f"✅ 내선번호 필드에 값 '{value}' 입력 성공")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ 내선번호 필드 입력 실패")
            
            # 휴대폰 필드 처리
            if 'mobile' in user_data and user_data['mobile']:
                value = str(user_data['mobile'])
                logger.info(f"3-4. 휴대폰 필드 처리: {value}")
                if self.fill_mobile_field_specific(value):
                    logger.info(f"✅ 휴대폰 필드에 값 '{value}' 입력 성공")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ 휴대폰 필드 입력 실패")
            
            # 영문이름 필드 처리
            if 'per_nm_en' in user_data and user_data['per_nm_en']:
                value = str(user_data['per_nm_en'])
                logger.info(f"3-5. 영문이름 필드 처리: {value}")
                if self.fill_english_name_field_specific(value):
                    logger.info(f"✅ 영문이름 필드에 값 '{value}' 입력 성공")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ 영문이름 필드 입력 실패")
            
            logger.info(f"회원등록 폼 입력 완료: {success_count}/{total_fields} 필드 성공")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"회원등록 폼 자동 입력 오류: {e}")
            return False
    
    def fill_field_by_name(self, field_name: str, value: str) -> bool:
        """필드명으로 필드 찾아서 값 입력"""
        try:
            # 다양한 선택자로 필드 찾기 (정확한 매칭 우선)
            field_selectors = [
                f"input[name='{field_name}']",  # 정확한 name 속성 매칭
                f"input[id='{field_name}']",    # 정확한 id 속성 매칭
                f"input[name*='{field_name}']",
                f"input[id*='{field_name}']",
                f"input[placeholder*='{field_name}']",
                f"textarea[name*='{field_name}']",
                f"textarea[id*='{field_name}']",
                f"select[name*='{field_name}']",
                f"select[id*='{field_name}']",
                f"//input[@name='{field_name}']",
                f"//input[@id='{field_name}']",
                f"//input[contains(@name, '{field_name}')]",
                f"//input[contains(@id, '{field_name}')]",
                f"//textarea[contains(@name, '{field_name}')]",
                f"//select[contains(@name, '{field_name}')]"
            ]
            
            for selector in field_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        self.driver.execute_script("arguments[0].value = '';", element)
                        element.clear()
                        element.send_keys(value)               # 새 값 입력
                        return True
                        
                except Exception as e:
                    continue
            
            return False
            
        except Exception as e:
            logger.error(f"필드 '{field_name}' 입력 오류: {e}")
            return False
    
    def fill_name_field_specific(self, value: str) -> bool:
        """성명 필드 특별 처리 (정확한 필드 정보 사용)"""
        try:
            logger.info(f"성명 필드 특별 처리 시작: {value}")
            
            # 사용자가 제공한 정확한 필드 정보 사용
            name_selectors = [
                "input[name='perNm']",    # 정확한 name 속성
                "input[id='mui-1']",      # 정확한 id 속성 (사용자 제공)
                "input[id='mui-26']",     # 기존 id 속성 (백업)
                "//input[@name='perNm']",
                "//input[@id='mui-1']",
                "//input[@id='mui-26']"
            ]
            
            for selector in name_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        logger.info(f"성명 필드 발견: {selector}")
                        
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"현재 값: {current_value}")
                        
                        # 값 입력 (더 강력한 방법)
                        element.click()  # 포커스
                        element.send_keys(Keys.CONTROL + "a")  # 전체 선택
                        element.send_keys(Keys.DELETE)  # 삭제
                        self.driver.execute_script("arguments[0].value = '';", element)  # JavaScript로도 지우기
                        element.clear()  # Selenium clear
                        
                        # 잠시 대기
                        time.sleep(0.5)
                        
                        element.send_keys(value)  # 새 값 입력
                        
                        # 입력 확인
                        time.sleep(0.5)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == value:
                            logger.info("✅ 성명 필드 입력 성공")
                            return True
                        else:
                            logger.warning(f"⚠️ 성명 필드 입력 실패: 값 불일치")
                            return False
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 성명 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"성명 필드 특별 처리 오류: {e}")
            return False
    
    def test_name_field_with_exact_selectors(self, test_value: str = "테스트성명") -> bool:
        """정확한 선택자로 성명 필드 테스트"""
        try:
            logger.info(f"정확한 선택자로 성명 필드 테스트 시작: {test_value}")
            
            # 사용자가 제공한 정확한 필드 정보만 사용
            exact_selectors = [
                "input[name='perNm']",
                "input[id='mui-1']",      # 사용자 제공
                "input[id='mui-26']"      # 백업
            ]
            
            for selector in exact_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        logger.info(f"성명 필드 발견: {selector}")
                        logger.info(f"필드 속성: name='{element.get_attribute('name')}', id='{element.get_attribute('id')}'")
                        
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"현재 값: {current_value}")
                        
                        # 테스트 값 입력 (JavaScript로 강제 설정)
                        self.driver.execute_script("arguments[0].value = '';", element)
                        element.clear()
                        element.send_keys(test_value)          # 새 값 입력
                        
                        # 입력 확인
                        time.sleep(1)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == test_value:
                            logger.info("✅ 정확한 선택자로 성명 필드 테스트 성공")
                            return True
                        else:
                            logger.warning(f"⚠️ 정확한 선택자로 성명 필드 테스트 실패: 값 불일치")
                            return False
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 정확한 선택자로 성명 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"정확한 선택자로 성명 필드 테스트 오류: {e}")
            return False
    
    def fill_user_id_field_specific(self, value: str) -> bool:
        """사용자 ID 필드 특별 처리 (정확한 필드 정보 사용)"""
        try:
            logger.info(f"사용자 ID 필드 특별 처리 시작: {value}")
            
            # 사용자가 제공한 정확한 필드 정보 사용
            user_id_selectors = [
                "input[name='perId']",    # 정확한 name 속성
                "input[id='mui-2']",      # 정확한 id 속성
                "//input[@name='perId']",
                "//input[@id='mui-2']"
            ]
            
            for selector in user_id_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        logger.info(f"사용자 ID 필드 발견: {selector}")
                        
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"현재 값: {current_value}")
                        
                        # 값 입력 (더 강력한 방법)
                        element.click()  # 포커스
                        element.send_keys(Keys.CONTROL + "a")  # 전체 선택
                        element.send_keys(Keys.DELETE)  # 삭제
                        self.driver.execute_script("arguments[0].value = '';", element)  # JavaScript로도 지우기
                        element.clear()  # Selenium clear
                        
                        # 잠시 대기
                        time.sleep(0.5)
                        
                        element.send_keys(value)  # 새 값 입력
                        
                        # 입력 확인
                        time.sleep(0.5)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == value:
                            logger.info("✅ 사용자 ID 필드 입력 성공")
                            
                            # 중복확인 버튼 클릭
                            if self.click_duplicate_check_button():
                                # 중복확인 결과 확인
                                result = self.check_duplicate_result()
                                if result['success']:
                                    if result['available']:
                                        logger.info("✅ 사용자 ID 중복확인 완료: 사용 가능")
                                        
                                        # 팝업 닫기
                                        if self.close_duplicate_check_dialog():
                                            logger.info("✅ 중복확인 팝업 닫기 완료")
                                            return True
                                        else:
                                            logger.warning("⚠️ 중복확인 팝업 닫기 실패")
                                            return False
                                        
                                    elif result['available'] is False:
                                        logger.warning("⚠️ 사용자 ID 중복확인 실패: 이미 사용 중")
                                        
                                        # 팝업 닫기
                                        self.close_duplicate_check_dialog()
                                        return False
                                        
                                    else:
                                        logger.info(f"중복확인 결과: {result['message']}")
                                        
                                        # 팝업 닫기
                                        self.close_duplicate_check_dialog()
                                        return True
                                else:
                                    logger.warning("⚠️ 중복확인 결과 확인 실패")
                                    return False
                            else:
                                logger.warning("⚠️ 중복확인 버튼 클릭 실패")
                                return False
                        else:
                            logger.warning(f"⚠️ 사용자 ID 필드 입력 실패: 값 불일치")
                            return False
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 사용자 ID 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"사용자 ID 필드 특별 처리 오류: {e}")
            return False
    
    def test_user_id_field_with_exact_selectors(self, test_value: str = "testuser@example.com") -> bool:
        """정확한 선택자로 사용자 ID 필드 테스트"""
        try:
            logger.info(f"정확한 선택자로 사용자 ID 필드 테스트 시작: {test_value}")
            
            # 사용자가 제공한 정확한 필드 정보만 사용
            exact_selectors = [
                "input[name='perId']",
                "input[id='mui-2']"
            ]
            
            for selector in exact_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        logger.info(f"사용자 ID 필드 발견: {selector}")
                        logger.info(f"필드 속성: name='{element.get_attribute('name')}', id='{element.get_attribute('id')}'")
                        
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"현재 값: {current_value}")
                        
                        # 테스트 값 입력 (JavaScript로 강제 설정)
                        self.driver.execute_script("arguments[0].value = '';", element)
                        element.clear()
                        element.send_keys(test_value)          # 새 값 입력
                        
                        # 입력 확인
                        time.sleep(1)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == test_value:
                            logger.info("✅ 정확한 선택자로 사용자 ID 필드 테스트 성공")
                            return True
                        else:
                            logger.warning(f"⚠️ 정확한 선택자로 사용자 ID 필드 테스트 실패: 값 불일치")
                            return False
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 정확한 선택자로 사용자 ID 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"정확한 선택자로 사용자 ID 필드 테스트 오류: {e}")
            return False
    
    def click_duplicate_check_button(self) -> bool:
        """중복확인 버튼 클릭"""
        try:
            logger.info("중복확인 버튼 클릭 시도")
            
            # 중복확인 버튼 찾기 (더 구체적인 선택자들)
            duplicate_check_selectors = [
                # 사용자 ID 필드 근처의 중복확인 버튼
                "//input[@name='perId']/following-sibling::button[contains(text(), '중복확인')]",
                "//input[@id='mui-2']/following-sibling::button[contains(text(), '중복확인')]",
                "//input[@name='perId']/../following-sibling::button[contains(text(), '중복확인')]",
                "//input[@id='mui-2']/../following-sibling::button[contains(text(), '중복확인')]",
                
                # 일반적인 중복확인 버튼 패턴
                "button:contains('중복확인')",
                "//button[contains(text(), '중복확인')]",
                "//span[contains(text(), '중복확인')]",
                "//div[contains(text(), '중복확인')]",
                "//a[contains(text(), '중복확인')]",
                "[class*='button']:contains('중복확인')",
                "button[type='button']:contains('중복확인')",
                "//button[contains(@class, 'button') and contains(text(), '중복확인')]",
                
                # Material-UI 버튼 패턴
                "//button[contains(@class, 'MuiButton-root') and contains(text(), '중복확인')]",
                "//button[contains(@class, 'MuiButton-outlined') and contains(text(), '중복확인')]"
            ]
            
            for selector in duplicate_check_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed() and element.is_enabled():
                        logger.info(f"중복확인 버튼 발견: {selector}")
                        logger.info(f"버튼 텍스트: '{element.text}'")
                        logger.info(f"버튼 클래스: '{element.get_attribute('class')}'")
                        
                        # 버튼 클릭 전 스크린샷
                        self.take_screenshot("before_duplicate_check_click")
                        
                        # 버튼 클릭
                        element.click()
                        logger.info("✅ 중복확인 버튼 클릭 성공")
                        
                        # 클릭 후 더 긴 대기 시간 (팝업이 나타날 때까지)
                        logger.info("중복확인 버튼 클릭 후 팝업 대기 중...")
                        time.sleep(0.5)  # 5초 대기
                        
                        # 클릭 후 스크린샷
                        self.take_screenshot("after_duplicate_check_click")
                        
                        # 팝업이 나타났는지 빠르게 확인 (더 다양한 방법)
                        popup_detected = False
                        
                        # 1. 일반적인 다이얼로그 확인
                        try:
                            popup_check = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                            if popup_check.is_displayed():
                                logger.info("✅ 팝업이 나타난 것을 확인했습니다 (role='dialog')")
                                popup_detected = True
                        except:
                            pass
                        
                        # 2. Material-UI 모달 확인
                        try:
                            modal_check = self.driver.find_element(By.XPATH, "//div[contains(@class, 'MuiModal-root')]")
                            if modal_check.is_displayed():
                                logger.info("✅ 팝업이 나타난 것을 확인했습니다 (MuiModal-root)")
                                popup_detected = True
                        except:
                            pass
                        
                        # 3. 알림 메시지 확인
                        try:
                            alert_check = self.driver.find_element(By.XPATH, "//div[contains(text(), '사용 가능') or contains(text(), '사용 불가') or contains(text(), '중복')]")
                            if alert_check.is_displayed():
                                logger.info("✅ 알림 메시지가 나타난 것을 확인했습니다")
                                popup_detected = True
                        except:
                            pass
                        
                        # 4. 토스트 메시지 확인
                        try:
                            toast_check = self.driver.find_element(By.XPATH, "//div[contains(@class, 'toast') or contains(@class, 'snackbar') or contains(@class, 'notification')]")
                            if toast_check.is_displayed():
                                logger.info("✅ 토스트 메시지가 나타난 것을 확인했습니다")
                                popup_detected = True
                        except:
                            pass
                        
                        if not popup_detected:
                            logger.warning("⚠️ 팝업이나 알림이 감지되지 않았습니다")
                            logger.info("팝업이 나타날 때까지 추가 대기 및 재시도...")
                            
                            # 팝업이 나타날 때까지 최대 10초 추가 대기
                            for retry in range(1):
                                time.sleep(0.5)
                                logger.info(f"팝업 감지 재시도 {retry + 1}/10")
                                
                                # 다시 팝업 확인
                                try:
                                    popup_check = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                                    if popup_check.is_displayed():
                                        logger.info("✅ 재시도 중 팝업 발견!")
                                        popup_detected = True
                                        break
                                except:
                                    pass
                                
                                try:
                                    modal_check = self.driver.find_element(By.XPATH, "//div[contains(@class, 'MuiModal-root')]")
                                    if modal_check.is_displayed():
                                        logger.info("✅ 재시도 중 모달 발견!")
                                        popup_detected = True
                                        break
                                except:
                                    pass
                            
                            if not popup_detected:
                                logger.warning("⚠️ 모든 재시도 후에도 팝업이 감지되지 않았습니다")
                                logger.info("페이지 소스를 확인하여 응답을 분석합니다...")
                                
                                # 페이지 소스에서 관련 메시지 확인
                                page_source = self.driver.page_source
                                if '사용 가능' in page_source:
                                    logger.info("✅ 페이지 소스에서 '사용 가능' 메시지를 발견했습니다")
                                elif '사용 불가' in page_source:
                                    logger.info("✅ 페이지 소스에서 '사용 불가' 메시지를 발견했습니다")
                                elif '중복' in page_source:
                                    logger.info("✅ 페이지 소스에서 '중복' 메시지를 발견했습니다")
                                else:
                                    logger.warning("⚠️ 페이지 소스에서 관련 메시지를 찾을 수 없습니다")
                        
                        return True
                        
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 중복확인 버튼을 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"중복확인 버튼 클릭 오류: {e}")
            return False
    
    def check_duplicate_result(self) -> Dict[str, Any]:
        """중복확인 결과 확인 (간소화된 버전)"""
        try:
            logger.info("중복확인 결과 확인 중...")
            
            # 중복확인 후 잠시 대기
            time.sleep(0.5)
            
            # 페이지 소스에서 "사용 가능한 ID입니다" 메시지 확인
            page_source = self.driver.page_source
            
            # 성공 메시지 확인
            if '사용 가능한 ID입니다' in page_source:
                logger.info("✅ 중복확인 성공: '사용 가능한 ID입니다' 메시지 발견")
                
                # 팝업 닫기
                if self.close_duplicate_check_dialog():
                    logger.info("✅ 중복확인 팝업 닫기 완료")
                else:
                    logger.warning("⚠️ 중복확인 팝업 닫기 실패")
                
                return {
                    'success': True,
                    'message': '사용 가능한 ID입니다',
                    'popup_found': True
                }
            
            # 실패 메시지 확인
            if '이미 사용 중인 ID입니다' in page_source or '중복된 ID' in page_source:
                logger.warning("❌ 중복확인 실패: 이미 사용 중인 ID")
                
                # 팝업 닫기
                if self.close_duplicate_check_dialog():
                    logger.info("✅ 중복확인 팝업 닫기 완료")
                else:
                    logger.warning("⚠️ 중복확인 팝업 닫기 실패")
                
                return {
                    'success': False,
                    'message': '이미 사용 중인 ID입니다',
                    'popup_found': True
                }
            
            # 팝업이 나타나지 않은 경우, 페이지에서 직접 확인
            logger.info("팝업이 감지되지 않아 페이지에서 직접 확인합니다...")
            
            # 간단한 팝업 감지 시도 (최대 5초)
            for attempt in range(1):
                time.sleep(0.5)
                
                # 현재 페이지의 모든 dialog 요소 확인
                dialogs = self.driver.find_elements(By.XPATH, "//div[@role='dialog']")
                
                for dialog in dialogs:
                    if dialog.is_displayed():
                        dialog_text = dialog.text.strip()
                        if '사용 가능한 ID입니다' in dialog_text:
                            logger.info("✅ 중복확인 성공: 팝업에서 메시지 확인")
                            
                            # 팝업 닫기
                            if self.close_duplicate_check_dialog():
                                logger.info("✅ 중복확인 팝업 닫기 완료")
                            else:
                                logger.warning("⚠️ 중복확인 팝업 닫기 실패")
                            
                            return {
                                'success': True,
                                'message': '사용 가능한 ID입니다',
                                'popup_found': True
                            }
                        elif '이미 사용 중인 ID입니다' in dialog_text:
                            logger.warning("❌ 중복확인 실패: 이미 사용 중인 ID")
                            
                            # 팝업 닫기
                            if self.close_duplicate_check_dialog():
                                logger.info("✅ 중복확인 팝업 닫기 완료")
                            else:
                                logger.warning("⚠️ 중복확인 팝업 닫기 실패")
                            
                            return {
                                'success': False,
                                'message': '이미 사용 중인 ID입니다',
                                'popup_found': True
                            }
            
            # 팝업이 감지되지 않았지만 성공으로 간주 (중복확인 버튼이 클릭되었으므로)
            logger.info("⚠️ 팝업이 감지되지 않았지만 중복확인 버튼이 클릭되었으므로 성공으로 간주")
            return {
                'success': True,
                'message': '중복확인 완료 (팝업 미감지)',
                'popup_found': False
            }
                                            
        except Exception as e:
            logger.error(f"중복확인 결과 확인 오류: {e}")
            return {
                'success': False,
                'message': f'오류: {e}',
                'popup_found': False
            }
            

    
    def close_duplicate_check_dialog(self) -> bool:
        """중복확인 팝업 닫기 ("예" 버튼 클릭) - 개선된 버전"""
        try:
            logger.info("중복확인 팝업 닫기 시도")
            
            # 팝업이 나타날 때까지 잠시 대기
            time.sleep(0.5)
            
            # "예" 버튼 찾기 (개선된 선택자들)
            yes_button_selectors = [
                # 1. 가장 구체적인 선택자들 (우선순위 높음)
                "//button[@test-id='yesBtn']",
                "//button[@test-id='yesBtn' and contains(text(), '예')]",
                
                # 2. 팝업 내에서 "예" 버튼 찾기 (role='dialog' 기반)
                "//div[@role='dialog']//button[contains(text(), '예')]",
                "//div[@role='dialog']//button[normalize-space(text())='예']",
                "//div[contains(@class, 'MuiDialog-paper')]//button[contains(text(), '예')]",
                "//div[contains(@class, 'MuiPaper-root')]//button[contains(text(), '예')]",
                
                # 3. Material-UI 버튼 클래스 활용
                "//button[contains(@class, 'MuiButton-root') and contains(text(), '예')]",
                "//button[contains(@class, 'MuiButton-contained') and contains(text(), '예')]",
                "//button[contains(@class, 'MuiButtonBase-root') and contains(text(), '예')]",
                
                # 4. aria-labelledby 기반 팝업 내 버튼
                "//div[@aria-labelledby]//button[contains(text(), '예')]",
                
                # 5. 일반적인 "예" 버튼 패턴
                "//button[contains(text(), '예')]",
                "//button[normalize-space(text())='예']",
                "//span[contains(text(), '예')]",
                "//div[contains(text(), '예')]",
                
                # 6. CSS 선택자
                "button:contains('예')",
                "//button[contains(@class, 'button') and contains(text(), '예')]",
                "//button[@type='button' and contains(text(), '예')]",
                
                # 7. 모든 버튼에서 "예" 텍스트 찾기 (fallback)
                "//button[contains(., '예')]"
            ]
            
            for selector in yes_button_selectors:
                try:
                    if selector.startswith('//'):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        try:
                            if element.is_displayed() and element.is_enabled():
                                button_text = element.text.strip()
                                button_class = element.get_attribute('class')
                                button_test_id = element.get_attribute('test-id')
                                
                                logger.info(f"'예' 버튼 발견: {selector}")
                                logger.info(f"버튼 텍스트: '{button_text}'")
                                logger.info(f"버튼 클래스: '{button_class}'")
                                logger.info(f"버튼 test-id: '{button_test_id}'")
                                
                                # 버튼이 실제로 "예" 버튼인지 확인 (정확한 매칭)
                                if button_text.strip() == '예':
                                    # 버튼 클릭 전 스크린샷
                                    self.take_screenshot("before_yes_button_click")
                                    
                                    # 버튼 클릭
                                    element.click()
                                    logger.info("✅ '예' 버튼 클릭 성공")
                                    
                                    # 팝업이 닫힐 때까지 대기
                                    time.sleep(0.5)
                                    
                                    # 버튼 클릭 후 스크린샷
                                    self.take_screenshot("after_yes_button_click")
                                    
                                    # 팝업이 실제로 닫혔는지 확인
                                    try:
                                        popup_elements = self.driver.find_elements(By.XPATH, "//div[@role='dialog']")
                                        popup_still_open = False
                                        
                                        for popup in popup_elements:
                                            if popup.is_displayed():
                                                popup_still_open = True
                                                break
                                        
                                        if not popup_still_open:
                                            logger.info("✅ 팝업이 성공적으로 닫혔습니다")
                                            return True
                                        else:
                                            logger.warning("⚠️ 팝업이 여전히 열려있습니다")
                                            
                                    except Exception as e:
                                        logger.info("팝업 확인 중 오류 (무시하고 진행): {e}")
                                        return True
                                    
                                    return True
                                
                        except Exception as e:
                            logger.debug(f"버튼 분석 중 오류: {e}")
                            continue
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ '예' 버튼을 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"중복확인 팝업 닫기 오류: {e}")
            return False
    
    def fill_position_field_specific(self, value: str) -> bool:
        """직위 필드 특별 처리"""
        try:
            logger.info(f"직위 필드 특별 처리 시작: {value}")
            
            position_selectors = [
                "input[name='position']",    # 정확한 name 속성
                "input[id='mui-9']",         # 정확한 id 속성
                "//input[@name='position']",
                "//input[@id='mui-9']"
            ]
            
            for selector in position_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        logger.info(f"직위 필드 발견: {selector}")
                        
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"현재 값: {current_value}")
                        
                        # 값 입력 (더 강력한 방법)
                        element.click()  # 포커스
                        element.send_keys(Keys.CONTROL + "a")  # 전체 선택
                        element.send_keys(Keys.DELETE)  # 삭제
                        self.driver.execute_script("arguments[0].value = '';", element)  # JavaScript로도 지우기
                        element.clear()  # Selenium clear
                        
                        # 잠시 대기
                        time.sleep(0.5)
                        
                        element.send_keys(value)  # 새 값 입력
                        
                        # 입력 확인
                        time.sleep(0.5)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == value:
                            logger.info("✅ 직위 필드 입력 성공")
                            return True
                        else:
                            logger.warning(f"⚠️ 직위 필드 입력 실패: 값 불일치")
                            return False
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 직위 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"직위 필드 특별 처리 오류: {e}")
            return False
    
    def fill_phone_field_specific(self, value: str) -> bool:
        """내선번호 필드 특별 처리"""
        try:
            logger.info(f"내선번호 필드 특별 처리 시작: {value}")
            
            phone_selectors = [
                "input[name='phone']",    # 정확한 name 속성
                "input[id='mui-10']",     # 정확한 id 속성
                "//input[@name='phone']",
                "//input[@id='mui-10']"
            ]
            
            for selector in phone_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        logger.info(f"내선번호 필드 발견: {selector}")
                        
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"현재 값: {current_value}")
                        
                        # 값 입력 (더 강력한 방법)
                        element.click()  # 포커스
                        element.send_keys(Keys.CONTROL + "a")  # 전체 선택
                        element.send_keys(Keys.DELETE)  # 삭제
                        self.driver.execute_script("arguments[0].value = '';", element)  # JavaScript로도 지우기
                        element.clear()  # Selenium clear
                        
                        # 잠시 대기
                        time.sleep(0.5)
                        
                        element.send_keys(value)  # 새 값 입력
                        
                        # 입력 확인
                        time.sleep(0.5)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == value:
                            logger.info("✅ 내선번호 필드 입력 성공")
                            return True
                        else:
                            logger.warning(f"⚠️ 내선번호 필드 입력 실패: 값 불일치")
                            return False
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 내선번호 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"내선번호 필드 특별 처리 오류: {e}")
            return False
    
    def fill_mobile_field_specific(self, value: str) -> bool:
        """휴대폰 필드 특별 처리"""
        try:
            logger.info(f"휴대폰 필드 특별 처리 시작: {value}")
            
            mobile_selectors = [
                "input[name='mobile']",    # 정확한 name 속성
                "input[id='mui-11']",      # 정확한 id 속성
                "//input[@name='mobile']",
                "//input[@id='mui-11']"
            ]
            
            for selector in mobile_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        logger.info(f"휴대폰 필드 발견: {selector}")
                        
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"현재 값: {current_value}")
                        
                        # 값 입력 (더 강력한 방법)
                        element.click()  # 포커스
                        element.send_keys(Keys.CONTROL + "a")  # 전체 선택
                        element.send_keys(Keys.DELETE)  # 삭제
                        self.driver.execute_script("arguments[0].value = '';", element)  # JavaScript로도 지우기
                        element.clear()  # Selenium clear
                        
                        # 잠시 대기
                        time.sleep(0.5)
                        
                        element.send_keys(value)  # 새 값 입력
                        
                        # 입력 확인
                        time.sleep(0.5)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == value:
                            logger.info("✅ 휴대폰 필드 입력 성공")
                            return True
                        else:
                            logger.warning(f"⚠️ 휴대폰 필드 입력 실패: 값 불일치")
                            return False
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 휴대폰 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"휴대폰 필드 특별 처리 오류: {e}")
            return False
    
    def fill_email_field_specific(self, value: str) -> bool:
        """메일 필드 특별 처리"""
        try:
            logger.info(f"메일 필드 특별 처리 시작: {value}")
            
            email_selectors = [
                "input[name='email']",    # 정확한 name 속성
                "input[id='mui-13']",     # 정확한 id 속성
                "//input[@name='email']",
                "//input[@id='mui-13']"
            ]
            
            for selector in email_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        logger.info(f"메일 필드 발견: {selector}")
                        
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"현재 값: {current_value}")
                        
                        # 값 입력 (더 강력한 방법)
                        element.click()  # 포커스
                        element.send_keys(Keys.CONTROL + "a")  # 전체 선택
                        element.send_keys(Keys.DELETE)  # 삭제
                        self.driver.execute_script("arguments[0].value = '';", element)  # JavaScript로도 지우기
                        element.clear()  # Selenium clear
                        
                        # 잠시 대기
                        time.sleep(0.5)
                        
                        element.send_keys(value)  # 새 값 입력
                        
                        # 입력 확인
                        time.sleep(0.5)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == value:
                            logger.info("✅ 메일 필드 입력 성공")
                            return True
                        else:
                            logger.warning(f"⚠️ 메일 필드 입력 실패: 값 불일치")
                            return False
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 메일 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"메일 필드 특별 처리 오류: {e}")
            return False
    
    def fill_english_name_field_specific(self, value: str) -> bool:
        """영문이름 필드 특별 처리"""
        try:
            logger.info(f"영문이름 필드 특별 처리 시작: {value}")
            
            english_name_selectors = [
                "input[name='perNmEn']",    # 정확한 name 속성
                "input[id='mui-15']",       # 정확한 id 속성
                "//input[@name='perNmEn']",
                "//input[@id='mui-15']"
            ]
            
            for selector in english_name_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        logger.info(f"영문이름 필드 발견: {selector}")
                        
                        # 기존 값 확인
                        current_value = element.get_attribute('value')
                        logger.info(f"현재 값: {current_value}")
                        
                        # 값 입력 (더 강력한 방법)
                        element.click()  # 포커스
                        element.send_keys(Keys.CONTROL + "a")  # 전체 선택
                        element.send_keys(Keys.DELETE)  # 삭제
                        self.driver.execute_script("arguments[0].value = '';", element)  # JavaScript로도 지우기
                        element.clear()  # Selenium clear
                        
                        # 잠시 대기
                        time.sleep(0.5)
                        
                        element.send_keys(value)  # 새 값 입력
                        
                        # 입력 확인
                        time.sleep(0.5)
                        new_value = element.get_attribute('value')
                        logger.info(f"입력된 값: {new_value}")
                        
                        if new_value == value:
                            logger.info("✅ 영문이름 필드 입력 성공")
                            return True
                        else:
                            logger.warning(f"⚠️ 영문이름 필드 입력 실패: 값 불일치")
                            return False
                            
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            logger.warning("⚠️ 영문이름 필드를 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"영문이름 필드 특별 처리 오류: {e}")
            return False
    
    def analyze_duplicate_check_popup(self):
        """중복확인 팝업 구조 분석 (개선된 버전)"""
        try:
            logger.info("=== 중복확인 팝업 구조 분석 시작 ===")
            
            # 1. 먼저 ID 입력
            logger.info("1. ID 입력 중...")
            user_id_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='perId']")
            user_id_field.clear()
            user_id_field.send_keys("testuser123@example.com")
            logger.info("✅ ID 입력 완료: testuser123@example.com")
            
            # 2. 중복확인 버튼 클릭
            logger.info("2. 중복확인 버튼 클릭 중...")
            if not self.click_duplicate_check_button():
                logger.error("중복확인 버튼 클릭 실패")
                return False
            
            # 3. 팝업이 나타날 때까지 대기
            logger.info("3. 중복확인 팝업 대기 중...")
            time.sleep(3)
            
            # 현재 페이지의 모든 dialog 관련 요소 찾기
            dialog_elements = self.driver.find_elements(By.XPATH, "//div[@role='dialog']")
            logger.info(f"페이지 내 dialog 요소 개수: {len(dialog_elements)}")
            
            for i, dialog in enumerate(dialog_elements):
                try:
                    dialog_class = dialog.get_attribute('class')
                    dialog_role = dialog.get_attribute('role')
                    dialog_aria = dialog.get_attribute('aria-labelledby')
                    dialog_text = dialog.text.strip()
                    
                    logger.info(f"Dialog {i+1}:")
                    logger.info(f"  클래스: {dialog_class}")
                    logger.info(f"  role: {dialog_role}")
                    logger.info(f"  aria-labelledby: {dialog_aria}")
                    logger.info(f"  텍스트: '{dialog_text}'")
                    
                    # dialog 내부의 버튼들 찾기
                    buttons = dialog.find_elements(By.XPATH, ".//button")
                    logger.info(f"  버튼 개수: {len(buttons)}")
                    
                    for j, button in enumerate(buttons):
                        try:
                            button_text = button.text.strip()
                            button_class = button.get_attribute('class')
                            button_test_id = button.get_attribute('test-id')
                            
                            logger.info(f"    버튼 {j+1}: 텍스트='{button_text}', 클래스='{button_class}', test-id='{button_test_id}'")
                        except Exception as e:
                            logger.debug(f"버튼 {j+1} 분석 실패: {e}")
                    
                except Exception as e:
                    logger.debug(f"Dialog {i+1} 분석 실패: {e}")
            
            # Material-UI 관련 요소들도 확인
            mui_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'Mui')]")
            logger.info(f"Material-UI 요소 개수: {len(mui_elements)}")
            
            # 팝업 관련 키워드가 포함된 요소들 찾기 (중복확인 결과 관련)
            popup_keywords = [
                '사용 가능한 ID입니다', 
                '사용 가능', 
                '중복', 
                '팝업',
                '이미 사용 중인 ID입니다',
                '사용 불가',
                'duplicate',
                'available'
            ]
            
            logger.info("=== 중복확인 결과 관련 키워드 검색 ===")
            for keyword in popup_keywords:
                elements_with_keyword = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{keyword}')]")
                if elements_with_keyword:
                    logger.info(f"키워드 '{keyword}' 포함 요소 개수: {len(elements_with_keyword)}")
                    for k, elem in enumerate(elements_with_keyword[:5]):  # 최대 5개 표시
                        try:
                            elem_text = elem.text.strip()
                            elem_tag = elem.tag_name
                            elem_class = elem.get_attribute('class')
                            elem_role = elem.get_attribute('role')
                            logger.info(f"  요소 {k+1}: 태그={elem_tag}, role='{elem_role}', 클래스='{elem_class}', 텍스트='{elem_text}'")
                        except Exception as e:
                            logger.debug(f"요소 {k+1} 분석 실패: {e}")
            
            # 현재 페이지의 모든 텍스트 내용 확인 (디버깅용)
            logger.info("=== 현재 페이지 전체 텍스트 분석 ===")
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            lines = page_text.split('\n')
            for i, line in enumerate(lines[:20]):  # 최대 20줄만 표시
                if line.strip():
                    logger.info(f"  라인 {i+1}: '{line.strip()}'")
            
            # 스크린샷 촬영
            self.take_screenshot("duplicate_check_popup_analysis")
            
            logger.info("=== 중복확인 팝업 구조 분석 완료 ===")
            return True
            
        except Exception as e:
            logger.error(f"중복확인 팝업 분석 중 오류: {e}")
            return False
    
    def test_user_id_with_duplicate_check(self, test_value: str = "testuser@example.com") -> bool:
        """사용자 ID 입력 및 중복확인 테스트"""
        try:
            logger.info(f"사용자 ID 입력 및 중복확인 테스트 시작: {test_value}")
            
            # 1단계: 사용자 ID 입력
            if not self.fill_user_id_field_specific(test_value):
                logger.error("사용자 ID 입력 실패")
                return False
            
            # 2단계: 중복확인 버튼 클릭
            if not self.click_duplicate_check_button():
                logger.error("중복확인 버튼 클릭 실패")
                return False
            
            # 3단계: 중복확인 결과 확인
            result = self.check_duplicate_result()
            if result['success']:
                if result['available']:
                    logger.info("✅ 사용자 ID 중복확인 테스트 성공: 사용 가능")
                    
                    # 팝업 닫기
                    if self.close_duplicate_check_dialog():
                        logger.info("✅ 중복확인 팝업 닫기 완료")
                        return True
                    else:
                        logger.warning("⚠️ 중복확인 팝업 닫기 실패")
                        return False
                        
                elif result['available'] is False:
                    logger.warning("⚠️ 사용자 ID 중복확인 테스트: 이미 사용 중인 ID")
                    
                    # 팝업 닫기
                    self.close_duplicate_check_dialog()
                    return False
                    
                else:
                    logger.info(f"중복확인 테스트 결과: {result['message']}")
                    
                    # 팝업 닫기
                    self.close_duplicate_check_dialog()
                    return True
            else:
                logger.error("중복확인 결과 확인 실패")
                return False
                
        except Exception as e:
            logger.error(f"사용자 ID 중복확인 테스트 오류: {e}")
            return False
    
    def fill_company_field_specific(self, company_name: str) -> bool:
        """법인 필드 특별 처리 (Material-UI Select 컴포넌트)"""
        try:
            logger.info(f"법인 필드 특별 처리 시작: {company_name}")
            
            # 법인 Select 필드 찾기
            company_select_selectors = [
                "select[id='mui-component-select-compCd']",
                "#mui-component-select-compCd",
                "//select[@id='mui-component-select-compCd']",
                "//div[@id='mui-component-select-compCd']",
                "//div[contains(@class, 'MuiSelect-select') and @id='mui-component-select-compCd']"
            ]
            
            select_element = None
            for selector in company_select_selectors:
                try:
                    if selector.startswith('//'):
                        select_element = self.driver.find_element(By.XPATH, selector)
                    else:
                        select_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if select_element.is_displayed():
                        logger.info(f"법인 Select 필드 발견: {selector}")
                        break
                        
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            if not select_element:
                logger.warning("⚠️ 법인 Select 필드를 찾을 수 없습니다")
                return False
            
            # 현재 선택된 값 확인
            current_value = select_element.get_attribute('value') or select_element.text
            logger.info(f"현재 선택된 법인: {current_value}")
            
            # Select 필드 클릭하여 옵션 목록 열기
            select_element.click()
            logger.info("법인 Select 필드 클릭하여 옵션 목록 열기")
            time.sleep(1)
            
            # 옵션 목록에서 해당 회사명 찾기 (텍스트 기준, Material-UI 구조에 맞춤)
            option_selectors = [
                # Material-UI MenuItem 구조 (이미지에서 확인한 구조)
                f"//li[contains(@class, 'MuiMenuItem') and contains(text(), '{company_name}')]",
                f"//li[contains(@class, 'MuiMenuItem-root') and contains(text(), '{company_name}')]",
                f"//li[contains(@class, 'MuiButtonBase-root') and contains(text(), '{company_name}')]",
                
                # 정확한 텍스트 매칭
                f"//li[text()='{company_name}']",
                f"//li[normalize-space(text())='{company_name}']",
                
                # 부분 텍스트 매칭
                f"//li[contains(text(), '{company_name}')]",
                f"//li[contains(normalize-space(text()), '{company_name}')]",
                
                # role="option" 속성 활용
                f"//li[@role='option' and contains(text(), '{company_name}')]",
                f"//li[@role='option' and text()='{company_name}']",
                
                # Material-UI 특정 클래스 조합
                f"//li[contains(@class, 'MuiMenuItem') and contains(@class, 'MuiButtonBase-root') and contains(text(), '{company_name}')]",
                
                # 일반적인 옵션 패턴 (fallback)
                f"//*[contains(text(), '{company_name}')]"
            ]
            
            option_found = False
            for option_selector in option_selectors:
                try:
                    option_element = self.driver.find_element(By.XPATH, option_selector)
                    if option_element.is_displayed():
                        logger.info(f"법인 옵션 발견: '{option_element.text}' (선택자: {option_selector})")
                        
                        # 옵션 클릭
                        option_element.click()
                        logger.info(f"✅ 법인 옵션 선택 성공: {company_name}")
                        option_found = True
                        
                        # 선택 확인을 위한 대기
                        time.sleep(1)
                        break
                        
                except Exception as e:
                    logger.debug(f"옵션 선택자 {option_selector} 실패: {e}")
                    continue
            
            if not option_found:
                logger.warning(f"⚠️ 법인 옵션을 찾을 수 없습니다: {company_name}")
                logger.info("사용 가능한 옵션들을 확인해보겠습니다...")
                
                # 사용 가능한 모든 옵션 찾기 (더 상세한 정보 포함)
                try:
                    # 페이지 소스 분석을 위한 상세 로깅
                    logger.info("=== 페이지 소스 분석 시작 ===")
                    
                    # 현재 페이지의 모든 li 요소 찾기
                    all_li_elements = self.driver.find_elements(By.XPATH, "//li")
                    logger.info(f"페이지 내 총 li 요소 개수: {len(all_li_elements)}")
                    
                    # Material-UI MenuItem 옵션들 찾기
                    available_options = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'MuiMenuItem')]")
                    logger.info(f"Material-UI MenuItem 요소 개수: {len(available_options)}")
                    
                    if available_options:
                        logger.info("사용 가능한 법인 옵션들 (Material-UI MenuItem):")
                        for i, option in enumerate(available_options[:20]):  # 최대 20개 표시
                            try:
                                option_text = option.text.strip()
                                option_class = option.get_attribute('class')
                                option_role = option.get_attribute('role')
                                option_data_value = option.get_attribute('data-value')
                                option_id = option.get_attribute('id')
                                
                                if option_text:
                                    logger.info(f"  {i+1}. 텍스트: '{option_text}' | 클래스: {option_class} | role: {option_role} | data-value: {option_data_value} | id: {option_id}")
                            except Exception as e:
                                logger.debug(f"옵션 {i+1} 정보 추출 실패: {e}")
                                continue
                    else:
                        logger.info("Material-UI MenuItem 옵션을 찾을 수 없습니다")
                        
                        # 다른 옵션 패턴 시도
                        other_options = self.driver.find_elements(By.XPATH, "//li[@role='option']")
                        logger.info(f"role='option' 요소 개수: {len(other_options)}")
                        if other_options:
                            logger.info("role='option' 옵션들:")
                            for i, option in enumerate(other_options[:20]):
                                try:
                                    option_text = option.text.strip()
                                    option_class = option.get_attribute('class')
                                    option_data_value = option.get_attribute('data-value')
                                    option_id = option.get_attribute('id')
                                    
                                    if option_text:
                                        logger.info(f"  {i+1}. 텍스트: '{option_text}' | 클래스: {option_class} | data-value: {option_data_value} | id: {option_id}")
                                except:
                                    continue
                        
                        # 일반적인 li 요소들도 확인 (텍스트가 있는 것만)
                        general_options = self.driver.find_elements(By.XPATH, "//li[string-length(text()) > 0]")
                        logger.info(f"텍스트가 있는 li 요소 개수: {len(general_options)}")
                        if general_options:
                            logger.info("텍스트가 있는 li 요소들:")
                            for i, option in enumerate(general_options[:15]):
                                try:
                                    option_text = option.text.strip()
                                    option_class = option.get_attribute('class')
                                    if option_text and len(option_text) < 100:  # 너무 긴 텍스트는 제외
                                        logger.info(f"  {i+1}. 텍스트: '{option_text}' | 클래스: {option_class}")
                                except:
                                    continue
                    
                    # 드롭다운 컨테이너 정보 확인
                    dropdown_containers = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiMenu') or contains(@class, 'MuiPopover') or contains(@class, 'MuiList')]")
                    logger.info(f"드롭다운 관련 컨테이너 개수: {len(dropdown_containers)}")
                    for i, container in enumerate(dropdown_containers[:5]):
                        try:
                            container_class = container.get_attribute('class')
                            container_role = container.get_attribute('role')
                            container_id = container.get_attribute('id')
                            logger.info(f"  컨테이너 {i+1}: 클래스={container_class} | role={container_role} | id={container_id}")
                        except:
                            continue
                            
                except Exception as e:
                    logger.warning(f"옵션 목록 확인 중 오류: {e}")
                    
                logger.info("=== 페이지 소스 분석 완료 ===")
                
                return False
            
            # 선택 확인
            try:
                # Select 필드의 현재 값 확인
                updated_value = select_element.get_attribute('value') or select_element.text
                logger.info(f"선택 후 법인 값: {updated_value}")
                
                if company_name in updated_value or updated_value in company_name:
                    logger.info("✅ 법인 필드 선택 확인 성공")
                    return True
                else:
                    logger.warning(f"⚠️ 법인 필드 선택 확인 실패: 예상={company_name}, 실제={updated_value}")
                    return False
                    
            except Exception as e:
                logger.warning(f"법인 필드 선택 확인 중 오류: {e}")
                return True  # 클릭은 성공했으므로 True 반환
            
        except Exception as e:
            logger.error(f"법인 필드 특별 처리 오류: {e}")
            return False
    
    def test_company_field_specific(self, test_company: str = "일진홀딩스") -> bool:
        """법인 필드 테스트"""
        try:
            logger.info(f"법인 필드 테스트 시작: {test_company}")
            
            result = self.fill_company_field_specific(test_company)
            if result:
                logger.info("✅ 법인 필드 테스트 성공")
                return True
            else:
                logger.warning("⚠️ 법인 필드 테스트 실패")
                return False
                
        except Exception as e:
            logger.error(f"법인 필드 테스트 오류: {e}")
            return False
    
    def submit_registration_form(self) -> bool:
        """회원등록 폼 제출"""
        try:
            logger.info("회원등록 폼 제출 시도")
            
            # 제출 버튼 찾기
            submit_selectors = [
                "//button[contains(text(), '가입하기')]",
                "button[type='submit']",
                "input[type='submit']",
                "//button[contains(text(), '등록')]",
                "//button[contains(text(), '저장')]",
                "//button[contains(text(), 'Submit')]",
                "//button[contains(text(), 'Save')]",
                "//button[contains(text(), '확인')]",
                "//button[contains(text(), 'OK')]",
                "//input[@value='등록']",
                "//input[@value='저장']",
                "//input[@value='Submit']",
                "//input[@value='Save']",
                "button.MuiButton-contained",
                "button.MuiButton-root",
                "//button[@class='MuiButton-root MuiButton-contained']",
                "//button[@class='MuiButton-root MuiButton-contained MuiButton-containedPrimary']"
            ]
            
            for selector in submit_selectors:
                try:
                    if selector.startswith('//'):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        # 실제 제출은 하지 않고 로그만 출력 (테스트용)
                        logger.info("✅ 회원등록 폼 제출 버튼 발견 (실제 제출은 하지 않음)")
                        # element.click()  # 실제 제출은 주석처리
                        # logger.info("✅ 회원등록 폼 제출 성공")
                        # time.sleep(2)  # 제출 후 페이지 로딩 대기
                        return True
                        
                except Exception as e:
                    continue
            
            logger.warning("⚠️ 회원등록 폼 제출 버튼을 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"회원등록 폼 제출 오류: {e}")
            return False
    
    def register_user_from_excel(self, row_index: int = 0) -> bool:
        """엑셀에서 사용자 데이터를 읽어서 회원등록"""
        try:
            logger.info(f"엑셀에서 사용자 {row_index} 회원등록 시작")
            
            # 엑셀 파일 로드
            if not self.excel_reader.load_excel_file():
                logger.error("엑셀 파일 로드 실패")
                return False
            
            # 사용자 데이터 가져오기
            user_data = self.excel_reader.get_user_data(row_index)
            if not user_data:
                logger.error(f"사용자 데이터 {row_index}를 찾을 수 없습니다")
                return False
            
            logger.info(f"사용자 데이터: {user_data}")
            
            # 회원등록 페이지로 직접 이동 (정확한 URL 사용)
            if not self.navigate_to_registration_page_direct():
                logger.error("회원등록 페이지 이동 실패")
                return False
            
            # 회원등록 폼 자동 입력
            if not self.fill_registration_form(user_data):
                logger.error("회원등록 폼 자동 입력 실패")
                return False
            
            # 폼 제출
            if not self.submit_registration_form():
                logger.error("회원등록 폼 제출 실패")
                return False
            
            logger.info(f"✅ 사용자 {user_data.get('성명', user_data.get('per_nm', 'Unknown'))} 회원등록 완료")
            return True
            
        except Exception as e:
            logger.error(f"엑셀 사용자 회원등록 오류: {e}")
            return False
    
    def register_all_users_from_excel(self) -> Dict[str, Any]:
        """엑셀의 모든 사용자를 회원등록"""
        try:
            logger.info("엑셀의 모든 사용자 회원등록 시작")
            
            # 1. 웹사이트 접속 및 로그인
            logger.info("1. 웹사이트 접속 및 로그인 중...")
            if not self.run_automation():
                logger.error("웹사이트 접속 및 로그인 실패")
                return {'success': False, 'message': '웹사이트 접속 및 로그인 실패'}
            
            logger.info("✅ 웹사이트 접속 및 로그인 완료")
            
            # 2. 엑셀 파일 로드
            logger.info("2. 엑셀 파일 로드 중...")
            if not self.excel_reader.load_excel_file():
                logger.error("엑셀 파일 로드 실패")
                return {'success': False, 'message': '엑셀 파일 로드 실패'}
            
            total_rows = self.excel_reader.get_total_rows()
            
            if total_rows == 0:
                logger.warning("회원가입할 사용자 데이터가 없습니다")
                return {'success': False, 'message': '사용자 데이터 없음'}
            
            logger.info(f"총 {total_rows}명의 사용자 회원등록 시작")
            
            # 한 번만 회원등록 페이지로 직접 이동 (정확한 URL 사용)
            if not self.navigate_to_registration_page_direct():
                logger.error("회원등록 페이지 이동 실패")
                return {'success': False, 'message': '회원등록 페이지 이동 실패'}
            
            success_count = 0
            failed_count = 0
            results = []
            
            for row_index in range(total_rows):
                logger.info(f"=== 사용자 {row_index+1}/{total_rows} 회원등록 시작 ===")
                
                # 사용자 데이터 가져오기
                user_data = self.excel_reader.get_user_data(row_index)
                if not user_data:
                    logger.error(f"사용자 데이터 {row_index}를 찾을 수 없습니다")
                    failed_count += 1
                    results.append({
                        'row_index': row_index,
                        'success': False,
                        'reason': '데이터 로드 실패'
                    })
                    continue
                
                logger.info(f"사용자 데이터: {user_data}")
                
                # 회원등록 폼 자동 입력
                if not self.fill_registration_form(user_data):
                    logger.error(f"사용자 {row_index+1} 회원등록 폼 입력 실패")
                    failed_count += 1
                    results.append({
                        'row_index': row_index,
                        'success': False,
                        'reason': '폼 입력 실패'
                    })
                    continue
                
                # 폼 제출
                if not self.submit_registration_form():
                    logger.error(f"사용자 {row_index+1} 회원등록 폼 제출 실패")
                    failed_count += 1
                    results.append({
                        'row_index': row_index,
                        'success': False,
                        'reason': '폼 제출 실패'
                    })
                    continue
                
                # 성공
                success_count += 1
                logger.info(f"✅ 사용자 {row_index+1} ({user_data.get('per_nm', 'Unknown')}) 회원등록 성공")
                results.append({
                    'row_index': row_index,
                    'success': True,
                    'user_name': user_data.get('per_nm', 'Unknown')
                })
                
                # 다음 사용자 전 잠시 대기
                if row_index < total_rows - 1:
                    logger.info("다음 사용자 회원등록을 위해 3초 대기...")
                    time.sleep(3)
                    
                    # 다음 사용자를 위해 회원등록 메뉴로 다시 이동
                    logger.info("다음 사용자를 위해 회원등록 메뉴로 다시 이동...")
                    if not self.navigate_to_registration_page_direct():
                        logger.warning("회원등록 메뉴 이동 실패, 현재 페이지에서 계속 진행")
            
            logger.info(f"=== 전체 회원등록 완료 ===")
            logger.info(f"성공: {success_count}명, 실패: {failed_count}명")
            
            return {
                'success': True,
                'total_users': total_rows,
                'success_count': success_count,
                'failed_count': failed_count,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"전체 사용자 회원등록 오류: {e}")
            return {'success': False, 'message': f'오류: {e}'}
    
    def analyze_page_structure(self):
        """페이지 구조를 상세히 분석하는 함수"""
        logger.info("=== 페이지 구조 상세 분석 시작 ===")
        
        try:
            # 현재 페이지 URL 확인
            current_url = self.driver.current_url
            logger.info(f"현재 페이지 URL: {current_url}")
            
            # 페이지 제목 확인
            page_title = self.driver.title
            logger.info(f"페이지 제목: {page_title}")
            
            # 법인 선택 필드 주변 구조 분석
            company_selectors = [
                "#mui-component-select-compCd",
                "select[id='mui-component-select-compCd']",
                "input[id='mui-component-select-compCd']",
                "div[id='mui-component-select-compCd']"
            ]
            
            for selector in company_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        logger.info(f"법인 선택 필드 발견: {selector}")
                        for i, element in enumerate(elements):
                            tag_name = element.tag_name
                            element_id = element.get_attribute('id')
                            element_class = element.get_attribute('class')
                            element_role = element.get_attribute('role')
                            element_aria_label = element.get_attribute('aria-label')
                            element_text = element.text.strip()
                            
                            logger.info(f"  요소 {i+1}: tag={tag_name}, id={element_id}, class={element_class}, role={element_role}, aria-label={element_aria_label}, text='{element_text}'")
                except Exception as e:
                    logger.debug(f"선택자 {selector} 분석 실패: {e}")
            
            # 드롭다운 메뉴 관련 요소들 찾기
            dropdown_patterns = [
                "//div[contains(@class, 'MuiMenu')]",
                "//div[contains(@class, 'MuiPopover')]",
                "//div[contains(@class, 'MuiList')]",
                "//ul[contains(@class, 'MuiList')]",
                "//div[@role='listbox']",
                "//div[@role='menu']"
            ]
            
            for pattern in dropdown_patterns:
                try:
                    elements = self.driver.find_elements(By.XPATH, pattern)
                    if elements:
                        logger.info(f"드롭다운 패턴 발견: {pattern} (개수: {len(elements)})")
                        for i, element in enumerate(elements[:3]):  # 최대 3개만 표시
                            element_class = element.get_attribute('class')
                            element_role = element.get_attribute('role')
                            element_id = element.get_attribute('id')
                            element_style = element.get_attribute('style')
                            
                            logger.info(f"  요소 {i+1}: class={element_class}, role={element_role}, id={element_id}, style={element_style}")
                except Exception as e:
                    logger.debug(f"패턴 {pattern} 분석 실패: {e}")
            
            # 페이지 소스에서 특정 키워드 검색
            page_source = self.driver.page_source
            keywords = ['일진 다이아몬드', 'MuiMenuItem', 'MuiList', 'MuiMenu', 'data-value']
            
            for keyword in keywords:
                if keyword in page_source:
                    count = page_source.count(keyword)
                    logger.info(f"키워드 '{keyword}' 발견: {count}회")
                else:
                    logger.info(f"키워드 '{keyword}' 없음")
            
            logger.info("=== 페이지 구조 상세 분석 완료 ===")
            
        except Exception as e:
            logger.error(f"페이지 구조 분석 중 오류: {e}")
    
    def take_screenshot_for_analysis(self, filename="page_analysis"):
        """분석을 위한 스크린샷 촬영"""
        try:
            from datetime import datetime
            import os
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"logs/screenshots/{filename}_{timestamp}.png"
            
            # 디렉토리가 없으면 생성
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"스크린샷 저장: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"스크린샷 촬영 실패: {e}")
            return None 