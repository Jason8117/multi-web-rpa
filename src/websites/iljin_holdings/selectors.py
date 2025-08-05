"""
일진홀딩스 웹사이트 요소 선택자 정의
"""

class IljinSelectors:
    """일진홀딩스 웹사이트 선택자 클래스"""
    
    # 메인 페이지
    MAIN_PAGE = "http://visit.iljin.co.kr"
    
    # 일진홀딩스 선택
    ILJIN_HOLDINGS_LINK = "a[href*='ijhd']"
    
    # 방문신청하기
    VISIT_REQUEST_LINK = "a[href*='visitProposal']"
    
    # 방문신청약관 페이지
    TERMS_PAGE = "http://visit.iljin.co.kr/ijhd/visitProposal"
    
    # 체크박스
    AGREE_CHECKBOX_1 = "agreeChk_1"
    AGREE_CHECKBOX_2 = "agreeChk_2"
    
    # 동의 버튼
    AGREE_BUTTON = "button:contains('동의합니다')"
    
    # 방문신청 폼 페이지
    VISIT_FORM_PAGE = "http://visit.iljin.co.kr/ijhd/visitReserve"
    
    # 방문사업장 선택
    VISIT_LOCATION_SELECT = "select[name='select_0']"
    
    # 전화번호 입력 필드들
    PHONE_INPUT_1 = "input[name='input_1']"  # 두 번째 텍스트 박스
    PHONE_INPUT_2 = "input[name='input_2']"  # 세 번째 텍스트 박스
    
    # 피방문자 입력 필드
    VISIT_PERSON_INPUT = "input[name='input_2']"  # 세 번째 텍스트 박스
    
    # 확인 버튼
    CONFIRM_BUTTON = "button:contains('확인')"
    
    # 모든 텍스트 입력 필드
    ALL_TEXT_INPUTS = "input[type='text']"
    
    # 모든 select 요소
    ALL_SELECTS = "select"
    
    # XPath 선택자들
    XPATH_SELECTORS = {
        'iljin_holdings_link': "//a[contains(@href, 'ijhd')]",
        'visit_request_link': "//a[contains(@href, 'visitProposal')]",
        'agree_button': "//button[contains(text(), '동의합니다')]",
        'confirm_button': "//button[contains(text(), '확인')]",
        'visit_location_select': "//select[@name='select_0']",
        'phone_inputs': "//input[@type='text']",
    }
    
    @classmethod
    def get_phone_input_selectors(cls):
        """전화번호 입력 필드 선택자 목록"""
        return [
            cls.PHONE_INPUT_1,
            cls.PHONE_INPUT_2,
            cls.ALL_TEXT_INPUTS
        ]
    
    @classmethod
    def get_agree_checkbox_ids(cls):
        """동의 체크박스 ID 목록"""
        return [cls.AGREE_CHECKBOX_1, cls.AGREE_CHECKBOX_2]
    
    @classmethod
    def get_confirm_button_selectors(cls):
        """확인 버튼 선택자 목록"""
        return [
            cls.CONFIRM_BUTTON,
            "button[type='submit']",
            "input[type='submit']",
            "button[type='button']:contains('확인')",
            ".confirm-btn",
            "#confirmBtn",
            "button.confirm"
        ] 