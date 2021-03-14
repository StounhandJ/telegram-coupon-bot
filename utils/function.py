async def set_state_active(state):
    async with state.proxy() as data:
        data["state_active"] = await state.get_state()


def string_handler(text: str):
    return text.replace("&", "&amp;").replace("<","&lt;").replace(">","&gt;")


def checkID(mes):
    elements = mes.split(' ')
    for element in elements:
        if element.isdigit():
            return int(element)
    return -1
