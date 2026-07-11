def __tool_call__(tool_name, **kwargs):
    raise NotImplementedError("Dispatcher not implemented yet.")

def weather(city):
    return __tool_call__(
        "weather",
        city=city
    )