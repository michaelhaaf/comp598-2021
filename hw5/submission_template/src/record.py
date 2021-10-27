

class Record(object):
    ## Record-level requiremetns:
    # 1. no title nor title_text field == toast
    # 4. invalid datetime (ISO stantard)
    # 5. invalid JSON
    # 6. no author field / empty null N/A author field
    # 7. cannot cast total_count to int OR type not in int, float, str. BUT if total_count not present it's fine
    # 

    def __init__(self, title, author, text, createdAt, total_count, tags):
        self.title = title
        self.author = author
        self.text = text
        self.createdAt = createdAt
        self.total_count = total_count
        self.tags = tags

    def fromJson(self, line):
        return "" 

