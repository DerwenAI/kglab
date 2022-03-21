
from icecream import ic
import numpy as np

x = np.empty(shape=[0, 1], dtype=object)
x = np.append(x, "foo")
x = np.append(x, "bar")
ic(x)
ic(x[0])

#np.array([ "foo", "bar" ])
ic(np.where(x == "bar"))

t = np.array([
    [ 1, 2, 3, "foo" ],
    [ 2, 3, 4, "bar" ],
    [ 5, 6, 7, "hello" ],
    [ 8, 9, 1, "bar" ],
])

add_row = np.array([ 4, 5, 6, "wow" ])
t = np.vstack([t, add_row])
ic(t)

ic(t[0, 3])


rows = np.where(t[:,3] == "bar")
ic(type(rows[0]))
ic(len(rows[0]))
ic(rows)
ic(rows[0][0])
ic(t[rows])
