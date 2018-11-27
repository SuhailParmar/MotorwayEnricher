import logging


class FailurePostToAPI(Exception):
    def __init__(self, status_code, content=None):

        if content is not None:
            self.msg = "FPTA:{0}:Content:{1}".format(status_code, content)
        else:
            self.msg = "Failed To Post Converted Tweet To API. HTTPStatus Code:{}".format(
                status_code)

    def __str__(self):
        return "{}".format(self.msg)
