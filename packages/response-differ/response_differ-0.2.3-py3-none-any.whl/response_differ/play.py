import importlib
import json
from subprocess import Popen, PIPE

import requests
import yaml

from requests.structures import CaseInsensitiveDict
from vcr import VCR

from response_differ import cheks
from response_differ.Config_store import Serialize
from response_differ.cassetes.serializer import filter_cassette
from response_differ.cheks import Replayed


#custom_serializer_path = 'tests.custom_serializer2'
#custom_serializer_path = []

def get_vcr():
    if Serialize.custom_serializer_path:
        d = Serialize.custom_serializer_path[0].replace('/', '.')
        s = d.replace('.py', '')
        serializer = importlib.import_module(s)
    else:
        from response_differ.cassetes import serializer

    d_vcr = VCR(record_mode='all')
    d_vcr.register_serializer(name='binary', serializer=serializer.BinarySerializer())
    d_vcr.serializer = 'binary'
    d_vcr.register_persister(serializer.CustomPersister)
    return d_vcr

def get_prepared_request(data):
    prepared = requests.PreparedRequest()
    prepared.method = data["method"]
    prepared.url = data["uri"]
    prepared._cookies = RequestsCookieJar()
    prepared.body = data["body"]
    prepared.headers = CaseInsensitiveDict([('Accept', '*/*')])
    if data.get('headers'):
        prepared.headers = CaseInsensitiveDict([(key, value[0]) for key, value in data["headers"].items()])
    #if data.get('headers'):
    #    prepared.headers = CaseInsensitiveDict(data["headers"])
    return prepared


def store_responses(replayed):
    if not replayed.cass_response:
        raise Exception("Not response. не передавайте флаг дифф")
    #Replayed.responses.append(
    #    {
    #       'id': replayed.interaction['id'],
    #        'uri': urlparse(replayed.interaction['request']['uri']).path,
    #        'old': json.loads(replayed.interaction['response']['body']['string']),
    #       'new': replayed.response.json()
    #    })


def get_cassette(cassette_path):
    with open(cassette_path) as cass:
        if cass.name.lower().endswith(('yaml', 'yml')):
            return yaml.load(cass, Loader=yaml.SafeLoader)
        if cass.name.lower().endswith('json'):
            return json.load(cass)
        else:
            raise Exception('cassette format should be yaml or json')


def grpc_request(cassette_path, host, diff):
    d_vcr = get_vcr()
    with d_vcr.use_cassette(f'{cassette_path}') as cass:
        cass_data = cass.data.copy()

    with d_vcr.use_cassette(f'{cassette_path}') as cass2:
        for request, cass_response in cass_data:
            grpc_cli = ['grpc_cli', 'call', '--json_input', '--json_output', host, request['uri'], json.dumps(request['body'])]
            process = Popen(grpc_cli, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()

            cass2.append(request, stdout.decode('utf-8'))
            #VCRConnection.getresponse(cass2)

            replayed = Replayed(request, stdout, cass_response)
            Replayed.responses_list.append(stdout)
            yield replayed
            #cheks.check_status_code(replayed)
            diff and store_responses(replayed)

    #'grpc_cli call service1.stg.a.o3.ru:82 Cpu "hosts: ['wallet-broker.stg.a.o3.ru'],permanent: true"'

    #with d_vcr.use_cassette(f'{cassette_path}') as cass:
#
    #    uri = f'{host}{cass["uri"]}'
    #    a = cass['requests']
#
    #    request_data = cass['body']
    #    client = Client.get_by_endpoint(host)
    #    response = client.request("helloworld.Greeter", "SayHello", request_data)
#
    #    response = requests.post(uri, headers=cass['headers'], data=body)
    #    resp.append(response)
    #return response


def http_request(cassette_path, host, diff, status, ignore_body):
    d_vcr = get_vcr()
    with d_vcr.use_cassette(f'{cassette_path}') as cass:
        cass_data = filter_cassette(cass.data.copy(), status=status, ignore_body=ignore_body)

    with d_vcr.use_cassette(f'new_{cassette_path}'):
        for id, (request, cass_response) in enumerate(list(cass_data)):
            uri = f"{request.protocol}://{request.host}:{request.port}{request.path}"
            #async with httpx.AsyncClient() as client:
            #    response = await client.post(
            #        f"{request.protocol}://{request.host}:{request.port}{request.path}",
            #        headers=request.headers,
            #        data=request.body
            #    )
            if host:
                uri = f'{host}{request.path}'
            response = requests.post(
               uri,
               headers=request.headers,
               data=request.body.decode('utf-8')
           )
            replayed = Replayed(id, request, response, cass_response)
            Replayed.responses_list.append(response)
            yield replayed
            cheks.check_status_code(replayed)
            diff and store_responses(replayed)


def replay(cassette_path, host, protocol, ignore_body,  status=None, diff=None):
    #cassette = get_cassette(cassette_path)
    if protocol == 'grpc':
        yield from grpc_request(cassette_path, host, diff)
    else:
        yield from list(http_request(cassette_path, host, diff, status, ignore_body))
    #session = requests.Session()
    #for interaction in filter_cassette(cassette['interactions'], status, uri):
    #    request = interaction["request"]
#
    #    #request = get_prepared_request(interaction["request"])
    #    d_vcr = d_vcr_get()
    #    with d_vcr.use_cassette(f'new_{cassette_path}'):
    #        response = requests.post(request['uri'], headers=request['headers'], data=request['body'])
    #        #response = session.send(request)
    #        replayed = Replayed(interaction, response)
    #        yield replayed
    #        cheks.check_status_code(replayed)
    #        diff and store_responses(replayed)
