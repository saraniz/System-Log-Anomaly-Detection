# # defines input variables for your Terraform project

# # A variable is like a parameter you pass into your infrastructure code
# # This defines a variable named aws_region
# variable "aws_region" {
#   default = "us-east-1"
# }

# variable "cluster_name" {
#   default = "anomaly-cluster"
# }
variable "ami_id" {
  default = "ami-0c02fb55956c7d316" # Ubuntu 22.04 (us-east-1)
}

variable "instance_type" {
  default = "t3.micro"
}