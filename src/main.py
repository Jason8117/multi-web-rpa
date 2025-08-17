"""
다중 웹사이트 RPA 시스템 메인 실행 파일
"""

import sys
import argparse
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.config_manager import ConfigManager
from core.plugin_manager import PluginManager
from core.excel_processor import ExcelProcessor
from utils.logger import setup_logger
from loguru import logger


def test_iljin_holdings_automation(input_file=None, keep_browser=True):
    """일진홀딩스 웹사이트 자동화 테스트"""
    try:
        logger.info("=== 일진홀딩스 자동화 테스트 시작 ===")
        
        # 설정 관리자 초기화
        config_manager = ConfigManager()
        
        # 일진홀딩스 웹사이트 설정 가져오기
        website_id = "iljin_holdings"
        website_config = config_manager.get_website_config(website_id)
        
        if not website_config:
            logger.error(f"웹사이트 설정을 찾을 수 없습니다: {website_id}")
            return False
        
        # 엑셀 데이터 읽기
        excel_processor = ExcelProcessor(config_manager.get_global_config())
        
        # 입력 파일이 지정된 경우 해당 파일 사용, 아니면 기본 파일 사용
        excel_filename = input_file if input_file else "sample_data.xlsx"
        excel_data = excel_processor.read_excel_file(excel_filename)
        
        if not excel_data:
            logger.error(f"엑셀 데이터를 읽을 수 없습니다: {excel_filename}")
            return False
        
        # 데이터 검증
        if not excel_processor.verify_excel_data(excel_data):
            logger.error("엑셀 데이터 검증 실패")
            return False
        
        # 방문객 정보 읽기
        visitor_data = excel_processor.read_visitor_data(excel_filename)
        
        if not visitor_data:
            logger.warning("방문객 정보를 읽을 수 없습니다. 신청자 정보만 입력합니다.")
        
        # 일진홀딩스 자동화 인스턴스 생성
        from websites.iljin_holdings.automation import IljinHoldingsAutomation
        automation = IljinHoldingsAutomation(website_config)
        
        # 브라우저 유지 설정
        automation.set_keep_browser(keep_browser)
        
        # 첫 번째 행 데이터로 테스트
        test_data = excel_data[0]
        logger.info(f"엑셀에서 읽은 테스트 데이터: {test_data}")
        
        # 자동화 실행 (신청자 정보 입력) - keep_browser 파라미터 전달
        success = automation.run_automation(test_data, keep_browser)
        
        if success and visitor_data:
            logger.info("신청자 정보 입력 완료. 방문객 정보 입력을 시작합니다.")
            
            # 방문객 정보 입력
            visitor_success = automation.fill_visitor_information(visitor_data, test_data)
            
            if visitor_success:
                logger.info("✅ 방문객 정보 입력 완료!")
            else:
                logger.warning("⚠️ 방문객 정보 입력에 실패했습니다.")
        
        if success:
            logger.info("✅ 일진홀딩스 자동화 테스트 성공!")
        else:
            logger.error("❌ 일진홀딩스 자동화 테스트 실패")
        
        # 웹에서 호출된 경우 브라우저 유지, 콘솔에서 호출된 경우 사용자 입력 대기
        if keep_browser:
            logger.info("브라우저가 열린 상태로 유지됩니다. 웹에서 다음 작업을 진행할 수 있습니다.")
        else:
            logger.info("브라우저가 열린 상태로 유지됩니다. 확인 후 수동으로 닫아주세요.")
            input("엔터 키를 누르면 브라우저가 닫힙니다...")
            automation.cleanup()
        
        return success
        
    except Exception as e:
        logger.error(f"일진홀딩스 자동화 테스트 오류: {e}")
        return False


def test_ip168_itsm_name_field(input_file=None, keep_browser=True):
    """IP 168 ITSM 웹사이트 성명 필드 테스트"""
    try:
        logger.info("=== IP 168 ITSM 성명 필드 테스트 시작 ===")
        
        # 설정 관리자 초기화
        config_manager = ConfigManager()
        
        # IP 168 ITSM 웹사이트 설정 가져오기
        website_id = "ip_168_itsm"
        website_config = config_manager.get_website_config(website_id)
        
        if not website_config:
            logger.error(f"웹사이트 설정을 찾을 수 없습니다: {website_id}")
            return False
        
        # IP 168 ITSM 자동화 인스턴스 생성
        from websites.ip_168_itsm.automation import IP168ITSMAutomation
        automation = IP168ITSMAutomation(website_config)
        
        # 브라우저 유지 설정
        automation.set_keep_browser(keep_browser)
        
        # 1. 성명 필드 테스트
        logger.info("성명 필드 테스트 시작...")
        
        # 1-1. 기본 테스트 메서드
        if automation.test_name_field("홍길동"):
            logger.info("✅ 성명 필드 기본 테스트 메서드 성공")
        else:
            logger.warning("⚠️ 성명 필드 기본 테스트 메서드 실패")
        
        # 1-2. 특별 처리 메서드
        if automation.test_name_field_specific("김철수"):
            logger.info("✅ 성명 필드 특별 처리 메서드 성공")
        else:
            logger.warning("⚠️ 특별 처리 메서드 실패")
        
        # 2. 이메일 필드 테스트
        logger.info("이메일 필드 테스트 시작...")
        
        # 2-1. 기본 테스트 메서드
        if automation.test_email_field("test@example.com"):
            logger.info("✅ 이메일 필드 기본 테스트 메서드 성공")
        else:
            logger.warning("⚠️ 이메일 필드 기본 테스트 메서드 실패")
        
        # 2-2. 특별 처리 메서드
        if automation.test_email_field_specific("user@example.com"):
            logger.info("✅ 이메일 필드 특별 처리 메서드 성공")
        else:
            logger.warning("⚠️ 이메일 필드 특별 처리 메서드 실패")
        
        # 3. 비밀번호 필드 테스트
        logger.info("비밀번호 필드 테스트 시작...")
        
        # 3-1. 기본 테스트 메서드
        if automation.test_password_field("TestPassword123!"):
            logger.info("✅ 비밀번호 필드 기본 테스트 메서드 성공")
        else:
            logger.warning("⚠️ 비밀번호 필드 기본 테스트 메서드 실패")
        
        # 3-2. 특별 처리 메서드
        if automation.test_password_field_specific("SecurePass456!"):
            logger.info("✅ 비밀번호 필드 특별 처리 메서드 성공")
        else:
            logger.warning("⚠️ 특별 처리 메서드 실패")
        
        # 4. 사용자 ID 필드 테스트
        logger.info("사용자 ID 필드 테스트 시작...")
        
        # 4-1. 정확한 선택자 테스트 메서드
        if automation.test_user_id_field_with_exact_selectors("testuser@example.com"):
            logger.info("✅ 사용자 ID 필드 정확한 선택자 테스트 메서드 성공")
        else:
            logger.warning("⚠️ 사용자 ID 필드 정확한 선택자 테스트 메서드 실패")
        
        # 4-2. 특별 처리 메서드 (중복확인 포함)
        if automation.fill_user_id_field_specific("another@example.com"):
            logger.info("✅ 사용자 ID 필드 특별 처리 메서드 성공")
        else:
            logger.warning("⚠️ 사용자 ID 필드 특별 처리 메서드 실패")
        
        # 4-3. 중복확인 포함 테스트 메서드
        if automation.test_user_id_with_duplicate_check("newuser@example.com"):
            logger.info("✅ 사용자 ID 중복확인 포함 테스트 성공")
        else:
            logger.warning("⚠️ 사용자 ID 중복확인 포함 테스트 실패")
        
        # 5. 법인 필드 테스트
        logger.info("법인 필드 테스트 시작...")
        
        # 5-1. 법인 필드 테스트 메서드
        if automation.test_company_field_specific("일진홀딩스"):
            logger.info("✅ 법인 필드 테스트 성공")
        else:
            logger.warning("⚠️ 법인 필드 테스트 실패")
        
        # 6. 전체 회원가입 자동화 테스트
        logger.info("=== 전체 회원가입 자동화 테스트 시작 ===")
        
        # 6-1. 엑셀 파일의 모든 사용자 회원가입
        result = automation.register_all_users_from_excel()
        
        if result['success']:
            logger.info(f"✅ 전체 회원가입 완료!")
            logger.info(f"총 {result['total_users']}명 중 성공: {result['success_count']}명, 실패: {result['failed_count']}명")
            
            # 상세 결과 출력
            for i, user_result in enumerate(result['results']):
                status = "✅ 성공" if user_result['success'] else "❌ 실패"
                logger.info(f"사용자 {i+1}: {status}")
        else:
            logger.error(f"❌ 전체 회원가입 실패: {result['message']}")
        
        logger.info("=== 전체 회원가입 자동화 테스트 완료 ===")
        
        # 웹에서 호출된 경우 브라우저 유지, 콘솔에서 호출된 경우 사용자 입력 대기
        if keep_browser:
            logger.info("🎉 IP 168 ITSM 자동화가 성공적으로 완료되었습니다!")
            logger.info("🌐 브라우저가 열린 상태로 유지됩니다.")
            logger.info("💡 웹에서 직접 다음 작업을 진행할 수 있습니다.")
            logger.info("📝 자동화 결과를 확인하고 필요한 경우 수동으로 조정하세요.")
            logger.info("⚠️  브라우저를 닫으려면 수동으로 닫기 버튼을 클릭하세요.")
        else:
            logger.info("브라우저가 열린 상태로 유지됩니다. 확인 후 수동으로 닫아주세요.")
            input("엔터 키를 누르면 브라우저가 닫힙니다...")
            automation.cleanup()
        
        return True
        
    except Exception as e:
        logger.error(f"IP 168 ITSM 성명 필드 테스트 오류: {e}")
        return False


def run_website_automation(website_id, input_file=None, keep_browser=True):
    """웹에서 호출할 때 사용하는 통합 자동화 함수"""
    try:
        logger.info(f"=== {website_id} 자동화 시작 ===")
        
        if website_id == "iljin_holdings":
            return test_iljin_holdings_automation(input_file, keep_browser)
        elif website_id == "ip_168_itsm":
            return test_ip168_itsm_name_field(input_file, keep_browser)
        else:
            logger.error(f"지원하지 않는 웹사이트입니다: {website_id}")
            return False
            
    except Exception as e:
        logger.error(f"{website_id} 자동화 실행 중 오류: {e}")
        return False


def main():
    """메인 실행 함수"""
    try:
        # 로거 설정
        logger = setup_logger()
        logger.info("=== 다중 웹사이트 RPA 시스템 시작 ===")
        
        # 명령행 인수 파싱
        parser = argparse.ArgumentParser(description='다중 웹사이트 RPA 시스템')
        parser.add_argument('--website', type=str, help='실행할 웹사이트 ID')
        parser.add_argument('--test', action='store_true', help='테스트 모드')
        parser.add_argument('--input-file', type=str, help='입력 엑셀 파일 경로')
        parser.add_argument('--web-mode', action='store_true', help='웹 모드 (브라우저 유지)')
        
        args = parser.parse_args()
        
        # 웹에서 호출된 경우 (--website 인수가 있는 경우)
        if args.website:
            logger.info(f"웹에서 선택된 웹사이트: {args.website}")
            success = run_website_automation(
                args.website, 
                args.input_file, 
                keep_browser=args.web_mode or True
            )
            
            if success:
                logger.info(f"{args.website} 자동화가 성공적으로 완료되었습니다.")
            else:
                logger.error(f"{args.website} 자동화가 실패했습니다.")
            return
        
        # 콘솔에서 호출된 경우 (기존 방식)
        print("\n=== 테스트할 웹사이트를 선택하세요 ===")
        print("1. 일진홀딩스 자동화 테스트")
        print("2. IP 168 ITSM 성명 필드 테스트")
        
        choice = input("\n선택 (1 또는 2): ").strip()
        
        if choice == "1":
            # 일진홀딩스 자동화 테스트 실행
            if test_iljin_holdings_automation(keep_browser=False):
                logger.info("일진홀딩스 자동화 테스트가 성공적으로 완료되었습니다.")
            else:
                logger.error("일진홀딩스 자동화 테스트가 실패했습니다.")
        elif choice == "2":
            # IP 168 ITSM 성명 필드 테스트 실행
            if test_ip168_itsm_name_field(keep_browser=False):
                logger.info("IP 168 ITSM 성명 필드 테스트가 성공적으로 완료되었습니다.")
            else:
                logger.error("IP 168 ITSM 성명 필드 테스트가 실패했습니다.")
        else:
            logger.error("잘못된 선택입니다. 1 또는 2를 입력해주세요.")
        
    except Exception as e:
        logger.error(f"RPA 시스템 실행 중 오류: {e}")
        raise


if __name__ == "__main__":
    main() 