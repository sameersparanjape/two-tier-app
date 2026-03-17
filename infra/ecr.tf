resource "aws_ecr_repository" "frontend" {
  name         = "${var.project_name}-frontend"
  force_delete = true
}

resource "aws_ecr_repository" "backend" {
  name         = "${var.project_name}-backend"
  force_delete = true
}
