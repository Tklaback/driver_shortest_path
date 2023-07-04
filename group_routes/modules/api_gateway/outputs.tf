output "api_gateway_id" {
  description = "ID of the API Gateway"
  value       = aws_api_gateway_rest_api.cluster-api.id
}

output "api_gateway_execution_arn" {
  description = "value of arn for api gateway"
  value       = aws_api_gateway_rest_api.cluster-api.execution_arn
}