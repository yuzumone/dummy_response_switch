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


class DummyResponseSwitch(simple_switch_13.SimpleSwitch13):
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(DummyResponseSwitch, self).__init__(*args, **kwargs)
        self.switches = {}
        wsgi = kwargs['wsgi']
        wsgi.register(RESTController)


class RESTController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(RESTController, self).__init__(req, link, data, **config)

    @route('dummy_response_switch', '/v1/priorities/priority.json', methods=['GET'])
    def get_priorities(self, req, **kwargs):
        params = req.params.mixed()
        if 'count' in params:
            count = int(params['count'])
        else:
            count = 20

        priorities = []
        for var in range(0, count):
            device = 'device' + str(var)
            mac = ':'.join(map(lambda x: "%02x" % x, [0xb8, 0xae, 0xed,
                                                      random.randint(0x00, 0x7f),
                                                      random.randint(0x00, 0xff),
                                                      random.randint(0x00, 0xff)]))
            priority = {'name': device, 'hw_addr': mac}
            priorities.append(priority)
        priorities_json = json.dumps(priorities)
        return Response(content_type='application/json', body=priorities_json)

    @route('dummy_response_switch', '/v1/predictions/prediction.json', methods=['GET'])
    def get_predictions(self, req, **kwargs):
        params = req.params.mixed()
        if 'datapath_id' in params:
            datapath_id = params['datapath_id']
        else:
            return Response(status=400)
        print 'datapath_id is ' + datapath_id

        if 'count' in params:
            count = int(params['count'])
        else:
            count = 20
        print "count is " + str(count)

        predictions = []
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        for var in range(0, count):
            time = time - timedelta(minutes=1)
            bandwidth = random.randint(1000000, 100000000)
            prediction = {'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'bandwidth': bandwidth}
            predictions.append(prediction)
        predictions_json = json.dumps(predictions)
        return Response(content_type='application/json', body=predictions_json)

    @route('dummy_response_switch', '/v1/guarantee/bandwidth.json', methods=['GET'])
    def get_guarantee_bandwidth(self, req, **kwargs):
        params = req.params.mixed()
        if 'datapath_id' in params:
            datapath_id = params['datapath_id']
        else:
            return Response(status=400)
        print 'datapath_id is ' + datapath_id

        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        guarantee = {'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'bandwidth': '7000000'}
        guarantee_json = json.dumps(guarantee)
        return Response(content_type='application/json', body=guarantee_json)

    @route('dummy_response_switch', '/v1/switches/switch.json', methods=['GET'])
    def get_switches(self, req, **kwargs):
        params = req.params.mixed()
        if 'count' in params:
            count = int(params['count'])
        else:
            count = 20
        print "count is " + str(count)

        switches = []
        bandwidths = []
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        for var in range(0, 2):
            time = time - timedelta(minutes=1)
            bandwidth = random.randint(1000000, 100000000)
            bandwidths.append({'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'bandwidth': bandwidth})
        ports = [{'name': 'phone', 'hw_addr': '00:00:00:00:00:00', 'port_no': 4, 'state': 4, 'max_speed': 10000000,
                  'bandwidths': bandwidths}]
        for var in range(0, count):
            datapath_id = var
            switch = {'datapath_id': datapath_id, 'ports': ports}
            switches.append(switch)
        switches_json = json.dumps(switches)
        return Response(content_type='application/json', body=switches_json)

    @route('dummy_response_switch', '/v1/switches/show.json', methods=['GET'])
    def get_switch(self, req, **kwargs):
        params = req.params.mixed()
        if 'datapath_id' in params:
            datapath_id = params['datapath_id']
        else:
            return Response(status=400)
        print 'datapath_id is ' + datapath_id

        bandwidths = []
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        for var in range(0, 2):
            time = time - timedelta(minutes=1)
            bandwidth = random.randint(1000000, 100000000)
            bandwidths.append({'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'bandwidth': bandwidth})
        ports = [{'name': 'phone', 'hw_addr': '00:00:00:00:00:00', 'port_no': 4, 'state': 4, 'max_speed': 10000000,
                  'bandwidths': bandwidths}]
        switch = {'datapath_id': datapath_id, 'ports': ports}
        switch_json = json.dumps(switch)
        return Response(content_type='application/json', body=switch_json)

    @route('dummy_response_switch', '/v1/ports/usage.json', methods=['GET'])
    def get_ports(self, req, **kwargs):
        params = req.params.mixed()
        if 'datapath_id' in params:
            datapath_id = params['datapath_id']
        else:
            return Response(status=400)
        print 'datapath_id is ' + datapath_id

        if 'count' in params:
            count = int(params['count'])
        else:
            count = 20
        print "count is " + str(count)

        devices = []
        bandwidths = []
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        for var in range(0, 2):
            time = time - timedelta(minutes=1)
            bandwidth = random.randint(1000000, 100000000)
            bandwidths.append({'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'bandwidth': bandwidth})
        for var in range(0, count):
            name = 'device' + str(var)
            hw_addr = ':'.join(map(lambda x: "%02x" % x, [0xb8, 0xae, 0xed,
                                                          random.randint(0x00, 0x7f),
                                                          random.randint(0x00, 0xff),
                                                          random.randint(0x00, 0xff)]))
            device = {'name': name, 'hw_addr': hw_addr, 'port_no': 4, 'state': 4, 'max_speed': 10000000,
                      'bandwidths': bandwidths}
            devices.append(device)
        devices_json = json.dumps(devices)
        return Response(content_type='application/json', body=devices_json)

    @route('dummy_response_switch', '/v1/ports/show.json', methods=['GET'])
    def get_port(self, req, **kwargs):
        params = req.params.mixed()
        if 'hw_addr' in params:
            hw_addr = params['hw_addr']
        else:
            return Response(status=400)
        print 'hw_addr is ' + hw_addr

        bandwidths = []
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        for var in range(0, 2):
            time = time - timedelta(minutes=1)
            bandwidth = random.randint(1000000, 100000000)
            bandwidths.append({'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'bandwidth': bandwidth})
        device = {'name': 'device1', 'hw_addr': hw_addr, 'port_no': 4, 'state': 4, 'max_speed': 10000000,
                  'bandwidths': bandwidths}
        device_json = json.dumps(device)
        return Response(content_type='application/json', body=device_json)

    @route('dummy_response_switch', '/v1/system/ping.json', methods=['GET'])
    def ping(self, req, **kwargs):
        response = {'result': 'ok', 'code': 200}
        response_json = json.dumps(response)
        return Response(content_type='application/json', body=response_json)

    @route('dummy_response_switch', '/v1/system/status.json', methods=['GET'])
    def get_status(self, req, **kwargs):
        params = req.params.mixed()
        if 'count' in params:
            count = params['count']
        else:
            count = 20
        print "count is " + str(count)

        statuses = []
        time = datetime.now(pytz.timezone('Asia/Tokyo'))
        for var in range(0, count):
            time = time - timedelta(minutes=1)
            title = "Title"
            body = "test!!!"
            statuses.append({'time': str(time.strftime('%a %b %d %H:%M:%S %z %Y')), 'title': title, 'body': body})
        statuses_json = json.dumps(statuses)
        return Response(content_type='application/json', body=statuses_json)
