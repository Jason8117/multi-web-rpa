# IP 168 ITSM 웹사이트 자동화

이 모듈은 `http://4.144.198.168/sign-in` 웹사이트에 대한 자동 로그인 및 회원등록 기능을 제공합니다.

## 기능

- 웹사이트 자동 접속
- 로그인 정보 자동 입력
- 로그인 버튼 자동 클릭
- 로그인 성공 여부 확인
- **언어 자동 선택** (로그인 페이지에서 한국어 선택)
- **메뉴 네비게이션** (시스템관리 > 회원관리 메뉴로 이동)
- **엑셀 데이터 처리** (회원 정보 자동 읽기)
- **회원등록 자동화** (엑셀 데이터 기반 폼 자동 입력)
- **일괄 회원등록** (여러 사용자 순차 처리)
- 스크린샷 촬영 기능
- **브라우저 유지 모드** (로그인 후 브라우저 유지)
- **추가 자동 입력 기능** (폼 입력, 버튼 클릭, 옵션 선택)
- **대화형 자동화** (실시간 상호작용)

## 설정

### 기본 로그인 정보
- **사용자명**: `ij_itsmadmin`
- **비밀번호**: `0`

### 설정 파일 (`config.yaml`)
```yaml
website:
  name: "IP 168 ITSM"
  url: "http://4.144.198.168/sign-in"
  requires_login: true
  timeout: 10

login:
  username: "ij_itsmadmin"
  password: "0"
```

## 사용법

### 1. 기본 실행
```bash
cd multi_website_rpa/src/websites/ip_168_itsm
python run_automation.py
```

### 2. 사용자 정의 로그인 정보로 실행
```bash
python run_automation.py --username "your_username" --password "your_password"
```

### 3. 스크린샷과 함께 실행
```bash
python run_automation.py --screenshot
```

### 4. 테스트 모드 실행
```bash
python run_automation.py --test
```

### 5. 브라우저 유지 모드 (기본값)
```bash
python run_automation.py
```

### 6. 자동화 완료 후 브라우저 닫기
```bash
python run_automation.py --close-browser
```

### 7. 언어 선택 비활성화
```bash
python run_automation.py --no-language-select
```

### 8. 목표 페이지 이동 비활성화
```bash
python run_automation.py --no-navigate
```

### 9. 고급 자동화 실행
```bash
# 대화형 모드 (기본값)
python advanced_automation.py

# 폼 입력 예제
python advanced_automation.py --mode form

# 메뉴 네비게이션 예제
python advanced_automation.py --mode menu
```

### 10. 엑셀 데이터 확인
```bash
python excel_reader.py
```

## 파일 구조

```
ip_168_itsm/
├── __init__.py              # 모듈 초기화
├── automation.py            # 메인 자동화 로직
├── config.yaml              # 설정 파일
├── element_selectors.py     # 웹 요소 선택자 정의
├── excel_reader.py          # 엑셀 데이터 리더
├── test_automation.py       # 테스트 스크립트
├── run_automation.py        # 실행 스크립트
├── advanced_automation.py   # 고급 자동화 스크립트
└── README.md               # 이 파일
```

## 주요 클래스

### IP168ITSMAutomation
메인 자동화 클래스로 다음 메서드들을 제공합니다:

- `setup_driver()`: 웹드라이버 설정
- `navigate_to_website()`: 웹사이트 접속
- `login()`: 로그인 수행
- `select_language_on_login_page()`: 로그인 페이지에서 언어 선택
- `navigate_to_system_management()`: 시스템관리 메뉴로 이동
- `navigate_to_member_registration()`: 회원등록 메뉴로 이동
- `navigate_to_target_page()`: 목표 페이지로 이동
- `analyze_registration_form()`: 회원등록 폼 분석
- `fill_registration_form()`: 회원등록 폼 자동 입력
- `submit_registration_form()`: 회원등록 폼 제출
- `register_user_from_excel()`: 엑셀에서 사용자 데이터로 회원등록
- `register_all_users_from_excel()`: 엑셀의 모든 사용자 회원등록
- `run_automation()`: 전체 자동화 실행
- `take_screenshot()`: 스크린샷 촬영
- `fill_form_data()`: 폼 데이터 입력
- `fill_field()`: 개별 필드 입력
- `click_button()`: 버튼 클릭
- `select_option()`: 옵션 선택
- `get_current_page_info()`: 현재 페이지 정보
- `wait_for_user_input()`: 사용자 입력 대기

### ITSMExcelReader
엑셀 데이터 처리 클래스로 다음 메서드들을 제공합니다:

- `load_excel_file()`: 엑셀 파일 로드
- `get_user_data_list()`: 사용자 데이터 리스트 반환
- `get_user_data_by_index()`: 인덱스로 특정 사용자 데이터 반환
- `get_excel_info()`: 엑셀 파일 정보 반환
- `validate_user_data()`: 사용자 데이터 유효성 검사

### IP168ITSMSelectors
웹 요소 선택자를 정의하는 클래스입니다:

- 다양한 웹사이트 구조에 대응하는 대체 선택자들
- CSS 선택자와 XPath 선택자 모두 지원
- 폴백 메커니즘으로 안정성 향상

## 로그

자동화 과정의 모든 단계가 로그로 기록됩니다:

- 웹사이트 접속 상태
- 로그인 시도 결과
- 에러 메시지
- 성공/실패 여부

## 에러 처리

- 네트워크 연결 오류
- 웹 요소를 찾을 수 없는 경우
- 로그인 실패
- 타임아웃 오류

모든 에러는 적절히 처리되고 로그에 기록됩니다.

## 테스트

테스트 스크립트를 통해 다음 항목들을 검증할 수 있습니다:

1. 웹사이트 접속 테스트
2. 기본 로그인 테스트
3. 사용자 정의 로그인 정보 테스트

```bash
python test_automation.py
```

## 엑셀 파일 형식

회원등록을 위한 엑셀 파일은 `data/input/itsm_user_reg_template.xlsx` 형식을 따릅니다:

- **헤더**: 2번째 행에 컬럼명
- **데이터**: 3번째 행부터 회원 정보
- **필수 필드**: `per_nm` (사용자명), `email` (이메일)
- **선택 필드**: `per_id`, `comp_cd`, `dept_cd`, `per_work`, `phone`, `mobile`, `사번`, `부서명`, `계열사` 등

## 의존성

- Selenium WebDriver
- Loguru (로깅)
- PyYAML (설정 파일)
- Pandas (엑셀 데이터 처리)
- 기타 프로젝트 공통 의존성

## 주의사항

1. 웹사이트 구조가 변경될 경우 `selectors.py` 파일을 업데이트해야 합니다.
2. 로그인 정보는 보안을 위해 환경 변수나 별도 설정 파일로 관리하는 것을 권장합니다.
3. 자동화 실행 시 웹사이트의 이용약관을 준수해야 합니다. 