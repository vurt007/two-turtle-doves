resource "aws_apigatewayv2_api" "doves" {
  name                       = "doves-api"
  protocol_type              = "HTTP"
}
