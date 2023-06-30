from AdminApi.models.branch import AdminBranchRows, AdminBranch
from base import BaseSteps, validate_response
from constants.request_constants import BRANCHES, COMPANIES
from enums.statuses import HttpStatus
from utils.helper import join_url_paths

""" Steps are the api requests to some backend.
After getting response validate_response will check 
response status and validate the expected data types"""


class BranchSteps(BaseSteps):
    @validate_response(HttpStatus.Ok, AdminBranchRows)
    def get_company_branches_positive(self, company_id, auth, max=50):
        response = self._client._get(
            url=join_url_paths(COMPANIES, company_id, BRANCHES),
            params={'max': max},
            auth=auth)
        return response

    @validate_response(HttpStatus.Ok, AdminBranch)
    def create_company_branch_positive(self, company_id, command, auth):
        response = self._client._post(
            url=join_url_paths(COMPANIES, company_id, BRANCHES),
            json=command,
            auth=auth)
        return response

    @validate_response(HttpStatus.Validation_Error)
    def create_company_branch_validation_error(self, company_id, command, auth):
        response = self._client._post(
            url=join_url_paths(COMPANIES, company_id, BRANCHES),
            json=command,
            auth=auth)
        return response

    @validate_response(HttpStatus.Deleted)
    def delete_company_branch_positive(self, company_id, branch_id, auth):
        response = self._client._delete(
            url=join_url_paths(COMPANIES, company_id, BRANCHES, branch_id),
            auth=auth)
        return response

    @validate_response(HttpStatus.Ok, AdminBranch)
    def get_company_branch_by_id_positive(self, company_id, branch_id, auth):
        response = self._client._get(
            url=join_url_paths(COMPANIES, company_id, BRANCHES, branch_id),
            auth=auth)
        return response

    @validate_response(HttpStatus.Ok, AdminBranch)
    def update_company_branch_positive(self, company_id, branch_id, command, auth):
        response = self._client._put(
            url=join_url_paths(COMPANIES, company_id, BRANCHES, branch_id),
            json=command,
            auth=auth)
        return response

    @validate_response(HttpStatus.Validation_Error)
    def update_company_branch_validation_error(self, company_id, branch_id, command, auth):
        response = self._client._put(
            url=join_url_paths(COMPANIES, company_id, BRANCHES, branch_id),
            json=command,
            auth=auth)
        return response
