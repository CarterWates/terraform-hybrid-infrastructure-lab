from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / "infrastructure" / "terraform" / "environments" / "dev"


class TerraformFoundationTests(unittest.TestCase):
    def test_dev_environment_files_exist(self):
        expected = {
            "versions.tf",
            "providers.tf",
            "variables.tf",
            "locals.tf",
            "main.tf",
            "outputs.tf",
            "terraform.tfvars.example",
            "README.md",
        }

        actual = {path.name for path in DEV.iterdir() if path.is_file()}

        self.assertTrue(expected.issubset(actual))

    def test_s3_bucket_has_security_controls(self):
        main = (DEV / "main.tf").read_text()

        self.assertIn("aws_s3_bucket_public_access_block", main)
        self.assertIn("block_public_acls", main)
        self.assertIn("block_public_policy", main)
        self.assertIn("ignore_public_acls", main)
        self.assertIn("restrict_public_buckets", main)
        self.assertIn("aws_s3_bucket_server_side_encryption_configuration", main)
        self.assertIn("aws_s3_bucket_versioning", main)
        self.assertIn("force_destroy = var.backup_bucket_force_destroy", main)
        self.assertIn("expiration {", main)
        self.assertIn("days = var.backup_lifecycle_expiration_days", main)

    def test_dynamodb_table_has_expected_keys_and_recovery(self):
        main = (DEV / "main.tf").read_text()

        self.assertRegex(main, re.compile(r'hash_key\s+=\s+"nodeId"'))
        self.assertRegex(main, re.compile(r'range_key\s+=\s+"timestamp"'))
        self.assertIn("billing_mode = \"PAY_PER_REQUEST\"", main)
        self.assertIn("point_in_time_recovery", main)
        self.assertIn("server_side_encryption", main)

    def test_alerting_and_log_groups_exist(self):
        main = (DEV / "main.tf").read_text()

        self.assertIn("aws_sns_topic", main)
        self.assertIn("aws_sns_topic_subscription", main)
        self.assertIn("aws_cloudwatch_log_group", main)
        self.assertIn("/aws/lambda/hybrid-lab-health-api", main)
        self.assertIn("/hybrid-lab/monitoring-jobs", main)

    def test_variables_have_validation_blocks(self):
        variables = (DEV / "variables.tf").read_text()

        self.assertIn("validation {", variables)
        self.assertIn("var.aws_region", variables)
        self.assertIn("var.environment", variables)
        self.assertIn("var.log_retention_days", variables)

    def test_no_real_tfvars_or_state_files_are_tracked(self):
        tracked_sensitive = [
            path
            for path in ROOT.rglob("*")
            if ".git" not in path.parts
            and path.is_file()
            and (path.name.endswith(".tfvars") or ".tfstate" in path.name)
            and path.name != "terraform.tfvars.example"
        ]

        self.assertEqual(tracked_sensitive, [])


if __name__ == "__main__":
    unittest.main()
