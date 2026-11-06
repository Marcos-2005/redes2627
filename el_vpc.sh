#!/bin/bash

# Obtén los IDs de las VPCs que tienen la etiqueta tipo=prueba
VPC_IDS=$(aws ec2 describe-vpcs \
    --filters "Name=tag:tipo,Values=prueba" \
    --query "Vpcs[*].VpcId" \
    --output text)

# Recorre cada ID de VPC y elimínala de forma segura limpiando sus dependencias
for VPC_ID in $VPC_IDS; do
    echo "Eliminación para la VPC: $VPC_ID"
    
    # Terminar y esperar a que se eliminen las instancias EC2 asociadas
    INSTANCE_IDS=$(aws ec2 describe-instances \
        --filters "Name=vpc-id,Values=$VPC_ID" "Name=instance-state-name,Values=running,stopped,pending" \
        --query "Reservations[*].Instances[*].InstanceId" \
        --output text)
    
    if [ -n "$INSTANCE_IDS" ]; then
        echo "-> Terminando instancias EC2: $INSTANCE_IDS"
        aws ec2 terminate-instances --instance-ids $INSTANCE_IDS
        echo "   Esperando a que las instancias se terminen por completo..."
        aws ec2 wait instance-terminated --instance-ids $INSTANCE_IDS
    fi

    # Eliminar Internet Gateways (IGW)
    IGW_IDS=$(aws ec2 describe-internet-gateways \
        --filters "Name=attachment.vpc-id,Values=$VPC_ID" \
        --query "InternetGateways[*].InternetGatewayId" \
        --output text)
        
    for IGW_ID in $IGW_IDS; do
        echo "-> Desvinculando y eliminando Internet Gateway: $IGW_ID"
        aws ec2 detach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID
        aws ec2 delete-internet-gateway --internet-gateway-id $IGW_ID
    done

    # Eliminar Tablas de Rutas 
    RT_IDS=$(aws ec2 describe-route-tables \
        --filters "Name=vpc-id,Values=$VPC_ID" \
        --query "RouteTables[?Associations[!Main]].RouteTableId" \
        --output text)
        
    for RT_ID in $RT_IDS; do
        echo "-> Eliminando Tabla de Rutas: $RT_ID"
        aws ec2 delete-route-table --route-table-id $RT_ID
    done

    # Eliminar los Grupos de Seguridad 
    SG_IDS=$(aws ec2 describe-security-groups \
        --filters "Name=vpc-id,Values=$VPC_ID" \
        --query "SecurityGroups[?GroupName != 'default'].GroupId" \
        --output text)
        
    for SG_ID in $SG_IDS; do
        echo "-> Eliminando Grupo de Seguridad: $SG_ID"
        aws ec2 delete-security-group --group-id $SG_ID
    done

    # Eliminar las Subredes
    SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[*].SubnetId" --output text)
    for SUBNET_ID in $SUBNET_IDS; do
        aws ec2 delete-subnet --subnet-id $SUBNET_ID
        echo "-> Subnet $SUBNET_ID eliminada."
    done
    
    # Eliminar la VPC
    aws ec2 delete-vpc --vpc-id $VPC_ID
    echo ">>> VPC $VPC_ID eliminada correctamente."
    echo ""
done

echo "Limpieza finalizado."