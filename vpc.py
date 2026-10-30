import boto3

def configurar_red_y_ec2():
    # Crear cliente
    ec2 = boto3.client('ec2')

    #Crear la VPC
    vpc = ec2.create_vpc(CidrBlock='193.168.5.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    print(f"VPC ID: {vpc_id}")

    # DNS
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
    
    # Tags VPC
    ec2.create_tags(
        Resources=[vpc_id],
        Tags=[{'Key': 'Name', 'Value': 'MiVPC-Boto3'}]
    )
    print("DNS habilitado")

    # Crear Internet Gateway (IGW)
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']
    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    ec2.create_tags(
        Resources=[igw_id],
        Tags=[{'Key': 'Name', 'Value': 'MiIGW-Boto3'}]
    )
    print(f"Internet Gateway ID: {igw_id}")

    # Crear la Subnet dentro de la VPC
    subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='193.168.5.0/24'
    )
    subnet_id = subnet['Subnet']['SubnetId']
    
    # Configurar subred 
    ec2.modify_subnet_attribute(
        SubnetId=subnet_id,
        MapPublicIpOnLaunch={'Value': True}
    )

    ec2.create_tags(
        Resources=[subnet_id],
        Tags=[{'Key': 'Name', 'Value': 'MiSubnet-Boto3'}]
    )
    print(f"Subnet pública ID: {subnet_id}")

    # Crear la Tabla de Rutas
    route_table = ec2.create_route_table(VpcId=vpc_id)
    rt_id = route_table['RouteTable']['RouteTableId']

    ec2.create_route(
        RouteTableId=rt_id,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id
    )

    ec2.associate_route_table(
        RouteTableId=rt_id,
        SubnetId=subnet_id
    )
    
    ec2.create_tags(
        Resources=[rt_id],
        Tags=[{'Key': 'Name', 'Value': 'MiRouteTable-Boto3'}]
    )
    print(f"Tabla de rutas ID: {rt_id}")

    # Crear el Grupo de Seguridad
    sg = ec2.create_security_group(
        GroupName='MiSecurityGroup-Boto3',
        Description='Grupo de seguridad para acceso publico y ping',
        VpcId=vpc_id
    )
    sg_id = sg['GroupId']

    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'icmp', 'FromPort': -1, 'ToPort': -1, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )
    print(f"Grupo de seguridad ID: {sg_id}")

    # Lanzar Instancia EC2
    instancia = ec2.run_instances(
        ImageId='ami-0bfc5cae5711ffac8',  # Asegúrate de que esta AMI sea válida en tu región de AWS Academy
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SubnetId=subnet_id,
        SecurityGroupIds=[sg_id],
        KeyName='vockey',  # Par de claves estándar de los laboratorios AWS Academy
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'MiEC2-Boto3'}]
        }]
    )

    instance_id = instancia['Instances'][0]['InstanceId']
    print(f"Instancia EC2 ID: {instance_id}")

    return instance_id

if __name__ == "__main__":
    instance_id = configurar_red_y_ec2()
    print(f"✨✨✨ Proceso completado, id instancia: {instance_id}✨✨✨")