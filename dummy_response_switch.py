# Copyright 2016 yuzumone
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import random

from datetime import timedelta, datetime

import pytz
from ryu.app import simple_switch_13
from webob import Response
from ryu.app.wsgi import ControllerBase, WSGIApplication, route

switch_instance = 'switch_instance'


class DummyResponseSwitch(simple_switch_13.SimpleSwitch13):
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(DummyResponseSwitch, self).__init__(*args, **kwargs)
        self.switches = {}
        wsgi = kwargs['wsgi']
        wsgi.register(RESTController, {switch_instance: self})
        self.priorities = []
        self.predictions = []
        self.guarantee = {}
        self.ports = []
        self.switches = []
        self.statuses = []
        self.prepare_dummy_data()

    def prepare_dummy_data(self):
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        # priorities
        for var in range(0, 20):
            device = 'device' + str(var)
            mac = ':'.join(map(lambda x: "%02x" % x, [0xb8, 0xae, 0xed,
                                                      random.randint(0x00, 0x7f),
                                                      random.randint(0x00, 0xff),
                                                      random.randint(0x00, 0xff)]))
            priority = {'name': device, 'hw_addr': mac}
            self.priorities.append(priority)

        # predictions
        for var in range(0, 20):
            time = time - timedelta(minutes=1)
            bandwidth = random.randint(1000000, 100000000)
            bandwidth = {'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'bandwidth': bandwidth}
            self.predictions.append(bandwidth)

        # guarantee
        guarantee_bandwidth = int(self.predictions[0]['bandwidth'] * 0.7)
        self.guarantee = {'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'bandwidth': guarantee_bandwidth}

        # ports
        ports_bandwidths = []
        for var in range(0, 20):
            time = time - timedelta(minutes=1)
            bandwidth = random.randint(1000000, 100000000)
            bandwidth = {'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'bandwidth': bandwidth}
            ports_bandwidths.append(bandwidth)
        for var in range(0, 20):
            name = 'device' + str(var)
            hw_addr = ':'.join(map(lambda x: "%02x" % x, [0xb8, 0xae, 0xed,
                                                          random.randint(0x00, 0x7f),
                                                          random.randint(0x00, 0xff),
                                                          random.randint(0x00, 0xff)]))
            ports = {'name': name, 'hw_addr': hw_addr, 'port_no': 4, 'state': 4, 'max_speed': 10000000,
                     'bandwidths': ports_bandwidths}
            self.ports.append(ports)

        # switches
        for var in range(0, 20):
            datapath_id = var
            switch = {'datapath_id': datapath_id, 'ports': self.ports}
            self.switches.append(switch)

        # statuses
        for var in range(0, 20):
            time = time - timedelta(minutes=1)
            title = "Title"
            body = "test!!!"
            self.statuses.append(
                {'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'title': title, 'body': body})

    def get_priorities(self):
        return self.priorities

    def get_predictions(self):
        return self.predictions

    def get_guarantee(self):
        return self.guarantee

    def get_switches(self):
        return self.switches

    def get_ports(self):
        return self.ports

    def get_statuses(self):
        return self.statuses


class RESTController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(RESTController, self).__init__(req, link, data, **config)
        self.switch = data[switch_instance]

    @route('dummy_response_switch', '/v1/priorities/priority.json', methods=['GET'])
    def get_priorities(self, req, **kwargs):
        data = self.switch.get_priorities()
        params = req.params.mixed()
        if 'count' in params:
            count = int(params['count'])
            if count > len(data):
                count = len(data)
            priorities = data[:count]
        else:
            priorities = data
        priorities_json = json.dumps(priorities)
        return Response(content_type='application/json', body=priorities_json)

    @route('dummy_response_switch', '/v1/predictions/prediction.json', methods=['GET'])
    def get_predictions(self, req, **kwargs):
        data = self.switch.get_predictions()
        params = req.params.mixed()
        if 'datapath_id' in params:
            datapath_id = params['datapath_id']
        else:
            return Response(status=400)
        if 'count' in params:
            count = int(params['count'])
            if count > len(data):
                count = len(data)
            predictions = data[:count]
        else:
            predictions = data
        predictions_json = json.dumps(predictions)
        return Response(content_type='application/json', body=predictions_json)

    @route('dummy_response_switch', '/v1/guarantee/bandwidth.json', methods=['GET'])
    def get_guarantee_bandwidth(self, req, **kwargs):
        data = self.switch.get_guarantee()
        params = req.params.mixed()
        if 'datapath_id' in params:
            datapath_id = params['datapath_id']
        else:
            return Response(status=400)
        guarantee_json = json.dumps(data)
        return Response(content_type='application/json', body=guarantee_json)

    @route('dummy_response_switch', '/v1/switches/switch.json', methods=['GET'])
    def get_switches(self, req, **kwargs):
        data = self.switch.get_switches()
        params = req.params.mixed()
        if 'count' in params:
            count = int(params['count'])
            if count > len(data):
                count = len(data)
            switches = data[:count]
        else:
            switches = data
        switches_json = json.dumps(switches)
        return Response(content_type='application/json', body=switches_json)

    @route('dummy_response_switch', '/v1/switches/show.json', methods=['GET'])
    def get_switch(self, req, **kwargs):
        data = self.switch.get_switches()
        params = req.params.mixed()
        if 'datapath_id' in params:
            datapath_id = params['datapath_id']
        else:
            return Response(status=400)
        switch = data[0]
        switch_json = json.dumps(switch)
        return Response(content_type='application/json', body=switch_json)

    @route('dummy_response_switch', '/v1/ports/usage.json', methods=['GET'])
    def get_ports(self, req, **kwargs):
        data = self.switch.get_ports()
        params = req.params.mixed()
        if 'datapath_id' in params:
            datapath_id = params['datapath_id']
        else:
            return Response(status=400)
        if 'count' in params:
            count = int(params['count'])
            if count > len(data):
                count = len(data)
            ports = data[:count]
        else:
            ports = data
        devices_json = json.dumps(ports)
        return Response(content_type='application/json', body=devices_json)

    @route('dummy_response_switch', '/v1/ports/show.json', methods=['GET'])
    def get_port(self, req, **kwargs):
        data = self.switch.get_ports()
        params = req.params.mixed()
        if 'hw_addr' in params:
            hw_addr = params['hw_addr']
        else:
            return Response(status=400)
        port = data[0]
        device_json = json.dumps(port)
        return Response(content_type='application/json', body=device_json)

    @route('dummy_response_switch', '/v1/system/ping.json', methods=['GET'])
    def ping(self, req, **kwargs):
        response = {'result': 'ok', 'code': 200}
        response_json = json.dumps(response)
        return Response(content_type='application/json', body=response_json)

    @route('dummy_response_switch', '/v1/system/status.json', methods=['GET'])
    def get_status(self, req, **kwargs):
        data = self.switch.get_statuses()
        params = req.params.mixed()
        if 'count' in params:
            count = int(params['count'])
            if count > len(data):
                count = len(data)
            statuses = data[:count]
        else:
            statuses = data
        statuses_json = json.dumps(statuses)
        return Response(content_type='application/json', body=statuses_json)
