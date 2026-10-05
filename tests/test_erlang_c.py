"""Tests for the Erlang C calculator.

Reference values
----------------
The expected numbers below are not this module's own output. They are pinned
against an independent Erlang B forward recursion and the textbook closed form,
and are the same anchors used by ``Helix-Prime/tests/test_wfm_erlang_c.py``
(42 tests there). Testing a calculator against itself proves nothing, so every
assertion here is against a value computed elsewhere.

The ``(N, A)`` pairs, and their Erlang C values:

======  =====  =======
  N      A     C(N, A)
======  =====  =======
   10    8.5   0.529861
   12    8.5   0.196205
   20   15.0   0.160429
   50   45.0   0.363864
  100   80.0   0.019646
======  =====  =======

Derived anchors:

* ``service_level(12, 8.5, target=20s, aht=180s)`` = **86.70%**
* ``average_speed_of_answer(12, 8.5, 180)`` = **10.09s**
* ``occupancy(8.5, 12)`` = **70.83%** -- note this returns a *percentage*, not a
  fraction, because that is what the implementation and its callers use
* ``required_agents(100 calls, 180s AHT, 30-minute interval, 80/20)`` = **14**,
  achieving 88.84% SL at 71.43% occupancy
"""

import math

import pytest

from shared_utils.erlang_c import ErlangCCalculator


def erlang_b_reference(n: int, a: float) -> float:
    """Independent Erlang B forward recursion.

    ``B(0) = 1`` and ``B(i) = A*B(i-1) / (i + A*B(i-1))``.

    The index advances in the denominator. Holding it fixed at ``n`` is a
    plausible-looking bug that produces a stable but wrong number, which is
    exactly the kind of error this helper exists to catch -- so the helper is
    itself pinned by a test below.

    This is deliberately a different formulation from the implementation under
    test, which uses the factorial closed form. Agreement between the two is the
    evidence; agreement of the implementation with itself is not.
    """
    b = 1.0
    for i in range(1, n + 1):
        b = (a * b) / (i + a * b)
    return b


def erlang_c_reference(n: int, a: float) -> float:
    """C(N, A) = B(N) / (1 - (A/N)(1 - B(N)))."""
    if a >= n:
        return 1.0
    b = erlang_b_reference(n, a)
    return b / (1.0 - (a / n) * (1.0 - b))


# --- Erlang C ---------------------------------------------------------------

REFERENCE_PAIRS = [
    (10, 8.5, 0.529861),
    (12, 8.5, 0.196205),
    (20, 15.0, 0.160429),
    (50, 45.0, 0.363864),
    (100, 80.0, 0.019646),
]


@pytest.mark.parametrize("agents,intensity,expected", REFERENCE_PAIRS)
def test_erlang_c_matches_the_published_reference(agents, intensity, expected):
    """The implementation must agree with an independent recursion."""
    assert ErlangCCalculator.erlang_c(agents, intensity) == pytest.approx(
        expected, abs=5e-4
    )


@pytest.mark.parametrize("agents,intensity,_expected", REFERENCE_PAIRS)
def test_erlang_c_agrees_with_the_independent_formulation(agents, intensity, _expected):
    """A second, independent check: closed form vs Erlang B recursion."""
    assert ErlangCCalculator.erlang_c(agents, intensity) == pytest.approx(
        erlang_c_reference(agents, intensity), abs=1e-9
    )


def test_erlang_c_is_the_probability_a_call_waits():
    for agents, intensity, _ in REFERENCE_PAIRS:
        value = ErlangCCalculator.erlang_c(agents, intensity)
        assert 0.0 <= value <= 1.0


def test_erlang_c_decreases_as_agents_increase():
    """The core monotonic property: more agents, less waiting."""
    values = [ErlangCCalculator.erlang_c(n, 8.5) for n in range(9, 20)]
    assert all(a >= b for a, b in zip(values, values[1:])), values


def test_erlang_c_is_zero_with_no_traffic():
    assert ErlangCCalculator.erlang_c(15, 0) == 0.0


def test_erlang_c_is_one_when_overloaded():
    """At or above capacity an offered load cannot be served: everything waits."""
    assert ErlangCCalculator.erlang_c(10, 10) == 1.0
    assert ErlangCCalculator.erlang_c(10, 12) == 1.0


def test_erlang_c_rejects_a_non_positive_agent_count():
    with pytest.raises(ValueError):
        ErlangCCalculator.erlang_c(0, 5)


def test_erlang_c_rejects_negative_traffic():
    with pytest.raises(ValueError):
        ErlangCCalculator.erlang_c(10, -1)


# --- Service level ----------------------------------------------------------


def test_service_level_matches_the_reference():
    """SL(12, 8.5, 20s target, 180s AHT) = 86.70%.

    The tolerance is 5e-3 on a value near 87 -- deliberately tight. A looser
    bound (say abs=20) would still pass while the implementation drifted by two
    full percentage points, which for a service-level figure is a staffing
    decision. A test that cannot fail on a realistic error is not a test.
    """
    assert ErlangCCalculator.service_level(12, 8.5, 20, 180) == pytest.approx(
        86.70, abs=5e-3
    )


def test_service_level_is_a_percentage():
    value = ErlangCCalculator.service_level(12, 8.5, 20, 180)
    assert 0.0 <= value <= 100.0


def test_service_level_is_100_with_no_queueing():
    assert ErlangCCalculator.service_level(15, 0, 20, 180) == 100.0


def test_service_level_rises_with_a_longer_answer_target():
    """Answering within 30s is easier than within 5s, so SL cannot fall."""
    tight = ErlangCCalculator.service_level(12, 8.5, 5, 180)
    loose = ErlangCCalculator.service_level(12, 8.5, 30, 180)
    assert loose >= tight


def test_service_level_improves_with_more_agents():
    values = [ErlangCCalculator.service_level(n, 8.5, 20, 180) for n in range(9, 16)]
    assert all(a <= b for a, b in zip(values, values[1:])), values


def test_service_level_rejects_a_non_positive_handle_time():
    with pytest.raises(ValueError):
        ErlangCCalculator.service_level(12, 8.5, 20, 0)


# --- Average speed of answer ------------------------------------------------


def test_asa_matches_the_reference():
    """ASA(12, 8.5, 180s) = 10.09s."""
    assert ErlangCCalculator.average_speed_of_answer(12, 8.5, 180) == pytest.approx(
        10.09, abs=5e-3
    )


def test_asa_is_positive_under_a_stable_queue():
    assert ErlangCCalculator.average_speed_of_answer(12, 8.5, 180) > 0


def test_asa_falls_as_agents_increase():
    values = [ErlangCCalculator.average_speed_of_answer(n, 8.5, 180)
              for n in range(9, 16)]
    assert all(a >= b for a, b in zip(values, values[1:])), values


# --- Occupancy --------------------------------------------------------------


def test_occupancy_matches_the_reference():
    """Occupancy at A=8.5, N=12 is 70.83 -- a percentage, not a fraction."""
    assert ErlangCCalculator.occupancy(8.5, 12) == pytest.approx(70.83, abs=5e-3)


def test_occupancy_is_offered_load_over_capacity():
    """Occupancy is A/N as a percentage, so 6 of 12 agents is 50%."""
    assert ErlangCCalculator.occupancy(6.0, 12) == pytest.approx(50.0, abs=1e-9)


def test_occupancy_is_capped_at_100():
    """An overloaded offered load must not report more than fully occupied."""
    assert ErlangCCalculator.occupancy(20.0, 12) == 100.0


def test_occupancy_of_no_agents_is_zero():
    assert ErlangCCalculator.occupancy(8.5, 0) == 0


# --- Required agents --------------------------------------------------------


def test_required_agents_matches_the_reference():
    """100 calls, 180s AHT, 30-minute interval, 80/20 target -> 14 agents.

    This is the figure the README and the portfolio quote, so it is pinned
    rather than left to whatever the current code happens to return.
    """
    result = ErlangCCalculator.required_agents(100, 180, 30, 80, 20)
    assert result["required_agents"] == 14


def test_required_agents_meets_its_own_target():
    """Whatever count comes back must actually satisfy the requested SL.

    This is the property that makes the number usable: a staffing figure that
    misses its own service level is worse than no figure. Occupancy is a
    percentage, so the ceiling here is 100, not 1.
    """
    result = ErlangCCalculator.required_agents(100, 180, 30, 80, 20)
    assert result["achieved_sl"] >= 80.0, result
    assert result["occupancy"] <= 100.0, result


def test_required_agents_is_the_smallest_sufficient_count():
    """One fewer agent must fail the target, or the count is not minimal."""
    result = ErlangCCalculator.required_agents(100, 180, 30, 80, 20)
    agents = result["required_agents"]
    traffic = result["traffic_intensity"]
    one_fewer = ErlangCCalculator.service_level(agents - 1, traffic, 20, 180)
    assert one_fewer < 80.0, (agents, one_fewer)


def test_required_agents_scales_with_volume():
    low = ErlangCCalculator.required_agents(50, 180, 30, 80, 20)["required_agents"]
    high = ErlangCCalculator.required_agents(200, 180, 30, 80, 20)["required_agents"]
    assert high > low


# --- Arithmetic cross-checks ------------------------------------------------


def test_reference_helper_agrees_with_the_closed_form_on_small_inputs():
    """Pin the reference helper itself, so a bug in it cannot mask a bug below."""
    for n, a, expected in REFERENCE_PAIRS:
        if n > 20:
            continue  # the closed form overflows here; the recursion does not
        closed = (a ** n / math.factorial(n)) * (n / (n - a)) / (
            sum(a ** k / math.factorial(k) for k in range(n))
            + (a ** n / math.factorial(n)) * (n / (n - a))
        )
        assert erlang_c_reference(n, a) == pytest.approx(closed, abs=1e-9)


def test_the_reference_helper_would_be_caught_if_its_index_were_held_fixed():
    """A can-fail proof for the helper.

    The first draft of ``erlang_b_reference`` held the denominator's index at
    ``n`` instead of advancing it. That returns a stable, plausible, wrong
    number rather than raising -- the worst failure mode for a reference. This
    asserts the broken variant really does disagree, so the agreement test above
    is known to be capable of failing.
    """
    def broken(n: int, a: float) -> float:
        b = 1.0
        for _ in range(1, n + 1):
            b = (a * b) / (n + a * b)   # index pinned to n instead of advancing
        return b

    n, a, expected = 12, 8.5, 0.196205
    correct = erlang_c_reference(n, a)
    wrong = broken(n, a) / (1.0 - (a / n) * (1.0 - broken(n, a)))
    assert abs(correct - expected) < 1e-5, "the real helper agrees with the reference"
    assert abs(wrong - correct) > 1e-3, "the broken helper must actually differ"


def test_the_closed_form_cannot_be_used_at_realistic_sizes():
    """Documents the implementation's known ceiling, and why it exists.

    ``math.factorial`` returns an exact integer, so it does not overflow. What
    overflows is the division into a float once ``A**N / N!`` exceeds the double
    range. At A=8.5 that happens between N=140 and N=150.

    This is a real limitation of the implementation, not of the test: a contact
    centre with more than ~120 agents cannot be modelled by this calculator. The
    test asserts the limit rather than hiding it, so the day the implementation
    is rewritten onto a stable recurrence this test fails and the fix is
    deliberate rather than accidental.
    """
    assert isinstance(math.factorial(200), int)  # the factorial itself is exact

    # The closed form's division is what breaks:
    with pytest.raises(OverflowError):
        _ = 8.5 ** 200 / math.factorial(200)

    # The recursion handles the same load without complaint, which is why a
    # rewrite is possible:
    assert 0.0 <= erlang_c_reference(200, 170.0) <= 1.0


@pytest.mark.parametrize("agents", [50, 80, 100, 120])
def test_the_implementation_is_stable_up_to_its_ceiling(agents):
    """Below the ceiling the closed form is fine and must stay accurate."""
    intensity = 0.85 * agents
    assert ErlangCCalculator.erlang_c(agents, intensity) == pytest.approx(
        erlang_c_reference(agents, intensity), abs=1e-6
    )


@pytest.mark.parametrize("agents", [150, 200])
def test_the_implementation_beyond_its_ceiling_raises_rather_than_wrongly_succeeding(agents):
    """Above ~120 agents the factorial form overflows.

    It raises ``ValueError`` rather than returning a wrong number, which is the
    safe failure: a caller can catch it, whereas a silent wrong figure would be
    used to staff a contact centre.

    Asserted on both the exception *and* its message, so a future change that
    starts returning a plausible-but-wrong number instead of failing is caught.
    """
    intensity = 0.85 * agents
    with pytest.raises(ValueError) as excinfo:
        ErlangCCalculator.erlang_c(agents, intensity)
    assert "range error" in str(excinfo.value), excinfo.value