# cython: language_level=2
import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport sqrt, acos, exp


def calc_sparse_distances(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, dim
    cdef int ptr, ptr_fr, ptr_to

    # Vars: coordinates and distances
    cdef double x, y, z

    # Vars: result
    result = np.empty(len(r_indices), dtype=float)
    cdef double[::1] result_mv = result

    for row in range(nrows):
        ptr_fr = r_indptr[row]
        ptr_to = r_indptr[row + 1]
        for ptr in range(ptr_fr, ptr_to):
            col = r_indices[ptr]
            result_mv[ptr] = 0
            for dim in range(3):
                result_mv[ptr] += (cartesian_col[col, dim] - cartesian_row[row, dim]) * (cartesian_col[col, dim] - cartesian_row[row, dim])
            result_mv[ptr] = sqrt(result_mv[ptr])

    return result


def adf(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double[::1] theta, double theta_sigma,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col2, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]
    cdef int n_theta = len(theta)

    cdef int r12_symmetry_allowed = col1_mask == col2_mask

    cdef double r1, r2, r12_cos, angle

    theta_sigma = 1. / 2 / theta_sigma / theta_sigma

    for row in range(nrows,):
        if species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2:
                                col2 = r_indices[ptr2]
                                if species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        angle = acos(r12_cos)
                                        for dim in range(n_theta):
                                            out[dim] += exp(- (angle - theta[dim]) * (angle - theta[dim]) * theta_sigma)
