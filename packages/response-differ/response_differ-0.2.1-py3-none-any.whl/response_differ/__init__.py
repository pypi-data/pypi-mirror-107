import copy

from vcr import cassette
from vcr.matchers import requests_match
from vcr import stubs


def _load_patched(self):
    try:
        requests, responses = self._persister.load_cassette(self._path, serializer=self._serializer)
        #if not responses:
        #    for r in requests:
        #       self.data.append((r, None))
            #self.responses.append(responses)
            #for request in requests:
             #   self.requests.append(request)
        #else:
        if responses:
            res_req = zip(requests, responses)
        else:
            res_req = [(r, responses) for r in requests]
        for request, response in res_req:
            self.append(request, response)
        self.dirty = False
        self.rewound = True
    except ValueError:
        pass


def append_patched(self, request, response):
    """Add a request, response pair to this cassette"""
    #log.info("Appending request %s and response %s", request, response)
    if response and [] in self.responses:
        self.__dict__.update({"data": [], "requests": [], "responses": []})
    request = self._before_record_request(request)
    if not request:
        return
    # Deepcopy is here because mutation of `response` will corrupt the
    # real response.
    response = copy.deepcopy(response)
    response = self._before_record_response(response)
    self.data.append((request, response))
    self.dirty = True


cassette.Cassette._load = _load_patched
cassette.Cassette.append = append_patched
