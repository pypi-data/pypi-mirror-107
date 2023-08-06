import os
from typing import Any, Optional
from .api_client import APIClientBase


class Central(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(url_base or os.environ.get("CENTRAL_SERVICE", ""), **kwargs)

    def activate_product(
        self, email: str, password: str, activation_key: Optional[str]
    ) -> Any:
        body: Dict = {
            "email": email,
            "password": password,
            "activation_key": activation_key,
        }
        return self.post_request("/licensing/activate", body=body)

    def sync_product_licensing_information(self) -> Any:
        return self.post_request("/licensing/sync")

    def is_monitoring_purchased(self) -> Any:
        return self.get_request("/monitoring/is-purchased")

    def is_monitoring_enabled(self) -> Any:
        return self.get_request("/monitoring/is-enabled")

    def get_monitoring_endpoints(self) -> Any:
        return self.get_request("/monitoring/endpoints")

    def enable_monitoring(self) -> Any:
        return self.post_request("/monitoring/enable")

    def disable_monitoring(self) -> Any:
        return self.post_request("/monitoring/disable")
