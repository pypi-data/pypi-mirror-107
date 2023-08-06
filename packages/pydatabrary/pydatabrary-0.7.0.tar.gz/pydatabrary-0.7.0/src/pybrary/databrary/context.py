from .record import Record

from .types.category import Category
from .types.setting import Setting


class Context(Record):
    CONTEXT_METRICS = {
        "32": "name",
        "33": "setting",
        "34": "language",
        "35": "country",
        "36": "state"
    }

    # TODO: Add State and country types
    def __init__(
            self,
            key,
            id,
            name=None,
            language=None,
            setting=None,
            country=None,
            state=None
    ):
        super().__init__(key, id, Category.CONTEXT, name=name)
        self._country = country
        self._state = state
        self._setting = setting
        self._language = language

    @staticmethod
    def from_dict(context_dict):
        id = context_dict.get('key')
        setting = Setting.get_name(context_dict['setting'])
        country = context_dict['country']
        state = context_dict['state']
        name = context_dict['name']
        language = context_dict['language']

        return Context(
            key=id,
            id=id,
            name=name,
            language=language,
            setting=setting,
            country=country,
            state=state
        )

    @staticmethod
    def from_databrary(context_dict):
        id = context_dict.get('id')
        measures = context_dict.get('measures')
        setting = Setting.get_name(measures.get('33'))
        country = measures.get('35')
        state = measures.get('36')
        name = measures.get('32')
        language = measures.get('34')

        return Context(
            key=id,
            id=id,
            name=name,
            language=language,
            setting=setting,
            country=country,
            state=state
        )

    def to_dict(self, template=False):
        result = {
            "key": "{}".format(self.get_key()),
            "ID": "{}".format(self.get_id()),
            "name": self.get_name(),
            "category": self.get_category().value,
        }

        if template or self.get_language() is not None:
            result["language"] =  self.get_language()

        if template or self.get_setting() is not None:
            result["setting"] = self.get_setting().value

        if template or self.get_state() is not None:
            result["state"] =  self.get_state()

        if template or self.get_country() is not None:
            result["country"] = self.get_country()

        return result

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_language(self):
        return self._language

    def get_setting(self):
        return self._setting

    def get_state(self):
        return self._state

    def get_country(self):
        return self._country
