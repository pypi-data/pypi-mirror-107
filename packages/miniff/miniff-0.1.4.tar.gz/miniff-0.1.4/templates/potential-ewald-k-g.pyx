# Template potential-ewald-k.pyx
# Ewald integration in k-space
$decorators
def $name(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double eta, double[::1] charges, double volume, double[:, ::1] k_grid,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, ::1] out,
):
    # Vars: indexing
    cdef int nrows = cartesian_row.shape[0]
    cdef int nk = k_grid.shape[0]
    cdef int row, col, k, dim, dim1
    cdef double phase, sn, cs

    cdef double[::1] weights = np.linalg.norm(k_grid, axis=-1)
    cdef double prefactor = 4 * pi / (2 * volume) * 2
    for k in range(nk):
        weights[k] = prefactor * exp(-0.25 * weights[k] * weights[k] / eta / eta) / (weights[k] * weights[k])

    cdef double[:, ::1] structure_factor = np.zeros((k_grid.shape[0], 2), dtype=float)
    for k in $range(nk, $range_args):
        for row in range(nrows):
            phase = 0
            for dim in range(3):
                phase = phase + k_grid[k, dim] * cartesian_row[row, dim]
            cs = cos(phase)
            sn = sin(phase)
            structure_factor[k, 0] += cs * charges[row]
            structure_factor[k, 1] += sn * charges[row]

    for row in $range(nrows, $range_args):
        for dim in range(3):
            for k in range(nk):
                phase = 0
                for dim1 in range(3):
                    phase = phase + k_grid[k, dim1] * cartesian_row[row, dim1]
                out[row, dim] += weights[k] * charges[row] * k_grid[k, dim] * (cos(phase) * structure_factor[k, 1] - sin(phase) * structure_factor[k, 0])
out_shape["$name"] = "rd"
coordination["$name"] = 1
resolving["$name"] = False
