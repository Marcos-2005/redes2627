import boto3

def crear_infraestructura():
    ec2 = boto3.client('ec2')

    # VPC
    vpc = ec2.create_vpc(CidrBlock='172.16.0.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    
    ec2.create_tags(
        Resources=[vpc_id],
        Tags=[{'Key': 'Name', 'Value': 'VPC-Marcos'}]
    )
    print(f"VPC ID: {vpc_id}")

    # Subred Pública
    subnet_pub = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='172.16.0.0/20'
    )
    subnet_pub_id = subnet_pub['Subnet']['SubnetId']
    
    ec2.modify_subnet_attribute(
        SubnetId=subnet_pub_id,
        MapPublicIpOnLaunch={'Value': True}
    )

    ec2.create_tags(
        Resources=[subnet_pub_id],
        Tags=[{'Key': 'Name', 'Value': 'Subnet-Publica'}]
    )
    print(f"Subnet Publica ID: {subnet_pub_id}")

    # Subred Privada
    subnet_priv = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='172.16.64.0/20'
    )
    subnet_priv_id = subnet_priv['Subnet']['SubnetId']
    
    ec2.create_tags(
        Resources=[subnet_priv_id],
        Tags=[{'Key': 'Name', 'Value': 'Subnet-Privada'}]
    )
    print(f"Subnet Privada ID: {subnet_priv_id}")

    # Grupo de Seguridad
    sg_id = 'sg-0ee6888e4a1e83a4f'

    # Instancia EC2 en Subred Pública
    instancia_pub = ec2.run_instances(
        ImageId='ami-0d97d7f07b25dd693',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SubnetId=subnet_pub_id,
        SecurityGroupIds=[sg_id],
        KeyName='vockey'
    )
    instance_pub_id = instancia_pub['Instances'][0]['InstanceId']
    
    ec2.create_tags(
        Resources=[instance_pub_id],
        Tags=[{'Key': 'Name', 'Value': 'Servidor-Publico'}]
    )
    print(f"EC2 Publica ID: {instance_pub_id}")

    # Instancia EC2 en Subred Privada
    instancia_priv = ec2.run_instances(
        ImageId='ami-0d97d7f07b25dd693',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SubnetId=subnet_priv_id,
        SecurityGroupIds=[sg_id],
        KeyName='vockey'
    )
    instance_priv_id = instancia_priv['Instances'][0]['InstanceId']
    
    ec2.create_tags(
        Resources=[instance_priv_id],
        Tags=[{'Key': 'Name', 'Value': 'Servidor-Privado'}]
    )
    print(f"EC2 Privada ID: {instance_priv_id}")

    return vpc_id, subnet_pub_id, subnet_priv_id, instance_pub_id, instance_priv_id

if __name__ == "__main__":
    crear_infraestructura()
    print("Proceso completado.")