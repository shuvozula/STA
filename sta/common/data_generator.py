
__author__ = 'Spondon Saha'


import logging
import math
import random


class Error(Exception):
    """Native exception class."""
    pass


def GenData(num_robots, coalition_size_range, bid_limit, task_size,
            max_bid_value, max_bids_per_task):
    """Data generator for creating random bids submitted by robot coalitions.

    List of tasks to accomplish have been announced and this data generator
    creates random bids and submits them as a tuple of the bid-value and
    the list of robots (robot coalition) that submitted it. The data is
    generated based on the provided parameters.

    The data generated looks a lot like this:
    T3 2,3 7
    T1 1,3,5 9
    T4 4 10
    ...

    Arguments:
        num_robots: the number of robots
        coalition_size_range: allowed range of coalition sizes in the following
        format [min_range, max_range] where min_range <= max_range.
        bid_limit: The maximum number of bids that the STA algorithm will take
        for this round.
        task_size: Number of tasks to accomplish
        max_bid_valiue: Maximum allowable bid value accepted in the auction.
        max_bids_per_task: Maximum number of bids allowed to be submitted for
        each task.

    Raises:
        Error: Whenever we have one of the following problems:
        1. The provided coalition_size_range set does not have 2 elements within
        2. The min. range value in coalition_size_range is greater than the max.
        range value in coalition_size_range

    Returns:
        The generated data as collected in all_bids.
    """
    all_bids = []
    # create the task list
    task_names = ['T%s' % (task_num + 1) for task_num in range(task_size)]
    task_counts = [0] * task_size
    all_tasks = dict(zip(task_names, task_counts))
    # generate bids
    curr_bid_count = 0
    while curr_bid_count <= bid_limit:
        # acquire a random task
        while True:
            rnd_task = random.choice(task_names)
            if all_tasks[rnd_task] < max_bids_per_task:
                all_tasks[rnd_task] += 1
                break
        # validate coalition size ranges and acquire random coalition size
        if len(coalition_size_range) > 2:
            raise Error('Expected [lower, upper] got %s' % coalition_size_range)
        elif coalition_size_range[0] > coalition_size_range[1]:
            raise Error('Min-range > Max-range: %s' % coalition_size_range)
        else:
            rnd_coalition_size = random.randint(*coalition_size_range)
        # generate a coalition of robots of size rnd_coalition_size
        # assumption: robots are identified as numbers
        coalition = random.sample(range(1, num_robots), rnd_coalition_size)
        coalition = [str(x) for x in coalition]
        # put them together
        rnd_bid_value = random.randint(1, max_bid_value)
        all_bids.append('%s %s %s' % (rnd_task,
                                      ','.join(coalition),
                                      rnd_bid_value))
        # update the bid count
        curr_bid_count += 1
    return '\n'.join(all_bids)
