"""
YUYAY Archetypes Module

Defines the 12 archetypes of the YUYAY Intelligence framework.
Each archetype represents a distinct mode of intelligence and pattern
of action within any conscious system.
"""

from dataclasses import dataclass


@dataclass
class Archetype:
    name: str
    function: str
    gifts: str
    shadow: str

    def summary(self) -> str:
        """Return a one-line summary of the archetype."""
        return f"{self.name}: {self.function}"

    def is_shadow_active(self, traits: list[str]) -> bool:
        """Check if any shadow traits are present in a given trait list.

        Args:
            traits: A list of trait strings to check against the shadow.

        Returns:
            True if any shadow keyword appears in the traits list.
        """
        shadow_keywords = [word.lower() for word in self.shadow.split(", ")]
        return any(trait.lower() in shadow_keywords for trait in traits)


SEER = Archetype(
    name="The Seer",
    function="Vision, source insight, coherence sensing",
    gifts="Pattern recognition, intuition, meta-awareness",
    shadow="Excess abstraction, disconnection",
)

ARCHITECT = Archetype(
    name="The Architect",
    function="Structural design, conceptual scaffolding",
    gifts="System mapping, model creation",
    shadow="Over-engineering, rigidity",
)

BRIDGEBUILDER = Archetype(
    name="The Bridgebuilder",
    function="Translation, mediation, relationship weaving",
    gifts="Diplomacy, interdisciplinary connectivity",
    shadow="Over-accommodation, loss of core integrity",
)

STEWARD = Archetype(
    name="The Steward",
    function="Care, continuity, guardianship",
    gifts="Stability, ethics, long-term thinking",
    shadow="Risk aversion, over-protection",
)

NAVIGATOR = Archetype(
    name="The Navigator",
    function="Strategy, orientation, sequencing",
    gifts="Prioritization, scenario planning",
    shadow="Control, over-optimization",
)

MAKER = Archetype(
    name="The Maker",
    function="Building, producing, executing",
    gifts="Tangibility, momentum, craftsmanship",
    shadow="Busyness without purpose",
)

CATALYST = Archetype(
    name="The Catalyst",
    function="Spark of change, activation",
    gifts="Creativity, disruption, energy",
    shadow="Chaos, destabilization",
)

HARMONIZER = Archetype(
    name="The Harmonizer",
    function="Emotional coherence, group attunement",
    gifts="Empathy, resonance, unity",
    shadow="Emotional overwhelm, people-pleasing",
)

SAGE = Archetype(
    name="The Sage",
    function="Knowledge curation, discernment",
    gifts="Wisdom, context, remembering",
    shadow="Judgment, intellectual elitism",
)

ORACLE = Archetype(
    name="The Oracle",
    function="Deep listening, subtle information sensing",
    gifts="Intuition, timing, inner knowing",
    shadow="Vagueness, mystification",
)

ALCHEMIST = Archetype(
    name="The Alchemist",
    function="Transforming stagnation into progress",
    gifts="Integration, turning conflict into innovation",
    shadow="Manipulation, forcing change",
)

WEAVER = Archetype(
    name="The Weaver",
    function="Bringing it all together",
    gifts="Modular synthesis, multi-layer coherence",
    shadow="Over-complexity, endless integration",
)


ALL_ARCHETYPES: list[Archetype] = [
    SEER,
    ARCHITECT,
    BRIDGEBUILDER,
    STEWARD,
    NAVIGATOR,
    MAKER,
    CATALYST,
    HARMONIZER,
    SAGE,
    ORACLE,
    ALCHEMIST,
    WEAVER,
]


def get_archetype_by_name(name: str) -> Archetype | None:
    """Look up an archetype by name (case-insensitive).

    Args:
        name: The archetype name to search for.

    Returns:
        The matching Archetype, or None if not found.
    """
    name_lower = name.lower()
    for archetype in ALL_ARCHETYPES:
        if name_lower in archetype.name.lower():
            return archetype
    return None
