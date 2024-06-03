import urllib3
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://localhost:8080"
USERNAME = "admin"
PASSWORD = "admin"


def create_restconf_session() -> requests.Session:
    http_headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }
    session = requests.session()
    session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
    session.headers.update(http_headers)
    session.verify = False
    return session


def apply_data(session: requests.Session, path: str, data: str) -> str:
    response = session.patch(BASE_URL + path, json=data)
    response.raise_for_status()
    return response.text


def add_dns_server_dry_run(
    service_name: str, device_name: str, server_address: str
) -> tuple[str, dict]:
    path = "/restconf/data?dry-run"
    data = _get_dns_server_payload(service_name, device_name, server_address)
    return path, data


def add_dns_server(
    service_name: str, device_name: str, server_address: str
) -> tuple[str, dict]:
    path = "/restconf/data"
    data = _get_dns_server_payload(service_name, device_name, server_address)
    return path, data


def _get_dns_server_payload(
    service_name: str, device_name: str, server_address: str
) -> str:
    print(f"{type(service_name)=}")
    print(f"{type(device_name)=}")
    print(f"{type(server_address)=}")
    data = {
        "router:router": [
            {
                "name": "core",
                "device": ["core-rtr0"],
                "sys": {"ntp": {"server": [{"name": "4.4.4.4"}]}},
            }
        ]
    }

    print(f"{data=}")
    print(f"{type(data)=}")
    return data


def print_response(response: str) -> None:
    print(f"{'#' * 20} xml received: {'#' * 20}")
    print(response.prettify())
    print(f"{'#' * 20} text received: {'#' * 20}")
    print(response.text)


def parse_xml(xml: str) -> dict:
    return BeautifulSoup(xml, "xml")


def main() -> None:
    SERVICE_NAME = "core"
    DEVICE_NAME = "core-rtr0"
    SERVER_ADDRESS = "1.1.1.1"

    session = create_restconf_session()

    ## Dry run
    path, data = add_dns_server_dry_run(
        service_name=SERVICE_NAME,
        device_name=DEVICE_NAME,
        server_address=SERVER_ADDRESS,
    )
    response = apply_data(session, path, data=data)
    parsed_response = parse_xml(response)
    print_response(parsed_response)

    ## Apply
    # path, data = add_dns_server(
    #     service_name=SERVICE_NAME,
    #     device_name=DEVICE_NAME,
    #     server_address=SERVER_ADDRESS,
    # )
    # response = apply_data(session, path, data=data)
    # parsed_response = parse_xml(response)
    # print_response(parsed_response)


if __name__ == "__main__":
    main()
