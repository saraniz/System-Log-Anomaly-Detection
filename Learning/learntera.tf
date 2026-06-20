// provider block
provider "aws" {
    region = "us-east-1"
}

// resource block
resource "aws_instance" "web-server" {
    ami = "ami_2345"
    instance_type = "t2.macro"

    tags = {
        Name = "Development-Server"
    }
}

# s3 bucket
resource "aws_s3_bucket" "new-bucket" {
    bucket = "amie-bucket"

    tags = {
        Environment = "Dev"
        Team = "Backend"
        Owner = "Amie"
    }
}

