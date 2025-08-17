"""
일진홀딩스 웹사이트 자동화 플러그인
"""

import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement

from src.core.base_automation import BaseAutomation
from src.core.web_driver_manager import WebDriverManager
from .selectors import IljinSelectors
from loguru import logger


class IljinHoldingsAutomation(BaseAutomation):
    """일진홀딩스 웹사이트 자동화 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.selectors = IljinSelectors()
        
    def setup_driver(self) -> None:
        """웹드라이버 설정"""
        try:
            self.driver = WebDriverManager.create_driver(self.config)
            self.wait = WebDriverManager.create_wait(self.driver, self.config.get('browser.timeout', 10))
            logger.info("일진홀딩스 웹드라이버 설정 완료")
        except Exception as e:
            logger.error(f"웹드라이버 설정 오류: {e}")
            raise
            
    def navigate_to_website(self) -> bool:
        """웹사이트 접속"""
        try:
            url = self.config.get('website.url', self.selectors.MAIN_PAGE)
            logger.info(f"일진홀딩스 웹사이트 접속 중: {url}")
            
            self.driver.get(url)
            time.sleep(3)
            
            logger.info("일진홀딩스 웹사이트 접속 완료")
            return True
            
        except Exception as e:
            logger.error(f"웹사이트 접속 오류: {e}")
            return False
            
    def login(self, credentials: Dict[str, str]) -> bool:
        """로그인 (일진홀딩스는 로그인이 필요하지 않음)"""
        logger.info("일진홀딩스는 로그인이 필요하지 않습니다")
        return True
        
    def select_iljin_holdings(self) -> bool:
        """일진홀딩스 선택"""
        try:
            logger.info("일진홀딩스 선택 중...")
            
            # 일진홀딩스 링크 찾기 및 클릭
            iljin_link = self.driver.find_element(By.CSS_SELECTOR, self.selectors.ILJIN_HOLDINGS_LINK)
            iljin_link.click()
            
            time.sleep(3)
            logger.info("일진홀딩스 선택 완료")
            return True
            
        except Exception as e:
            logger.error(f"일진홀딩스 선택 오류: {e}")
            return False
            
    def select_visit_request(self) -> bool:
        """방문신청하기 선택"""
        try:
            logger.info("방문신청하기 선택 중...")
            
            # 방문신청하기 링크 찾기 및 클릭
            visit_link = self.driver.find_element(By.CSS_SELECTOR, self.selectors.VISIT_REQUEST_LINK)
            visit_link.click()
            
            time.sleep(3)
            logger.info("방문신청하기 선택 완료")
            return True
            
        except Exception as e:
            logger.error(f"방문신청하기 선택 오류: {e}")
            return False
            
    def agree_to_terms(self) -> bool:
        """방문신청약관 동의"""
        try:
            logger.info("방문신청약관 동의 중...")
            
            # 페이지 로딩 대기
            time.sleep(3)
            
            # Vue.js 앱이 완전히 로드될 때까지 대기
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)
            
            # 이전 프로젝트에서 성공한 방법 사용
            self.check_vue_checkboxes()
            
            # "동의합니다" 버튼 클릭
            self.click_agree_button()
            
            logger.info("방문신청약관 동의 완료")
            return True
            
        except Exception as e:
            logger.error(f"약관 동의 오류: {e}")
            return False
            
    def check_vue_checkboxes(self):
        """Vue.js 체크박스 체크 (이전 프로젝트에서 성공한 방법)"""
        try:
            logger.info("Vue.js 체크박스 체크 시작...")
            
            # 방법 1: Vue.js 앱 인스턴스에 직접 접근
            js_code_1 = """
            try {
                // Vue.js 앱 찾기
                var app = null;
                
                // Vue DevTools를 통한 접근
                if (window.__VUE_DEVTOOLS_GLOBAL_HOOK__ && window.__VUE_DEVTOOLS_GLOBAL_HOOK__.apps) {
                    app = window.__VUE_DEVTOOLS_GLOBAL_HOOK__.apps[0];
                }
                
                // data-v- 속성을 가진 요소에서 찾기
                if (!app) {
                    var vueElements = document.querySelectorAll('[data-v-]');
                    for (var i = 0; i < vueElements.length; i++) {
                        if (vueElements[i].__vue__) {
                            app = vueElements[i].__vue__;
                            break;
                        }
                    }
                }
                
                // 모든 요소에서 Vue 인스턴스 찾기
                if (!app) {
                    var allElements = document.querySelectorAll('*');
                    for (var i = 0; i < allElements.length; i++) {
                        if (allElements[i].__vue__) {
                            app = allElements[i].__vue__;
                            break;
                        }
                    }
                }
                
                if (app) {
                    // Vue.js 데이터 직접 수정
                    if (app.agreeChk_1 !== undefined) {
                        app.agreeChk_1 = true;
                    }
                    if (app.agreeChk_2 !== undefined) {
                        app.agreeChk_2 = true;
                    }
                    
                    // Vue.js 강제 업데이트
                    if (app.$forceUpdate) {
                        app.$forceUpdate();
                    }
                    
                    return {
                        success: true,
                        message: 'Vue.js 데이터 수정 완료'
                    };
                } else {
                    return {
                        success: false,
                        message: 'Vue.js 앱을 찾을 수 없습니다'
                    };
                }
            } catch (error) {
                return {
                    success: false,
                    message: 'Vue.js 처리 중 오류: ' + error.message
                };
            }
            """
            
            result_1 = self.driver.execute_script(js_code_1)
            logger.info(f"Vue.js 앱 처리 결과: {result_1}")
            
            # 방법 2: DOM 요소 직접 조작 (성공한 방법)
            js_code_2 = """
            try {
                var successCount = 0;
                
                // agreeChk_1 처리
                var checkbox1 = document.getElementById('agreeChk_1');
                if (checkbox1) {
                    // 체크박스 체크
                    checkbox1.checked = true;
                    
                    // 모든 가능한 이벤트 발생
                    var events = ['change', 'input', 'click', 'focus', 'blur'];
                    events.forEach(function(eventType) {
                        var event = new Event(eventType, { bubbles: true, cancelable: true });
                        checkbox1.dispatchEvent(event);
                    });
                    
                    successCount++;
                }
                
                // agreeChk_2 처리
                var checkbox2 = document.getElementById('agreeChk_2');
                if (checkbox2) {
                    // 체크박스 체크
                    checkbox2.checked = true;
                    
                    // 모든 가능한 이벤트 발생
                    var events = ['change', 'input', 'click', 'focus', 'blur'];
                    events.forEach(function(eventType) {
                        var event = new Event(eventType, { bubbles: true, cancelable: true });
                        checkbox2.dispatchEvent(event);
                    });
                    
                    successCount++;
                }
                
                return {
                    success: successCount > 0,
                    message: 'DOM 요소 처리 완료',
                    successCount: successCount
                };
            } catch (error) {
                return {
                    success: false,
                    message: 'DOM 처리 중 오류: ' + error.message
                };
            }
            """
            
            result_2 = self.driver.execute_script(js_code_2)
            logger.info(f"DOM 요소 처리 결과: {result_2}")
            
            # 방법 3: MutationObserver를 사용한 강제 업데이트 (성공한 방법)
            js_code_3 = """
            try {
                // MutationObserver를 사용하여 DOM 변경 감지 및 강제 업데이트
                var observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        if (mutation.type === 'attributes' && mutation.attributeName === 'checked') {
                            console.log('체크박스 상태 변경 감지됨');
                        }
                    });
                });
                
                // 체크박스들 관찰 시작
                var checkboxes = document.querySelectorAll('input[type="checkbox"]');
                checkboxes.forEach(function(checkbox) {
                    observer.observe(checkbox, {
                        attributes: true,
                        attributeFilter: ['checked']
                    });
                });
                
                // 체크박스 강제 체크
                var checkbox1 = document.getElementById('agreeChk_1');
                var checkbox2 = document.getElementById('agreeChk_2');
                
                if (checkbox1) {
                    checkbox1.checked = true;
                    checkbox1.setAttribute('checked', 'checked');
                    checkbox1.dispatchEvent(new Event('change', { bubbles: true }));
                }
                
                if (checkbox2) {
                    checkbox2.checked = true;
                    checkbox2.setAttribute('checked', 'checked');
                    checkbox2.dispatchEvent(new Event('change', { bubbles: true }));
                }
                
                // 잠시 대기 후 observer 해제
                setTimeout(function() {
                    observer.disconnect();
                }, 1000);
                
                return {
                    success: true,
                    message: 'MutationObserver 처리 완료'
                };
            } catch (error) {
                return {
                    success: false,
                    message: 'MutationObserver 처리 중 오류: ' + error.message
                };
            }
            """
            
            result_3 = self.driver.execute_script(js_code_3)
            logger.info(f"MutationObserver 처리 결과: {result_3}")
            
            # 체크박스 상태 확인
            self.verify_checkbox_status()
            
        except Exception as e:
            logger.error(f"Vue.js 체크박스 체크 오류: {e}")
            
    def verify_checkbox_status(self):
        """체크박스 상태 확인"""
        try:
            logger.info("체크박스 상태 확인 중...")
            
            for checkbox_id in ['agreeChk_1', 'agreeChk_2']:
                try:
                    checkbox = self.driver.find_element(By.ID, checkbox_id)
                    is_checked = checkbox.is_selected()
                    logger.info(f"체크박스 {checkbox_id}: {'체크됨' if is_checked else '체크되지 않음'}")
                except:
                    logger.warning(f"체크박스 {checkbox_id}를 찾을 수 없습니다")
                    
        except Exception as e:
            logger.error(f"체크박스 상태 확인 오류: {e}")
            
    def click_agree_button(self) -> bool:
        """동의합니다 버튼 클릭"""
        try:
            logger.info("동의합니다 버튼 클릭 중...")
            
            # 여러 방법으로 버튼 찾기
            button_selectors = [
                self.selectors.AGREE_BUTTON,
                "button:contains('동의합니다')",
                "input[value='동의합니다']",
                ".agree-btn",
                "#agreeBtn"
            ]
            
            for selector in button_selectors:
                try:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    button.click()
                    logger.info("동의합니다 버튼 클릭 완료")
                    time.sleep(2)
                    return True
                except Exception as e:
                    continue
                    
            # XPath로 시도
            xpath_selectors = [
                "//button[contains(text(), '동의합니다')]",
                "//input[@value='동의합니다']",
                "//button[text()='동의합니다']"
            ]
            
            for xpath in xpath_selectors:
                try:
                    button = self.driver.find_element(By.XPATH, xpath)
                    button.click()
                    logger.info("동의합니다 버튼 클릭 완료 (XPath)")
                    time.sleep(2)
                    return True
                except Exception as e:
                    continue
                    
            logger.error("동의합니다 버튼을 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"동의합니다 버튼 클릭 오류: {e}")
            return False
            
    def fill_form(self, data: Dict[str, Any]) -> bool:
        """방문신청 폼 작성"""
        try:
            logger.info("방문신청 폼 작성 중...")
            
            # 페이지 로딩 대기 (더 긴 시간)
            time.sleep(5)
            
            # 현재 URL 확인
            current_url = self.driver.current_url
            logger.info(f"현재 페이지 URL: {current_url}")
            
            # 페이지 제목 확인
            page_title = self.driver.title
            logger.info(f"페이지 제목: {page_title}")
            
            # 페이지 소스 일부 출력 (디버깅용)
            page_source = self.driver.page_source[:1000]
            logger.info(f"페이지 소스 일부: {page_source}")
            
            # 1단계: 방문사업장 선택
            if '방문사업장' in data and data['방문사업장']:
                self.select_visit_location(data['방문사업장'])
                time.sleep(1)
            
            # 2단계: 피방문자 연락처 입력
            contact_key = None
            for key in data.keys():
                if '피방문자 연락처' in key:
                    contact_key = key
                    break
            
            if contact_key and data[contact_key]:
                logger.info(f"피방문자 연락처 데이터 확인: {data[contact_key]}")
                self.fill_contact_number(data[contact_key])
                time.sleep(1)
            else:
                logger.warning("피방문자 연락처 데이터가 없습니다")
            
            # 3단계: 피방문자 입력
            if '피방문자' in data and data['피방문자']:
                logger.info(f"피방문자 데이터 확인: {data['피방문자']}")
                self.fill_visit_person(data['피방문자'])
                time.sleep(1)
            else:
                logger.warning("피방문자 데이터가 없습니다")
            
            # 4단계: 피방문자 정보 확인 버튼 클릭
            logger.info("피방문자 정보 입력 완료, 확인 버튼 클릭 중...")
            if not self.click_confirm_button():
                logger.error("피방문자 정보 확인 버튼 클릭 실패")
                return False
            time.sleep(2)  # 정보 확인 페이지 로딩 대기
            
            # 5단계: 신청자 입력
            if '신청자' in data and data['신청자']:
                logger.info(f"신청자 데이터 확인: {data['신청자']}")
                self.fill_applicant(data['신청자'])
                time.sleep(1)
            else:
                logger.warning("신청자 데이터가 없습니다")
            
            # 6단계: 신청자 연락처 입력
            if '연락처' in data and data['연락처']:
                logger.info(f"신청자 연락처 데이터 확인: {data['연락처']}")
                self.fill_applicant_contact(data['연락처'])
                time.sleep(1)
            else:
                logger.warning("신청자 연락처 데이터가 없습니다")
            
            # 7단계: 방문객으로 추가 체크박스 체크 제거 (신청자 비교 로직 단순화)
            # logger.info("방문객으로 추가 체크박스 체크 중...")
            # if not self.check_visitor_add_checkbox():
            #     logger.warning("방문객으로 추가 체크박스 체크 실패")
            # else:
            #     logger.info("방문객으로 추가 체크박스 체크 완료")
            # time.sleep(1)
            
            # 8단계: 소속회사 입력
            if '소속회사' in data and data['소속회사']:
                logger.info(f"소속회사 데이터 확인: {data['소속회사']}")
                self.fill_company(data['소속회사'])
                time.sleep(1)
            else:
                logger.warning("소속회사 데이터가 없습니다")
            
            # 9단계: 회사주소 입력
            if '회사주소' in data and data['회사주소']:
                logger.info(f"회사주소 데이터 확인: {data['회사주소']}")
                self.fill_company_address(data['회사주소'])
                time.sleep(1)
            else:
                logger.warning("회사주소 데이터가 없습니다")
            
            # 10단계: 방문기간 입력
            if '방문기간' in data and data['방문기간']:
                logger.info(f"방문기간 데이터 확인: {data['방문기간']}")
                self.fill_visit_dates(data['방문기간'])
                time.sleep(1)
            else:
                logger.warning("방문기간 데이터가 없습니다")
            
            # 11단계: 내용 입력
            if '내용' in data and data['내용']:
                logger.info(f"내용 데이터 확인: {data['내용']}")
                self.fill_content(data['내용'])
                time.sleep(1)
            else:
                logger.warning("내용 데이터가 없습니다")
            
            logger.info("방문신청 폼 작성 완료")
            return True
            
        except Exception as e:
            logger.error(f"방문신청 폼 작성 중 오류: {e}")
            return False
            
    def select_visit_location(self, location_name: str) -> bool:
        """방문사업장 선택"""
        try:
            logger.info(f"방문사업장 선택 중: {location_name}")
            
            # 여러 방법으로 select 요소 찾기
            select_selectors = [
                "select_0",  # 기존 방법
                "select[name*='select']",  # name에 'select'가 포함된 요소
                "select",  # 모든 select 요소
                "select[data-v-*]",  # Vue.js data-v- 속성이 있는 select
                "//select[contains(@class, 'form-control')]",  # XPath
                "//select[contains(@class, 'select')]",  # XPath
            ]
            
            select_element = None
            
            # 1. name 속성으로 찾기
            for selector in select_selectors:
                try:
                    if selector.startswith("//"):
                        # XPath 사용
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        # CSS 선택자 사용
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if element.tag_name == "select":
                            # 옵션 확인
                            options = element.find_elements(By.TAG_NAME, "option")
                            option_texts = [opt.text.strip() for opt in options]
                            
                            if "마곡빌딩(홀딩스)" in option_texts:
                                select_element = element
                                logger.info(f"방문사업장 select 요소 찾음: {selector}")
                                break
                    
                    if select_element:
                        break
                        
                except Exception as e:
                    logger.warning(f"선택자 {selector}로 찾기 실패: {str(e)}")
                    continue
            
            if not select_element:
                # 2. 모든 select 요소를 찾아서 확인
                try:
                    all_selects = self.driver.find_elements(By.TAG_NAME, "select")
                    logger.info(f"발견된 select 요소 수: {len(all_selects)}")
                    
                    for i, select in enumerate(all_selects):
                        try:
                            options = select.find_elements(By.TAG_NAME, "option")
                            option_texts = [opt.text.strip() for opt in options]
                            
                            logger.info(f"Select {i+1} 옵션들: {option_texts}")
                            
                            if "마곡빌딩(홀딩스)" in option_texts:
                                select_element = select
                                logger.info(f"방문사업장 select 요소 찾음: Select {i+1}")
                                break
                        except:
                            continue
            
                except Exception as e:
                    logger.error(f"모든 select 요소 검색 실패: {str(e)}")
            
            if select_element:
                # select 요소가 보이도록 스크롤
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_element)
                time.sleep(1)
                
                # 방법 1: value로 선택 (B1)
                try:
                    select = Select(select_element)
                    
                    if location_name == "마곡빌딩(홀딩스)":
                        select.select_by_value("B1")
                        logger.info("방문사업장 '마곡빌딩(홀딩스)' value 'B1'로 선택 완료")
                        return True
                except Exception as e:
                    logger.warning(f"value로 선택 실패: {str(e)}")
                
                # 방법 2: 텍스트로 선택
                try:
                    select = Select(select_element)
                    select.select_by_visible_text(location_name)
                    logger.info(f"방문사업장 '{location_name}' 텍스트로 선택 완료")
                    return True
                except Exception as e:
                    logger.error(f"텍스트로 선택 실패: {str(e)}")
                    return False
            else:
                logger.error("방문사업장 select 요소를 찾을 수 없습니다")
                return False
                
        except Exception as e:
            logger.error(f"방문사업장 선택 오류: {str(e)}")
            return False
            
    def fill_contact_number(self, phone_number: str) -> bool:
        """피방문자 연락처 입력"""
        try:
            logger.info(f"피방문자 연락처 입력 중: {phone_number}")
            
            # 휴대폰 번호를 하이픈으로 분리
            if '-' not in phone_number:
                logger.error(f"하이픈이 포함되지 않은 휴대폰 번호: {phone_number}")
                return False
                
            parts = phone_number.split('-')
            if len(parts) != 3:
                logger.error(f"휴대폰 번호 형식이 올바르지 않습니다: {phone_number}")
                return False
                
            first_part = parts[0]   # 010
            second_part = parts[1]  # 1234
            third_part = parts[2]   # 5678
            
            logger.info(f"분리된 번호: {first_part}-{second_part}-{third_part}")
            
            # 첫 번째 텍스트 박스 (두 번째 부분 입력)
            first_input = self.find_input_element(0)
            if first_input:
                first_input.clear()
                time.sleep(0.5)
                first_input.send_keys(second_part)
                logger.info(f"첫 번째 텍스트 박스에 '{second_part}' 입력 완료")
            else:
                logger.error("첫 번째 텍스트 박스를 찾을 수 없습니다")
            
            # 두 번째 텍스트 박스 (세 번째 부분 입력)
            second_input = self.find_input_element(1)
            if second_input:
                second_input.clear()
                time.sleep(0.5)
                second_input.send_keys(third_part)
                logger.info(f"두 번째 텍스트 박스에 '{third_part}' 입력 완료")
            else:
                logger.error("두 번째 텍스트 박스를 찾을 수 없습니다")
            
            logger.info("피방문자 연락처 입력 완료")
            return True
            
        except Exception as e:
            logger.error(f"피방문자 연락처 입력 중 오류: {e}")
            return False
            
    def fill_visit_person(self, person_name: str) -> bool:
        """피방문자 입력"""
        try:
            logger.info(f"피방문자 입력 중: {person_name}")
            
            # 세 번째 텍스트 박스에 입력
            third_input = self.find_input_element(2)  # 인덱스 2 (세 번째)
            if third_input:
                third_input.clear()
                time.sleep(0.5)
                third_input.send_keys(person_name)
                logger.info(f"세 번째 텍스트 박스에 피방문자 '{person_name}' 입력 완료")
                return True
            else:
                logger.error("세 번째 텍스트 박스를 찾을 수 없습니다")
                return False
                
        except Exception as e:
            logger.error(f"피방문자 입력 중 오류: {e}")
            return False
            
    def fill_applicant(self, applicant_name: str) -> bool:
        """신청자 입력"""
        try:
            logger.info(f"신청자 입력 중: {applicant_name}")
            
            # 네 번째 텍스트 박스에 입력
            fourth_input = self.find_input_element(3)  # 인덱스 3 (네 번째)
            if fourth_input:
                fourth_input.clear()
                time.sleep(0.5)
                fourth_input.send_keys(applicant_name)
                logger.info(f"네 번째 텍스트 박스에 신청자 '{applicant_name}' 입력 완료")
                return True
            else:
                logger.error("네 번째 텍스트 박스를 찾을 수 없습니다")
                return False
                
        except Exception as e:
            logger.error(f"신청자 입력 중 오류: {e}")
            return False
            
    def fill_applicant_contact(self, phone_number: str) -> bool:
        """신청자 연락처 입력"""
        try:
            logger.info(f"신청자 연락처 입력 중: {phone_number}")
            
            # 휴대폰 번호를 하이픈으로 분리
            if '-' not in phone_number:
                logger.error(f"하이픈이 포함되지 않은 휴대폰 번호: {phone_number}")
                return False
                
            parts = phone_number.split('-')
            if len(parts) != 3:
                logger.error(f"휴대폰 번호 형식이 올바르지 않습니다: {phone_number}")
                return False
                
            first_part = parts[0]   # 010
            second_part = parts[1]  # 1234
            third_part = parts[2]   # 5678
            
            logger.info(f"분리된 번호: {first_part}-{second_part}-{third_part}")
            
            # 다섯 번째 텍스트 박스 (두 번째 부분 입력)
            fifth_input = self.find_input_element(4)
            if fifth_input:
                fifth_input.clear()
                time.sleep(0.5)
                fifth_input.send_keys(second_part)
                logger.info(f"다섯 번째 텍스트 박스에 '{second_part}' 입력 완료")
            else:
                logger.error("다섯 번째 텍스트 박스를 찾을 수 없습니다")
            
            # 여섯 번째 텍스트 박스 (세 번째 부분 입력)
            sixth_input = self.find_input_element(5)
            if sixth_input:
                sixth_input.clear()
                time.sleep(0.5)
                sixth_input.send_keys(third_part)
                logger.info(f"여섯 번째 텍스트 박스에 '{third_part}' 입력 완료")
            else:
                logger.error("여섯 번째 텍스트 박스를 찾을 수 없습니다")
            
            logger.info("신청자 연락처 입력 완료")
            return True
            
        except Exception as e:
            logger.error(f"신청자 연락처 입력 중 오류: {e}")
            return False
            
    def check_visitor_add_checkbox(self) -> bool:
        """방문객으로 추가 체크박스 체크"""
        try:
            logger.info("방문객으로 추가 체크박스 체크 시작...")
            
            # 여러 방법으로 체크박스 찾기 및 체크
            checkbox_selectors = [
                "input[id='visitorAdd']",
                "input[type='checkbox'][id='visitorAdd']",
                "#visitorAdd",
                "input[data-v-*][id='visitorAdd']"
            ]
            
            label_selectors = [
                "label[for='visitorAdd']",
                "label[for='visitorAdd']:contains('방문객으로 추가')",
                "//label[@for='visitorAdd']",
                "//label[contains(text(), '방문객으로 추가')]"
            ]
            
            # 방법 1: 직접 체크박스 클릭 시도
            for selector in checkbox_selectors:
                try:
                    checkbox = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if not checkbox.is_selected():
                        checkbox.click()
                        logger.info(f"체크박스 직접 클릭 성공: {selector}")
                        time.sleep(1)
                        return True
                    else:
                        logger.info("체크박스가 이미 체크되어 있습니다")
                        return True
                except Exception as e:
                    logger.warning(f"체크박스 직접 클릭 실패: {selector} - {str(e)}")
                    continue
            
            # 방법 2: label 클릭 시도
            for selector in label_selectors:
                try:
                    if selector.startswith("//"):
                        # XPath 사용
                        label = self.driver.find_element(By.XPATH, selector)
                    else:
                        # CSS 선택자 사용
                        label = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    label.click()
                    logger.info(f"label 클릭 성공: {selector}")
                    time.sleep(1)
                    return True
                except Exception as e:
                    logger.warning(f"label 클릭 실패: {selector} - {str(e)}")
                    continue
            
            # 방법 3: JavaScript로 체크박스 체크
            try:
                script = """
                var checkbox = document.getElementById('visitorAdd');
                if (checkbox) {
                    checkbox.checked = true;
                    checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                    return true;
                }
                return false;
                """
                result = self.driver.execute_script(script)
                if result:
                    logger.info("JavaScript로 체크박스 체크 성공")
                    time.sleep(1)
                    return True
            except Exception as e:
                logger.warning(f"JavaScript 체크 실패: {str(e)}")
            
            # 방법 4: Vue.js 데이터 직접 수정
            try:
                script = """
                // Vue.js 컴포넌트에서 데이터 직접 수정
                var app = document.querySelector('[data-v-bb30b12c]') || 
                         document.querySelector('[data-v-*]') ||
                         document.querySelector('body');
                
                if (app && app.__vue__) {
                    // Vue 인스턴스에서 데이터 수정
                    if (app.__vue__.$data) {
                        app.__vue__.$data.visitorAdd = true;
                        return 'Vue data modified';
                    }
                }
                return 'Vue instance not found';
                """
                result = self.driver.execute_script(script)
                logger.info(f"Vue.js 데이터 수정 결과: {result}")
                time.sleep(1)
                return True
            except Exception as e:
                logger.warning(f"Vue.js 데이터 수정 실패: {str(e)}")
            
            logger.error("방문객으로 추가 체크박스를 찾을 수 없거나 체크할 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"방문객으로 추가 체크박스 체크 중 오류: {str(e)}")
            return False
            
    def fill_company(self, company_name: str) -> bool:
        """소속회사 입력"""
        try:
            logger.info(f"소속회사 입력 중: {company_name}")
            
            # 7번째 텍스트 박스에 입력
            seventh_input = self.find_input_element(6)  # 인덱스 6 (7번째)
            if seventh_input:
                seventh_input.clear()
                time.sleep(0.5)
                seventh_input.send_keys(company_name)
                logger.info(f"7번째 텍스트 박스에 소속회사 '{company_name}' 입력 완료")
                return True
            else:
                logger.error("7번째 텍스트 박스를 찾을 수 없습니다")
                return False
                
        except Exception as e:
            logger.error(f"소속회사 입력 중 오류: {e}")
            return False
            
    def fill_company_address(self, address: str) -> bool:
        """회사주소 입력"""
        try:
            logger.info(f"회사주소 입력 중: {address}")
            
            # 8번째 텍스트 박스에 입력
            eighth_input = self.find_input_element(7)  # 인덱스 7 (8번째)
            if eighth_input:
                eighth_input.clear()
                time.sleep(0.5)
                eighth_input.send_keys(address)
                logger.info(f"8번째 텍스트 박스에 회사주소 '{address}' 입력 완료")
                return True
            else:
                logger.error("8번째 텍스트 박스를 찾을 수 없습니다")
                return False
                
        except Exception as e:
            logger.error(f"회사주소 입력 중 오류: {e}")
            return False
            
    def fill_visit_dates(self, visit_date: str) -> bool:
        """방문기간 입력 (시작일과 종료일)"""
        try:
            logger.info(f"방문기간 입력 중: {visit_date}")
            
            # 날짜 파싱
            try:
                if isinstance(visit_date, str):
                    # 문자열인 경우 파싱
                    start_date = datetime.strptime(visit_date, '%Y-%m-%d %H:%M:%S')
                else:
                    # Timestamp 객체인 경우
                    start_date = visit_date
                
                # 시작일을 YYYY-MM-DD 형식으로 변환
                start_date_str = start_date.strftime('%Y-%m-%d')
                
                # 종료일 계산 (시작일 + 4일)
                end_date = start_date + timedelta(days=4)
                end_date_str = end_date.strftime('%Y-%m-%d')
                
                logger.info(f"시작일: {start_date_str}, 종료일: {end_date_str}")
                
            except Exception as e:
                logger.error(f"날짜 파싱 오류: {e}")
                return False
            
            # 방문기간 입력 필드를 정확히 찾기
            if not self._fill_visit_dates_specific(start_date_str, end_date_str):
                return False
                
            return True
                
        except Exception as e:
            logger.error(f"방문기간 입력 중 오류: {e}")
            return False
            
    def _fill_visit_dates_specific(self, start_date: str, end_date: str) -> bool:
        """방문기간 입력 필드를 정확히 찾아서 입력"""
        try:
            # 방문기간 관련 선택자들 (우선순위 순)
            date_selectors = [
                # 1. 방문기간 관련 텍스트가 있는 행에서 찾기
                "//td[contains(text(), '방문기간')]/following-sibling::td//input[@type='text']",
                "//td[contains(text(), '방문기간')]/following-sibling::td//input",
                # 2. 날짜 입력 필드 찾기
                "//input[@type='text'][contains(@placeholder, '날짜')]",
                "//input[@type='text'][contains(@placeholder, '기간')]",
                # 3. 일반적인 인덱스 기반 (기존 방식)
                "(//input[@type='text'])[8]",  # 시작일
                "(//input[@type='text'])[9]",  # 종료일
                # 4. 모든 텍스트 입력 필드
                "//input[@type='text']"
            ]
            
            start_input = None
            end_input = None
            
            # 시작일 입력 필드 찾기
            for selector in date_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if len(elements) >= 2:  # 최소 2개 이상 있어야 시작일/종료일
                        # 첫 번째 요소를 시작일로, 두 번째 요소를 종료일로
                        start_input = elements[0]
                        end_input = elements[1]
                        logger.info(f"방문기간 입력 필드 찾음: {selector}")
                        break
                except Exception as e:
                    continue
            
            if not start_input or not end_input:
                logger.error("방문기간 입력 필드를 찾을 수 없습니다")
                return False
            
            # 시작일 입력
            if self._input_to_element(start_input, start_date, "시작일"):
                logger.info(f"시작일 '{start_date}' 입력 완료")
            else:
                logger.error("시작일 입력 실패")
                return False
            
            # 종료일 입력
            if self._input_to_element(end_input, end_date, "종료일"):
                logger.info(f"종료일 '{end_date}' 입력 완료")
                return True
            else:
                logger.error("종료일 입력 실패")
                return False
                
        except Exception as e:
            logger.error(f"방문기간 입력 중 오류: {e}")
            return False
            
    def _input_to_element(self, element, value: str, field_name: str) -> bool:
        """특정 요소에 입력"""
        try:
            # 요소가 보이도록 스크롤
            self._ensure_element_visible(element)
            time.sleep(1)
            
            # 요소를 클릭 가능한 상태로 만들기
            self._make_element_interactable(element)
            
            # JavaScript를 통한 직접 입력 시도
            if self._input_via_javascript(element, value):
                logger.info(f"{field_name} '{value}' 입력 완료 (JavaScript)")
                return True
            
            # 일반적인 방법으로 재시도
            try:
                element.clear()
                time.sleep(0.5)
                element.send_keys(value)
                
                # 입력 확인
                actual_value = element.get_attribute('value')
                if actual_value == value:
                    logger.info(f"{field_name} '{value}' 입력 완료")
                    return True
                else:
                    logger.warning(f"{field_name} 입력 확인 실패. 예상값: {value}, 실제값: {actual_value}")
                    return False
                    
            except Exception as e:
                logger.warning(f"일반 입력 방법 실패: {e}")
                return False
                
        except Exception as e:
            logger.error(f"{field_name} 입력 중 오류: {e}")
            return False
            
    def _input_with_retry(self, index: int, value: str, field_name: str, max_retries: int = 3) -> bool:
        """재시도 로직을 포함한 입력 처리"""
        for attempt in range(max_retries):
            try:
                logger.info(f"{field_name} 입력 시도 {attempt + 1}/{max_retries}")
                
                # 요소 찾기
                element = self.find_input_element(index)
                if not element:
                    logger.error(f"{field_name} 입력 요소를 찾을 수 없습니다 (시도 {attempt + 1})")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    return False
                
                # 강화된 스크롤 처리
                self._ensure_element_visible(element)
                time.sleep(1)
                
                # 요소를 클릭 가능한 상태로 만들기
                self._make_element_interactable(element)
                
                # JavaScript를 통한 직접 입력 시도
                if self._input_via_javascript(element, value):
                    logger.info(f"{field_name} '{value}' 입력 완료 (JavaScript)")
                    return True
                
                # 일반적인 방법으로 재시도
                try:
                    element.clear()
                    time.sleep(0.5)
                    element.send_keys(value)
                    
                    # 입력 확인
                    actual_value = element.get_attribute('value')
                    if actual_value == value:
                        logger.info(f"{field_name} '{value}' 입력 완료")
                        return True
                    else:
                        logger.warning(f"{field_name} 입력 확인 실패. 예상값: {value}, 실제값: {actual_value}")
                        if attempt < max_retries - 1:
                            time.sleep(2)
                            continue
                except Exception as e:
                    logger.warning(f"일반 입력 방법 실패: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                
            except Exception as e:
                logger.error(f"{field_name} 입력 중 오류 (시도 {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        
        return False
        
    def _make_element_interactable(self, element):
        """요소를 클릭 가능한 상태로 만들기"""
        try:
            # 요소가 클릭 가능한지 확인하고 클릭
            if element.is_enabled() and element.is_displayed():
                # JavaScript로 요소를 완전히 활성화
                self.driver.execute_script("""
                    var element = arguments[0];
                    
                    // 요소의 모든 제약사항 제거
                    element.disabled = false;
                    element.readOnly = false;
                    element.style.pointerEvents = 'auto';
                    element.style.opacity = '1';
                    element.style.visibility = 'visible';
                    element.style.display = 'block';
                    
                    // 요소를 클릭 가능한 상태로 만들기
                    element.removeAttribute('disabled');
                    element.removeAttribute('readonly');
                    element.removeAttribute('hidden');
                    
                    // 포커스 설정
                    element.focus();
                    element.click();
                """, element)
                
                time.sleep(1)
                
                # 요소를 클릭하여 포커스 설정
                try:
                    element.click()
                    time.sleep(0.5)
                except Exception as e:
                    logger.warning(f"요소 클릭 실패: {e}")
                
                # JavaScript로 포커스 설정
                self.driver.execute_script("arguments[0].focus();", element)
                time.sleep(0.5)
                
                # 요소가 실제로 상호작용 가능한지 확인
                is_interactable = self.driver.execute_script("""
                    var element = arguments[0];
                    return element.offsetParent !== null && 
                           !element.disabled && 
                           element.style.display !== 'none' && 
                           element.style.visibility !== 'hidden' &&
                           element.style.pointerEvents !== 'none';
                """, element)
                
                if is_interactable:
                    logger.info("요소가 상호작용 가능한 상태입니다")
                    return True
                else:
                    logger.warning("요소가 상호작용 불가능한 상태입니다")
                    return False
            else:
                logger.warning("요소가 활성화되지 않았거나 표시되지 않습니다")
                return False
                
        except Exception as e:
            logger.warning(f"요소 상호작용 가능 상태 설정 중 오류: {e}")
            return False
            
    def fill_content(self, content: str) -> bool:
        """내용 입력"""
        try:
            logger.info(f"내용 입력 중: {content}")
            
            # textarea 요소를 직접 찾기
            textarea_selectors = [
                "textarea[placeholder*='상세 내용']",
                "textarea[class*='textarea']",
                "textarea[data-v-*]",
                "textarea"
            ]
            
            textarea_element = None
            for selector in textarea_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        textarea_element = elements[0]
                        logger.info(f"textarea 요소 찾음: {selector}")
                        break
                except Exception as e:
                    continue
            
            if not textarea_element:
                logger.error("textarea 요소를 찾을 수 없습니다")
                return False
            
            # textarea에 직접 입력
            if self._input_to_element(textarea_element, content, "내용"):
                return True
            else:
                logger.error("내용 입력에 실패했습니다")
                return False
                
        except Exception as e:
            logger.error(f"내용 입력 중 오류: {e}")
            return False
            
    def fill_visitor_information(self, visitor_data: List[Dict[str, Any]], applicant_data: Dict[str, Any]) -> bool:
        """방문객 정보 입력 (단순화된 버전)"""
        try:
            logger.info(f"방문객 정보 입력 시작: {len(visitor_data)}명")
            
            # 방문객 정보 입력 전에 페이지 구조 디버깅
            logger.info("방문객 정보 입력 전 페이지 구조 분석...")
            self._debug_page_structure()
            
            # 방문객 정보 순서대로 입력
            for i, visitor in enumerate(visitor_data):
                logger.info(f"방문객 {i+1} 입력 중: {visitor.get('성명', '')}")
                
                if i == 0:
                    # 첫 번째 방문객: 기존 빈 ul에 직접 입력
                    logger.info("첫 번째 방문객입니다. 기존 빈 ul에 직접 입력합니다.")
                    if not self._fill_visitor_basic_info(visitor, is_first_visitor=True):
                        logger.error(f"방문객 {i+1} 추가 실패")
                        return False
                    
                    # 첫 번째 방문객의 차량정보 입력 (있는 경우)
                    if visitor.get('차종') and visitor.get('차종') != '':
                        if not self._fill_vehicle_info(visitor):
                            logger.warning("첫 번째 방문객 차량정보 입력 실패")
                    
                    # 첫 번째 방문객의 개인정보 동의 체크박스 클릭
                    if not self._check_privacy_consent():
                        logger.error(f"첫 번째 방문객 개인정보 동의 체크 실패")
                        return False
                else:
                    # 두 번째 방문객부터: 방문객추가 버튼 클릭 후 새 ul에 입력
                    logger.info(f"방문객 {i+1}입니다. 방문객추가 버튼을 클릭합니다.")
                    if not self._add_new_visitor(visitor):
                        logger.error(f"방문객 {i+1} 추가 실패")
                        return False
            
            logger.info("방문객 정보 입력 완료")
            
            # 방문객 정보 입력 후 피방문자 정보 변경 여부 확인
            logger.info("방문객 정보 입력 후 피방문자 정보 검증...")
            if not self._verify_applicant_info_unchanged(applicant_data):
                logger.error("❌ 방문객 정보 입력 중 피방문자 정보가 변경되었습니다!")
                return False
            else:
                logger.info("✅ 피방문자 정보가 정상적으로 유지되었습니다")
            
            return True
            
        except Exception as e:
            logger.error(f"방문객 정보 입력 중 오류: {e}")
            return False
            
    def _verify_applicant_in_visitor_table(self, applicant_data: Dict[str, Any]) -> bool:
        """신청자 정보가 방문객 테이블에 자동 입력되었는지 확인"""
        try:
            applicant_name = applicant_data.get('신청자', '')
            applicant_phone = applicant_data.get('연락처', '')
            
            # 방문객 정보 ul 찾기
            visitor_uls = self.driver.find_elements(By.CSS_SELECTOR, "ul")
            if not visitor_uls:
                logger.warning("방문객 정보 ul을 찾을 수 없습니다")
                return False
            
            logger.info(f"방문객 정보 ul {len(visitor_uls)}개 발견")
            
            # 방문객 정보 ul에서 신청자 정보 찾기
            for ul_idx, ul in enumerate(visitor_uls):
                try:
                    # list_1 (성명) 확인
                    name_li = ul.find_element(By.CSS_SELECTOR, "li.list_1")
                    name_input = name_li.find_element(By.CSS_SELECTOR, "input")
                    name_value = name_input.get_attribute('value')
                    logger.info(f"ul {ul_idx+1}의 성명: '{name_value}'")
                    
                    # list_3 (연락처) 확인
                    phone_li = ul.find_element(By.CSS_SELECTOR, "li.list_3")
                    phone_inputs = phone_li.find_elements(By.CSS_SELECTOR, "input")
                    if len(phone_inputs) >= 2:
                        phone_value = phone_inputs[0].get_attribute('value') + phone_inputs[1].get_attribute('value')
                        logger.info(f"ul {ul_idx+1}의 연락처: '{phone_value}'")
                        
                        # 연락처 비교 (엑셀의 두 번째, 세 번째 값만 추출)
                        phone_parts = applicant_phone.split('-')
                        if len(phone_parts) >= 3:
                            applicant_phone_clean = phone_parts[1] + phone_parts[2]  # 두 번째 + 세 번째 값
                            logger.info(f"신청자 연락처 비교: '{phone_value}' vs '{applicant_phone_clean}'")
                            if name_value == applicant_name and phone_value == applicant_phone_clean:
                                logger.info("신청자 정보가 방문객 테이블에 자동 입력됨을 확인")
                                return True
                            
                except Exception as e:
                    logger.debug(f"ul {ul_idx+1} 처리 중 오류: {e}")
                    continue
            
            logger.warning("신청자 정보를 방문객 테이블에서 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"신청자 정보 확인 중 오류: {e}")
            return False
            
    def _is_same_as_applicant(self, visitor: Dict[str, Any], applicant_data: Dict[str, Any]) -> bool:
        """방문객이 신청자와 동일한지 확인"""
        try:
            visitor_name = visitor.get('성명', '')
            visitor_phone = visitor.get('휴대폰번호', '')
            applicant_name = applicant_data.get('신청자', '')
            applicant_phone = applicant_data.get('연락처', '')
            
            return visitor_name == applicant_name and visitor_phone == applicant_phone
            
        except Exception as e:
            logger.error(f"방문객 신청자 동일성 확인 중 오류: {e}")
            return False
            
    def _add_new_visitor(self, visitor: Dict[str, Any]) -> bool:
        """새로운 방문객 추가 (단순화된 버전)"""
        try:
            # 방문객추가 버튼 클릭
            logger.info("방문객추가 버튼을 클릭합니다.")
            if not self._click_add_visitor_button():
                return False
            
            # 방문객 정보 입력
            if not self._fill_visitor_basic_info(visitor, is_first_visitor=False):
                return False
            
            # 3. 차량정보 입력 (있는 경우)
            if visitor.get('차종') and visitor.get('차종') != '':
                if not self._fill_vehicle_info(visitor):
                    logger.warning("차량정보 입력 실패")
            
            # 4. 개인정보 동의 체크박스 클릭
            if not self._check_privacy_consent():
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"새로운 방문객 추가 중 오류: {e}")
            return False
            
    def _get_current_visitor_ul(self, is_first_visitor: bool = False) -> Optional[WebElement]:
        """현재 방문객 정보를 입력할 ul 요소 찾기"""
        try:
            # 방문객 정보 ul 찾기 (list_1 클래스를 가진 li가 있는 ul만 필터링)
            all_uls = self.driver.find_elements(By.CSS_SELECTOR, "ul")
            visitor_uls = []
            
            for ul in all_uls:
                try:
                    # list_1 클래스를 가진 li가 있는지 확인
                    list_1_li = ul.find_element(By.CSS_SELECTOR, "li.list_1")
                    visitor_uls.append(ul)
                except:
                    # list_1이 없는 ul은 건너뛰기
                    continue
            
            if not visitor_uls:
                logger.error("방문객 정보 ul을 찾을 수 없습니다")
                return None
            
            # 방문객 정보 ul과 피방문자 정보 ul을 구분
            visitor_only_uls = []
            for ul in visitor_uls:
                try:
                    # 피방문자 정보 ul인지 확인 (피방문자 연락처가 있는지 체크)
                    phone_li = ul.find_element(By.CSS_SELECTOR, "li.list_3")
                    phone_inputs = phone_li.find_elements(By.CSS_SELECTOR, "input")
                    
                    # 피방문자 정보 ul은 연락처 input이 3개 (010-XXXX-XXXX)
                    # 방문객 정보 ul은 연락처 input이 2개 (XXXX-XXXX)
                    if len(phone_inputs) == 2:  # 방문객 정보 ul
                        visitor_only_uls.append(ul)
                        logger.info("방문객 정보 ul 발견 (연락처 input 2개)")
                    else:
                        logger.info("피방문자 정보 ul 발견 (연락처 input 3개) - 제외")
                        
                except Exception as e:
                    logger.debug(f"ul 분석 중 오류: {e}")
                    continue
            
            if not visitor_only_uls:
                logger.error("방문객 정보만을 위한 ul을 찾을 수 없습니다")
                return None
            
            if is_first_visitor and len(visitor_only_uls) >= 2:
                # 첫 번째 방문객: 두 번째 방문객 정보 ul 반환 (기존 빈 ul)
                current_ul = visitor_only_uls[1]  # 두 번째 방문객 정보 ul
                logger.info(f"첫 번째 방문객입니다. 두 번째 방문객 정보 ul 선택 (총 {len(visitor_only_uls)}개 방문객 정보 ul)")
            else:
                # 두 번째 방문객부터: 마지막 방문객 정보 ul 반환
                current_ul = visitor_only_uls[-1]  # 마지막 방문객 정보 ul
                logger.info(f"마지막 방문객 정보 ul 선택 (총 {len(visitor_only_uls)}개 방문객 정보 ul)")
            
            # ul의 구조 디버깅
            try:
                li_elements = current_ul.find_elements(By.CSS_SELECTOR, "li")
                logger.info(f"현재 방문객 정보 ul의 li 개수: {len(li_elements)}")
                for i, li in enumerate(li_elements):
                    li_class = li.get_attribute('class')
                    logger.info(f"li {i+1}: class='{li_class}'")
                    
                    # 연락처 input 개수 확인
                    if li_class == 'list_3':
                        phone_inputs = li.find_elements(By.CSS_SELECTOR, "input")
                        logger.info(f"  - 연락처 input 개수: {len(phone_inputs)}")
                        
            except Exception as e:
                logger.warning(f"ul 구조 디버깅 중 오류: {e}")
            
            return current_ul
            
        except Exception as e:
            logger.error(f"현재 방문객 정보 ul 찾기 중 오류: {e}")
            return None
            
    def _find_applicant_ul_index(self, applicant_data: Dict[str, Any]) -> Optional[int]:
        """신청자 정보가 입력된 ul의 인덱스 찾기"""
        try:
            applicant_name = applicant_data.get('신청자', '')
            applicant_phone = applicant_data.get('연락처', '')
            
            # 연락처에서 두 번째, 세 번째 값만 추출
            phone_parts = applicant_phone.split('-')
            if len(phone_parts) >= 3:
                applicant_phone_clean = phone_parts[1] + phone_parts[2]  # 두 번째 + 세 번째 값
            else:
                applicant_phone_clean = applicant_phone.replace('-', '')
            
            # 방문객 정보 ul 찾기
            visitor_uls = self.driver.find_elements(By.CSS_SELECTOR, "ul")
            
            for ul_idx, ul in enumerate(visitor_uls):
                try:
                    # list_1 (성명) 확인
                    name_li = ul.find_element(By.CSS_SELECTOR, "li.list_1")
                    name_input = name_li.find_element(By.CSS_SELECTOR, "input")
                    name_value = name_input.get_attribute('value')
                    
                    # list_3 (연락처) 확인
                    phone_li = ul.find_element(By.CSS_SELECTOR, "li.list_3")
                    phone_inputs = phone_li.find_elements(By.CSS_SELECTOR, "input")
                    if len(phone_inputs) >= 2:
                        phone_value = phone_inputs[0].get_attribute('value') + phone_inputs[1].get_attribute('value')
                        
                        if name_value == applicant_name and phone_value == applicant_phone_clean:
                            logger.info(f"신청자 정보가 입력된 ul 인덱스: {ul_idx}")
                            return ul_idx
                            
                except Exception as e:
                    continue
            
            logger.warning("신청자 정보가 입력된 ul을 찾을 수 없습니다")
            return None
            
        except Exception as e:
            logger.error(f"신청자 ul 인덱스 찾기 중 오류: {e}")
            return None
            
    def _click_add_visitor_button(self) -> bool:
        """방문객추가 버튼 클릭"""
        try:
            # 방문객추가 버튼 찾기 (class="button-add")
            add_button = self.driver.find_element(By.CSS_SELECTOR, "button.button-add")
            
            # 버튼이 화면에 보이도록 스크롤
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            time.sleep(1)
            
            # JavaScript로 버튼 클릭
            self.driver.execute_script("arguments[0].click();", add_button)
            time.sleep(2)
            logger.info("방문객추가 버튼 클릭 완료 (JavaScript)")
            return True
                
        except Exception as e:
            logger.error(f"방문객추가 버튼 클릭 중 오류: {e}")
            return False
            
    def _fill_visitor_basic_info(self, visitor: Dict[str, Any], is_first_visitor: bool = False) -> bool:
        """방문객 기본 정보 입력"""
        try:
            # 현재 방문객 정보 ul 찾기
            current_ul = self._get_current_visitor_ul(is_first_visitor)
            if not current_ul:
                return False
            
            # 추가 보호: 이 ul이 실제로 방문객 정보 ul인지 한 번 더 확인
            try:
                phone_li = current_ul.find_element(By.CSS_SELECTOR, "li.list_3")
                phone_inputs = phone_li.find_elements(By.CSS_SELECTOR, "input")
                
                if len(phone_inputs) != 2:
                    logger.error(f"잘못된 ul 선택: 연락처 input이 {len(phone_inputs)}개입니다. 방문객 정보 ul이 아닙니다.")
                    return False
                    
                logger.info(f"방문객 정보 ul 확인 완료: 연락처 input {len(phone_inputs)}개")
                
            except Exception as e:
                logger.error(f"ul 검증 중 오류: {e}")
                return False
            
            # 방문자명 입력 (list_1)
            visitor_name = visitor.get('성명', '')
            if visitor_name:
                name_li = current_ul.find_element(By.CSS_SELECTOR, "li.list_1")
                name_input = name_li.find_element(By.CSS_SELECTOR, "input")
                
                # disabled 속성 제거
                self.driver.execute_script("arguments[0].removeAttribute('disabled')", name_input)
                name_input.clear()
                name_input.send_keys(visitor_name)
                logger.info(f"방문자명 입력: {visitor_name}")
            
            # 연락처 입력 (list_3)
            visitor_phone = visitor.get('휴대폰번호', '')
            if visitor_phone:
                phone_li = current_ul.find_element(By.CSS_SELECTOR, "li.list_3")
                phone_inputs = phone_li.find_elements(By.CSS_SELECTOR, "input")
                
                if len(phone_inputs) >= 2:
                    # 하이픈으로 분리
                    phone_parts = visitor_phone.split('-')
                    if len(phone_parts) >= 3:
                        # 첫 번째 input (두 번째 값)
                        self.driver.execute_script("arguments[0].removeAttribute('disabled')", phone_inputs[0])
                        phone_inputs[0].clear()
                        phone_inputs[0].send_keys(phone_parts[1])
                        
                        # 두 번째 input (세 번째 값)
                        self.driver.execute_script("arguments[0].removeAttribute('disabled')", phone_inputs[1])
                        phone_inputs[1].clear()
                        phone_inputs[1].send_keys(phone_parts[2])
                        
                        logger.info(f"연락처 입력: {phone_parts[1]}-{phone_parts[2]}")
            
            return True
            
        except Exception as e:
            logger.error(f"방문객 기본 정보 입력 중 오류: {e}")
            return False
            
    def _fill_vehicle_info(self, visitor: Dict[str, Any]) -> bool:
        """차량정보 입력"""
        try:
            vehicle_type = visitor.get('차종', '')  # 차종
            vehicle_number = visitor.get('차량번호', '')  # 차량번호
            
            if not vehicle_type or vehicle_type == '':
                logger.info("차종이 없어서 차량정보 입력을 건너뜁니다")
                return True
            
            # 현재 방문객 정보 ul에서 차량정보 등록 버튼 클릭 (list_5)
            current_ul = self._get_current_visitor_ul()
            if not current_ul:
                return False
            
            vehicle_li = current_ul.find_element(By.CSS_SELECTOR, "li.list_5")
            vehicle_button = vehicle_li.find_element(By.CSS_SELECTOR, "button.button-itemadd")
            vehicle_button.click()
            time.sleep(1)
            
            # 팝업에서 차량정보 입력
            if not self._fill_vehicle_popup(vehicle_type, vehicle_number):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"차량정보 입력 중 오류: {e}")
            return False
            
    def _fill_vehicle_popup(self, vehicle_type: str, vehicle_number: str) -> bool:
        """차량정보 팝업 입력"""
        try:
            logger.info(f"차량정보 팝업 입력 시작: {vehicle_type}, {vehicle_number}")
            
            # 팝업이 나타날 때까지 대기
            time.sleep(2)
            
            # Vue.js 차량정보 팝업의 정확한 입력 필드 찾기
            try:
                # JavaScript 소스 분석 결과에 따른 정확한 선택자 사용
                vehicle_inputs = []
                
                # 방법 1: Vue.js v-model 바인딩된 input 필드 찾기 (ref="carNm", ref="carNumber")
                try:
                    # 차량명 입력 필드 (ref="carNm")
                    car_name_input = self.driver.find_element(By.CSS_SELECTOR, "input[ref='carNm'], input[data-v-model*='carNm']")
                    # 차량번호 입력 필드 (ref="carNumber") 
                    car_number_input = self.driver.find_element(By.CSS_SELECTOR, "input[ref='carNumber'], input[data-v-model*='carNumber']")
                    vehicle_inputs = [car_name_input, car_number_input]
                    logger.info("방법 1 - Vue.js ref 속성으로 차량정보 입력 필드 찾기 성공")
                except:
                    logger.info("방법 1 실패, 다음 방법 시도")
                
                # 방법 2: 정확한 CSS 선택자로 찾기 (staticClass="input")
                if len(vehicle_inputs) < 2:
                    try:
                        vehicle_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input.input[type='text']")
                        logger.info(f"방법 2 - input.input[type='text'] 요소 개수: {len(vehicle_inputs)}")
                    except:
                        pass
                
                # 방법 3: 팝업 내의 모든 input 요소
                if len(vehicle_inputs) < 2:
                    try:
                        vehicle_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                        logger.info(f"방법 3 - input[type='text'] 요소 개수: {len(vehicle_inputs)}")
                    except:
                        pass
                
                if len(vehicle_inputs) < 2:
                    logger.error(f"차량정보 입력 필드가 부족합니다. 필요: 2개, 실제: {len(vehicle_inputs)}개")
                    # 디버깅을 위해 모든 input 요소 정보 출력
                    for i, inp in enumerate(vehicle_inputs):
                        try:
                            placeholder = inp.get_attribute('placeholder') or 'N/A'
                            name = inp.get_attribute('name') or 'N/A'
                            id_attr = inp.get_attribute('id') or 'N/A'
                            class_attr = inp.get_attribute('class') or 'N/A'
                            ref_attr = inp.get_attribute('ref') or 'N/A'
                            logger.info(f"Input {i}: placeholder='{placeholder}', name='{name}', id='{id_attr}', class='{class_attr}', ref='{ref_attr}'")
                        except:
                            logger.info(f"Input {i}: 정보 읽기 실패")
                    return False
                
                # 차량명 입력 (첫 번째 input)
                vehicle_name_input = vehicle_inputs[0]
                logger.info(f"차량명 입력 필드 선택: placeholder='{vehicle_name_input.get_attribute('placeholder')}', ref='{vehicle_name_input.get_attribute('ref')}'")
                
                # Vue.js 컴포넌트에 직접 차량명 값 할당
                try:
                    # 방법 1: Vue.js 컴포넌트 인스턴스에 직접 값 할당
                    self.driver.execute_script("""
                        // 팝업 내의 Vue.js 컴포넌트 찾기
                        var popup = document.querySelector('.modal-card');
                        if (popup && popup.__vue__) {
                            popup.__vue__.carNm = arguments[0];
                            console.log('Vue.js carNm 설정 완료:', arguments[0]);
                        }
                        
                        // 입력 필드에 값 설정
                        arguments[1].value = arguments[0];
                        arguments[1].dispatchEvent(new Event('input', { bubbles: true }));
                        arguments[1].dispatchEvent(new Event('change', { bubbles: true }));
                        
                        // Vue.js v-model 업데이트
                        if (arguments[1]._vnode && arguments[1]._vnode.componentInstance) {
                            arguments[1]._vnode.componentInstance.carNm = arguments[0];
                        }
                    """, vehicle_type, vehicle_name_input)
                    logger.info(f"차량명 입력 완료 (Vue.js 직접 할당): {vehicle_type}")
                except Exception as e:
                    logger.warning(f"Vue.js 직접 할당 실패: {e}")
                    try:
                        # 방법 2: 일반 JavaScript 입력
                        self.driver.execute_script("arguments[0].value = '';", vehicle_name_input)
                        self.driver.execute_script(f"arguments[0].value = '{vehicle_type}';", vehicle_name_input)
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", vehicle_name_input)
                        logger.info(f"차량명 입력 완료 (JavaScript): {vehicle_type}")
                    except Exception as e2:
                        logger.warning(f"JavaScript 차량명 입력 실패: {e2}")
                        try:
                            # 방법 3: Selenium send_keys 사용
                            vehicle_name_input.clear()
                            vehicle_name_input.send_keys(vehicle_type)
                            logger.info(f"차량명 입력 완료 (send_keys): {vehicle_type}")
                        except Exception as e3:
                            logger.error(f"모든 차량명 입력 방법 실패: {e3}")
                            return False
                
                # 차량번호 입력 (두 번째 input)
                vehicle_number_input = vehicle_inputs[1]
                logger.info(f"차량번호 입력 필드 선택: placeholder='{vehicle_number_input.get_attribute('placeholder')}', ref='{vehicle_number_input.get_attribute('ref')}'")
                
                # Vue.js 컴포넌트에 직접 차량번호 값 할당
                try:
                    # 방법 1: Vue.js 컴포넌트 인스턴스에 직접 값 할당
                    self.driver.execute_script("""
                        // 팝업 내의 Vue.js 컴포넌트 찾기
                        var popup = document.querySelector('.modal-card');
                        if (popup && popup.__vue__) {
                            popup.__vue__.carNumber = arguments[0];
                            console.log('Vue.js carNumber 설정 완료:', arguments[0]);
                        }
                        
                        // 입력 필드에 값 설정
                        arguments[1].value = arguments[0];
                        arguments[1].dispatchEvent(new Event('input', { bubbles: true }));
                        arguments[1].dispatchEvent(new Event('change', { bubbles: true }));
                        
                        // Vue.js v-model 업데이트
                        if (arguments[1]._vnode && arguments[1]._vnode.componentInstance) {
                            arguments[1]._vnode.componentInstance.carNumber = arguments[0];
                        }
                    """, vehicle_number, vehicle_number_input)
                    logger.info(f"차량번호 입력 완료 (Vue.js 직접 할당): {vehicle_number}")
                except Exception as e:
                    logger.warning(f"Vue.js 직접 할당 실패: {e}")
                    try:
                        # 방법 2: 일반 JavaScript 입력
                        self.driver.execute_script("arguments[0].value = '';", vehicle_number_input)
                        self.driver.execute_script(f"arguments[0].value = '{vehicle_number}';", vehicle_number_input)
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", vehicle_number_input)
                        logger.info(f"차량번호 입력 완료 (JavaScript): {vehicle_number}")
                    except Exception as e2:
                        logger.warning(f"JavaScript 차량번호 입력 실패: {e2}")
                        try:
                            # 방법 3: Selenium send_keys 사용
                            vehicle_number_input.clear()
                            vehicle_number_input.send_keys(vehicle_number)
                            logger.info(f"차량번호 입력 완료 (send_keys): {vehicle_number}")
                        except Exception as e3:
                            logger.error(f"모든 차량번호 입력 방법 실패: {e3}")
                            return False
                
            except Exception as e:
                logger.error(f"차량정보 입력 실패: {e}")
                return False
            
            # 입력 후 잠시 대기
            time.sleep(1)
            
            # 등록 버튼 찾기 및 클릭 (팝업 내의 등록 버튼만 찾기)
            try:
                # 팝업 내의 등록 버튼만 찾기 (메인페이지의 신청하기 버튼과 구분)
                register_button = None
                
                # 방법 1: 팝업 내에서만 등록 버튼 찾기
                try:
                    # 팝업 요소 내에서 등록 버튼 찾기
                    popup = self.driver.find_element(By.CSS_SELECTOR, ".modal-card, .modal, .popup, [role='dialog']")
                    register_button = popup.find_element(By.CSS_SELECTOR, "button.button-request")
                    logger.info("팝업 내에서 등록 버튼 찾기 성공")
                except:
                    logger.info("팝업 내에서 등록 버튼 찾기 실패, 다른 방법 시도")
                
                # 방법 2: 텍스트로 정확한 등록 버튼 찾기
                if not register_button:
                    try:
                        register_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '등록') and not(contains(text(), '신청'))]")
                        logger.info("텍스트로 등록 버튼 찾기 성공")
                    except:
                        logger.info("텍스트로 등록 버튼 찾기 실패")
                
                # 방법 3: 팝업 내의 모든 버튼 중에서 등록 버튼 찾기
                if not register_button:
                    try:
                        popup_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".modal-card button, .modal button, .popup button, [role='dialog'] button")
                        for button in popup_buttons:
                            button_text = button.text.strip()
                            if "등록" in button_text and "신청" not in button_text:
                                register_button = button
                                logger.info(f"팝업 내 버튼 중 등록 버튼 찾기 성공: {button_text}")
                                break
                    except:
                        logger.info("팝업 내 버튼 중 등록 버튼 찾기 실패")
                
                if not register_button:
                    logger.error("차량정보 팝업 내의 등록 버튼을 찾을 수 없습니다")
                    return False
                
                # JavaScript로 버튼 클릭
                self.driver.execute_script("arguments[0].click();", register_button)
                logger.info("차량정보 등록 버튼 클릭 완료")
                
                # 팝업이 닫힐 때까지 대기
                time.sleep(3)
                
                # 팝업이 실제로 닫혔는지 확인 및 강제 닫기
                try:
                    time.sleep(2)  # 추가 대기
                    
                    # SweetAlert2 팝업 확인 및 닫기
                    swal_popups = self.driver.find_elements(By.CSS_SELECTOR, ".swal2-popup, .swal2-modal")
                    if swal_popups:
                        logger.warning("SweetAlert2 팝업이 감지되었습니다. 닫기 시도...")
                        # SweetAlert2 닫기 버튼 찾기
                        try:
                            close_button = self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm, .swal2-cancel, .swal2-close")
                            self.driver.execute_script("arguments[0].click();", close_button)
                            logger.info("SweetAlert2 팝업 닫기 버튼 클릭 완료")
                        except:
                            # ESC 키로 닫기 시도
                            from selenium.webdriver.common.keys import Keys
                            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                            logger.info("ESC 키로 SweetAlert2 팝업 닫기 시도")
                        
                        time.sleep(1)
                    
                    # 일반 팝업 요소 확인
                    popup_elements = self.driver.find_elements(By.CSS_SELECTOR, ".modal, .popup, [role='dialog']")
                    if not popup_elements:
                        logger.info("모든 팝업이 성공적으로 닫혔습니다")
                    else:
                        logger.warning("일부 팝업이 아직 열려있습니다. 강제 닫기 시도...")
                        # 강제로 ESC 키를 눌러 팝업 닫기 시도
                        from selenium.webdriver.common.keys import Keys
                        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                        time.sleep(1)
                        
                except Exception as e:
                    logger.warning(f"팝업 상태 확인 중 오류: {e}")
                    # 오류 발생 시에도 ESC 키로 닫기 시도
                    try:
                        from selenium.webdriver.common.keys import Keys
                        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                        time.sleep(1)
                    except:
                        pass
                
            except Exception as e:
                logger.error(f"등록 버튼 클릭 실패: {e}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"차량정보 팝업 입력 중 오류: {e}")
            return False
            
    def _fill_vehicle_info_for_applicant(self, visitor: Dict[str, Any]) -> bool:
        """신청자와 동일한 방문객의 차량정보 입력"""
        try:
            vehicle_type = visitor.get('차종', '')  # 차종
            vehicle_number = visitor.get('차량번호', '')  # 차량번호
            
            if not vehicle_type or vehicle_type == '':
                logger.info("차종이 없어서 차량정보 입력을 건너뜁니다")
                return True
            
            # 신청자 정보가 있는 방문객 ul 찾기
            visitor_uls = self.driver.find_elements(By.CSS_SELECTOR, "ul")
            
            for ul in visitor_uls:
                try:
                    # list_1에서 성명 확인
                    name_li = ul.find_element(By.CSS_SELECTOR, "li.list_1")
                    name_input = name_li.find_element(By.CSS_SELECTOR, "input")
                    name_value = name_input.get_attribute('value')
                    
                    if name_value == visitor.get('성명', ''):
                        # 해당 ul의 차량정보 등록 버튼 클릭 (list_5)
                        vehicle_li = ul.find_element(By.CSS_SELECTOR, "li.list_5")
                        vehicle_button = vehicle_li.find_element(By.CSS_SELECTOR, "button.button-itemadd")
                        vehicle_button.click()
                        time.sleep(1)
                        
                        # 팝업에서 차량정보 입력
                        if self._fill_vehicle_popup(vehicle_type, vehicle_number):
                            logger.info("신청자 차량정보 입력 완료")
                            return True
                        else:
                            return False
                            
                except Exception as e:
                    continue
            
            logger.error("신청자 정보가 있는 방문객 ul을 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"신청자 차량정보 입력 중 오류: {e}")
            return False
            
    def _check_privacy_consent(self) -> bool:
        """개인정보 동의 체크박스 클릭"""
        try:
            # 현재 방문객 정보 ul에서 체크박스들 클릭
            current_ul = self._get_current_visitor_ul()
            if not current_ul:
                return False
            
            # list_6 체크박스 (개인정보 처리방침 동의)
            try:
                privacy_li_6 = current_ul.find_element(By.CSS_SELECTOR, "li.list_6")
                privacy_checkbox1 = privacy_li_6.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                # JavaScript로 체크박스 클릭
                self.driver.execute_script("arguments[0].click();", privacy_checkbox1)
                logger.info("list_6 개인정보 처리방침 동의 체크박스 클릭 완료 (JavaScript)")
            except Exception as e:
                logger.warning(f"list_6 체크박스 클릭 실패: {e}")
            
            # list_7 체크박스 (개인정보 수집동의)
            try:
                privacy_li_7 = current_ul.find_element(By.CSS_SELECTOR, "li.list_7")
                privacy_checkbox2 = privacy_li_7.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                # JavaScript로 체크박스 클릭
                self.driver.execute_script("arguments[0].click();", privacy_checkbox2)
                logger.info("list_7 개인정보 수집동의 체크박스 클릭 완료 (JavaScript)")
            except Exception as e:
                logger.warning(f"list_7 체크박스 클릭 실패: {e}")
            
            logger.info("개인정보 동의 체크박스 클릭 완료")
            return True
            
        except Exception as e:
            logger.error(f"개인정보 동의 체크박스 클릭 중 오류: {e}")
            return False
            
    def find_input_element(self, index: int):
        """인덱스에 해당하는 input/textarea 요소 찾기"""
        try:
            # input과 textarea 모두 포함하는 선택자들
            input_selectors = [
                "input[name='input_0']",
                "input[name='input_1']", 
                "input[name='input_2']",
                "input[name='input_3']",
                "input[name='input_4']",
                "input[name='input_5']",
                "input[name='input_6']",
                "input[name='input_7']",
                "input[name='input_8']",
                "input[name='input_9']",
                "input[name='input_10']",
                "input[placeholder*='번호']",
                "input[type='text']",
                "textarea",  # textarea 요소 추가
                "textarea[class*='textarea']",  # textarea 클래스
                "textarea[data-v-*]",  # Vue.js data-v 속성
                "textarea[placeholder*='상세 내용']"  # 내용 필드 특정 placeholder
            ]
            
            for selector in input_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > index:
                        element = elements[index]
                        element_type = element.tag_name
                        logger.info(f"인덱스 {index} {element_type} 요소 찾음: {selector}")
                        return element
                except Exception as e:
                    continue
            
            # XPath를 사용한 대안적 방법 (input과 textarea 모두 포함)
            try:
                xpath_selectors = [
                    f"(//input[@type='text'])[{index + 1}]",
                    f"(//textarea)[{index + 1}]",
                    f"(//input[@type='text'] | //textarea)[{index + 1}]"
                ]
                
                for xpath_selector in xpath_selectors:
                    try:
                        element = self.driver.find_element(By.XPATH, xpath_selector)
                        element_type = element.tag_name
                        logger.info(f"인덱스 {index} {element_type} 요소 찾음 (XPath): {xpath_selector}")
                        return element
                    except Exception as e:
                        continue
                        
            except Exception as e:
                logger.warning(f"XPath로 요소 찾기 실패: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"input/textarea 요소 찾기 오류: {e}")
            return None
            
    def _ensure_element_visible(self, element):
        """요소가 화면에 보이도록 강화된 스크롤 처리"""
        try:
            # 여러 스크롤 방법 시도
            scroll_methods = [
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                "arguments[0].scrollIntoView({block: 'start'});",
                "arguments[0].scrollIntoView({block: 'end'});",
                "window.scrollTo(0, arguments[0].offsetTop - 100);",
                "arguments[0].scrollIntoView();"
            ]
            
            for method in scroll_methods:
                try:
                    self.driver.execute_script(method, element)
                    time.sleep(1)
                    
                    # 요소가 실제로 보이는지 확인
                    if self._is_element_visible(element):
                        logger.info("요소가 성공적으로 화면에 표시됨")
                        return True
                except Exception as e:
                    logger.warning(f"스크롤 방법 실패: {method}, 오류: {e}")
                    continue
            
            # 마지막 시도: 페이지 하단으로 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            return True
            
        except Exception as e:
            logger.error(f"요소 가시성 확보 중 오류: {e}")
            return False
            
    def _is_element_visible(self, element):
        """요소가 화면에 보이는지 확인"""
        try:
            # JavaScript로 요소의 가시성 확인
            is_visible = self.driver.execute_script("""
                var elem = arguments[0];
                var rect = elem.getBoundingClientRect();
                var windowHeight = window.innerHeight || document.documentElement.clientHeight;
                var windowWidth = window.innerWidth || document.documentElement.clientWidth;
                
                return (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= windowHeight &&
                    rect.right <= windowWidth &&
                    elem.offsetParent !== null
                );
            """, element)
            
            return is_visible
            
        except Exception as e:
            logger.warning(f"요소 가시성 확인 중 오류: {e}")
            return False
            
    def _input_via_javascript(self, element, value):
        """JavaScript를 통한 직접 입력"""
        try:
            element_type = element.tag_name.lower()
            
            # 요소 타입에 따른 JavaScript 입력 방법
            if element_type == 'textarea':
                js_methods = [
                    # textarea 전용 방법들
                    "arguments[0].value = arguments[1];",
                    "arguments[0].innerHTML = arguments[1]; arguments[0].value = arguments[1];",
                    "arguments[0].textContent = arguments[1]; arguments[0].value = arguments[1];",
                    "arguments[0].innerText = arguments[1]; arguments[0].value = arguments[1];"
                ]
            else:
                # input 전용 방법들
                js_methods = [
                    "arguments[0].value = arguments[1];",
                    "arguments[0].setAttribute('value', arguments[1]);",
                    "arguments[0].defaultValue = arguments[1]; arguments[0].value = arguments[1];"
                ]
            
            for method in js_methods:
                try:
                    self.driver.execute_script(method, element, value)
                    
                    # 다양한 이벤트 발생
                    self.driver.execute_script("""
                        var element = arguments[0];
                        
                        // focus 이벤트
                        element.focus();
                        
                        // input 이벤트
                        var inputEvent = new Event('input', { bubbles: true });
                        element.dispatchEvent(inputEvent);
                        
                        // change 이벤트
                        var changeEvent = new Event('change', { bubbles: true });
                        element.dispatchEvent(changeEvent);
                        
                        // keyup 이벤트
                        var keyupEvent = new Event('keyup', { bubbles: true });
                        element.dispatchEvent(keyupEvent);
                        
                        // blur 이벤트
                        element.blur();
                    """, element)
                    
                    time.sleep(0.5)
                    
                    # 값이 실제로 설정되었는지 확인
                    actual_value = element.get_attribute('value')
                    if actual_value == value:
                        logger.info(f"JavaScript 입력 성공 ({element_type}, 방법 {js_methods.index(method) + 1}): {value}")
                        return True
                    else:
                        logger.warning(f"JavaScript 입력 실패 ({element_type}, 방법 {js_methods.index(method) + 1}). 예상값: {value}, 실제값: {actual_value}")
                        continue
                        
                except Exception as e:
                    logger.warning(f"JavaScript 입력 방법 {js_methods.index(method) + 1} 실패: {e}")
                    continue
            
            return False
                
        except Exception as e:
            logger.error(f"JavaScript 입력 중 오류: {e}")
            return False
            
    def submit_form(self) -> bool:
        """폼 제출 (확인 버튼 클릭)"""
        return self.click_confirm_button()
        
    def click_submit_button(self) -> bool:
        """신청하기 버튼 클릭 (최종 제출)"""
        try:
            logger.info("신청하기 버튼 클릭 중...")
            
            # 신청하기 버튼 찾기 - 여러 방법 시도
            submit_selectors = [
                "button:contains('신청하기')",
                "button:contains('신청')",
                "button:contains('제출')",
                "button:contains('완료')",
                "input[value='신청하기']",
                "input[value='신청']",
                "button[type='submit']",
                ".submit-btn",
                "#submitBtn",
                "button.submit"
            ]
            
            for selector in submit_selectors:
                try:
                    # CSS 선택자로 찾기
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    submit_button.click()
                    logger.info("신청하기 버튼 클릭 완료")
                    time.sleep(2)  # 페이지 전환 대기
                    return True
                except Exception as e:
                    continue
            
            # XPath로 찾기 시도
            xpath_selectors = [
                "//button[contains(text(), '신청하기')]",
                "//button[contains(text(), '신청')]",
                "//button[contains(text(), '제출')]",
                "//button[contains(text(), '완료')]",
                "//input[@value='신청하기']",
                "//input[@value='신청']",
                "//button[@type='submit']",
                "//button[contains(@class, 'submit')]"
            ]
            
            for xpath in xpath_selectors:
                try:
                    submit_button = self.driver.find_element(By.XPATH, xpath)
                    submit_button.click()
                    logger.info("신청하기 버튼 클릭 완료 (XPath)")
                    time.sleep(2)  # 페이지 전환 대기
                    return True
                except Exception as e:
                    continue
            
            logger.error("신청하기 버튼을 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"신청하기 버튼 클릭 중 오류: {e}")
            return False
        
    def click_confirm_button(self) -> bool:
        """확인 버튼 클릭"""
        try:
            logger.info("확인 버튼 클릭 중...")
            
            # 확인 버튼 찾기 - 여러 방법 시도
            confirm_selectors = self.selectors.get_confirm_button_selectors()
            
            for selector in confirm_selectors:
                try:
                    # CSS 선택자로 찾기
                    confirm_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    confirm_button.click()
                    logger.info("확인 버튼 클릭 완료")
                    time.sleep(2)  # 페이지 전환 대기
                    return True
                except Exception as e:
                    continue
            
            # XPath로 찾기 시도
            xpath_selectors = [
                "//button[contains(text(), '확인')]",
                "//input[@value='확인']",
                "//button[text()='확인']",
                "//button[contains(@class, 'confirm')]"
            ]
            
            for xpath in xpath_selectors:
                try:
                    confirm_button = self.driver.find_element(By.XPATH, xpath)
                    confirm_button.click()
                    logger.info("확인 버튼 클릭 완료 (XPath)")
                    time.sleep(2)  # 페이지 전환 대기
                    return True
                except Exception as e:
                    continue
            
            logger.error("확인 버튼을 찾을 수 없습니다")
            return False
            
        except Exception as e:
            logger.error(f"확인 버튼 클릭 중 오류: {e}")
            return False
            
    def validate_result(self) -> bool:
        """결과 검증"""
        try:
            logger.info("결과 검증 중...")
            
            # 현재 URL 확인
            current_url = self.driver.current_url
            logger.info(f"현재 페이지 URL: {current_url}")
            
            # 성공 여부 판단 (예: 특정 메시지나 페이지 확인)
            # 여기에 실제 검증 로직을 추가할 수 있습니다
            
            logger.info("결과 검증 완료")
            return True
            
        except Exception as e:
            logger.error(f"결과 검증 오류: {e}")
            return False
            
    def run_automation(self, data: Dict[str, Any], keep_browser: bool = True) -> bool:
        """일진홀딩스 자동화 실행"""
        try:
            self.logger.info("일진홀딩스 자동화 시작")
            
            # 브라우저 유지 설정
            self.set_keep_browser(keep_browser)
            
            # 1. 웹드라이버 설정
            self.setup_driver()
            
            # 2. 웹사이트 접속
            if not self.navigate_to_website():
                return False
                
            # 3. 일진홀딩스 선택
            if not self.select_iljin_holdings():
                return False
                
            # 4. 방문신청하기 선택
            if not self.select_visit_request():
                return False
                
            # 5. 방문신청약관 동의
            if not self.agree_to_terms():
                return False
                
            # 6. 폼 작성 (피방문자 정보 입력 → 확인 버튼 클릭 → 신청자 정보 입력)
            if not self.fill_form(data):
                return False
                
            # 7. 신청하기 버튼 클릭 (최종 제출) - 주석 처리
            # if not self.click_submit_button():
            #     return False
                
            # 8. 결과 검증
            if not self.validate_result():
                return False
                
            self.logger.info("일진홀딩스 자동화 완료")
            
            # 브라우저 유지 여부에 따른 처리
            if self.keep_browser:
                self.logger.info("🎉 자동화가 성공적으로 완료되었습니다!")
                self.logger.info("🌐 브라우저가 열린 상태로 유지됩니다.")
                self.logger.info("💡 웹에서 직접 다음 작업을 진행할 수 있습니다.")
                self.logger.info("📝 자동화 결과를 확인하고 필요한 경우 수동으로 조정하세요.")
                self.logger.info("⚠️  브라우저를 닫으려면 수동으로 닫기 버튼을 클릭하세요.")
                
                # 브라우저 유지를 위한 추가 설정
                try:
                    # 현재 창을 활성화하여 사용자가 쉽게 접근할 수 있도록 함
                    self.driver.switch_to.window(self.driver.current_window_handle)
                    self.logger.info("현재 브라우저 창이 활성화되었습니다.")
                except Exception as e:
                    self.logger.warning(f"브라우저 창 활성화 중 경고: {e}")
                    
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

    def _debug_page_structure(self):
        """현재 페이지의 ul 구조를 디버깅하여 방문객 정보와 피방문자 정보를 구분"""
        try:
            logger.info("=== 페이지 구조 디버깅 시작 ===")
            
            # 모든 ul 찾기
            all_uls = self.driver.find_elements(By.CSS_SELECTOR, "ul")
            logger.info(f"페이지에서 발견된 ul 개수: {len(all_uls)}")
            
            for ul_idx, ul in enumerate(all_uls):
                try:
                    logger.info(f"\n--- ul {ul_idx + 1} 분석 ---")
                    
                    # ul의 li 요소들 찾기
                    li_elements = ul.find_elements(By.CSS_SELECTOR, "li")
                    logger.info(f"li 개수: {len(li_elements)}")
                    
                    for li_idx, li in enumerate(li_elements):
                        li_class = li.get_attribute('class')
                        logger.info(f"  li {li_idx + 1}: class='{li_class}'")
                        
                        # 연락처 정보가 있는 li인지 확인
                        if li_class == 'list_3':
                            try:
                                phone_inputs = li.find_elements(By.CSS_SELECTOR, "input")
                                logger.info(f"    - 연락처 input 개수: {len(phone_inputs)}")
                                
                                # 각 input의 현재 값 확인
                                for input_idx, phone_input in enumerate(phone_inputs):
                                    input_value = phone_input.get_attribute('value')
                                    input_placeholder = phone_input.get_attribute('placeholder')
                                    logger.info(f"      input {input_idx + 1}: value='{input_value}', placeholder='{input_placeholder}'")
                                
                                # ul 유형 판단
                                if len(phone_inputs) == 3:
                                    logger.info(f"    -> 이 ul은 피방문자 정보 ul입니다 (연락처 input 3개)")
                                elif len(phone_inputs) == 2:
                                    logger.info(f"    -> 이 ul은 방문객 정보 ul입니다 (연락처 input 2개)")
                                else:
                                    logger.info(f"    -> 이 ul은 기타 정보 ul입니다 (연락처 input {len(phone_inputs)}개)")
                                    
                            except Exception as e:
                                logger.warning(f"    - 연락처 input 분석 중 오류: {e}")
                        
                        # 성명 정보가 있는 li인지 확인
                        elif li_class == 'list_1':
                            try:
                                name_inputs = li.find_elements(By.CSS_SELECTOR, "input")
                                if name_inputs:
                                    name_value = name_inputs[0].get_attribute('value')
                                    name_placeholder = name_inputs[0].get_attribute('placeholder')
                                    logger.info(f"    - 성명 input: value='{name_value}', placeholder='{name_placeholder}'")
                            except Exception as e:
                                logger.warning(f"    - 성명 input 분석 중 오류: {e}")
                                
                except Exception as e:
                    logger.warning(f"ul {ul_idx + 1} 분석 중 오류: {e}")
                    continue
            
            logger.info("=== 페이지 구조 디버깅 완료 ===")
            
        except Exception as e:
            logger.error(f"페이지 구조 디버깅 중 오류: {e}")

    def _verify_applicant_info_unchanged(self, applicant_data: Dict[str, Any]) -> bool:
        """방문객 정보 입력 후 피방문자 정보가 변경되지 않았는지 확인"""
        try:
            logger.info("피방문자 정보 변경 여부 확인 중...")
            
            # 피방문자 정보 ul 찾기 (연락처 input이 3개인 ul)
            all_uls = self.driver.find_elements(By.CSS_SELECTOR, "ul")
            applicant_ul = None
            
            for ul in all_uls:
                try:
                    phone_li = ul.find_element(By.CSS_SELECTOR, "li.list_3")
                    phone_inputs = phone_li.find_elements(By.CSS_SELECTOR, "input")
                    
                    if len(phone_inputs) == 3:  # 피방문자 정보 ul
                        applicant_ul = ul
                        break
                except:
                    continue
            
            if not applicant_ul:
                logger.warning("피방문자 정보 ul을 찾을 수 없습니다")
                return True  # 찾을 수 없으면 검증 통과
            
            # 피방문자 연락처 확인
            try:
                phone_li = applicant_ul.find_element(By.CSS_SELECTOR, "li.list_3")
                phone_inputs = phone_li.find_elements(By.CSS_SELECTOR, "input")
                
                if len(phone_inputs) >= 3:
                    # 첫 번째 input (010)
                    first_input_value = phone_inputs[0].get_attribute('value')
                    # 두 번째 input (XXXX)
                    second_input_value = phone_inputs[1].get_attribute('value')
                    # 세 번째 input (XXXX)
                    third_input_value = phone_inputs[2].get_attribute('value')
                    
                    logger.info(f"피방문자 연락처 현재 값: {first_input_value}-{second_input_value}-{third_input_value}")
                    
                    # 원래 값과 비교 (엑셀 데이터의 피방문자 연락처)
                    expected_phone = applicant_data.get('피방문자 연락처', '')
                    if expected_phone:
                        phone_parts = expected_phone.split('-')
                        if len(phone_parts) >= 3:
                            expected_first = phone_parts[0]
                            expected_second = phone_parts[1]
                            expected_third = phone_parts[2]
                            
                            if (first_input_value == expected_first and 
                                second_input_value == expected_second and 
                                third_input_value == expected_third):
                                logger.info("✅ 피방문자 연락처가 변경되지 않았습니다")
                                return True
                            else:
                                logger.error("❌ 피방문자 연락처가 변경되었습니다!")
                                logger.error(f"  기대값: {expected_first}-{expected_second}-{expected_third}")
                                logger.error(f"  실제값: {first_input_value}-{second_input_value}-{third_input_value}")
                                return False
                    
            except Exception as e:
                logger.warning(f"피방문자 연락처 확인 중 오류: {e}")
            
            # 피방문자 성명 확인
            try:
                name_li = applicant_ul.find_element(By.CSS_SELECTOR, "li.list_2")
                name_input = name_li.find_element(By.CSS_SELECTOR, "input")
                current_name = name_input.get_attribute('value')
                expected_name = applicant_data.get('피방문자', '')
                
                logger.info(f"피방문자 성명 현재 값: '{current_name}'")
                logger.info(f"피방문자 성명 기대값: '{expected_name}'")
                
                if current_name == expected_name:
                    logger.info("✅ 피방문자 성명이 변경되지 않았습니다")
                else:
                    logger.error("❌ 피방문자 성명이 변경되었습니다!")
                    return False
                    
            except Exception as e:
                logger.warning(f"피방문자 성명 확인 중 오류: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"피방문자 정보 변경 여부 확인 중 오류: {e}")
            return False