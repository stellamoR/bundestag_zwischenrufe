"""Compact the deployment-only Space history before uploading fresh data."""

import os

from huggingface_hub import HfApi


SPACE_REPO = "stellamo/bundestag_stats"


def main() -> None:
    token = os.environ["HF_TOKEN"]
    HfApi(token=token).super_squash_history(
        repo_id=SPACE_REPO,
        repo_type="space",
        commit_message="Compact deployment history",
    )


if __name__ == "__main__":
    main()
