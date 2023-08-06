from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

import arrow
import requests
from loguru import logger
from marshmallow import Schema
from requests import HTTPError, Timeout
from scalpl import Cut
from validate_docbr import CNPJ

from snatch.base.data import BaseData
from snatch.config import get_settings
from snatch.helpers.only_numbers import only_numbers
from snatch.helpers.time_it import time_it


@dataclass
class BaseSnatch:
    """Base Snatch Class.

    For each Datasource, you`ll need to subclass this class
    overriding the following properties:

    * serializer_class (Schema):    The Serializer Class used to deserialize
                                    backend response dict to DataSource Data Object.
                                    Must be a Marshmallow schema.
    * default_timeout (int):        Default timeout in seconds, for wait backend
                                    response for pending prospections.
                                    Please make sure you give enough
                                    time to backend complete prospect the Datasource.
    * default_max_days (int):       Default max days for expiration check. All
                                    prospections with prospect_date older than
                                    max_days will be marked as EXPIRED.
    * authorization_token (str):    The Datasource Authorization Token.
    * tax_id (str):                 The TaxId prospected. Must be a valid CNPJ,
                                    formatted or not.
    * base_url (str):               DataSource base url.
    """

    serializer_class: Optional[Type[Schema]] = None
    default_timeout: int = 60
    default_max_days: int = 30
    authorization_token_key: Optional[str] = None
    tax_id: Optional[str] = None
    base_url_key: Optional[str] = None
    settings: Optional[Cut] = None

    def __post_init__(self):
        self.settings = get_settings()

    @property
    def authorization_token(self) -> str:
        return self.settings[self.authorization_token_key]

    @property
    def base_url(self) -> str:
        return self.settings[self.base_url_key]

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.authorization_token}",
        }

    @property
    def tax_id(self) -> str:  # noqa
        """Return current TaxId."""
        return self._tax_id

    @tax_id.setter
    def tax_id(self, data: str):
        """Save current TaxId for DataSource Integration.

        Will check a valid CNPJ first and convert to numbers only.

        :param data: TaxId (must be a valid CNPJ)
        :return: None
        """
        cnpj = CNPJ()
        if not cnpj.validate(data):
            raise ValueError("Invalid TaxId")
        self._tax_id = only_numbers(data)  # noqa

    def _waiter(self, timeout: Optional[int] = None):
        if not timeout:
            timeout = self.default_timeout
        max_waiting_time = arrow.utcnow().shift(seconds=timeout)
        now = arrow.utcnow()
        next_check = now
        while now <= max_waiting_time:
            if now >= next_check:
                next_check = arrow.utcnow().shift(seconds=1)
                data = self._last_prospect(timeout=timeout)
                if data and data.integration_status in [
                    "SUCCESS",
                    "ERROR",
                    "CONN_ERROR",
                    "NOT_FOUND",
                ]:
                    logger.info(f"Data Received - Status is: {data.integration_status}")
                    return data
            now = arrow.utcnow()
        return self._format_timeout_response("/last_prospect")

    def _post_new_prospect(self, timeout: int) -> BaseData:
        url = "/api/prospects/from_tax_id/"
        payload = {"tax_id": self.tax_id}
        data = self._request_and_create_data(url=url, timeout=timeout, payload=payload)
        return data

    def _last_prospect(self, timeout: int) -> BaseData:
        url = f"/api/companies/{self.tax_id}/last_prospect/"
        return self._request_and_create_data(url=url, timeout=timeout)

    def _last_valid(self, timeout: int) -> BaseData:
        url = f"/api/companies/{self.tax_id}/last_valid/"
        return self._request_and_create_data(url=url, timeout=timeout)

    def _format_response(self, data: Dict[Any, Any]) -> BaseData:
        data_obj = self.serializer_class().load(data)
        data_obj.current_environment = self.settings["current_environment"]
        data_obj.datasource_base_url = self.base_url
        return data_obj

    def _format_error_response(self, error):
        status_code = (
            error.response.status_code if hasattr(error, "response") else "N/D"
        )
        integration_status = "NOT_FOUND" if status_code == 404 else "CONN_ERROR"
        if integration_status == "CONN_ERROR":
            payload = {}
        else:
            payload = error.response.json() if hasattr(error, "response") else {}
        data_obj = self.serializer_class().load(
            {
                "status_reason": f"Status Code: {status_code} "
                f"when accessing {error.request.url}",
                "status": integration_status,
                "payload": payload,
            }
        )
        data_obj.current_environment = self.settings["current_environment"]
        data_obj.datasource_base_url = self.base_url
        return data_obj

    def _format_timeout_response(self, url):
        data_obj = self.serializer_class().load(
            {
                "status_reason": f"Timeout when accessing: {url}",
                "status": "TIMEOUT",
            }
        )
        data_obj.current_environment = self.settings["current_environment"]
        data_obj.datasource_base_url = self.base_url
        return data_obj

    def _request_and_create_data(
        self, url: str, timeout: int, payload: Dict[Any, Any] = None
    ):
        try:
            method = "POST" if payload else "GET"
            full_url = f"{self.base_url}{url}"
            logger.info(f"Start {method} request to {full_url} ...")
            response = requests.request(
                method=method,
                url=full_url,
                json=payload,
                headers=self.headers,
                timeout=timeout,
            )
            logger.debug(f"Response status code is: {response.status_code}")
            response.raise_for_status()
            return self._format_response(response.json())
        except HTTPError as error:
            return self._format_error_response(error)
        except Timeout as error:
            return self._format_timeout_response(error.request.url)

    @time_it
    def last_valid(self, timeout: Optional[int] = None):
        """Return last valid DataSource integration for TaxId.

        It will check for the last valid Datasource Integration
        for selected TaxId. The last valid integration is the
        last one with "SUCCESS" status, regardless prospect time.

        :param timeout: Time in seconds before timeout connection. Default: 60 seconds.
        :return: DataSource Data Object
        """
        if not timeout:
            timeout = self.default_timeout
        return self._last_valid(timeout=timeout)

    @time_it
    def get_data(
        self, timeout: Optional[int] = None, max_days_old: Optional[int] = None
    ):
        """Get or Request DataSource Integration Data.

        It will:

        1. Check if exists a valid integration for
        selected TaxId in backend. A valid integration
        is a successfully integration (status: SUCCESS) with
        prospect date less or equal the `max_days_old` informed.

        2. If integration does not exist,
        has EXPIRED or has an status "ERROR",
        automatically start a new integration.

        3. If integration was started or already PENDING/RUNNING,
        wait `timeout` seconds for the backend response.

        :param max_days_old: Max days old for last integration,
                                if exists. Default: 30 days old.
        :param timeout: Time in seconds before timeout connection. Default: 60 seconds.
        :return: DataSource Data Object
        """
        if not timeout:
            timeout = self.default_timeout

        if not max_days_old:
            max_days_old = self.default_max_days

        data = self._last_prospect(timeout=timeout)
        data.find_current_status(max_days_old=max_days_old)

        # Check Status
        if data.integration_status in ["SUCCESS", "TIMEOUT", "CONN_ERROR"]:
            return data

        if data.integration_status == "WAITING":
            wait_data = self._waiter(timeout=timeout)
            return wait_data

        # Status: NOT_FOUND, ERROR or EXPIRED
        self._post_new_prospect(timeout)
        wait_data = self._waiter(timeout=timeout)
        return wait_data
