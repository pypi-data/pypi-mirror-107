class ScoreVariant(object):
    # non-public

    def __init__(self, part, start_time=0):
        self.t_unfold = start_time
        self.segments = []
        self.part = part

    def add_segment(self, start, end):
        self.segments.append((start, end, self.t_unfold))
        self.t_unfold += end.t - start.t

    @property
    def segment_times(self):
        """
        Return segment (start, end, offset) information for each of the segments in
        the score variant.
        """
        return [(s.t, e.t, o) for (s, e, o) in self.segments]

    def __str__(self):
        return f"{super().__str__()} {self.segment_times}"

    def clone(self):
        """
        Return a clone of the ScoreVariant
        """
        clone = ScoreVariant(self.part, self.t_unfold)
        clone.segments = self.segments[:]
        return clone

    def create_variant_part(self):
        part = Part(self.part.id, part_name=self.part.part_name)

        for start, end, offset in self.segments:
            delta = offset - start.t
            qd = self.part.quarter_durations(start.t, end.t)
            for t, quarter in qd:
                part.set_quarter_duration(t + delta, quarter)
            # After creating the new part we need to replace references to
            # objects in the old part to references in the new part
            # (e.g. t.next, t.prev, note.tie_next). For this we keep track of
            # correspondences between objects (timepoints, notes, measures,
            # etc), in o_map
            o_map = {}
            o_new = set()
            tp = start
            while tp != end:
                # make a new timepoint, corresponding to tp
                tp_new = part.get_or_add_point(tp.t + delta)
                o_gen = (o for oo in tp.starting_objects.values() for o in oo)
                for o in o_gen:

                    # special cases:

                    # don't include repeats/endings in the unfolded part
                    if isinstance(o, (Repeat, Ending)):
                        continue
                    # don't repeat time sig if it hasn't changed
                    elif isinstance(o, TimeSignature):
                        prev = next(tp_new.iter_prev(TimeSignature), None)
                        if (prev is not None) and (
                            (o.beats, o.beat_type) == (prev.beats, prev.beat_type)
                        ):
                            continue
                    # don't repeat key sig if it hasn't changed
                    elif isinstance(o, KeySignature):
                        prev = next(tp_new.iter_prev(KeySignature), None)
                        if (prev is not None) and (
                            (o.fifths, o.mode) == (prev.fifths, prev.mode)
                        ):
                            continue

                    # make a copy of the object
                    o_copy = copy(o)
                    # add it to the set of new objects (for which the refs will
                    # be replaced)
                    o_new.add(o_copy)
                    # keep track of the correspondence between o and o_copy
                    o_map[o] = o_copy
                    # add the start of the new object to the part
                    tp_new.add_starting_object(o_copy)
                    if o.end is not None:
                        # add the end of the object to the part
                        tp_end = part.get_or_add_point(o.end.t + delta)
                        tp_end.add_ending_object(o_copy)

                tp = tp.next
                if tp is None:
                    raise Exception(
                        "segment end not a successor of segment start, "
                        "invalid score variant"
                    )

            # special case: fermata starting at end of segment should be
            # included if it does not belong to a note, and comes at the end of
            # a measure (o.ref == 'right')
            for o in end.starting_objects[Fermata]:
                if o.ref in (None, "right"):
                    o_copy = copy(o)
                    tp_new = part.get_or_add_point(end.t + delta)
                    tp_new.add_starting_object(o_copy)

            # for each of the new objects, replace the references to the old
            # objects to their corresponding new objects
            for o in o_new:
                o.replace_refs(o_map)

        # replace prev/next references in timepoints
        for tp, tp_next in iter_current_next(part._points):
            tp.next = tp_next
            tp_next.prev = tp

        return part


def iter_unfolded_parts(part):
    """Iterate over unfolded clones of `part`.

    For each repeat construct in `part` the iterator produces two
    clones, one with the repeat included and another without the
    repeat. That means the number of items returned is two to the
    power of the number of repeat constructs in the part.

    The first item returned by the iterator is the version of the part
    without any repeated sections, the last item is the version of the
    part with all repeat constructs expanded.

    Parameters
    ----------
    part : :class:`Part`
        Part to unfold

    Yields
    ------

    """

    for sv in make_score_variants(part):
        yield sv.create_variant_part()


def unfold_part_maximal(part, update_ids=False):
    """Return the "maximally" unfolded part, that is, a copy of the
    part where all segments marked with repeat signs are included
    twice.

    Parameters
    ----------
    part : :class:`Part`
        The Part to unfold.
    update_ids : bool (optional)
        Update note ids to reflect the repetitions. Note IDs will have
        a '-<repetition number>', e.g., 'n132-1' and 'n132-2'
        represent the first and second repetition of 'n132' in the
        input `part`. Defaults to False.

    Returns
    -------
    unfolded_part : :class:`Part`
        The unfolded Part

    """

    sv = make_score_variants(part)[-1]

    unfolded_part = sv.create_variant_part()
    if update_ids:
        update_note_ids_after_unfolding(unfolded_part)
    return unfolded_part


def unfold_part_alignment(part, alignment):
    """Return the unfolded part given an alignment, that is, a copy
    of the part where the segments are repeated according to the
    repetitions in a performance.

    Parameters
    ----------
    part : :class:`Part`
        The Part to unfold.
    alignment : list of dictionaries
        List of dictionaries containing an alignment (like the ones
        obtained from a MatchFile (see `alignment_from_matchfile`).

    Returns
    -------
    unfolded_part : :class:`Part`
        The unfolded Part

    """

    unfolded_parts = []

    alignment_ids = []

    for n in alignment:
        if n["label"] == "match" or n["label"] == "deletion":
            alignment_ids.append(n["score_id"])

    score_variants = make_score_variants(part)

    alignment_score_ids = np.zeros((len(alignment_ids), len(score_variants)))
    unfolded_part_length = np.zeros(len(score_variants))
    for j, sv in enumerate(score_variants):
        u_part = sv.create_variant_part()
        update_note_ids_after_unfolding(u_part)
        unfolded_parts.append(u_part)
        u_part_ids = [n.id for n in u_part.notes_tied]
        unfolded_part_length[j] = len(u_part_ids)
        for i, aid in enumerate(alignment_ids):
            alignment_score_ids[i, j] = aid in u_part_ids

    coverage = np.mean(alignment_score_ids, 0)

    best_idx = np.where(coverage == coverage.max())[0]

    if len(best_idx) > 1:
        best_idx = best_idx[unfolded_part_length[best_idx].argmin()]

    return unfolded_parts[int(best_idx)]


def make_score_variants(part):
    # non-public (use unfold_part_maximal, or iter_unfolded_parts)

    """Create a list of ScoreVariant objects, each representing a
    distinct way to unfold the score, based on the repeat structure.

    Parameters
    ----------
    part : :class:`Part`
        A part for which to make the score variants

    Returns
    -------
    list
        List of ScoreVariant objects

    Notes
    -----
    This function does not currently support nested repeats, such as in
    case 45d of the MusicXML Test Suite.

    """

    if len(list(part.iter_all(DaCapo)) + list(part.iter_all(Fine))) > 0:
        LOGGER.warning(
            (
                "Generation of repeat structures involving da "
                "capo/fine/coda/segno directions is not "
                "supported yet"
            )
        )

    # TODO: check if we need to wrap in list
    repeats = list(part.iter_all(Repeat))
    # repeats may not have start or end times. `repeats_to_start_end`
    # returns the start/end paisr for each repeat, making educated guesses
    # when these are missing.
    repeat_start_ends = repeats_to_start_end(repeats, part.first_point, part.last_point)

    # check for nestings and raise if necessary
    if any(n < c for c, n in iter_current_next(repeat_start_ends)):
        raise NotImplementedError("Nested endings are currently not supported")

    # t_score is used to keep the time in the score
    t_score = part.first_point
    svs = [ScoreVariant(part)]
    # each repeat holds start and end time of a score interval to
    # be repeated
    for i, (rep_start, rep_end) in enumerate(repeat_start_ends):
        new_svs = []
        for sv in svs:
            # is the start of the repeat after our current score
            # position?
            if rep_start > t_score:
                # yes: add the tuple (t_score, rep_start) to the
                # result this is the span before the interval that is
                # to be repeated
                sv.add_segment(t_score, rep_start)

            # create a new ScoreVariant for the repetition (sv will be the
            # score variant where this repeat is played only once)
            new_sv = sv.clone()

            # get any "endings" (e.g. 1 / 2 volta) of the repeat
            # (there are not supposed to be more than one)
            ending1 = next(rep_end.iter_ending(Ending), None)
            # is there an ending?
            if ending1:

                # add the first occurrence of the repeat
                sv.add_segment(rep_start, ending1.start)

                ending2 = next(rep_end.iter_starting(Ending), None)

                if ending2:
                    # add the first occurrence of the repeat
                    sv.add_segment(ending2.start, ending2.end)

                    # new_sv includes the 1/2 ending repeat, which means:
                    # 1. from repeat start to repeat end (which includes ending 1)
                    new_sv.add_segment(rep_start, rep_end)
                    # 2. from repeat start to ending 1 start
                    new_sv.add_segment(rep_start, ending1.start)
                    # 3. ending 2 start to ending 2 end
                    new_sv.add_segment(ending2.start, ending2.end)

                    # new score time will be the score time
                    t_end = ending2.end

                else:
                    # ending 1 without ending 2, should not happen normally
                    LOGGER.warning("ending 1 without ending 2")
                    # new score time will be the score time
                    t_end = ending1.end
            else:
                # add the first occurrence of the repeat
                sv.add_segment(rep_start, rep_end)

                # no: add the full interval of the repeat (the second time)
                new_sv.add_segment(rep_start, rep_end)
                new_sv.add_segment(rep_start, rep_end)

                # update the score time
                t_end = rep_end

            # add both score variants
            new_svs.append(sv)
            new_svs.append(new_sv)
        t_score = t_end

        svs = new_svs

    # are we at the end of the piece already?
    if t_score < part.last_point:
        # no, append the interval from the current score
        # position to the end of the piece
        for sv in svs:
            sv.add_segment(t_score, part.last_point)

    return svs


def add_measures(part):
    """Add measures to a part.

    This function adds Measure objects to the part according to any
    time signatures present in the part. Any existing measures will be
    untouched, and added measures will be delimited by the existing
    measures.

    The Part object will be modified in place.

    Parameters
    ----------
    part : :class:`Part`
        Part instance

    """

    timesigs = np.array(
        [(ts.start.t, ts.beats) for ts in part.iter_all(TimeSignature)], dtype=int
    )

    if len(timesigs) == 0:
        LOGGER.warning("No time signatures found, not adding measures")
        return

    start = part.first_point.t
    end = part.last_point.t

    if start == end:
        return

    # make sure we cover time from the start of the timeline
    if len(timesigs) == 0 or timesigs[0, 0] > start:
        timesigs = np.vstack(([[start, 4]], timesigs))

    # in unlikely case of timesig at last point, remove it
    if timesigs[-1, 0] >= end:
        timesigs = timesigs[:-1]

    ts_start_times = timesigs[:, 0]
    beats_per_measure = timesigs[:, 1]
    ts_end_times = ts_start_times[1:]

    # make sure we cover time until the end of the timeline
    if len(ts_end_times) == 0 or ts_end_times[-1] < end:
        ts_end_times = np.r_[ts_end_times, end]

    assert len(ts_start_times) == len(ts_end_times)

    beat_map = part.beat_map
    inv_beat_map = part.inv_beat_map
    mcounter = 1

    for ts_start, ts_end, measure_dur in zip(
        ts_start_times, ts_end_times, beats_per_measure
    ):
        pos = ts_start

        while pos < ts_end:

            measure_start = pos
            measure_end_beats = min(beat_map(pos) + measure_dur, beat_map(end))
            measure_end = min(ts_end, inv_beat_map(measure_end_beats))
            # any existing measures between measure_start and measure_end
            existing_measure = next(
                part.iter_all(Measure, measure_start, measure_end), None
            )
            if existing_measure:
                if existing_measure.start.t == measure_start:
                    assert existing_measure.end.t > pos
                    pos = existing_measure.end.t
                    if existing_measure.number != 0:
                        # if existing_measure is a match anacrusis measure, keep number 0
                        existing_measure.number = mcounter
                        mcounter += 1
                    continue

                else:
                    measure_end = existing_measure.start.t

            part.add(Measure(number=mcounter), int(measure_start), int(measure_end))

            # if measure exists but was not at measure_start, a filler measure is added with number mcounter
            if existing_measure:
                pos = existing_measure.end.t
                existing_measure.number = mcounter + 1
                mcounter = mcounter + 2
            else:
                pos = measure_end
                mcounter += 1


def remove_grace_notes(part):
    """Remove all grace notes from a timeline.

    The specified timeline object will be modified in place.

    Parameters
    ----------
    timeline : Timeline
        The timeline from which to remove the grace notes

    """
    for gn in list(part.iter_all(GraceNote)):
        part.remove(gn)


def expand_grace_notes(part):
    """Expand grace note durations in a part.

    The specified part object will be modified in place.

    Parameters
    ----------
    part : :class:`Part`
        The part on which to expand the grace notes

    """
    for gn in part.iter_all(GraceNote):
        dur = symbolic_to_numeric_duration(gn.symbolic_duration, gn.start.quarter)
        part.remove(gn, "end")
        part.add(gn, end=gn.start.t + int(np.round(dur)))


def iter_parts(partlist):
    """Iterate over all Part instances in partlist, which is a list of
    either Part or PartGroup instances. PartGroup instances contain
    one or more parts or further partgroups, and are traversed in a
    depth-first fashion.

    This function is designed to take the result of
    :func:`partitura.load_score_midi` and :func:`partitura.load_musicxml` as
    input.

    Parameters
    ----------
    partlist : list, Part, or PartGroup
        A :class:`partitura.score.Part` object,
        :class:`partitura.score.PartGroup` or a list of these

    Yields
    -------
        :class:`Part` instances in `partlist`

    """

    if not isinstance(partlist, (list, tuple, set)):
        partlist = [partlist]

    for el in partlist:
        if isinstance(el, Part):
            yield el
        else:
            for eel in iter_parts(el.children):
                yield eel


def repeats_to_start_end(repeats, first, last):
    # non-public
    """Return pairs of (start, end) TimePoints corresponding to the start and
    end times of each Repeat object. If any of the start or end attributes
    are None, replace it with the end/start of the preceding/succeeding
    Repeat, respectively, or `first` or `last`.

    Parameters
    ----------
    repeats : list
        list of Repeat instances, possibly with None-valued start/end
        attributes
    first : TimePoint
        The first TimePoint in the timeline
    last : TimePoint
        The last TimePoint in the timeline

    Returns
    -------
    list
        list of (start, end) TimePoints corresponding to each Repeat in
        `repeats`

    """
    t = first
    starts = []
    ends = []
    for repeat in repeats:
        starts.append(t if repeat.start is None else repeat.start)
        if repeat.end is not None:
            t = repeat.end

    t = last
    for repeat in reversed(repeats):
        ends.append(t if repeat.end is None else repeat.end)
        if repeat.start is not None:
            t = repeat.start
    ends.reverse()
    return list(zip(starts, ends))


def _make_tied_note_id(prev_id):
    # non-public
    """Create a derived note ID for newly created notes, by appending
    letters to the ID. If the original ID has the form X-Y (e.g.
    n1-1), then the letter will be appended to the X part.

    Parameters
    ----------
    prev_id : str
        Original note ID

    Returns
    -------
    str
        Derived note ID

    Examples
    --------
    >>> _make_tied_note_id('n0')
    'n0a'
    >>> _make_tied_note_id('n0a')
    'n0b'
    >>> _make_tied_note_id('n0-1')
    'n0a-1'

    """
    prev_id_parts = prev_id.split("-", 1)
    prev_id_p1 = prev_id_parts[0]
    if prev_id_p1:
        if ord(prev_id_p1[-1]) < ord("a") - 1:
            return "-".join(["{}a".format(prev_id_p1)] + prev_id_parts[1:])
        else:
            return "-".join(
                ["{}{}".format(prev_id_p1[:-1], chr(ord(prev_id[-1]) + 1))]
                + prev_id_parts[1:]
            )
    else:
        return None


def tie_notes(part):
    """Find notes that span measure boundaries and notes with composite
    durations, and split them adding ties.

    Parameters
    ----------
    part : :class:`Part`
        Description of `part`

    """
    # split and tie notes at measure boundaries
    for note in list(part.iter_all(Note)):
        next_measure = next(note.start.iter_next(Measure), None)
        cur_note = note
        note_end = cur_note.end

        # keep the list of stopping slurs, we need to transfer them to the last
        # tied note
        slur_stops = cur_note.slur_stops

        while next_measure and cur_note.end > next_measure.start:
            part.remove(cur_note, "end")
            cur_note.slur_stops = []
            part.add(cur_note, None, next_measure.start.t)
            cur_note.symbolic_duration = estimate_symbolic_duration(
                next_measure.start.t - cur_note.start.t, cur_note.start.quarter
            )
            sym_dur = estimate_symbolic_duration(
                note_end.t - next_measure.start.t, next_measure.start.quarter
            )
            if cur_note.id is not None:
                note_id = _make_tied_note_id(cur_note.id)
            else:
                note_id = None
            next_note = Note(
                note.step,
                note.octave,
                note.alter,
                id=note_id,
                voice=note.voice,
                staff=note.staff,
                symbolic_duration=sym_dur,
            )
            part.add(next_note, next_measure.start.t, note_end.t)

            cur_note.tie_next = next_note
            next_note.tie_prev = cur_note

            cur_note = next_note

            next_measure = next(cur_note.start.iter_next(Measure), None)

        if cur_note != note:
            for slur in slur_stops:
                slur.end_note = cur_note

    # then split/tie any notes that do not have a fractional/dot duration
    divs_map = part.quarter_duration_map
    max_splits = 3
    failed = 0
    succeeded = 0
    for i, note in enumerate(list(part.iter_all(Note))):
        if note.symbolic_duration is None:

            splits = find_tie_split(
                note.start.t, note.end.t, int(divs_map(note.start.t)), max_splits
            )

            if splits:
                succeeded += 1
                split_note(part, note, splits)
            else:
                failed += 1


def set_end_times(parts):
    # non-public
    """Set missing end times of musical elements in a part to equal
    the start times of the subsequent element of the same class. This
    is useful for some classes

    This function modifies the parts in place.

    Parameters
    ----------
    part : Part or PartGroup, or list of these
        Parts to be processed

    """
    for part in iter_parts(parts):
        # page, system, loudnessdirection, tempodirection
        _set_end_times(part, Page)
        _set_end_times(part, System)
        _set_end_times(part, ConstantLoudnessDirection)
        _set_end_times(part, ConstantTempoDirection)
        _set_end_times(part, ConstantArticulationDirection)


def _set_end_times(part, cls):
    acc = []
    t = None

    for obj in part.iter_all(cls, include_subclasses=True):

        if obj.start == t:

            if obj.end is None:

                acc.append(obj)

        else:

            for o in acc:

                part.add(o, end=obj.start.t)

            acc = []

            if obj.end is None:

                acc.append(obj)

            t = obj.start

    for o in acc:

        part.add(o, end=part.last_point.t)


def split_note(part, note, splits):
    # non-public

    # TODO: we shouldn't do this, but for now it's a good sanity check
    assert len(splits) > 0
    # TODO: we shouldn't do this, but for now it's a good sanity check
    assert note.symbolic_duration is None
    part.remove(note)
    orig_tie_next = note.tie_next
    slur_stops = note.slur_stops
    cur_note = note
    start, end, sym_dur = splits.pop(0)
    cur_note.symbolic_duration = sym_dur
    part.add(cur_note, start, end)
    while splits:
        note.slur_stops = []

        if cur_note.id is not None:
            note_id = _make_tied_note_id(cur_note.id)
        else:
            note_id = None

        next_note = Note(
            note.step,
            note.octave,
            note.alter,
            voice=note.voice,
            id=note_id,
            staff=note.staff,
        )
        cur_note.tie_next = next_note
        next_note.tie_prev = cur_note

        cur_note = next_note
        start, end, sym_dur = splits.pop(0)
        cur_note.symbolic_duration = sym_dur

        part.add(cur_note, start, end)

    cur_note.tie_next = orig_tie_next

    if cur_note != note:
        for slur in slur_stops:
            slur.end_note = cur_note


def find_tuplets(part):
    """Identify tuplets in `part` and set their symbolic durations
    explicitly.

    This function adds `actual_notes` and `normal_notes` keys to
    the symbolic duration of tuplet notes.

    This function modifies the part in place.

    Parameters
    ----------
    part : :class:`Part`
        Part instance

    """

    # quick shot at finding tuplets intended to cover some common cases.

    # are tuplets always in the same voice?

    # quite arbitrary:
    search_for_tuplets = [9, 7, 5, 3]
    # only look for x:2 tuplets
    normal_notes = 2

    candidates = []
    prev_end = None

    # 1. group consecutive notes without symbolic_duration
    for note in part.iter_all(GenericNote, include_subclasses=True):

        if note.symbolic_duration is None:
            if note.start.t == prev_end:
                candidates[-1].append(note)
            else:
                candidates.append([note])
            prev_end = note.end.t

    # 2. within each group
    for group in candidates:

        # 3. search for the predefined list of tuplets
        for actual_notes in search_for_tuplets:

            if actual_notes > len(group):
                # tuplet requires more notes than we have
                continue

            tup_start = 0

            while tup_start <= (len(group) - actual_notes):
                note_tuplet = group[tup_start : tup_start + actual_notes]
                # durs = set(n.duration for n in group[:tuplet-1])
                durs = set(n.duration for n in note_tuplet)

                if len(durs) > 1:
                    # notes have different durations (possibly valid but not
                    # supported here)
                    # continue
                    tup_start += 1
                else:

                    start = note_tuplet[0].start.t
                    end = note_tuplet[-1].end.t
                    total_dur = end - start

                    # total duration of tuplet notes must be integer-divisble by
                    # normal_notes
                    if total_dur % normal_notes > 0:
                        tup_start += 1
                    else:
                        # estimate duration type
                        dur_type = estimate_symbolic_duration(
                            total_dur // normal_notes, note_tuplet[0].start.quarter
                        )

                        if dur_type and dur_type.get("dots", 0) == 0:
                            # recognized duration without dots
                            dur_type["actual_notes"] = actual_notes
                            dur_type["normal_notes"] = normal_notes
                            for note in note_tuplet:
                                note.symbolic_duration = dur_type.copy()
                            start_note = note_tuplet[0]
                            stop_note = note_tuplet[-1]
                            tuplet = Tuplet(start_note, stop_note)
                            part.add(tuplet, start_note.start.t, stop_note.end.t)
                            tup_start += actual_notes

                        else:
                            tup_start += 1


def sanitize_part(part):
    """Find and remove incomplete structures in a part such as Tuplets
    and Slurs without start or end and grace notes without a main
    note.

    This function modifies the part in place.

    Parameters
    ----------
    part : :class:`Part`
        Part instance

    """
    remove_grace_counter = 0
    elements_to_remove = []
    for gn in part.iter_all(GraceNote):
        if gn.main_note is None:
            for no in part.iter_all(
                Note, include_subclasses=False, start=gn.start.t, end=gn.start.t + 1
            ):
                if no.voice == gn.voice:
                    gn.last_grace_note_in_seq.grace_next = no

        if gn.main_note is None:
            elements_to_remove.append(gn)
            remove_grace_counter += 1

    remove_tuplet_counter = 0
    for tp in part.iter_all(Tuplet):
        if tp.end_note is None or tp.start_note is None:
            elements_to_remove.append(tp)
            remove_tuplet_counter += 1

    remove_slur_counter = 0
    for sl in part.iter_all(Slur):
        if sl.end_note is None or sl.start_note is None:
            elements_to_remove.append(sl)
            remove_slur_counter += 1

    for el in elements_to_remove:
        part.remove(el)
    LOGGER.info(
        "part_sanitize removed {} incomplete tuplets, "
        "{} incomplete slurs, and {} incomplete grace "
        "notes".format(remove_tuplet_counter, remove_slur_counter, remove_grace_counter)
    )
