import datetime
from datetime import timezone
from json import JSONEncoder

class Record:
    

    def __init__(self, title, author, createdAt, text="", total_count=0, tags=[]):
        self.title = title
        self.author = author
        self.text = text
        self.createdAt = createdAt
        self.total_count = total_count
        self.tags = tags


    @property
    def createdAt(self):
        return self._createdAt

    @createdAt.setter
    def createdAt(self, value):
        str_format="%Y-%m-%dT%H:%M:%S%z"
        try: 
            self._createdAt = datetime.datetime.strptime(value, str_format).astimezone(tz=timezone.utc).strftime(str_format)
        except ValueError as e:
            raise RecordException("createdAt attribute must be a valid ISO datetime string", e)

    
    @property
    def total_count(self):
        return self._total_count

    @total_count.setter
    def total_count(self, value):
        if not isinstance(value, (str, int, float)):
            raise RecordException("total_count attribute must be a str, int, or float")
        
        try:
            self._total_count = int(value)
        except ValueError as e:
            raise RecordException("total_count attribute must cast to int", e) 


    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = [split_tag for tag in value for split_tag in tag.split(' ')]


    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        
        if value and value != "N/A":
            self._author = value
        else:
            raise RecordException("author attribute cannot be empty/null")


class RecordException(Exception):
    pass


class RecordFactory:

    def from_dictionary(json_dict):
        if 'title_text' in json_dict:
            json_dict['title'] = json_dict.pop('title_text')

        try:
            return Record(**json_dict)
        except TypeError as e:
            raise RecordException("missing required attributes", e)
    

class RecordEncoder(JSONEncoder):
    
        def default(self, o):
            # custom encoder inspired by https://stackoverflow.com/a/31813203
            return {k.lstrip('_'): v for k, v in vars(o).items()}
