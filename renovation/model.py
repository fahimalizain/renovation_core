from typing import Union, List, Optional, TypeVar, Generic

import frappe
from frappe.model.document import Document

T = TypeVar("T")

doctype_map = {}


def map_doctype(doctype: str, renovation_class: type):
    global doctype_map
    doctype_map[renovation_class] = doctype


class FrappeModel(Generic[T], Document):

    @classmethod
    def get_doctype(cls):
        global doctype_map
        return doctype_map[cls]

    @classmethod
    def get_doc(cls, doc_id: str) -> Optional[T]:
        if cls.exists(doc_id):
            return frappe.get_doc(cls.get_doctype(), doc_id)
        return None

    @classmethod
    def get_all(cls,
                filters: dict,
                fields: List[str],
                offset: int = 0,
                count: int = 10) -> List[T]:
        return frappe.get_all(cls.get_doctype(), filters=filters, fields=fields, limit_start=offset,
                              limit_page_length=count)

    @classmethod
    def query(cls,
              query: str,
              values: Union[dict, tuple, list],
              as_dict: bool = True) -> Union[dict, list]:
        return frappe.db.sql(query, values, as_dict=as_dict)

    @classmethod
    def get_count(cls, filters: dict) -> int:
        return frappe.db.count(cls.get_doctype(), filters=filters)

    @classmethod
    def exists(cls, doc_id: str):
        return frappe.db.exists(cls.get_doctype(), doc_id)

    def insert(self) -> T:
        return super().insert()

    def update(self, d) -> T:
        super().update(d)
        return self

    def delete(self) -> None:
        super().delete()
        return None
