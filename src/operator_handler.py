import kopf
import kubernetes
import json
import logging
from base64 import b64encode

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@kopf.on.create('juanjo.garciaamaya.com','v1alpha1','resecret')
def create_fn(body, spec, **kwargs):
  # API Server handler
  api = kubernetes.client.CoreV1Api()

  # Get info from resecret body
  name = body['metadata']['name']
  namespace = body['metadata']['namespace']

  # Secret template
  secret = {
    'apiVersion': 'v1',
    'kind': 'Secret',
    'metadata': {
      'name': spec['name']
    },
    'data': {}
  }

  if 'labels' in body['metadata']:
      secret['labels'] = body['metadata']['labels']

  # Process secret data
  for data in spec['secrets']:
    logger.warning(json.dumps(data))
    if 'value' in data:
      value = data['value']
    else:
      ref_secret = api.read_namespaced_secret(name=data['secretKeyRef']['name'], namespace=namespace)
      #value = b64encode((data['secretKeyRef']['name'] + '.' + data['secretKeyRef']['key']).encode()).decode()
      value = ref_secret.data[data['secretKeyRef']['key']]

    secret['data'][data['key']] = value

  # Make the secret child of the resecret object
  kopf.adopt(secret, owner=body)


  # Create secret
  obj = api.create_namespaced_secret(namespace, secret)
  msg = f"Secret {obj.metadata.name} created"
  logger.info(msg)

  return {'message': msg}

@kopf.on.delete('juanjo.garciaamaya.com', 'v1alpha1', 'resecret')
def delete(body, **kwarg):
  msg = f"Resecret {body['metadata']['name']} and its secret child deleted"

  return {'message': msg}
