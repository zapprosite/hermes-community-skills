"""Smoke tests para hermes-community-skills."""
import pytest
from pathlib import Path


def test_skills_dir_exists():
    """skills/ deve existir e ter community skills."""
    skills_dir = Path(__file__).parent.parent / "skills"
    assert skills_dir.exists()
    skills = [d for d in skills_dir.iterdir() if d.is_dir()]
    assert len(skills) >= 5, f"Esperado 5+ skills, encontrado {len(skills)}"


def test_categories():
    """Deve ter skills de browser, creative, github, research, mcp."""
    skills_dir = Path(__file__).parent.parent / "skills"
    categories = {d.name for d in skills_dir.iterdir() if d.is_dir()}
    expected = {"browser", "creative", "github", "research", "mcp"}
    missing = expected - categories
    assert not missing, f"Categorias faltando: {missing}"
