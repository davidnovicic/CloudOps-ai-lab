
data "aws_availability_zones" "available" {
  state = "available"
}

module "networking" {
  source = "./modules/networking"

  project_name = var.project_name
  vpc_cidr     = var.vpc_cidr
  availability_zones = slice(
    data.aws_availability_zones.available.names,
    0,
    var.availability_zone_count
  )
}


module "iam" {
  source = "./modules/iam"

  project_name = var.project_name
}


module "eks" {
  source = "./modules/eks"

  project_name       = var.project_name
  cluster_role_arn   = module.iam.cluster_role_arn
  node_role_arn      = module.iam.node_role_arn
  private_subnet_ids = module.networking.private_subnet_ids
  eks_admin_cidrs    = var.eks_admin_cidrs

  node_instance_types = ["t3.small"]
  node_desired_size   = 1
  node_min_size       = 1
  node_max_size       = 2

  depends_on = [
    module.iam
  ]
}
