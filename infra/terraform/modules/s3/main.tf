variable "name" { type = string }
variable "kms_key_arn" { type = string }
resource "aws_s3_bucket" "documents" { bucket = "${var.name}-documents" }
resource "aws_s3_bucket_public_access_block" "documents" {
  bucket = aws_s3_bucket.documents.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_server_side_encryption_configuration" "documents" {
  bucket = aws_s3_bucket.documents.id
  rule { apply_server_side_encryption_by_default { sse_algorithm = "aws:kms"; kms_master_key_id = var.kms_key_arn } }
}
