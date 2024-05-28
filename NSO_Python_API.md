# NSO Python API/SDK

- The NSO Python, Java, Erlang (and C) APIs are **SDKs** used to extend NSO.
- Typically used by applications running on the same processor/system as NSO is running.
- Uses IPC over TCP sockets to communicate with NSO for low latency.
- Not available via `pip install`

<https://developer.cisco.com/docs/nso/api/nso-sdk-api-reference/>

## Development

| Scripts                                     | Services                                                       |
| ------------------------------------------- | -------------------------------------------------------------- |
| Connect directly to NSO datastore.          | Perform complex calculations & external system - integrations. |
| Onetime operations.                         | Apply XML templates from Python.                               |
| Importing device configurations.            | Get FASTMAP algorithm benefits.                                |
| Generating reports from the configurations. |                                                                |

## High-level & Low-level APIs

- Low-level APIs are a direct mapping of the NSO C APIs, CDB and MAAPI.
  - See man `confd_lib_lib` for more information.
- High-level APIs are an abstraction layer on top of the low-level APIs.
  - Easier to use.
  - Improved code readability and development for common use cases.

<https://developer.cisco.com/docs/nso/guides/python-api-overview/>
<https://developer.cisco.com/docs/nso/guides/ncs-man-pages-volume-3/>

## MAAPI API

Management Agent API

- Transactional Northbound interface.
- User session-based interface.
- Configuration & Operational data
  - Read.
  - Written and committed as one transaction.

```python
import ncs

with ncs.maapi.Maapi() as maapi:
  with ncs.maapi.Session(maapi=maapi, user="admin", context="system"):
    with maapi.start_read_trans() as transaction:
      address = transaction.get_elem("/ncs:devices/device{ex0}/address")
      print("First read: Address = %s" % address)

with ncs.maapi.single_write_trans(user="admin", context="system") as transaction:
  transaction.set_elem2("Vegas was here", "/ncs:devices/device{ex0}/description")
  transaction.apply()
```

<https://developer.cisco.com/docs/nso/guides/python-api-overview/>

## MAAGIC API

- Manipulate data according to YANG schema
- Use standard Python object dot notation.
- Special characters are replaced with underscores
- Element `my-address` becomes `my_address`
  - Crossing Namespaces with _double-underscore_
    - `root.myns__top.val`

> MAAGIC = Management Agent API (MAAPI) + magic Python methods

<https://developer.cisco.com/docs/nso/guides/python-api-overview/#maagic-api>

### MAAGIC Object Navigation

| Action                                       | Object Returned   |
| -------------------------------------------- | ----------------- |
| `root.devices`                               | Container         |
| `root.devices.device`                        | List              |
| `root.devices.device["ce0"]`                 | ListElement       |
| `root.devices.device['ce0'].device_type.cli` | PresenceContainer |
| `root.devices.device['ce0'].address`         | str               |
| `root.devices.device['ce0'].port`            | int               |

Maagic object from a keypath:
`node = ncs.maagic.get_node(transaction_id, '/ncs:devices/device{ce0}')`

https://developer.cisco.com/docs/nso/guides/python-api-overview/#maagic-api
https://developer.cisco.com/docs/nso/api/ncs-maagic/
