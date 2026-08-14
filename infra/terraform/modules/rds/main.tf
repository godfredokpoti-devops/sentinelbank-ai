variable "name" { type = string }
variable "subnet_ids" { type = list(string) }
variable "security_group_ids" { type = list(string) }
variable "kms_key_arn" { type = string }
variable "username" { type = string; default = "sentineladmin" }
resource "aws_db_subnet_group" "this" { name = var.name; subnet_ids = var.subnet_ids }
resource "aws_db_instance" "this" {
  identifier = var.name
  engine = "postgres"
  instance_class = "db.t4g.medium"
  allocated_storage = 50
  max_allocated_storage = 200
  db_name = "sentinelbank"
  username = var.username
  manage_master_user_password = true
  db_subnet_group_name = aws_db_subnet_group.this.name
  vpc_security_group_ids = var.security_group_ids
  storage_encrypted = true
  kms_key_id = var.kms_key_arn
  backup_retention_period = 7
  deletion_protection = true
  skip_final_snapshot = false
}
output "endpoint" { value = aws_db_instance.this.endpoint }
