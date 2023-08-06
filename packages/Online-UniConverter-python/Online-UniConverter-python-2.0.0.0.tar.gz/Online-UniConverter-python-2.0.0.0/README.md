# Online-UniConvert-python

This is the official Python SDK v2 for the [Online UniConverter](https://developer.media.io/) _API v2_. 

## Installation

```
 pip install Online-UniConverter-python
```

## Creating API Client

```
  import mediaio
 
  mediaio.configure(api_key = 'API_KEY')
```

Or set the environment variable `MEDIAIO_API_KEY` and use:

```
  import mediaio
 
  mediaio.default()
```

## Useage
You have tow way to use UniConvert SDK.

### **1.Facade mode**
```python
### init media.io convert env
import os
import mediaio

config = {
    'api_key' : 'api_key',
    'endpoint': 'https://api.media.io',
}

mediaio.configure(**config)

# test convert video from mov to mp4

file_info = mediaio.convertFile('56.mp4', 'mp4', 'mov')
mediaio.download(file_info['url'], os.path.join('output' , file_info['filename'])

# convert mp4 to mp3
file_info = mediaio.convertFile('56.mp4', 'mp4', 'mp3')
mediaio.download(file_info['url'], os.path.join('output' , file_info['filename'])

# convert png to bmp 
file_info = mediaio.convertFile('56.png', 'png', 'bmp')
mediaio.download(file_info['url'], os.path.join('output' , file_info['filename'])

# compress video

file_info = mediaio.compressVideo('11.mp4', 'mp4', ratio=0.9)
print(file_info)
mediaio.download(file_info['url'], os.path.join('output' , file_info['filename']))

# compress audio
file_info = mediaio.compressAudio('2.mp3', 'mp3', bitrate=96)
print(file_info)
mediaio.download(file_info['url'], os.path.join('output', file_info['filename']))

# compress png
file_info = mediaio.compressImage('13.png', 'png')
print(file_info)
mediaio.download(file_info['url'], os.path.join('output', file_info['filename']))

# need progress
def convertCallback(step, progress):
    print(step, progress)

file_info = mediaio.convertFile('56.mp4', 'mp4', 'mov')
mediaio.download(file_info['url'], os.path.join('output' , file_info['filename'], progress=convertCallback)

## advanceParams
advanceParams = {
    "videoParams":{
        'enable': True,
        'encode':'H264',
        'resolution':'640*360',
        'bitrate':'1500kbps',
        'frameRate':'12fps',
    },
    "audioParams":{
        'enable': True,
        'encode': 'AC-3',
        'bitrate': '96kbps'
    }
}
file_info = mediaio.convertFile('56.mp4', 'mp4', 'mp4', advanceParams=advanceParams)
mediaio.download(file_info['url'], os.path.join('output' , file_info['filename'])
```

### **2. DIY mode**

<br>

#### ***Uploading Files***

Uploads to UniConvert are done via `import/upload` tasks (see the [docs](https://developer.media.io/import-upload.html)). This SDK offers a convenient upload method:

```python

import os
from mediaio.task import Task

config = {
    'api_key' : 'api_key',
    'endpoint': 'https://api.media.io',
}

mediaio.configure(**config)

task = Task.create(operation='import/upload')
if task['code'] >0: raise Exception(task['msg'])   
result = Task.upload(file_name=urlOrFile, task=task) 
```

#### ***Convert File***
UniConvert can convert file after you uploaded file for using `convert` tasks. You can use `Task.wait` wait for task is finish.

```python

payload ={
    'input': result['data']['id'],
    'input_format': input_format,
    'output_format': output_format,
}    
if advanceParams: 
    payload.update(advanceParams)
task = Task.create(operation='convert', payload=payload) 
if (task['code'] > 0): raise Exception(task['msg'])   
result = Task.wait(task['data']['id'])   

```

#### ***Compress File***
UniConvert can convert file after you uploaded file for using `compress` tasks. You can use `Task.wait` wait for task is finish.
```python

payload = {
    'input': task_id,
    'input_format': input_format,
    'output_format': input_format,
    'ratio': 0.2 
}

task = Task.create(operation='compress', payload=payload) 
if (task['code'] > 0): raise Exception(task['msg'])   
return Task.wait(task['data']['id'])     
  
```

#### ***Downloading Files***

UniConvert can generate public URLs for using `export/url` tasks. You can use the SDK to download the output files when the task is finished.

```python
from mediaio.task import Task
task_id = '{task_id}'
task = Task.create(operation='export/url', payload={'input': task_id})
result = Task.wait(task['data']['id'])          
fileInfo = result['data']['result']['files'][0] 
```

## **Resource**
* [API Doc](https://developer.media.io/api-introduction.html)
* [API Price](https://developer.media.io/api-pricing.html)
* [Support Format](https://developer.media.io/api-formats.html)
* [Feedback](mailto:onlineuniconverter@service.wondershare.com)