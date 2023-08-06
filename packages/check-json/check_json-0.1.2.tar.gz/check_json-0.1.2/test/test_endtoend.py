"""
End-to-end test for check_json
"""
import subprocess

import pytest  # type:ignore


JSON = """
{
"name": "firstname lastname",
"description": "somedescription",
"email": "name@domain.tld"
}
"""
JSON_FILENAME = "input.json"


@pytest.mark.endtoend
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            # OK
            [
                "--filter",
                "select(.name)",
                "--",
            ],
            {
                "returncode": 0,
                "output": "JSONFILE OK - filter0 is 1 | filter0=1;@0",
            },
        ),
        (
            # OK with named filter for perfdata
            [
                "--filter",
                "select(.name) # filter-name",
                "--",
            ],
            {
                "returncode": 0,
                "output": "JSONFILE OK - filter-name is 1 | 'filter-name'=1;@0",
            },
        ),
        (
            # WARN
            [
                "--filter",
                "select(.missingkey)",
                "--",
            ],
            {
                "returncode": 1,
                "output": (
                    "JSONFILE WARNING - filter0 is 0 (outside range @0:0) | "
                    "filter0=0;@0"
                ),
            },
        ),
        (
            # CRIT
            [
                "--filter",
                "select(.missingkey)",
                "--fail-status",
                "critical",
                "--",
            ],
            {
                "returncode": 2,
                "output": (
                    "JSONFILE CRITICAL - filter0 is 0 (outside range @0:0) | "
                    "filter0=0;;@0"
                ),
            },
        ),
    ],
)
def test_end_to_end(test_input, expected, tmp_path):
    """Test"""
    filepath = tmp_path / JSON_FILENAME
    filepath.write_text(JSON)
    command = ["python3", "-m", "check_json"] + test_input + [str(filepath)]
    res = subprocess.run(command, capture_output=True, check=False, text=True)
    assert res.returncode == expected["returncode"]
    assert res.stdout.strip() == expected["output"]
