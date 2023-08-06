"""Update instance status, get list of instances on a host

Raises:
    DbodConfigException: Missing configuration
        in /etc/dbod/sensors/dbod_sensor.ini or /etc/dbod/core.conf
"""
import json
from socket import gethostname

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
import apacheconfig
import requests
from dbod_instances import EntityMalformedException, MalformedDbodInstance, \
    instance_types
import collectd  # pylint: disable=import-error


class DbodConfigException(Exception):
    """Raised when the config is missing or malformed."""


class DbodCollectdHelper:
    """Class mostly used in performing operations with DBOD API."""

    # pylint: disable=unsubscriptable-object, too-many-instance-attributes
    # pylint: disable=import-outside-toplevel
    def __init__(self):
        """Read DBOD config file."""
        from apacheconfig import make_loader
        config_file = "/etc/dbod/core.conf"
        ##################################################
        # Load DBOD config file to get api endpoints and
        # cachefile location
        ##################################################
        with make_loader() as loader:
            try:
                self.config = loader.load(config_file)
            except apacheconfig.error.ConfigFileReadError as e:
                raise DbodConfigException(e)
        ##################################################
        # Get interesting info from the config file
        ##################################################
        try:
            self.cachefile = self.config['api']['cachefile']
            self.api_url = self.config['api']['host']
            self.host_metadata_endpoint = \
                self.config['api']['host_metadata_endpoint']
            self.entity_endpoint = \
                self.config['api']['entity_endpoint']
            self.api_user = self.config['api']['user']
            self.api_password = self.config['api']['password']
        except KeyError as e:
            raise DbodConfigException(
                "Error in DBOD config file (%s): missing key '%s'"
                % (config_file, e.args[0]))
        ##################################################
        # Read /etc/dbod/sensors/dbod_sensor.ini to get the password
        ##################################################
        try:
            config = ConfigParser()
            config.read("/etc/dbod/sensors/dbod_sensor.ini")
            self.user = config.get("mysql", "user")
            self.password = config.get("mysql", "password")
        except Exception as e:
            raise DbodConfigException(
                "Error reading /etc/dbod/sensors/dbod_sensor.ini: %s"
                % (e))

    def get_instances(self):
        """
        Get running instances in the node
        First try an API call - if it fails use entities.json
        Returns:
            entities data as a dict (from /etc/dbod/cache/entities.json)
        """
        # Get host name
        hostname = gethostname()
        hostname = hostname.split(".")[0]
        url = "%s/%s/%s" % (self.api_url, self.host_metadata_endpoint,
                            hostname)

        ###################################
        # Get data from the API
        ###################################
        try:
            request = requests.get(url)
            # If status code != 200 - get it from entities.json
            if request.status_code != 200:
                with open(self.cachefile) as f:
                    data = json.load(f)
            else:
                data = request.json()["response"]
        except requests.ConnectionError:
            with open(self.cachefile) as f:
                data = json.load(f)

        ######################################
        # Create Instances from the response
        ######################################
        instances = []

        for instance_dict in data:
            # If creating DbodInstance raises exception, we either
            # pass it further or ignore it - depends on the metric!
            try:
                #####################################################
                # Create instances based on the db_type attribute
                #####################################################
                # Dynamically decide which instance
                # to create based on the db_type
                if instance_dict['state'] != 'MAINTENANCE':
                    try:
                        #check if we use the old api:
                        if 'db_type' in instance_dict:
                            type = instance_dict['db_type']
                        else:
                            type = instance_dict['type']
                        instances.append(
                            instance_types[type](instance_dict,
                              user=self.user,
                              password=self.password
                              ))

                    except KeyError:
                        # Missing db_type
                        instances.append(
                            MalformedDbodInstance(instance_dict,
                                                  user=self.user,
                                                  password=self.password))
            except EntityMalformedException:
                # Create MalformedDbodInstance
                instances.append(MalformedDbodInstance(
                    instance_dict, user=self.user, password=self.password))
        return instances

    def update_state(self, instance, state):
        """
        instance - one of DbodInstance
        state - DbodInstance.STOPPED or DbodInstance.RUNNING for now

        update instance state in DBOD API
        """
        if instance.state in ["JOB_PENDING", "AWAITING_APPROVAL",
                              "MAINTENANCE"]:
            collectd.debug("Not updating state of %s. Instance state: %s"
                           % (instance.db_name, instance.state))
        elif instance.state == state:
            collectd.debug("Instance %s state [%s] has not changed"
                           % (instance.db_name, instance.state))
        else:
            collectd.debug("Updating %s instance state to: %s"
                           % (instance.db_name, state))
            if hasattr(instance, 'id'):
                url = "%s/%s/%s" % (self.api_url,
                                self.entity_endpoint,
                                instance.id)
            else:
                url = "%s/%s/%s" % (self.api_url,
                                self.entity_endpoint,
                                instance.db_name)
            response = requests.put(
                url, auth=(self.api_user, self.api_password),
                json={"state": state},
                verify=False)  # nosec
            if response.status_code != 204:
                collectd.error("Failed updating state of %s. Response code %s, url %s, self.api_url %s, self.entity_endpoint %s, "
                               % (instance.db_name, response.status_code, url,self.api_url,self.entity_endpoint))
