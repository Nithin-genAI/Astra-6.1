class LoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        # Code to be executed for each request before
        print(f"Hey I got Request Method: {request.method},for Request Path: {request.path}")
        #print(f"Request Headers: {request.headers}")
        response = self.get_response(request)
        # Code to be executed for each request/response after
        print(f"Response Status Code: {response.status_code}")

        return response

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        print(f"{request.method} request from IP: {client_ip}")
        print(f"Here is the User Agent: {request.META.get('HTTP_USER_AGENT', 'unknown')}")
        response = self.get_response(request)
        return response