# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import assisted_service_client
from assisted_service_client.api.installer_api import InstallerApi  # noqa: E501
from assisted_service_client.rest import ApiException


class TestInstallerApi(unittest.TestCase):
    """InstallerApi unit test stubs"""

    def setUp(self):
        self.api = assisted_service_client.api.installer_api.InstallerApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_cancel_installation(self):
        """Test case for cancel_installation

        """
        pass

    def test_complete_installation(self):
        """Test case for complete_installation

        """
        pass

    def test_deregister_cluster(self):
        """Test case for deregister_cluster

        """
        pass

    def test_deregister_host(self):
        """Test case for deregister_host

        """
        pass

    def test_disable_host(self):
        """Test case for disable_host

        """
        pass

    def test_download_cluster_files(self):
        """Test case for download_cluster_files

        """
        pass

    def test_download_cluster_iso(self):
        """Test case for download_cluster_iso

        """
        pass

    def test_download_cluster_iso_clone(self):
        """Test case for download_cluster_iso_clone

        """
        pass

    def test_download_cluster_iso_headers(self):
        """Test case for download_cluster_iso_headers

        """
        pass

    def test_download_cluster_iso_headers_clone(self):
        """Test case for download_cluster_iso_headers_clone

        """
        pass

    def test_download_cluster_kubeconfig(self):
        """Test case for download_cluster_kubeconfig

        """
        pass

    def test_download_cluster_logs(self):
        """Test case for download_cluster_logs

        """
        pass

    def test_download_host_ignition(self):
        """Test case for download_host_ignition

        """
        pass

    def test_download_host_logs(self):
        """Test case for download_host_logs

        """
        pass

    def test_enable_host(self):
        """Test case for enable_host

        """
        pass

    def test_generate_cluster_iso(self):
        """Test case for generate_cluster_iso

        """
        pass

    def test_get_cluster(self):
        """Test case for get_cluster

        """
        pass

    def test_get_cluster_default_config(self):
        """Test case for get_cluster_default_config

        """
        pass

    def test_get_cluster_host_requirements(self):
        """Test case for get_cluster_host_requirements

        """
        pass

    def test_get_cluster_install_config(self):
        """Test case for get_cluster_install_config

        """
        pass

    def test_get_credentials(self):
        """Test case for get_credentials

        """
        pass

    def test_get_discovery_ignition(self):
        """Test case for get_discovery_ignition

        """
        pass

    def test_get_free_addresses(self):
        """Test case for get_free_addresses

        """
        pass

    def test_get_host(self):
        """Test case for get_host

        """
        pass

    def test_get_host_ignition(self):
        """Test case for get_host_ignition

        """
        pass

    def test_get_host_requirements(self):
        """Test case for get_host_requirements

        """
        pass

    def test_get_next_steps(self):
        """Test case for get_next_steps

        """
        pass

    def test_get_preflight_requirements(self):
        """Test case for get_preflight_requirements

        """
        pass

    def test_get_presigned_for_cluster_files(self):
        """Test case for get_presigned_for_cluster_files

        """
        pass

    def test_install_cluster(self):
        """Test case for install_cluster

        """
        pass

    def test_install_host(self):
        """Test case for install_host

        """
        pass

    def test_install_hosts(self):
        """Test case for install_hosts

        """
        pass

    def test_list_clusters(self):
        """Test case for list_clusters

        """
        pass

    def test_list_hosts(self):
        """Test case for list_hosts

        """
        pass

    def test_list_of_cluster_operators(self):
        """Test case for list_of_cluster_operators

        """
        pass

    def test_post_step_reply(self):
        """Test case for post_step_reply

        """
        pass

    def test_register_add_hosts_cluster(self):
        """Test case for register_add_hosts_cluster

        """
        pass

    def test_register_cluster(self):
        """Test case for register_cluster

        """
        pass

    def test_register_host(self):
        """Test case for register_host

        """
        pass

    def test_report_monitored_operator_status(self):
        """Test case for report_monitored_operator_status

        """
        pass

    def test_reset_cluster(self):
        """Test case for reset_cluster

        """
        pass

    def test_reset_host(self):
        """Test case for reset_host

        """
        pass

    def test_reset_host_validation(self):
        """Test case for reset_host_validation

        Reset failed host validation.  # noqa: E501
        """
        pass

    def test_update_cluster(self):
        """Test case for update_cluster

        """
        pass

    def test_update_cluster_install_config(self):
        """Test case for update_cluster_install_config

        """
        pass

    def test_update_cluster_logs_progress(self):
        """Test case for update_cluster_logs_progress

        """
        pass

    def test_update_discovery_ignition(self):
        """Test case for update_discovery_ignition

        """
        pass

    def test_update_host_ignition(self):
        """Test case for update_host_ignition

        """
        pass

    def test_update_host_install_progress(self):
        """Test case for update_host_install_progress

        """
        pass

    def test_update_host_installer_args(self):
        """Test case for update_host_installer_args

        """
        pass

    def test_update_host_logs_progress(self):
        """Test case for update_host_logs_progress

        """
        pass

    def test_upload_cluster_ingress_cert(self):
        """Test case for upload_cluster_ingress_cert

        """
        pass

    def test_upload_host_logs(self):
        """Test case for upload_host_logs

        """
        pass

    def test_upload_logs(self):
        """Test case for upload_logs

        """
        pass


if __name__ == '__main__':
    unittest.main()
