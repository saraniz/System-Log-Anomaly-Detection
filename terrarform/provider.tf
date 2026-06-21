# # tells Terraform what version rules to follow and how to connect to AWS.

# # define global terraform settings
# terraform {
#   required_version = ">= 1.5"  # this mean we need terraform version higher than or the 1.5

#   # which external provider that use in here
#   required_providers {
#     aws = {
#         source = "hashicorp/aws" # official aws provider that hashicorp maintain
#         version = ">= 6.0" # Use any version starting from 5.0 up to but not including 6.0
#     }
#   }
# }

# # This is where you actually configure the AWS provider
# # a) provider "aws"
# # This tells Terraform:
# # “Use AWS as the cloud platform for resources”
# # b) region = var.aws_region
# # This sets the AWS region where resources will be created
# # Example regions:
# # ap-south-1 (Mumbai)
# # us-east-1 (N. Virginia)
# provider "aws" {
#     region = "us-east-1"
  
# }
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.42.0, < 7.0.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}