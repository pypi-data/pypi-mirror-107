import copy
import json

import attr
import click
from deepdiff import DeepDiff
from deepdiff.model import REPORT_KEYS
from nested_lookup import nested_delete

#from response_differ import play, get_grouped_exception
#from .exceptions import get_grouped_exception


@attr.s(slots=True)
class Replayed:
    id = attr.ib()
    request = attr.ib()
    response = attr.ib()
    cass_response = attr.ib()
    responses_list = []
    config = attr.ib(default={})
    errors = []


def check_status_code(replayed):
    if not replayed.response.ok:
        message = f"URL:{replayed.response.url}\n " \
                  f"STATUS CODE: {replayed.response.status_code}"
        Replayed.errors.append(AssertionError(message))


def check_diff_responses(replayed):
    paths = Replayed.config['path']
    if replayed.request.path in paths:
        old = json.loads(replayed.cass_response['body']['string'])
        new = replayed.response.json()
        if paths[replayed.request.path]:
            old = _filter(old, filters=paths[replayed.request.path])
            new = _filter(new, filters=paths[replayed.request.path])
        result = DeepDiff(old, new,  ignore_order=True)

    #for i in replayed.cass_response:
    #    paths = Replayed.config['path']
    #    if replayed.request.path in paths:
    #        old = i['old']
    #        new = i['new']
    #        if paths[i['uri']]:
    #            old = _filter(old, filters=paths[i['uri']])
    #            new = _filter(new, filters=paths[i['uri']])
    #        result = DeepDiff(old, new, ignore_order=True)

        if any(key in list(REPORT_KEYS) for key in result.keys()):
            message = f"""
Response difference:
  {'ID'}              | {replayed.id}
  {'URI'}             | {replayed.request.uri}
  {'Difference'}      | {result}"""
            #message = f"{click.secho(f"  {'Difference'}              | {result}")}"
            Replayed.errors.append(message)
    #if Replayed.errors:
    #    raise AssertionError
                #exception_cls = get_grouped_exception(*play.Replayed.errors)
                #raise exception_cls(play.Replayed.errors)


def _filter(resp, filters):
    filtered_resp = copy.deepcopy(resp)
    for f in filters:
        filtered_resp = _filter(nested_delete(filtered_resp, f), filters=filters[1::])
    return filtered_resp
