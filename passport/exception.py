
class SnackException(Exception):
    
    message = _("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass
        if not message:
            try:
                message = self.message % kwargs
            except Exception as e:
                message = self.message

        super(SnackException, self).__init__(message)

class InvalidRequestArgument(SnackException):
    message = _("Invalid request argument.")

class NotLoggedInError(SnackException):
    message = _("Not logged in yet")

class APIRequestError(SnackException):
    message = _("Error happens when request API message :"
                " %(message)s details : %(details)s")

class AjaxRequestError(SnackException):
    message = _("Ajax Request error : %(reason)s")
    
class AuthenticationRequired(SnackException):
    message = _("NotAuthencation")

class LoginError(SnackException):
    pass

def from_response(response, body):
    if body:
        message = "n/a"
        details = "n/a"
        if hasattr(body, 'keys'):
            error = body[body.keys()[0]]
            message = error.get('message', None)
            details = error.get('details', None)
    else:
        message = None
        details = None
    
    if response.status == 401:
        return AuthenticationRequired(code=response.status, message=message, details=details)
        
    return APIRequestError(code=response.status, message=message, details=details)