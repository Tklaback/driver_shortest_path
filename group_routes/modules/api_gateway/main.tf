resource "aws_api_gateway_rest_api" "cluster-api" {
  name = "cluster-api"
}

resource "aws_api_gateway_resource" "cluster-api-resource" {
  parent_id   = aws_api_gateway_rest_api.cluster-api.root_resource_id
  path_part   = "api"
  rest_api_id = aws_api_gateway_rest_api.cluster-api.id
}

resource "aws_api_gateway_resource" "cluster-v1-resource" {
  parent_id   = aws_api_gateway_resource.cluster-api-resource.id
  path_part   = "v1"
  rest_api_id = aws_api_gateway_rest_api.cluster-api.id
}

resource "aws_api_gateway_resource" "proxy_plus" {
  rest_api_id = aws_api_gateway_rest_api.cluster-api.id
  parent_id   = aws_api_gateway_resource.cluster-v1-resource.id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "lambda_post" {
  authorization    = "NONE"
  http_method      = "ANY"
  resource_id      = aws_api_gateway_resource.proxy_plus.id
  rest_api_id      = aws_api_gateway_rest_api.cluster-api.id
  api_key_required = true
}

resource "aws_api_gateway_api_key" "cluster-api-key" {
  name     = "cluster-api-key"
}

resource "aws_api_gateway_deployment" "cluster-api-deployment" {
  rest_api_id = aws_api_gateway_rest_api.cluster-api.id
  depends_on = [
    aws_api_gateway_resource.proxy_plus,
    aws_api_gateway_integration.integration
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "cluster-api-stage" {
  deployment_id = aws_api_gateway_deployment.cluster-api-deployment.id
  rest_api_id   = aws_api_gateway_rest_api.cluster-api.id
  stage_name    = "prod"
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.cluster-api.id
  resource_id             = aws_api_gateway_resource.proxy_plus.id
  http_method             = aws_api_gateway_method.lambda_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda.lambda_function_invoke_arn
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda.lambda_function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "${aws_api_gateway_rest_api.esst_api.execution_arn}/*/*/*"
}

resource "aws_api_gateway_usage_plan" "esst_plan" {
  name         = "Unlimited"
  description  = "Plan for cluster api calls"

  api_stages {
    api_id = aws_api_gateway_rest_api.cluster-api.id
    stage  = aws_api_gateway_stage.cluster-api-stage.stage_name
  }
}

resource "aws_api_gateway_usage_plan_key" "main" {
  key_id        = aws_api_gateway_api_key.cluster-api-key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.esst_plan.id
}