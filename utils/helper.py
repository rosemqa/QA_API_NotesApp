import json
import allure
import requests
from allure_commons.types import AttachmentType


class Helper:
    @staticmethod
    def attach_response(response: requests.Response, name: str = 'API Response'):
        try:
            response_json = response.json()
        except ValueError:
            response_json = response.text

        try:
            response_str = json.dumps(response_json, indent=4)
        except (TypeError, ValueError):
            response_str = str(response_json)

        allure.attach(body=response_str, name=name, attachment_type=AttachmentType.JSON)
