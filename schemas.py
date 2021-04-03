from pydantic import BaseModel
from typing import List, Optional

from mixins import StatDataMixin


class StatisticData(StatDataMixin, BaseModel):
    mac: str
    rx_byte: Optional[int] = 0
    cur_udp: Optional[int] = 0
    cur_syn: Optional[int] = 0
    ip: str
    cur_icmp: Optional[int] = 0
    total_pkt: Optional[int] = 0
    retx_byte: Optional[int] = 0
    total_byte: int
    cur_pkt: Optional[int] = 0
    cur_byte: Optional[int] = 0
    rerx_byte: Optional[int] = 0
    tx_byte: Optional[int] = 0


class StatisticsResponse(BaseModel):
    success: bool
    data: List[StatisticData]

