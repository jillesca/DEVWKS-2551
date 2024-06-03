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
        "Accept": "application/yang-data+xml",
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
    return response.text, response.status_code


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
    return {
        "router:router": [
            {
                "name": service_name,
                "device": [device_name],
                "sys": {"ntp": {"server": [{"name": server_address}]}},
            }
        ]
    }


def print_response(response: BeautifulSoup, status_code: str) -> None:
    print(f"{'#' * 20} xml received: {'#' * 20}")
    print(response.prettify())
    print(f"http status code: {status_code}")


def parse_xml(xml: str) -> BeautifulSoup:
    return BeautifulSoup(xml, "xml")


def main() -> None:
    SERVICE_NAME = "core"
    DEVICE_NAME = "core-rtr0"
    SERVER_ADDRESS = "9.9.9.9"

    session = create_restconf_session()

    ## Dry run
    path, data = add_dns_server_dry_run(
        service_name=SERVICE_NAME,
        device_name=DEVICE_NAME,
        server_address=SERVER_ADDRESS,
    )
    response, status_code = apply_data(session, path, data=data)
    parsed_response = parse_xml(response)
    print_response(parsed_response, status_code)

    # Apply
    path, data = add_dns_server(
        service_name=SERVICE_NAME,
        device_name=DEVICE_NAME,
        server_address=SERVER_ADDRESS,
    )
    response, status_code = apply_data(session, path, data=data)
    parsed_response = parse_xml(response)
    print_response(parsed_response, status_code)


if __name__ == "__main__":
    main()
