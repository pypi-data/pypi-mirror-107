# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2021 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

import hashlib
import math
from itertools import islice

from hypothesis import HealthCheck, settings
from hypothesis.errors import HypothesisException
from hypothesis.internal.conjecture.data import ConjectureResult, Status
from hypothesis.internal.conjecture.dfa.lstar import LStar
from hypothesis.internal.conjecture.shrinking.learned_dfas import (
    SHRINKING_DFAS,
    __file__ as learned_dfa_file,
)

"""
This is a module for learning new DFAs that help normalize test
functions. That is, given a test function that sometimes shrinks
to one thing and sometimes another, this module is designed to
help learn new DFA-based shrink passes that will cause it to
always shrink to the same thing.
"""


class FailedToNormalise(HypothesisException):
    pass


def update_learned_dfas():
    """Write any modifications to the SHRINKING_DFAS dictionary
    back to the learned DFAs file."""

    with open(learned_dfa_file) as i:
        source = i.read()

    lines = source.splitlines()

    i = lines.index("# AUTOGENERATED BEGINS")

    del lines[i + 1 :]

    lines.append("")
    lines.append("# fmt: off")
    lines.append("")

    for k, v in sorted(SHRINKING_DFAS.items()):
        lines.append(f"SHRINKING_DFAS[{k!r}] = {v!r}  # noqa: E501")

    lines.append("")
    lines.append("# fmt: on")

    new_source = "\n".join(lines) + "\n"

    if new_source != source:
        with open(learned_dfa_file, "w") as o:
            o.write(new_source)


def learn_a_new_dfa(runner, u, v, predicate):
    """Given two buffers ``u`` and ``v```, learn a DFA that will
    allow the shrinker to normalise them better. ``u`` and ``v``
    should not currently shrink to the same test case when calling
    this function."""
    from hypothesis.internal.conjecture.shrinker import dfa_replacement, sort_key

    assert predicate(runner.cached_test_function(u))
    assert predicate(runner.cached_test_function(v))

    u_shrunk = fully_shrink(runner, u, predicate)
    v_shrunk = fully_shrink(runner, v, predicate)

    u, v = sorted((u_shrunk.buffer, v_shrunk.buffer), key=sort_key)

    assert u != v

    assert not v.startswith(u)

    # We would like to avoid using LStar on large strings as its
    # behaviour can be quadratic or worse. In order to help achieve
    # this we peel off a common prefix and suffix of the two final
    # results and just learn the internal bit where they differ.
    #
    # This potentially reduces the length quite far if there's
    # just one tricky bit of control flow we're struggling to
    # reduce inside a strategy somewhere and the rest of the
    # test function reduces fine.
    if v.endswith(u):
        prefix = b""
        suffix = u
        u_core = b""
        assert len(u) > 0
        v_core = v[: -len(u)]
    else:
        i = 0
        while u[i] == v[i]:
            i += 1
        prefix = u[:i]
        assert u.startswith(prefix)
        assert v.startswith(prefix)

        i = 1
        while u[-i] == v[-i]:
            i += 1

        suffix = u[max(len(prefix), len(u) + 1 - i) :]
        assert u.endswith(suffix)
        assert v.endswith(suffix)

        u_core = u[len(prefix) : len(u) - len(suffix)]
        v_core = v[len(prefix) : len(v) - len(suffix)]

    assert u == prefix + u_core + suffix, (list(u), list(v))
    assert v == prefix + v_core + suffix, (list(u), list(v))

    better = runner.cached_test_function(u)
    worse = runner.cached_test_function(v)

    allow_discards = worse.has_discards or better.has_discards

    def is_valid_core(s):
        if not (len(u_core) <= len(s) <= len(v_core)):
            return False
        buf = prefix + s + suffix
        result = runner.cached_test_function(buf)
        return (
            predicate(result)
            # Because we're often using this to learn strategies
            # rather than entire complex test functions, it's
            # important that our replacements are precise and
            # don't leave the rest of the test case in a weird
            # state.
            and result.buffer == buf
            # Because the shrinker is good at removing discarded
            # data, unless we need discards to allow one or both
            # of u and v to result in valid shrinks, we don't
            # count attempts that have them as valid. This will
            # cause us to match fewer strings, which will make
            # the resulting shrink pass more efficient when run
            # on test functions it wasn't really intended for.
            and (allow_discards or not result.has_discards)
        )

    assert sort_key(u_core) < sort_key(v_core)

    assert is_valid_core(u_core)
    assert is_valid_core(v_core)

    learner = LStar(is_valid_core)

    prev = -1
    while learner.generation != prev:
        prev = learner.generation
        learner.learn(u_core)
        learner.learn(v_core)

        # L* has a tendency to learn DFAs which wrap around to
        # the beginning. We don't want to it to do that unless
        # it's accurate, so we use these as examples to show
        # check going around the DFA twice.
        learner.learn(u_core * 2)
        learner.learn(v_core * 2)

        if learner.dfa.max_length(learner.dfa.start) > len(v_core):
            # The language we learn is finite and bounded above
            # by the length of v_core. This is important in order
            # to keep our shrink passes reasonably efficient -
            # otherwise they can match far too much. So whenever
            # we learn a DFA that could match a string longer
            # than len(v_core) we fix it by finding the first
            # string longer than v_core and learning that as
            # a correction.
            x = next(learner.dfa.all_matching_strings(min_length=len(v_core) + 1))
            assert not is_valid_core(x)
            learner.learn(x)
            assert not learner.dfa.matches(x)
            assert learner.generation != prev
        else:
            # We mostly care about getting the right answer on the
            # minimal test case, but because we're doing this offline
            # anyway we might as well spend a little more time trying
            # small examples to make sure the learner gets them right.
            for x in islice(learner.dfa.all_matching_strings(), 100):
                if not is_valid_core(x):
                    learner.learn(x)
                    assert learner.generation != prev
                    break

    # We've now successfully learned a DFA that works for shrinking
    # our failed normalisation further. Canonicalise it into a concrete
    # DFA so we can save it for later.
    new_dfa = learner.dfa.canonicalise()

    assert math.isfinite(new_dfa.max_length(new_dfa.start))

    shrinker = runner.new_shrinker(runner.cached_test_function(v), predicate)

    assert (len(prefix), len(v) - len(suffix)) in shrinker.matching_regions(new_dfa)

    name = "tmp-dfa-" + repr(new_dfa)

    shrinker.extra_dfas[name] = new_dfa

    shrinker.fixate_shrink_passes([dfa_replacement(name)])

    assert sort_key(shrinker.buffer) < sort_key(v)

    return new_dfa


def fully_shrink(runner, test_case, predicate):
    if not isinstance(test_case, ConjectureResult):
        test_case = runner.cached_test_function(test_case)
    while True:
        shrunk = runner.shrink(test_case, predicate)
        if shrunk.buffer == test_case.buffer:
            break
        test_case = shrunk
    return test_case


def normalize(
    base_name,
    test_function,
    *,
    required_successes=100,
    allowed_to_update=False,
    max_dfas=10,
):
    """Attempt to ensure that this test function successfully normalizes - i.e.
    whenever it declares a test case to be interesting, we are able
    to shrink that to the same interesting test case (which logically should
    be the shortlex minimal interesting test case, though we may not be able
    to detect if it is).

    Will run until we have seen ``required_successes`` many interesting test
    cases in a row normalize to the same value.

    If ``allowed_to_update`` is True, whenever we fail to normalize we will
    learn a new DFA-based shrink pass that allows us to make progress. Any
    learned DFAs will be written back into the learned DFA file at the end
    of this function. If ``allowed_to_update`` is False, this will raise an
    error as soon as it encounters a failure to normalize.

    Additionally, if more than ``max_dfas` DFAs are required to normalize
    this test function, this function will raise an error - it's essentially
    designed for small patches that other shrink passes don't cover, and
    if it's learning too many patches then you need a better shrink pass
    than this can provide.
    """
    # Need import inside the function to avoid circular imports
    from hypothesis.internal.conjecture.engine import BUFFER_SIZE, ConjectureRunner

    runner = ConjectureRunner(
        test_function,
        settings=settings(database=None, suppress_health_check=HealthCheck.all()),
        ignore_limits=True,
    )

    seen = set()

    dfas_added = 0

    found_interesting = False
    consecutive_successes = 0
    failures_to_find_interesting = 0
    while consecutive_successes < required_successes:
        attempt = runner.cached_test_function(b"", extend=BUFFER_SIZE)
        if attempt.status < Status.INTERESTING:
            failures_to_find_interesting += 1
            assert (
                found_interesting or failures_to_find_interesting <= 1000
            ), "Test function seems to have no interesting test cases"
            continue

        found_interesting = True

        target = attempt.interesting_origin

        def shrinking_predicate(d):
            return d.status == Status.INTERESTING and d.interesting_origin == target

        if target not in seen:
            seen.add(target)
            runner.shrink(attempt, shrinking_predicate)
            continue

        previous = fully_shrink(
            runner, runner.interesting_examples[target], shrinking_predicate
        )
        current = fully_shrink(runner, attempt, shrinking_predicate)

        if current.buffer == previous.buffer:
            consecutive_successes += 1
            continue

        consecutive_successes = 0

        if not allowed_to_update:
            raise FailedToNormalise(
                "Shrinker failed to normalize %r to %r and we are not allowed to learn new DFAs."
                % (previous.buffer, current.buffer)
            )

        if dfas_added >= max_dfas:
            raise FailedToNormalise(
                "Test function is too hard to learn: Added %d DFAs and still not done."
                % (dfas_added,)
            )

        dfas_added += 1

        new_dfa = learn_a_new_dfa(
            runner, previous.buffer, current.buffer, shrinking_predicate
        )

        name = (
            base_name
            + "-"
            + hashlib.sha256(repr(new_dfa).encode("utf-8")).hexdigest()[:10]
        )

        # If there is a name collision this DFA should already be being
        # used for shrinking, so we should have already been able to shrink
        # v further.
        assert name not in SHRINKING_DFAS
        SHRINKING_DFAS[name] = new_dfa

    if dfas_added > 0:
        # We've learned one or more DFAs in the course of normalising, so now
        # we update the file to record those for posterity.
        update_learned_dfas()
