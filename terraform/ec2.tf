resource "aws_instance" "bastion" {
    instance_type = var.instance_type
    ami = var.ami 
    key_name = var.key_name
    subnet_id = var.subnet_id
    vpc_security_group_ids = [aws_security_group.sg.id]
    tags = merge(var.mytags, {Name="bastion"})
    user_data = <<EOF
#!/bin/bash
apt update
apt install tmux awscli -y
EOF

}

resource "aws_security_group" "sg" {
    name = "bastion_sg"
    vpc_id = var.vpc_id
    tags = var.mytags

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        description = "SSH"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        description = "HTTPS"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 8200
        to_port = 8200
        protocol = "tcp"
        description = "Telegram Bot"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 8100
        to_port = 8100
        protocol = "tcp"
        description = "Telegram Bot"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port        = 0
        to_port          = 0
        protocol         = "-1"
        cidr_blocks      = ["0.0.0.0/0"]    
    }
}


variable "key_name" {
    type = string
}
variable "vpc_id" {
    type = string
}
variable "subnet_id" {
    type = string
}
variable "instance_type" {
    type = string
}
variable "ami" {
    type = string
}