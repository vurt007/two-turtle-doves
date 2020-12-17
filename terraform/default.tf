
resource "aws_iam_role" "default_lambda" {
  name = "default-lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF

}

data "archive_file" "default" {
  type        = "zip"
  source_file = "${path.module}/files/default.py"
  output_path = "${path.module}/files/default.zip"
}

resource "aws_lambda_function" "default" {
  filename         = "${path.module}/files/default.zip"
  function_name    = "default"
  role             = aws_iam_role.default_lambda.arn
  handler          = "default.handler"
  runtime          = "python3.6"
  source_code_hash = data.archive_file.default.output_base64sha256

  depends_on = [data.archive_file.default]

//  environment {
//    variables = {
//    }
//  }
}


resource "aws_lambda_permission" "default" {
  statement_id = "AllowExecutionFromApiGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.default.function_name
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_apigatewayv2_api.doves.execution_arn}/*/*/*"

}


resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.doves.id
  route_key = "$default"
}


resource "aws_apigatewayv2_integration" "default" {
  api_id           = aws_apigatewayv2_api.doves.id
  integration_type = "AWS_PROXY"
  integration_method        = "POST"
  integration_uri           = aws_lambda_function.default.invoke_arn

}
