import logging
import urllib3
from typing import Dict,Any,List

from atlassian import Confluence
from atlassian.rest_client import AtlassianRestAPI

from confluence.cli.utils import type_wrap_decorator, type_wrap, requests_error_handling, base_methods_decorator

## logger definition
logger = logging.getLogger("confluence_log")
## Disable certificate warnings for testing pourposes
urllib3.disable_warnings()


@base_methods_decorator(deco=type_wrap_decorator, regex=r"_response_handler", base_class=AtlassianRestAPI)
@base_methods_decorator(deco=requests_error_handling, regex=r"(post|put|delete)", base_class=AtlassianRestAPI)
class ConfluenceWrapper(Confluence):
    ## Borg pattern
    _shared_state: dict = {}

    def __init__(self, params: Dict[str,Any]):
        self.__dict__ = ConfluenceWrapper._shared_state
        if not self.__dict__ or params:
            super().__init__(
                url=params["baseURL"],
                username=params["user"],
                password=params["password"],
                proxies=params["proxies"],
                verify_ssl=params["verify_ssl"])
            logger.info("Confluence python client initialized")

    @requests_error_handling
    def get(self, path, data=None, flags=None, params=None, headers=None, not_json_response=None,
            trailing=None, absolute=False, advanced_mode=False):
        """Overriden GET operations to ensure custom type return"""
        logger.info(path)
        result = super().get(path, data, flags, params, headers, not_json_response, trailing, absolute, advanced_mode)
        if not_json_response or advanced_mode:
            return result
        if path == "rest/api/search":  # ? cql() search
            return result
        if result.get("results"):
            return {"results": [type_wrap(content) for content in result.get("results")]}
        elif result.get("id"):
            return type_wrap(result)
        else:
            return result

        
    @requests_error_handling
    def add_space_permissions(self, space_key: str, permissions: List[str], entity_name: str) -> bool:               
        url = "rpc/json-rpc/confluenceservice-v2"
        data = {
            "jsonrpc": "2.0",
            "method": "addPermissionsToSpace",
            "id": 7,            
            "params": [permissions,entity_name,space_key]            
        }
        logger.debug(f"params: {data['params']}")
        json = self.post(url, data=data)
        logger.debug(json)
        return json.get("result")


    @requests_error_handling
    def remove_space_permission(self, space_key: str, permission: str, entity_name: str) -> bool:               
        url = "rpc/json-rpc/confluenceservice-v2"
        data = {
            "jsonrpc": "2.0",
            "method": "removePermissionFromSpace",
            "id": 7,            
            "params": [permission,entity_name,space_key]            
        }
        logger.debug(f"params: {data['params']}")
        json = self.post(url, data=data)
        logger.debug(json)
        return json.get("result")
    

    @requests_error_handling
    def add_content_restrictions(self, content_id: str, operations: List[str], entity_name: str, entity_type:str) -> dict:
        """
        add read or update restrictions to content_id
        :param operations: List[str] List with "read" and "update" tokens. Ex: ["read"], ["read", "update"] ...
        :param entity_name: str User o Group name.
        :param entity_type: str user/group
        """
        url = f"rest/experimental/content/{content_id}/restriction"
        restriction_type = entity_type if entity_type == "group" else "known"        
        data_list: List[dict] = []
        for operation in operations:
            data_oper : dict = {"operation":operation}
            data_oper["restrictions"] = {entity_type:[ {"type":restriction_type,"name":entity_name}]}
            data_list.append(data_oper)
        json = self.put(url, data=data_list)        
        return json


    def delete_content_restriction(self, content_id: str, operation: str, entity_name, entity_type):
        url = f"rest/experimental/content/{content_id}/restriction/byOperation/{operation}/{entity_type}/{entity_name}"
        json = self.delete(url)        
        
        

    
    