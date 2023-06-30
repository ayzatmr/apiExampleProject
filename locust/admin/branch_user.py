from locust import run_single_user

from locust.base_locust import BaseHttpUser

from locust.admin.tasks.locust_customer_steps import LocustCustomerStepsTask


class BranchUser(BaseHttpUser):
    tasks = [LocustCustomerStepsTask]


# only for debug
if __name__ == "__main__":
    run_single_user(BranchUser)
