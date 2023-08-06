from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

import arrow
from scalpl import Cut


@dataclass
class BaseData:
    """Base Data Class.

    The subclasses created using this class will be available
    to Data Scientists.

    Default Properties
    ==================

    * tax_id (str):                 The TaxId prospected.
                                    must be a valid CNPJ, formatted or not.
    * integration_status (str):     The current Integration Status. Current status are:
                                    NOT_FOUND, WAITING, SUCCESS, EXPIRED, ERROR,
                                    CONN_ERROR and TIMEOUT
                                    Please check the `find_current_status` method
                                    for more info.
    * status_reason (str):          The human friendly reason for current status
    * prospect_date (datetime):     The prospect datetime.
    * payload (dict):               Original payload received from prospection.
    * timeit                        Time in seconds for retrieving data.
    * datasource_base_url           Data Source Base Url
    * current_environment           Current AWS Environment. Available environments are:
                                    local, dev, staging, production. Default: production
    """

    tax_id: Optional[str] = None
    integration_status: Optional[str] = None
    status_reason: str = ""
    prospect_date: Optional[datetime] = None
    payload: Optional[Dict[str, Any]] = None
    timeit: Optional[float] = None
    datasource_base_url: Optional[str] = None
    current_environment: Optional[Cut] = None

    def find_current_status(self, max_days_old: int):
        """Find current Status for Data.

        Current available status:

        * NOT_FOUND   When backend responds 404 for TaxId
        * WAITING     When backend responds with status "PENDING" or "RUNNING"
        * SUCCESS     When backend responds with status "SUCCESS"
                        and prospect date is lower or equal than max_days_old
        * EXPIRED     When backend responds with status "SUCCESS"
                        and prospect date is greater than max_days_old
        * ERROR       When backend responds a integration error
                        when prospecting the DataSource
        * CONN_ERROR  When backend responds 40x,50x
        * TIMEOUT     When timeout occurs

        :param max_days_old: Max days old for current data, for check expiration.
        """
        if self.integration_status == "SUCCESS":
            days_old = (arrow.utcnow() - arrow.get(self.prospect_date)).days
            self.integration_status = (
                "EXPIRED" if days_old > max_days_old else "SUCCESS"
            )
        if self.integration_status in ["PENDING", "RUNNING"]:
            self.integration_status = "WAITING"
