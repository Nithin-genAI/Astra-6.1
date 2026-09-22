class LoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print(f"Hey I got Request Method: {request.method},for Request Path: {request.path}")
        print(f"Here is the IP Address of User: {request.META['REMOTE_ADDR']}")
        print(f"Here is the User Agent: {request.META['HTTP_USER_AGENT']}")
        #print(f"Request Headers: {request.headers}")
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        print(f"Response Status Code: {response.status_code}")

        return response