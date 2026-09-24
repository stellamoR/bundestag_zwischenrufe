"""Launch the shared Bundestag dashboard in compact embed-only mode."""

import os

os.environ["BUNDESTAG_EMBED_ONLY"] = "1"

from app import demo  # noqa: E402, F401
