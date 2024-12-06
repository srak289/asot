import boto3
import yaml


keys = yaml.safe_load(open("config.yml").read())

class AwsConnection:

    def __init__(self, config):
        self._config = config

    @property
    def session(self):
        return boto3.Session(
            aws_access_key_id=self._config["aws_access_key_id"],
            aws_secret_access_key=self._config["aws_secret_access_key"],
            region_name=self._config["region_name"],
        )

    def _prepare(self):
        pass

    def tag_for_key(name, tags):
        for t in tags:
            if t["Key"] == name:
                return t["Value"]
        return None

    async def list_elastic_ips(self):
        r = ec2.describe_addresses()
        ips_by_name = {}
        for x in r["Addresses"]:
            if "AssociationId" in x:
                continue
            name = tag_for_key("Name", x["Tags"])
            if name is None:
                print(f"{x} has no tag 'Name'")
                continue
            print(f"Adding {name}")
            ips_by_name[name] = x

        pass

    async def list_associations(self):
        ips_by_name = {}
        for x in r["Addresses"]:
            if "AssociationId" in x:
                continue
            name = tag_for_key("Name", x["Tags"])
            if name is None:
                print(f"{x} has no tag 'Name'")
                continue
            print(f"Adding {name}")
            ips_by_name[name] = x

        pass

    async def allocate_ip(self):
        pass

    async def release_ip(self):
        pass

    async def associate_ip(self):
        ec2.associate_address(
            NetworkInterfaceId=interface_id,
            AllocationId=ips_by_name["alma.devstack.ninja."]["AllocationId"],
            PrivateIpAddress="172.31.16.18",
        )
        r = ec2.assign_private_ip_addresses(
            NetworkInterfaceId=interface_id,
            Ipv4Prefixes=["172.31.16.16/28"],
        )
        pass

    async def disassociate_ip(self):
        pass

    async def create_a_record(self):
        pass

    async def delete_a_record(self):
        pass

    async def discover_instance(self):
        r = ec2.describe_instances(Filter=[dict(Name="vpn.devstack.ninja.")])
        instance_id = r["Instances"][0]["InstanceId"]
        interface_id = r["Instances"][0]["NetworkInterfaces"][0]["NetworkInterfaceId"]
