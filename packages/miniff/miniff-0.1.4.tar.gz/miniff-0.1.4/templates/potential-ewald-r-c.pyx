# Template potential-ewald-r-c.pyx
# Charge gradient of the real-space component
$decorators
def $name(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, $parameters
    int[::1] species_row,
    int[::1] species_mask,
    double[:, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    for row in $range(nrows,$range_args):
        ptr_fr = r_indptr[row]
        ptr_to = r_indptr[row + 1]
        for ptr in range(ptr_fr, ptr_to):
            col = r_indices[ptr]
            col_ = cython.cmod(col, nrows)
            r = r_data[ptr]

            if r < a:
                g = erfc(eta * r) / r / 2
                out[row, row] += g * charges[col_]
                out[row, col_] += g * charges[row]
out_shape["$name"] = "rr"
coordination["$name"] = 2
resolving["$name"] = True
