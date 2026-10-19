
variable "aws_region" {
  description = "AWS region for the CloudOps AI Lab platform."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project identifier used in resource names."
  type        = string
  default     = "cloudops-ai-lab"
}

variable "vpc_cidr" {
  description = "Private IPv4 address range for the VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "availability_zone_count" {
  description = "Number of Availability Zones for the platform."
  type        = number
  default     = 3

  validation {
    condition     = var.availability_zone_count == 3
    error_message = "This architecture currently requires three Availability Zones."
  }
}


variable "eks_admin_cidrs" {
  description = "Trusted public IPv4 CIDR ranges allowed to access the EKS Kubernetes API."
  type        = list(string)

  validation {
    condition = (
      length(var.eks_admin_cidrs) > 0 &&
      alltrue([
        for cidr in var.eks_admin_cidrs :
        can(cidrhost(cidr, 0)) && cidr != "0.0.0.0/0"
      ])
    )
    error_message = "Provide at least one valid trusted IPv4 CIDR, not 0.0.0.0/0."
  }
}

