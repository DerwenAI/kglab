
from icecream import ic
import numpy as np

t = np.array([
    [ 1, 2, 3, "foo" ],
    [ 2, 3, 4, "bar" ],
    [ 5, 6, 7, "hello" ],
    [ 8, 9, 1, "bar" ],
])

add_row = np.array([ 4, 5, 6, "wow" ])

t = np.vstack([t, add_row])

ic(t)

rows = np.where(t[:,3] == "bar")
ic(rows)
ic(t[rows])
