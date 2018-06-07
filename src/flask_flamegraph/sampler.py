import collections
import signal
import subprocess  # nosec
import time

import pkg_resources

flamegraph_pl = pkg_resources.resource_filename(
    'flask_flamegraph',
    'flamegraph.pl',
)


class Sampler:
    def __init__(self, interval=0.001):
        self.stack_counts = collections.Counter()
        self.interval = interval

    def _sample(self, signum, frame):
        now = time.time()

        stack = []
        while frame is not None:
            formatted_frame = '{}({})'.format(
                frame.f_code.co_name,
                frame.f_globals.get('__name__'),
            )
            stack.append(formatted_frame)
            frame = frame.f_back

        formatted_stack = ';'.join(reversed(stack))
        self.stack_counts[formatted_stack] += 1

        delta = now - self._last
        if delta > 5 * self.interval:
            # Last sample happened a long time ago, most likely we were "stuck"
            # in some external module.
            missed = delta / self.interval
            formatted_stack = (
                formatted_stack.rpartition(';')[0] + ';NATIVE CODE EXECUTION'
            )
            self.stack_counts[formatted_stack] += missed - 1
        self._last = now

    def _get_stats(self):
        return '\n'.join(
            f'{key} {value}'
            for key, value in sorted(self.stack_counts.items())
        )

    def generate_svg(self):
        stats = self._get_stats()
        result, _ = (
            subprocess.Popen(  # nosec
                args=[flamegraph_pl, '--title', ' '],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
            .communicate(stats)
        )
        return result

    def start(self):
        self._start = self._last = time.time()
        signal.signal(signal.SIGALRM, self._sample)
        signal.siginterrupt(signal.SIGALRM, False)
        signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)

    def stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
