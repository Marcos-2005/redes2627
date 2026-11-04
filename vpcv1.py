import boto3

def crear_vpc_subnet_ec2():
    ec2 = boto3.client('ec2')

    # VPC
    vpc = ec2.create_vpc(CidrBlock='193.168.5.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    
    ec2.create_tags(
        Resources=[vpc_id],
        Tags=[{'Key': 'Name', 'Value': 'VPC-Marcos'},
              {'Key': 'entorno', 'Value': 'prueba'}]
    )
    print(f"VPC ID: {vpc_id} ")

    # Subred
    subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='193.168.5.0/24'
    )
    subnet_id = subnet['Subnet']['SubnetId']
    
    ec2.create_tags(
        Resources=[subnet_id],
        Tags=[{'Key': 'Name', 'Value': 'Subnet-Publica'}]
    )
    print(f"Subnet ID: {subnet_id}")

    # Instancia EC2
    instancia = ec2.run_instances(
        ImageId='ami-0d97d7f07b25dd693',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SubnetId=subnet_id,
        KeyName='vockey'
    )
    instance_id = instancia['Instances'][0]['InstanceId']
    
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[{'Key': 'Name', 'Value': 'Servidor-Ubuntu'}]
    )
    print(f"Instancia EC2 ID: {instance_id} ")

    return vpc_id, subnet_id, instance_id

if __name__ == "__main__":
    crear_vpc_subnet_ec2()
    print("Proceso completado.")