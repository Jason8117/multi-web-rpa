"""
IP 168 ITSM 웹사이트 요소 선택자 정의
"""

from typing import Optional

class IP168ITSMSelectors:
    """IP 168 ITSM 웹사이트 선택자 클래스"""
    
    # 메인 페이지
    MAIN_PAGE = "http://4.144.198.168/sign-in"
    LOGIN_PAGE = "http://4.144.198.168/sign-in"
    
    # 로그인 폼 요소들
    USERNAME_INPUT = "input[name='userName']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    LOGIN_FORM = "form"
    
    # 대체 선택자들 (다양한 웹사이트 구조 대응)
    ALTERNATIVE_SELECTORS = {
        'username': [
            "input[name='userName']",
            "input[id='mui-1']",
            "input[name='username']",
            "input[name='user']",
            "input[name='email']",
            "input[id='username']",
            "input[id='user']",
            "input[id='email']",
            "input[type='text']",
            "#mui-1",
            "#username",
            "#user",
            "#email"
        ],
        'password': [
            "input[name='password']",
            "input[id='mui-2']",
            "input[name='pass']",
            "input[name='pwd']",
            "input[id='password']",
            "input[id='pass']",
            "input[id='pwd']",
            "input[type='password']",
            "#mui-2",
            "#password",
            "#pass",
            "#pwd"
        ],
        'login_button': [
            "button[type='submit']",
            "input[type='submit']",
            "button:contains('로그인')",
            "button:contains('Login')",
            "button:contains('Sign In')",
            "button:contains('Sign in')",
            ".login-btn",
            ".btn-login",
            "#loginBtn",
            "#submitBtn"
        ]
    }
    
    # XPath 선택자들
    XPATH_SELECTORS = {
        'username_input': "//input[@name='userName']",
        'password_input': "//input[@name='password']",
        'login_button': "//button[@type='submit']",
        'login_form': "//form",
        'username_alt': "//input[@type='text']",
        'password_alt': "//input[@type='password']",
        'submit_button': "//input[@type='submit']"
    }
    
    @classmethod
    def get_username_selectors(cls):
        """사용자명 입력 필드 선택자 목록"""
        return cls.ALTERNATIVE_SELECTORS['username']
    
    @classmethod
    def get_password_selectors(cls):
        """비밀번호 입력 필드 선택자 목록"""
        return cls.ALTERNATIVE_SELECTORS['password']
    
    @classmethod
    def get_login_button_selectors(cls):
        """로그인 버튼 선택자 목록"""
        return cls.ALTERNATIVE_SELECTORS['login_button']
    
    @classmethod
    def get_all_form_selectors(cls):
        """모든 폼 관련 선택자"""
        return {
            'username': cls.get_username_selectors(),
            'password': cls.get_password_selectors(),
            'login_button': cls.get_login_button_selectors()
        }
    
    def get_field_selector(self, field_name: str) -> Optional[str]:
        """필드 이름으로 선택자 가져오기"""
        field_selectors = {
            'username': self.USERNAME_INPUT,
            'password': self.PASSWORD_INPUT,
            # 추가 필드들을 여기에 정의
            'title': 'input[name="title"]',
            'description': 'textarea[name="description"]',
            'priority': 'select[name="priority"]',
            'category': 'select[name="category"]',
            'assignee': 'input[name="assignee"]',
            'due_date': 'input[name="dueDate"]',
        }
        return field_selectors.get(field_name)
    
    def get_button_selector(self, button_name: str) -> Optional[str]:
        """버튼 이름으로 선택자 가져오기"""
        button_selectors = {
            'login': self.LOGIN_BUTTON,
            'submit': 'button[type="submit"]',
            'save': 'button:contains("저장")',
            'cancel': 'button:contains("취소")',
            'confirm': 'button:contains("확인")',
            'add': 'button:contains("추가")',
            'edit': 'button:contains("수정")',
            'delete': 'button:contains("삭제")',
            'search': 'button:contains("검색")',
            'reset': 'button:contains("초기화")',
        }
        return button_selectors.get(button_name)
    
    def get_select_selector(self, select_name: str) -> Optional[str]:
        """셀렉트 이름으로 선택자 가져오기"""
        select_selectors = {
            'priority': 'select[name="priority"]',
            'category': 'select[name="category"]',
            'status': 'select[name="status"]',
            'type': 'select[name="type"]',
            'department': 'select[name="department"]',
        }
        return select_selectors.get(select_name) 