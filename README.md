# Multi-Website RPA (Robotic Process Automation)

웹사이트 자동화를 위한 Python 기반 RPA 시스템입니다. 다양한 웹사이트에서 반복적인 작업을 자동화할 수 있습니다.

## 🚀 주요 기능

- **다중 웹사이트 지원**: 다양한 웹사이트에 대한 자동화 스크립트 제공
- **엑셀 데이터 연동**: 엑셀 파일에서 데이터를 읽어와 자동 입력
- **Vue.js 지원**: Vue.js 기반 웹사이트와의 상호작용 최적화
- **스마트 요소 탐지**: JavaScript, CSS 선택자, XPath 등 다양한 방법으로 웹 요소 탐지
- **로깅 시스템**: 상세한 로그를 통한 디버깅 지원
- **에러 처리**: 강력한 예외 처리 및 재시도 메커니즘

## 📋 지원하는 웹사이트

### 1. 일진홀딩스 (Iljin Holdings)
- **URL**: http://visit.iljin.co.kr
- **기능**: 방문신청 자동화
  - 신청자 정보 입력
  - 방문객 정보 입력 (최대 20명)
  - 차량정보 등록
  - 개인정보 동의 체크박스 자동 체크

### 2. IP 168 ITSM
- **기능**: ITSM 시스템 자동화
  - 성명 필드 테스트

## 🛠️ 설치 및 설정

### 1. 시스템 요구사항
- Python 3.8 이상
- Chrome 브라우저
- ChromeDriver (자동 설치됨)

### 2. 프로젝트 클론
```bash
git clone https://github.com/[your-username]/multi_website_rpa.git
cd multi_website_rpa
```

### 3. 가상환경 생성 및 활성화
```bash
python3.12 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows
```

### 4. 의존성 설치
```bash
pip install -r requirements.txt
```

## 📖 사용법

### 1. 기본 실행
```bash
python src/main.py --website [website_name] --test
```

### 2. 일진홀딩스 자동화 실행
```bash
python src/main.py --website iljin_holdings --test
```

### 3. IP 168 ITSM 테스트 실행
```bash
python src/main.py --website ip_168_itsm --test
```

## 📁 프로젝트 구조

```
multi_website_rpa/
├── src/
│   ├── main.py                 # 메인 실행 파일
│   ├── core/
│   │   ├── base_automation.py  # 기본 자동화 클래스
│   │   ├── config_manager.py   # 설정 관리
│   │   └── excel_processor.py  # 엑셀 파일 처리
│   ├── utils/
│   │   └── logger.py           # 로깅 유틸리티
│   └── websites/
│       ├── iljin_holdings/     # 일진홀딩스 자동화
│       ├── ip_168_itsm/        # IP 168 ITSM 자동화
│       └── company_b/          # 기타 회사 자동화
├── config/
│   ├── global_config.yaml      # 전역 설정
│   └── website_registry.yaml   # 웹사이트 등록 정보
├── data/
│   ├── input/                  # 입력 데이터 (엑셀 파일)
│   └── output/                 # 출력 데이터
├── logs/                       # 로그 파일
├── tests/                      # 테스트 파일
└── requirements.txt            # Python 의존성
```

## 📊 엑셀 데이터 형식

### 일진홀딩스 방문신청 데이터
- **파일**: `data/input/sample_data.xlsx`
- **시트 1**: 신청자 정보
  - 방문사업장, 피방문자 연락처, 피방문자, 신청자, 연락처, 소속회사, 회사주소, 방문기간, 방문목적, 내용
- **시트 2**: 방문객 정보 (5번째 행부터)
  - 성명, 휴대폰번호, 차종, 차량번호

## 🔧 설정 파일

### global_config.yaml
```yaml
browser:
  headless: false
  window_size: [1920, 1080]
  implicit_wait: 10
  page_load_timeout: 30

logging:
  level: INFO
  format: "%(asctime)s | %(levelname)s | %(message)s"
```

### website_registry.yaml
```yaml
websites:
  iljin_holdings:
    name: "일진홀딩스"
    url: "http://visit.iljin.co.kr"
    automation_class: "IljinHoldingsAutomation"
  ip_168_itsm:
    name: "IP 168 ITSM"
    url: "http://ip168.com"
    automation_class: "IP168ITSMAutomation"
```

## 🐛 문제 해결

### 일반적인 문제들

1. **ChromeDriver 오류**
   ```bash
   # ChromeDriver 자동 업데이트
   pip install --upgrade webdriver-manager
   ```

2. **요소를 찾을 수 없음**
   - 페이지 로딩 시간 증가
   - 요소 선택자 확인
   - JavaScript 실행 대기

3. **Vue.js 요소 상호작용 문제**
   - Vue.js v-model 이벤트 시뮬레이션
   - 컴포넌트 인스턴스 직접 접근

## 📝 로그 확인

로그 파일은 `logs/` 디렉토리에 저장됩니다:
- `logs/automation/rpa_automation.log`: 일반 로그
- `logs/errors/error.log`: 오류 로그
- `logs/screenshots/`: 스크린샷 (오류 발생 시)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

---

**주의사항**: 이 도구는 교육 및 테스트 목적으로 제작되었습니다. 실제 운영 환경에서 사용하기 전에 충분한 테스트를 진행하시기 바랍니다. 