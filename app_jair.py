import requests

from datetime import datetime
from pyquery import PyQuery as pq

from clients import WR941HPClient
from config import load_config
from utils import write_output_to_file, save_output_in_database



def main(show_result=True):
    (router_ip,
     auth_token,
     output_file,
     output_file_completo) = load_config("JAIR")

    created_date = datetime.now()

    client = WR941HPClient(router_ip, auth_token)
    client.login()
    stats = client.get_stats_data()
    client.logout()

    write_output_to_file(
        stats, created_date, output_file, output_file_completo
    )
    save_output_in_database(stats, created_date, show_result)

if __name__ == '__main__':
    main()