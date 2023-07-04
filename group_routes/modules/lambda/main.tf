module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name            = local.function_name
  create_package           = true
  description              = "My awesome lambda function"
  handler                  = "main.handler"
  runtime                  = "python3.9"
  attach_policy_statements = false
  timeout                  = 180


  layers = [
    module.lambda_layer.lambda_layer_arn,
    module.lambda_layer_2.lambda_layer_arn
  ]

  source_path = "src/code"

}

module "lambda_layer" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "lambda-layer"
  description         = "My amazing lambda layer"
  compatible_runtimes = ["python3.9"]

  source_path = "src/dependencies"
}

module "lambda_layer_2" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "lambda-layer-2"
  description         = "My amazing lambda layer"
  compatible_runtimes = ["python3.9"]

  source_path = "src/large_dependencies"
}