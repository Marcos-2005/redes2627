import boto3

def crear_vpc_subnet_ec2():
    ec2 = boto3.client('ec2')

    # VPC
    vpc = ec2.create_vpc(CidrBlock='193.168.5.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    print(f"VPC ID: {vpc_id}")

    # 2. Subnet
    subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='193.168.5.0/24'
    )
    subnet_id = subnet['Subnet']['SubnetId']
    print(f"Subnet ID: {subnet_id}")

    # 3. Instancia EC2
    instancia = ec2.run_instances(
        ImageId='ami-0bfc5cae5711ffac8',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SubnetId=subnet_id,
        KeyName='vockey'
    )
    instance_id = instancia['Instances'][0]['InstanceId']
    print(f"Instancia EC2 ID: {instance_id}")

    return vpc_id, subnet_id, instance_id

if __name__ == "__main__":
    crear_vpc_subnet_ec2()
    print("Proceso completado.")