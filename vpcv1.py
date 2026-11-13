import boto3

def crear_infraestructura():
    ec2 = boto3.client('ec2')

    # Creación VPC
    vpc = ec2.create_vpc(CidrBlock='172.16.0.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    
    ec2.create_tags(
        Resources=[vpc_id],
        Tags=[{'Key': 'Name', 'Value': 'VPC-Marcos'}]
    )
    print(f"VPC ID: {vpc_id}")

    # Crear el IGW para poder salir al exterior
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']
    
    ec2.create_tags(
        Resources=[igw_id],
        Tags=[{'Key': 'Name', 'Value': 'IGW-Marcos'}]
    )
    
    ec2.attach_internet_gateway(
        InternetGatewayId=igw_id,
        VpcId=vpc_id
    )
    print(f"Internet Gateway ID: {igw_id}")

    # Creación subred (Pública)
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

    # Creación subred (Privada)
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

    # Tabla de enrutamiento
    route_table = ec2.create_route_table(VpcId=vpc_id)
    route_table_id = route_table['RouteTable']['RouteTableId']
    
    ec2.create_tags(
        Resources=[route_table_id],
        Tags=[{'Key': 'Name', 'Value': 'RT-Publica'}]
    )
    print(f"Route Table ID: {route_table_id}")

    # 4. Agregamos una ruta para la salida a internet
    ec2.create_route(
        RouteTableId=route_table_id,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id
    )
    print(f"Ruta 0.0.0.0/0 añadida hacia el IGW: {igw_id}")

    # Grupo de seguridad
    security_group = ec2.create_security_group(
        GroupName='SG-Practica',
        Description='Grupo de seguridad para la VPC de Marcos',
        VpcId=vpc_id
    )
    sg_id = security_group['GroupId']

    ec2.create_tags(
        Resources=[sg_id],
        Tags=[{'Key': 'Name', 'Value': 'SG-Acceso'}]
    )
    print(f"Security Group ID: {sg_id}")

    # Creación EC2 (Instancia Pública)
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

    # Creación EC2 (Instancia Privada)
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

    return vpc_id, igw_id, subnet_pub_id, subnet_priv_id, route_table_id, sg_id, instance_pub_id, instance_priv_id

if __name__ == "__main__":
    crear_infraestructura()
    print("Proceso completado.")