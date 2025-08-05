"""
IP 168 ITSM 엑셀 데이터 읽기 모듈
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from loguru import logger


class ITSMExcelReader:
    """IP 168 ITSM 엑셀 파일 읽기 클래스"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.excel_file_path = None
        self.data = None
        
    def load_excel_file(self, file_path: str = None) -> bool:
        """엑셀 파일 로드"""
        try:
            if file_path is None:
                # 기본 파일 경로 사용
                base_path = Path(__file__).parent.parent.parent.parent
                file_path = base_path / "data" / "input" / "itsm_user_reg_template.xlsx"
            
            self.excel_file_path = Path(file_path)
            
            if not self.excel_file_path.exists():
                logger.error(f"엑셀 파일을 찾을 수 없습니다: {self.excel_file_path}")
                return False
            
            logger.info(f"엑셀 파일 로드 중: {self.excel_file_path}")
            
            # 엑셀 파일 읽기 (첫 번째 행을 헤더로 사용)
            self.data = pd.read_excel(self.excel_file_path, header=0)
            
            logger.info(f"엑셀 파일 로드 완료: {len(self.data)} 행, {len(self.data.columns)} 열")
            logger.info(f"컬럼 목록: {list(self.data.columns)}")
            
            # 처음 몇 행 미리보기
            logger.info("데이터 미리보기:")
            logger.info(self.data.head())
            
            return True
            
        except Exception as e:
            logger.error(f"엑셀 파일 로드 오류: {e}")
            return False
    
    def get_user_data(self, row_index: int) -> Optional[Dict[str, Any]]:
        """특정 행의 사용자 데이터 가져오기"""
        try:
            if self.data is None:
                logger.error("엑셀 데이터가 로드되지 않았습니다")
                return None
            
            if row_index >= len(self.data):
                logger.error(f"행 인덱스가 범위를 벗어났습니다: {row_index} >= {len(self.data)}")
                return None
            
            # 해당 행의 데이터 가져오기
            row_data = self.data.iloc[row_index]
            
            # NaN 값을 None으로 변환
            user_data = {}
            for column in self.data.columns:
                value = row_data[column]
                if pd.isna(value) or value == '':
                    user_data[column] = None
                else:
                    user_data[column] = str(value).strip()
            
            logger.info(f"행 {row_index} 데이터: {user_data}")
            return user_data
            
        except Exception as e:
            logger.error(f"사용자 데이터 가져오기 오류: {e}")
            return None
    
    def get_total_rows(self) -> int:
        """전체 행 수 반환"""
        if self.data is None:
            return 0
        return len(self.data)
    
    def get_column_names(self) -> List[str]:
        """컬럼명 목록 반환"""
        if self.data is None:
            return []
        return list(self.data.columns)
    
    def preview_data(self, max_rows: int = 5) -> None:
        """데이터 미리보기"""
        if self.data is None:
            logger.warning("데이터가 로드되지 않았습니다")
            return
        
        logger.info(f"데이터 미리보기 (최대 {max_rows}행):")
        logger.info(self.data.head(max_rows)) 