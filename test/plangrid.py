import requests
from collections import OrderedDict

api_prefix = 'https://io.plangrid.com'
api_key = '4271a24c984e6f1143f3d68ccbe1a387'
version_headers = {'Accept': 'application/vnd.plangrid+json; version=1'}

def get_first_project_uid():
    # Get the UID of the first project returned from the API
    projects_url = '{}/projects'.format(api_prefix)
    response = requests.get(projects_url, auth=(api_key, None), headers=version_headers)
    projects = response.json()['data']
    print projects[0]
    first_project_uid = projects[0]['uid']
    return first_project_uid

def request_attachment_upload(project_uid):
    attachment_upload_url = '{}/projects/{}/attachments/uploads'.format(api_prefix, project_uid)
    headers = {'content-type': 'application/json'}
    headers.update(version_headers)
    data = {'content_type': 'application/pdf', 'name': '0001-060000-1.pdf', 'folder': 'Submittals'}
    response = requests.post(attachment_upload_url, json=data, headers=headers,
                             auth=(api_key, None))
    file_upload_info = response.json()
    print response.text
    return file_upload_info

def upload_file(file_upload_info):
    url = '{}?'.format(file_upload_info['aws_post_form_arguments']['action'])
    fields = file_upload_info['aws_post_form_arguments']['fields']
    fields = OrderedDict([(kv['name'], kv['value']) for kv in fields])
    files = OrderedDict([('file', open('sample1.pdf'))])
    response = requests.post(url, files=files, data=fields)
    return response.text

# Example
project_uid = get_first_project_uid()

# Step 1
file_upload_info = request_attachment_upload(project_uid=project_uid)

# Step 2 (3 is handled automatically)
print upload_file(file_upload_info=file_upload_info)