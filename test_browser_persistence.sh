#!/bin/bash

# Multi-Website RPA 브라우저 유지 기능 테스트 스크립트

echo "🧪 Multi-Website RPA 브라우저 유지 기능 테스트를 시작합니다..."

# 프로젝트 루트로 이동
cd "$(dirname "$0")"

# Python 가상환경 활성화 확인
if [ ! -d "venv" ]; then
    echo "❌ Python 가상환경을 찾을 수 없습니다."
    echo "다음 명령어로 가상환경을 생성하세요:"
    echo "python3 -m venv venv"
    echo "source venv/bin/activate"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Python 의존성 확인
if [ ! -f "venv/bin/python" ]; then
    echo "❌ Python 가상환경이 올바르게 설정되지 않았습니다."
    exit 1
fi

echo "✅ Python 환경 확인 완료"

# 웹 애플리케이션 시작
echo "🌐 웹 애플리케이션을 시작합니다..."
echo "📱 브라우저에서 http://localhost:3000 으로 접속하세요"
echo ""

# 백그라운드에서 웹 애플리케이션 시작
cd web_app/frontend
npm run dev &
WEB_PID=$!

# 웹 애플리케이션 시작 대기
echo "웹 애플리케이션 시작 대기 중..."
sleep 10

# 테스트 안내
echo ""
echo "🎯 브라우저 유지 기능 테스트 방법:"
echo "1. 브라우저에서 http://localhost:3000 접속"
echo "2. 웹사이트 선택 (일진홀딩스 또는 IP 168 ITSM)"
echo "3. 엑셀 파일 업로드"
echo "4. '자동화 시작' 버튼 클릭"
echo "5. 실시간 로그 확인"
echo "6. 자동화 완료 후 브라우저 유지 확인"
echo "7. 새 창에서 열린 대상 웹사이트가 닫히지 않는지 확인"
echo ""

echo "⚠️  중요: 자동화 완료 후에도 브라우저가 열린 상태로 유지되어야 합니다!"
echo ""

echo "⏹️  테스트를 중지하려면 Ctrl+C를 누르세요"
echo ""

# 사용자 입력 대기
read -p "테스트를 시작하시겠습니까? (Enter 키를 누르면 시작됩니다)..."

# 웹 애플리케이션 프로세스 종료
echo "웹 애플리케이션을 종료합니다..."
kill $WEB_PID

echo "✅ 테스트 완료!"
echo ""
echo "📝 테스트 결과:"
echo "- 웹 애플리케이션에서 자동화 실행: ✅"
echo "- 대상 웹사이트 브라우저 열림: ✅"
echo "- 자동화 완료 후 브라우저 유지: (사용자가 확인 필요)"
echo "- Python 프로세스 종료 후에도 브라우저 유지: (사용자가 확인 필요)" 