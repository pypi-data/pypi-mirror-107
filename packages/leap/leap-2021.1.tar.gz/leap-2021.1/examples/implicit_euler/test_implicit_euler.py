#! /usr/bin/env python

import pytest
import sys
import numpy as np


__copyright__ = "Copyright (C) 2014 Andreas Kloeckner, Matt Wala"

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


# Taken from test.utils
def python_method_impl_interpreter(code, **kwargs):
    from dagrt.exec_numpy import NumpyInterpreter
    return NumpyInterpreter(code, **kwargs)


# Taken from test.utils
def python_method_impl_codegen(code, **kwargs):
    from dagrt.codegen import PythonCodeGenerator
    codegen = PythonCodeGenerator(class_name="Method")
    return codegen.get_class(code)(**kwargs)


def solver(f, t, h, y, guess):
    from scipy.optimize import newton
    return newton(lambda u: u-y-h*f(t=t, y=u), guess)


def solver_hook(expr, var, solver_id, guess):
    from dagrt.expression import match, substitute
    pieces = match("unk-y-h*<func>f(t=t,y=unk)", expr, pre_match={"unk": var})
    pieces["guess"] = guess
    return substitute("<func>solver(t,h,y,guess)", pieces)


@pytest.mark.parametrize("python_method_impl",
    [python_method_impl_codegen, python_method_impl_interpreter])
def test_im_euler_accuracy(python_method_impl, show_dag=False,
                           plot_solution=False):
    component_id = "y"

    from .implicit_euler import ImplicitEulerMethodBuilder

    method = ImplicitEulerMethodBuilder(component_id)
    code = method.generate(solver_hook)

    expected_order = 1

    if show_dag:
        from dagrt.language import show_dependency_graph
        show_dependency_graph(code)

    h = -0.5
    y_0 = 1.0

    def rhs(t, y):
        return h * y

    def soln(t):
        return y_0 * np.exp(h * t)

    from pytools.convergence import EOCRecorder
    eocrec = EOCRecorder()

    for n in range(1, 5):
        dt = 2**(-n)
        t = 0.0
        y = y_0
        final_t = 1

        from functools import partial
        interp = python_method_impl(code,
            function_map={method.rhs_func.name: rhs,
                          "<func>solver": partial(solver, rhs)})

        interp.set_up(t_start=t, dt_start=dt, context={component_id: y})

        times = []
        values = []
        for event in interp.run(t_end=final_t):
            if isinstance(event, interp.StateComputed):
                assert event.component_id == component_id
                values.append(event.state_component)
                times.append(event.t)

        assert abs(times[-1] - final_t) < 1e-10

        times = np.array(times)

        if plot_solution:
            import matplotlib.pyplot as pt
            pt.plot(times, values, label="comp")
            pt.plot(times, soln(times), label="true")
            pt.show()

        error = abs(values[-1]-soln(final_t))
        eocrec.add_data_point(dt, error)

    print("------------------------------------------------------")
    print("%s: expected order %d" % (method, expected_order))
    print("------------------------------------------------------")
    print(eocrec.pretty_print())

    orderest = eocrec.estimate_order_of_convergence()[0, 1]
    assert orderest > expected_order*0.9


if __name__ == "__main__":
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from pytest import main
        main([__file__])
