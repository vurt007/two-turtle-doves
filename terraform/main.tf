provider aws {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    profile = "hackday"
    bucket = "nhsd-turtle-doves-terraform"
    key    = "path/to/my/key"
    region = "us-east-1"
  }
}

//data "aws_iam_policy_document" "lambda_assume_role" {
//  statement {
//    actions = ["sts:AssumeRole"]
//    principals {
//      type        = "Service"
//      identifiers = ["lambda.amazonaws.com"]
//    }
//  }
//}