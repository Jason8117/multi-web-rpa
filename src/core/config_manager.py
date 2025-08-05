"""
설정 관리 모듈
전역 설정 및 웹사이트별 설정을 관리
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
from loguru import logger


class ConfigManager:
    """설정 관리 클래스"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.global_config = {}
        self.website_registry = {}
        self.load_configs()
        
    def load_configs(self) -> None:
        """모든 설정 파일 로드"""
        try:
            # 전역 설정 로드
            global_config_path = self.config_dir / "global_config.yaml"
            if global_config_path.exists():
                with open(global_config_path, 'r', encoding='utf-8') as f:
                    self.global_config = yaml.safe_load(f)
                logger.info("전역 설정 로드 완료")
            else:
                logger.warning("전역 설정 파일이 없습니다")
                
            # 웹사이트 레지스트리 로드
            registry_path = self.config_dir / "website_registry.yaml"
            if registry_path.exists():
                with open(registry_path, 'r', encoding='utf-8') as f:
                    self.website_registry = yaml.safe_load(f)
                logger.info("웹사이트 레지스트리 로드 완료")
            else:
                logger.warning("웹사이트 레지스트리 파일이 없습니다")
                
        except Exception as e:
            logger.error(f"설정 로드 오류: {e}")
            
    def get_global_config(self) -> Dict[str, Any]:
        """전역 설정 반환"""
        return self.global_config
        
    def get_website_config(self, website_id: str) -> Dict[str, Any]:
        """웹사이트별 설정 반환"""
        try:
            if website_id not in self.website_registry.get('websites', {}):
                raise ValueError(f"웹사이트 ID '{website_id}'가 레지스트리에 없습니다")
                
            website_info = self.website_registry['websites'][website_id]
            config_file = website_info.get('config_file')
            
            if not config_file:
                return {}
                
            config_path = Path(config_file)
            if not config_path.is_absolute():
                config_path = Path("src") / config_path
                
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    website_config = yaml.safe_load(f)
                    
                # 전역 설정과 병합
                merged_config = self.merge_configs(self.global_config, website_config)
                return merged_config
            else:
                logger.warning(f"웹사이트 설정 파일이 없습니다: {config_path}")
                return self.global_config
                
        except Exception as e:
            logger.error(f"웹사이트 설정 로드 오류: {e}")
            return self.global_config
            
    def merge_configs(self, global_config: Dict[str, Any], website_config: Dict[str, Any]) -> Dict[str, Any]:
        """전역 설정과 웹사이트 설정 병합"""
        merged = global_config.copy()
        
        def deep_merge(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    base[key] = deep_merge(base[key], value)
                else:
                    base[key] = value
            return base
            
        return deep_merge(merged, website_config)
        
    def get_website_registry(self) -> Dict[str, Any]:
        """웹사이트 레지스트리 반환"""
        return self.website_registry
        
    def list_websites(self) -> Dict[str, str]:
        """등록된 웹사이트 목록 반환"""
        websites = self.website_registry.get('websites', {})
        return {k: v.get('name', k) for k, v in websites.items() if v.get('enabled', True)}
        
    def is_website_enabled(self, website_id: str) -> bool:
        """웹사이트 활성화 여부 확인"""
        websites = self.website_registry.get('websites', {})
        return websites.get(website_id, {}).get('enabled', False) 