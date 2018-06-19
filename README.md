# shawty

An HTTP-based RESTful API for managing short URLS.

It consists of a DynamoDB backend that stores the short URL and long URL mappings, and the server is an AWS Lambda job written in Python and deployed with Zappa. This should allow it to scale up quickly and automatically based on heavy usage.

# Requirements

* Python 3.6.6
* AWS credentials
* Terraform
* [zappa](https://github.com/Miserlou/Zappa)

# Deploying

1. Ensure you have AWS credentials with proper access in `~/.aws/credentials`
2. `cd` into the `terraform` directory and run `terraform init` to install the AWS provider
3. Run `terraform plan` and then `terraform apply` to provision the DynamoDB table:
```
(shawty) ~/C/s/terraform ❯❯❯ terraform apply                                                                                                                                                                                                ⏎

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  + aws_dynamodb_table.shawty_test
      id:                        <computed>
      arn:                       <computed>
      attribute.#:               "1"
      attribute.3330311623.name: "short_url"
      attribute.3330311623.type: "S"
      hash_key:                  "short_url"
      name:                      "shawty_test"
      point_in_time_recovery.#:  <computed>
      read_capacity:             "20"
      server_side_encryption.#:  <computed>
      stream_arn:                <computed>
      stream_enabled:            "false"
      stream_label:              <computed>
      stream_view_type:          <computed>
      write_capacity:            "20"


Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_dynamodb_table.shawty_test: Creating...
  arn:                       "" => "<computed>"
  attribute.#:               "" => "1"
  attribute.3330311623.name: "" => "short_url"
  attribute.3330311623.type: "" => "S"
  hash_key:                  "" => "short_url"
  name:                      "" => "shawty_test"
  point_in_time_recovery.#:  "" => "<computed>"
  read_capacity:             "" => "20"
  server_side_encryption.#:  "" => "<computed>"
  stream_arn:                "" => "<computed>"
  stream_enabled:            "" => "false"
  stream_label:              "" => "<computed>"
  stream_view_type:          "" => "<computed>"
  write_capacity:            "" => "20"
aws_dynamodb_table.shawty_test: Still creating... (10s elapsed)
aws_dynamodb_table.shawty_test: Creation complete after 11s (ID: shawty_test)

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```
4. Run `zappa deploy dev` which will package, upload, and deploy the Lambda function.
```
(shawty) ~/C/shawty ❯❯❯ zappa deploy dev
Calling deploy for stage dev..
Warning! Your project and virtualenv have the same name! You may want to re-create your venv with a new name, or explicitly define a 'project_name', as this may cause errors.
Downloading and installing dependencies..
 - lazy-object-proxy==1.3.1: Using locally cached manylinux wheel
 - sqlite==python36: Using precompiled lambda package
Packaging project as zip.
Uploading shawty-dev-1529368815.zip (26.1MiB)..
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 27.3M/27.3M [00:13<00:00, 1.36MB/s]
Scheduling..
Scheduled shawty-dev-zappa-keep-warm-handler.keep_warm_callback with expression rate(4 minutes)!
Uploading shawty-dev-template-1529368846.json (1.6KiB)..
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.60K/1.60K [00:00<00:00, 8.21KB/s]
Waiting for stack shawty-dev to create (this can take a bit)..
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:09<00:00,  2.79s/res]
Deploying API Gateway..
Deployment complete!: https://8towom9km4.execute-api.us-west-2.amazonaws.com/dev
```
5. Rejoice

You can also run this locally, just run the terraform task, install the pip requirements via `pip install -r requirements.txt`, and then start the application via `flask run`.

# Usage

To create a new short URL, post a JSON document with the `url` key:

```
(shawty) ~/C/shawty ❯❯❯ cat test_url.json
{
  "url": "http://google.com"
}
(shawty) ~/C/shawty ❯❯❯ curl -H "Content-Type: application/json" -X POST https://8towom9km4.execute-api.us-west-2.amazonaws.com/dev/ -d @test_url.json
{"short_url":"p2vJCgBN"}
```

Performing a `GET` request to the short URL will cause you to 302 redirect to the mapped long URL.