import datetime

class Record:
    ## Record-level requiremetns:
    # 1. no title nor title_text field == toast
    # 4. invalid datetime (ISO stantard)
    # 6. no author field / empty null N/A author field
    # 7. cannot cast total_count to int OR type not in int, float, str. BUT if total_count not present it's fine
    # 

    def __init__(self, title, author, createdAt, text="", total_count=0, tags=[]):
        self.title = title
        self.author = author
        self.text = text
        self.createdAt = createdAt
        self.total_count = total_count
        self.tags = tags


    @property
    def createdAt(self, value):
        # str_format="%Y-%m-%dT%H:%M:%S"
        try: 
            self._createdAt = datetime.datetime.fromisoformat(value).isoformat() 
        except ValueError as e:
            raise RecordException("createdAt attribute must be a valid ISO datetime string", e)

    
    @property
    def total_count(self, value):
        if not isinstance(value, (str, int, float)):
            raise RecordException("total_count attribute must be a str, int, or float")
        
        try:
            self._total_count = int(value)
        except ValueError as e:
            raise RecordException("total_count attribute must cast to int", e) 


    @property
    def tags(self, value):
        self._tags = [split_tag for tag in value for split_tag in tag.split(' ')]


    @property
    def author(self, value):
    
        if value:
            self._author = value
        else:
            raise RecordException("author attribute cannot be empty/null")



class RecordException(Exception):
    pass


class RecordFactory:

    def from_dictionary(json_dict):
        return Record(**json_dict)
    
