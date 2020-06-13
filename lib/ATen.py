
from lib.utils import  logger

IP_HEADER = "X-ClientIP"

def GetXClientIP(request):
    try:
        return request.headers[IP_HEADER]
    except Exception as e:
        return request.remote_addr


    
