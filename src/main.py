"""
다중 웹사이트 RPA 시스템 메인 실행 파일
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.config_manager import ConfigManager
from core.plugin_manager import PluginManager
from core.excel_processor import ExcelProcessor
from utils.logger import setup_logger
from loguru import logger


def test_iljin_holdings_automation():
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
        excel_data = excel_processor.read_excel_file("sample_data.xlsx")
        
        if not excel_data:
            logger.error("엑셀 데이터를 읽을 수 없습니다")
            return False
        
        # 데이터 검증
        if not excel_processor.verify_excel_data(excel_data):
            logger.error("엑셀 데이터 검증 실패")
            return False
        
        # 방문객 정보 읽기
        visitor_data = excel_processor.read_visitor_data("sample_data.xlsx")
        
        if not visitor_data:
            logger.warning("방문객 정보를 읽을 수 없습니다. 신청자 정보만 입력합니다.")
        
        # 일진홀딩스 자동화 인스턴스 생성
        from websites.iljin_holdings.automation import IljinHoldingsAutomation
        automation = IljinHoldingsAutomation(website_config)
        
        # 첫 번째 행 데이터로 테스트
        test_data = excel_data[0]
        logger.info(f"엑셀에서 읽은 테스트 데이터: {test_data}")
        
        # 자동화 실행 (신청자 정보 입력)
        success = automation.run_automation(test_data)
        
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
        
        # 브라우저 유지 (결과 확인용)
        logger.info("브라우저가 열린 상태로 유지됩니다. 확인 후 수동으로 닫아주세요.")
        input("엔터 키를 누르면 브라우저가 닫힙니다...")
        automation.cleanup()
        
        return success
        
    except Exception as e:
        logger.error(f"일진홀딩스 자동화 테스트 오류: {e}")
        return False


def test_iljin_holdings_automation_web(input_file=None):
    """일진홀딩스 웹사이트 자동화 테스트 (웹용)"""
    try:
        logger.info("=== 일진홀딩스 자동화 테스트 시작 (웹용) ===")
        
        # 설정 관리자 초기화
        config_manager = ConfigManager()
        
        # 일진홀딩스 웹사이트 설정 가져오기
        website_id = "iljin_holdings"
        website_config = config_manager.get_website_config(website_id)
        
        if not website_config:
            logger.error(f"웹사이트 설정을 찾을 수 없습니다: {website_id}")
            return False
        
        # 파일 경로 설정
        if input_file and Path(input_file).exists():
            excel_file = input_file
            logger.info(f"웹에서 업로드된 파일 사용: {excel_file}")
        else:
            excel_file = "sample_data.xlsx"
            logger.info(f"기본 파일 사용: {excel_file}")
        
        # 엑셀 데이터 읽기
        excel_processor = ExcelProcessor(config_manager.get_global_config())
        excel_data = excel_processor.read_excel_file(excel_file)
        
        if not excel_data:
            logger.error("엑셀 데이터를 읽을 수 없습니다")
            return False
        
        # 데이터 검증
        if not excel_processor.verify_excel_data(excel_data):
            logger.error("엑셀 데이터 검증 실패")
            return False
        
        # 방문객 정보 읽기
        visitor_data = excel_processor.read_visitor_data(excel_file)
        
        if not visitor_data:
            logger.warning("방문객 정보를 읽을 수 없습니다. 신청자 정보만 입력합니다.")
        
        # 일진홀딩스 자동화 인스턴스 생성
        from websites.iljin_holdings.automation import IljinHoldingsAutomation
        automation = IljinHoldingsAutomation(website_config)
        
        # 첫 번째 행 데이터로 테스트
        test_data = excel_data[0]
        logger.info(f"엑셀에서 읽은 테스트 데이터: {test_data}")
        
        # 자동화 실행 (신청자 정보 입력)
        success = automation.run_automation(test_data)
        
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
        
        # 웹에서는 브라우저를 자동으로 닫음
        automation.cleanup()
        
        return success
        
    except Exception as e:
        logger.error(f"일진홀딩스 자동화 테스트 오류: {e}")
        return False


def test_ip168_itsm_name_field():
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
        
        # 자동화 실행 (브라우저 유지)
        success = automation.run_automation(
            data=None,  # 로그인 정보는 설정에서 가져옴
            keep_browser=True,
            select_language=True,
            navigate_to_target=True
        )
        
        if not success:
            logger.error("자동화 실행 실패")
            return False
        
        # 성명 필드 테스트
        logger.info("성명 필드 테스트 시작...")
        
        # 1. 기존 테스트 메서드
        if automation.test_name_field("테스트성명1"):
            logger.info("✅ 기존 테스트 메서드 성공")
        else:
            logger.warning("⚠️ 기존 테스트 메서드 실패")
        
        # 2. 정확한 선택자 테스트 메서드
        if automation.test_name_field_with_exact_selectors("테스트성명2"):
            logger.info("✅ 정확한 선택자 테스트 메서드 성공")
        else:
            logger.warning("⚠️ 정확한 선택자 테스트 메서드 실패")
        
        # 3. 특별 처리 메서드
        if automation.fill_name_field_specific("테스트성명3"):
            logger.info("✅ 특별 처리 메서드 성공")
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
        logger.info("브라우저가 열린 상태로 유지됩니다. 확인 후 수동으로 닫아주세요.")
        
        # 사용자 입력 대기
        input("엔터 키를 누르면 브라우저가 닫힙니다...")
        automation.cleanup()
        
        return True
        
    except Exception as e:
        logger.error(f"IP 168 ITSM 성명 필드 테스트 오류: {e}")
        return False


def test_ip168_itsm_name_field_web(input_file=None):
    """IP 168 ITSM 웹사이트 성명 필드 테스트 (웹용)"""
    try:
        logger.info("=== IP 168 ITSM 성명 필드 테스트 시작 (웹용) ===")
        
        # 설정 관리자 초기화
        config_manager = ConfigManager()
        
        # IP 168 ITSM 웹사이트 설정 가져오기
        website_id = "ip_168_itsm"
        website_config = config_manager.get_website_config(website_id)
        
        if not website_config:
            logger.error(f"웹사이트 설정을 찾을 수 없습니다: {website_id}")
            return False
        
        # 파일 경로 설정
        if input_file and Path(input_file).exists():
            excel_file = input_file
            logger.info(f"웹에서 업로드된 파일 사용: {excel_file}")
        else:
            excel_file = "sample_data.xlsx"
            logger.info(f"기본 파일 사용: {excel_file}")
        
        # 엑셀 데이터 읽기
        excel_processor = ExcelProcessor(config_manager.get_global_config())
        excel_data = excel_processor.read_excel_file(excel_file)
        
        if not excel_data:
            logger.error("엑셀 데이터를 읽을 수 없습니다")
            return False
        
        # IP 168 ITSM 자동화 인스턴스 생성
        from websites.ip_168_itsm.automation import IP168ITSMAutomation
        automation = IP168ITSMAutomation(website_config)
        
        # 첫 번째 행 데이터로 테스트
        test_data = excel_data[0]
        logger.info(f"엑셀에서 읽은 테스트 데이터: {test_data}")
        
        # 자동화 실행
        success = automation.run_automation(test_data)
        
        if success:
            logger.info("✅ IP 168 ITSM 자동화 테스트 성공!")
        else:
            logger.error("❌ IP 168 ITSM 자동화 테스트 실패")
        
        # 웹에서는 브라우저를 자동으로 닫음
        automation.cleanup()
        
        return success
        
    except Exception as e:
        logger.error(f"IP 168 ITSM 자동화 테스트 오류: {e}")
        return False


def main():
    """메인 실행 함수"""
    try:
        # 로거 설정
        logger = setup_logger()
        logger.info("=== 다중 웹사이트 RPA 시스템 시작 ===")
        
        # 명령행 인수 파싱
        import argparse
        parser = argparse.ArgumentParser(description="Multi-Website RPA 시스템")
        parser.add_argument("--website", type=str, help="실행할 웹사이트 (iljin_holdings 또는 ip_168_itsm)")
        parser.add_argument("--test", action="store_true", help="테스트 모드")
        parser.add_argument("--input-file", type=str, help="입력 파일 경로")
        
        args = parser.parse_args()
        
        # 웹에서 실행되는 경우 (--website 인수가 제공된 경우)
        if args.website:
            logger.info(f"웹에서 실행: {args.website}")
            
            if args.website == "iljin_holdings":
                # 일진홀딩스 자동화 테스트 실행
                if test_iljin_holdings_automation_web(args.input_file):
                    logger.info("일진홀딩스 자동화 테스트가 성공적으로 완료되었습니다.")
                else:
                    logger.error("일진홀딩스 자동화 테스트가 실패했습니다.")
            elif args.website == "ip_168_itsm":
                # IP 168 ITSM 성명 필드 테스트 실행
                if test_ip168_itsm_name_field_web(args.input_file):
                    logger.info("IP 168 ITSM 성명 필드 테스트가 성공적으로 완료되었습니다.")
                else:
                    logger.error("IP 168 ITSM 성명 필드 테스트가 실패했습니다.")
            else:
                logger.error(f"지원하지 않는 웹사이트입니다: {args.website}")
        else:
            # 콘솔에서 직접 실행되는 경우
            print("\n=== 테스트할 웹사이트를 선택하세요 ===")
            print("1. 일진홀딩스 자동화 테스트")
            print("2. IP 168 ITSM 성명 필드 테스트")
            
            choice = input("\n선택 (1 또는 2): ").strip()
            
            if choice == "1":
                # 일진홀딩스 자동화 테스트 실행
                if test_iljin_holdings_automation():
                    logger.info("일진홀딩스 자동화 테스트가 성공적으로 완료되었습니다.")
                else:
                    logger.error("일진홀딩스 자동화 테스트가 실패했습니다.")
            elif choice == "2":
                # IP 168 ITSM 성명 필드 테스트 실행
                if test_ip168_itsm_name_field():
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