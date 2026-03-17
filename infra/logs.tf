resource "aws_cloudwatch_log_group" "frontend" {
  name = "/ecs/${var.project_name}-frontend"
}

resource "aws_cloudwatch_log_group" "backend" {
  name = "/ecs/${var.project_name}-backend"
}
