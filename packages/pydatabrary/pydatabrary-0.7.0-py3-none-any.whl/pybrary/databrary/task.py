from .record import Record
from .types.category import Category


class Task(Record):
    TASK_METRICS = {
        "29": "name",
        "30": "description",
        "31": "info"
    }

    def __init__(self, key, id, name=None, info=None, description=None):
        super().__init__(key, id, Category.TASK, name=name)
        self._info = info
        self._description = description

    @staticmethod
    def from_dict(task_dict):
        id = task_dict.get('key')
        name = task_dict.get('name')
        info = task_dict.get('info')
        description = task_dict.get('description')

        return Task(key=id, id=id, name=name, info=info, description=description)

    @staticmethod
    def from_databrary(task_dict):
        id = task_dict.get('id')
        measures = task_dict.get('measures')
        name = measures.get('29')
        info = measures.get('31')
        description = measures.get('30')

        return Task(key=id, id=id, name=name, info=info, description=description)

    def to_dict(self, template=False):
        result = {
            "key": "{}".format(self.get_key()),
            "ID": "{}".format(self.get_id()),
            "name": self.get_name(),
            "category": self.get_category().value,
        }

        if template or self.get_info() is not None:
            result["info"] =  self.get_info()

        if template or self.get_description() is not None:
            result["descritption"] = self.get_description()

        return result

    def to_json(self, indent=4):
        return json.dumps(self.to_dict(), indent=indent)

    def get_info(self):
        return self._info

    def get_description(self):
        return self._description