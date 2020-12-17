resource "aws_apigatewayv2_api" "doves" {
  name                       = "doves-api"
  protocol_type              = "HTTP"
  target = aws_lambda_function.default.arn
}

//resource "aws_apigatewayv2_deployment" "example" {
//  api_id      = aws_apigatewayv2_api.doves.id
//  description = "live"
//
//  triggers = {
//    redeployment = sha1(join(",", list(
//      jsonencode(aws_apigatewayv2_integration.default),
//      jsonencode(aws_apigatewayv2_route.default),
//    )))
//  }
//
//  lifecycle {
//    create_before_destroy = true
//  }
//}


# This is to optionally manage the CloudWatch Log Group for the Lambda Function.
# If skipping this resource configuration, also add "logs:CreateLogGroup" to the IAM policy below.
resource "aws_cloudwatch_log_group" "default" {
  name              = "/aws/lambda/${aws_lambda_function.default.function_name}"
  retention_in_days = 14
}

# See also the following AWS managed policy: AWSLambdaBasicExecutionRole
resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.default_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}