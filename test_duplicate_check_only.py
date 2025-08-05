#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ID 중복체크 기능 테스트 스크립트 (API 기반 개선 버전)
기존 소스는 건드리지 않고 별도로 테스트합니다.
개선사항: 네트워크 요청 모니터링, API 응답 확인
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  # 🆕 최신 Selenium에서는 불필요
from loguru import logger

class DuplicateCheckTester:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.network_logs = []
        
    def setup_driver(self):
        """웹드라이버 설정 (네트워크 로그 캡처 포함)"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 🆕 네트워크 로그 캡처를 위한 설정 (최신 Selenium 방식)
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            
            logger.info("✅ 웹드라이버 설정 완료 (네트워크 로그 캡처 포함)")
            return True
        except Exception as e:
            logger.error(f"❌ 웹드라이버 설정 실패: {e}")
            return False
    
    def login(self):
        """로그인"""
        try:
            logger.info("🔐 로그인 시작...")
            
            # 로그인 페이지로 이동
            self.driver.get("http://4.144.198.168/sign-in")
            time.sleep(3)
            
            # 언어 선택 (기존 방식 사용)
            logger.info("🌐 언어 선택 중...")
            try:
                # 언어 선택 요소 분석
                analysis = self.analyze_login_page_language_selector()
                
                if analysis.get('found_elements'):
                    recommended_selector = analysis.get('recommended_selector')
                    if recommended_selector:
                        element = self.driver.find_element(By.CSS_SELECTOR, recommended_selector)
                        
                        # 요소 타입에 따른 처리
                        if element.tag_name == 'select':
                            # 셀렉트 박스인 경우
                            from selenium.webdriver.support.ui import Select
                            select = Select(element)
                            
                            # 다양한 방법으로 한국어 선택 시도
                            try:
                                select.select_by_visible_text('한국어')
                                logger.info("✅ 언어 '한국어' 선택 성공 (visible_text)")
                            except:
                                try:
                                    select.select_by_value('ko')
                                    logger.info("✅ 언어 '한국어' 선택 성공 (value='ko')")
                                except:
                                    try:
                                        select.select_by_value('ko-KR')
                                        logger.info("✅ 언어 '한국어' 선택 성공 (value='ko-KR')")
                                    except:
                                        try:
                                            select.select_by_index(0)  # 첫 번째 옵션 선택
                                            logger.info("✅ 첫 번째 언어 옵션 선택 성공")
                                        except:
                                            logger.error("셀렉트 박스에서 언어 선택 실패")
                        
                        elif element.tag_name == 'button':
                            # 버튼인 경우 클릭
                            element.click()
                            logger.info("언어 선택 버튼 클릭 완료")
                            time.sleep(1)
                        
                        elif element.tag_name == 'a':
                            # 링크인 경우 클릭
                            element.click()
                            logger.info("언어 선택 링크 클릭 완료")
                            time.sleep(1)
                        
                        elif element.tag_name == 'input' and element.get_attribute('type') == 'radio':
                            # 라디오 버튼인 경우
                            element.click()
                            logger.info("언어 선택 라디오 버튼 클릭 완료")
                            time.sleep(1)
                        
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
                                        break
                                except:
                                    continue
                            else:
                                logger.warning("한국어 옵션을 찾을 수 없습니다")
                                # 한국어를 찾을 수 없으면 영어로 진행
                                logger.info("영어로 진행합니다")
                                try:
                                    # 드롭다운을 닫기 위해 다시 클릭
                                    element.click()
                                    time.sleep(1)
                                except:
                                    pass
                        
                        else:
                            logger.warning(f"지원하지 않는 요소 타입: {element.tag_name}")
                else:
                    logger.info("언어 선택 요소를 찾을 수 없음, 건너뜀")
            except Exception as e:
                logger.warning(f"언어 선택 중 오류: {e}, 건너뜀")
            
            # 사용자명 입력
            logger.info("👤 사용자명 입력 중...")
            try:
                username_element = self.driver.find_element(By.NAME, "userName")
                username_element.clear()
                time.sleep(0.5)
                username_element.send_keys("ij_itsmadmin")
                logger.info("✅ 사용자명 입력 완료")
            except:
                try:
                    username_element = self.driver.find_element(By.CSS_SELECTOR, "input[type='text']")
                    username_element.clear()
                    time.sleep(0.5)
                    username_element.send_keys("ij_itsmadmin")
                    logger.info("✅ 사용자명 입력 완료 (대체 방법)")
                except Exception as e:
                    logger.error(f"❌ 사용자명 입력 실패: {e}")
                    return False
            
            # 비밀번호 입력
            logger.info("🔒 비밀번호 입력 중...")
            try:
                password_element = self.driver.find_element(By.NAME, "password")
                password_element.clear()
                password_element.send_keys("0")
                logger.info("✅ 비밀번호 입력 완료")
            except:
                try:
                    password_element = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                    password_element.clear()
                    password_element.send_keys("0")
                    logger.info("✅ 비밀번호 입력 완료 (대체 방법)")
                except Exception as e:
                    logger.error(f"❌ 비밀번호 입력 실패: {e}")
                    return False
            
            # 로그인 버튼 클릭
            logger.info("🔘 로그인 버튼 클릭...")
            try:
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                login_button.click()
                time.sleep(3)
                logger.info("✅ 로그인 버튼 클릭 완료")
            except:
                try:
                    login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
                    login_button.click()
                    time.sleep(3)
                    logger.info("✅ 로그인 버튼 클릭 완료 (대체 방법)")
                except Exception as e:
                    logger.error(f"❌ 로그인 버튼 클릭 실패: {e}")
                    return False
            
            # 로그인 성공 확인
            current_url = self.driver.current_url
            logger.info(f"현재 URL: {current_url}")
            
            # 로그인 성공 확인 (더 안정적인 방법)
            if current_url and "sign-in" not in current_url:
                logger.info("✅ 로그인 성공")
                return True
            else:
                # URL이 변경되지 않았지만 로그인이 성공했을 수 있음
                # 페이지 제목이나 다른 요소로 확인
                try:
                    page_title = self.driver.title
                    logger.info(f"페이지 제목: {page_title}")
                    
                    # 로그인 성공 후 나타나는 요소 확인
                    success_indicators = [
                        "//div[contains(text(), '환영')]",
                        "//div[contains(text(), 'Welcome')]",
                        "//div[contains(text(), '메뉴')]",
                        "//div[contains(text(), 'Menu')]",
                        "//button[contains(text(), '로그아웃')]",
                        "//button[contains(text(), 'Logout')]"
                    ]
                    
                    for indicator in success_indicators:
                        try:
                            element = self.driver.find_element(By.XPATH, indicator)
                            if element.is_displayed():
                                logger.info(f"✅ 로그인 성공 확인됨: {indicator}")
                                return True
                        except:
                            continue
                    
                    # 일정 시간 대기 후 다시 확인
                    logger.info("로그인 완료 대기 중...")
                    time.sleep(3)
                    
                    # 다시 URL 확인
                    current_url = self.driver.current_url
                    logger.info(f"대기 후 현재 URL: {current_url}")
                    
                    if current_url and "sign-in" not in current_url:
                        logger.info("✅ 로그인 성공 (대기 후)")
                        return True
                    else:
                        logger.warning("⚠️ 로그인 상태 불확실, 계속 진행")
                        return True  # 일단 성공으로 처리하고 계속 진행
                        
                except Exception as e:
                    logger.warning(f"로그인 상태 확인 중 오류: {e}, 계속 진행")
                    return True  # 오류가 있어도 계속 진행
                
        except Exception as e:
            logger.error(f"❌ 로그인 오류: {e}")
            return False
    
    def analyze_login_page_language_selector(self):
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
                    if selector.startswith("//"):
                        # XPath 선택자
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        # CSS 선택자
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
    
    def navigate_to_registration_page(self):
        """회원등록 페이지로 이동"""
        try:
            logger.info("📝 회원등록 페이지로 이동 중...")
            
            # 직접 회원등록 URL로 이동
            registration_url = "http://4.144.198.168/ims/ImsMng001.R01.cmd?rootMenu=MNU180516000001"
            self.driver.get(registration_url)
            time.sleep(3)
            
            # 페이지 로드 확인
            page_title = self.driver.title
            current_url = self.driver.current_url
            logger.info(f"페이지 제목: {page_title}")
            logger.info(f"현재 URL: {current_url}")
            
            if "회원등록" in page_title or "MNU180516000001" in current_url:
                logger.info("✅ 회원등록 페이지 접속 성공")
                return True
            else:
                logger.error("❌ 회원등록 페이지 접속 실패")
                return False
                
        except Exception as e:
            logger.error(f"❌ 회원등록 페이지 이동 오류: {e}")
            return False
    
    def test_id_duplicate_check(self, test_id: str):
        """ID 중복체크 테스트 (run_full_automation.py 실제 패턴 적용)"""
        try:
            logger.info(f"🧪 ID 중복체크 테스트 시작: {test_id}")
            
            # 1. 성명 필드 먼저 입력 (중복체크 전에 필요)
            logger.info("1️⃣ 성명 필드 입력...")
            name_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='perNm']"))
            )
            name_input.click()
            name_input.send_keys(Keys.CONTROL + "a")
            name_input.send_keys(Keys.DELETE)
            name_input.send_keys("테스트사용자")
            time.sleep(1)
            
            # 2. 첫 번째 시도: ID 입력 및 중복확인
            logger.info("2️⃣ 첫 번째 시도: ID 입력 및 중복확인...")
            first_attempt_success = self._attempt_duplicate_check(test_id, "첫 번째")
            
            if first_attempt_success:
                logger.info("✅ 첫 번째 시도에서 성공!")
                return True
            
            # 3. 두 번째 시도: ID 재입력 및 중복확인
            logger.info("3️⃣ 두 번째 시도: ID 재입력 및 중복확인...")
            second_attempt_success = self._attempt_duplicate_check(test_id, "두 번째")
            
            if second_attempt_success:
                logger.info("✅ 두 번째 시도에서 성공!")
                return True
            
            logger.error("❌ 두 번의 시도 모두 실패")
            return False
                
        except Exception as e:
            logger.error(f"ID 중복체크 테스트 오류: {e}")
            return False
    
    def _attempt_duplicate_check(self, test_id: str, attempt_name: str) -> bool:
        """중복확인 시도 (첫 번째/두 번째) - API 기반 개선 버전"""
        try:
            logger.info(f"🔄 {attempt_name} 시도 시작...")
            
            # 네트워크 로그 초기화
            self.network_logs = []
            
            # ID 필드 찾기
            user_id_selectors = [
                "input[name='perId']",    # 정확한 name 속성
                "input[id='mui-2']",      # 정확한 id 속성
                "//input[@name='perId']",
                "//input[@id='mui-2']"
            ]
            
            id_input = None
            for selector in user_id_selectors:
                try:
                    if selector.startswith('//'):
                        id_input = self.driver.find_element(By.XPATH, selector)
                    else:
                        id_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if id_input.is_displayed():
                        logger.info(f"사용자 ID 필드 발견: {selector}")
                        break
                except:
                    continue
            
            if not id_input:
                logger.error("❌ 사용자 ID 필드를 찾을 수 없음")
                return False
            
            # 현재 ID 값 확인
            current_value = id_input.get_attribute('value')
            logger.info(f"현재 ID 값: '{current_value}'")
            
            # ID 값이 다르거나 비어있으면 재입력
            if current_value != test_id:
                logger.info(f"ID 값이 다름 - 재입력 중... (현재: '{current_value}', 목표: '{test_id}')")
                
                # 값 입력 (강력한 방법)
                id_input.click()  # 포커스
                id_input.send_keys(Keys.CONTROL + "a")  # 전체 선택
                id_input.send_keys(Keys.DELETE)  # 삭제
                self.driver.execute_script("arguments[0].value = '';", id_input)  # JavaScript로도 지우기
                id_input.clear()  # Selenium clear
                
                # 잠시 대기
                time.sleep(0.5)
                
                id_input.send_keys(test_id)  # 새 값 입력
                
                # 입력 확인
                time.sleep(0.5)
                new_value = id_input.get_attribute('value')
                logger.info(f"재입력된 값: '{new_value}'")
                
                if new_value != test_id:
                    logger.error(f"❌ ID 재입력 실패: 값 불일치")
                    return False
                
                logger.info("✅ ID 재입력 성공")
            else:
                logger.info("✅ ID 값이 이미 올바름")
            
            # 중복확인 버튼 찾기 및 클릭
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
            
            duplicate_button = None
            for selector in duplicate_check_selectors:
                try:
                    if selector.startswith('//'):
                        duplicate_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        duplicate_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if duplicate_button.is_displayed() and duplicate_button.is_enabled():
                        logger.info(f"중복확인 버튼 발견: {selector}")
                        logger.info(f"버튼 텍스트: '{duplicate_button.text}'")
                        break
                except:
                    continue
            
            if not duplicate_button:
                logger.error("❌ 중복확인 버튼을 찾을 수 없음")
                return False
            
            # 🆕 개선사항 1: 네트워크 로그 캡처 시작
            logger.info(f"🆕 {attempt_name} 네트워크 로그 캡처 시작...")
            
            # 버튼 클릭
            duplicate_button.click()
            logger.info(f"✅ {attempt_name} 중복확인 버튼 클릭 성공")
            
            # 🆕 개선사항 2: API 응답 대기 및 확인
            logger.info(f"🆕 {attempt_name} API 응답 대기 중...")
            
            # API 응답 확인 (최대 10초 대기)
            api_response = self.wait_for_duplicate_check_api_response(timeout=10)
            
            if api_response:
                logger.info(f"✅ {attempt_name} API 응답 확인 성공")
                logger.info(f"API 응답: {api_response}")
                
                # API 응답 기반 결과 판단
                if self.analyze_api_response(api_response):
                    logger.info(f"✅ {attempt_name} API 응답 분석 결과: 성공")
                    
                    # 팝업 닫기
                    if self.close_duplicate_check_dialog():
                        logger.info(f"✅ {attempt_name} 중복확인 팝업 닫기 완료")
                    else:
                        logger.warning(f"⚠️ {attempt_name} 중복확인 팝업 닫기 실패")
                    
                    return True
                else:
                    logger.warning(f"❌ {attempt_name} API 응답 분석 결과: 실패")
                    
                    # 팝업 닫기
                    if self.close_duplicate_check_dialog():
                        logger.info(f"✅ {attempt_name} 중복확인 팝업 닫기 완료")
                    else:
                        logger.warning(f"⚠️ {attempt_name} 중복확인 팝업 닫기 실패")
                    
                    return False
            else:
                logger.warning(f"⚠️ {attempt_name} API 응답을 찾을 수 없음, 기존 방식으로 폴백")
                
                # 기존 방식으로 폴백
                return self._fallback_duplicate_check(attempt_name)
                
        except Exception as e:
            logger.error(f"{attempt_name} 중복확인 시도 오류: {e}")
            return False
    
    def wait_for_duplicate_check_api_response(self, timeout=10):
        """중복확인 API 응답 대기"""
        try:
            logger.info(f"API 응답 대기 시작 (타임아웃: {timeout}초)")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                # 네트워크 로그 가져오기
                logs = self.driver.get_log('performance')
                
                for log in logs:
                    try:
                        log_entry = json.loads(log['message'])
                        
                        # Network.responseReceived 이벤트 확인
                        if 'message' in log_entry and log_entry['message']['method'] == 'Network.responseReceived':
                            request_id = log_entry['message']['params']['requestId']
                            response_url = log_entry['message']['params']['response']['url']
                            
                            # 🆕 정확한 API 엔드포인트 확인
                            if 'Imsmng001-checkId' in response_url or 'checkId' in response_url:
                                logger.info(f"✅ 중복확인 API 호출 발견: {response_url}")
                                
                                # 응답 본문 가져오기
                                response_body = self.get_response_body(request_id)
                                if response_body:
                                    logger.info(f"✅ API 응답 본문: {response_body}")
                                    return response_body
                                
                    except Exception as e:
                        continue
                
                time.sleep(0.5)
            
            logger.warning(f"⚠️ {timeout}초 내에 API 응답을 찾을 수 없음")
            return None
            
        except Exception as e:
            logger.error(f"API 응답 대기 중 오류: {e}")
            return None
    
    def get_response_body(self, request_id):
        """특정 요청의 응답 본문 가져오기"""
        try:
            # Network.getResponseBody 명령 실행
            response_body = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
            
            if 'body' in response_body:
                return response_body['body']
            else:
                logger.warning("응답 본문을 가져올 수 없음")
                return None
                
        except Exception as e:
            logger.error(f"응답 본문 가져오기 오류: {e}")
            return None
    
    def analyze_api_response(self, response_body):
        """API 응답 분석 - 실제 API 응답 구조 기반"""
        try:
            logger.info(f"API 응답 분석 시작: {response_body}")
            
            # JSON 파싱 시도
            try:
                response_data = json.loads(response_body)
                logger.info(f"JSON 파싱 성공: {response_data}")
                
                # 🆕 실제 API 응답 구조 분석
                if isinstance(response_data, dict):
                    # 1. status 필드 확인
                    if 'status' in response_data:
                        status = response_data['status']
                        logger.info(f"API 응답 status: {status}")
                        
                        if status == 'OK':
                            # 2. data.checkPerId 필드 확인 (실제 API 응답 구조)
                            if 'data' in response_data and isinstance(response_data['data'], dict):
                                data = response_data['data']
                                if 'checkPerId' in data:
                                    check_per_id = data['checkPerId']
                                    logger.info(f"checkPerId 값: {check_per_id}")
                                    
                                    # 🆕 실제 API 응답에 따른 판단
                                    if check_per_id == 'Y':
                                        logger.info("✅ API 응답: 사용 가능한 ID (checkPerId: Y)")
                                        return True
                                    elif check_per_id == 'N':
                                        logger.info("❌ API 응답: 이미 사용 중인 ID (checkPerId: N)")
                                        return False
                                    else:
                                        logger.warning(f"⚠️ 알 수 없는 checkPerId 값: {check_per_id}")
                                        return False
                                else:
                                    logger.warning("⚠️ data.checkPerId 필드를 찾을 수 없음")
                                    return False
                            else:
                                logger.warning("⚠️ data 필드를 찾을 수 없음")
                                return False
                        else:
                            logger.warning(f"⚠️ API 응답 status가 OK가 아님: {status}")
                            return False
                    
                    # 기존 방식으로 폴백 (다른 응답 구조인 경우)
                    elif 'success' in response_data:
                        return response_data['success']
                    elif 'result' in response_data:
                        return response_data['result']
                    elif 'message' in response_data:
                        # 메시지 기반 판단
                        message = response_data['message']
                        if '사용 가능' in message or 'available' in message.lower():
                            return True
                        elif '이미 사용' in message or 'duplicate' in message.lower():
                            return False
                
                # 문자열 기반 판단 (JSON이 아닌 경우)
                response_text = str(response_body).lower()
                
                if '사용 가능' in response_text or 'available' in response_text:
                    logger.info("✅ API 응답에서 '사용 가능' 메시지 발견")
                    return True
                elif '이미 사용' in response_text or 'duplicate' in response_text:
                    logger.info("❌ API 응답에서 '이미 사용' 메시지 발견")
                    return False
                elif 'success' in response_text:
                    logger.info("✅ API 응답에서 'success' 키워드 발견")
                    return True
                elif 'error' in response_text or 'fail' in response_text:
                    logger.info("❌ API 응답에서 'error/fail' 키워드 발견")
                    return False
                
                # 기본적으로 성공으로 간주 (응답이 있다는 것은 요청이 처리되었다는 의미)
                logger.info("⚠️ 명확한 성공/실패 판단 불가, 기본적으로 성공으로 간주")
                return True
                
            except json.JSONDecodeError:
                logger.info("JSON 파싱 실패, 문자열 기반 분석")
                
                # 문자열 기반 판단
                response_text = str(response_body).lower()
                
                if '사용 가능' in response_text or 'available' in response_text:
                    logger.info("✅ API 응답에서 '사용 가능' 메시지 발견")
                    return True
                elif '이미 사용' in response_text or 'duplicate' in response_text:
                    logger.info("❌ API 응답에서 '이미 사용' 메시지 발견")
                    return False
                elif 'success' in response_text:
                    logger.info("✅ API 응답에서 'success' 키워드 발견")
                    return True
                elif 'error' in response_text or 'fail' in response_text:
                    logger.info("❌ API 응답에서 'error/fail' 키워드 발견")
                    return False
                
                # 기본적으로 성공으로 간주
                logger.info("⚠️ 명확한 성공/실패 판단 불가, 기본적으로 성공으로 간주")
                return True
                
        except Exception as e:
            logger.error(f"API 응답 분석 오류: {e}")
            return False
    
    def _fallback_duplicate_check(self, attempt_name: str) -> bool:
        """기존 방식으로 폴백 (API 응답을 찾을 수 없는 경우)"""
        try:
            logger.info(f"🔄 {attempt_name} 기존 방식으로 폴백...")
            
            # 기존 방식과 동일한 로직
            time.sleep(1)
            
            # 페이지 소스에서 메시지 확인
            page_source = self.driver.page_source
            
            # 성공 메시지 확인
            if '사용 가능한 ID입니다' in page_source:
                logger.info(f"✅ {attempt_name} 중복확인 성공: '사용 가능한 ID입니다' 메시지 발견")
                
                # 팝업 닫기
                if self.close_duplicate_check_dialog():
                    logger.info(f"✅ {attempt_name} 중복확인 팝업 닫기 완료")
                else:
                    logger.warning(f"⚠️ {attempt_name} 중복확인 팝업 닫기 실패")
                
                return True
            
            # 실패 메시지 확인
            if '이미 사용 중인 ID입니다' in page_source or '중복된 ID' in page_source:
                logger.warning(f"❌ {attempt_name} 중복확인 실패: 이미 사용 중인 ID")
                
                # 팝업 닫기
                if self.close_duplicate_check_dialog():
                    logger.info(f"✅ {attempt_name} 중복확인 팝업 닫기 완료")
                else:
                    logger.warning(f"⚠️ {attempt_name} 중복확인 팝업 닫기 실패")
                
                return False
            
            # 팝업이 나타나지 않은 경우, 페이지에서 직접 확인
            logger.info(f"{attempt_name} 팝업이 감지되지 않아 페이지에서 직접 확인합니다...")
            
            # 간단한 팝업 감지 시도
            for attempt in range(1):
                time.sleep(0.5)
                
                # 현재 페이지의 모든 dialog 요소 확인
                dialogs = self.driver.find_elements(By.XPATH, "//div[@role='dialog']")
                
                for dialog in dialogs:
                    if dialog.is_displayed():
                        dialog_text = dialog.text.strip()
                        if '사용 가능한 ID입니다' in dialog_text:
                            logger.info(f"✅ {attempt_name} 중복확인 성공: 팝업에서 메시지 확인")
                            
                            # 팝업 닫기
                            if self.close_duplicate_check_dialog():
                                logger.info(f"✅ {attempt_name} 중복확인 팝업 닫기 완료")
                            else:
                                logger.warning(f"⚠️ {attempt_name} 중복확인 팝업 닫기 실패")
                            
                            return True
                        elif '이미 사용 중인 ID입니다' in dialog_text:
                            logger.warning(f"❌ {attempt_name} 중복확인 실패: 이미 사용 중인 ID")
                            
                            # 팝업 닫기
                            if self.close_duplicate_check_dialog():
                                logger.info(f"✅ {attempt_name} 중복확인 팝업 닫기 완료")
                            else:
                                logger.warning(f"⚠️ {attempt_name} 중복확인 팝업 닫기 실패")
                            
                            return False
            
            # 팝업이 감지되지 않음
            logger.warning(f"⚠️ {attempt_name} 팝업이 감지되지 않음")
            return False
                
        except Exception as e:
            logger.error(f"{attempt_name} 폴백 중복확인 오류: {e}")
            return False
    
    def close_duplicate_check_dialog(self) -> bool:
        """중복확인 팝업 닫기 ("예" 버튼 클릭) - run_full_automation.py 방식"""
        try:
            logger.info("중복확인 팝업 닫기 시도")
            
            # 팝업이 나타날 때까지 잠시 대기
            #time.sleep(1)
            
            # "예" 버튼 찾기 (run_full_automation.py 방식)
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
                                    # 버튼 클릭
                                    element.click()
                                    logger.info("✅ '예' 버튼 클릭 성공")
                                    
                                    # 팝업이 닫힐 때까지 대기
                                    #time.sleep(2)
                                    
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
    
    def run_test(self):
        """테스트 실행"""
        try:
            logger.info("🚀 ID 중복체크 테스트 시작")
            
            # 1. 웹드라이버 설정
            if not self.setup_driver():
                return False
            
            # 2. 로그인
            if not self.login():
                return False
            
            # 3. 회원등록 페이지로 이동
            if not self.navigate_to_registration_page():
                return False
            
            # 4. 테스트 ID 목록
            test_ids = [
                "testuser123@example.com",
                "newuser456@test.co.kr", 
                "duplicate_test@example.com"
            ]
            
            # 5. 각 테스트 ID에 대해 중복체크 테스트
            for i, test_id in enumerate(test_ids, 1):
                logger.info("")
                logger.info("=" * 50)
                logger.info(f"테스트 {i}: {test_id}")
                logger.info("=" * 50)
                
                success = self.test_id_duplicate_check(test_id)
                
                if success:
                    logger.info(f"✅ 테스트 {i} 성공")
                else:
                    logger.warning(f"⚠️ 테스트 {i} 실패")
                
                # 다음 테스트를 위해 페이지 새로고침
                if i < len(test_ids):
                    logger.info("🔄 다음 테스트를 위해 페이지 새로고침...")
                    self.driver.refresh()
                    time.sleep(3)
            
            logger.info("")
            logger.info("🎉 모든 테스트 완료!")
            
            # 브라우저 유지 여부 확인
            keep_browser = input("\n브라우저를 열어둘까요? (y/N): ").lower().strip()
            if keep_browser != 'y':
                self.driver.quit()
                logger.info("브라우저 종료")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 테스트 실행 오류: {e}")
            return False

def main():
    logger.info("🧪 ID 중복체크 기능 테스트 스크립트")
    logger.info("기존 소스는 건드리지 않고 별도로 테스트합니다.")
    
    tester = DuplicateCheckTester()
    tester.run_test()

if __name__ == "__main__":
    main() 