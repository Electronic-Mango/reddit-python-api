from werkzeug.routing import BaseConverter

from reddit.wrapper import SortType


class SortTypeConverter(BaseConverter):
    def to_python(self, value: str) -> SortType:
        return SortType[value.lower()]

    def to_url(slef, value: SortType) -> str:
        return value.value
