from .record import Record
from .types.category import Category


class Pilot(Record):
    PILOT_METRICS = {
        "16": "pilot",
        "17": "name",
        "18": "description"
    }

    def __init__(self, key, id, name=None, pilot=None, description=None):
        super().__init__(key, id, Category.PILOT, name=name)
        self._pilot = pilot
        self._description = description

    @staticmethod
    def from_dict(pilot_dict):
        id = pilot_dict.get('key')
        name = pilot_dict.get('name')
        pilot = pilot_dict.get('pilot')
        description = pilot_dict.get('description')
        return Pilot(key=id, id=id, name=name, pilot=pilot, description=description)

    @staticmethod
    def from_databrary(pilot_dict):
        id = pilot_dict.get('id')
        measures = pilot_dict.get('measures')
        name = measures.get('17')
        pilot = measures.get('16')
        description = measures.get('18')
        return Pilot(key=id, id=id, name=name, pilot=pilot, description=description)

    def to_dict(self, template=False):
        result = {
            "key": "{}".format(self.get_key()),
            "ID": "{}".format(self.get_id()),
            "name": self.get_name(),
            "category": self.get_category().value,
        }

        if template or self.get_pilot() is not None:
            result["pilot"] =  self.get_pilot()

        if template or self.get_description() is not None:
            result["descritption"] = self.get_description()

        return result

    def to_json(self, indent=4):
        return json.dumps(self.to_dict(), indent=indent)

    def get_pilot(self):
        return self._pilot

    def get_description(self):
        return self._description
