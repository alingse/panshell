# coding=utf-8


class FS(object):
    """filesystem Base Class"""

    prompt_fmt = '{}-sh$>'

    def __init__(self, name, **kwargs):
        self.name = name

        prompt = kwargs.pop('prompt', None)
        if prompt is None:
            prompt = self.prompt_fmt.format(name)

        self.prompt = prompt
