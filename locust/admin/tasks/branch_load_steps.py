import random

from locust import task, User
from locust.base_locust import BaseTaskSet

from AdminApi.fixtures.admin_api_fixture import branch_steps_method
from AdminApi.models.commands.branch import Branch
from AdminApi.models.commands.company import Company, Admin
from definitions import CUSTOMER_CREDENTIALS
from utils.auth import AdminAuth

# create mock object
branch = Branch(id=random.randint(10000, 999999))
company = Company(
    id=random.randint(10000, 999999),
    name='Test Company',
    tariff='Enterprise',
    admin=Admin(email='example@mail.ru', password='password'),
    branches=[branch]),

"""Create load test task set which will be called by user session"""


class LocustCustomerStepsTask(BaseTaskSet):
    def __init__(self, parent: "User", path=CUSTOMER_CREDENTIALS):
        super().__init__(parent, path)

    @task(1)
    def get_branches(self):
        company_id = self.company.id
        auth = AdminAuth(email=self.company.admin.email,
                         password=self.company.admin.password)
        branch_steps_method().get_company_branches_positive(
            company_id=company_id,
            auth=auth)
