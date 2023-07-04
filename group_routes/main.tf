module "api_gateway" {
  source = "./modules/api_gateway"
  lambda = module.cluster_lambda.cluster-api-output
}

module "cluster_lambda" {
  source = "./modules/lambda"
}
