import json

from pydantic import BaseModel
from typing import List


class People(BaseModel):
    job: str
    company: str
    ssn: str
    residence: str
    current_location: List = []
    blood_group: str
    website: List = []
    username: str
    name: str
    sex: str
    address: str
    mail: str
    birthdate: str

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return People(**json_dict)

    def __repr__(self):
        return f'<People {self.username}>'
