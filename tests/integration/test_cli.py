"""Integration tests for CLI."""

from unittest.mock import Mock, patch

from click.testing import CliRunner

from laodeng.cli.gen_image import main


class TestCliBasicInvocation:
    """Tests for basic CLI invocation."""

    def test_cli_with_prompt_success(self):
        """Test CLI with valid prompt returns success."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/generated.png"}]
        }

        with patch("requests.post", return_value=mock_response):
            with patch.dict("os.environ", {"T8STAR_TOKEN": "test-token"}):
                runner = CliRunner()
                result = runner.invoke(main, ["A sunset over mountains"])

                assert result.exit_code == 0
                assert "https://example.com/generated.png" in result.output

    def test_cli_without_prompt_fails(self):
        """Test CLI without prompt shows error."""
        runner = CliRunner()
        result = runner.invoke(main, [])

        assert result.exit_code != 0

    def test_cli_with_missing_token_fails(self):
        """Test CLI fails gracefully when token is missing."""
        with patch.dict("os.environ", {}, clear=True):
            import os

            os.environ.pop("T8STAR_TOKEN", None)

            runner = CliRunner()
            result = runner.invoke(main, ["A sunset"])

            assert result.exit_code == 3  # ERROR_AUTH
            assert "token" in result.output.lower()

    def test_cli_help_shows_usage(self):
        """Test CLI --help shows usage information."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "PROMPT" in result.output


class TestCliOptions:
    """Tests for CLI option parameters (User Story 2)."""

    def test_cli_with_size_option(self):
        """Test CLI with --size option passes size to provider."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/image.png"}]
        }

        with patch("requests.post", return_value=mock_response) as mock_post:
            with patch.dict("os.environ", {"T8STAR_TOKEN": "test-token"}):
                runner = CliRunner()
                result = runner.invoke(main, ["A sunset", "--size", "1024x1024"])

                assert result.exit_code == 0
                # Verify size was passed to API
                call_args = mock_post.call_args
                assert call_args[1]["json"]["size"] == "1024x1024"

    def test_cli_with_model_option(self):
        """Test CLI with --model option passes model to provider."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/image.png"}]
        }

        with patch("requests.post", return_value=mock_response) as mock_post:
            with patch.dict("os.environ", {"T8STAR_TOKEN": "test-token"}):
                runner = CliRunner()
                result = runner.invoke(main, ["A sunset", "--model", "custom-model"])

                assert result.exit_code == 0
                # Verify model was passed to API
                call_args = mock_post.call_args
                assert call_args[1]["json"]["model"] == "custom-model"

    def test_cli_with_timeout_option(self):
        """Test CLI with --timeout option passes timeout to request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/image.png"}]
        }

        with patch("requests.post", return_value=mock_response) as mock_post:
            with patch.dict("os.environ", {"T8STAR_TOKEN": "test-token"}):
                runner = CliRunner()
                result = runner.invoke(main, ["A sunset", "--timeout", "300"])

                assert result.exit_code == 0
                # Verify timeout was passed to requests
                call_args = mock_post.call_args
                assert call_args[1]["timeout"] == 300

    def test_cli_with_json_output(self):
        """Test CLI with --json flag outputs JSON format."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/image.png"}]
        }

        with patch("requests.post", return_value=mock_response):
            with patch.dict("os.environ", {"T8STAR_TOKEN": "test-token"}):
                runner = CliRunner()
                result = runner.invoke(main, ["A sunset", "--json"])

                assert result.exit_code == 0
                import json

                output = json.loads(result.output)
                assert output["success"] is True
                assert "urls" in output
                assert "https://example.com/image.png" in output["urls"]

    def test_cli_with_invalid_size_format(self):
        """Test CLI with invalid size format fails with validation error."""
        with patch.dict("os.environ", {"T8STAR_TOKEN": "test-token"}):
            runner = CliRunner()
            result = runner.invoke(main, ["A sunset", "--size", "invalid"])

            assert result.exit_code == 2  # EXIT_ERROR_INVALID_ARGS
            assert "invalid size format" in result.output.lower()

    def test_cli_with_all_options(self):
        """Test CLI with all options combined."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/image.png"}]
        }

        with patch("requests.post", return_value=mock_response) as mock_post:
            with patch.dict("os.environ", {"T8STAR_TOKEN": "test-token"}):
                runner = CliRunner()
                result = runner.invoke(
                    main,
                    [
                        "A sunset",
                        "--size",
                        "512x512",
                        "--model",
                        "test-model",
                        "--timeout",
                        "60",
                    ],
                )

                assert result.exit_code == 0
                call_args = mock_post.call_args
                assert call_args[1]["json"]["size"] == "512x512"
                assert call_args[1]["json"]["model"] == "test-model"
                assert call_args[1]["timeout"] == 60


class TestCliReferenceImage:
    """Tests for CLI with reference image URLs (User Story 3)."""

    def test_cli_with_reference_url_in_prompt(self):
        """Test CLI handles prompts containing reference URLs."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/generated.png"}]
        }

        prompt = "A person like this: https://example.com/ref.jpg in a sunset"

        with patch("requests.post", return_value=mock_response) as mock_post:
            with patch.dict("os.environ", {"T8STAR_TOKEN": "test-token"}):
                runner = CliRunner()
                result = runner.invoke(main, [prompt])

                assert result.exit_code == 0
                call_args = mock_post.call_args
                assert call_args[1]["json"]["prompt"] == prompt
