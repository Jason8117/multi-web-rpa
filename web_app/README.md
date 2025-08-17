# Multi-Website RPA Web Application

웹 기반으로 RPA 자동화를 실행할 수 있는 Next.js 애플리케이션입니다.

## 🚀 주요 기능

- **웹 기반 인터페이스**: 브라우저에서 직관적으로 RPA 자동화 실행
- **실시간 로그**: 자동화 진행 상황을 실시간으로 확인
- **브라우저 유지**: 자동화 완료 후 브라우저를 열린 상태로 유지하여 다음 작업 진행 가능
- **파일 업로드**: 엑셀 파일을 직접 업로드하여 자동화 실행
- **다중 웹사이트 지원**: 일진홀딩스, IP 168 ITSM 등 다양한 웹사이트 지원

## 🛠️ 설치 및 실행

### 1. 시스템 요구사항

- Node.js 18.0.0 이상
- Python 3.8 이상 (RPA 백엔드용)
- Chrome 브라우저

### 2. 빠른 시작

```bash
# 프로젝트 루트에서 실행
cd multi_website_rpa/web_app

# 시작 스크립트 실행 (권장)
./start_web_app.sh

# 또는 수동으로 실행
cd frontend
npm install
npm run dev
```

### 3. 수동 설치 및 실행

```bash
# 1. 프론트엔드 디렉토리로 이동
cd multi_website_rpa/web_app/frontend

# 2. 의존성 설치
npm install

# 3. 개발 서버 시작
npm run dev

# 4. 브라우저에서 접속
# http://localhost:3000
```

## 📖 사용법

### 1. 웹사이트 선택
- **일진홀딩스**: 방문신청 자동화
- **IP 168 ITSM**: ITSM 시스템 자동화

### 2. 엑셀 파일 업로드
- `.xlsx` 또는 `.xls` 형식의 파일 업로드
- 자동화에 필요한 데이터가 포함된 엑셀 파일

### 3. 자동화 실행
- "자동화 시작" 버튼 클릭
- 실시간으로 진행 상황 확인
- 로그를 통해 각 단계별 실행 결과 확인

### 4. 자동화 완료 후
- 브라우저가 열린 상태로 유지
- 웹에서 직접 다음 작업 진행 가능
- "새 자동화 시작" 버튼으로 새로운 자동화 실행

## 🔧 기술 스택

- **프론트엔드**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **백엔드**: Python (RPA 자동화)
- **통신**: HTTP API, Server-Sent Events
- **파일 처리**: Excel 파일 업로드 및 처리

## 📁 프로젝트 구조

```
web_app/
├── frontend/                 # Next.js 프론트엔드
│   ├── app/                 # App Router
│   │   ├── page.tsx        # 메인 페이지
│   │   └── api/            # API 라우트
│   │       └── run-automation/  # 자동화 실행 API
│   ├── package.json        # Node.js 의존성
│   └── next.config.ts      # Next.js 설정
├── backend/                 # 백엔드 (향후 확장 예정)
├── shared/                 # 공유 모듈
└── start_web_app.sh        # 시작 스크립트
```

## 🌐 API 엔드포인트

### POST /api/run-automation

자동화를 실행하는 API 엔드포인트입니다.

**요청 파라미터:**
- `website`: 웹사이트 ID (iljin_holdings, ip_168_itsm)
- `file`: 엑셀 파일

**응답:**
- 스트리밍 텍스트 응답으로 실시간 로그 제공
- 자동화 완료 후 브라우저 유지

## 🔄 워크플로우

1. **웹사이트 선택**: 자동화할 웹사이트 선택
2. **파일 업로드**: 엑셀 데이터 파일 업로드
3. **자동화 실행**: Python 백엔드에서 RPA 자동화 실행
4. **실시간 모니터링**: 웹에서 진행 상황 실시간 확인
5. **브라우저 유지**: 자동화 완료 후 브라우저 열린 상태 유지
6. **다음 작업**: 웹에서 직접 추가 작업 진행

## 🐛 문제 해결

### 일반적인 문제들

1. **포트 충돌**
   ```bash
   # 다른 포트로 실행
   npm run dev -- -p 3001
   ```

2. **Python 경로 문제**
   - Python 가상환경이 올바르게 설정되어 있는지 확인
   - `multi_website_rpa/venv/bin/python` 경로 확인

3. **파일 업로드 실패**
   - 파일 크기 제한 확인
   - 파일 형식이 `.xlsx` 또는 `.xls`인지 확인

4. **자동화 실행 실패**
   - 로그를 통해 구체적인 오류 메시지 확인
   - Python 백엔드 로그 확인

## 🚀 배포

### 개발 환경
```bash
npm run dev
```

### 프로덕션 빌드
```bash
npm run build
npm run start
```

### Vercel 배포
```bash
# Vercel CLI 설치
npm i -g vercel

# 배포
vercel
```

## 📝 개발 가이드

### 새로운 웹사이트 추가

1. `src/websites/` 디렉토리에 새로운 웹사이트 모듈 추가
2. `src/main.py`에 새로운 웹사이트 함수 추가
3. `run_website_automation` 함수에 새로운 웹사이트 케이스 추가
4. 프론트엔드 `websites` 배열에 새로운 웹사이트 정보 추가

### API 확장

1. `app/api/` 디렉토리에 새로운 API 엔드포인트 추가
2. 필요한 경우 새로운 Python 스크립트 함수 추가
3. 프론트엔드에서 새로운 API 호출 추가

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

---

**주의사항**: 이 도구는 교육 및 테스트 목적으로 제작되었습니다. 실제 운영 환경에서 사용하기 전에 충분한 테스트를 진행하시기 바랍니다. 