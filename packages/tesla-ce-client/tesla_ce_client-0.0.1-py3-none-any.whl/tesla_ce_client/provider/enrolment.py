#  Copyright (c) 2020 Xavier Baró
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
""" TeSLA CE Enrolment Client module """
import io
import simplejson
import requests
from enum import Enum
from tesla_ce_client import exception


class SampleValidationStatus(Enum):
    """ SampleValidationStatus definition """
    VALIDATING = 0
    VALID = 1
    ERROR = 2
    TIMEOUT = 3
    WAITING_EXTERNAL_SERVICE = 4


class Enrolment:
    """
        Enrolment Client class
    """

    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        # Connector object -> Connector
        self._connector = connector

    def get_model_lock(self, provider_id, learner_id, task_id):
        """
            Get learner model for a provider ready to be modified.

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param task_id: Task UUID value. It will allow to update the model.
            :type task_id: str
            :return: Learner model
            :rtype: dict
        """
        try:
            return self._connector.post('/api/v2/provider/{}/enrolment/'.format(provider_id),
                                        body={
                                            'learner_id': learner_id,
                                            'task_id': task_id
                                        })
        except exception.BadRequestException as exc:
            if 'Model is locked' in exc.value:
                raise exception.LockedResourceException("Model is locked")

    def get_model(self, provider_id, learner_id):
        """
            Get learner model for a provider.

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :return: Learner model
            :rtype: dict
        """
        return self._connector.get('/api/v2/provider/{}/enrolment/{}/'.format(provider_id, learner_id))

    def unlock_model(self, provider_id, learner_id, task_id):
        """
            Unlock the learner model for a provider.

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param task_id: Task UUID value. It will allow to update the model.
            :type task_id: str
        """
        self._connector.post('/api/v2/provider/{}/enrolment/{}/unlock/'.format(provider_id, learner_id),
                             body={
                                 'token': task_id
                             })

    def save_model(self, provider_id, learner_id, task_id, model):
        """
            Get learner model for a provider ready to be modified.

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param task_id: Task UUID value. It will allow to update the model.
            :type task_id: str
            :return: Learner model
            :rtype: dict
        """
        try:
            # Upload the new model to storage
            if not self._connector._verify_ssl:
                resp = requests.post(model['model_upload_url']['url'], data=model['model_upload_url']['fields'],
                                     files={'file': io.StringIO(simplejson.dumps(model['model']))}, verify=False)
            else:
                resp = requests.post(model['model_upload_url']['url'], data=model['model_upload_url']['fields'],
                                     files={'file': io.StringIO(simplejson.dumps(model['model']))})

            # Check given response
            self._connector._check_response_status(resp.status_code, resp.content)

            return self._connector.put('/api/v2/provider/{}/enrolment/{}/'.format(provider_id, learner_id),
                                        body={
                                            'learner_id': learner_id,
                                            'task_id': task_id,
                                            'percentage': model['percentage'],
                                            'can_analyse': model['can_analyse'],
                                            'used_samples': model['used_samples']
                                        })
        except exception.BadRequestException as exc:
            if 'Model is locked' in exc.value:
                raise exception.LockedResourceException("Model is locked")

    def get_sample(self, provider_id, learner_id, sample_id):
        """
            Get enrolment sample

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param sample_id: Sample id
            :type sample_id: int
            :return: Enrolment sample
            :rtype: dict
        """
        return self._connector.get('/api/v2/provider/{}/enrolment/{}/sample/{}/'.format(provider_id,
                                                                                        learner_id,
                                                                                        sample_id))

    def get_sample_validation(self, provider_id, learner_id, sample_id, validation_id):
        """
            Get validation result for an enrolment sample

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param sample_id: Sample id
            :type sample_id: int
            :param validation_id: Sample validation id
            :type validation_id: int
            :param result: Validation result
            :type result: dict
        """
        return self._connector.get('/api/v2/provider/{}/enrolment/{}/sample/{}/validation/{}/'.format(
            provider_id, learner_id, sample_id, validation_id))

    def set_sample_validation(self, provider_id, learner_id, sample_id, validation_id, result):
        """
            Store validation result for an enrolment sample

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param sample_id: Sample id
            :type sample_id: int
            :param validation_id: Sample Validation id
            :type validation_id: int
            :param result: Validation result
            :type result: dict
        """
        return self._connector.put('/api/v2/provider/{}/enrolment/{}/sample/{}/validation/{}/'.format(
            provider_id, learner_id, sample_id, validation_id), body=result)

    def get_sample_validation_list(self, provider_id, learner_id, sample_id):
        """
            Get validation result for an enrolment sample

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param sample_id: Sample id
            :type sample_id: int
            :param result: Validation results
            :type result: dict
        """
        return self._connector.get('/api/v2/provider/{}/enrolment/{}/sample/{}/validation/'.format(
            provider_id, learner_id, sample_id))

    def get_model_samples(self, provider_id, learner_id):
        """
            Get the list of enrolment samples used in current model

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param result: Enrolment samples
            :type result: dict
        """
        return self._connector.get('/api/v2/provider/{}/enrolment/{}/used_samples/'.format(
            provider_id, learner_id))

    def get_available_samples(self, provider_id, learner_id):
        """
            Get the list of available validated enrolment samples that are not used in current model

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param result: Enrolment samples
            :type result: dict
        """
        return self._connector.get('/api/v2/provider/{}/enrolment/{}/available_samples/'.format(
            provider_id, learner_id))

    def set_sample_validation_status(self, provider_id, learner_id, sample_id, validation_id, status):
        """
            Change sample validation status

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param sample_id: Sample id
            :type sample_id: int
            :param validation_id: Validation id
            :type validation_id: int
            :param status: Sample's status. Valid status: 0 validating, 1 valid, 2 error, 3 timeout, 4 waiting external
            service
            :type status: SampleValidationStatus

            :return:
        """
        return self._connector.post('/api/v2/provider/{}/enrolment/{}/sample/{}/validation/{}/status/'.format(
            provider_id, learner_id, sample_id, validation_id), body={"status": status.value})

    def set_sample_status(self, provider_id, learner_id, sample_id, status):
        """
            Change sample status

            :param provider_id: Provider ID
            :type provider_id: int
            :param learner_id: The learner UUID
            :type learner_id: str
            :param sample_id: Sample id
            :type sample_id: int
            :param status: Sample's status. Valid status: 0 validating, 1 valid, 2 error, 3 timeout, 4 waiting external
            service
            :type status: SampleValidationStatus

            :return:
        """
        raise exception.NotImplementedException()
        '''
        This should be the endpoint in the API, but now not exists
        return self._connector.post('/api/v2/provider/{}/enrolment/{}/sample/{}/status/'.format(
            provider_id, learner_id, sample_id), body={"status": status.value})
            '''
