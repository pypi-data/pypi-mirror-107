from requests import HTTPError


class CLIError:
    def __init__(self, errors, return_code=1):
        self.errors = errors
        self.return_code = return_code


class ErrorHandler:
    def __init__(self, app):
        self.app = app

    def handle(self, exception):
        if self.app.debug_mode:
            raise exception
        try:
            if isinstance(exception, HTTPError):
                result = self._on_http_error(exception)
                if result:
                    return result
            return self.get_unexpected_error()
        except Exception:
            return self.get_unexpected_error()

    def _on_http_error(self, exception):
        response = exception.response
        status_code = response.status_code
        handler = getattr(self, '_on_{}'.format(status_code), None)
        if callable(handler):
            return handler(response)

    def _on_400(self, response):
        error_msg = response.json()
        if 'namespace_header' in error_msg:
            selected_ns = response.request.headers.get("Digicloud-Namespace")
            if selected_ns is None:
                return CLIError(
                    [dict(
                        msg="You didn't select a namespace",
                        hint="You can select a namespace by using "
                             "`digicloud namespace select` command"
                    )]
                )
            else:
                return CLIError(
                    [
                        dict(
                            msg="You've chosen an invalid namespace, "
                                "either you removed the current namespace, "
                                "left from it or "
                                "someone removed you.\n",
                            hint="You need to select one of your namespaces using "
                                 "'digicloud namespace select'.\n"
                                 "Also you can see list of your namespaces using "
                                 "'digicloud namespace list'"
                        )
                    ]
                )
        elif 'region_header' in error_msg:
            return CLIError([dict(
                msg="You need to select a region for this command",
                hint="You need to select a region appropriately, "
                     "by using 'digicloud region select' and "
                     "'digicloud region list'"
            )])
        elif 'errors' in error_msg:
            errors = error_msg['errors']
            if isinstance(errors, dict):
                return CLIError(
                    [
                        dict(
                            msg="You need to provide an appropriate value for "
                                "[bold red]{}[/bold red] attribute".format(field_name),
                            hint=error_msg
                        ) for field_name, error_msg in errors.items()
                    ]
                )
            elif isinstance(errors, str):
                return CLIError([dict(msg=errors)])
            else:
                return CLIError([dict(msg=str(errors))])  # TODO: <-- Fix this

    def _on_401(self, response):
        return CLIError(
            [dict(
                msg="You're not authorized to perform this operation",
                hint="You can login to you account via `digicloud account login`"
                     "or go to https://digicloud.ir for registration"
            )]
        )

    def _on_404(self, response):
        msg = "Unable to find the object"
        response_payload = response.json()
        if 'errors' in response_payload:
            msg = response_payload['errors']
        return CLIError(
            [dict(
                msg=msg,
                hint="It might be a typo in your object name or ID"
            )]
        )

    def get_unexpected_error(self):
        return CLIError(
            [
                dict(
                    msg="An unexpected error happened while running your command.",
                    hint="Please run your command with --debug and send the output "
                         "to us via support@digicloud.ir"
                )
            ]
        )
