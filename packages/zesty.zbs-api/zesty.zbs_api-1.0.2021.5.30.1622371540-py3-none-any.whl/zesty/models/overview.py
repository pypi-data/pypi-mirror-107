from zesty.id_handler import create_zesty_id


class MachineData:
    os = None
    instance = None

    def __init__(self, machine_data):
        self.cloud_vendor = machine_data.get('cloud', 'Amazon')
        self.os = self.OS(machine_data.get('os', {}))
        self.instance = self.Instance(machine_data.get('instance', {}), self.cloud_vendor)

    class OS:
        system = None
        name = None
        processor = None
        id = None
        os_pretty_name = "N/A"

        def __init__(self, os_data):
            for k, v in os_data.items():
                exec('self.' + k + '=v')

    class Instance:
        accountId = None
        architecture = None
        availabilityZone = None
        billingProducts = None
        devpayProductCodes = None
        marketplaceProductCodes = None
        imageId = None
        instanceId = None
        instanceType = None
        kernelId = None
        pendingTime = None
        privateIp = None
        ramdiskId = None
        region = None
        version = None

        def __init__(self, instance_data, cloud_vendor):
            for k, v in instance_data.items():
                exec('self.' + k + '=v')
            try:
                self.instanceId = create_zesty_id(cloud=cloud_vendor, resource_id=self.instanceId)
            except Exception as e:
                print(f"Failed to create ZestyID, will stay with {self.instanceId} || ERROR : {e}")