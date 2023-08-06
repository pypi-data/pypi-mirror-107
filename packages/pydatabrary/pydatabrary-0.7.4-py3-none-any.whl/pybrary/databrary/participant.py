from .record import Record
from .types.category import Category
from .types.gender import Gender
from .types.ethnicity import Ethnicity
from .types.race import Race


class Participant(Record):
    PARTICIPANT_METRICS = {
        "1": "ID",
        "2": "info",
        "3": "description",
        "4": "birthdate",
        "5": "gender",
        "6": "race",
        "7": "ethnicity",
        "8": "gestational age",
        "9": "pregnancy term",
        "10": "birth weight",
        "11": "disability",
        "12": "language",
        "13": "country",
        "14": "state",
        "15": "setting"
    }

    def __init__(
        self,
        key,
        id,
        participant_id=None,
        race=Race.UNKNOWN_OR_NOT_REPORTED,
        ethnicity=None,
        gender=None,
        birthdate=None,
        disability=None,
        language=None,
        gestational_age=None,
        birth_weight=None,
    ):
        super().__init__(key, id, Category.PARTICIPANT)
        self._participant_id = participant_id
        self._race = race
        self._ethnicity = ethnicity
        self._gender = gender
        self._birthdate = birthdate
        self._disability = disability
        self._language = language
        self._gestational_age = gestational_age
        self._birth_weight = birth_weight

    @staticmethod
    def from_dict(participant_dict):
        id = participant_dict.get('key')
        participant_id = participant_dict.get('participant_id')
        race = Race.get_name(participant_dict.get('race'))
        ethnicity = Ethnicity.get_name(participant_dict.get('ethnicity'))
        gender = Gender.get_name(participant_dict.get('gender'))
        birthdate = participant_dict.get('birthdate')
        disability = participant_dict.get('disability')
        language = participant_dict.get('language')
        gestational_age = participant_dict.get('gestational_age')
        birth_weight = participant_dict.get('birth_weight')

        return Participant(
            key=id,
            id=id,
            participant_id=participant_id,
            race=race,
            ethnicity=ethnicity,
            gender=gender,
            birthdate=birthdate,
            disability=disability,
            language=language,
            gestational_age=gestational_age,
            birth_weight=birth_weight
        )

    @staticmethod
    def from_databrary(participant_dict):
        # TODO: Get measures from the hash map
        id = participant_dict.get('id')
        measures = participant_dict['measures']
        race = Race.get_name(measures.get('6'))
        participant_id = int(measures.get('1'))
        ethnicity = Ethnicity.get_name(measures.get('7'))
        gender = Gender.get_name(measures.get('5'))
        birthdate = measures.get('4')
        disability = measures.get('11')
        language = measures.get('12')
        gestational_age = measures.get('8')
        birth_weight = measures.get('10')

        return Participant(
            key=id,
            id=id,
            participant_id=participant_id,
            race=race,
            ethnicity=ethnicity,
            gender=gender,
            birthdate=birthdate,
            disability=disability,
            language=language,
            gestational_age=gestational_age,
            birth_weight=birth_weight
        )

    def to_dict(self, template=False):
        result = {
            "key": "{}".format(self.get_key()),
            "ID": "{}".format(self.get_participant_id() if self.get_participant_id() is not None else self.get_id()),
            "category": self.get_category().value,
        }

        if template or self.get_birthdate() is not None:
            result['birthdate'] = self.get_birthdate()
        if template or self.get_disability() is not None:
            result['disability'] = self.get_disability()
        if template or self.get_gender() is not None:
            result['gender'] = self.get_gender().value
        if template or self.get_race() is not None:
            result['race'] = self.get_race().value

        return result

    def to_json(self, indent=4):
        return json.dumps(self.to_dict(), indent=indent)

    def get_race(self):
        return self._race

    def get_ethnicity(self):
        return self._ethnicity

    def get_gender(self):
        return self._gender

    def get_birthdate(self):
        return self._birthdate

    def get_disability(self):
        return self._disability

    def get_language(self):
        return self._language

    def get_participant_id(self):
        return self._participant_id

    def get_gestational_age(self):
        return self._gestational_age

    def get_birth_weight(self):
        return self._birth_weight
