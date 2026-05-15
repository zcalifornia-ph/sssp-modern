from __future__ import annotations

from bench.datasets import (
    DEFAULT_DATASET_SEED,
    DatasetProfile,
    build_dataset_graph,
    dataset_cache_path,
    dataset_fingerprint,
    dataset_profiles,
    ensure_dataset,
)
from sssp.io import read_edge_list


def test_dataset_profiles_cover_required_matrix() -> None:
    profiles = dataset_profiles()

    assert len(profiles) == 30
    assert {profile.size_label for profile in profiles} == {"small", "medium", "large"}
    assert {profile.density_label for profile in profiles} == {"sparse", "dense"}
    assert {profile.generator for profile in profiles} == {
        "erdos-renyi",
        "geometric",
        "dag",
        "barabasi-albert",
        "signed-dag",
    }
    assert [profile.name for profile in profiles] == sorted(
        [profile.name for profile in profiles],
        key=_expected_profile_sort_key,
    )


def test_dataset_fingerprint_is_deterministic_for_same_profile_and_seed() -> None:
    profile = _profile("erdos-renyi", "medium", "sparse")

    first = build_dataset_graph(profile, DEFAULT_DATASET_SEED)
    second = build_dataset_graph(profile, DEFAULT_DATASET_SEED)

    assert dataset_fingerprint(first) == dataset_fingerprint(second)
    assert first.order() == profile.order
    assert first.size() == second.size()


def test_ensure_dataset_reloads_cached_graph_with_same_fingerprint(tmp_path) -> None:
    profile = _profile("dag", "small", "dense")

    created = ensure_dataset(profile, seed=11, root=tmp_path)
    reloaded = ensure_dataset(profile, seed=11, root=tmp_path)
    graph = read_edge_list(created.path)

    assert created.path == reloaded.path
    assert created.path.is_file()
    assert created.fingerprint == reloaded.fingerprint
    assert dataset_fingerprint(graph) == created.fingerprint
    assert created.order == profile.order
    assert created.edge_count == graph.size()


def test_signed_dag_profiles_record_bellman_ford_only_negative_compatibility() -> None:
    signed_profiles = [
        profile for profile in dataset_profiles() if profile.generator == "signed-dag"
    ]

    assert signed_profiles
    for profile in signed_profiles:
        graph = build_dataset_graph(profile, seed=DEFAULT_DATASET_SEED)
        assert profile.allows_negative_weights
        assert profile.compatible_algorithms == ("bellman-ford",)
        assert any(edge.weight < 0 for edge in graph.edges())


def test_dataset_cache_paths_are_stable_and_safe(tmp_path) -> None:
    profile = _profile("barabasi-albert", "large", "dense")

    first = dataset_cache_path(profile, seed=DEFAULT_DATASET_SEED, root=tmp_path)
    second = dataset_cache_path(profile, seed=DEFAULT_DATASET_SEED, root=tmp_path)

    assert first == second
    assert first.name == "barabasi-albert-large-dense-seed-2026.edge-list.json"
    assert first.parent == tmp_path


def test_build_dataset_graph_uses_profile_source_vertex() -> None:
    for profile in dataset_profiles():
        graph = build_dataset_graph(profile, seed=DEFAULT_DATASET_SEED)
        assert profile.source == "v0"
        assert profile.source in set(graph.vertices())


def _profile(generator: str, size_label: str, density_label: str) -> DatasetProfile:
    for profile in dataset_profiles():
        if (
            profile.generator == generator
            and profile.size_label == size_label
            and profile.density_label == density_label
        ):
            return profile
    raise AssertionError("profile not found")


def _expected_profile_sort_key(name: str) -> tuple[int, int, int]:
    generators = {
        "erdos-renyi": 0,
        "geometric": 1,
        "dag": 2,
        "barabasi-albert": 3,
        "signed-dag": 4,
    }
    sizes = {"small": 0, "medium": 1, "large": 2}
    densities = {"sparse": 0, "dense": 1}
    generator, size, density = name.rsplit("-", 2)
    return (generators[generator], sizes[size], densities[density])
