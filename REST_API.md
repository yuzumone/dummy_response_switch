# REST API
## Outline
- [GET priorities/priority](#get-prioritiespriority)
- [GET predictions/prediction](#get-predictionsprediction)
- [GET guarantee/bandwidth](#get-guaranteebandwidth)
- [GET switches/switch](#get-switchesswitch)
- [GET switches/show/:datapath_id](#get-switchesshowdatapath_id)
- [GET ports/usage](#get-portsusage)
- [GET ports/show/:hw_addr](#get-portsshowhw_addr)
- [GET system/ping](#get-systemping)
- [GET system/status](#get-systemstatus)

## GET priorities/priority
Return all of the priority information which OpenFlow controller has.

### Resource URL
http://&lt;Server_IP&gt;:&lt;Port_No&gt;/v1/prioprities/priority.json

### Resource Information
- **Response formats:** JSON

### Parameters
| Name | Explanation |
| :------------------ |  :------------------ | 
| **count**<br>optional | Specifies the number of records to retrieve. <br>Example Values: 20 |

### Example Request
GET  
http://192.168.1.10:8080/v1/priorities/priority.json?count=20

### Example Result
```json
[
  {
    "name": "laptop",
    "hw_addr": "11:22:33:44:55:66"
  },
  {
    "name": "phone",
    "hw_addr": "77:88:99:aa:bb:cc"
  }
]  
```

## GET predictions/prediction
Return all bandwidth prediction results.

### Resource URL
http://&lt;Server_IP&gt;:&lt;Port_No&gt;/v1/predictions/prediction.json

### Resource Information
- **Response formats:** JSON

### Parameters
| Name | Explanation |
| :------------------ |  :------------------ | 
| **datapath_id**<br>required | The datapath id of the OpenFlow switch.<br>Example Values: 0000000000000001 |
| **count**<br>optional | Specifies the number of records to retrieve.<br>Example Values: 20 |

### Example Request
GET  
http://192.168.1.10:8080/v1/predictions/prediction.json?datapath_id=0000000000000001

### Example Result
```json
[
  {
    "time": "Tue Oct 25 10:00:00 +0900 2016",
    "bandwidth": 10000000
  },
  {
    "time": "Tue Oct 25 10:01:00 +0900 2016",
    "bandwidth": 9000000
  }
]
```

## GET guarantee/bandwidth
Return the guarantee bandwidth based on bandwidth predictions.

### Resource URL
http://&lt;Server_IP&gt;:&lt;Port_No&gt;/v1/guarantee/bandwidth.json

### Resource Information
- **Response formats:** JSON

### Parameters
| Name | Explanation |
| :------------------ |  :------------------ | 
| **datapath_id**<br>required | The datapath id of the OpenFlow switch.<br>Example Values: 0000000000000001 |

### Example Request
GET  
http://192.168.1.10:8080/v1/guarantee/bandwidth.json?datapath_id=0000000000000001

### Example Result
```json
{
  "time": "Tue Oct 25 10:00:00 +0900 2016",
  "bandwidth": 7000000
}
```

## GET switches/switch
Return all of the OpenFlow switch information that are connected to the OpenFlow controller.

### Resource URL
http://&lt;Server_IP&gt;:&lt;Port_No&gt;/v1/switches/switch.json

### Resource Information
- **Response formats:** JSON

### Parameters
| Name | Explanation |
| :------------------ |  :------------------ | 
| **count**<br>optional | Specifies the number of records to retrieve.<br>Example Values: 20 |

### Example Request
GET  
http://192.168.1.10:8080/v1/switches/switch.json

### Example Result
```json
[
  {
    "datapath_id": 0000000000000001,
    "ports": [
      {
        "name": "phone",
        "hw_addr": "00:00:00:00:00:00",
        "port_no": 4,
        "state": 4,
        "max_speed": 5000
      },
      {
        "name": "tablet",
        "hw_addr": "11:11:11:11:11:11",
        "port_no": 5,
        "state": 4,
        "max_speed": 5000
      }
    ]
  },
  {
    "datapath_id": 0000000000000002,
    "ports": [
      {
        "name": "phone",
        "hw_addr": "22:22:22:22:22:22",
        "port_no": 3,
        "state": 4,
        "max_speed": 1000
      }
    ]
  }
]
```

## GET switches/show:datapath_id
Return a single OpenFlow switch information, specified by the datapath id parameter.

### Resource URL
http://&lt;Server_IP&gt;:&lt;Port_No&gt;/v1/switches/show.json

### Resource Information
- **Response formats:** JSON

### Parameters
| Name | Explanation |
| :------------------ |  :------------------ | 
| **datapath_id**<br>required | The datapath id of the OpenFlow switch.<br>Example Values: 0000000000000001 |

### Example Request
GET  
http://192.168.1.10:8080/v1/switches/show.json?datapath_id=0000000000000001

### Example Result
```json
{
  "datapath_id": 0000000000000001,
  "ports": [
    {
      "name": "phone",
      "hw_addr": "00:00:00:00:00:00",
      "port_no": 4,
      "state": 4,
      "max_speed": 5000
    },
    {
      "name": "tablet",
      "hw_addr": "11:11:11:11:11:11",
      "port_no": 5,
      "state": 4,
      "max_speed": 5000
    }
  ]
}
```

## GET ports/usage
Return all of the bandwidth usage information of each port.

### Resource URL
http://&lt;Server_IP&gt;:&lt;Port_No&gt;/v1/devices/usage.json

### Resource Information
- **Response formats:** JSON

### Parameters
| Name | Explanation |
| :------------------ |  :------------------ | 
| **datapath_id**<br>required | The datapath id of the OpenFlow switch.<br>Example Values: 0000000000000001 |
| **count**<br>optional | Specifies the number of records to retrieve.<br>Example Values: 20 |

### Example Request
GET  
http://192.168.1.10:8080/v1/devices/usage.json?datapath_id=0000000000000001

### Example Result
```json
[
  {
    "name": "phone",
    "hw_addr": "00:00:00:00:00:00",
    "bandwidths": [
      {
        "time": "Tue Oct 25 10:02:00 +0900 2016",
        "bandwidth": 500
      },
      {
        "time": "Tue Oct 25 10:01:00 +0900 2016",
        "bandwidth": 500
      },
      {
        "time": "Tue Oct 25 10:00:00 +0900 2016",
        "bandwidth": 550
      }
    ]
  },
  {
    "name": "tablet",
    "hw_addr": "11:11:11:11:11:11",
    "bandwidths": [
      {
        "time": "Tue Oct 25 10:02:00 +0900 2016",
        "bandwidth": 500
      },
      {
        "time": "Tue Oct 25 10:01:00 +0900 2016",
        "bandwidth": 500
      },
      {
        "time": "Tue Oct 25 10:00:00 +0900 2016",
        "bandwidth": 550
      }
    ]
  }
]
```

## GET ports/show/:hw_addr
Return a single port information, specified by the MAC address parameter.

### Resource URL
http://&lt;Server_IP&gt;:&lt;Port_No&gt;/v1/devices/show.json

### Resource Information
- **Response formats:** JSON

### Parameters
| Name | Explanation |
| :------------------ |  :------------------ | 
| **hw_addr**<br>required | The MAC address of the port.<br>Example Values: 00:00:00:00:00:00 |

### Example Request
GET  
http://192.168.1.10:8080/v1/devices/show.json?hw_addr=11:11:11:11:11:11

### Example Result
```json
{
  "name": "phone",
  "hw_addr": "11:11:11:11:11:11",
  "port_no": 3,
  "state": 4,
  "max_speed": 1000,
  "bandwidths": [
    {
      "time": "Tue Oct 25 10:02:00 +0900 2016",
      "bandwidth": 500
    },
    {
      "time": "Tue Oct 25 10:01:00 +0900 2016",
      "bandwidth": 500
    },
    {
      "time": "Tue Oct 25 10:00:00 +0900 2016",
      "bandwidth": 550
    }
  ]
}
```

## GET system/ping
Return ping.

### Resource URL
http://&lt;Server_IP&gt;:&lt;Port_No&gt;/v1/system/ping.json

### Resource Information
- **Response formats:** JSON

### Example Result
```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
...
```

## GET system/status
Return all of the system message information.

### Resource URL
http://&lt;Server_IP&gt;:&lt;Port_No&gt;/v1/system/status.json

### Resource Information
- **Response formats:** JSON

### Parameters
| Name | Explanation |
| :------------------ |  :------------------ | 
| **count**<br>optinal | Specifies the number of records to retrieve.<br>Example Values: 20 |

### Example Result