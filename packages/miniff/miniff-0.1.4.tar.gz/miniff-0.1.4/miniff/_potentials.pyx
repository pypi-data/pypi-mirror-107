# cython: language_level=2
import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport exp, cos, sin, pi, pow, sqrt, erfc
from cython.parallel import prange


out_shape = {}
coordination = {}
resolving = {}


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_general_2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, f, df_dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += f(r, row, col)
out_shape["kernel_general_2"] = "r"
coordination["kernel_general_2"] = 2
resolving["kernel_general_2"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_general_2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, f, df_dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = f(r, row, col)
                        # ---  grad  ---
                        g = df_dr(r, row, col)
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["kernel_g_general_2"] = "rrd"
coordination["kernel_g_general_2"] = 2
resolving["kernel_g_general_2"] = True


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_general_3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, f, df_dr1, df_dr2, df_dt,
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

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if False or species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if False or species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        # (no 'before' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (f(r1, r2, r12_cos, row, col1, col2))
out_shape["kernel_general_3"] = "r"
coordination["kernel_general_3"] = 3
resolving["kernel_general_3"] = True


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_g_general_3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, f, df_dr1, df_dr2, df_dt,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if False or species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # (no 'before1_grad' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if False or species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        # (no 'before' statements)
                                        # (no 'before_grad' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = f(r1, r2, r12_cos, row, col1, col2)
                                            # ---  grad  ---
                                            dfunc_dr1 = df_dr1(r1, r2, r12_cos, row, col1, col2)
                                            dfunc_dr2 = df_dr2(r1, r2, r12_cos, row, col1, col2)
                                            dfunc_dct = df_dt(r1, r2, r12_cos, row, col1, col2)
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2
out_shape["kernel_g_general_3"] = "rrd"
coordination["kernel_g_general_3"] = 3
resolving["kernel_g_general_3"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_harmonic_repulsion(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += epsilon * (r - a) * (r - a) / a / a / 2
out_shape["kernel_harmonic_repulsion"] = "r"
coordination["kernel_harmonic_repulsion"] = 2
resolving["kernel_harmonic_repulsion"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_harmonic_repulsion(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = epsilon * (r - a) * (r - a) / a / a / 2
                        # ---  grad  ---
                        g = epsilon * (r - a) / a / a
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["kernel_g_harmonic_repulsion"] = "rrd"
coordination["kernel_g_harmonic_repulsion"] = 2
resolving["kernel_g_harmonic_repulsion"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_harmonic_repulsion(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += epsilon * (r - a) * (r - a) / a / a / 2
out_shape["pkernel_harmonic_repulsion"] = "r"
coordination["pkernel_harmonic_repulsion"] = 2
resolving["pkernel_harmonic_repulsion"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_harmonic_repulsion(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = epsilon * (r - a) * (r - a) / a / a / 2
                        # ---  grad  ---
                        g = epsilon * (r - a) / a / a
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["pkernel_g_harmonic_repulsion"] = "rrd"
coordination["pkernel_g_harmonic_repulsion"] = 2
resolving["pkernel_g_harmonic_repulsion"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_lj(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, 
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += 4 * (pow(r, -12) - pow(r, -6))
out_shape["kernel_lj"] = "r"
coordination["kernel_lj"] = 2
resolving["kernel_lj"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_lj(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, 
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = 4 * (pow(r, -12) - pow(r, -6))
                        # ---  grad  ---
                        g = 4 * (- 12 * pow(r, -12) + 6 * pow(r, -6)) / r
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["kernel_g_lj"] = "rrd"
coordination["kernel_g_lj"] = 2
resolving["kernel_g_lj"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_lj(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, 
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += 4 * (pow(r, -12) - pow(r, -6))
out_shape["pkernel_lj"] = "r"
coordination["pkernel_lj"] = 2
resolving["pkernel_lj"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_lj(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, 
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = 4 * (pow(r, -12) - pow(r, -6))
                        # ---  grad  ---
                        g = 4 * (- 12 * pow(r, -12) + 6 * pow(r, -6)) / r
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["pkernel_g_lj"] = "rrd"
coordination["pkernel_g_lj"] = 2
resolving["pkernel_g_lj"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_sw_phi2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double gauge_a, double gauge_b, double p, double q,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += gauge_a * (gauge_b * r ** (-p) - r ** (-q)) * exp(1. / (r - a))
out_shape["kernel_sw_phi2"] = "r"
coordination["kernel_sw_phi2"] = 2
resolving["kernel_sw_phi2"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_sw_phi2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double gauge_a, double gauge_b, double p, double q,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = gauge_a * (gauge_b * r ** (-p) - r ** (-q)) * exp(1. / (r - a))
                        # ---  grad  ---
                        g = (- p * gauge_a * gauge_b * r ** (- p - 1) + gauge_a * q * r ** (- q - 1)) * exp(1. / (r - a)) - function_value / (r - a) / (r - a)
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["kernel_g_sw_phi2"] = "rrd"
coordination["kernel_g_sw_phi2"] = 2
resolving["kernel_g_sw_phi2"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_sw_phi2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double gauge_a, double gauge_b, double p, double q,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += gauge_a * (gauge_b * r ** (-p) - r ** (-q)) * exp(1. / (r - a))
out_shape["pkernel_sw_phi2"] = "r"
coordination["pkernel_sw_phi2"] = 2
resolving["pkernel_sw_phi2"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_sw_phi2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double gauge_a, double gauge_b, double p, double q,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = gauge_a * (gauge_b * r ** (-p) - r ** (-q)) * exp(1. / (r - a))
                        # ---  grad  ---
                        g = (- p * gauge_a * gauge_b * r ** (- p - 1) + gauge_a * q * r ** (- q - 1)) * exp(1. / (r - a)) - function_value / (r - a) / (r - a)
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["pkernel_g_sw_phi2"] = "rrd"
coordination["pkernel_g_sw_phi2"] = 2
resolving["pkernel_g_sw_phi2"] = True


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_sw_phi3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double l, double gamma, double cos_theta0,
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

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if False or species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if False or species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        # (no 'before' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (l * (r12_cos - cos_theta0) * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a))))
out_shape["kernel_sw_phi3"] = "r"
coordination["kernel_sw_phi3"] = 3
resolving["kernel_sw_phi3"] = True


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_g_sw_phi3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double l, double gamma, double cos_theta0,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if False or species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # (no 'before1_grad' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if False or species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        # (no 'before' statements)
                                        # (no 'before_grad' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = l * (r12_cos - cos_theta0) * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a)))
                                            # ---  grad  ---
                                            dfunc_dr1 = - function_value * gamma / (r1 - a) / (r1 - a)
                                            dfunc_dr2 = - function_value * gamma / (r2 - a) / (r2 - a)
                                            dfunc_dct = 2 * l * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a)))
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2
out_shape["kernel_g_sw_phi3"] = "rrd"
coordination["kernel_g_sw_phi3"] = 3
resolving["kernel_g_sw_phi3"] = True


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_sw_phi3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double l, double gamma, double cos_theta0,
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

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if False or species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if False or species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        # (no 'before' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (l * (r12_cos - cos_theta0) * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a))))
out_shape["pkernel_sw_phi3"] = "r"
coordination["pkernel_sw_phi3"] = 3
resolving["pkernel_sw_phi3"] = True


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_sw_phi3(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double l, double gamma, double cos_theta0,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 0 and col1_mask == col2_mask

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if False or species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        # (no 'before1' statements)
                        # (no 'before1_grad' statements)
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if False or species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        # (no 'before' statements)
                                        # (no 'before_grad' statements)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = l * (r12_cos - cos_theta0) * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a)))
                                            # ---  grad  ---
                                            dfunc_dr1 = - function_value * gamma / (r1 - a) / (r1 - a)
                                            dfunc_dr2 = - function_value * gamma / (r2 - a) / (r2 - a)
                                            dfunc_dct = 2 * l * (r12_cos - cos_theta0) * exp(gamma * (1 / (r1 - a) + 1 / (r2 - a)))
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2
out_shape["pkernel_g_sw_phi3"] = "rrd"
coordination["pkernel_g_sw_phi3"] = 3
resolving["pkernel_g_sw_phi3"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_mlsf_g2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double r_sphere, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    cdef int pre_compute_r_fn_handle = pre_compute_r_handles[0]
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fn_handle]
out_shape["kernel_mlsf_g2"] = "r"
coordination["kernel_mlsf_g2"] = 2
resolving["kernel_mlsf_g2"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_mlsf_g2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double r_sphere, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    cdef int pre_compute_r_fn_handle = pre_compute_r_handles[0]
    cdef int pre_compute_r_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fn_handle]
                        # ---  grad  ---
                        g = - 2 * eta * (r - r_sphere) * function_value + exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fp_handle]
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["kernel_g_mlsf_g2"] = "rrd"
coordination["kernel_g_mlsf_g2"] = 2
resolving["kernel_g_mlsf_g2"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_mlsf_g2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double r_sphere, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    cdef int pre_compute_r_fn_handle = pre_compute_r_handles[0]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fn_handle]
out_shape["pkernel_mlsf_g2"] = "r"
coordination["pkernel_mlsf_g2"] = 2
resolving["pkernel_mlsf_g2"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_mlsf_g2(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double r_sphere, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    cdef int pre_compute_r_fn_handle = pre_compute_r_handles[0]
    cdef int pre_compute_r_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fn_handle]
                        # ---  grad  ---
                        g = - 2 * eta * (r - r_sphere) * function_value + exp(- eta * (r - r_sphere) * (r - r_sphere)) * pre_compute_r[ptr, pre_compute_r_fp_handle]
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["pkernel_g_mlsf_g2"] = "rrd"
coordination["pkernel_g_mlsf_g2"] = 2
resolving["pkernel_g_mlsf_g2"] = True


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_mlsf_g5(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
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

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if False or species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if False or species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                        _fn_pw = pow(1 + l * r12_cos, zeta)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (_fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2)
out_shape["kernel_mlsf_g5"] = "r"
coordination["kernel_mlsf_g5"] = 3
resolving["kernel_mlsf_g5"] = True


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_g_mlsf_g5(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if False or species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if False or species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                        _fn_pw = pow(1 + l * r12_cos, zeta)
                                        _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            # ---  grad  ---
                                            dfunc_dr1 = - 2 * eta * r1 * function_value + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            dfunc_dr2 = - 2 * eta * r2 * function_value + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            dfunc_dct = zeta * l * pow(1 + l * r12_cos, zeta - 1) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2
out_shape["kernel_g_mlsf_g5"] = "rrd"
coordination["kernel_g_mlsf_g5"] = 3
resolving["kernel_g_mlsf_g5"] = True


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_mlsf_g5(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
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

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if False or species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if False or species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                        _fn_pw = pow(1 + l * r12_cos, zeta)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (_fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2)
out_shape["pkernel_mlsf_g5"] = "r"
coordination["pkernel_mlsf_g5"] = 3
resolving["pkernel_mlsf_g5"] = True


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_mlsf_g5(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if False or species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if False or species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                        _fn_pw = pow(1 + l * r12_cos, zeta)
                                        _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            # ---  grad  ---
                                            dfunc_dr1 = - 2 * eta * r1 * function_value + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            dfunc_dr2 = - 2 * eta * r2 * function_value + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            dfunc_dct = zeta * l * pow(1 + l * r12_cos, zeta - 1) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2
out_shape["pkernel_g_mlsf_g5"] = "rrd"
coordination["pkernel_g_mlsf_g5"] = 3
resolving["pkernel_g_mlsf_g5"] = True


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_mlsf_g4(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
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

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_cutoff3, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _r3, _r3_factor, g5_fun
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if False or species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if False or species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _r3 = sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * r12_cos)
                                        if _r3 < a:
                                            # --- before ---
                                            _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                            _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                            _fn_pw = pow(1 + l * r12_cos, zeta)
                                            g5_fun = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor = exp(-eta * _r3 * _r3) * (.5 + cos(pi * _r3 / a) / 2)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (g5_fun * _r3_factor)
out_shape["kernel_mlsf_g4"] = "r"
coordination["kernel_mlsf_g4"] = 3
resolving["kernel_mlsf_g4"] = True


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_g_mlsf_g4(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_cutoff3, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _r3, _r3_factor, g5_fun
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    cdef double _r3_factor_p, _r3_grad_r1, _r3_grad_r2, _r3_grad_cosine, g5_grad_r1, g5_grad_r2, g5_grad_cosine
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if False or species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if False or species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _r3 = sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * r12_cos)
                                        # (no 'before_grad' statements)
                                        if _r3 < a:
                                            # --- before ---
                                            _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                            _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                            _fn_pw = pow(1 + l * r12_cos, zeta)
                                            g5_fun = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor = exp(-eta * _r3 * _r3) * (.5 + cos(pi * _r3 / a) / 2)
                                            _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                            g5_grad_r1 = - 2 * eta * r1 * g5_fun + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            g5_grad_r2 = - 2 * eta * r2 * g5_fun + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            g5_grad_cosine = zeta * l * pow(1 + l * r12_cos, zeta - 1) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor_p = - 2 * eta * _r3 * _r3_factor - exp(- eta * _r3 * _r3) * sin(pi * _r3 / a) * pi / a / 2
                                            _r3_grad_r1 = (r1 - r2 * r12_cos) / _r3
                                            _r3_grad_r2 = (r2 - r1 * r12_cos) / _r3
                                            _r3_grad_cosine = - r1 * r2 / _r3
                                            # --- kernel ---
                                            function_value = g5_fun * _r3_factor
                                            # ---  grad  ---
                                            dfunc_dr1 = g5_grad_r1 * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_r1
                                            dfunc_dr2 = g5_grad_r2 * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_r2
                                            dfunc_dct = g5_grad_cosine * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_cosine
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2
out_shape["kernel_g_mlsf_g4"] = "rrd"
coordination["kernel_g_mlsf_g4"] = 3
resolving["kernel_g_mlsf_g4"] = True


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_mlsf_g4(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
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

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_cutoff3, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _r3, _r3_factor, g5_fun
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if False or species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if False or species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _r3 = sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * r12_cos)
                                        if _r3 < a:
                                            # --- before ---
                                            _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                            _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                            _fn_pw = pow(1 + l * r12_cos, zeta)
                                            g5_fun = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor = exp(-eta * _r3 * _r3) * (.5 + cos(pi * _r3 / a) / 2)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (g5_fun * _r3_factor)
out_shape["pkernel_mlsf_g4"] = "r"
coordination["pkernel_mlsf_g4"] = 3
resolving["pkernel_mlsf_g4"] = True


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_mlsf_g4(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta, double l, double zeta, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_cutoff3, _fn_exponent, _fn_pw
    cdef double _prefactor = pow(2, 1 - zeta) * epsilon
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp_fn_handle = pre_compute_r_handles[2]
    cdef double _r3, _r3_factor, g5_fun
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    cdef double _r3_factor_p, _r3_grad_r1, _r3_grad_r2, _r3_grad_cosine, g5_grad_r1, g5_grad_r2, g5_grad_cosine
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if False or species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if False or species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _r3 = sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * r12_cos)
                                        # (no 'before_grad' statements)
                                        if _r3 < a:
                                            # --- before ---
                                            _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                            _fn_exponent = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp_fn_handle]
                                            _fn_pw = pow(1 + l * r12_cos, zeta)
                                            g5_fun = _fn_pw * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor = exp(-eta * _r3 * _r3) * (.5 + cos(pi * _r3 / a) / 2)
                                            _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                            g5_grad_r1 = - 2 * eta * r1 * g5_fun + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            g5_grad_r2 = - 2 * eta * r2 * g5_fun + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            g5_grad_cosine = zeta * l * pow(1 + l * r12_cos, zeta - 1) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            _r3_factor_p = - 2 * eta * _r3 * _r3_factor - exp(- eta * _r3 * _r3) * sin(pi * _r3 / a) * pi / a / 2
                                            _r3_grad_r1 = (r1 - r2 * r12_cos) / _r3
                                            _r3_grad_r2 = (r2 - r1 * r12_cos) / _r3
                                            _r3_grad_cosine = - r1 * r2 / _r3
                                            # --- kernel ---
                                            function_value = g5_fun * _r3_factor
                                            # ---  grad  ---
                                            dfunc_dr1 = g5_grad_r1 * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_r1
                                            dfunc_dr2 = g5_grad_r2 * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_r2
                                            dfunc_dct = g5_grad_cosine * _r3_factor + g5_fun * _r3_factor_p * _r3_grad_cosine
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2
out_shape["pkernel_g_mlsf_g4"] = "rrd"
coordination["pkernel_g_mlsf_g4"] = 3
resolving["pkernel_g_mlsf_g4"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_sigmoid(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double r0, double dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += 1. / (1 + exp((r - r0) / dr)) * (.5 + cos(pi * r / a) / 2)
out_shape["kernel_sigmoid"] = "r"
coordination["kernel_sigmoid"] = 2
resolving["kernel_sigmoid"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_sigmoid(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double r0, double dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = 1. / (1 + exp((r - r0) / dr)) * (.5 + cos(pi * r / a) / 2)
                        # ---  grad  ---
                        g = - 1. / (1 + exp((r - r0) / dr)) * exp((r - r0) / dr) / dr * function_value - 1. / (1 + exp((r - r0) / dr)) * .5 * sin(pi * r / a) * pi / a
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["kernel_g_sigmoid"] = "rrd"
coordination["kernel_g_sigmoid"] = 2
resolving["kernel_g_sigmoid"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_sigmoid(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double r0, double dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += 1. / (1 + exp((r - r0) / dr)) * (.5 + cos(pi * r / a) / 2)
out_shape["pkernel_sigmoid"] = "r"
coordination["pkernel_sigmoid"] = 2
resolving["pkernel_sigmoid"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_sigmoid(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double r0, double dr,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if False or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = 1. / (1 + exp((r - r0) / dr)) * (.5 + cos(pi * r / a) / 2)
                        # ---  grad  ---
                        g = - 1. / (1 + exp((r - r0) / dr)) * exp((r - r0) / dr) / dr * function_value - 1. / (1 + exp((r - r0) / dr)) * .5 * sin(pi * r / a) * pi / a
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["pkernel_g_sigmoid"] = "rrd"
coordination["pkernel_g_sigmoid"] = 2
resolving["pkernel_g_sigmoid"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_ewald_real(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double[::1] charges,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in range(nrows,):
        if True or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if True or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += erfc(eta * r) / r * charges[row] * charges[col_] / 2
out_shape["kernel_ewald_real"] = "r"
coordination["kernel_ewald_real"] = 2
resolving["kernel_ewald_real"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms

def kernel_g_ewald_real(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double[::1] charges,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in range(nrows,):
        if True or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if True or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = erfc(eta * r) / r * charges[row] * charges[col_] / 2
                        # ---  grad  ---
                        g = (- eta * exp(- (r * eta) * (r * eta)) / sqrt(pi) * charges[row] * charges[col_] - function_value) / r
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["kernel_g_ewald_real"] = "rrd"
coordination["kernel_g_ewald_real"] = 2
resolving["kernel_g_ewald_real"] = True


# Template potential-2.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_ewald_real(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double[::1] charges,
    int[::1] species_row,
    int[::1] species_mask,
    double[::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r
    cdef int row_mask_, col_mask_, reverse

    # --- preamble ---
    # (no 'preamble' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if True or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if True or species_row[col_] == col_mask:
                    r = r_data[ptr]
                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # --- kernel ---
                        out[row] += erfc(eta * r) / r * charges[row] * charges[col_] / 2
out_shape["pkernel_ewald_real"] = "r"
coordination["pkernel_ewald_real"] = 2
resolving["pkernel_ewald_real"] = True


# Template potential-2-g.pyx
# A two-point potential: depends on the distance between pairs of atoms
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_ewald_real(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double[::1] charges,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    # Vars: indexing
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col, col_, dim
    cdef int ptr, ptr_fr, ptr_to
    cdef int row_mask = species_mask[0]
    cdef int col_mask = species_mask[1]

    cdef double r, function_value, g, x

    # --- preamble ---
    # (no 'preamble' statements)
    # (no 'preamble_grad' statements)
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if True or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr in range(ptr_fr, ptr_to):
                col = r_indices[ptr]
                col_ = cython.cmod(col, nrows)
                if True or species_row[col_] == col_mask:
                    r = r_data[ptr]

                    if r < a:
                        # --- before ---
                        # (no 'before' statements)
                        # (no 'before_grad' statements)
                        # --- kernel ---
                        function_value = erfc(eta * r) / r * charges[row] * charges[col_] / 2
                        # ---  grad  ---
                        g = (- eta * exp(- (r * eta) * (r * eta)) / sqrt(pi) * charges[row] * charges[col_] - function_value) / r
                        # --------------
                        for dim in range(3):
                            x = (cartesian_row[row, dim] - cartesian_col[col, dim]) / r * g
                            out[row, row, dim] += x   # df_self / dr_self
                            out[row, col_, dim] -= x  # df_self / dr_neighbor
out_shape["pkernel_g_ewald_real"] = "rrd"
coordination["pkernel_g_ewald_real"] = 2
resolving["pkernel_g_ewald_real"] = True


# Template potential-ewald-r-c.pyx
# Charge gradient of the real-space component

def kernel_c_ewald_real(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double[::1] charges,
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

    for row in range(nrows,):
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
out_shape["kernel_c_ewald_real"] = "rr"
coordination["kernel_c_ewald_real"] = 2
resolving["kernel_c_ewald_real"] = True


# Template potential-ewald-r-c.pyx
# Charge gradient of the real-space component
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_c_ewald_real(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double eta, double[::1] charges,
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

    for row in prange(nrows,nogil=True, schedule='static'):
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
out_shape["pkernel_c_ewald_real"] = "rr"
coordination["pkernel_c_ewald_real"] = 2
resolving["pkernel_c_ewald_real"] = True


# Template potential-ewald-k-g.pyx
# Ewald integration in k-space

def kernel_ewald_k(
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

    for k in range(nk, ):
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
out_shape["kernel_ewald_k"] = ""
coordination["kernel_ewald_k"] = 1
resolving["kernel_ewald_k"] = False


# Template potential-ewald-k.pyx
# Ewald integration in k-space

def kernel_g_ewald_k(
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
    for k in range(nk, ):
        for row in range(nrows):
            phase = 0
            for dim in range(3):
                phase = phase + k_grid[k, dim] * cartesian_row[row, dim]
            cs = cos(phase)
            sn = sin(phase)
            structure_factor[k, 0] += cs * charges[row]
            structure_factor[k, 1] += sn * charges[row]

    for row in range(nrows, ):
        for dim in range(3):
            for k in range(nk):
                phase = 0
                for dim1 in range(3):
                    phase = phase + k_grid[k, dim1] * cartesian_row[row, dim1]
                out[row, dim] += weights[k] * charges[row] * k_grid[k, dim] * (cos(phase) * structure_factor[k, 1] - sin(phase) * structure_factor[k, 0])
out_shape["kernel_g_ewald_k"] = "rd"
coordination["kernel_g_ewald_k"] = 1
resolving["kernel_g_ewald_k"] = False


# Template potential-ewald-k-g.pyx
# Ewald integration in k-space
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_ewald_k(
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

    for k in prange(nk, nogil=True, schedule='static'):
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
out_shape["pkernel_ewald_k"] = ""
coordination["pkernel_ewald_k"] = 1
resolving["pkernel_ewald_k"] = False


# Template potential-ewald-k.pyx
# Ewald integration in k-space
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_ewald_k(
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
    for k in prange(nk, nogil=True, schedule='static'):
        for row in range(nrows):
            phase = 0
            for dim in range(3):
                phase = phase + k_grid[k, dim] * cartesian_row[row, dim]
            cs = cos(phase)
            sn = sin(phase)
            structure_factor[k, 0] += cs * charges[row]
            structure_factor[k, 1] += sn * charges[row]

    for row in prange(nrows, nogil=True, schedule='static'):
        for dim in range(3):
            for k in range(nk):
                phase = 0
                for dim1 in range(3):
                    phase = phase + k_grid[k, dim1] * cartesian_row[row, dim1]
                out[row, dim] += weights[k] * charges[row] * k_grid[k, dim] * (cos(phase) * structure_factor[k, 1] - sin(phase) * structure_factor[k, 0])
out_shape["pkernel_g_ewald_k"] = "rd"
coordination["pkernel_g_ewald_k"] = 1
resolving["pkernel_g_ewald_k"] = False


# Template potential-ewald-k-c.pyx
# Ewald integration in k-space

def kernel_c_ewald_k(
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
    cdef int row, col, k, dim, dim1
    cdef double phase, sn, cs

    cdef double[::1] weights = np.linalg.norm(k_grid, axis=-1)
    cdef double prefactor = 4 * pi / (2 * volume) * 2
    for k in range(nk):
        weights[k] = prefactor * exp(-0.25 * weights[k] * weights[k] / eta / eta) / (weights[k] * weights[k])

    cdef double[:, ::1] structure_factor = np.zeros((k_grid.shape[0], 2), dtype=float)
    for k in range(nk, ):
        for row in range(nrows):
            phase = 0
            for dim in range(3):
                phase = phase + k_grid[k, dim] * cartesian_row[row, dim]
            cs = cos(phase)
            sn = sin(phase)
            structure_factor[k, 0] += cs * charges[row]
            structure_factor[k, 1] += sn * charges[row]

    for row in range(nrows, ):
        for k in range(nk):
            phase = 0
            for dim in range(3):
                phase = phase + k_grid[k, dim] * cartesian_row[row, dim]
            out[row] += (structure_factor[k, 0] * cos(phase) + structure_factor[k, 1] * sin(phase)) * weights[k]
out_shape["kernel_c_ewald_k"] = "r"
coordination["kernel_c_ewald_k"] = 1
resolving["kernel_c_ewald_k"] = False


# Template potential-ewald-k-c.pyx
# Ewald integration in k-space
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_c_ewald_k(
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
    cdef int row, col, k, dim, dim1
    cdef double phase, sn, cs

    cdef double[::1] weights = np.linalg.norm(k_grid, axis=-1)
    cdef double prefactor = 4 * pi / (2 * volume) * 2
    for k in range(nk):
        weights[k] = prefactor * exp(-0.25 * weights[k] * weights[k] / eta / eta) / (weights[k] * weights[k])

    cdef double[:, ::1] structure_factor = np.zeros((k_grid.shape[0], 2), dtype=float)
    for k in prange(nk, nogil=True, schedule='static'):
        for row in range(nrows):
            phase = 0
            for dim in range(3):
                phase = phase + k_grid[k, dim] * cartesian_row[row, dim]
            cs = cos(phase)
            sn = sin(phase)
            structure_factor[k, 0] += cs * charges[row]
            structure_factor[k, 1] += sn * charges[row]

    for row in prange(nrows, nogil=True, schedule='static'):
        for k in range(nk):
            phase = 0
            for dim in range(3):
                phase = phase + k_grid[k, dim] * cartesian_row[row, dim]
            out[row] += (structure_factor[k, 0] * cos(phase) + structure_factor[k, 1] * sin(phase)) * weights[k]
out_shape["pkernel_c_ewald_k"] = "r"
coordination["pkernel_c_ewald_k"] = 1
resolving["pkernel_c_ewald_k"] = False


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_mlsf_g5x(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta1, double eta2, double cos_theta0, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
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

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_exponent1, _fn_exponent2, _fn_pw
    cdef double _prefactor = epsilon / 4
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp1_fn_handle = pre_compute_r_handles[2], pre_compute_r_exp2_fn_handle = pre_compute_r_handles[3]
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if False or species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if False or species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent1 = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp1_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp2_fn_handle]
                                        _fn_exponent2 = _prefactor * pre_compute_r[ptr2, pre_compute_r_exp1_fn_handle] * pre_compute_r[ptr1, pre_compute_r_exp2_fn_handle]
                                        _fn_exponent = _fn_exponent1 + _fn_exponent2
                                        _fn_pw = (r12_cos - cos_theta0) * (r12_cos - cos_theta0)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (_fn_pw * (_fn_exponent1 + _fn_exponent2) * _fn_cutoff1 * _fn_cutoff2)
out_shape["kernel_mlsf_g5x"] = "r"
coordination["kernel_mlsf_g5x"] = 3
resolving["kernel_mlsf_g5x"] = True


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed

def kernel_g_mlsf_g5x(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta1, double eta2, double cos_theta0, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_exponent1, _fn_exponent2, _fn_pw
    cdef double _prefactor = epsilon / 4
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp1_fn_handle = pre_compute_r_handles[2], pre_compute_r_exp2_fn_handle = pre_compute_r_handles[3]
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in range(nrows,):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if False or species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if False or species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent1 = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp1_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp2_fn_handle]
                                        _fn_exponent2 = _prefactor * pre_compute_r[ptr2, pre_compute_r_exp1_fn_handle] * pre_compute_r[ptr1, pre_compute_r_exp2_fn_handle]
                                        _fn_exponent = _fn_exponent1 + _fn_exponent2
                                        _fn_pw = (r12_cos - cos_theta0) * (r12_cos - cos_theta0)
                                        _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = _fn_pw * (_fn_exponent1 + _fn_exponent2) * _fn_cutoff1 * _fn_cutoff2
                                            # ---  grad  ---
                                            dfunc_dr1 = - 2 * r1 * _fn_pw * (eta1 * _fn_exponent1 +  eta2 * _fn_exponent2) * _fn_cutoff1 * _fn_cutoff2 + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            dfunc_dr2 = - 2 * r2 * _fn_pw * (eta2 * _fn_exponent1 +  eta1 * _fn_exponent2) * _fn_cutoff1 * _fn_cutoff2 + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            dfunc_dct = 2 * (r12_cos - cos_theta0) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2
out_shape["kernel_g_mlsf_g5x"] = "rrd"
coordination["kernel_g_mlsf_g5x"] = 3
resolving["kernel_g_mlsf_g5x"] = True


# Template potential-3.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_mlsf_g5x(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta1, double eta2, double cos_theta0, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
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

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    cdef double r1, r2, r12_cos

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_exponent1, _fn_exponent2, _fn_pw
    cdef double _prefactor = epsilon / 4
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp1_fn_handle = pre_compute_r_handles[2], pre_compute_r_exp2_fn_handle = pre_compute_r_handles[3]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                if False or species_row[cython.cmod(col1, nrows)] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                if False or species_row[cython.cmod(col2, nrows)] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)
                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent1 = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp1_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp2_fn_handle]
                                        _fn_exponent2 = _prefactor * pre_compute_r[ptr2, pre_compute_r_exp1_fn_handle] * pre_compute_r[ptr1, pre_compute_r_exp2_fn_handle]
                                        _fn_exponent = _fn_exponent1 + _fn_exponent2
                                        _fn_pw = (r12_cos - cos_theta0) * (r12_cos - cos_theta0)
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # --- kernel ---
                                            out[row] += (1 + r12_symmetry_allowed * (ptr1 != ptr2)) * (_fn_pw * (_fn_exponent1 + _fn_exponent2) * _fn_cutoff1 * _fn_cutoff2)
out_shape["pkernel_mlsf_g5x"] = "r"
coordination["pkernel_mlsf_g5x"] = 3
resolving["pkernel_mlsf_g5x"] = True


# Template potential-3-g.pyx
# A three-point potential: depends on the distance between two pairs of atoms
# sharing the same atom at origin and the cosine of the angle formed
@cython.boundscheck(False)
@cython.wraparound(False)
def pkernel_g_mlsf_g5x(
    int[::1] r_indptr,
    int[::1] r_indices,
    double[::1] r_data,
    double[:, ::1] cartesian_row,
    double[:, ::1] cartesian_col,
    double a, double epsilon, double eta1, double eta2, double cos_theta0, double[:, ::1] pre_compute_r, int[::1] pre_compute_r_handles,
    int[::1] species_row,
    int[::1] species_mask,
    double[:, :, ::1] out,
):
    cdef int nrows = len(r_indptr) - 1
    cdef int row, col1, col1_, col2, col2_, dim
    cdef int ptr1, ptr2, ptr_fr, ptr_to, _ptr_fr
    cdef int row_mask = species_mask[0]
    cdef int col1_mask = species_mask[1]
    cdef int col2_mask = species_mask[2]

    cdef double r1, r2, r12_cos, function_value, dfunc_dr1, dfunc_dr2, dfunc_dct
    cdef double nx1, nx2, cx1, cx2

    cdef int r12_symmetry_allowed = 1 and col1_mask == col2_mask

    # --- preamble ---
    cdef double _fn_cutoff1, _fn_cutoff2, _fn_exponent, _fn_exponent1, _fn_exponent2, _fn_pw
    cdef double _prefactor = epsilon / 4
    cdef int pre_compute_r_cutoff_fn_handle = pre_compute_r_handles[0], pre_compute_r_exp1_fn_handle = pre_compute_r_handles[2], pre_compute_r_exp2_fn_handle = pre_compute_r_handles[3]
    cdef double _fp_cutoff1, _fp_cutoff2
    cdef int pre_compute_r_cutoff_fp_handle = pre_compute_r_handles[1]
    # ----------------

    for row in prange(nrows,nogil=True, schedule='static'):
        if False or species_row[row] == row_mask:
            ptr_fr = r_indptr[row]
            ptr_to = r_indptr[row + 1]
            for ptr1 in range(ptr_fr, ptr_to):
                col1 = r_indices[ptr1]
                col1_ = cython.cmod(col1, nrows)
                if False or species_row[col1_] == col1_mask:
                    r1 = r_data[ptr1]
                    if r1 < a:
                        # --- before ---
                        _fn_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fn_handle]
                        _fp_cutoff1 = pre_compute_r[ptr1, pre_compute_r_cutoff_fp_handle]
                        # --------------
                        _ptr_fr = ptr_fr
                        if r12_symmetry_allowed:
                            _ptr_fr = ptr1
                        for ptr2 in range(_ptr_fr, ptr_to):
                            if ptr1 != ptr2 or False:
                                col2 = r_indices[ptr2]
                                col2_ = cython.cmod(col2, nrows)
                                if False or species_row[col2_] == col2_mask:
                                    r2 = r_data[ptr2]
                                    if r2 < a:
                                        r12_cos = 0
                                        # (r1, r2)
                                        for dim in range(3):
                                            r12_cos = r12_cos + (cartesian_col[col1, dim] - cartesian_row[row, dim]) * (cartesian_col[col2, dim]- cartesian_row[row, dim])
                                        r12_cos = r12_cos / (r1 * r2)

                                        # --- before ---
                                        _fn_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fn_handle]
                                        _fn_exponent1 = _prefactor * pre_compute_r[ptr1, pre_compute_r_exp1_fn_handle] * pre_compute_r[ptr2, pre_compute_r_exp2_fn_handle]
                                        _fn_exponent2 = _prefactor * pre_compute_r[ptr2, pre_compute_r_exp1_fn_handle] * pre_compute_r[ptr1, pre_compute_r_exp2_fn_handle]
                                        _fn_exponent = _fn_exponent1 + _fn_exponent2
                                        _fn_pw = (r12_cos - cos_theta0) * (r12_cos - cos_theta0)
                                        _fp_cutoff2 = pre_compute_r[ptr2, pre_compute_r_cutoff_fp_handle]
                                        if True:
                                            # --- before ---
                                            # (no 'before_inner' statements)
                                            # (no 'before_inner_grad' statements)
                                            # --- kernel ---
                                            function_value = _fn_pw * (_fn_exponent1 + _fn_exponent2) * _fn_cutoff1 * _fn_cutoff2
                                            # ---  grad  ---
                                            dfunc_dr1 = - 2 * r1 * _fn_pw * (eta1 * _fn_exponent1 +  eta2 * _fn_exponent2) * _fn_cutoff1 * _fn_cutoff2 + _fn_pw * _fn_exponent * _fn_cutoff2 * _fp_cutoff1
                                            dfunc_dr2 = - 2 * r2 * _fn_pw * (eta2 * _fn_exponent1 +  eta1 * _fn_exponent2) * _fn_cutoff1 * _fn_cutoff2 + _fn_pw * _fn_exponent * _fn_cutoff1 * _fp_cutoff2
                                            dfunc_dct = 2 * (r12_cos - cos_theta0) * _fn_exponent * _fn_cutoff1 * _fn_cutoff2
                                            if r12_symmetry_allowed and ptr1 != ptr2:
                                                dfunc_dr1 = dfunc_dr1 * 2
                                                dfunc_dr2 = dfunc_dr2 * 2
                                                dfunc_dct = dfunc_dct * 2

                                            # Derivatives

                                            for dim in range(3):
                                                nx1 = (cartesian_row[row, dim] - cartesian_col[col1, dim]) / r1
                                                nx2 = (cartesian_row[row, dim] - cartesian_col[col2, dim]) / r2
                                                # d(cos θ) / dr = 1/r (n_s - n_r cos θ)
                                                cx1 = (nx2 - nx1 * r12_cos) / r1
                                                cx2 = (nx1 - nx2 * r12_cos) / r2

                                                out[row, row, dim] += nx1 * dfunc_dr1 + cx1 * dfunc_dct + nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_self
                                                out[row, col1_, dim] -= nx1 * dfunc_dr1 + cx1 * dfunc_dct  # df_self / dr_n1
                                                out[row, col2_, dim] -= nx2 * dfunc_dr2 + cx2 * dfunc_dct  # df_self / dr_n2
out_shape["pkernel_g_mlsf_g5x"] = "rrd"
coordination["pkernel_g_mlsf_g5x"] = 3
resolving["pkernel_g_mlsf_g5x"] = True
