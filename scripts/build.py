import boto3
import yaml


keys = yaml.safe_load(open("config.yml").read())

userdata = open("userdata.sh").read()


ec2 = boto3.Session(
    aws_access_key_id=keys["aws_access_key_id"],
    aws_secret_access_key=keys["aws_secret_access_key"],
    region_name="us-east-2",
).client("ec2")

#r = ec2.describe_instances(Filter=[dict(Name="vpn.devstack.ninja.")])

r = ec2.run_instances(
    BlockDeviceMappings=[
        {
            "DeviceName": "/dev/xvda",
            "Ebs": {
                "DeleteOnTermination": True,
                "VolumeSize": 20,
                "VolumeType": "standard",
            },
        },
    ],
    ImageId="ami-0bb7d855677353076",
    InstanceType="t3.micro",
    KeyName="srak",
    UserData=userdata,
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[
        {
            "AssociatePublicIpAddress": False,
            "DeleteOnTermination": True,
            "DeviceIndex": 0,
            "Description": "vpn.ngnh.org.",
            "Groups": ["sg-06c2fb84dea98006b"],
            "SubnetId": "subnet-07fa2b2152939dae4",
            "PrivateIpAddress": "172.31.16.5",
        },
    ],
    TagSpecifications=[
        {
            "ResourceType": "instance",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "vpn.ngnh.org."
                },
            ]
        },
    ],
)

instance_id = r["Instances"][0]["InstanceId"]
interface_id = r["Instances"][0]["NetworkInterfaces"][0]["NetworkInterfaceId"]

r = ec2.assign_private_ip_addresses(
    NetworkInterfaceId=interface_id,
    Ipv4Prefixes=["172.31.16.16/28"],
)

r = ec2.describe_addresses()

def tag_for_key(name, tags):
    for t in tags:
        if t["Key"] == name:
            return t["Value"]
    return None

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

print("Fetched ips by name")
print(ips_by_name)

print(f"Waiting for {instance_id} to start")
ec2.get_waiter("instance_running").wait(InstanceIds=[instance_id])

print(f"Assigning addresses to instance")
ec2.associate_address(
    NetworkInterfaceId=interface_id,
    AllocationId=ips_by_name["vpn.ngnh.org."]["AllocationId"],
    PrivateIpAddress="172.31.16.5",
)
ec2.associate_address(
    NetworkInterfaceId=interface_id,
    AllocationId=ips_by_name["bigmomma.ngnh.org."]["AllocationId"],
    PrivateIpAddress="172.31.16.17",
)
ec2.associate_address(
    NetworkInterfaceId=interface_id,
    AllocationId=ips_by_name["bigpoppa.ngnh.org."]["AllocationId"],
    PrivateIpAddress="172.31.16.18",
)
