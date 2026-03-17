output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "ecr_frontend_uri" {
  value = aws_ecr_repository.frontend.repository_url
}

output "ecr_backend_uri" {
  value = aws_ecr_repository.backend.repository_url
}
