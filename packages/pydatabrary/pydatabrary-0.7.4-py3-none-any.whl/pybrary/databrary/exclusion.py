from .record import Record
from .types.category import Category
from .types.reason import Reason


class Exclusion(Record):
    EXCLUSION_METRICS = {
        "19": "excluded",
        "20": "name",
        "21": "reason",
        "22": "description"
    }

    def __init__(
            self,
            key,
            id,
            reason=None,
            excluded=None,
            name=None,
            description=None
    ):
        super().__init__(key, id, Category.EXCLUSION, name=name)
        self._reason = reason
        self._excluded = excluded
        self._description = description


    @staticmethod
    def from_dict(exclusion_dict):
        id = exclusion_dict.get('key')
        excluded = exclusion_dict.get('excluded')
        name = exclusion_dict.get('name')
        description = exclusion_dict.get('description')
        reason = Exclusion.get_name(exclusion_dict['reason'])

        return Exclusion(
            key=id,
            id=id,
            reason=reason,
            excluded=excluded,
            name=name,
            description=description
        )

    @staticmethod
    def from_databrary(exclusion_dict):
        id = exclusion_dict.get('id')
        measures = exclusion_dict.get('measures')
        excluded = measures.get('19')
        name = measures.get('20')
        description = measures.get('22')
        reason = Reason.get_name(measures['21'])

        return Exclusion(
            key=id,
            id=id,
            reason=reason,
            excluded=excluded,
            name=name,
            description=description
        )

    def to_dict(self, template=False):
        result = {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
        }

        if template or self.get_reason() is not None:
            result['reason'] = self.get_reason().value

        if template or self.get_excluded() is not None:
            result["excluded"] =  self.get_excluded()

        if template or self.get_description() is not None:
            result["descritption"] = self.get_description()

        return result

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_reason(self):
        return self._reason

    def get_excluded(self):
        return self._excluded

    def get_description(self):
        return self._description
