from flask import request
from app import app

import base64
import json
import os

@app.route('/mutate', methods=['POST'])
def mutate():
  try:
    request_json = json.loads(request.data.decode('utf-8'))
  except Exception as e:
    print(str(e))

  response = {
    "apiVersion": "admission.k8s.io/v1",
    "kind": "AdmissionReview",
    "response": {
      "uid": request_json['request']['uid'],
      "allowed": True,
    }
  }

  labels = request_json['request']['object']['metadata']['labels']
  if "tcpdump-sidecar" not in labels:
    return json.dumps(response), 200, {'ContentType':'application/json-patch+json'} 

  patch = """
    [
      { 
        "op": "add",
        "path": "/spec/containers/1",
        "value": {
          "image": "bilalunalnet/tcpdump-alpine",
          "name": "tcpdump-sidecar" 
        }
      }
    ]
    """
  patch_bytes = patch.encode('ascii')
  patch_base64_bytes = base64.b64encode(patch_bytes)
  patch_base64 = patch_base64_bytes.decode('ascii')

  response['response']['patch'] = patch_base64
  response['response']['patchType'] = "JSONPatch"

  return json.dumps(response), 200, {'ContentType':'application/json-patch+json'} 
