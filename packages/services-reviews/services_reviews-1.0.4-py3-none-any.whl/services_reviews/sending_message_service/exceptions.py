class SendingMessageException(Exception):
    pass


class UnknownTemplateVariableException(SendingMessageException):
    pass
