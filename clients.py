import json
import requests

from pyquery import PyQuery as pq

from schemas import StatisticsResponse, StatisticData

class WR941HPClient:
    def __init__(self, router_url, auth_token):
        self.router_url = router_url
        self.auth_token = auth_token
        self.sysauth = ""
        self.stok_token = ""

    @property
    def base_url(self):
        base_url= f"{self.router_url}/cgi-bin/luci/;stok={self.stok_token}"
        return base_url

    @property
    def headers(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;',
        }
        if self.sysauth:
            headers['Cookie'] = f'sysauth={self.sysauth}'
        return headers

    def login(self):
        url = f"{self.base_url}/login?form=login"
        payload = f"operation=login&password={self.auth_token}&confirm=true"
        response = requests.post(url, headers=self.headers, data=payload)
        self.sysauth = response.cookies.get('sysauth')
        self.stok_token = response.json()['data']['stok']
        return self.sysauth, self.stok_token

    def logout(self):
        url = f"{self.base_url}/admin/system?form=logout"
        payload = "operation=write"
        response = requests.post(url, headers=self.headers, data=payload)
        return response.json()['success']

    def get_stats_data(self):
        url = f"{self.base_url}/admin/traffic?form=lists"
        payload = 'operation=load'
        response = requests.post(url, headers=self.headers, data=payload)
        return StatisticsResponse(**response.json()).data


class WR720NClient:
    def __init__(self, router_url, auth_token):
        self.router_url = router_url
        self.auth_token = auth_token

    @property
    def headers(self):
        headers = {
            "Authorization": self.auth_token,
            "Referer": f"{self.router_url}/userRpm/MenuRpm.htm",
        }
        return headers

    def process_get_stats_data_response_text(self, response):
        r_text = (
            pq(response.content.decode())('[language="javascript"]')[0].text
        )
        stats_values = [
            line.split(",")
            for line in r_text.split("Array(\n")[-1].split(" );")[0].split("\n")
            if len(line) > 10
        ]
        stats = []
        for line in stats_values:
            stat = StatisticData(
                ip=line[1].strip("\""),
                mac=line[2].strip("\""),
                total_byte=int(line[4]),
            )
            stats.append(stat)
        
        return stats

    def process_get_stats_data_response_json(self, response):
        r_text = (
            pq(response.content.decode())('[language="javascript"]')[0].text
        )
        r_list = json.loads(r_text[25:-2].replace("(", "[").replace(")", "]"))

        ip_index = 1
        mac_index = 2
        total_byte_index = 4
        line_qnt_info = 21
        qnt_devices = int(len(r_list)/line_qnt_info)
        
        stats = []
        for device_id in range(qnt_devices):
            stat = StatisticData(
                ip=r_list[device_id*line_qnt_info+ip_index],
                mac=r_list[device_id*line_qnt_info+mac_index],
                total_byte=r_list[device_id*line_qnt_info+total_byte_index],
            )
            stats.append(stat)

        return stats

    def get_stats_data(self):
        url = (
            f"{self.router_url}/userRpm/SystemStatisticRpm.htm"
            f"?itnerval=10&Num_per_page=100"
        )
        response = requests.get(url, headers=self.headers)

        stats = self.process_get_stats_data_response_json(response)

        return stats
