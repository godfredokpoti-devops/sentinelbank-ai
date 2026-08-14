variable "name" { type = string }
variable "subnet_ids" { type = list(string) }
variable "cluster_role_arn" { type = string }
variable "node_role_arn" { type = string }
resource "aws_eks_cluster" "this" {
  name = var.name
  role_arn = var.cluster_role_arn
  vpc_config {
    subnet_ids = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access = false
  }
  encryption_config {
    provider { key_arn = var.cluster_kms_key_arn }
    resources = ["secrets"]
  }
}
variable "cluster_kms_key_arn" { type = string }
resource "aws_eks_node_group" "this" {
  cluster_name = aws_eks_cluster.this.name
  node_group_name = "${var.name}-system"
  node_role_arn = var.node_role_arn
  subnet_ids = var.subnet_ids
  scaling_config { desired_size = 2; min_size = 2; max_size = 6 }
  instance_types = ["m6i.large"]
}
output "cluster_name" { value = aws_eks_cluster.this.name }
