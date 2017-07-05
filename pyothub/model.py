"""
...
"""



devicekeys = {'0001': 'asdfsfgw3g',
              '0002': 'uhwefuihwef',
              '0003': 'uihwefiuhawefawef',
              '0004': 'uoihwefiuhwef',
              '0005': 'iqweroih1r'}


def getDeviceKey(deviceid):
    return devicekeys.get(deviceid)
