# -*- coding: utf-8 -*-

# Copyright (c) 2014, Joshua Stone
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
from requests import codes
from sys import version_info
from .helpers import format_params, join_params

__all__ = [
  "url",
  "request",
  "get_images",
  "get_image_data",
  "set_limit"
]

if version_info < (3, 0):
  from urllib import urlencode
else:
  from urllib.parse import urlencode

def url(params):
  p = format_params(params)
  url = "https://derpibooru.org/search?{}".format(urlencode(p))

  return url

def request(params):
  session = params["session"]
  search, p = "https://derpibooru.org/search.json", format_params(params)

  request = session.get(search, params=p)

  while request.status_code == codes.ok:
    images, image_count = request.json()["search"], 0
    for image in images:
      image["scope"] = {"total": request.json()["total"], "this": image_count+1}
      yield image
      image_count += 1
    if image_count < 50:
      break

    p["page"] += 1

    request = session.get(search, params=p)

def get_images(parameters, limit=50):
  session = parameters["session"]
  params = join_params(parameters, {"perpage": 50, "page": 1})

  if parameters["filter"] is not None:
    set_site_filter(session, parameters["filter"])

  if limit is not None:
    l = limit
    if l > 0:
      r, counter = request(params), 0
      for index, image in enumerate(r, start=1):
        yield image
        if index >= l:
          break
  else:
    r = request(params)
    for image in r:
      yield image

def get_image_data(session, id_number):
  url = "https://derpibooru.org/{}.json?fav=&comments=".format(id_number)

  request = session.get(url)

  if request.status_code == codes.ok:
    data = request.json()

    if "duplicate_of" in data:
      return get_image_data(data["duplicate_of"])
    else:
      return data

def set_site_filter(session, filter_id):
  spoofrequest = session.get("https://derpibooru.org/filters")  # Contacted Clover, hopefully won't need this later
  spoofdata = {"_method": "patch"}
  if spoofrequest.status_code == codes.ok:
    csrfnameregex = '<meta name="csrf-param" content="(.+?)"\/>'  # I know, regex and HTML
    csrfregex = '<meta name="csrf-token" content="(.+?)"\/>'  # I am the devil reincarnate
    spoofdata[re.search(csrfnameregex, spoofrequest.text).group(1)] = re.search(csrfregex, spoofrequest.text).group(1)
  else:
    return False
  url = "https://derpibooru.org/filters/select?id={}".format(filter_id)
  remoterequest = session.post(url, data=spoofdata)
  return remoterequest.status_code == codes.found or remoterequest.status_code == codes.ok
