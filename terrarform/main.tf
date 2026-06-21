# # This main.tf is the core of your Terraform setup. It defines your EKS (Elastic Kubernetes Service) cluster using a reusable community module instead of writing everything from scratch.

# module "vpc" {
#   source  = "terraform-aws-modules/vpc/aws"
#   version = "~> 5.0"

#   name = "${var.cluster_name}-vpc"
#   cidr = "10.0.0.0/16"

#   azs             = ["us-east-1a", "us-east-1b"]

#   public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]

#   enable_nat_gateway = false

#   map_public_ip_on_launch = true

#   tags = {
#     "Environment" = "dev"
#   }
# }

# # This tells Terraform:
#     # “Use a pre-built EKS module”
#     # “Create a Kubernetes cluster on AWS”
#     # “Also create worker nodes (EC2 machines) for it”
# # So instead of manually writing 100+ lines of AWS resources, you are using a Terraform module abstraction.
# module "eks" {
#   source  = "terraform-aws-modules/eks/aws"
#   version = "~> 21.0"  # Use version 21.x Avoid version 22.0 or higher

#   name               = var.cluster_name
#   kubernetes_version = "1.30"

#   vpc_id     = module.vpc.vpc_id
#   subnet_ids = module.vpc.public_subnets

#   # Keep API endpoint public for a simple, low-cost public-subnet lab setup.
#   endpoint_private_access = false
#   endpoint_public_access  = true

#   # This defines worker nodes (EC2 instances) that run your pods.
#   # create one node group as default 
#   eks_managed_node_groups = {
#     default = {
#       desired_size = 1  # keep 2 EC2 running instance always
#       min_size     = 1  # Cluster can scale down to 1 node. prevent full shutdown
#       max_size     = 1  # Cluster can scale up to 3 nodes.[auto scaling behavior]

#       # Free Tier-eligible for study usage in most accounts/regions.
#       instance_types = ["t3.micro"]

#       ami_type = "AL2_x86_64"

#       kubernetes_version = "1.30"

#       associate_public_ip_address = true
#     }
#   }
# }
resource "aws_security_group" "ec2_sg" {
  name = "anomaly-sg"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "FastAPI"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = var.instance_type

  key_name = "anomaly-key"

  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = {
    Name = "anomaly-api-ec2"
  }
}