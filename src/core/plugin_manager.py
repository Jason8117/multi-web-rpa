"""
플러그인 관리 모듈
웹사이트별 플러그인을 동적으로 로드하고 관리
"""

import importlib
from typing import Dict, Any, Type, Optional
from src.core.base_automation import BaseAutomation
from src.core.config_manager import ConfigManager
from loguru import logger


class PluginManager:
    """웹사이트 플러그인 관리 클래스"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.plugins: Dict[str, Type[BaseAutomation]] = {}
        self.load_plugins()
        
    def load_plugins(self) -> None:
        """등록된 플러그인 로드"""
        try:
            registry = self.config_manager.get_website_registry()
            websites = registry.get('websites', {})
            
            for website_id, info in websites.items():
                if info.get('enabled', True):
                    try:
                        plugin_class = self.load_plugin(website_id, info)
                        if plugin_class:
                            self.plugins[website_id] = plugin_class
                            logger.info(f"플러그인 로드 완료: {website_id}")
                    except Exception as e:
                        logger.error(f"플러그인 로드 실패 {website_id}: {e}")
                        
        except Exception as e:
            logger.error(f"플러그인 로드 중 오류: {e}")
            
    def load_plugin(self, website_id: str, info: Dict[str, Any]) -> Optional[Type[BaseAutomation]]:
        """개별 플러그인 로드"""
        try:
            module_name = info.get('module')
            class_name = info.get('class')
            
            if not module_name or not class_name:
                logger.error(f"플러그인 정보가 불완전합니다: {website_id}")
                return None
                
            # 모듈 동적 로드
            module = importlib.import_module(module_name)
            
            # 클래스 가져오기
            plugin_class = getattr(module, class_name)
            
            # BaseAutomation을 상속받았는지 확인
            if not issubclass(plugin_class, BaseAutomation):
                logger.error(f"플러그인이 BaseAutomation을 상속받지 않았습니다: {website_id}")
                return None
                
            return plugin_class
            
        except ImportError as e:
            logger.error(f"모듈 로드 실패 {website_id}: {e}")
            return None
        except AttributeError as e:
            logger.error(f"클래스 로드 실패 {website_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"플러그인 로드 실패 {website_id}: {e}")
            return None
            
    def get_plugin(self, website_id: str) -> Optional[Type[BaseAutomation]]:
        """플러그인 반환"""
        return self.plugins.get(website_id)
        
    def create_plugin_instance(self, website_id: str) -> Optional[BaseAutomation]:
        """플러그인 인스턴스 생성"""
        try:
            plugin_class = self.get_plugin(website_id)
            if not plugin_class:
                logger.error(f"플러그인을 찾을 수 없습니다: {website_id}")
                return None
                
            # 웹사이트별 설정 가져오기
            config = self.config_manager.get_website_config(website_id)
            
            # 플러그인 인스턴스 생성
            instance = plugin_class(config)
            return instance
            
        except Exception as e:
            logger.error(f"플러그인 인스턴스 생성 실패 {website_id}: {e}")
            return None
            
    def list_plugins(self) -> Dict[str, str]:
        """등록된 플러그인 목록 반환"""
        return {k: v.__name__ for k, v in self.plugins.items()}
        
    def is_plugin_loaded(self, website_id: str) -> bool:
        """플러그인 로드 여부 확인"""
        return website_id in self.plugins
        
    def reload_plugin(self, website_id: str) -> bool:
        """플러그인 재로드"""
        try:
            registry = self.config_manager.get_website_registry()
            website_info = registry.get('websites', {}).get(website_id)
            
            if not website_info:
                logger.error(f"웹사이트 정보를 찾을 수 없습니다: {website_id}")
                return False
                
            # 기존 플러그인 제거
            if website_id in self.plugins:
                del self.plugins[website_id]
                
            # 플러그인 재로드
            plugin_class = self.load_plugin(website_id, website_info)
            if plugin_class:
                self.plugins[website_id] = plugin_class
                logger.info(f"플러그인 재로드 완료: {website_id}")
                return True
            else:
                logger.error(f"플러그인 재로드 실패: {website_id}")
                return False
                
        except Exception as e:
            logger.error(f"플러그인 재로드 중 오류 {website_id}: {e}")
            return False 