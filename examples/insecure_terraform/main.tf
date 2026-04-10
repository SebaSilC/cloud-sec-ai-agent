resource "aws_iam_policy" "bad_policy" {
  policy = jsonencode({
    Statement = [{
      Action   = "*"
      Effect   = "Allow"
      Resource = "*"
    }]
  })
}

resource "aws_security_group" "bad_sg" {
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "bad_bucket" {
  acl = "public-read"
}

variable "db_password" {
  default = "supersecret123"
}
