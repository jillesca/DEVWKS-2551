import urllib3
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://localhost:8080"
USERNAME = "admin"
PASSWORD = "admin"


def create_restconf_session() -> requests.Session:
    session = requests.session()
    session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
    session.headers.update({"Accept": "application/yang-data+xml"})
    session.verify = False
    return session


def fetch_data(session: requests.Session, path: str) -> str:
    response = session.get(url=BASE_URL + path)
    response.raise_for_status()
    return response.text


def parse_xml(xml: str) -> dict:
    return BeautifulSoup(xml, "xml")


def get_xr_device_hostname_rest_path(device_name: str) -> str:
    return f"/restconf/data/tailf-ncs:devices/device={device_name}/config/tailf-ned-cisco-ios-xr:hostname"


def main() -> None:
    DEVICE_NAME = "core-rtr0"

    session = create_restconf_session()
    path = get_xr_device_hostname_rest_path(device_name=DEVICE_NAME)
    response = fetch_data(session, path)
    parsed_response = parse_xml(response)

    print(f"{'#' * 20} xml received: {'#' * 20}")
    print(parsed_response.prettify())
    print(f"{'#' * 20} text received: {'#' * 20}")
    print(parsed_response.text)


if __name__ == "__main__":
    main()