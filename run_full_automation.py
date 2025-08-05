#!/usr/bin/env python3
"""
IP 168 ITSM 전체 자동화 프로세스 실행 스크립트
엑셀 파일의 모든 사용자를 자동으로 회원가입 처리
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트 경로를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.config_manager import ConfigManager
from src.websites.ip_168_itsm.automation import IP168ITSMAutomation
from src.utils.logger import setup_logger

def run_full_automation():
    """전체 자동화 프로세스 실행"""
    try:
        # 로거 설정
        logger = setup_logger()
        logger.info("=== IP 168 ITSM 전체 자동화 프로세스 시작 ===")
        
        # 1. 설정 로드
        logger.info("1. 설정 로드 중...")
        config_manager = ConfigManager()
        config_manager.load_configs()
        
        # 설정 로드 결과 확인
        global_config = config_manager.get_global_config()
        website_registry = config_manager.get_website_registry()
        
        if not global_config or not website_registry:
            logger.error("❌ 설정 로드 실패")
            return False
        
        logger.info("✅ 설정 로드 완료")
        
        # 2. 자동화 객체 생성
        logger.info("2. 자동화 객체 생성 중...")
        
        # IP 168 ITSM 웹사이트 설정 가져오기
        website_config = config_manager.get_website_config('ip_168_itsm')
        if not website_config:
            logger.error("❌ IP 168 ITSM 웹사이트 설정 로드 실패")
            return False
            
        automation = IP168ITSMAutomation(website_config)
        logger.info("✅ 자동화 객체 생성 완료")
        
        # 3. 전체 사용자 회원등록 실행
        logger.info("3. 전체 사용자 회원등록 시작...")
        result = automation.register_all_users_from_excel()
        
        if result['success']:
            logger.info("=== 회원등록 결과 요약 ===")
            logger.info(f"총 사용자 수: {result['total_users']}")
            logger.info(f"성공: {result['success_count']}명")
            logger.info(f"실패: {result['failed_count']}명")
            
            if result['failed_count'] > 0:
                logger.info("실패한 사용자 상세:")
                for failed_user in result['results']:
                    if not failed_user['success']:
                        logger.warning(f"  - 행 {failed_user['row_index']+1}: {failed_user['reason']}")
            
            logger.info("✅ 전체 자동화 프로세스 완료!")
            return True
        else:
            logger.error(f"❌ 전체 자동화 프로세스 실패: {result['message']}")
            return False
            
    except Exception as e:
        logger.error(f"전체 자동화 프로세스 오류: {e}")
        return False

def main():
    """메인 함수"""
    print("🚀 IP 168 ITSM 전체 자동화 프로세스를 시작합니다...")
    print("📋 이 프로세스는 엑셀 파일의 모든 사용자를 자동으로 회원가입 처리합니다.")
    print("⚠️  실행하기 전에 다음 사항을 확인해주세요:")
    print("   1. 엑셀 파일이 올바른 형식으로 준비되어 있는지")
    print("   2. 네트워크 연결이 안정적인지")
    print("   3. 웹사이트 접속이 가능한지")
    print()
    
    # 사용자 확인
    confirm = input("계속 진행하시겠습니까? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ 자동화 프로세스가 취소되었습니다.")
        return
    
    # 자동화 실행
    success = run_full_automation()
    
    if success:
        print("🎉 전체 자동화 프로세스가 성공적으로 완료되었습니다!")
    else:
        print("❌ 전체 자동화 프로세스 실행 중 오류가 발생했습니다.")
        print("로그를 확인하여 문제를 해결해주세요.")
    
    # 브라우저 유지 (선택사항)
    keep_browser = input("브라우저를 열어둘까요? (y/N): ").strip().lower()
    if keep_browser not in ['y', 'yes']:
        try:
            automation.cleanup()
            print("✅ 브라우저가 종료되었습니다.")
        except:
            pass

if __name__ == "__main__":
    main() 