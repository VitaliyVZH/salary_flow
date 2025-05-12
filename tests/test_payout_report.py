from src.core.cli import CommandLineParser


def test_cli_parser():
    parser = CommandLineParser()
    args = parser.parse(["file1.csv", "--report", "payout"])

    assert args.files == ["file1.csv"]
    assert args.report == "payout"
