"""Leap root module"""


__copyright__ = "Copyright (C) 2014 Andreas Kloeckner"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


# {{{ command-line generator

def run_script_from_commandline():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("script", metavar="SCRIPT.PY")
    parser.add_argument("args", metavar="ARG", nargs="*")
    args = parser.parse_args()

    from os.path import abspath, dirname
    scriptdir = dirname(abspath(args.script))

    import sys
    sys.argv[1:] = args.args
    sys.path.append(scriptdir)

    with open(args.script) as s:
        script_contents = s.read()

    namespace = {"__name__": "__main__"}
    exec(compile(script_contents, args.script, "exec"), namespace)

# }}}


# {{{ method builder base class

class MethodBuilder:

    def generate(self, *solver_hooks):
        """
        Generate a method description.

        :arg solver_hooks: A list of callbacks that generate expressions
        for calling user-supplied implicit solvers

        :return: A `DAGCode` instance
        """
        raise NotImplementedError()

    def implicit_expression(self, expression_tag=None):
        """
        Return a template that expressions in `class`:AssignImplicit
        instances will follow.

        :arg expression_tag: A name for the expression, if multiple
        expressions are present in the generated code.

        :return: A tuple consisting of :mod:`pymbolic` expressions and
        the names of the free variables in the expressions.
        """
        raise NotImplementedError()

# }}}


# {{{ two-order adaptivity

class TwoOrderAdaptiveMethodBuilderMixin(MethodBuilder):
    """
    This class expected the following members to be defined: state, t, dt.
    """

    def __init__(self, atol=0, rtol=0, max_dt_growth=None, min_dt_shrinkage=None):
        self.adaptive = bool(atol or rtol)
        self.atol = atol
        self.rtol = rtol

        if max_dt_growth is None:
            max_dt_growth = 5

        if min_dt_shrinkage is None:
            min_dt_shrinkage = 0.1

        self.max_dt_growth = max_dt_growth
        self.min_dt_shrinkage = min_dt_shrinkage

    def finish_nonadaptive(self, cb, high_order_estimate, low_order_estimate):
        raise NotImplementedError()

    def finish_adaptive(self, cb, high_order_estimate, low_order_estimate):
        from pymbolic import var
        from pymbolic.primitives import Comparison, LogicalOr, Max, Min
        from dagrt.expression import IfThenElse

        norm_start_state = var("norm_start_state")
        norm_end_state = var("norm_end_state")
        rel_error_raw = var("rel_error_raw")
        rel_error = var("rel_error")

        def norm(expr):
            return var("<builtin>norm_2")(expr)

        cb(norm_start_state, norm(self.state))
        cb(norm_end_state, norm(low_order_estimate))
        cb(rel_error_raw, norm(high_order_estimate - low_order_estimate)
                / (var("<builtin>len")(self.state) ** 0.5
                    * (
                        self.atol + self.rtol
                        * Max((norm_start_state, norm_end_state))
                        )))

        cb(rel_error, IfThenElse(Comparison(rel_error_raw, "==", 0),
                                 1.0e-14, rel_error_raw))

        with cb.if_(LogicalOr((Comparison(rel_error, ">", 1),
                               var("<builtin>isnan")(rel_error)))):

            with cb.if_(var("<builtin>isnan")(rel_error)):
                cb(self.dt, self.min_dt_shrinkage * self.dt)
            with cb.else_():
                cb(self.dt, Max((0.9 * self.dt
                    * rel_error ** (-1 / self.low_order),
                    self.min_dt_shrinkage * self.dt)))

            with cb.if_(self.t + self.dt, "==", self.t):
                cb.raise_(TimeStepUnderflow)
            with cb.else_():
                cb.fail_step()

        with cb.else_():
            # This updates <t>: <dt> should not be set before this is called.
            self.finish_nonadaptive(cb, high_order_estimate, low_order_estimate)

            cb(self.dt,
               Min((0.9 * self.dt * rel_error ** (-1 / self.high_order),
                    self.max_dt_growth * self.dt)))

# }}}


# {{{ diagnostics

class TimeStepUnderflow(RuntimeError):
    pass

# }}}

# vim: foldmethod=marker
