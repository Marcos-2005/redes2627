import boto3

def crear_vpc():
    # Crear cliente de EC2
    ec2 = boto3.client('ec2')

    # Crear la VPC
    vpc = ec2.create_vpc(CidrBlock='193.168.5.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    print(f"✅ VPC creada con ID: {vpc_id}")

    # Habilitar DNS support
    ec2.modify_vpc_attribute(
        VpcId=vpc_id,
        EnableDnsSupport={'Value': True}
    )

    # Habilitar DNS hostnames
    ec2.modify_vpc_attribute(
        VpcId=vpc_id,
        EnableDnsHostnames={'Value': True}
    )

    # Etiquetar la VPC (opcional)
    ec2.create_tags(
        Resources=[vpc_id],
        Tags=[{'Key': 'Name', 'Value': 'MiVPC-Boto3'}]
    )

    print("🌐 DNS habilitado y etiqueta 'MiVPC-Boto3' asignada.")
    return vpc_id

def create_subnet(vpc_id):
    # Crear cliente de EC2
    ec2 = boto3.client('ec2')

    # Crear subnet dentro de la VPC
    subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='193.168.5.0/24'
    )

    # Obtener el ID de la subnet creada
    subnet_id = subnet['Subnet']['SubnetId']

    # Etiquetar la subnet
    ec2.create_tags(
        Resources=[subnet_id],
        Tags=[{'Key': 'Name', 'Value': 'MiSubnet-Boto3'}]
    )

    print(f"✅ Subnet creada con ID: {subnet_id}")

    return subnet_id


def crear_ec2(subnet_id):
    # Crear cliente de EC2
    ec2 = boto3.client('ec2')

    # Lanzar una instancia
    instancia = ec2.run_instances(
        ImageId='ami-xxxxxxxxxxxxxxxxx',  # Sustituir por una AMI válida
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SubnetId=subnet_id
    )

    instance_id = instancia['Instances'][0]['InstanceId']

    # Etiquetar la instancia
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[{'Key': 'Name', 'Value': 'MiEC2-Boto3'}]
    )

    print(f"✅ Instancia creada con ID: {instance_id}")

    return instance_id


if __name__ == "__main__":
    vpc_id = crear_vpc()
    print(f"🚀 Proceso completado. ID de la VPC: {vpc_id}")

    subnet_id = create_subnet(vpc_id)
    print(f"🚀 Subnet creada: {subnet_id}")

    instance_id = crear_ec2(subnet_id)
    print(f"🚀 EC2 creada: {instance_id}")