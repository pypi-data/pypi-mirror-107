import time
from mediaio.mediaiorestclient import *
from mediaio.task import Task

def configure(**config):
    """
    Configure the REST Client With Latest API Key and Mode
    :return:
    """
    set_config(**config)


def default():
    """
    Configure the REST Client With Default API Key and Mode
    :return:
    """
    default_client()

 

def _importFile(urlOrFile, progress):
    if urlOrFile.startswith('http'):
        task = Task.create(operation='import/url')
        result = Task.wait(id, progressCallback=lambda value: progress(0, value))      
    elif urlOrFile.startswith('base64'):
        task = Task.create(operation='import/base64')
        result = Task.wait(id, progressCallback=lambda value: progress(0, value))
    else:
        task = Task.create(operation='import/upload')
        if task['code'] >0: raise Exception(task['msg'])   
        result = Task.upload(file_name=urlOrFile, task=task, progressCallback = lambda moniter: progress(0, moniter.bytes_read / moniter.len))        
    return result

def _exportFile(task_id, progress):
    task = Task.create(operation='export/url', payload={'input': task_id})
    result = Task.wait(task['data']['id'], progressCallback=lambda value: progress(2, value))          
    return result['data']['result']['files'][0]                    

def _compressFileProcess(task_id, input_format, output_format = None, ratio=None, bitrate=None, progress=None):
    payload = {
            'input': task_id,
            'input_format': input_format,
            'output_format': output_format if output_format else input_format
    }
    if ratio: payload['ratio'] = str(ratio)
    if bitrate: payload['bitrate'] = int(bitrate)
    task = Task.create(operation='compress', payload=payload) 
    if (task['code'] > 0): raise Exception(task['msg'])   
    return Task.wait(task['data']['id'], progressCallback=lambda value: progress(1, value))     

def convertFile(urlOrFile, input_format, output_format, advanceParams=None, progress=lambda step, value: print(step, value)):
    result = _importFile(urlOrFile, progress)

    payload ={
        'input': result['data']['id'],
        'input_format': input_format,
        'output_format': output_format,
    }    
    if advanceParams: 
        payload.update(advanceParams)
    task = Task.create(operation='convert', payload=payload) 
    result = Task.wait(task['data']['id'], progressCallback=lambda value: progress(1, value))   
    return _exportFile(result['data']['id'], progress)

def compressVideo(urlOrFile, input_format, ratio, progress=lambda step, value: print(step, value)):
    result = _importFile(urlOrFile, progress)
    result = _compressFileProcess(result['data']['id'], input_format, ratio=ratio, progress=progress)    
    return _exportFile(result['data']['id'], progress)

def compressAudio(urlOrFile, input_format, bitrate, progress=lambda step, value: print(step, value)):
    result = _importFile(urlOrFile, progress)
    result = _compressFileProcess(result['data']['id'], input_format, bitrate=bitrate, progress=progress)    
    return _exportFile(result['data']['id'], progress)

def compressImage(urlOrFile, input_format, progress=lambda step, value: print(step, value)):
    result = _importFile(urlOrFile, progress)
    result = _compressFileProcess(result['data']['id'], input_format, progress=progress)    
    return _exportFile(result['data']['id'], progress)
