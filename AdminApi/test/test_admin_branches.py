import allure
import pytest
from hamcrest import equal_to

from AdminApi.models.commands.branch import Branch
from constants.allure_constants import ADMIN_API_TESTS, BRANCHES
from enums.branch import DeliveryOptions
from utils.asserts import check_that
from utils.auth import AdminAuth


@allure.feature(ADMIN_API_TESTS)
@allure.story(BRANCHES)
class TestBranches:
    """This test only validate api response body object types.
    For Example: I expect that I will get AdminBranchRows object and it has described fields and they have
    exactly the same types which I have set in a model description"""

    def test_get_company_branches_positive(self, company, branch_steps):
        company_id = company.id
        auth = AdminAuth(email=company.admin.email, password=company.admin.password)
        branch_steps.get_company_branches_positive(
            company_id=company_id,
            auth=auth)

    """This test validate api response body and check the incoming values"""

    def test_create_company_branch_positive(self, company, branch_steps):
        company_id = company.id
        auth = AdminAuth(email=company.admin.email, password=company.admin.password)
        command = Branch().to_dict()
        branch = branch_steps.create_company_branch_positive(
            company_id=company_id,
            command=command,
            auth=auth).json()
        check_that(branch.get('address'),
                   equal_to(command.address),
                   'new branch address is correct')
        check_that(branch.get('phones'),
                   equal_to(command.phones),
                   'phone is correct')

    def test_delete_company_branch_positive(self, company, branch_steps):
        company_id = company.id
        auth = AdminAuth(email=company.admin.email, password=company.admin.password)
        command = Branch().to_dict()
        branch_id = branch_steps.create_company_branch_positive(
            company_id=company_id,
            command=command,
            auth=auth).json().get('id')
        branch_steps.delete_company_branch_positive(company_id, branch_id)
        branches = branch_steps.get_company_branches_positive(
            company_id=company_id,
            auth=auth)
        check_that(all(branch['id'] != branch_id for branch in branches),
                   equal_to(False),
                   'branch is deleted')

    def test_get_company_branch_by_admin_positive(self, company, branch_steps):
        branch_id = company.branches[0].id
        auth = AdminAuth(email=company.admin.email, password=company.admin.password)
        branch_steps.get_company_branch_by_id_positive(
            company_id=company.id,
            branch_id=branch_id,
            auth=auth)

    @pytest.mark.ignore_on("prod")
    def test_update_company_branch_positive(self, company, branch_steps):
        branch_id = company.branches[0].id
        auth = AdminAuth(email=company.admin.email, password=company.admin.password)
        command = Branch(
            address='new_address',
            deliveryOptions=DeliveryOptions.DELIVERY.value
        ).to_dict()
        branch = branch_steps.update_company_branch_positive(
            company_id=company.id,
            branch_id=branch_id,
            command=command,
            auth=auth).json()
        check_that(branch.get('address'),
                   equal_to(command.address),
                   'address has been updated')
        check_that(branch.get('deliveryOptions'),
                   equal_to(command.deliveryOptions),
                   'deliveryOptions has been updated')
