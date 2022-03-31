
from renovation import RenovationModel
from .pms_customer_types import PMSCustomerMeta


class PMSCustomer(RenovationModel["PMSCustomer"], PMSCustomerMeta):
    pass
