import os
import re

import yaml
from requests.structures import CaseInsensitiveDict
from vcr.request import Request
from vcr.serialize import CASSETTE_FORMAT_VERSION, _warn_about_old_cassette_format, _looks_like_an_old_cassette
from vcr.serializers import compat
from vcr.serializers.compat import convert_to_bytes

from response_differ.cheks import Replayed

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_headers(request):
    if not request.get('headers'):
        request['headers'] = {}
    else:
        request['headers'] = CaseInsensitiveDict([(key, value[0]) for key, value in request["headers"].items()])
    return request


class BinarySerializer(object):

    @classmethod
    def deserialize(cls, cassette_string):
        data = yaml.load(cassette_string, Loader=yaml.Loader)

        request = [Request._from_dict(get_headers(compat.convert_to_unicode(r['request']))) for r in data["interactions"]]
        #request = [dict(zip(('uri', 'request_data'), itemgetter('call', 'payload')(d))) for d in data]
        response = [r["response"] for r in data["interactions"] if r.get('response')]
        return request, response

    @classmethod
    def serialize(cls, cassette_dict):
        resp = Replayed.responses_list
        #for x in cassette_dict:
        #    if x.get('responses'):
        #        pass
        interactions = [
            {
                "id": str(i),
                "request": compat.convert_to_unicode(r[0]._to_dict()),
                "response": compat.convert_to_unicode(r[1]),
            }
            for i, r in enumerate(zip(cassette_dict["requests"], cassette_dict["responses"]))
        ]
        data = {"version": CASSETTE_FORMAT_VERSION, "interactions": interactions}
        return yaml.dump(data, Dumper=Dumper, allow_unicode=True)


class CustomPersister:
    @classmethod
    def load_cassette(cls, cassette_path, serializer=BinarySerializer):
        try:
            with open(cassette_path) as f:
                cassette_content = f.read()
        except OSError:
            raise ValueError("Cassette not found.")
        cassette = serializer.deserialize(cassette_content)
        return cassette

    @staticmethod
    def save_cassette(cassette_path, cassette_dict,
                      serializer=BinarySerializer):
        cassette_path = f'new_{cassette_path}'
        data = serializer.serialize(cassette_dict)
        dirname, filename = os.path.split(cassette_path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        if filename and not os.path.exists(dirname):
            open(filename, 'w')
        with open(cassette_path, "wb") as f:
            #f.write(data)
            f.write(data.encode('utf-8'))


def filter_cassette(
        interactions, id_=None, status=None, uri=None, method=None, ignore_body=None
):

    filters = []

    def id_filter(item):
        return item["id"] == id_

    def status_filter(item):
        return item[1]['status']['code'] == status

    def uri_filter(item):
        return bool(re.search(uri, item["request"]["uri"]))

    def method_filter(item):
        return bool(re.search(method, item["request"]["method"]))

    def body_filter(item):
        return item[1]["body"]["string"].rstrip() != ignore_body

    if id_ is not None:
        filters.append(id_filter)

    if status is not None:
        filters.append(status_filter)

    if uri is not None:
        filters.append(uri_filter)

    if method is not None:
        filters.append(method_filter)

    if ignore_body is not None:
        filters.append(body_filter)

    def is_match(interaction):
        return all(filter_(interaction) for filter_ in filters)

    return filter(is_match, interactions)