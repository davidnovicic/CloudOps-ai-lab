
variable "project_name" {
  description = "Project identifier."
  type        = string
}

variable "cluster_role_arn" {
  description = "IAM role ARN assumed by the EKS control plane."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnets used by EKS."
  type        = list(string)
}

variable "eks_admin_cidrs" {
  description = "Trusted public IPv4 CIDRs for Kubernetes API access."
  type        = list(string)
}

variable "kubernetes_version" {
  description = "Kubernetes version for the EKS cluster."
  type        = string
  default     = "1.34"
}


variable "node_role_arn" {
  description = "IAM role assumed by EKS worker nodes."
  type        = string
}

variable "node_instance_types" {
  description = "EC2 instance types for worker nodes."
  type        = list(string)
  default     = ["t3.small"]
}

variable "node_desired_size" {
  description = "Desired worker count when deployed."
  type        = number
  default     = 1
}

variable "node_min_size" {
  description = "Minimum worker count."
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum worker count."
  type        = number
  default     = 2
}
