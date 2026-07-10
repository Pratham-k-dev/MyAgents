class BaseModelProvider:

    def generate(
        self,
        messages,
        response_schema,
        tools=None,
        **kwargs
    ):
        raise NotImplementedError