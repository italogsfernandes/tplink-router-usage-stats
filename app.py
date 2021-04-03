import requests

from datetime import datetime

from config import load_config
from clients import WR720NClient
from utils import write_output_to_file


def main():
    (router_ip,
     auth_token,
     output_file,
     output_file_completo) = load_config("VAN")

    created_date = datetime.now()
    stats = WR720NClient(router_ip, auth_token).get_stats_data()

    write_output_to_file(
        stats, created_date, output_file, output_file_completo
    )

if __name__ == '__main__':
    main()