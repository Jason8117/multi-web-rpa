#!/bin/bash

# Multi-Website RPA Web App 시작 스크립트

echo "🚀 Multi-Website RPA Web App을 시작합니다..."

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

# 프론트엔드 디렉토리로 이동
cd web_app/frontend

# 의존성 설치 확인
if [ ! -d "node_modules" ]; then
    echo "📦 Node.js 의존성을 설치합니다..."
    npm install
fi

# 개발 서버 시작
echo "🌐 개발 서버를 시작합니다..."
echo "📱 브라우저에서 http://localhost:3000 으로 접속하세요"
echo "⏹️  서버를 중지하려면 Ctrl+C를 누르세요"
echo ""

npm run dev 