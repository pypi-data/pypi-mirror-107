""" DBR gratings
wavelength = 2*period*neff
period = wavelength/2/neff

dbr default parameters are from Stephen Lin thesis
https://open.library.ubc.ca/cIRcle/collections/ubctheses/24/items/1.0388871

Period: 318nm, width: 500nm, dw: 20 ~ 120 nm.
"""
import pp
from pp.cell import cell
from pp.component import Component
from pp.components.straight import straight as straight_function
from pp.types import ComponentFactory

period = 318e-3
w0 = 0.5
dw = 50e-3
w1 = w0 - dw / 2
w2 = w0 + dw / 2


@cell
def dbr_cell(
    w1: float = w1,
    w2: float = w2,
    l1: float = period / 2,
    l2: float = period / 2,
    straight: ComponentFactory = straight_function,
) -> Component:
    l1 = pp.snap_to_grid(l1)
    l2 = pp.snap_to_grid(l2)
    w1 = pp.snap_to_grid(w1, 2)
    w2 = pp.snap_to_grid(w2, 2)
    c = Component()
    c1 = c << straight(length=l1, width=w1)
    c2 = c << straight(length=l2, width=w2)
    c2.connect(port="W0", destination=c1.ports["E0"])
    c.add_port("W0", port=c1.ports["W0"])
    c.add_port("E0", port=c2.ports["E0"])
    return c


@cell
def dbr(
    w1: float = w1,
    w2: float = w2,
    l1: float = period / 2,
    l2: float = period / 2,
    n: int = 10,
    straight: ComponentFactory = straight_function,
) -> Component:
    """Distributed Bragg Reflector

    Args:
        w1: thin width
        l1: thin length
        w2: thick width
        l2: thick length
        n: number of periods

    .. code::

           l1      l2
        <-----><-------->
                _________
        _______|

          w1       w2       ...  n times
        _______
               |_________


    """
    c = Component()
    l1 = pp.snap_to_grid(l1)
    l2 = pp.snap_to_grid(l2)
    cell = dbr_cell(
        w1=w1,
        w2=w2,
        l1=l1,
        l2=l2,
        straight=straight,
    )
    c.add_array(cell, columns=n, rows=1, spacing=(l1 + l2, 100))
    c.add_port("W0", port=cell.ports["W0"])
    p1 = c.add_port("E0", port=cell.ports["E0"])
    p1.midpoint = [(l1 + l2) * n, 0]
    return c


if __name__ == "__main__":
    # c = dbr(w1=0.5, w2=0.6, l1=0.2, l2=0.3, n=10)
    # c = dbr()
    c = dbr_cell()
    c.assert_ports_on_grid()
    c.show()
