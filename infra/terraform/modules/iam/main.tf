variable "name" { type = string }
data "aws_iam_policy_document" "eks_assume" {
  statement { actions=["sts:AssumeRole"]; principals { type="Service"; identifiers=["eks.amazonaws.com"] } }
}
resource "aws_iam_role" "eks_cluster" { name="${var.name}-eks-cluster"; assume_role_policy=data.aws_iam_policy_document.eks_assume.json }
resource "aws_iam_role_policy_attachment" "eks_cluster" { role=aws_iam_role.eks_cluster.name; policy_arn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy" }
data "aws_iam_policy_document" "ec2_assume" {
  statement { actions=["sts:AssumeRole"]; principals { type="Service"; identifiers=["ec2.amazonaws.com"] } }
}
resource "aws_iam_role" "eks_nodes" { name="${var.name}-eks-nodes"; assume_role_policy=data.aws_iam_policy_document.ec2_assume.json }
resource "aws_iam_role_policy_attachment" "node_worker" { role=aws_iam_role.eks_nodes.name; policy_arn="arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy" }
resource "aws_iam_role_policy_attachment" "node_ecr" { role=aws_iam_role.eks_nodes.name; policy_arn="arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly" }
resource "aws_iam_role_policy_attachment" "node_cni" { role=aws_iam_role.eks_nodes.name; policy_arn="arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy" }
output "cluster_role_arn" { value=aws_iam_role.eks_cluster.arn }
output "node_role_arn" { value=aws_iam_role.eks_nodes.arn }
