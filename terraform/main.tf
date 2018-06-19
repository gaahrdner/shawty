variable "aws_access_key" {
  default = ""
}

variable "aws_secret_key" {
  default = ""
}

variable "region" {
  default = "us-west-2"
}

provider "aws" {
  region                  = "${var.region}"
  shared_credentials_file = "~/.aws/credentials"
}

resource "aws_dynamodb_table" "shawty_test" {
  name = "shawty_test"

  read_capacity  = 20
  write_capacity = 20
  stream_enabled = false

  hash_key = "short_url"

  attribute {
    name = "short_url"
    type = "S"
  }
}
