from dbod_helpers import DbodCollectdHelper, \
    DbodConfigException
from mock import MagicMock, call
from pytest import raises
import pytest
import apacheconfig
import requests
import json
import dbod_helpers
import dbod_instances


@pytest.fixture
def helper_mocks(mocker, httpserver):
    """
    Mock all external libraries calls
    """
    mocker.patch('apacheconfig.make_loader')
    loader_mock = MagicMock()
    apacheconfig.make_loader.return_value.__enter__.return_value = loader_mock
    loader_mock.load.return_value = {"api": {
        "cachefile": "/some/cache/file.json",
        "host": httpserver.url,
        "host_metadata_endpoint": "test/host",
        "entity_endpoint": "v1/instance",
        "user": "dbod_api",
        "password": "pass-api"
        }}
    mocker.patch('dbod_helpers.gethostname', create=True)

    dbod_helpers.gethostname.return_value = "dbod-test1.cern.ch"
    # Mock requests
    mocker.patch("requests.get")
    requests.get.return_value.status_code = 200
    # Mock instance
    mocker.patch('dbod_instances.DbodInstance.__init__')
    mocker.patch('dbod_instances.MySQLDbodInstance.__init__')
    mocker.patch('dbod_instances.PostgresDbodInstance.__init__')
    mocker.patch('dbod_instances.InfluxDbodInstance.__init__')
    mocker.patch('dbod_instances.MalformedDbodInstance.__init__')
    dbod_instances.MySQLDbodInstance.__init__.return_value = None
    dbod_instances.PostgresDbodInstance.__init__.return_value = None
    dbod_instances.InfluxDbodInstance.__init__.return_value = None
    dbod_instances.MalformedDbodInstance.__init__.return_value = None
    dbod_instances.DbodInstance.__init__.return_value = None
    config = mocker.patch("dbod_helpers.ConfigParser")
    config.return_value.get.return_value = "uu"

    return {"loader_mock": loader_mock,
            "httpserver": httpserver,
            "requests": requests}


def test_dbod_helper_reads_config(mocker, tmpdir, helper_mocks):
    """
    Test a method to get the "source of truth"
    May it be JSON from the disk or API call
    """
    # Test configuration was read
    h = DbodCollectdHelper()
    apacheconfig.make_loader.return_value.__enter__. \
        return_value.load.assert_called_with("/etc/dbod/core.conf")
    assert h.config == apacheconfig.make_loader.return_value.__enter__. \
        return_value.load.return_value
    assert h.cachefile == "/some/cache/file.json"
    assert h.api_url == helper_mocks["httpserver"].url
    assert h.api_user == "dbod_api"
    assert h.api_password == "pass-api"


def test_dbod_helper_reads_config_malformed(mocker, tmpdir, helper_mocks):
    """
    Test a method to get the "source of truth"
    May it be JSON from the disk or API call
    """
    # Test configuration was read
    helper_mocks["loader_mock"].load.return_value = {"t": {}}
    with raises(DbodConfigException) as exc:
        DbodCollectdHelper()
    assert str(exc.value) == "Error in DBOD config file " \
        "(/etc/dbod/core.conf): missing key 'api'"
    ##########################################################
    helper_mocks["loader_mock"].load.return_value = {"api": {}}
    with raises(DbodConfigException) as exc:
        DbodCollectdHelper()
    assert str(exc.value) == "Error in DBOD config file " \
        "(/etc/dbod/core.conf): missing key 'cachefile'"

    ##########################################################
    helper_mocks["loader_mock"].load.return_value = {"api": {
        "cachefile": "/some/cache/file.json",
        "host": "127.0.0.0"
        }}
    with raises(DbodConfigException) as exc:
        DbodCollectdHelper()
    assert str(exc.value) == "Error in DBOD config file " \
        "(/etc/dbod/core.conf): missing key 'host_metadata_endpoint'"
    ##########################################################
    helper_mocks["loader_mock"].load.return_value = {"api": {
        "cachefile": "/some/cache/file.json",
        "host": "127.0.0.0",
        "host_metadata_endpoint": "/end/point"
        }}
    with raises(DbodConfigException) as exc:
        DbodCollectdHelper()
    assert str(exc.value) == "Error in DBOD config file " \
        "(/etc/dbod/core.conf): missing key 'entity_endpoint'"
    ##########################################################
    helper_mocks["loader_mock"].load.side_effect = \
        apacheconfig.error.ConfigFileReadError("sth wrong")
    with raises(DbodConfigException) as exc:
        DbodCollectdHelper()
    assert str(exc.value) == "sth wrong"


def test_get_instances_from_get(mocker, tmpdir, helper_mocks):
    """
    Test get_instances calls api to get a list of instances
        if it fails, it reads entities.json
        Then it creates a list of DbodInstance object
        which is returned
    """
    # Everything ok - status code 200
    mocker.patch('dbod_helpers.open')
    requests.get.return_value.json.return_value = \
        {"response": [
            {"instance": "1", "db_type": "MYSQL", "state": "RUNNING"},
            {"instance": "2", "db_type": "InfluxDB", "state": "RUNNING"},
            {"instance": "3", "db_type": "MYSQL", "state": "RUNNING"},
            {"instance": "4", "db_type": "PG", "state": "RUNNING"}
        ]}
    h = DbodCollectdHelper()
    h.user = "user"
    h.password = "pass"
    assert h.host_metadata_endpoint == "test/host"
    instances = h.get_instances()
    dbod_helpers.gethostname.assert_called()
    requests.get.assert_called_with("%s/test/host/dbod-test1"
                                    % h.api_url)
    requests.get.return_value.json.assert_called()
    dbod_helpers.open.assert_not_called()
    # ############ MYSQL INSTANCES #####################
    assert dbod_instances.MySQLDbodInstance.__init__. \
        mock_calls \
        == [call({"instance": "1", "db_type": "MYSQL", "state": "RUNNING"},
                 user="user", password="pass"),
            call({"instance": "3", "db_type": "MYSQL", "state": "RUNNING"},
                 user="user", password="pass")]
    # ############ POSTGRES INSTANCES #####################
    assert dbod_instances.PostgresDbodInstance.__init__. \
        mock_calls \
        == [call({"instance": "4", "db_type": "PG", "state": "RUNNING"},
                 user="user", password="pass")]
    # ############ INFLUXDB INSTANCES #####################
    assert dbod_instances.InfluxDbodInstance.__init__. \
        mock_calls \
        == [call({"instance": "2", "db_type": "InfluxDB", "state": "RUNNING"},
                 user="user", password="pass")]
    # ########## SUPER CALLS
    assert len(instances) == 4


@pytest.fixture
def instances_from_json(helper_mocks, mocker):
    requests.get.return_value.status_code = 404

    mocker.patch('dbod_helpers.open')
    mocker.patch('json.load')
    json.load.return_value = [
            {"instance": "1", "db_type": "PG", "state": "RUNNING"},
            {"instance": "2", "db_type": "MYSQL", "state": "RUNNING"},
            {"instance": "3", "db_type": "InfluxDB", "state": "RUNNING"}
        ]

    open_file = MagicMock()
    dbod_helpers.open.return_value.__enter__.return_value = open_file


def test_get_instances_from_json(mocker, tmpdir, instances_from_json):
    """
    API call failed - use entities.json
    """

    h = DbodCollectdHelper()
    instances = h.get_instances()
    json.load.assert_called_with(
        dbod_helpers.open.return_value.__enter__.return_value)
    dbod_helpers.open.assert_called_with(h.cachefile)
    assert dbod_instances.MySQLDbodInstance.__init__. \
        mock_calls == [call({"instance": "2", "db_type": "MYSQL", "state": "RUNNING"},
                            user="uu", password="uu")]
    assert dbod_instances.PostgresDbodInstance.__init__. \
        mock_calls == [call({"instance": "1", "db_type": "PG", "state": "RUNNING"},
                            user="uu", password="uu")]
    assert dbod_instances.InfluxDbodInstance.__init__. \
        mock_calls == [call({"instance": "3", "db_type": "InfluxDB", "state": "RUNNING"},
                            user="uu", password="uu")]
    assert len(instances) == 3


def test_get_instances_instance_raises_exception(
        mocker, tmpdir, instances_from_json):
    """
    When DbodInstance creation raises exception - we should get
        MalformedDbodInstance
    """
    dbod_instances.MySQLDbodInstance.__init__.side_effect = \
        dbod_helpers.EntityMalformedException("sth wrong")
    h = DbodCollectdHelper()
    instances = h.get_instances()
    assert dbod_instances.MalformedDbodInstance.__init__. \
        mock_calls == [call({"instance": "2", "db_type": "MYSQL", "state": "RUNNING"},
                            user="uu", password="uu")]
    assert len(instances) == 3
    assert isinstance(instances[1], dbod_instances.MalformedDbodInstance)


def test_get_instances_request_raises_exception_use_json(
        mocker, tmpdir, instances_from_json):
    requests.get.side_effect = requests.ConnectionError("Something wrong")
    h = DbodCollectdHelper()
    instances = h.get_instances()
    json.load.assert_called_with(
        dbod_helpers.open.return_value.__enter__.return_value)
    assert len(instances) == 3


def test_get_instances_db_type_missing(mocker, tmpdir, helper_mocks):
    """
    Test get_instances calls api to get a list of instances
        if it fails, it reads entities.json
        Then it creates a list of DbodInstance object
        which is returned
    """
    # Everything ok - status code 200
    mocker.patch('dbod_helpers.open')
    requests.get.return_value.json.return_value = \
        {"response": [
            {"instance": "1", "db_type": "MYSQL", "state": "RUNNING"},
            {"instance": "2", "db_type": "InfluxDB", "state": "RUNNING"},
            {"instance": "3", "db_type": "MYSQL", "state": "RUNNING"},
            {"instance": "4", "state": "RUNNING"}
        ]}
    h = DbodCollectdHelper()
    instances = h.get_instances()
    assert len(instances) == 4
    assert dbod_instances.MalformedDbodInstance.__init__. \
        mock_calls == [call({"instance": "4", "state": "RUNNING"},
                            password='uu', user='uu')]
    assert isinstance(instances[3], dbod_instances.MalformedDbodInstance)


def test_init_opens_and_reads_dbod_sensor_config(mocker):
    """
    /etc/dbod/sensors/dbod_sensor.ini holds credentials
    to get to each of the databases, for now we'll use this file.
    Maybe it could be read from core.conf?
    """
    mocker.patch("apacheconfig.make_loader")
    mock_config_parser = mocker.patch('dbod_helpers.ConfigParser')
    mock_config_parser.return_value.get.side_effect = ["user", "pass"]
    helper = DbodCollectdHelper()
    mock_config_parser.assert_called()
    mock_config_parser.return_value.read.assert_called_with(
        "/etc/dbod/sensors/dbod_sensor.ini")
    mock_config_parser.return_value.get.mock_calls == [
        call("mysql", "user"), call("mysql", "password")]
    assert helper.user == "user"
    assert helper.password == "pass"
    ######################################################
    # It should raise DbodConfigException on any problems
    ######################################################
    try:
        from ConfigParser import NoOptionError
    except ImportError: # Python 3
        from configparser import NoOptionError
    mock_config_parser.return_value.get.side_effect = \
        NoOptionError("pro", "section")
    with raises(DbodConfigException) as exc:
        helper = DbodCollectdHelper()
    assert "Error reading /etc/dbod/sensors/dbod_sensor.ini: "\
        in str(exc.value)


@pytest.mark.parametrize(
    "state,api_url,endpoint,dbname,status_code,current_state",
    [("STOPPED", "api.cern.ch:3", "api/test", "db1",
      204, "RUNNING"),
     ("RUNNING", "a.c/232", "api/ent", "db2",
      204, "RUNNING"),
     ("BUSY", "test-api:33", "api/entities", "db3",
      200, "RUNNING"),
     ("RUNNING", "test-api:33", "api/entities", "db6",
      200, "JOB_PENDING"),
     ("RUNNING", "test-api:33", "api/entities", "db5",
      200, "AWAITING_APPROVAL"),
     ("BUSY", "test-api:33", "api/entities", "db4",
      200, "MAINTENANCE"),
     ])
def test_update_state(mocker, state, api_url, endpoint, dbname,
                       status_code, current_state):
    init = mocker.patch('dbod_helpers.DbodCollectdHelper.__init__')
    init.return_value = None
    helper = DbodCollectdHelper()
    helper.api_url = api_url
    helper.entity_endpoint = endpoint
    helper.api_user = "user"
    helper.api_password = "pass"

    import requests
    import collectd
    mocker.resetall()
    requests.put.reset_mock()

    class Instance:
        pass
    instance = Instance()
    instance.db_name = dbname
    instance.state = current_state
    expected_url = "%s/%s/%s" % (api_url, endpoint, dbname)
    requests.put.return_value.status_code = status_code
    helper.update_state(instance, state)

    if current_state in ["JOB_PENDING", "AWAITING_APPROVAL", "MAINTENANCE"]:
        requests.put.assert_not_called()
        collectd.debug.assert_called_with(
            "Not updating state of %s. Instance state: %s"
            % (dbname, current_state))
    elif current_state == state:
        requests.put.assert_not_called()
        collectd.debug("Instance %s state [%s] has not changed"
                        % (instance.db_name, instance.state))
    else:
        collectd.debug("Updating %s instance state to: %s"
                        % (instance.db_name, instance.state))
        if hasattr(instance, 'id'):
            expected_url = "%s/%s/%s" % (api_url,
                                    endpoint,
                                    instance.id)
        else:
            expected_url = "%s/%s/%s" % (api_url,
                                    endpoint,
                                    instance.db_name)

        data_to_post = {"state": state}
        requests.put.assert_called_with(
            expected_url,
            auth=(helper.api_user, helper.api_password),
            json=data_to_post,
            verify=False
            )
        if status_code != 204:
            collectd.error.assert_called_with(
                "Failed updating state of %s. Response code %s, url %s, self.api_url %s, self.entity_endpoint %s, "
                % (dbname, status_code, expected_url, api_url, endpoint))

