"""Tests for the YUYAY archetypes module."""

from yuyay.archetypes import ALL_ARCHETYPES, SEER, Archetype, get_archetype_by_name


class TestArchetype:
    """Tests for the Archetype dataclass."""

    def test_archetype_has_correct_fields(self) -> None:
        """Test that an Archetype instance has all required fields."""
        assert SEER.name == "The Seer"
        assert SEER.function == "Vision, source insight, coherence sensing"
        assert SEER.gifts == "Pattern recognition, intuition, meta-awareness"
        assert SEER.shadow == "Excess abstraction, disconnection"

    def test_summary_returns_correct_format(self) -> None:
        """Test that summary returns name and function joined by colon."""
        result = SEER.summary()
        assert result == "The Seer: Vision, source insight, coherence sensing"

    def test_is_shadow_active_returns_true_when_shadow_present(self) -> None:
        """Test that is_shadow_active returns True when a shadow trait is present."""
        assert SEER.is_shadow_active(["disconnection"]) is True

    def test_is_shadow_active_returns_false_when_no_shadow_present(self) -> None:
        """Test that is_shadow_active returns False when no shadow traits present."""
        assert SEER.is_shadow_active(["creativity", "empathy"]) is False

    def test_is_shadow_active_case_insensitive(self) -> None:
        """Test that is_shadow_active works regardless of case."""
        assert SEER.is_shadow_active(["DISCONNECTION"]) is True


class TestAllArchetypes:
    """Tests for the ALL_ARCHETYPES registry and lookup function."""

    def test_all_archetypes_has_twelve_items(self) -> None:
        """Test that ALL_ARCHETYPES contains exactly 12 archetypes."""
        assert len(ALL_ARCHETYPES) == 12

    def test_all_archetypes_are_archetype_instances(self) -> None:
        """Test that every item in ALL_ARCHETYPES is an Archetype instance."""
        for archetype in ALL_ARCHETYPES:
            assert isinstance(archetype, Archetype)

    def test_get_archetype_by_name_returns_correct_archetype(self) -> None:
        """Test that searching by name returns the correct archetype."""
        result = get_archetype_by_name("seer")
        assert result == SEER

    def test_get_archetype_by_name_returns_none_for_unknown(self) -> None:
        """Test that searching for unknown name returns None."""
        result = get_archetype_by_name("unknown")
        assert result is None

    def test_get_archetype_by_name_case_insensitive(self) -> None:
        """Test that name lookup works regardless of case."""
        assert get_archetype_by_name("SEER") == SEER
        assert get_archetype_by_name("Seer") == SEER
        assert get_archetype_by_name("seer") == SEER
