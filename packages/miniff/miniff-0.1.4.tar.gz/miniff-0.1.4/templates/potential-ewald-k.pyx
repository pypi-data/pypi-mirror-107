# Template potential-ewald-k-g.pyx
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
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = cartesian_row.shape[0]
    cdef int nk = k_grid.shape[0]
    cdef int row, k, dim
    cdef double accu = 0, phase, sn, cs, structure_factor_r, structure_factor_i, ksq
    cdef double prefactor = 4 * pi / (2 * volume)
    cdef double result = 0

    for k in $range(nk, $range_args):
        structure_factor_r = 0
        structure_factor_i = 0
        for row in range(nrows):
            phase = 0
            for dim in range(3):
                phase = phase + k_grid[k, dim] * cartesian_row[row, dim]
            cs = cos(phase)
            sn = sin(phase)
            structure_factor_r = structure_factor_r + cs * charges[row]
            structure_factor_i = structure_factor_i + sn * charges[row]
        ksq = 0
        for dim in range(3):
            ksq = ksq + k_grid[k, dim] * k_grid[k, dim]
        result += (structure_factor_r * structure_factor_r + structure_factor_i * structure_factor_i) * exp(-0.25 * ksq / eta / eta) / ksq * prefactor
    out[0] += result  # This is a workaround for cython to recognize a reduction sum
out_shape["$name"] = ""
coordination["$name"] = 1
resolving["$name"] = False
