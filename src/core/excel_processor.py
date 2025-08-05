"""
엑셀 처리 모듈
엑셀 파일 읽기 및 처리를 담당
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger


class ExcelProcessor:
    """엑셀 처리 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.input_folder = Path(config.get('paths.data_input', './data/input/'))
        self.output_folder = Path(config.get('paths.data_output', './data/output/'))
        
    def read_excel_file(self, filename: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        엑셀 파일을 읽어서 데이터를 반환
        
        Args:
            filename: 읽을 엑셀 파일명 (None이면 input 폴더의 첫 번째 파일)
            
        Returns:
            List[Dict]: 엑셀 데이터를 딕셔너리 리스트로 변환
        """
        try:
            if filename is None:
                # input 폴더에서 첫 번째 엑셀 파일 찾기
                excel_files = list(self.input_folder.glob("*.xlsx"))
                if not excel_files:
                    logger.error(f"엑셀 파일을 찾을 수 없습니다: {self.input_folder}")
                    return []
                filename = excel_files[0].name
                
            file_path = self.input_folder / filename
            if not file_path.exists():
                logger.error(f"엑셀 파일이 존재하지 않습니다: {file_path}")
                return []
                
            logger.info(f"엑셀 파일 읽기 시작: {filename}")
            
            # 엑셀 파일 읽기
            df = pd.read_excel(file_path, header=0)  # 첫 번째 행을 헤더로 사용
            
            # 데이터 검증
            if df.empty:
                logger.error("엑셀 파일이 비어있습니다")
                return []
                
            # 데이터프레임을 딕셔너리 리스트로 변환
            data = df.to_dict('records')
            
            logger.info(f"엑셀 파일 읽기 완료: {len(data)}개 행")
            
            # 데이터 구조 디버깅
            self.debug_excel_structure(data)
            
            return data
            
        except Exception as e:
            logger.error(f"엑셀 파일 읽기 오류: {e}")
            return []
            
    def debug_excel_structure(self, data: List[Dict[str, Any]]) -> None:
        """엑셀 파일 구조 상세 디버깅"""
        try:
            logger.info("=== 엑셀 파일 구조 상세 분석 ===")
            
            if not data:
                logger.error("엑셀 데이터가 비어있습니다")
                return
            
            # 첫 번째 행(헤더) 분석
            first_row = data[0]
            logger.info(f"첫 번째 행의 키들: {list(first_row.keys())}")
            
            # 각 키의 값 확인
            for key, value in first_row.items():
                logger.info(f"컬럼 '{key}': 값='{value}', 타입={type(value).__name__}")
            
            # 방문사업장 컬럼 특별 확인
            if '방문사업장' in first_row:
                logger.info(f"✓ 방문사업장 컬럼 발견: '{first_row['방문사업장']}'")
            else:
                logger.warning("✗ 방문사업장 컬럼이 없습니다")
                
            logger.info("=== 엑셀 파일 구조 분석 완료 ===")
            
        except Exception as e:
            logger.error(f"엑셀 구조 디버깅 오류: {e}")
            
    def verify_excel_data(self, data: List[Dict[str, Any]]) -> bool:
        """엑셀 데이터 검증"""
        try:
            logger.info("=== 엑셀 데이터 검증 시작 ===")
            
            if not data:
                logger.error("엑셀 데이터가 비어있습니다")
                return False
                
            # 첫 번째 행 데이터 검증
            first_row = data[0]
            logger.info(f"전체 엑셀 데이터: {first_row}")
            
            # 필수 필드 확인 (공백 처리)
            required_fields = ['방문사업장', '피방문자', '피방문자 연락처']
            for field in required_fields:
                # 공백이 포함된 필드명도 찾기
                found = False
                for key in first_row.keys():
                    if field in key and first_row[key]:
                        logger.info(f"✓ {key} 데이터: '{first_row[key]}'")
                        found = True
                        break
                
                if not found:
                    logger.warning(f"✗ {field} 관련 데이터가 없거나 비어있습니다")
                    
            logger.info("=== 엑셀 데이터 검증 완료 ===")
            return True
            
        except Exception as e:
            logger.error(f"엑셀 데이터 검증 오류: {e}")
            return False
            
    def save_result(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """결과 데이터를 엑셀 파일로 저장"""
        try:
            output_path = self.output_folder / filename
            
            # 출력 폴더가 없으면 생성
            self.output_folder.mkdir(parents=True, exist_ok=True)
            
            # 데이터프레임으로 변환하여 저장
            df = pd.DataFrame(data)
            df.to_excel(output_path, index=False)
            
            logger.info(f"결과 저장 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"결과 저장 오류: {e}")
            return False
            
    def get_template_path(self, website_id: str) -> Optional[Path]:
        """웹사이트별 템플릿 파일 경로 반환"""
        try:
            template_path = Path("src/websites") / website_id / "template.xlsx"
            if template_path.exists():
                return template_path
            else:
                logger.warning(f"템플릿 파일이 없습니다: {template_path}")
                return None
                
        except Exception as e:
            logger.error(f"템플릿 경로 확인 오류: {e}")
            return None
            
    def read_visitor_data(self, filename: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        방문객 정보를 읽어서 반환
        
        Args:
            filename: 읽을 엑셀 파일명 (None이면 input 폴더의 첫 번째 파일)
            
        Returns:
            List[Dict]: 방문객 데이터를 딕셔너리 리스트로 변환
        """
        try:
            if filename is None:
                # input 폴더에서 첫 번째 엑셀 파일 찾기
                excel_files = list(self.input_folder.glob("*.xlsx"))
                if not excel_files:
                    logger.error(f"엑셀 파일을 찾을 수 없습니다: {self.input_folder}")
                    return []
                filename = excel_files[0].name
                
            file_path = self.input_folder / filename
            if not file_path.exists():
                logger.error(f"엑셀 파일이 존재하지 않습니다: {file_path}")
                return []
                
            logger.info(f"방문객 정보 읽기 시작: {filename}")
            
            # 엑셀 파일을 헤더 없이 읽기
            df = pd.read_excel(file_path, header=None)
            
            # 방문객 정보 헤더 찾기 (4번째 행, 인덱스 3)
            if len(df) < 4:
                logger.error("방문객 정보 헤더를 찾을 수 없습니다")
                return []
            
            # 방문객 정보 헤더 확인
            header_row = df.iloc[3]  # 4번째 행
            if '방문객정보' not in str(header_row.values):
                logger.error("방문객 정보 헤더를 찾을 수 없습니다")
                return []
            
            # 방문객 데이터 추출 (5번째 행부터)
            visitor_df = df.iloc[4:].copy()
            
            # 컬럼명 설정
            visitor_df.columns = ['번호', '성명', '휴대폰번호', '차종', '차량번호', 'col5', 'col6', 'col7', 'col8', 'col9']
            
            # 빈 행 제거
            visitor_df = visitor_df[visitor_df['성명'].notna() & (visitor_df['성명'] != '')]
            
            # NaN 값 처리
            visitor_df = visitor_df.fillna('')
            
            # 데이터프레임을 딕셔너리 리스트로 변환
            visitor_data = visitor_df.to_dict('records')
            
            logger.info(f"방문객 정보 읽기 완료: {len(visitor_data)}명")
            
            # 방문객 데이터 구조 디버깅
            self.debug_visitor_structure(visitor_data)
            
            return visitor_data
            
        except Exception as e:
            logger.error(f"방문객 정보 읽기 오류: {e}")
            return []
            
    def debug_visitor_structure(self, visitor_data: List[Dict[str, Any]]) -> None:
        """방문객 데이터 구조 디버깅"""
        try:
            logger.info("=== 방문객 데이터 구조 분석 ===")
            
            if not visitor_data:
                logger.error("방문객 데이터가 비어있습니다")
                return
            
            # 첫 번째 방문객 데이터 분석
            first_visitor = visitor_data[0]
            logger.info(f"첫 번째 방문객의 키들: {list(first_visitor.keys())}")
            
            # 각 키의 값 확인
            for key, value in first_visitor.items():
                logger.info(f"컬럼 '{key}': 값='{value}', 타입={type(value).__name__}")
            
            # 필수 컬럼 확인
            required_columns = ['성명', '휴대폰번호', '차종', '차량번호']
            for col in required_columns:
                if col in first_visitor:
                    logger.info(f"✓ {col} 컬럼 발견")
                else:
                    logger.warning(f"✗ {col} 컬럼이 없습니다")
            
            # 방문객 데이터 샘플 출력
            logger.info("=== 방문객 데이터 샘플 ===")
            for i, visitor in enumerate(visitor_data[:3]):  # 처음 3명만
                logger.info(f"방문객 {i+1}: {visitor}")
                    
            logger.info("=== 방문객 데이터 구조 분석 완료 ===")
            
        except Exception as e:
            logger.error(f"방문객 데이터 구조 디버깅 오류: {e}")
            
    def get_visitor_data_by_index(self, visitor_data: List[Dict[str, Any]], index: int) -> Optional[Dict[str, Any]]:
        """인덱스로 방문객 데이터 가져오기"""
        try:
            if 0 <= index < len(visitor_data):
                return visitor_data[index]
            else:
                logger.warning(f"방문객 인덱스 {index}가 범위를 벗어났습니다. 총 {len(visitor_data)}명")
                return None
        except Exception as e:
            logger.error(f"방문객 데이터 조회 오류: {e}")
            return None 