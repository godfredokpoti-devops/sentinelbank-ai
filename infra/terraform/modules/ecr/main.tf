variable "name" { type = string }
resource "aws_ecr_repository" "api" {
  name = "${var.name}-api"
  image_scanning_configuration { scan_on_push = true }
  encryption_configuration { encryption_type = "AES256" }
}
output "repository_url" { value = aws_ecr_repository.api.repository_url }
