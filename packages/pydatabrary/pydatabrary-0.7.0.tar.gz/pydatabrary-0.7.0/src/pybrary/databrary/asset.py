import json
import warnings

from src.pybrary.databrary.types.release import Release
from src.pybrary.utils import utils
from src.pybrary import constants


class Asset:
    def __init__(
            self,
            file_path,
            id,
            name=None,
            position='auto',
            release=Release.PRIVATE,
            clips=None
    ):
        if id is None:
            raise Exception('Asset id is required')

        if file_path is None:
            raise Exception('You must provide a file path to the asset {}.'.format(id))

        self._file_ext = utils.get_file_extension(file_path)
        if not Asset.is_ext_supported(self._file_ext):
            raise Exception('Asset format {} not supported'.format(self._file_ext))

        if not Asset.is_media(self._file_ext) and clips is not None:
            raise Exception('Cannot add clips for {}. Clips are only supported for media types'.format(self._file_ext))

        self._clips = clips
        self._id = id
        self._file_path = file_path
        self._name = utils.get_file_name(file_path) if name is None else name
        self._position = position
        self._release = release

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_release(self):
        return self._release

    def set_release(self, release):
        self._release = release

    @staticmethod
    def from_dict(asset_dict):
        file = asset_dict.get('file')
        id = asset_dict.get('id')
        name = asset_dict.get('name')
        return Asset(id, file_path=file, name=name)

    @staticmethod
    def from_databrary(asset_dict, path_prefix=constants.DEFAULT_SERVER_PREFIX):
        """
        Building an Asset Object from Databrary Asset Dict fetched from the API.
        Important: Pybrary cannot know the file name, so it will build the file path
        from the Asset's name, Make sure that your file names and asset
        names are the same
        if not, please contact you Databrary Administrator
        Example: {
          "id": 12094,
          "format": -800,
          "duration": 1925035,
          "segment": [
            0,
            1925035
          ],
          "name": "InfantOHApS#74",
          "permission": 5,
          "size": 659371898
        }
        :param asset_dict:
        :param path_prefix:
        :return:
        """
        id = asset_dict.get('id')

        file_name = asset_dict.get('name')
        format_id = str(asset_dict.get('format'))
        file_ext = utils.get_databrary_ext_from_format(format_id)

        if not file_name:
            raise Exception("Asset {} does not contain a file name".format(id))

        if utils.get_file_extension(file_name) is not None:
            file_path = "{}.{}".format(file_name, file_ext)

        if file_ext is None:
            raise Exception('Format {} of Asset id {} is not supported by Databrary'.format(format_id, id))

        file_path = "{}{}".format(path_prefix, file_path)
        return Asset(file_path=file_path, id=id, name=file_name)

    def to_dict(self, template=False):
        result = {
            "release": self._release.value,
            "position": self._position,
            "name": self._name,
            "file": self._file_path
        }

        if template and self._clips is None:
            result['clip'] = []
        if not template and self._clips is not None:
            result['clip'] = self._clips

        return result

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def is_media(file_ext):
        if file_ext in constants.VIDEO_EXTENSIONS \
                or file_ext in constants.AUDIO_EXTENSIONS:
            return True
        else:
            return False

    @staticmethod
    def is_ext_supported(file_ext):
        if file_ext is None:
            raise Exception('File extension is missing, please provide a file name with a valid extension')

        if file_ext in constants.SUPPORTED_FORMATS.values():
            return True

        return False
