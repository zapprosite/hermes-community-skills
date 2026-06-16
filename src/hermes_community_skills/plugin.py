"""CommunitySkillsPlugin: hermes-community-skills para hermes-agent."""
from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger("hermes-community-skills")


class CommunitySkillsPlugin:
    """Plugin standalone."""
    name = "hermes-community-skills"
    kind = "standalone"
    version = "1.0.0"

    def register(self, ctx) -> None:
        """Hook de registro."""
        # Tools
        ctx.register_tool("hermes_community_skills_status", self._tool_status)

        # Skills
        skill_path = self._skill_path()
        if skill_path.exists():
            ctx.register_skill("hermes-community-skills", skill_path)

        log.info("hermes-community-skills v%s registrado", self.version)

    def _skill_path(self) -> Path:
        return Path(__file__).parent.parent.parent / "skills" / "community-skills"

    def _tool_status(self, **_):
        return {"status": "ready", "version": self.version}
