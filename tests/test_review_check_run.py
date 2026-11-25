import subprocess
import pathlib
import unittest

class CheckRunTests(unittest.TestCase):
    def test_repeated_evaluations_update_existing_check(self):
        script = pathlib.Path("scripts/review_check_run.sh").read_text()
        shell = r'''
set -euo pipefail
export GITHUB_REPOSITORY=owner/repo
gh() {
  if [[ "$*" == *"/commits/"* ]]; then
    printf '[{"check_runs":[{"name":"review-policy","app":{"slug":"github-actions"},"external_id":"ai-frontier-review-policy-v1","id":42}]}]'
  elif [[ "$*" == *"--method PATCH"*"/check-runs/42"* ]]; then
    echo PATCH >&2
  else
    return 99
  fi
}
for i in {1..5}; do
  set_check aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa in_progress
  set_check aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa completed success
done
'''
        result = subprocess.run(["bash", "-c", script + "\n" + shell], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr.count("PATCH"), 10)
