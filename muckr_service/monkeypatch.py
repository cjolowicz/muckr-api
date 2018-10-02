import flask_restless

if flask_restless.__version__ == '0.17.0':
    # flask_restless swallows its own only use of ValidationError, replacing the
    # error message "Model does not have field '{0}'" with "Could not determine
    # specific validation errors".

    import flask_restless.views

    def _extract_validation_error_message(exception):
        try:
            left, _ = str(exception).rsplit("'", 1)
            _, fieldname = left.rsplit("'", 1)
            return {fieldname: str(exception)}
        except ValueError:
            return None

    def extract_error_messages(exception):
        rv = _extract_error_messages(exception)
        if rv is None and isinstance(exception, flask_restless.views.ValidationError):
            return _extract_validation_error_message(exception)
        return rv

    _extract_error_messages, flask_restless.views.extract_error_messages = \
        flask_restless.views.extract_error_messages, extract_error_messages
