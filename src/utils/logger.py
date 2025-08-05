"""
로거 설정 유틸리티
"""

import sys
from pathlib import Path
from loguru import logger


def setup_logger():
    """로거 설정"""
    # 기존 로거 제거
    logger.remove()
    
    # 콘솔 출력 설정
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        colorize=True
    )
    
    # 파일 출력 설정
    log_dir = Path("logs/automation")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_dir / "rpa_automation.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        rotation="1 day",
        retention="30 days",
        encoding="utf-8"
    )
    
    # 에러 로그 설정
    error_log_dir = Path("logs/errors")
    error_log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        error_log_dir / "error.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="ERROR",
        rotation="1 day",
        retention="30 days",
        encoding="utf-8"
    )
    
    return logger 