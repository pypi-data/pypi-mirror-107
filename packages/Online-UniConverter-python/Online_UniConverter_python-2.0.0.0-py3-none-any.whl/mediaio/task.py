import os
import json
import time
import requests 
from requests_toolbelt.multipart import encoder
from mediaio.resource import Create, Info, Resource, Wait
import mediaio.utils as util


class Upload(Resource): 
    @classmethod
    def upload(cls, file_name, task, progressCallback=None):
        """Upload a resource e.g.
        """
        form = task['data']['result']['form']
        port_url = form['url']
        params = form['parameters']
        params['x:timestamp'] = int(time.time())       
       
        fields = params if params else {}
        try:
            file = open(file_name, 'rb')
            _, shortName, ext = util.get_fileNameExt(file_name)
            for key in fields.keys():
                if isinstance(fields[key], int):
                    fields[key] = str(fields[key])
            fields['file'] = (shortName+ext, file, 'video/mp4')
            e = encoder.MultipartEncoder(fields=fields)
            m = encoder.MultipartEncoderMonitor(e, progressCallback)     
            res = requests.request(method='POST', url=port_url, data=m, headers={'Content-Type': m.content_type})                       
            file.close()
            if res.status_code != 200:
                raise Exception("got exception while uploading file")
            else:
                result = json.loads(res.text)
                if result['code'] > 0: 
                    raise Exception(result['msg'])
                if result['data']['status']=='failed':
                    raise Exception(result['data']['message'])    
                return result
        except Exception as e:
            raise Exception("got exception while uploading file")    
                      
class Task(Create, Upload, Info, Wait):
    """Task class wrapping the REST v2/tasks endpoint. Enabling New Task Creation, Showing a task, Waiting for task,
    Finding a task, Deleting a task, Cancelling a running task.

    Usage::        
        >>> Task.create(name="import/url")
    """

    path = "v2/tasks"  


Task.convert_resources['tasks'] = Task
Task.convert_resources['task'] = Task
