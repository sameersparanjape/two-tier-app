variable "aws_region" {
  default = "us-east-2"
}

variable "project_name" {
  default = "random-number-service"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "frontend_port" {
  default = 80
}

variable "backend_port" {
  default = 8000
}

variable "cpu" {
  default = "256"
}

variable "memory" {
  default = "512"
}
