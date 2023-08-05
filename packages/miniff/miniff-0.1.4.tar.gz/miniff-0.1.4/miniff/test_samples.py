import json
json.dumps
runner_input_sample = """
# UNITS: Bohr. Type 2 radial SFs and Type 3 angular SFs, see e.g. Eqs. 8 and 9 in https://doi.org/10.1063/1.3553717
#
# SAMPLE TYPE 2: global_symfunction_short 2 7.14214 0.0 11.338            ! type eta rshift funccutoff
# SAMPLE TYPE 3: global_symfunction_short 3 0.03571 -1.0 16.0  7.55891    ! type eta lambda zeta funccutoff
#
symfunction_short Ge 2 Ge 0.3 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff #
symfunction_short Te 2 Ge 0.3 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff #
symfunction_short Ge 2 Ge 0.2 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff
symfunction_short Ge 2 Te 0.2 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff
symfunction_short Te 2 Ge 0.2 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff
symfunction_short Te 2 Te 0.2 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff
symfunction_short Ge 2 Ge 0.07 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Ge 2 Te 0.07 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Te 2 Ge 0.07 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Te 2 Te 0.07 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Ge 2 Ge 0.03 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Ge 2 Te 0.03 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Te 2 Ge 0.03 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Te 2 Te 0.03 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Ge 2 Ge 0.01 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Ge 2 Te 0.01 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Te 2 Ge 0.01 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Te 2 Te 0.01 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Ge 2 Ge 0.001 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Ge 2 Te 0.001 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Te 2 Ge 0.001 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Te 2 Te 0.001 0.0 12.0 ! central_atom type neighbor_atom eta rshift funccutoff 
symfunction_short Ge 2 Ge 0.001 0.0 13.0 ! central_atom type neighbor_atom eta rshift funccutoff
symfunction_short Ge 2 Te 0.001 0.0 13.0 ! central_atom type neighbor_atom eta rshift funccutoff
symfunction_short Te 2 Ge 0.001 0.0 13.0 ! central_atom type neighbor_atom eta rshift funccutoff
symfunction_short Te 2 Te 0.001 0.0 13.0 ! central_atom type neighbor_atom eta rshift funccutoff
symfunction_short Ge 3 Ge Ge 0.2  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.2  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.2  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.2  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.2  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.2  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.2  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.2  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.2  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.2  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.2  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.2  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.2  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.2  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.2  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.2  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.2  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.2  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.2  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.2  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.2  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.2  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.2  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.2  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.2  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.2  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.2  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.2  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.2  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.2  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.2  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.2  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.2  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.2  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.2  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.2  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.2  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.2  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.2  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.2  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.2  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.2  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.07  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.07  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.07  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.07  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.07  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.07  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.07  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.07  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.07  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.07  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.07  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.07  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.07  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.07  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.07  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.07  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.07  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.07  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.07  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.07  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.07  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.07  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.07  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.07  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.07  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.07  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.07  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.07  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.07  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.07  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.07  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.07  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.07  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.07  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.07  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.07  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.07  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.07  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.07  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.07  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.07  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.07  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.07  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.07  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.07  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.07  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.07  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.07  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.03  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.03  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.03  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.03  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.03  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.03  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.03  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.03  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.03  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.03  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.03  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.03  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.03  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.03  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.03  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.03  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.03  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.03  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.03  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.03  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.03  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.03  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.03  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.03  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.03  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.03  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.03  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.03  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.03  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.03  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.03  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.03  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.03  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.03  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.03  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.03  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.03  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.03  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.03  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.03  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.03  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.03  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.03  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.03  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.03  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.03  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.03  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.03  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.01  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.01  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.01  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.01  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.01  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.01  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.01  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.01  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.01  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.01  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.01  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.01  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.01  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.01  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.01  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.01  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.01  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.01  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.01  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.01  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.01  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.01  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.01  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.01  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.01  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.01  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.01  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.01  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.01  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.01  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.01  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.01  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.01  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.01  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.01  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.01  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.01  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.01  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.01  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.01  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.01  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.01  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.01  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.01  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.01  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.01  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.01  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.01  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  -1.0  1.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  1.0  4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  -1.0 4.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  1.0  2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  -1.0 2.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  1.0  16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  -1.0 16.0 12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  -1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  -1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  -1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  -1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  -1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  -1.0  1.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  1.0  4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  1.0  4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  1.0  4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  1.0  4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  1.0  4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  1.0  4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  -1.0 4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  -1.0 4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  -1.0 4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  -1.0 4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  -1.0 4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  -1.0 4.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  1.0  2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  1.0  2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  1.0  2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  1.0  2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  1.0  2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  1.0  2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  -1.0 2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  -1.0 2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  -1.0 2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  -1.0 2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  -1.0 2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  -1.0 2.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  1.0  16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  1.0  16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  1.0  16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  1.0  16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.001  -1.0 16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Ge 0.001  -1.0 16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Te Te 0.001  -1.0 16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.001  -1.0 16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Ge 0.001  -1.0 16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Te Te 0.001  -1.0 16.0 13.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.3   1.0  1.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff ##
symfunction_short Te 3 Ge Ge 0.3   1.0  1.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.3  -1.0  1.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.3  -1.0  1.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.3   1.0  4.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.3   1.0  4.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.3   1.0  2.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.3   1.0  2.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Ge 3 Ge Ge 0.3  -1.0  2.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
symfunction_short Te 3 Ge Ge 0.3  -1.0  2.0  12.0  ! central_atom type neighbor_atom1 neighbor_atom2 eta lambda zeta funccutoff
"""

lammps_nnp_sample = """
ELEM_LIST Si O

POT Si 6.0
SYM 70
2 6.0 0.003214 0.0 0.0 Si
2 6.0 0.035711 0.0 0.0 Si
2 6.0 0.071421 0.0 0.0 Si
2 6.0 0.124987 0.0 0.0 Si
2 6.0 0.214264 0.0 0.0 Si
2 6.0 0.357106 0.0 0.0 Si
2 6.0 0.714213 0.0 0.0 Si
2 6.0 1.428426 0.0 0.0 Si
2 6.0 0.003214 0.0 0.0 O
2 6.0 0.035711 0.0 0.0 O
2 6.0 0.071421 0.0 0.0 O
2 6.0 0.124987 0.0 0.0 O
2 6.0 0.214264 0.0 0.0 O
2 6.0 0.357106 0.0 0.0 O
2 6.0 0.714213 0.0 0.0 O
2 6.0 1.428426 0.0 0.0 O
4 6.0 0.000357 1.0 -1.0 Si Si
4 6.0 0.028569 1.0 -1.0 Si Si
4 6.0 0.089277 1.0 -1.0 Si Si
4 6.0 0.000357 2.0 -1.0 Si Si
4 6.0 0.028569 2.0 -1.0 Si Si
4 6.0 0.089277 2.0 -1.0 Si Si
4 6.0 0.000357 4.0 -1.0 Si Si
4 6.0 0.028569 4.0 -1.0 Si Si
4 6.0 0.089277 4.0 -1.0 Si Si
4 6.0 0.000357 1.0 1.0 Si Si
4 6.0 0.028569 1.0 1.0 Si Si
4 6.0 0.089277 1.0 1.0 Si Si
4 6.0 0.000357 2.0 1.0 Si Si
4 6.0 0.028569 2.0 1.0 Si Si
4 6.0 0.089277 2.0 1.0 Si Si
4 6.0 0.000357 4.0 1.0 Si Si
4 6.0 0.028569 4.0 1.0 Si Si
4 6.0 0.089277 4.0 1.0 Si Si
4 6.0 0.000357 1.0 -1.0 Si O
4 6.0 0.028569 1.0 -1.0 Si O
4 6.0 0.089277 1.0 -1.0 Si O
4 6.0 0.000357 2.0 -1.0 Si O
4 6.0 0.028569 2.0 -1.0 Si O
4 6.0 0.089277 2.0 -1.0 Si O
4 6.0 0.000357 4.0 -1.0 Si O
4 6.0 0.028569 4.0 -1.0 Si O
4 6.0 0.089277 4.0 -1.0 Si O
4 6.0 0.000357 1.0 1.0 Si O
4 6.0 0.028569 1.0 1.0 Si O
4 6.0 0.089277 1.0 1.0 Si O
4 6.0 0.000357 2.0 1.0 Si O
4 6.0 0.028569 2.0 1.0 Si O
4 6.0 0.089277 2.0 1.0 Si O
4 6.0 0.000357 4.0 1.0 Si O
4 6.0 0.028569 4.0 1.0 Si O
4 6.0 0.089277 4.0 1.0 Si O
4 6.0 0.000357 1.0 -1.0 O O
4 6.0 0.028569 1.0 -1.0 O O
4 6.0 0.089277 1.0 -1.0 O O
4 6.0 0.000357 2.0 -1.0 O O
4 6.0 0.028569 2.0 -1.0 O O
4 6.0 0.089277 2.0 -1.0 O O
4 6.0 0.000357 4.0 -1.0 O O
4 6.0 0.028569 4.0 -1.0 O O
4 6.0 0.089277 4.0 -1.0 O O
4 6.0 0.000357 1.0 1.0 O O
4 6.0 0.028569 1.0 1.0 O O
4 6.0 0.089277 1.0 1.0 O O
4 6.0 0.000357 2.0 1.0 O O
4 6.0 0.028569 2.0 1.0 O O
4 6.0 0.089277 2.0 1.0 O O
4 6.0 0.000357 4.0 1.0 O O
4 6.0 0.028569 4.0 1.0 O O
4 6.0 0.089277 4.0 1.0 O O
scale1 2.9579656875347435 2.010843911436129 1.3495712305969263 0.7817472414666415 0.3489072530470396 0.11399988737047898 0.00924739247215519 9.584104375607371e-05 7.774219358230172 5.764453085149254 4.389666262299411 3.165732341362819 2.077873223062988 1.245695101371358 0.4636364147983903 0.07232442585114009 0.3812011155346391 0.1434745844881319 0.023403777255425286 0.16389713643019824 0.06059516435158661 0.00891095818231492 0.061336578427146134 0.021809582108696383 0.0025578350323371963 0.9895534920860073 0.3788966932782315 0.0583354344929603 0.752892271172336 0.28692013098302677 0.043911391730312666 0.47886227639872103 0.17870198029774542 0.026844075218332784 3.281349015538932 1.4813385578524763 0.3371738874834447 1.5918161967556546 0.7056008081120456 0.15342809714331285 0.6488915076329849 0.2933351087673367 0.06286393049837462 10.567986066071683 5.164962507568603 1.4275133656797596 8.907158312726114 4.412134633993789 1.2456217879963911 7.074065983754059 3.5525069120301085 1.0217442037527285 6.284708699682017 3.4999429134432525 1.208591340628263 3.4365936328448434 1.946377967349492 0.7153627692922615 1.5124113549487361 0.8455098426200129 0.31570208231575536 10.142995505991525 4.996164045810176 1.344266891149485 7.299002190203092 3.450526616467828 0.8453518976281063 4.776128286479814 2.13775951625911 0.456840089571652
scale2 0.7019746179904176 0.530114971386907 0.40562997229952297 0.2792499782562679 0.16943875861884494 0.07751220698546049 0.008474439109556121 9.544944887929373e-05 1.2749263544243101 0.9448485300103253 0.7499181949326281 0.523664236216675 0.3172130568693806 0.23331075156191683 0.15912826882845993 0.04253553269907462 0.25474751775595805 0.10413466066977439 0.020554965591595455 0.12448246500207036 0.04901896646525309 0.008025324312684618 0.053576467331055956 0.019694063170021908 0.0024166944860470464 0.6115737353687977 0.2683973365806247 0.050668810794732747 0.46213283576136105 0.20285164311961046 0.03792916639282472 0.2780648739730588 0.12125173453844179 0.02268534119395787 1.5325425429469761 0.783051065073887 0.231736862737021 0.7439531077022226 0.37239793938606913 0.10479166734572663 0.327698247612619 0.16505363278660387 0.04463322616699897 3.9889695842829704 2.081952202116451 0.6790674872060265 3.1841897826949035 1.6787223717991542 0.5565997757064516 2.2108567041812415 1.1849644111829074 0.4121426618624854 2.151024827978146 1.147149247188126 0.4212342381472021 1.0773229325016616 0.5782373873391401 0.24838245261008424 0.49859989751320355 0.2551602799230097 0.108958339613821 3.7358660909102976 2.000627548609364 0.6238832770260091 2.7188937298476596 1.4237881720089682 0.4260905244548197 1.6836981938129538 0.8504394905729515 0.23011416729268985
NET 2 30 30 1
LAYER 0 sigmoid
w0 0.40744139431009757 0.13768315682109994 -0.41171463441504846 0.12437936137365513 0.597557209310046 0.06661007331652251 -0.1255049582086713 -0.5164935115266303 0.4802741316135833 -0.515212238292995 -0.5407462162689778 -1.2531064634861004 -0.7108620157523313 -0.18236544100321683 1.5333719816093871 -0.8835000267084904 -0.10952933265525924 0.12140314345949771 0.6974951612419933 0.08383085434163237 0.10506586677770526 0.7679212997162511 0.4539558625686496 0.06995872838141494 0.17954883629652743 -0.039782323406706684 0.6239942264927505 0.9454892264932152 1.0500582610128184 0.044308483073165685 0.5740790199015696 0.3919558231198251 0.7130098217340705 -0.15414945229840302 -0.4290051292568588 -0.4587496659934259 -0.09181424751424923 -0.26395615699740227 0.41081572567080177 -0.0567632165242752 -0.32012714494284317 0.23733152533044938 0.14166657978890929 -0.17503599199361983 -0.6556247441941859 0.014265596454818955 0.025814013063308598 0.08309596656996181 0.5916870080126305 0.22905812789377447 0.07882893040620621 0.42533874911589303 -0.4454505274473572 -0.7019922788362966 -0.048999207311888976 -0.33445217160658125 0.28606951769107825 1.2298580066422178 -0.44080491300825736 -1.3237400864388456 0.7032642518358109 0.3968916567798686 -0.2809783377129947 -0.5188153373113948 0.18888533372055386 0.05949670562354298 -0.07370830054877887 1.5066920690959793 2.7208689589596893 0.5926527618353189
b0 -0.746235202531
w1 0.4512867430429476 -0.14356253511388983 -0.26853382122004127 -0.5372101875640588 -0.26705758026892845 -0.1652896449147737 -0.19455220896338565 -0.15790162862502263 -0.7172818804857788 0.1105449827035709 -0.23350244112317659 -0.5055120277991126 -0.35860884721307035 0.5411507911107253 0.9121832791564451 -0.2714122985645769 0.1676066311610856 -0.07878764468394951 -0.11910473870870962 0.3844097681352091 -0.14212076328881032 0.06763315261465425 -0.4609144458094434 -0.11017123135542994 -0.058649171758832754 0.34607484185578025 0.2541441536353354 0.29096978634719034 -0.10851674697690197 0.008520577761121003 0.38924951361732435 -0.005856114917067266 0.5685438320417817 0.02949682386857174 -0.1794331125136195 0.08618311645625525 0.23461679273063699 -0.26107348223750626 -0.03507724254712063 -0.42270458049377013 0.17517876605720706 -0.2764188847539771 -0.4757822898908005 -0.27396927780609004 -0.38154800446500076 -0.40030712314723255 -0.07564260900627806 -0.46673204115724115 -0.2721973681607748 0.40883299168979037 -0.19536096149975754 0.4198045783474863 -0.6596149803186754 -0.0780305863609437 0.6043109569744926 -0.2968349139632566 0.2873511106266065 1.5732299654282949 -0.7840369149629767 0.07755784414189651 1.0764846307508529 0.2232881116155737 -0.0861184686552204 -0.04130316861560915 0.012970867734656806 -0.05758575204371245 -0.3296715786923992 0.25759745656434435 -0.24152814714901866 0.554863486047489
b1 -0.161302735825
w2 0.008497103729982983 -0.1677057716500474 0.04716101247579812 0.27162322774528225 0.020181122000226398 -0.11360966869322617 0.12750308688905237 0.11509131391743885 0.2279295890737934 0.22001897719564897 -0.37818713554844385 -0.1041471711218197 0.5743790344523405 0.3052477659250601 0.23425708487508848 -1.4237855657512632 -0.1757979968976501 0.02527155876603769 0.26561630071412384 -0.22238243285865922 -0.2787519413124316 0.17234828935201935 0.5466443805106914 0.23037978051233393 -0.20412330833070538 0.39612336453153685 -0.05907966602072016 0.15878812355149355 0.24033702071358426 0.14629758019057348 0.03643031540006915 0.2713147657976374 0.3665919428127249 -0.3015643533416529 -0.2569869176191595 0.5286696119604417 -0.06977801847541047 -0.012270894548855984 0.07126501541342625 -0.11100542755942933 0.05487771735066558 0.23768998187104481 0.3079331259588669 -0.3026186363162394 0.02306295802633314 -0.6006833443958048 -0.20127391533345784 0.4526420816964889 -0.13763506034566347 -0.0992164457210479 0.09667380453736604 0.16504167486965735 -0.2091459495601082 -0.048004672464142015 0.8592771285333447 0.3675238340313047 -0.18575090662425886 1.9609184802623143 -0.6189984261145017 -0.4925631781834688 0.18525042442279688 -0.19115279096518767 -0.18388595553739703 -0.4191401559594896 0.10881550785147752 -0.3140973120357375 -0.4236444371852962 0.19467491519549407 0.2815997220740394 -0.7756099944197534
b2 -0.203464798763
w3 0.025047696118872035 -0.5793568721245027 0.14970827157707137 -0.03686465666565098 0.17495911232011802 -0.14416013566334154 0.1811931931691327 0.020940143877192247 0.19888847512867258 0.00147807820049786 -0.11407333657039746 0.07886937258771556 -0.3019810442412452 0.3601725146372147 -0.036698366269913595 -0.9706429182741133 -0.15013746823995527 0.26217404954679857 -0.09246596597651413 -0.3208354648999581 0.2616999923017473 0.3553187708193784 -0.119476612025423 0.23101972926388623 -0.3124390390824912 -0.5861876958610285 -0.01072894908810143 0.33079944240889486 -0.2745142197325808 -0.640322197047555 -0.32589433047188643 -0.3602231533537314 0.256054208614795 -0.2617636285108845 0.19092302850256765 0.3690076087302131 0.238404838408034 0.3210353890730659 -0.09251969017123113 0.157883710685106 -0.2575691116047251 -0.08484533255209113 0.0678744227237271 0.1170265877558412 -0.22958215856735711 -0.3278180025771284 -0.21320697344242345 -0.5086914455957728 0.028950946938620676 0.16124894983272853 0.07883412262545474 -0.19629407388694015 -0.040375357882967186 -0.026364115127248372 0.04546538629371997 0.47919378550895275 0.263186905095257 1.0217277131783726 -0.3654030708479774 -0.7754074871201438 0.1034583944419719 0.05863795191356102 -0.28548136784335076 -0.14877068606814714 0.15781238706179604 0.1996963532550751 -0.29041759682660545 -0.24363520250549636 0.6903346870600213 0.11987401645340852
b3 0.183338754438
w4 0.06317138405024737 0.10848628770243911 0.021034038707702304 -0.15625090656254728 0.1029740211593916 0.340736167260211 0.18171910388929413 0.1287670193030977 -0.20078991078097883 0.4452951780100261 -0.14181709363929512 -0.27533769259250446 0.7390271081013788 0.25922027932209923 -0.17690251692747 0.9271464454103386 0.49752296370867094 0.10245321442747206 0.19808166674856514 -0.35810352367433956 0.03874455987434413 0.1438407961022001 0.4098250413792784 0.05595693887246683 0.12311517085708226 -0.0944165986000062 0.09144103669408894 -0.050302424732911265 -0.2505261875152163 0.27680203874626286 -0.1856927266073316 0.43894189669180694 -0.31785201648245703 0.16600994901563648 -0.0692508729052401 -0.10127007315673428 0.2184309044963101 -0.16428159372113152 -0.18810337584484926 -0.15898902668254475 0.2087361947838775 0.1314840403257691 0.3266697512919719 -0.018332661926631473 0.7436264654251203 0.23745605097620687 -0.0212771478789797 0.3354387152140505 0.6043083139465808 0.03316398420310382 0.01608989586415869 -0.024240991725446755 0.00684659098815106 0.013460840446027397 -0.28688462988433644 -0.22125462216166022 -0.26078625300667146 -1.413628515525289 -0.006272814482505934 0.7493912991962962 0.17353793229093645 0.3657217264957798 -0.0997204602020744 -0.1637362352168408 -0.16803500242122565 -0.2881844583744725 0.06007531637247218 -0.19026375494590309 -0.6860961044695296 -0.6566844627894863
b4 0.163589302199
w5 -0.2822973089625541 -0.16198446734821523 -0.12964669180152183 0.4073168351896695 0.29164270022290545 -0.43228252950345597 0.022670885858004503 -0.2839240977581945 -0.09809579884078508 0.21245904473629107 -0.3931463758685466 0.20557808172108932 0.020725074877542216 0.15482168094028975 -0.3361361221262362 -1.540365244962401 0.5359948172258693 0.5296361170911212 0.007812761676198285 -0.024678976154923753 0.14457161794955664 0.33672762825677643 0.23318858218328378 0.15325982475101402 0.25456564932474357 -0.37179212003584955 0.5898457790443746 -0.3936158144991789 -0.057902008207019406 0.19452012071426916 0.4535556861911363 -0.37825217693101254 0.23077618622005147 -0.3676175302669985 0.0355874808447082 -0.041848571637558465 0.34773931389012613 -0.2464238674614718 -0.17093293024687603 -0.2092814624071387 0.5172845042009278 0.24030910830667504 0.4214263989386001 -0.3598118946411718 0.11624190085103871 -0.55494197821692 -0.264735536201168 -0.3162347328170669 0.1406048411694456 -0.008461712714822746 -0.13077626949485513 -0.333656552831296 0.07990743194450828 0.28428254277433435 0.44669601889409843 -0.18103776077098152 0.07756150768997205 2.193493524358605 -0.4132484973568365 -0.6185366892911409 0.29936094695810433 0.4439280931703336 -0.10085492229624818 -0.5569948121615893 -0.223988350611615 -0.34953382213124956 -0.5622551639809465 0.11173285974168222 0.20099632515726423 0.18461525851360358
b5 -0.346252293686
w6 0.08689224177640807 -0.2048235489699244 0.17810639350077018 -0.17095688513942575 -0.12257946888477601 0.04982358729858277 -0.5352205627882153 -0.15967084581087287 0.23417267198509614 -0.24435426291256976 0.08631553513226367 0.2390168711174784 0.6665640942336035 0.01765159828800634 0.21885331909870862 -1.3689808833844863 -0.13583218440792816 -0.08634634208359628 0.08032348345262215 -0.41561024750562797 -0.3630677495488284 0.025102312119081642 0.22434835444927195 0.12613678040679852 0.03163324289665337 0.06703810520590414 0.09653534447526917 -0.008544302592673452 0.23337772784119898 -0.2537496708705479 0.24899449005133736 0.16154854883999922 0.021623047753190138 -0.015416865762056748 -0.08126402962658263 -0.08521710332416056 -0.004423921389055075 0.4218868896366467 0.4071822483991456 0.31675486434083955 0.2800245518682481 0.3704467195447274 -0.20044650040210854 -0.3676408825352283 0.09220061287462696 0.06233627344841322 -0.5158997300829219 -0.15485517935070434 -0.13201044852095767 -0.07301495572223256 -0.23570622523395557 -0.24288473327991145 0.08258388359054164 -0.09791305137092911 0.8789156169025578 -0.12452025454946908 0.3881885416537624 1.423411484084087 -0.6152350401799994 -0.1156491131968845 0.7450463764619839 0.2612807698873273 0.23199188158286912 -0.43056633596968286 0.29114854895717346 -0.20895800726838137 -0.3974588060261887 0.2324090859123065 0.3991252910824461 -0.4943222853274498
b6 -0.485618670673
w7 -0.17179678771665083 -0.33991629378379035 -0.10346496207723326 -0.35643060741849847 0.5341104635087233 -0.028792302830310944 -0.20903563860702504 -0.05766540430979307 -0.1950018963214288 0.29046529484213085 -0.029185038349516017 -0.36918529366341557 -0.22968177693646774 0.17749455796336924 0.4176506913720452 -1.3463117002006548 0.3730615728155513 0.2109466727259315 0.14002538324922298 0.1980515047630689 -0.09523283769772839 -0.45525408334849354 -0.04156293925581931 0.23723544987210443 0.07890247334415916 -0.006435616417433265 -0.4706587227473778 -0.00978322305455893 0.31416503497532344 0.12649478080422621 0.2172000333395557 -0.02343303965445596 0.06842103529840818 0.12219218552610021 -0.33658588492023034 0.18254358774628612 -0.2026021488798507 0.5065719893397651 0.16747116494918596 0.49375370369976007 -0.25139381417666284 -0.09287642379210666 0.2612441589872156 -0.039980785835215256 0.2757892318644364 0.13645959666250493 -0.058353759893368704 -0.10909331240151436 -0.17793301872611486 0.12595736606312466 0.047913851904332984 0.23201119103541065 0.037922756493945775 -0.2845626322953201 0.3098344486604198 -0.12344246059434659 0.36181678084568 1.8673527114758268 -0.01477431073820887 -0.3082438535883194 0.40571636019878665 -0.005301209352812958 -0.3456273679058899 -0.15348605656473963 0.10283766171267733 -0.31984913645916296 -0.5153523983709659 -0.3277621497366862 0.35400975318451017 0.3672560315394146
b7 -0.490209426062
w8 -0.058747916388133925 0.046326630434168 -0.062268624951558535 0.3677210823760302 -0.04391596028116216 -0.04997505355377067 0.08083204218890899 -0.2868802662308894 0.28239879799483275 0.09556546980307593 -0.4560474729549658 -0.266578241475798 0.4667835121309519 0.40156469030845804 -0.010100446931912067 -1.5837540860900543 -0.0670416487541166 -0.10038361247413827 -0.02296581583854822 0.05375992680193554 0.18134465275755637 -0.08811870983385378 -0.3416761965095762 0.3903591594644839 -0.039792116289422565 -0.32855378419874154 -0.33082179049616073 -0.35041763859759717 -0.046990930982062494 -0.1281394744354123 0.3094293191020667 0.16970428090901507 0.252406209665952 0.5249172085795744 0.06845049552810967 -0.3882198534714515 -0.4356793950803771 0.26286457934102386 0.11071022408885811 0.40939754168354786 -0.23448351788756222 0.3222537919746198 0.5512481241164767 -0.13697623825793265 0.4962696799743578 -0.126921660256648 0.4767402866039907 0.19960358768987146 0.3240955433257102 -0.02562804379113955 0.23907696222852262 -0.18646658448808823 -0.014304877557102408 -0.003954921649579088 0.15545623588812083 0.020962758989930573 0.2371943195603505 1.4616002433499007 -0.22216570506295455 -0.39323237925263116 0.5942654778736041 -0.22960776706757163 -0.15753213844517847 -0.7470888979977325 0.08233738991803961 0.005552192506206861 -0.5428064615340095 -0.2815041309794761 0.2752401392612884 -0.3041958184770564
b8 -0.290532794154
w9 -0.021217578391149225 -0.4285761484469761 -0.23593253230078665 0.32630138616948373 -0.1396622432188763 -0.03462068133644772 -0.46414977293816495 0.0009436648571146829 0.016732586509667403 0.049598099930167026 0.10646518835904978 0.2774015329629388 0.2992670050763437 0.3797132290128569 1.4023538877361035 -0.5860991298283881 0.029890810753730696 0.2526677591350055 -0.0846562596930261 -0.38741675448347274 -0.13395357286567466 -0.2852885751959221 -0.05760729546361017 -0.29075876626733954 -0.04873290275686666 -0.09280104985747942 0.3014562483297586 -0.41302554633552613 0.2458890390451654 -0.08116942311888761 0.3919053067515196 0.37031562542434754 -0.32872344852229807 -0.14855159292734027 -0.016867001729430998 0.3490202070088971 0.6787808461445168 0.18303212588386614 0.8347497568571541 0.13237544051287864 0.5464678554726974 0.33207156618589223 0.31172615332486886 0.1850722821367088 0.2997848571460357 0.03552055512538679 -0.22404661978654394 0.7169735417288956 0.6987078653509461 0.3632365069886478 -0.2905482187880336 0.2133884714819136 0.08926122936658638 0.3301113063990022 0.7234890299909555 0.2942253207598491 1.2808750620083902 2.4258070065404844 -0.2697503512268489 -0.19977290875489198 0.8922411378745665 -0.34479811058547505 0.02342888721314705 -0.49860084631726925 -0.3253233158341982 -0.43423455978486347 -0.35936858736028454 0.35589452302002617 0.4596945951014293 0.0861087691411939
b9 -0.108930733978
w10 0.06279316490005947 0.22861272184144305 -0.3094704488968226 0.006143236826253102 0.26311287115706466 -0.20917265431863608 -0.13867274674169539 -0.604213202301934 -0.10725967211622871 -0.17201440581720978 0.5800761115103826 0.4966815338359337 0.13389067875860303 -0.15817679129907888 -0.4900392171370212 -1.7427334357600086 0.05358722642164508 -0.1257905854210317 -0.142265598951419 -0.17446206337854098 -0.42379913517170775 0.11470860749963449 -0.4517474526834488 0.09288175205135539 0.06957759450959727 0.05965268545067206 0.1986594400759101 0.23004049668323068 0.12278409347134488 -0.004020868823785669 0.3448380951120304 -0.15904897034519785 -0.056002983834436706 -0.20874540858062585 -0.03290738476978696 0.10010446690690562 0.06773593462412542 0.49796869432207297 0.43634126972278786 0.1804026789443658 0.2561804123081654 -0.08549464413945515 -0.013640469002473747 -0.07596986054282871 0.5364243129458959 -0.2298585746435276 -0.18932843147613648 -0.3832270213516919 -0.37734547079463093 -0.2671911529290947 0.512149915467431 -0.2812516740175555 -0.08880791220250815 0.4305274758401326 0.6711293703678325 0.10600150328602613 0.4199714485407727 1.346791422237659 -0.35423257542767245 -0.8470203178845546 0.4944286434821331 0.032848204354942165 -0.29493988461226833 -0.38654264487178336 0.4671385963803798 -0.16679714207706156 -0.5202352531663661 0.1218604943825315 0.2028893720055954 0.06935536357218546
b10 -0.520214274626
w11 -0.30250275163472484 0.268267898929261 0.5390009117393416 -0.3336217220314848 -0.20598969633083342 -0.17681127804598493 0.002951872335413204 0.6163442891156315 0.21195307242656336 -0.302538805160575 -0.0436933121349304 -0.028507445431739123 0.2524327917271755 -0.41134181920289686 -0.7228982780510699 0.7222863036304983 0.17502685559456507 0.45866395028428086 0.23793666023573593 0.2007620972943817 0.1598399688942226 0.10223526399186056 -0.10311384097635296 0.16406081098275935 -0.22387282252406746 -0.19386133486218424 0.24328634421966094 -0.20866328008848917 -0.4061584565972945 -0.43847471610913463 0.1842825301922239 0.06222509331503063 0.35823013997905384 -0.4177850750032821 0.03372342257942123 0.09179501671987375 0.05982412364093832 0.3866719255293254 0.328191083289553 0.1772913076576372 0.06965144841730155 -0.22182095289760403 0.0467054109905043 -0.11715437732840736 0.36741495267167645 -0.07777930196732637 0.2061261231173387 0.15646251550261955 0.08439241806806513 0.3542723286616871 0.5671023796262384 0.4696859669661107 0.3558844188100877 0.26558393089527993 -0.1290678498806407 -0.031029519793258246 -0.24998763144669275 -1.4885341920299666 0.12948506823444508 0.501091329455123 -0.5353018033815877 0.3542495393468994 0.13499788971307003 -0.14928094652529172 0.37953980841108936 -0.3195110235299174 -0.0654250588493479 -0.08789826216843293 -0.4233256146364855 -0.478167686695388
b11 0.258686451403
w12 -0.008474536201213289 -0.3436995681685059 0.09678643093812639 -0.02097228357940603 0.26489419131026215 -0.10461294218223217 -0.2256461117688431 0.10824550489508017 -0.4505763332044523 -0.14430003839011654 0.0009178643292569197 -0.18135027840615167 -0.253073616641387 0.034731125335198815 -0.010074632875034378 -0.9593430123545058 0.0006653315445121305 -0.27270198913559723 0.2209380094186014 0.4408953529032497 0.4897341739029701 -0.15951667608380876 0.29993328188261226 0.42062773438973583 0.31320316914548935 0.026284024118507915 0.03562252980806578 -0.09797555940250126 -0.5643775894375118 -0.33535246334419494 -0.5647547326233279 0.23405833117773897 0.3210590443042788 -0.15481792069729344 -0.15513776323544876 0.010073750954010993 -0.20738583690465584 -0.03514594625914239 0.1508903614938658 0.469382198972346 -0.39409501714843836 -0.6525301168770834 -0.2667404328103066 -0.5723805984243105 -0.13894904598972946 -0.22001930673073003 0.2684529447683704 -0.09104192088281697 -0.6548285900352077 0.17417626763544 0.26303237829063364 -0.4475179872104188 0.19467197276790021 0.028106022546538396 -0.5844848970977189 0.18878693638156058 0.2955995759391016 1.0568709025874266 0.07476374770055995 -0.5641448232410208 0.5503496363650122 0.09139297099712454 0.42255683412459505 -0.5114223530356522 -0.44626331103465466 -0.36980960728250284 -0.16941552693410675 0.1888848379907452 0.40390410984583114 -0.013546114637843014
b12 -0.1442454679
w13 -0.31765058071643837 0.13550981823780256 -0.177647310088898 0.2542389748892161 -0.036982638845987376 0.034504455135967 -0.4808931799271998 -0.46389632977950873 0.07512666765500621 -0.16295618146936267 -0.06318512240027802 0.21518395532589527 0.47812478241645523 0.02701184378475996 -0.4915971461753254 -1.5584271738692554 0.2767993717927279 -0.047104725549873105 -0.21631554901588268 -0.38634537779674 0.3341543413355802 -0.5389336737415618 0.062408491402973346 -0.08392615234431289 -0.181624487685217 0.529879517434745 -0.025032769307408703 -0.17200723004565827 0.24856765654288285 0.1082258775425132 0.5625249063844965 0.0429517513168812 -0.016993961576363913 -0.06126040687349599 0.5109485745507172 0.6633536700005845 0.1501094173048127 0.16341156688921607 0.5649210658520272 -0.12977460307506586 0.05654610336649821 0.2709126871715901 -0.48131957027491357 0.1243181993877314 -0.28576551451682475 0.3705371296210763 -0.2953688139516733 0.12328923339282885 0.10531342121726395 0.07185803609159494 0.1336565400474083 0.5618993285450451 0.4429973953648615 0.08251000534143337 0.46518204989700146 0.5243885710924789 0.2044273860702332 0.9290877533536507 -0.7262574451821697 -0.07921153170055827 0.2706004222133308 0.33992406488176347 -0.1979017949714047 -0.2701283165215659 -0.005397885020910383 -0.16315479835382993 -0.4233040578315075 -0.0933210954255814 0.11256632445609178 -0.2086999763252564
b13 0.472636683449
w14 -0.022212544962211065 0.33133469092263496 0.4420818515358098 0.1501654090840164 0.3368340738171976 -0.4520395780649861 0.09239809482959993 0.31082582726564323 -0.20085290902632513 0.14609867090075906 0.4743121682447065 0.048312380330447026 0.01333654627236821 -0.33153989236264847 0.7076795842015152 -1.244536179243908 0.0602413000233074 0.24741521203603478 -0.12338994642624827 0.11945014329307743 0.2984916489617005 0.5458974830730933 0.378996516139532 0.1653018526804018 0.1531033684324483 -0.36361124185874094 -0.07441991684597213 -0.08038111089905306 -0.017558372166927773 -0.425566119744985 -0.4954322406792102 -0.09596628164302563 -0.13307640391605038 -0.14160244952403866 0.2818954641476719 0.14938783977715134 -0.15290610113369976 -0.17122648657475234 0.424603492893082 0.24769797502867083 -0.0831771926391247 -0.10311991341025639 0.3245182834569961 -0.17831694201216455 0.008496084268675083 -0.020847535097025995 -0.3509200876857456 -0.18395188564775874 0.5024301565405055 -0.2392313813600083 0.08870539766280187 0.5230569109889243 0.2962553956961356 -0.369021242447808 0.0019553383182587375 -0.3330429500138919 -0.3066923865611115 1.2550881008014763 -0.32974810912615954 -0.48777527174047236 0.05726337001841792 0.2217423606066904 0.03890071379999682 -0.40127100153741563 0.1621110838345405 0.4188074277589242 -0.34326116017782415 -0.01067303392364033 0.5810719648818444 0.4124074634958964
b14 -0.401171827297
w15 -0.012615931711855615 -0.1069977190041959 -0.21438974280608802 -0.5590171393627054 -0.4444881692357485 -0.012149087301439307 -0.14466476262999098 0.578750730184631 0.5414991315385556 -0.1738611741771763 0.3551834306670395 -0.05970206793027933 0.541507131514497 0.2625147005044049 0.6361800935945133 1.577554934390245 0.1287085326692738 0.2109674769836513 -0.020547440947489386 0.14160396805786615 -0.38746933782994336 -0.2515645526874775 -0.1894411041918969 -0.38408139868375013 0.2498294555958447 0.219908589383763 0.3675779099988777 -0.060911186457577544 -0.3063169473990914 0.25834294636117194 0.28011994162101467 0.6890248035747188 0.5427549947864866 0.389343679475885 0.34149986184587927 0.26929076607636265 0.5779743121482527 -0.20698348142402698 0.22666398395091963 0.2013531501824822 -0.3471213557919758 -0.11603214372790747 0.4604938556109066 0.01820215785082681 0.17071996685220006 0.2520435910196463 0.38213985231809294 -0.4302410693750801 0.0682328855887784 0.05807172554784922 -0.43733978714290844 -0.561106980588928 0.6156808689912976 0.19732074351251075 -0.26788724076834897 -0.17328226348017622 0.25288525708633186 0.21108341624645213 0.3809925301976272 1.2823624447390423 0.5074451659943081 0.1006355153599135 -0.1443672639743931 0.05316911760536415 0.26155609408094593 -0.17003138493509512 0.004856082060271665 -1.0407013354399484 -0.5436024337819497 -0.35763551669168564
b15 0.42812274589
w16 0.24539827855356505 -0.044417902080588156 -0.32526830826589775 0.6174119987218768 -0.0636889863633233 -0.1586561870411226 -0.6089858160403964 -0.08787385846858058 -0.32516476513384507 -0.22221075563632867 0.1612158448013912 0.11943879197321614 0.6063484630819599 -0.07058828322384182 0.5222193294336892 -0.8827025201400285 0.06957787251366716 -0.05626766588313959 -0.03353388644772416 0.4014343343095183 -0.04055177643532141 -0.06146644819314264 0.040433558606698734 0.20900829120528916 0.019114688098803647 0.5201435997531176 0.14979380686578717 0.21974500468072966 0.29053750043059945 0.07187311265871961 0.3517899762913946 0.40090662874911914 -0.25080855946763786 -0.1446174176610278 -0.3165289940727943 -0.06702215775285023 -0.43555867311330676 0.2655419969312668 0.22424204217452284 0.0007328032041738397 -0.1593764214100158 0.5698214140769156 0.10932839643563691 0.2230355630671861 -0.3968288701706435 -0.19130585114709292 0.049499347196224695 0.33328157248909623 -0.12455411052432624 -0.2725773556033637 0.020284972844191996 -0.1280369912983853 -0.3420647279713607 0.12039669418855554 0.21902146448037427 -0.0672149569669076 0.15290406738262866 1.129440012835214 -0.2302503948276062 -0.7573965528342897 1.2978486069243194 -0.05638373744754822 -0.3808769000911606 -0.6749281037433053 0.14466217140126825 0.12366269405603858 -0.47354541297106884 0.16933952197520108 0.26186198624095147 -0.02580068747994453
b16 -0.150640103419
w17 0.08608907331116589 -0.1773629998326855 0.2368675961611588 0.4055478366669395 -0.3103709356547724 -0.26685518177374784 0.29634319085582084 0.20316723493809946 0.38795735607857657 -0.20052259183237484 0.38873496127775 -0.13852258882370871 -0.3440895992479549 0.24594855507101157 0.40332711361151247 -0.7842811992085328 -0.18460704972779485 -0.41918843303728603 0.21045107024415238 -0.3655564717502814 0.10111656169674159 -0.28097972891444045 -0.39429560290104776 -0.06498179788452307 -0.3964804266027999 0.05389953085114612 0.354417224676582 -0.16488451188869696 -0.31293158713636454 0.13854143856944096 0.03959814615618496 -0.22785286583807782 0.07243958937913705 0.18670176697609867 -0.11417550534993752 -0.4067072572044443 0.01215744907347163 -0.20302198448161238 0.04903498224278319 0.30024162786081704 -0.07179841126377286 0.060824511330829466 -0.4853335487174487 -0.1517818785735406 -0.5453902399598062 -0.04688502254502125 0.3782388669484835 -0.5807415917789673 -0.06882530439899301 0.23251445532798948 -0.3241541066219822 0.44646784588647825 -0.015667862818301174 -0.4000205355895347 0.33711614859137995 0.044757444610155364 -0.15168782471107528 1.2188617670203714 -0.349583114138111 0.07428126859844339 0.3589562480102284 -0.009950992823039444 -0.5032352369754333 -0.4088463253489386 0.09804512257189077 0.1787622250654472 -0.32986540068651726 -0.12172155932676725 0.22821809611837948 0.25272197014441844
b17 0.0561906591449
w18 0.04267056858194958 -0.025735028609381583 -0.3435916027104394 0.5699103522488912 0.6629064809722104 -0.3107007882313384 -0.16957862927014566 -0.26703619968687803 -0.641198314675172 -0.5963027622746305 -0.23908099089622034 -0.4526426104785299 -0.7128339334079448 -0.2510427710378529 1.3623422759744892 -0.3420764955485865 -0.3121899262638115 0.14498090568705638 0.354344697780108 0.04659348267783969 0.6400580201411655 -0.1530043297461277 0.343896327272156 0.04794815665748402 -0.04479391335537036 -0.007998848662018903 -0.21061992066354726 -0.33126606087192634 -0.4904557217164925 0.28981481515964275 -0.16799583432154175 -0.16602077288852615 -0.35980685866648 -0.2370319737379504 0.15822036993739613 0.23359124984481194 -0.2830050146058368 -0.10521813229269705 0.16764324944497555 0.4582665261469339 0.2728296795701036 -0.4562493433810181 0.42792279123144433 0.13791500641705493 0.0735801194229201 0.4333824271666622 -0.44218257291768703 -0.09416800901290814 0.06343820693386105 0.033724517409321995 -0.10370726869894559 0.784866565038686 -0.1492439216536155 -0.12025140503828802 -0.1644985275704182 -0.08215764390514632 0.05987495628854547 0.5645779513773976 -0.5373838905384216 -1.3954974916990799 0.642482832007246 -0.2636253821002989 -0.5208441226261833 -0.37378858208211335 -0.07226187951433695 -0.1368817198225113 -0.1047475372913691 0.038818139489780606 0.13704541197701928 -0.10882732765938678
b18 0.550060771202
w19 -0.4845297102901687 0.4292308917611958 0.4053512130435408 0.10693040984636262 -0.0031472311659159974 -0.5747493152632068 0.20536902430230622 0.07387841191017896 -0.4244388389100651 0.4676660839769285 -0.04145412819328095 0.1422934316615335 0.6338683503302487 -0.054289814615234196 0.2934639637786113 -1.3392154297551544 0.2201423805923868 0.2769139643999778 0.018690679343577786 -0.15678974664474257 0.0715921388680171 0.09310509428858224 -0.07602515439497885 0.10267003596868625 -0.03420537257267495 -0.587282676055067 -0.22246849635849972 0.23080832885345015 0.2684600898965231 0.0992679882550992 0.5625548717365543 0.11828077805828777 -0.3738476373207683 0.14171643817695095 0.5539551034927325 -0.0058744053427931785 -0.4315206800199401 0.16091803129629428 0.14703212634031615 0.1551107836095836 -0.03781810001308635 -0.10727866645044962 0.08579814072774668 -0.2976575097882535 -0.5227258534615981 0.00016468006026641 0.42389268322090307 -0.12595384772033472 0.1491273474211877 0.37828412810809364 0.41833822269466675 -0.028352765357903903 -0.42119644130907863 0.16165097205599732 0.380961407435713 0.35164851347773857 0.18565964562325532 1.834101443641285 -0.3300789462540512 -0.7106031656725517 0.7607953540059009 -0.18587834597779565 -0.16477642720587057 -0.34226219553780063 -0.1578538900573355 0.2775760334381936 -0.5882171531368331 0.2543012466386194 0.23842732059725538 -0.5854745195575347
b19 0.129007974396
w20 -0.11388934408904922 -0.00421233296964129 -0.46068566439281927 -0.32953300304596383 -0.24816318871289794 -0.4106893818006543 0.153791574227519 0.18652828946473637 0.08765837557677376 0.0071592073622059075 -0.5152459691803879 -0.28791940734591126 0.32327313234593524 0.08734391213298784 0.31295530845426606 -1.157242875387667 -0.3411833648703088 0.23805879625484813 -0.4630659103415403 -0.09909260802664357 0.10488915099103198 -0.004809826630645043 0.49170738820315335 0.329828094943362 0.35003067485911193 0.17906952819054966 0.03256911489720488 0.18801063089055595 -0.34070511029522915 0.07213905597240092 -0.25271073984092446 -0.2857532722059516 0.33735101844962506 0.21324178186891535 -0.10626624810408698 -0.35092935348637555 -0.6438159733960119 0.23233997464359288 0.21015516425179187 0.12925920814213762 -0.08352908980315205 -0.07442889075858558 0.16280974685527932 -0.04831446873010573 -0.21167863701030565 -0.14059368432960945 -0.24390258233196532 -0.2688939028011755 0.03971920390287199 0.16243017732912518 0.25147642639262685 -0.06772317097627739 0.2565395136575883 0.043886038802906736 -0.044348944097592206 0.06965951869056018 0.35078710373040284 1.2296528990521594 0.3599734757018555 -0.2547646177314135 0.78650860360835 0.12960809523171973 -0.13049474444722248 -0.3275328180904101 0.1612214322433583 -0.082521448195273 -0.16520053778676486 -0.0963144412642384 -0.06362635986019388 0.4042312264765308
b20 0.00197052913948
w21 0.47124871913580396 0.1168500834917049 0.42022747845762937 0.09684795096505709 0.21171633071162863 0.19301174108288682 -0.19588679038644952 0.16329118223379274 -0.2167821539443419 -0.13883940959481866 -0.4614651570795058 0.24670858596741624 -0.031564836283373 0.08438542114666325 -0.9700753466216281 -2.2767961950325284 -0.1064909657835011 0.46952182461304576 0.02752668464140667 0.33968159040821777 -0.347778736254101 -0.6437072064379609 -0.05521765376136531 -0.017182929887628567 -0.006238679672684198 -0.11137683333263751 -0.03794871948462363 -0.14588942488629 0.053843497795529514 0.1611421809101853 -0.49911588045923394 -0.0011033817444995007 -0.07530068597151307 0.1113340520307402 0.11503990395525285 0.12169866164037792 -0.36182645215006226 0.5145850525100469 0.3678151085780348 -0.21140476436638755 -0.13756402137956358 0.2786001452698979 -0.23058886428403866 0.38280985406075174 0.037539789657540235 -0.366453388300671 -0.3721165713328461 0.28509515848492356 0.15646411248772876 -0.057193385404410116 0.6318240399605796 0.26620527666014127 -0.042716385948386656 -0.12526486127188377 0.4316208274084853 -0.11605373891372801 0.5079837337234843 0.6958114200881584 -0.24566346536598083 -0.7353272953775112 0.0936992636548751 -0.014754139329270647 -0.3633376547479102 -0.14201352846970638 0.00017234047422715255 -0.2074170306582106 -0.10688975764564114 -0.22241122350466108 -0.10210989231861496 0.006964529074659208
b21 0.0836216379711
w22 -0.13565234744156837 0.3065532852779582 -0.24740741230247007 0.15250259484094011 0.317464563632383 0.3285430269668506 -0.2761917733810788 0.11802015519760438 -0.3079103127254347 -0.07028339042949473 0.13451395510370875 0.1137875660449522 0.503216865986352 0.24185853195798312 -0.42183168578204844 -1.3232714742846663 -0.4170121022496404 0.14290263652971325 -0.20758546237772613 -0.254586601341328 0.49514117596428253 -0.06459058514317609 0.1821210804724864 0.5361739533761909 -0.4656243122866798 -0.13625589419602602 0.05098769272920612 -0.08400804235719088 -0.3385389769412056 0.16370603359865044 -0.44180914072951827 0.17666263544500893 -0.22629503595075745 0.294988483705537 0.06024081720892869 0.20705196220265318 0.39849015319714887 -0.0897290695992362 0.29074629073021857 -0.23582322186942814 -0.021447223853567735 0.42202396132321895 0.09591445167395399 -0.23185162545292146 0.23887990198242276 -0.2388199527215952 -0.34179521348712544 -0.15050696225568116 0.5238502368631 -0.13329231006393136 -0.10998442536969857 0.5691968538341906 -0.0047808895833318064 -0.38548900424731214 0.699196687781092 0.026177428790456543 0.5121884976055036 2.140266155910328 -0.07539989615226844 -0.3320859042184526 -0.3350357864542127 -0.3865160524172105 -0.041364345048923785 -0.27499485680740504 -0.15447740042279431 -0.3102541622857162 -0.1632236349347797 0.08554722165515952 0.41247663299849624 0.28373383131397545
b22 -0.389915729966
w23 0.5046158684736036 -0.2999496172291744 -0.29813238159523986 -0.39016168408082796 0.33124148863175745 -0.3052201382699973 0.10098994447837127 -0.5085584134025807 0.1449975627041239 -0.24772034281842206 0.12347019394385901 0.1383435701560379 0.10872576421886444 0.18098138749159373 0.13440844139263008 -1.284787008433837 -0.4434037534569255 0.14382485663306988 -0.1346672274701696 0.07772447739274743 0.12931166800389624 0.5730884389055433 -0.1411803950522278 0.07658325204448425 0.14508111837311613 0.08820477057946773 -0.17664512949601907 0.34309873492231574 -0.11862335222144742 0.38159860794443184 0.28228799572279295 -0.5033266441189436 0.19835408350936445 0.10639432945632117 -0.10268718626066561 -0.18556284277304771 0.48670608951007305 0.10147911341134846 0.629909082702562 0.03575964606107645 0.11062446907410708 0.03170454963433349 0.030630900689924637 0.23303055651317411 -0.11356774747635308 0.08696576174194696 0.014505735153134714 -0.06379078000050577 -0.346048686216055 -0.31039688493971757 0.15643425691643278 0.08510990482617034 0.2552584013964044 0.1729396626261356 0.37681818268990125 0.17134203280134583 0.4994555935623864 1.8896458477190559 -0.10971593018701671 -0.7022881159009772 0.20379258077796783 -0.3866853741701205 0.13497923030662404 0.18527122998474435 -0.04917103984252637 -0.6179989019611044 -0.6640940356978461 -0.04769849673165362 0.37002066519437216 -0.4099441125611742
b23 -0.284399981862
w24 0.10829242370232448 -0.36776861247659737 0.24433484002101344 -0.11101942193811062 0.03582716574099191 -0.15454004249448994 0.0982479170298247 0.11919442530202469 -0.30576478915671323 -0.023248684583790955 -0.35511306890084077 0.3520481593596332 0.02020999378684941 0.01650611546153957 0.542429396666896 -1.1889561031252425 -0.18914654855190166 0.41570153441480834 0.10852407746377782 -0.04531855583447434 0.32506193394857674 0.14734011185518395 0.11018422208425199 -0.25750496570675213 0.21662406107039991 -0.03612034724023958 0.21258987607818453 -0.24889748726336738 -0.3113956559015619 -0.07315165421703085 -0.49751393586918696 -0.07116784562187245 -0.49735372706023917 -0.037462791581912264 -0.38822740194202754 -0.18906880778910415 0.10272085367231731 -0.14623345409786506 0.1396901336009899 0.03255412008368465 0.14288132765356237 0.33721960562603787 -0.47035149767950735 0.015940280075309725 -0.15983479848710952 -0.5375364200305742 0.2578833964642723 -0.12305685079161778 0.21471239102521603 -0.2796325731765584 -0.3636875281373806 0.14613095786160274 0.2986770444717434 0.3069683870943731 0.541844494403059 0.09197795417158287 0.3393382396183808 1.4560109752523656 0.055182029626408245 -0.46547184266701236 0.3321512030933382 0.0058476014037154925 0.006029829452980092 -0.4185867623527679 0.032208956177347134 0.11720783347497582 -0.39896529754551757 0.6039733176085268 0.26266933270490594 0.4563940169269711
b24 0.00430935548661
w25 0.1289404124578398 -0.6450437012387173 -0.033511007358492564 0.3395222031825737 0.3213716250706242 0.13472245294349913 -0.15823172115752557 -0.17355177185294432 -0.0210330714999623 0.006876649097062635 0.036788672136590074 -0.32767244703087306 0.10976015644403814 -0.05504369996868538 -0.19802480924485483 -1.6778446978227413 -0.5619664251410231 0.0994801560129041 0.15688311785834363 -0.09034540540251584 0.3220488086468221 -0.26914169450020997 -0.10796423701141497 -0.08324821171322355 0.19053048024219363 0.4183148641619954 0.1824358810182208 -0.46022517672772206 0.14860978603249247 0.10874948335959536 0.05614046129689574 -0.24220051378767865 -0.11156987825802744 -0.0825232080720427 -0.010190260967967076 0.00109431461140396 -0.5436775207245617 0.13466307550952722 0.005538542580205677 0.5396951789656316 0.2706555381632359 -0.19029135770832906 -0.14196206630988997 -0.006047019433246727 0.30410726564655893 -0.21113598674528697 -0.16381177611897713 0.09361007698063467 0.5589699082664552 -0.04778200201309213 0.1275411247313155 0.7259052887957456 0.11223995455730576 0.2100259640345547 1.1795896849941407 0.061007613377704356 0.24889210640339282 2.197621385972031 -0.391196964359728 -0.890992463098089 -0.20715925856395265 -0.09654745652014163 0.35475612949855084 -0.1143416587210646 -0.048335417900847284 -0.36667269444289347 -0.5911900520917099 0.3412845248912442 0.13514237677575128 0.07390534259350141
b25 -0.416927638356
w26 -0.14758205526079005 -0.1135443356736709 0.36660058280751784 0.27097748383339265 -0.09417327753427226 0.08955668159970408 0.13275639448475132 -0.7288143099978995 -0.1580200415506508 -0.25771673909136095 0.15082654810428114 0.23857221238523293 -0.2380575842361187 -0.1597636349679907 0.8689882736472957 -0.8333829094890028 0.3779223543191051 -0.15644810303539142 0.20259145316884977 -0.4279445757137201 0.2834537098873791 0.12525752172761911 0.1696096144655553 0.5827951535892913 -0.3473240199638552 0.12985978994734113 -0.5020471312295088 0.19831987093091138 -0.09312648969808385 0.28827625227598175 0.2499197029563036 0.04477269019300541 0.000931094330697875 -0.2727267855927336 0.16280704449850186 -0.3077604557384906 -0.18466459331897336 -0.28704142116591724 0.2803040353366178 0.23318536862846367 -0.17436249639034054 0.1439692370611868 -0.20016188141459665 0.020462876101532825 0.40553686254729804 0.0018222655107548431 -0.28873502237559256 0.002264164339582251 -0.2401167598077538 -0.3806682012505834 -0.10727333708332763 -0.08166922469504191 0.3740017704075408 0.26639140693165775 0.9637813757821825 0.06045339777506315 0.3937230598734448 1.4308999276375254 -0.23812382061431633 -0.317002451266478 0.4193293056062599 -0.07936691227795019 -0.3587443364762327 -0.0021045900034617183 0.4500658879419256 0.08880403893440078 -0.40157897765302053 -0.26238009716987615 0.41546707423794965 0.11200043681991177
b26 -0.210906003793
w27 -0.1699128724798045 0.21724841832478195 0.25894998349925 0.45885072642293434 -0.03120418104592185 -0.052745208146405646 -0.26901485847359846 0.0009075879108893218 0.4735700685334478 -0.1966333552966079 0.08743737333815772 0.007999053447571515 -0.09294044599766065 -0.1545095151910753 1.0160090613786683 -0.27394996475439276 -0.46460914339868903 0.40733342178617526 -0.15293303259604724 -0.33664982554840645 -0.19993373981492515 0.16947319692038837 -0.09091343821136795 -0.0305924271705796 0.15193620032758 -0.14974437444143004 -0.1867555129080405 -0.02582020164781986 -0.1887630626164368 0.11473046645087988 -0.03191578705399331 0.37743846951443366 0.0026695045768238695 0.059246478104342255 -0.4547714037198323 -0.00022431082796412955 -0.4191642042690089 -0.2308946058968674 0.07685954469916817 -0.4812633725891597 -0.24957158775158253 -0.24258919544441648 -0.20162906279750542 -0.12104586353447114 -0.07892410028011171 0.1292093889788545 -0.39587928796365046 0.3531607161357694 -0.5810695684776935 -0.04388740528333311 0.03938904138829214 0.023992222932503398 0.08352039154374984 0.006122697294800327 0.8051634387365867 0.39919667996613545 0.057207528741750696 1.1697471160344202 0.19302152873241094 -0.39082340230896356 0.769811586509284 -0.17167394158978488 0.3775441396149009 -0.3708690194247168 0.3389197242298619 -0.3295709363525263 -0.2515629957249674 0.17433547523246457 0.06225969259863373 -0.48149924457272114
b27 -0.052321419834
w28 0.1945698128324137 -0.019665078426278182 0.2889181028687667 -0.143256589424599 -0.012746438547109693 0.5688209071850902 0.46115180060045835 -0.2074331844770078 0.40958097792151327 -0.11394826985838938 -0.17542048251272993 0.27449925996793256 0.6798055834432449 0.02326426431100929 -0.7290169938768981 0.7120962592138869 0.19727293393138295 -0.16967725394467287 -0.03316536929866799 -0.22561953892623146 0.28642409549615894 -0.1873638099798961 -0.24595322344579754 0.08367720822066374 -0.36482014842163935 -0.09904620753715938 -0.21922212975249916 0.0229778951517904 0.2375081800094183 -0.5056350041770651 -0.37051455890811796 -0.4409005683210031 0.47182071210954457 0.18674250950789542 0.2610915050398665 0.19899426906437448 0.17630670305133173 0.4077049099444406 0.4009320503708759 -0.08979885277397448 0.04576567342261204 0.20341166727817775 0.17002739464581443 -0.2483565447521883 0.06871037044007718 0.32117049978980633 0.18919836472789525 0.3378006931141896 -0.06349386930375578 0.2027570421867014 -0.2823112304508126 0.07892579310204194 -0.19404977012518848 0.11300122041000395 -0.18780376465048151 -0.3047384715167694 0.20409875683941095 -0.6720988493749318 0.791548003569104 1.0891209827136135 0.08238931241025287 -0.19446986595668214 -0.023186906106973458 0.07582244148935405 0.28444220377909585 -0.05434225453956441 0.460649264403058 -0.3378348510520329 -0.5342602440321818 -0.37196205068561555
b28 0.0978677327339
w29 0.4684835205490381 -0.053648906858778246 -0.038291649940574914 0.36807289439320134 0.29474177331047796 -0.49479305615289676 -0.4026268249953052 -0.16246788536444612 -0.1036671711341456 0.17617133794380382 -0.020406513660314776 -0.07523712401253686 0.15944714101607782 0.11392153913180333 0.47847286691201174 -1.1180150797452841 0.33327609105441836 -0.10398922803833674 0.13768769952132506 -0.15375004350134797 -0.16013508498576481 0.20346287501506907 -0.25087512106353316 0.29679080471773045 0.17479028453395953 0.10801877688287487 -0.35596240462644557 -0.0832386901207858 0.005345316718690128 0.3973528631711614 -0.0979728848770749 -0.13748684099690178 0.22354289676313072 0.5433201635189756 -0.12082939336360957 0.32574263283069566 0.19478344585177845 -0.288551810612326 0.5555810059519769 -0.010459791192214738 0.5366561751363076 0.2652226504469325 0.07567227081147003 -0.3051833708383857 0.1541958764396591 0.1424469178854135 -0.40500796018322793 0.3494353495149447 0.44336934275999984 -0.3807326031653247 -0.09197153705112261 0.16399156683950417 0.08528410418300567 0.05243665541075989 0.044435819990229955 0.33076693401575796 0.003762840270092681 1.2279840402023363 -0.8296982252365646 -0.7172098077099562 0.3986004252023078 0.11063734720075205 0.1312446700624436 -0.40339583715634175 0.4315764849259678 -0.4860246403870568 -0.03538436739477474 -0.06647947081131662 -0.036531262896522324 -0.6937368186360167
b29 0.144847850906
LAYER 1 sigmoid
w0 0.35946919006629946 0.04469767343365548 -0.24369167428705632 -0.019676318369085944 -0.06521500644304236 0.6318062252742257 0.5755006042857391 0.34861911203904306 0.1293974865529264 0.027509283248265123 0.2502491242695742 0.08696858369274409 -0.09816088992115984 0.199679173457105 -0.09148015774859 -0.6376115454261709 0.5254796229743288 -0.5385893565446173 -0.23852982156163455 0.17609504567151768 -0.03165468609316169 0.2284934032115595 -0.09388924854864367 0.4797117444464013 0.45018108373262017 0.5714649826372098 0.024554860204788743 0.109468240021858 -0.6824327752228475 -0.18534515414662855
b0 -0.00599013767356
w1 0.502412841672826 -0.12872941915949107 0.7291355424953028 0.4402489220766436 -0.45264795986930445 -0.11803695669565951 0.0501659596817121 0.0017827119994060176 -0.09929383791526972 -0.05366094560410397 0.7232598871356634 -0.4082670994454201 0.2283423864160675 0.3130195392398881 -0.2635671256899471 0.05429909322630592 -0.08376263065824 0.1508835521190718 -0.42081595306755976 0.016383317752037902 0.634681288808792 0.47721903227127377 0.5492225268836963 0.21867189866517314 0.19139836488127682 -0.03971481231748862 0.08808349274338899 0.14711239101548754 -0.3917845397363021 -0.12506131883924415
b1 -0.0851073306308
w2 -0.2821713874151143 -0.15329367432378402 0.04716434887578665 -0.0789114943109168 0.4738790053728425 -0.07218271012021574 -0.5340945979229996 -0.3031788789377372 -0.7738707228441131 0.09500092336453826 -0.17978414868683562 0.06657529774435991 -0.48048166814471194 -0.2421200140898904 0.03167129349899314 -0.18978246759567743 -0.012900642704610861 -0.2997067996845149 -0.0892130638839617 0.2848470450065388 -0.0876047790644087 0.10777002565563437 -0.24055542258205895 -0.11046637803776715 -0.5337054948742498 -0.11356304150808821 0.04766460154223416 -0.08536249578675088 0.512874188739496 0.03997294512924142
b2 -0.081479347111
w3 0.07127946398556308 -0.008660711666400875 0.20284994020096156 0.3707441044500869 -0.6859071086701248 0.2004903939145665 0.2808427994222104 -0.10008664499320749 0.07649538156951918 0.04105458506850151 0.2888006853521917 -0.1588174926585871 -0.060078650220220256 0.07388620876958446 -0.13368252481544302 -0.24227370485293157 -0.007355022051142317 -0.32977282779759176 0.249806357256509 0.24697668184852767 -0.09614942387817665 0.32897194782692196 -0.3824965788716678 0.15745019784163616 0.17440150863868198 0.2748445767826658 0.3321448527897033 0.18298774978411966 -0.34503367983055194 -0.08612799096538837
b3 -0.385653413581
w4 0.352942326119995 -0.17977274702873652 0.49908097465975426 0.2016922953790091 -0.7148163153197101 0.14134263760363167 -0.2259101433176206 -0.3538930186719868 -0.21484290589330168 0.1611276515390146 0.3354891663380876 0.03863057377040264 0.40916026908654557 -0.044489474204146916 0.2947391985374444 -0.5789285800037782 0.22531074694600386 0.26081628647515953 0.5277314123550882 -0.21993730086811225 -0.1617295633572118 0.40691335959633995 -0.00045232007969565386 0.05505835005616675 0.604381164805284 0.2568526749620534 0.11266291175029065 0.192535445097708 -0.47984895935406263 0.3284581735647533
b4 -0.214987138299
w5 0.223225860732549 -0.05734944322168375 0.4441359167636365 0.1593183547921279 0.022386032329686546 0.5024855049054413 0.21859235763835547 0.41884883229205827 0.6646171393662292 0.014367293204829261 0.1666487026621107 -0.14027110848793256 -0.10309608531341528 0.2804199637337572 -0.09550024066966505 -0.11512155227704315 -0.097364470369669 -0.025624700956646138 -0.039593268383233286 0.04672234422130203 0.08616095799750159 -0.22116272913795249 0.0579095495472978 0.29669049654456925 -0.02098652345889696 0.3985321150831688 -0.15727873774948173 0.1510096971684095 -0.21535206753307687 0.2261095373132192
b5 -0.0647753966263
w6 -0.4596003794141944 0.18922059066063773 -0.22582836916488686 -0.2852224004416738 0.3950105884330137 0.2849805727025491 -0.27358521666426716 0.25552675636323363 -0.06798835014248082 0.12615130561144838 -0.48958005473528377 0.626678971740773 0.22770309870147887 -0.3321961100575641 0.4306076908981233 0.25254763805095715 -0.6385198180435693 -0.5052678277603623 -0.532507253520811 -0.3626351058413527 -0.15117532051018617 0.25123252034817223 -0.09386150642110172 -0.4109566343940391 -0.18646364903085208 -0.17566225656104287 -0.09298765255131314 -0.5990299919541231 0.33325595116758594 -0.004717245398197017
b6 0.16901441033
w7 0.5269411909995373 0.2628442657294337 0.039749961272712506 0.21386574398499247 -0.7139470411321893 0.08077119987552135 0.14853347406086306 0.00031535600607519583 0.04368808898368988 0.24692550902693947 0.3421839700522536 -0.5665505268510599 0.6301298391152348 0.0520991351426669 0.0403936408957869 0.4459619862337621 0.1904164037182853 0.006256846329505643 0.4053013478749266 0.11076776976442414 0.46389183643705034 -0.03137211729310911 -0.20473718144328726 0.571767295607296 -0.0077485618519066895 -0.3698455881943172 -0.11403534587332435 0.5314340460690012 -0.40213766584740057 -0.0226445240696231
b7 0.156220687414
w8 0.47276867849577764 0.4425917636872285 0.33568868888218695 -0.4384663876389588 -0.22807110943164166 0.3443096501703427 0.05970809162374691 0.5862459217469175 0.5437351735038435 -0.17502077079714048 0.4455701434195543 -0.7370621356762113 -0.1427429628787464 0.5991705531000776 -0.08628200927022305 -0.5090388148526069 -0.20070217084260494 0.284557058928921 -0.12980573507370843 0.4127735801336809 -0.3738191113602957 0.3814953017790964 0.12767574618821984 -0.1075588463460313 -0.37796806824007034 0.08304803287075167 0.07859887821642465 0.3014914165693817 -0.2251658365531911 0.33822848684078777
b8 0.0438361323024
w9 -0.15504135194369983 -0.25221761566857615 0.09161650185768763 0.1715494961337378 -0.20727451755769752 -0.5220533256499879 0.04775848371856635 0.149100855016215 -0.07875006026298594 -0.4326707698484128 -0.4832669172100592 0.6402791314865449 -0.5843468667557479 0.08428821308672158 -0.2122536069551418 0.1364654214496446 -0.19141441919466146 0.08099060959831106 -0.11106489275068807 -0.6805024542764567 0.027878055544396086 -0.26224367708461427 -0.4423573148783393 -0.19132211122112255 -0.3733656267027074 -0.06462386585535707 0.21208970432186658 -0.26008975153232694 -0.29605751783109047 -0.27283463720286255
b9 -0.150596567099
w10 -0.18369639851632702 -0.15293884921611758 -0.47979826621823507 -0.3876003976087491 0.2006819502181763 -0.1822867593985495 -0.535728387826211 -0.15931442947272462 -0.30592377996559833 -0.013036796083146387 -0.2654663103987079 0.4902132119933366 -0.4986743428653079 0.027053070953051962 -0.14995867677181898 0.37725146565006673 0.11047523574603152 -0.26595520106327725 0.03445333420167093 -0.3951451676122453 -0.30297945191727726 -0.3696963112601797 -0.19004977920732996 0.3800800649281974 0.05884562093378018 -0.007818345134614137 -0.2975281158281969 0.446754702459681 0.1602106213562649 -0.018656797713098718
b10 0.0670974430299
w11 0.4194053216122723 0.203286938988584 -0.11238306283238052 -0.20885841214507653 -0.6662391630974329 0.07598039243208873 0.5293558693874895 -0.18250458233047248 0.40142555947780967 0.0013678832780314567 0.5264383254936346 -0.14924370533847622 0.1940303127624121 0.06752503237763913 0.040003259468470824 -0.6313694105573332 -0.34751937110963893 -0.6069157523237099 0.10500669427430066 0.13552083013813504 -0.36725415299096564 0.11485855002174265 0.5471558937062876 0.3395292905118064 -0.000504336273348427 0.4310512529183821 -0.3775418052839868 -0.22825871428957356 -0.47577769566307676 0.020916443720742695
b11 0.39202049099
w12 -0.45967954000722205 -0.5211342402354624 0.09682881001062432 -0.31950356975129546 0.17392184512559303 -0.33582803111690696 -0.47253418330461366 0.04185251094331696 -0.7080939252827297 -0.033337274388683204 0.42489841348825913 0.3876989733392681 0.16833849565420148 -0.19898357003297118 -0.3537180246054244 0.0013259250634941261 -0.5119612869070134 -0.26356332051717 -0.08881709071360747 0.40406346773598495 -0.3648465206346246 -0.031544718604670056 0.0639823502112155 0.3141759166483189 -0.39892856350484923 -0.30602963241473424 0.012126359325329503 -0.5981668536019258 0.4155923070830111 -0.3555995799249123
b12 0.401967176541
w13 0.21534251265836976 0.3456263721795037 -0.1764705404710527 -0.28033634972513116 -0.2660046901728075 -0.0768408908127007 0.05886082822761674 0.4271617691209039 0.5298665580290458 0.23414138350365485 0.23739475090199125 -0.3919132958799691 0.43650777944970237 -0.17926140236294105 0.45559940083731115 -0.5279269564167961 0.5578340257157595 0.2157783183874288 0.19643476178272856 0.5148890475437614 -0.3017826272050118 -0.07128776994278385 0.3402199803250056 0.6514510134279367 0.20083825964256388 -0.09828708809166778 0.15636516566687667 0.34774984517064916 0.04823236193714403 0.004257689969659736
b13 -0.261584426201
w14 -0.5327993192829996 0.011139003582236162 -0.4054117218523246 -0.20339018554851504 0.4850359212214094 0.004241807692924093 -0.16771319514320163 -0.026459956201407876 0.10101110951357427 0.048349749785898316 -0.3465141665711623 0.4421276741903617 -0.4911260773891909 -0.02131385345483784 0.1907443380626427 0.36445173807377196 0.203749828526124 -0.31521957428853487 -0.4699244294957749 -0.05964778252006583 -0.5000246213680726 -0.2715266606446931 0.07936531365406582 -0.28630607942171526 -0.20098102753119917 -0.41900032893846684 -0.08540742873773882 -0.0010338191771383175 -0.13039521219874245 0.2532794508929552
b14 -0.499695561115
w15 -0.3275430642792838 -0.7432048678670039 -0.18624801305208677 -0.32718284123604996 0.468042569512207 -0.3366068527166086 -0.2528897553487303 -0.28983010873744497 0.07851100954245512 -0.17240297825925474 -0.35110998950567646 0.12399308426945338 0.19631245959692986 0.10660661981313418 0.048892990697997823 0.021937071507792963 0.4044505384038132 -0.3328211019539071 -0.046239261186622846 -0.1994110730567534 0.35916585033941134 -0.3798728988577172 0.0715156963741047 -0.6778421756103076 -0.7735671335098782 -0.5257053298684041 0.07268565062214248 0.04812549746859069 0.08572572863455614 0.34876806682222317
b15 -0.136748499601
w16 0.03698201707613634 -0.21650203519739555 -0.188452297939007 -0.24203122821485393 -0.10712489519428205 -0.4018436415684327 -0.06796273337637808 -0.30117117420914286 0.13169539240026054 0.057571069057230424 -0.2956532573936372 0.2904529360377414 -0.7191694357064696 -0.05692861293453967 0.018958213548875603 0.40089947227892303 -0.14336419979796153 0.027916514956778223 0.024227188940916043 -0.33374023942841746 0.23956330722075705 0.25522421597421896 -0.13374597007465933 -0.49715107013256576 -0.6800508682418178 0.05132096573928852 -0.4086646910511416 -0.24905720899976438 0.030442742482146293 -0.3635815757002335
b16 -0.00036053525501
w17 -0.6732534747264288 -0.7336844064819955 -0.08350434133833386 0.009283289007961293 0.33032463722023153 -0.17525879829472013 -0.1860222424006288 -0.04445768669062088 0.3397746515291759 -0.24290213812424138 -0.542391608735829 0.27841592042644475 -0.2658269334271382 -0.19891911195574616 0.5370112508488726 0.11329752927049261 0.022449688462272306 -0.17698989819225325 -0.01352832389484431 0.0007692733226159179 -0.4455537733771732 -0.17209374271632674 0.27145685380549867 -0.08784113350531077 -0.2594269338406291 -0.09857526129570084 -0.3114951083315552 -0.23520499965203595 0.6684861799828803 -0.06660748948953384
b17 -0.16641337245
w18 0.07920092880421258 -0.05881323168540503 0.5960198014000738 -0.017636490268074748 0.0368921881582565 -0.0327519162698103 0.16994338558010233 0.482344936563888 0.13436688287024334 -0.04079173840914712 0.44910159184346304 0.05715981336413922 0.5969858453408032 0.6241839081531786 -0.242253674720216 -0.19106275164199849 0.23399560090542135 -0.3078250926536627 0.07909110050642235 0.33336012048291963 -0.05117276319757306 0.5075626434793818 -0.08033943084155364 0.4514610257994513 -0.33455399286398846 0.4602186173353156 0.31043484506259317 -0.22965595633652888 0.3350191160587284 0.1421535653022012
b18 -0.152386598354
w19 0.133002551556734 0.6189625222316895 0.26169002597494123 0.10561681988029653 -0.3426521927085969 0.10396490842406851 0.3411804640846067 0.3912466928029579 0.03673137199581553 0.051669961527347874 0.19476134341698842 -0.07451037941876434 0.5340866270681853 0.2220526022542989 0.014871294545482968 0.16068895143464498 0.204717609582929 0.12221517309115187 0.4241060855584368 -0.03412360741110094 0.734547569425319 -0.04735562161111999 0.5190038667666729 -0.08308382825019431 -0.06251399497743533 0.10314442197570274 -0.21367258031018213 -0.2437778252306615 0.04432295150447898 0.40723559448280394
b19 -0.243236287242
w20 0.16158928121859922 -0.24316963045089973 0.42799291782643667 0.6294547472413701 -0.3323930482974229 0.07868728513827407 -0.26532087215150085 0.10519567951593056 0.5141626861262591 -0.3759486337641045 0.3607108427549537 -0.5137223558780487 0.17904703830046576 0.07300906856140076 0.14610489801783536 -0.11494543936551781 -0.07711076903706685 0.08228960349958635 -0.043930012733831486 0.31154569994142794 0.3025218846920702 0.6773595900518782 0.4051856852730237 0.025328736145713012 -0.1987520438788743 0.602430618825298 -0.07197684098114618 -0.18980206248338355 -0.04263855781092029 0.44578801216122843
b20 -0.191228575786
w21 -0.3939474367467771 -0.1342461433813148 0.21724935147493504 -0.25590711968764107 -0.15739210043890853 -0.19429574244583206 -0.389449351558426 0.10082431541989725 -0.12789264961752206 -0.3562693872999645 -0.4077419000269903 0.23774129222537088 -0.3034681101145425 -0.6329892601280912 -0.05571404384281516 0.04813866736836079 -0.2942997759665719 0.40397971859193005 -0.2500700543589603 0.13441011551740029 -0.19638587259236037 -0.527987086354224 -0.20300331663413326 0.4189363034686461 -0.4115765273719837 -0.3399953624728454 -0.28414315785012156 0.18941095794041593 0.5850519766372053 0.08663795266056226
b21 0.16291537052
w22 -0.10748042274569669 0.1981974990525056 -0.01694943660286112 0.0394102456787541 -0.5848554655491127 0.19071190208989963 0.5521250648179156 0.4044615142831313 0.3148498433426228 -0.06776658978565656 0.04077791843942005 -0.03948038663697996 0.2756819421214668 -0.19898845356892642 -0.1016831078469322 -0.012206732125036729 0.40084246116686295 0.03606974776163017 -0.1544901317955114 0.30017390024785384 0.4940844180534173 0.2648544019726667 0.012660933893628297 -0.10071941061689896 0.5573758414518771 0.2094938708164663 0.41730278145144634 -0.23553746319996172 -0.4703203199407074 0.10924497086731688
b22 0.199437785649
w23 0.7638492688289139 -0.028075242371570566 0.7456954174384447 0.5373275609119216 0.10202860969411712 0.3976593231276876 0.361192605330969 0.0998939301706571 0.6204588903614225 0.23145771741909693 0.43007417516487056 -0.4204317370831266 0.030478252221243597 0.11294701377421354 -0.06913246308253741 -0.1629182595624454 -0.05153839519016406 0.002552514345984905 -0.22828105534716972 0.20124818870053185 0.28896564022331894 0.015380406159522516 -0.05256864421482926 -0.1762187353864973 -0.08547765156038738 0.05239661092319796 0.348699050841335 0.269254941396085 0.2917530845716939 0.1791248736139263
b23 -0.36322869368
w24 0.03799057774737021 0.579588875757175 0.4684044350517609 -0.17990083167541424 0.1667861717341531 -0.19559752245313175 0.062120934070652056 0.3347283137679602 0.19130817189223648 0.22960130068418638 0.19027276566365953 -0.005106452591405668 0.6850758181014867 -0.22858839606321046 0.6109107837117211 -0.2851784189427819 0.5951785994131752 0.05228183956954904 0.25711888927791277 -0.0956480010127607 -0.022750663222435248 0.49938440912121945 0.08612508592309452 0.21845186803876032 -0.1444028821334065 0.16180686599090757 -0.19442966140880835 0.04323152965974375 -0.3405336255396086 0.034371731415378345
b24 0.295850732829
w25 0.09947788845587097 0.29269467917075387 0.2800865571196392 -0.02439195289870431 0.15636808973373525 0.031410321010614285 0.34484591413936083 0.08188455537822792 0.128123555115937 -0.21461272493502254 0.1549698926546959 0.07064157285618161 0.5532385878166745 0.02281131031446227 0.2598499217242937 -0.04525921280757896 -0.12866298281426797 0.10584623296328273 -0.08085959594216119 -0.11837132966695466 -0.14380448997410564 0.5664516517941764 0.17926191646067888 0.6684386335500175 0.33443401008576207 0.5411368580237941 0.04578908577923827 -0.19686251002854163 -0.014971301056097905 0.22152962034519857
b25 0.0366730642838
w26 0.19785719730837417 0.3982422349600683 0.41959366409980126 0.44336537800685216 -0.1408420728866097 0.10234845310226676 0.48784152997748953 0.6202749601714069 0.10827642408112173 0.3641310882199813 -0.013463567155874802 -0.09928084947124018 0.2779081426393678 0.009830730368005565 0.0008624087723887058 -0.07016934189713363 -0.16166188530642925 0.5012054473145116 -0.26908158899068435 0.21525874655431115 -0.023980467053775073 0.18180039454066835 0.07122600764148361 0.43486150130305223 0.06852716828123864 0.3772877203668232 0.03286499103437241 -0.5351214874466291 -0.25582022734362125 0.6713090921631155
b26 -0.226431927261
w27 -0.28628619102576985 0.15635749482653827 -0.02909744339302649 -0.1040109082468349 -0.18761673613899024 -0.2745164373668422 -0.14578184256687446 -0.4154206238648201 0.09203567079813728 -0.07957816519404935 -0.2722586674427536 0.4761659063628597 -0.34738837098278164 0.24314537888961862 -0.4373865699290488 0.26246547104632406 -0.6901424036018804 -0.11171864668253348 -0.19495902257263975 -0.44136041432882295 -0.607722998360376 -0.4530273126665724 -0.14862476885885492 -0.12121463753461488 0.24123491883097667 -0.37402673818902477 -0.3413022640813234 -0.31277989568147296 -0.40153086229261675 0.2944913670874312
b27 0.451530634001
w28 -0.6671357867400391 -0.01468868205436264 0.14313951673353392 -0.632160130323499 0.3674801044065252 -0.22504973527383906 -0.32741528742140424 -0.1431239807704443 0.007859848646414822 -0.09022158637836665 -0.3333175557583434 0.11479746853390001 -0.11978009384179064 0.14617885049534093 -0.2763547646102827 0.08932960358896842 -0.35715413727387113 0.020472793101234395 -0.24580990378317785 -0.03744555780243334 -0.2824257438255978 -0.26136071643049485 -0.27705834636147236 0.314654741039816 -0.19063517320787424 -0.154827853218896 -0.006300968459079657 -0.3483937172725082 0.06064910317514367 -0.44977873570066856
b28 -0.096043558659
w29 0.25061357904421827 0.07849428368733183 -0.0008163165035852112 0.19756119012207662 -0.14580785108791003 0.10467763760306341 0.6421324503658437 0.5537353642570576 0.2048363898979982 -0.022385228691611334 -0.013539276425339943 -0.24730405950995976 0.7694538607185111 -0.42497907779614724 0.35118729073885013 -0.18025166367056397 0.3124270387122694 -0.2987094991998526 0.6198022808061391 0.37853704716227893 -0.10911839038225454 -0.36606837469048914 0.2037700169878986 0.2914784144847815 -0.03786816576167659 0.20305667533755814 0.2515076137385204 0.3645853597355514 -0.20803834182230557 -0.10064035369624617
b29 -0.261866430458
LAYER 2 linear
w0 -0.3597524424261046 -0.503809964252713 0.363021597791468 -0.15748946977701062 -0.7449794315562006 -0.1973799972276568 0.4005192115707977 -0.6005376871135619 -0.4844861053520108 0.16562669444246644 0.4146050534918409 -0.14702270960852942 0.3384698348126193 -0.3399574368515834 0.1374185818399585 0.11806206773544631 0.20096490076553955 0.4143148555390615 -0.4264967645697334 -0.3885037980324405 -0.40937114385301737 0.1924391100804814 -0.6443477415294064 -0.40472041278580945 -0.39225596187650164 -0.6254615035141197 -0.366997853749137 0.1497826080990335 0.12131474319100129 -0.5487067669311523
b0 0.132187475486

POT O 6.0
SYM 70
2 6.0 0.003214 0.0 0.0 Si
2 6.0 0.035711 0.0 0.0 Si
2 6.0 0.071421 0.0 0.0 Si
2 6.0 0.124987 0.0 0.0 Si
2 6.0 0.214264 0.0 0.0 Si
2 6.0 0.357106 0.0 0.0 Si
2 6.0 0.714213 0.0 0.0 Si
2 6.0 1.428426 0.0 0.0 Si
2 6.0 0.003214 0.0 0.0 O
2 6.0 0.035711 0.0 0.0 O
2 6.0 0.071421 0.0 0.0 O
2 6.0 0.124987 0.0 0.0 O
2 6.0 0.214264 0.0 0.0 O
2 6.0 0.357106 0.0 0.0 O
2 6.0 0.714213 0.0 0.0 O
2 6.0 1.428426 0.0 0.0 O
4 6.0 0.000357 1.0 -1.0 Si Si
4 6.0 0.028569 1.0 -1.0 Si Si
4 6.0 0.089277 1.0 -1.0 Si Si
4 6.0 0.000357 2.0 -1.0 Si Si
4 6.0 0.028569 2.0 -1.0 Si Si
4 6.0 0.089277 2.0 -1.0 Si Si
4 6.0 0.000357 4.0 -1.0 Si Si
4 6.0 0.028569 4.0 -1.0 Si Si
4 6.0 0.089277 4.0 -1.0 Si Si
4 6.0 0.000357 1.0 1.0 Si Si
4 6.0 0.028569 1.0 1.0 Si Si
4 6.0 0.089277 1.0 1.0 Si Si
4 6.0 0.000357 2.0 1.0 Si Si
4 6.0 0.028569 2.0 1.0 Si Si
4 6.0 0.089277 2.0 1.0 Si Si
4 6.0 0.000357 4.0 1.0 Si Si
4 6.0 0.028569 4.0 1.0 Si Si
4 6.0 0.089277 4.0 1.0 Si Si
4 6.0 0.000357 1.0 -1.0 Si O
4 6.0 0.028569 1.0 -1.0 Si O
4 6.0 0.089277 1.0 -1.0 Si O
4 6.0 0.000357 2.0 -1.0 Si O
4 6.0 0.028569 2.0 -1.0 Si O
4 6.0 0.089277 2.0 -1.0 Si O
4 6.0 0.000357 4.0 -1.0 Si O
4 6.0 0.028569 4.0 -1.0 Si O
4 6.0 0.089277 4.0 -1.0 Si O
4 6.0 0.000357 1.0 1.0 Si O
4 6.0 0.028569 1.0 1.0 Si O
4 6.0 0.089277 1.0 1.0 Si O
4 6.0 0.000357 2.0 1.0 Si O
4 6.0 0.028569 2.0 1.0 Si O
4 6.0 0.089277 2.0 1.0 Si O
4 6.0 0.000357 4.0 1.0 Si O
4 6.0 0.028569 4.0 1.0 Si O
4 6.0 0.089277 4.0 1.0 Si O
4 6.0 0.000357 1.0 -1.0 O O
4 6.0 0.028569 1.0 -1.0 O O
4 6.0 0.089277 1.0 -1.0 O O
4 6.0 0.000357 2.0 -1.0 O O
4 6.0 0.028569 2.0 -1.0 O O
4 6.0 0.089277 2.0 -1.0 O O
4 6.0 0.000357 4.0 -1.0 O O
4 6.0 0.028569 4.0 -1.0 O O
4 6.0 0.089277 4.0 -1.0 O O
4 6.0 0.000357 1.0 1.0 O O
4 6.0 0.028569 1.0 1.0 O O
4 6.0 0.089277 1.0 1.0 O O
4 6.0 0.000357 2.0 1.0 O O
4 6.0 0.028569 2.0 1.0 O O
4 6.0 0.089277 2.0 1.0 O O
4 6.0 0.000357 4.0 1.0 O O
4 6.0 0.028569 4.0 1.0 O O
4 6.0 0.089277 4.0 1.0 O O
scale1 3.8426963309032285 2.878280093115749 2.23102354738058 1.649625958776714 1.0970602852492177 0.6362157718162508 0.2306407595002675 0.039834967549286456 6.4813341509721845 4.470129029907509 3.1474676346461576 1.9716977088834726 0.9817601853827986 0.3533202856308093 0.03757405109907057 0.001286592108231314 1.615018174190524 0.8992337695059681 0.2891024449138566 0.9410533294211596 0.5441451874083687 0.1816768776560084 0.5002368102376358 0.3075076769025882 0.12091749924569284 2.198410867968965 1.0099632896255606 0.26379878583410304 1.6197615832149346 0.7331012822830398 0.17354003631184875 0.9790818436147595 0.43417703338373714 0.0929547401249847 4.303608086313083 2.1103224480721186 0.5490999076456067 2.1435807240874682 1.015084348374471 0.2353153651937485 0.9544249661796863 0.45117268520701787 0.10237238535366817 12.587994927233154 6.748988405785591 2.2384124018455536 10.520920126039094 5.657059619597936 1.9185879150998164 8.144184366799394 4.3887753143931585 1.5199955053139094 2.824330521656666 1.2431255553723 0.25133648749358467 1.2182800314992388 0.5100530012757073 0.09094212346853689 0.45225190279480737 0.1767822470188206 0.02580089223489459 7.03571936825934 3.1341571047762975 0.6629147092275298 5.482392891058352 2.3816885456398076 0.4981227414151587 3.5916238611734412 1.511517913059996 0.2969807079822041
scale2 1.1213694873627782 0.8328294561377623 0.6458254576967112 0.4953965319780115 0.33938054944564033 0.2079687561483844 0.11833993632248643 0.031421956692683835 1.7185882451974064 1.3131264336390756 1.02972007989995 0.7266489825218705 0.4194321556428284 0.18903981417871285 0.03001075092676225 0.0012681343434354532 1.0119082718971064 0.5827111133787369 0.2022444396337585 0.6276917013144971 0.3529511162299401 0.12302205684960663 0.3988609785366893 0.2502144937997447 0.10153769219897574 1.2690434171435245 0.6471983177429207 0.2130451366603372 0.8432067541965695 0.43499999801992084 0.13450521113154343 0.4460349037135359 0.23222744785146796 0.06509550430821609 2.643882665325804 1.3607914599729398 0.3812530262132238 1.4216559113009908 0.6992202575775902 0.17896304836485108 0.690412761572473 0.33830388432626607 0.08148770379598626 5.344496403824106 2.9638922703877952 1.0493136658276574 4.206791309051514 2.3162343989971093 0.8409837436854052 3.012053102934952 1.640500656652106 0.6124860442344928 1.793026628441772 0.8271571903010836 0.18000957905765963 0.8744944657823869 0.38367532019213146 0.07332318309860636 0.37091504715269225 0.14894228106311772 0.02282699151667207 3.527602365537176 1.6996590459692436 0.40149450860829616 2.671718136640817 1.2444314541092845 0.295156188001989 1.6947690921725762 0.7648131235064665 0.1747854739573169
NET 2 30 30 1
LAYER 0 sigmoid
w0 0.3082198128634948 0.8330937751250829 0.029950927633440108 -0.17404411318240062 0.6243488796373009 1.1194410101047647 0.45484873293111844 -0.46282225756887896 -0.5530124966745273 -0.7998063600539072 -0.31359530695538507 -0.09810705868090727 -0.2936044004153063 -0.7870866924289934 -1.2080554825617134 0.26573498330733925 0.11044785508620006 0.6107679260690247 0.3765096001772866 0.243266342504275 -0.2520156357168796 0.33113539163782585 -0.1972845368672359 0.20350437550876302 -0.04136763699326929 -0.07672624778504514 0.20358092890137997 -0.02395452209858402 -0.17777560604367768 -0.3390733498718256 -0.32019977158737967 0.345240814483629 -0.10675067179449037 0.045900059900441305 -0.03699502458610275 -0.46966073054174123 -0.0830974559470816 0.44997290897057535 0.3082219780561891 0.32150613157556 0.097886551766812 0.17067925449736815 0.4001258095862931 -0.13515975379418976 0.14979664263742895 -0.3767884972273164 0.47787565437742163 0.14690076608850658 0.038747505903547 -0.13555910225756507 0.18327947768047997 0.6393712899254718 -0.26635361118297146 -0.3727920935671947 -0.4497891818516141 -0.23785707427831249 -0.14186590638687127 -0.3117911966519239 -0.10757152225164872 -0.09152222053478029 -0.3966749439886645 -0.30196307694017177 -0.3104080323532706 -0.05900556319298205 0.25073607920407875 0.35059927872253277 -0.203552478498246 -0.08396649701292103 0.04268463335232305 0.14371045858250173
b0 -0.145578839985
w1 -0.15413842318646762 0.23189689390586685 0.15246623764018785 0.12099878996415867 0.37067582766599977 0.522424624816311 0.2550645193698969 -0.4539084189278063 -0.15032940417239118 -0.33872298800236184 -0.24192696080463505 0.08966819697424239 -0.04449860939132886 -0.038075656051633835 -0.4389376251898324 0.33186220848268605 0.43337321151687913 -0.0035736041785131905 0.3915842984712184 -0.08284169813289566 0.25044191488108064 0.33822245146809193 -0.11803258011579026 -0.6595689714966964 0.12859131705508758 0.17935934793844802 -0.12533350926681533 -0.12414999401634172 -0.15287475875524487 -0.21452381178876423 0.05625561058468097 -0.17295342799726746 0.1954307449254168 -0.10209287068375057 0.20735814023112428 0.21272788574573634 0.344509710052313 0.41697802960043084 0.6091223402209762 0.20929504500194018 -0.4009836724195011 0.08844714515449413 0.36282928285493654 -0.05000381940687254 -0.016404118040022404 -0.38352183021980935 0.16484495843424649 -0.5382809215118181 -0.33380634832972156 0.0030453338124974997 -0.40297787083495473 -0.45723180831292615 0.16139860635910205 0.5547541832252322 0.026108688888722576 -0.1664040869104951 -0.16687012331437356 0.2767743040286916 0.13914483594878987 -0.12597565476031725 0.2198579845022469 -0.3717355723292324 0.0938767593821903 -0.16423793298845915 -0.2739805839945827 -0.24806526452593558 -0.3220767074670192 -0.4370968611515828 0.49998485203705767 -0.3011491866497402
b1 -0.289858448948
w2 -0.6223030580257871 0.15905961397526433 -0.14486174170775443 0.337993678315559 -0.24357933245020782 -0.3315155200708461 -0.257707865792481 -1.7929028518509722 0.35778688137272907 -0.005464887293410791 0.27846232796861276 0.007065272232691109 -0.1092616456827827 0.06025253712764288 0.15756515196401033 -0.30898723146052715 -0.05779693033843118 -0.005704093141007847 -0.026686691546684533 0.2997580949562017 0.12199235875993707 0.16759075557947922 -0.000988220072602364 0.3443473339135415 0.07758512938442373 -0.11912782777398213 -0.10301535637203284 -0.24932768187810778 0.20553561016484814 0.4883224816257444 -0.09453413007902746 -0.08591837068793096 -0.1903168759609103 0.5384852119421489 0.18684195559023264 -0.4836355284074553 -0.27662979036053265 -0.029403796426715634 0.36571376043672854 0.00949779215320762 0.3563038843736312 0.31288226503967526 0.7754355328818437 -0.26381485431022494 -0.10765981709551954 -0.31164694670237386 0.07433732576474407 -0.3955589743275304 0.10699877366334344 -0.10533326587895718 0.3988017133147653 0.1837678701416376 -0.45684006382424286 -0.4006092240895158 0.3588771324414799 0.0599993086002096 -0.007659588897547045 0.3584430888923615 -0.13215745766854214 0.31173098837558605 -0.3399498880993516 0.19604965140815628 0.17952138744760537 -0.2770262846967315 -0.45500673705457667 0.2501705460888498 -0.04854812260612974 -0.13353345721387042 -0.6287464152134228 0.09894959452435008
b2 -0.115231056703
w3 -0.01951817050771948 0.26915690081893184 0.20371487627185553 -0.22998410260778246 -0.4287959909912408 0.26168650252412196 -0.1642138209981955 -1.676135754293638 -0.2023991740737279 0.025329352033266517 0.028067041206395672 0.5557166188037003 0.11869371333708949 -0.4665924104804443 -0.39806472915220853 0.0036750118766780237 0.09259848690148526 -0.311027710265729 -0.06243970887130509 0.4371406685894612 0.34373656661328417 0.1283822427144127 -0.37917268372823426 0.008073412261133795 0.38312994414422735 -0.4282481853304258 -0.296507336707187 -0.32726834323134624 -0.03703238259994716 -0.05969545991168871 0.02194903489140537 -0.12037709516608658 0.3295693519773851 -0.15656885679806404 -0.11974832072925483 0.33247994762369193 -0.4586461466795621 0.2764714628925351 0.009263814951215277 0.320899016972039 0.1832275339810605 0.37028392534003063 -0.34414843977573584 -0.20754570522117147 0.00035275594007331824 0.026658131963328002 -0.28543526332878344 -0.18381315965178935 -0.09266862625462562 0.45201775683107165 0.12046230437941004 0.24910205520014186 0.20162383424993593 -0.1237694838686326 0.07898790304511627 0.22849061297478734 -0.016642748461672047 0.16605279005492918 0.011536297761295706 0.0021301299083620034 -0.04743900950702574 0.05600995524130583 0.12982779804358097 0.14009724267428922 0.06840022765469322 -0.05659828243071704 0.1366970315640936 -0.32777783550983713 -0.17888221066854604 -0.19852982758656773
b3 -0.0494250240535
w4 0.32583185008628174 -0.1428957308286263 0.5079141678188657 0.07709392567957273 -0.045196554423766515 -0.1451491480983077 0.0204211371509897 1.7024126704917775 0.1779340867795484 -0.11734724763590229 -0.3181304595126697 -0.11904441079964471 -0.018367952585433573 0.2934813851055513 0.7506485064256531 0.3238879168423263 0.48936465305516674 -0.03282314884374121 -0.2440083460184262 0.06580238770903624 -0.13895471435055856 0.12568090035221904 0.41656141503210564 -0.20249770852169927 -0.22298817030313842 0.5720071109266444 0.3258243998038342 0.15641241356516952 0.294131336228366 -0.09012065167586036 -0.15753344182342477 0.2215413554467377 -0.15443256542077655 -0.10587661177591455 0.3677132802178764 0.1792780371678474 -0.13737737569458508 -0.23144596529965447 0.2834727110081292 -0.6310266139014848 0.05929395557372687 0.36332537442451446 -0.6753990930109205 -0.1694300546544817 -0.21699335032407194 0.2621070096424672 0.08203942611471883 0.09180339637339124 -0.22673768415478118 0.11997185511936247 0.41320342615635747 -0.36747703854118446 -0.32620811853328385 0.1145985878228829 -0.04693906446084459 -0.30883452060151834 0.03162382291334517 0.22685476166918847 -0.151963570731943 -0.046753825385294885 -0.5095820380939587 0.04401707500920951 -0.28256115642288115 -0.526808262646203 0.3136671922665358 -0.15404682497545244 0.008466249478787756 0.02975034709859107 0.23066299282058983 0.22692149107033047
b4 0.0623805681446
w5 -0.9721033735031532 -0.2794041347058956 -0.6761657171612622 0.19737252471156164 0.03502973302047096 0.11353390782301302 0.15615933289924533 -0.7577891858269307 -0.13582782185477316 0.02655495195393512 -0.25068843270827934 0.23250192761285274 -0.1882897077039366 -0.3902688668260274 -0.5303707048214757 0.18474116347743472 -0.08374276184786762 0.2733361401702172 0.10508566587097877 0.2797161103783656 0.049037394672243495 0.5991024576060131 -0.467328775526178 0.026843552291160606 -0.0590071166917191 -0.028460882995968446 0.233091200137967 -0.612677118209625 0.08832591743145776 -0.36075814659120625 0.4710290911092967 0.3207379211434409 0.2865748835849194 -0.16792322662912934 -0.23228919678931784 0.20390656370004562 -0.22780031245851415 -0.0725293081092854 0.280155368338977 0.4173212846316201 0.30301506061358896 0.33479089963921427 0.25038147340483047 -0.20542292912965887 -0.1421950518142314 -0.19864599294505528 0.11088198832912503 -0.34929999947200435 0.04342803689351255 -0.31732104835650526 0.29151450344171126 0.25333948099855075 0.1419531697795879 0.3301412841762038 0.17656559828096322 0.060163301589163866 0.23591370533103026 0.34242722906326545 0.1881184369877795 -0.01913787664959402 0.35473887853012886 0.4540108842219452 0.23142271274634738 0.3650471650798628 0.16456429578533854 0.2355636337567743 -0.020749921274815796 0.2670295120986356 0.5115234322712712 -0.05894369467313425
b5 0.0242628863179
w6 -0.5299054722146744 -0.02772911865342339 0.09606616294247515 0.08849582474887133 -0.23357899465681115 0.3088737160677326 -0.3686690982778937 -0.9564951163807007 0.10602306767342674 -0.2792599867199136 0.28724850943583796 0.2199387965000341 -0.02787719243714066 -0.7225393395790104 -0.6235329120944062 0.011635237603754161 -0.16728443758858075 -0.16057916167192854 0.2569082978595195 -0.669201306597673 -0.2689750844050578 0.24632312348762958 -0.6514547681562747 -0.028876823865706353 0.10238667941665382 0.3084122106366856 0.18959969029296436 0.26404281292702353 -0.4126803825798465 0.3342129351685528 -0.23021779578452198 0.02851993628579449 -0.07406482083167323 0.3700142076430544 -0.29224822452097166 0.18780766423003764 0.3545325147225004 -0.13198426160622442 0.32038670138035064 -0.31256330544146405 -0.5303809140061382 -0.12754511307627706 -0.08037950713127441 -0.46983076309388166 -0.021810266098258268 0.03746241000928362 -0.042166610113573325 -0.3111400273587659 0.014854136660000888 0.20200530061434302 -0.03832953930739751 0.2393802083518305 -0.1585310322837757 0.15808147859511448 -0.2756176456612931 0.4104820712208534 0.01340269074764705 0.10619389620075084 -0.3751806148545426 0.07600424909669418 0.30580608512751445 0.29254708587177347 0.4868796054637754 0.3968170588370102 -0.36927632613131045 -0.18383229341419136 0.002584698049442025 -0.26685912050226185 -0.3252135093514214 -0.18746434234882514
b6 0.0059044401408
w7 0.06768164471432582 -0.06021357112627082 0.47130592255633896 0.09483836296729209 0.11149800889769879 1.2418210271292243 0.5489104798697165 -0.7025015712475363 -0.11760402683980521 -0.36254031612626586 0.3101952815388576 -0.2727586720014844 -0.2617530065533079 -0.11841563413988328 -0.43986211150212073 -0.4892337283268891 -0.09555655366392654 -0.05609240848659392 0.49645156615440267 -0.13082371890773073 -0.2766571119920974 0.46317994121727635 -0.08531123796918288 0.07716093687976001 0.6333315240664804 0.18776447446311242 -0.2157440564161521 -0.09108286418857728 -0.07848630942142645 0.1798609925790133 -0.33601175003914946 -0.2746475975539247 0.21689032618208443 -0.389018174926544 0.2769856904478027 -0.30514324987798225 0.3396448146064622 0.4339971563053201 0.10126500446833983 0.61221293698138 0.29267320583715045 -0.17762601905907718 -0.09680005066638672 0.1113837174501729 -0.1828516621851279 0.46534080352773216 0.3867610846618837 -0.2014984862605103 -0.4941550056794995 0.4884068505649731 0.40768111451478956 0.3693020606172705 -0.2140857293301808 -0.07615469780343623 -0.5723626501374693 0.05321365969911101 0.4390014018421855 0.25381326300229534 0.02525555528041829 -0.13739893338361478 -0.37653724222686885 0.4118461604023629 0.3616703023975777 -0.3064871670305201 0.07132243387129154 -0.011223155375659717 -0.17410333754770757 -0.15571988874048162 0.09250669781265884 -0.32329621350589116
b7 0.273282973578
w8 -0.03267945326200052 0.21850572826200104 0.7323640188858707 0.6381463861875464 0.24380676689846148 1.7570891962225734 1.5999509106334675 -0.2435514685503689 -0.17391796254205033 0.15494379894587168 -0.0005002985506216877 0.130393988550168 0.26211908872239803 -0.7408971361761416 -0.5328769222119296 -0.7513616986010726 0.22579449210852054 -0.05702594030571384 -0.13017455107313472 0.13636950542097803 0.21607072375995326 0.41781925251291596 -0.02383391880942502 -0.14406150355522568 0.6510280133889057 -0.15368805097412047 -0.17061947712733128 -0.28564664477539103 -0.025524825839392692 -0.1287320937730058 -0.33954346518381284 0.18613154601274928 0.17060369042623477 0.017826912430704462 0.1322180654099194 0.11375358908584578 -0.1784792825940574 -0.004703843882088287 -0.08446493146795137 0.2680378711604159 -0.054772717050315806 0.13700600433342233 0.09871364427901068 0.3936215825424716 0.4814943133466905 -0.4054311583875353 0.03976242197028232 0.35192788370598654 -0.26938234353608126 0.32571448692325294 0.8069783706533485 0.08202379562374115 -0.31418578756518295 0.36816316329465565 0.13416174284448326 -0.18027118273037773 -0.02490745026592538 -0.07677608918052091 -0.10444234745417218 0.2889837449657575 0.1033662881305829 0.17039809654975147 0.3150647961894572 -0.09631791612237518 0.2435075367118362 0.341522367029862 0.3828533360702118 0.14545432737269437 0.2997846912272854 -0.38858170379054374
b8 0.0386805600953
w9 0.026075741797136114 0.6065923898098877 -0.2428881579491686 -0.08797602897970758 0.28833831911932545 0.7715249782041915 -0.16616509864934395 -1.3811627916713118 -0.2637265780566824 0.33878342024005836 0.5740352136143368 0.20875491293717396 -0.2442813622517909 -0.5056947460121081 -0.5433320730269136 -0.2684860848736771 -0.2245958081980138 0.33973646680533776 0.17368312830255941 0.05820912842048571 -0.011836041309143154 0.05747017747873486 -0.4819741425593948 0.04981751636399659 0.3771389043513613 0.08393062733318259 -0.3248478404386849 0.09015512008777533 -0.3027621945398272 0.11215693462657848 -0.16118960987797867 0.027611383114306814 0.11217846200492318 0.06072242700376043 0.43575631196220227 0.01225771214642397 0.05973410843328338 -0.1303104443469288 0.020273547525343924 -0.40002517867502774 0.19620579703662389 0.09675860945948248 0.04160672218281921 -0.27779991248093877 0.3703813366418123 -0.2110871667289101 0.1844604373032073 -0.0885484778463651 0.09190604028776549 0.3452318946473616 0.28839269601728834 0.11433857275221172 0.3503306538511663 0.04225654256940323 -0.10126715659388748 -0.06400179051474192 0.08013963132033064 -0.07945467514119448 0.2009898611971059 0.3285305080196447 -0.09539258396882186 0.06089690115414666 0.11905316575041251 -0.30884700782846924 -0.0024861828306000783 -0.3035404591163202 -0.1487643356442651 -0.2517341793477641 0.055083100864003184 0.10689037198741688
b9 -0.067300999507
w10 -0.2016737074086956 0.3701849973666091 0.08125965797365921 -0.05792601513561776 0.1818315354790214 1.169815185884842 1.6072862730211441 0.04030162504311612 -0.2634893374563496 0.29135521922001156 0.19017274084944594 -0.3197234982687391 -0.29034804369288725 -1.165489778800337 -0.6769245891275593 -0.33552864869985444 -0.25401202293668235 0.1843983929614735 0.14701899663685794 0.07843161604092652 0.03592783006909306 0.09550677792801124 -0.2311379522251548 -0.09132526435310596 0.04678618556628859 0.3899146179038447 0.04998971031747674 0.45219413996774394 -0.13453934434389225 0.43422907429480756 -0.07706392713288351 -0.33681934400464625 -0.3955375093909672 -0.467244093491297 0.09949564792582956 0.021312248924317108 0.025361255174471183 0.39192849862432455 -0.36436209938520436 0.3321969306925095 -0.32194206002871184 -0.011982793651076431 0.05419201518470297 0.05415749979141526 -0.3636526689669805 0.09397780380458867 0.08152285619348747 0.38104556171167575 0.3700641138942589 -0.13749340474668725 0.41112244412622834 -0.16874469144546075 0.1873675658869345 -0.14385073000314857 -0.3210120182239483 0.08074952827527102 0.3861203255379447 -0.030563414867162807 -0.3626384860405284 -0.3691328313382205 -0.10089980200133652 0.07655018909047327 0.132495616368412 -0.5792249563989963 0.24360440965279753 0.27151733340088663 0.03341844041324709 0.019491271250783315 -0.3496463101773943 -0.2786982447465991
b10 0.282136136875
w11 0.06429882486835929 0.3711477657764471 0.02793763242334495 0.4751481502792456 0.5586357965920852 1.2841780030748575 0.9556551801098176 -0.6903598059209274 0.4406382690023619 -0.17462246791865593 0.4907855137760313 -0.18527780824271814 0.45423714201427545 -0.7142509963539243 -0.4057697871420019 -0.2228182805617692 -0.09417636619663187 -0.2043397948165475 0.31806581029008785 0.4236171305519955 0.14376419117415046 -0.08151003811529595 0.3291078567842186 -0.16944423115882928 0.056403405013622884 0.18296220833817836 -0.05106245466778018 -0.0420494729173253 -0.2241228338419507 -0.2419880871065459 -0.03174128650325709 -0.036151994356748 0.6235235877912022 0.2219399469267588 -0.09217929520820495 -0.41229443758795564 -0.06340286526735887 -0.09100539704922664 0.7141717074845241 -0.08672052928318198 0.5206362275376475 -0.08487284163752176 0.17441489544534888 -0.264497844271304 0.2458981994634415 -0.08324516706901205 -0.36768509650278053 0.30177100777362675 -0.20249789755962525 -0.20007938144008722 0.03808530183654588 -0.168502722135609 -0.04116264409271134 0.37192025457410216 -0.1752373846511559 0.05105205917287759 -0.37407358558376175 0.057940946111807036 -0.042572065872423744 -0.06055249788677897 2.670746199373938e-05 -0.21292069087471496 -0.33762956871114025 -0.2346834373010721 0.0010200316566822726 -0.5606217876256224 -0.09259803442142915 -0.025640496883838338 -0.36810273615704814 0.32277818275786263
b11 0.445931174496
w12 0.29455114538539334 0.022923167439549617 -0.354662269665351 -0.043097261407654484 -0.17734583839932141 1.0341888574261564 0.6039891094453436 -1.0316954353193757 -0.5609914255293332 -0.33150006695326467 -0.032031437057115246 -0.23424978181892173 0.09361747330821264 -0.8289558969216204 -0.3250023773211157 -0.39141649149297203 0.20916749669927284 -0.149035290293568 0.2868812865411186 -0.5341698020560773 -0.3629443978982192 0.19518798116030667 0.1058448244549156 -0.37695542447631414 -0.25711779175763927 0.007836889911959523 0.13817623397033446 -0.01158333383903106 -0.29334176618232344 0.19299349623803386 -0.24206481124136722 -0.08387119736483893 -0.10410028720078973 0.31984581211846624 0.003095997415103041 0.19122177411497895 0.044794231056496096 0.0014627046962176662 -0.12508179493151012 0.43773768801041424 0.039025803756585764 0.5022041599080702 0.2242293254278842 0.010786146147991768 0.010810557331149571 -0.16903225684832382 0.27229036216735597 -0.1892967705377713 0.2717169002985505 0.2950925375292979 -0.22926152058968363 -0.3723666013137759 0.0436130260687638 -0.022251605492019665 0.011537333639953216 -0.1596021791041384 -0.32535764818675283 -0.4506847360036935 0.08882466003858469 0.11638607309072539 -0.29172632818195926 0.47817633431962847 0.3125941213959201 0.3209807405317924 -0.3666575134516442 0.09092981646057066 0.15793467789666155 0.08187100445222112 -0.0848836153544641 -0.41632020477006776
b12 -0.520377602446
w13 -0.037356814467240144 0.18751196007988022 0.6365987050735914 0.6733982995031833 0.17003328554792602 1.3712393359925665 0.7900655373383462 -0.3900995370431442 0.3166190752089584 0.36089567854446564 0.3393440569302149 0.25759051116987713 0.21229444772756884 0.08779136094379665 -0.44008203722863076 -0.36836895979603657 -0.17715881009713957 0.0685670864153893 -0.2707932812809559 0.11015805662926817 -0.11492555048535366 0.6221474582457469 -0.35196431445992926 0.2330534037440596 0.29274342818239985 -0.4258135056367739 0.45245215240268527 -0.31132802288858225 -0.20650281649476288 -0.3183759314955282 -0.32296140095537174 -0.20201906593072086 0.05303876754387874 -0.3963838347446643 0.3169943855055695 0.16746123034190105 0.2445134179942945 0.02131487717851961 0.4902563468093046 0.5091905177812096 0.08109606416472422 -0.11557613173386583 -0.028313846974030804 0.14269816575398261 0.012388935746491735 -0.09550861235653643 0.217983543787513 0.17042081329793363 0.16818651576591157 0.21695462185955117 0.2993415540753618 -0.0006909855849041591 -0.12852272453281396 -0.1030415650930447 -0.40909740125764976 -0.0793116067138516 0.2942653880963152 -0.2922411349862521 0.12031059091482839 -0.578702756159029 0.24922144321518713 -0.061779805878412856 -0.4165270078239743 -0.2709584876171073 -0.10519384483561631 0.26631897745300354 -0.2897475568310479 0.08786947254458591 -0.36847630938268566 -0.6147043121251495
b13 -0.0940440552775
w14 0.498613769425858 0.5582866598821523 -0.2057507606615589 0.06502864696314119 0.09956740387978269 1.1642496775906528 -0.29682617414674584 -1.1865902294917463 0.32114488204624075 0.1456784451704786 -0.2751162356523423 0.06843467022582601 -0.10600931254924219 -0.08565081818022634 -0.22429258923652376 -0.3194953532413745 0.03533036518962687 0.1426454939511707 -0.2745111749804602 0.06585795214897545 -0.21784473094849421 0.523820532369963 -0.13887866537646573 -0.17153108757304433 -0.40142812859026794 -0.2914505644395652 0.1711203799374656 -0.008911312669038919 -0.21506288624888684 0.22035211650674383 -0.47223386388586513 0.10847437856994281 0.22896567979156007 -0.15611769933964928 -0.24871958039477088 -0.14580842521300783 0.19149608776536162 -0.11842144927433212 0.03162249337963802 0.426611697311427 0.034181870689310646 -0.00980748079938701 0.044820681497077706 0.19277982805896987 0.16558031824010308 0.1589649883958023 -0.0551508205883805 0.4118859220634818 -0.0028977805807824056 0.18365058375321658 -0.11903328756221757 0.6607966224410138 -0.2653487770306853 -0.4050427954524423 0.22261053999248157 0.11183412916028149 -0.5266723950731619 -0.03929897123012428 0.2168575842430192 0.45495534203453936 -0.3901979435358001 -0.271061193130129 0.16684399567542235 0.5549370191107531 -0.4285469456375596 -0.2563304376019894 -0.22305395947041176 -0.23614791696573342 -0.22903605635468666 0.17264597182147126
b14 -0.148947749042
w15 0.2445438442427371 0.06216270585504998 0.1890490918540266 0.39274103819104045 0.0808333867163922 1.5343317161385621 1.109322861536683 -0.9201708793500534 -0.17833941672775336 -0.42166570720012225 -0.14627546499803223 0.015047408894854297 -0.03731059293015336 0.0716972871603394 -0.3827269556167375 0.38054210346405243 0.045633775978415 -0.017264204727575637 -0.05685890335553937 0.13221467840670675 0.29442631096960536 0.23293247370166054 0.413864182150705 0.11396506849437107 0.3117058658268467 0.15954356041343065 -0.14709569674595505 0.135385698395981 0.21406466664581378 0.2613759881149136 -0.2673387212328977 0.3442713746874125 0.032579586160838725 -0.13155616166249412 -0.02007229797071054 0.3848812315140609 0.4876150610068702 -0.36627296827602157 0.0361183290509529 -0.17348194521993282 0.3428517473879616 0.2863636880791115 0.19380887262613547 -0.28862007167480186 -0.42203397066067094 -0.13014639707509854 0.23442009748759726 0.06762468894424559 -0.06842492430873552 0.32435857831647963 0.3890636165411066 0.23394093277692304 -0.30954172937549745 -0.4028485525749883 0.3307374795551192 -0.2490466059057747 -0.4631788904427875 0.4437487626125975 0.19126378772979605 -0.12672751438883728 -0.274542593355994 0.26356048380229186 -0.11374491431783924 -0.12122028478340025 0.25887125505614017 -0.36276899207249674 -0.028561534664887315 -0.4805483944592218 -0.5830894337941198 -0.6212784969043366
b15 0.026920196822
w16 -0.19184380248560237 0.043252565482055444 0.526656802912888 0.3714249082543523 0.0134048415528077 1.5069596779806116 1.5223867692977695 -0.14033606911452662 0.15937776319602076 -0.05124197033304064 -0.030031933016436963 -0.22348076136588232 -0.6421374736323344 -0.9418956567643378 -0.8645154463358156 -0.2104485334588541 -0.24380029169487158 0.3582674044220096 0.25178121592976793 -0.22114542831093675 -0.2268818680944733 0.21283590225419444 -0.172325779594114 0.1933357187366421 0.5962457249291729 -0.10616997533212204 0.2783020719440489 0.5100800955910946 0.04885353752177134 0.025792686879621732 -0.09806007155234654 -0.4020772012703715 -0.193286863520504 -0.20817161625585726 0.33870158227022235 0.3368588316528051 0.19464894568576419 0.05829398653856344 -0.010578724877650146 -0.47814189692183645 0.5255002870041697 0.4554746963737764 0.2619310115158496 0.16723933518280476 0.4662335049010835 -0.15291174097278595 0.4918152443875359 0.0007815156896905653 0.12734286281415752 0.07527099581556065 0.24320149115131995 -0.34788768599519326 -0.07395825380707667 -0.3174607955635538 -0.09975995901651903 0.023211369190508317 0.38056179700794074 -0.32459108731620434 -0.0556153093689993 -0.21473394430836792 -0.06305079807324641 -0.28066358291794347 -0.3765789921675341 -0.44716320203357024 -0.3322821506598392 -0.06445439099006384 0.09699040310602218 0.2601752065028078 -0.21496361517667625 -0.12245491407367337
b16 0.159139607075
w17 0.10446971072276147 -0.05998958490146507 0.1824380651913694 0.18006159398878277 -0.3223875845059263 0.18873517318243338 -0.4437248104870957 -1.6234336417385007 -0.07955103350016833 -0.28039466857204526 0.17193965181162296 0.5919768683119558 -0.37520347116814984 -0.014444946401113563 -0.4544950127172885 -0.12786748750851948 -0.22764209163405164 0.22545972086596164 -0.22251289052754594 -0.1316788794034521 0.021982425782258872 0.4920493261738752 -0.006296813590661763 -0.08018891310241752 0.32056436045538506 0.039162406982985336 -0.24880035454180358 0.005562872271040707 -0.024970153337211986 0.5359246874848053 -0.2599426200411472 -0.17506316070294295 0.2542745360572619 0.019120312653321907 0.1030361452131682 0.04446906329986676 -0.43375787446109143 -0.010581494400426607 0.28521780193757557 0.035741166853440844 -0.0915350086261513 0.4410401987586964 -0.21020923656668786 0.3603667544014143 -0.33874525124881455 -0.2328351436747912 -0.07167927634303868 0.1497635881101571 0.06754543945818349 0.3677224036330647 0.45317398927683933 0.4683416099765199 -0.5055123367670527 -0.13119647144469512 0.24960460081076513 -0.24285716091899373 -0.39978821843960644 -0.14957797689191438 0.08932495659338727 0.015844786299412505 0.4710732636553224 0.21552762158428826 -0.3437037940374846 0.14629256044364364 -0.4051812635695228 -0.050328704995916254 0.07337799150166283 -0.33117257323377164 -0.1306842333060175 0.033407709957024675
b17 -0.17885291919
w18 -0.38009521557007664 0.2396381234041198 0.2316542242457561 0.12476001230466871 -0.04886481021492093 -0.07508021335116988 -0.133082124065189 -2.690070695636494 -0.3295352284702396 -0.09377370298578322 0.24997944147046902 0.03275322141133163 0.26808589338165684 0.26829989975779156 -0.48962871727208995 -0.5959559993753852 -0.22455552960735034 0.36347523442532254 -0.48095427727584206 -0.11498118752924484 0.24663371320606892 -0.2963986215858193 0.514701343877113 0.0010177973549710616 0.039789827644987064 -0.06824472709696083 0.26226833835862573 -0.49432154321397953 -0.16270764113304176 0.2842291639496613 0.29664563280299444 -0.0010889970469296836 0.33313951698422345 0.11512555995509982 -0.04500678133297495 -0.034432275992971544 0.015209733650711453 0.12687766563188696 -0.10248409499754865 -0.07335288237177397 0.40652889249621954 0.4093263441632437 -0.20418546869548823 0.30582058900801007 0.15961253768511222 0.3514369126972258 -0.22082535494794467 -0.054909776678346164 0.409503629252512 -0.02779786412575198 0.04015621911630299 -0.02511681292463387 -0.3889827813762137 0.044656800105670136 0.1551152356045878 0.333079729177533 -0.31912749984317795 0.029629806709614775 -0.2945640332584002 -0.4185875297730267 -0.25031123401946476 0.2799099846571374 0.14681644064094845 0.25098284358621314 -0.09764234710608093 -0.22603464831746217 -0.11248772892504112 0.09878193763752965 -0.07958037110655777 0.025297278227076277
b18 -0.152675546301
w19 0.6141077647824945 0.21026342772987766 0.2799874188786491 0.5762224262811843 0.325376222173555 1.53530443348157 1.848794799766454 -0.2134251742546442 -0.20330654107358814 0.013313643627127537 0.49978720363292256 -0.05444586567314909 0.3826185524489881 -0.478379511605727 -0.48664520936972383 -0.46367447557727864 0.19535094544526366 0.3926653818403815 0.18310036404327248 -0.21754118402910555 0.4104899973850946 -0.2710502003043167 -0.6894824008861724 0.3053009214488336 0.5479237371421819 0.14308305749567657 0.29421821607176024 -0.4564802655261615 -0.10250845478226488 -0.5726027096024434 -0.1992252277492723 -0.40805931672316614 -0.10963321992855767 0.0716094451061965 0.5578142794846396 0.2657053709332251 0.21697911636907644 -0.4532618899256572 -0.2289611336324093 0.4352559110237525 0.2916015612287326 0.19936737363502638 0.17415390953045767 0.022980448781389214 0.49088216180109157 -0.3068620966033834 -0.10242071099507259 -0.2627661225955285 -0.3047309550588994 0.0677684486310599 0.08081358676292992 -0.07040288183411302 -0.30238757383441633 -0.533492417232382 -0.089749787766805 -0.06192905588715606 -0.09376257672667039 -0.10128563529548229 0.2561917886732883 -0.07695958839026203 -0.09439587145119341 -0.03190461976123982 0.17134120381827936 -0.3860241542460973 0.2224601190097298 2.1080957532115645e-05 -0.4552573626633051 -0.11233332419697926 0.0033368904273525244 -0.04546165637811389
b19 0.099752535508
w20 -0.01899501977471183 0.11846956197022009 0.5103090012065036 0.6157257198867679 0.03589024636156108 1.9301659437051282 1.3254299282693063 -0.32441978118245324 -0.5145785890397269 -0.4130307232549252 -0.38224429718893793 -0.23134664848650904 0.12847383517410257 -0.748581657086287 -0.7826687545473192 0.25708449962736285 -0.33553579585750765 -0.0040887722942441 0.11748096826671693 -0.018252495778351294 -0.4008078050635888 0.5770311603926677 -0.2657610628099013 -0.06844246101155085 0.06668221806219385 0.3500026682047854 -0.17084590309321437 0.27420106624074797 0.3521245491514307 0.3534095427362301 -0.5705506847116664 -0.3492166483801207 0.05091757529113193 -0.32619271336214195 0.0908912008249444 0.05921280233628002 -0.13861511850462405 -0.1158082733478074 -0.3693001029846011 -0.04870326570657631 0.49740514647871037 0.3230977319414528 0.16917008388083457 -0.018676595626073687 0.14666690325765694 0.3069706185787071 0.011065690147679483 0.22546136160716065 -0.3755484445128764 0.6483844092661127 0.10241704123597291 -0.29716299437436827 -0.2411013330804566 0.43610933025893267 0.47804395886678913 0.03980932537980577 -0.5434517952101433 -0.33263515195627447 0.38487770235005986 0.029039117932011364 -0.6687684935956464 0.10573792500776756 0.26153245214306736 0.0788235250292302 -0.11523815588692664 -0.16023278647252098 -0.470973978499911 0.1774047241774387 -0.3698731646878839 -0.4043880519580411
b20 -0.222708257248
w21 -0.14050933599048485 0.027348586365937233 0.19677011464562444 0.01677214765241542 0.29962607935615454 0.5153440165461876 -0.5218795151634571 -1.4489431985855632 0.33599165371486256 -0.23188864776021856 0.2694459953726386 0.5859104658066855 -0.3136545413566571 0.03137326802956903 -0.294348446557908 -0.19258485482837065 0.04630536521039268 -0.5461274627423903 0.32821554791625696 -0.2852302540422891 0.11726440572285833 0.4901340716515174 0.5538318196692467 0.2563458202849779 -0.0625104278558124 -0.02228746003917217 0.36025346605675584 -0.5821474141552804 0.06512495845660586 -0.19390826694470065 -0.5305918592753803 0.3601443705244337 0.14523869019687538 -0.33472079601904736 -0.1529985585396002 -0.13958449094594835 0.10323935614775787 0.198017361510312 -0.15019206002117763 0.06163439519939765 0.11090186531897514 0.014788401665812734 -0.049642706997103776 -0.08573038634524248 0.23955294281568357 -0.23209383358735966 -0.16245368653134087 0.12644876505104327 0.35375288400094146 0.18232992694062738 0.33190171776471517 0.2088240630809796 0.26761520279668904 0.25058109584340565 -0.0003033374362716184 -0.03297628187834927 -0.042868956356446344 0.0629055438191248 0.031311590779979755 0.2587634948910837 -0.30755793490171907 -0.05040820682486998 0.06625771532998546 0.18686407938178615 0.1758376335227923 -0.41945881318530104 -0.3770442603644014 -0.09890426606631872 -0.11752097361771655 -0.19487902080169345
b21 0.00732713373467
w22 -0.3627260540694818 0.0796194265720516 -0.14674954046334304 -0.16579097699438192 -0.5307478376993392 0.6587314409627559 0.3011747779920534 -0.8768342852952982 0.1004213485424848 0.254531013345283 0.3465979860841096 -0.07186218977928767 -0.05938460915395744 -0.4516599971573068 -0.7496748710080411 0.11930122311953159 -0.004743734953892863 0.1707708728922519 0.07484569144610731 0.06664029908630895 -0.008651661733849207 0.1613028678551406 -0.45630628020269653 -0.1091374702019718 -0.3392383372699299 -0.13585336237131354 -0.12871946342369647 -0.2031206326161468 0.2066215755611041 -0.5330104882613117 -0.2859719791291682 0.30522405644426176 -0.3344953206846685 0.11654085895350906 0.24791944894189016 0.47415775413024924 -0.3156973138731803 -0.14131480423081255 0.3648206676427907 0.07726786335157278 0.10497934276843997 0.3406177450996144 0.3414997751470372 -0.31695211702381304 -0.06583445768774586 -0.18197092071665058 -0.027433606184986317 0.24695705977630128 -0.013386842424946178 0.42288442108783336 0.3840137071289307 0.6094446166723605 -0.3358163108681902 0.29180808333307784 -0.18807139935468678 -0.13928840111117277 -0.031616690015487885 0.13212984696413008 0.4082528772552947 0.041489884898134946 -0.06947751489054152 0.04995593092047322 -0.36161050012860907 -0.5279248575585832 -0.36385679777576124 0.2552043818949588 0.03287743589789351 0.04203733922630958 -0.0367992935446048 -0.20044862548728148
b22 -0.438779657438
w23 0.010373771167891213 -0.17037948908060743 0.156675420774012 -0.08571655505064565 0.37814943515866645 0.4914650745316825 0.6902966951638041 -0.20577887450767915 -0.034823304632195094 -0.5314742618297081 -0.4447533572357002 -0.03272436728102086 -0.913159512484884 -0.49255953108450035 -1.066225908515362 0.29905526757158696 0.548660698450237 0.5427464946096497 0.4190398170658332 0.1265081362339505 0.24906636165060292 0.40503424070960165 -0.08618320105798033 -0.22714253090571185 0.016841387597254866 0.07542516665355828 0.18822065599436683 -0.029284162095271186 -0.029365237397475426 0.3029112206201877 -0.3484186117806459 -0.5095066555731071 -0.3906626634383909 0.32805477179552656 0.31076032108408974 0.24689419613067062 -0.06392824849254812 0.4320071830541066 0.08557785302523702 0.2649137359831331 -0.2967342777312836 0.15826070332075806 0.06224031798246862 0.19446198314515967 0.22129426857987017 -0.2208585923044783 -0.29078874037443353 0.18708066866508336 0.09201094940904472 0.17757664967923728 -0.23699291187662697 -0.26826425208371174 0.026219940260101667 0.09632348117872487 -0.5287810641593935 0.09646296914184628 -0.12340989968616203 -0.07058534988092027 0.08976320475486578 -0.19727753304295945 -0.18826258145608626 -0.17598182536905332 -0.4428123947273558 0.5456240619629248 0.03214013251230321 0.038182588297481564 0.1720452390360827 -0.30574119830390917 -0.28398569378935495 0.2035983207593013
b23 0.251393826366
w24 -0.27376798669111224 0.07708353000453581 0.708863189764961 0.6306333792517277 0.5158120713169828 1.6604587648870381 0.5892114351065656 -1.1558756573949351 0.047140659667266833 -0.3159313214892187 0.4521793177229253 -0.020768612922079613 -0.5716350510863732 -0.17027725308555144 -0.6954687827880531 -0.24467416887086346 0.233781626278854 -0.5076614447065845 0.226325498120101 -0.37926745351148183 0.37117938074140605 0.012745696879836902 0.30205151166018385 0.4418551338509556 -0.19684194444187578 0.5106152805369643 0.3285387146633202 -0.2996534606265141 -0.5054273909054714 0.43909364058741085 0.10902381878364453 0.22943712150837353 -0.47089623870379704 0.3435105248893159 -0.22860346144889443 -0.30826635674087405 -0.12036976057016562 0.29151438320243184 0.3003515995642823 -0.2541298758555726 0.20966559333198578 0.589912043132038 -0.04565461668807846 -0.1359903368802779 0.1535147929491688 0.08039107741486357 0.13885012494996468 -0.2739986259211743 0.128022253575536 0.18103051034111894 0.3959070926266001 0.1518710019844648 -0.35464728244959093 -0.24789194322201752 -0.1980812175044521 0.0733995865572675 -0.39562110036113673 -0.17054287657223863 0.3854257317121863 0.4551147962007206 -0.3081471394736937 0.2354272665634195 0.1538568369014488 -0.1495680661269122 -0.2210535382737557 0.23296539918398926 -0.06284339791716467 -0.25811682235290245 -0.2683062942868457 -0.6658867236539632
b24 0.177151865766
w25 0.650189728504274 0.6132170845573773 -0.04342775635593173 0.11871727818450885 0.15222481711085298 1.7786412090183423 1.1897152363380712 -0.1528436438944876 0.3576450706948011 -0.36548704495777024 0.09094255668532429 0.05496192843792669 0.38849921859675085 -0.37167110878155224 -0.3073033900478171 0.004593731479083342 0.17180807570647477 0.3165053803464224 0.18376119370415864 -0.014235409131271711 0.6468565800867103 -0.16131296238309342 -0.34496896936682003 0.06055717060543171 0.0626315351636915 0.15949869244609996 -0.4793029200779029 -0.3959592111812403 0.43600795010522725 0.46252749511668373 0.13718414849260396 0.15647975717370294 -0.20599558891973196 -0.041702589201161655 -0.19885142344085335 0.2579677340725533 0.04690855690820119 0.13847490470548562 -0.08901902284963419 0.3494309944679461 0.5778198246929176 0.39036103443221765 -0.06830296959197382 0.22594132140737505 0.3233640776862672 -0.18166315490135873 -0.28064252079250973 -0.08319824349184937 -0.3387675182394138 0.5809539469061044 -0.28569145723640416 -0.32652241341216615 0.3581158311043496 -0.16718016509678263 -0.06753248398683669 -0.23864546968513775 0.16941877543768447 -0.06928801072064238 0.29033206578228116 -0.1316265327513638 -0.539363415450008 0.2038321486002081 -0.0281507931329902 -0.20447726748602088 -0.0017420264260526574 -0.6586172127956549 -0.21870617598444847 -0.2761521722403851 0.040209790530450144 -0.5924767608003741
b25 0.318589913216
w26 -1.133601219043002 -1.3264085110520887 -0.5868740430869671 -0.08000236171489004 -0.05297456046600742 -0.7259175989711716 -0.5237642114450144 -1.066521472633195 -0.34030613153862466 -1.0313231193371803 -0.14146380247299273 0.3310738112073538 0.7035158154003812 0.6422118818180708 -0.18605392812055915 -0.14296993180226764 0.2050312136719509 0.16917012907498039 -0.23460794524879927 0.2568910608035232 -0.4467344083272742 0.31235637848289166 0.5614151300956697 0.4962017075766384 0.33481050703569115 -0.7211614395985251 -0.38782535203594115 -0.12358410212718315 0.38634498346675933 -0.013438069302324598 0.37850000839410647 0.09831960345515185 0.3979143137058996 -0.15001585445819343 -0.5107379595394157 0.014066666744206273 -0.5378996637611542 -0.05308063663899782 0.25671223934039133 0.22477331970508976 0.2305040157671306 -0.1591412961830657 0.029546253392759503 -0.4710656746349058 0.07401078015510891 0.11231231249588688 -0.013247125194028073 0.14191467859834264 0.5424721824078045 -0.41848332907263563 -0.09219257716595121 0.6283321685882315 0.011392335058670646 0.29612611557258456 0.4372187774050785 0.29700025529228774 0.1844833338281027 0.299018749808256 0.72717078682261 -0.0890670262584473 -0.1136916479431419 -0.5900866102213129 -0.12433042067109151 0.2907391784454465 0.08484226909922282 0.154285950668546 0.5579829748857774 0.27914931110802294 -0.48145295167332897 0.49272066745007514
b26 -0.508741835661
w27 -0.2809181693484057 0.2914018811193787 0.2549210926308631 -0.4761626564137647 -0.28348476201318284 0.9447809558097053 0.39622840377645513 -1.8781989295088628 -0.21793750738032808 0.3749781571565662 0.2676741792819895 0.08122566321030382 -0.1868982618622954 -0.09541439653211894 -0.2193763302516927 -0.1223067735020772 0.25381338506254697 -0.025446563001173005 -0.30344152812774344 0.02308287855034034 -0.06468423859664946 -0.40593719913364507 -0.9519995748156996 -0.26036847007494396 -0.08016024484524899 0.2210273891813302 -0.2902703545598493 0.20266896460974496 -0.2410088534987494 -0.07522005016671172 0.07043361576536938 -0.30813290801602894 -0.07963788018332796 -0.4699764819005172 0.4632985182837938 -0.10806818775782222 0.3579099298578298 -0.3650198353078953 -0.30201995376738633 0.39167782200356877 -0.043641485659334046 -0.006473857013925949 -0.1792998257795014 -0.15781404965250234 0.1961894356725794 0.05913260105477003 -0.4228411865926807 0.345237797219401 0.31480029410586835 0.23992433357470902 0.1018926498142953 0.03885235286497122 -0.2425418421583997 0.5469022319315026 -0.42301610153718594 -0.3436538919580651 -0.1350819807055301 0.10446613594274162 0.19255050260401257 -0.037102159563261586 -0.04708807819604418 -0.1746930727509711 0.01894695384762118 -0.2872874941200845 -0.07434955938806015 0.1902744480938988 0.20067377682381085 -0.3172420416752455 -0.007757564640822975 -0.11684936428251189
b27 -0.347922061293
w28 0.06075446855491096 -0.07880518805683094 -0.3293104141908749 0.20882020948235314 -0.41273203543121767 -0.3549817512381129 -0.7022875124014467 -2.175305540432357 -0.12357331982199865 0.12374372269340801 -0.12712542365521534 0.15162804117822534 0.2026895739324211 0.31995603831685315 -0.27175339851056973 -0.2751589344012678 -0.3721001281641774 -0.21360012996421432 -0.05562274387089788 0.24805494145267534 0.4320238717177687 -0.30176732887635727 0.08873022481142663 0.10505877011225284 0.4249762261345666 -0.4048614924947706 0.10002681938098949 -0.5262111653562223 -0.27713285718800734 -0.10160933188848283 0.0002881060040007864 0.5327090784771514 0.2881195536524514 0.19134878904451785 0.33188833114800137 -0.06142022838821466 -0.27363512421637737 -0.22368588294872158 0.18655808790616507 -0.004749630643700763 0.6930281624203495 0.4217097921257421 0.6928915111013106 0.10768982032343605 -0.17512196243207434 0.1278047038231574 -0.1163715119611075 -0.2225634724958043 0.3851611699575744 0.33100375923806663 0.1449496756218982 0.15943674465179916 0.15133248237561223 0.37100565418607795 0.3425600919564843 -0.4344207236566298 -0.06400361230997036 -0.05218479649922406 0.15285802383702662 0.09183730988557529 -0.46006095109337025 0.08953987870459934 0.22710205393394675 -0.2468977925635063 0.2184467281428094 -0.37291145795775715 -0.1419082365565845 -0.3818953347225693 -0.118790509601697 -0.047247432676146006
b28 0.218733414143
w29 0.2619669679493637 -0.0694239516592824 0.10986179083753245 -0.15726438308243598 -0.12719047545065318 0.6088263131057253 -0.8567024304916547 -1.2916329298841849 0.15061357967093578 -0.6956786510910132 0.14136092819245774 0.3610731981478251 -0.014897569644353698 -0.022804888509429928 -0.770842367001969 -0.1576548112597509 -0.39706113134599547 0.5046399612076631 -0.3536890694849126 0.0470423873419781 0.0726982517934751 0.34467392675010616 0.21555940942635657 0.5275066120148836 0.24670828846065768 0.26308104212308364 -0.2392923353962195 -0.38399124621433095 -0.10130236752082024 0.43985952184473565 -0.37082281427534686 -0.07982216175988002 0.1379883270479795 -0.2616050478186669 -0.3816203502046351 0.17778656807076815 -0.16023986331908946 -0.13523452422849047 0.34201865310641055 0.11018546017698777 -0.08870654584204236 0.16011018111709982 0.2602104665734238 -0.21155822441764988 0.2906324652280779 0.39806137930455504 -0.183958413576653 -0.38957222497278343 0.17573501657345447 0.5156126264662237 0.2250269978029405 0.6923193420430113 0.13495159968140774 -0.012048323939306228 0.10650792151154455 0.20050232220750155 -0.1875899798802685 -0.6181067131292269 -0.43421364584265193 -0.0970440773737272 -0.11822359010670111 0.026855455769655857 0.3491464345214824 0.03612938727429683 0.2036819479625661 -0.04792704270398551 -0.012963852695216755 0.03007029699136628 0.0864574431395053 -0.22499557411072643
b29 0.191067738309
LAYER 1 sigmoid
w0 0.33762947961660317 0.1528732422974628 0.5070049305759261 0.09427932177941363 0.04867883324076111 0.20087501053120665 -0.06378065582419355 0.29084058658912426 0.34687556500976763 0.06662074393308255 0.43393343279945223 0.16879326961702606 0.009207451827033043 0.03501745243854886 0.28721365433273016 0.6741569717476178 0.13320826088697307 0.5928295879007157 -0.2585678645193112 0.18076407182595422 -0.2064163470760235 -0.18404519164401567 -0.1183654989553798 0.16836305929293635 0.4494214765207878 0.3846967936063415 0.2497593406573793 0.21023418192353638 0.2877512423165858 0.018886520398804004
b0 0.634314228177
w1 -0.43920886706974066 -0.09589005042563711 -0.21875441883905686 -0.07924246565670977 0.22747425762850512 -0.48166525858786846 -0.15159561760555929 0.28036402858406756 0.057635175800074476 -0.27764899242463653 0.11164140905180274 -0.36858888742644197 -0.7281005432515578 0.3233494732637806 -0.05430067440424403 -0.10532283752695419 -0.34758744189012675 -0.05502457840034072 0.03911572119309542 -0.4254477861059105 -0.38252365956359274 0.1362238351679578 -0.492522716968861 -0.38804271122550277 0.016603114860260008 -0.3739167294213608 0.11069167224880629 -0.3868912617415126 -0.17520309717841734 0.10529032519175342
b1 0.0734150486478
w2 0.09040359307259842 0.2884339975406792 0.20387284805683092 0.5721273035047503 0.10739355013492079 0.5264601494420822 0.5904590512776127 0.023117837994147936 0.6271366285819474 0.018251949505884303 0.13194404220698988 -0.17469490639561278 0.14386509517541807 0.03524637091711826 0.09732894141918907 0.08222690093302293 0.42606345385896566 0.05465530715389227 -0.13745611446044345 0.4575923349560929 0.3196293926182181 0.23154196780884123 0.04724947638618406 -0.003877421784976146 -0.07252281243575316 0.32386686149473876 -0.3555051069675466 -0.19540178001500436 0.16533998579762565 0.729341691303189
b2 0.202512681855
w3 -0.31077545119699124 -0.2733397951544186 -0.4036026513888936 -0.22798363835163493 0.13947473360933024 -0.4185954972809355 0.16996714539050436 -0.07736669549428737 0.27677469527430104 -0.2259969227658438 0.10385933370029915 -0.15173362919613684 -0.4669035765315872 0.17894903856204256 -0.02220992663013784 0.13804428297009042 -0.49688971392007325 -0.37091950770349263 -0.23017997918147454 -0.22093321266202107 -0.3566542911344874 -0.3359765125327118 -0.40148146473783874 -0.5059550255017623 -0.3821371454534636 -0.09462793085262007 -0.45375117686548794 0.3533008381748075 -0.6431692662467904 -0.3598445559050988
b3 -0.134216139578
w4 -0.5428358976147315 -0.23837244588743733 -0.019635342926359448 -0.7162376899152131 -0.22620513762766553 -0.3618761355348656 -0.19247266324683787 -0.09136572299674803 0.10213398452415846 -0.19730919251699233 -0.2870109812533745 -0.08416685203351126 -0.8149711411702498 -0.1848604671854011 -0.5736703729461196 -0.4822175289222558 -0.12346182119782853 -0.20040465707059973 0.08742966846890181 -0.20544743103272545 -0.11085053275960254 -0.18845624581167697 -0.19107606309013253 -0.400473803053598 -0.35386979322815043 -0.49254314142506866 -0.3255411415541271 0.08974043752136318 -0.3274495243403294 0.020317865868611104
b4 -0.194013890882
w5 -0.21112126792779523 -0.16395620928362906 -0.17196199549245864 -0.014786205018754328 0.2128660712412204 0.19815393897097283 -0.5416963245741931 -0.7042411532035694 -0.5713921925127173 -0.1109364265942935 -0.4611866592815137 -0.14362611017919466 0.05253764571045046 -0.004386825610551288 -0.4663679867442958 0.0392326142206718 -0.2690657298074764 0.18033675309667416 -0.3722548037629702 0.064829648760986 -0.2826629514045593 0.3024619282646882 -0.09920954762124629 -0.04940431909968845 -0.17720926129963482 -0.2694563215548842 0.14001790193813432 0.21915039019503021 -0.4495162387619048 -0.08365100585122244
b5 -0.691780401616
w6 -0.41209876868484413 -0.7436996349453721 -0.05791864212236267 -0.3097451906536244 -0.5397229865830595 -0.7775535151501712 -0.1571367714251264 -0.3965190085849922 -0.3194592573311835 -0.6972326770843218 -0.035091892367822855 -0.3967057089926228 -0.37440351552885687 -0.31475920193211815 -0.5450590726376273 -0.9078907757143507 0.03915786996441253 0.04206056978190463 -0.7764872082035376 -0.31982341144878246 -0.5091052144688738 -0.710940787526126 -0.20478347656019225 -0.5502520311765042 0.06836865035647245 -0.8283296407512337 -0.09970906336502904 -0.878802261186384 -0.5213707205696905 -0.050223240354073106
b6 0.113535122506
w7 -0.15370000769684558 0.21096600797386195 -0.33485637439092114 0.15935529628843645 -0.19273401319864958 -0.07428889346361327 -0.05190688487198399 -0.5741339642704816 -0.14639269769515742 -0.25169882589339115 -0.10179713044324089 -0.3470876627080021 -0.14086054290011985 -0.07212229296684233 0.1834816170490318 0.38078720594198473 -0.47333034773902993 -0.04983021466528859 -0.492459807649336 -0.3886300240241684 -0.595483198321987 -0.5814906305815524 -0.4502704688884256 -0.06537021889493735 -0.2688030843630335 -0.19071247789413426 -0.0011169449695357348 -0.10462907716488198 -0.14851728936404504 -0.5689856192476657
b7 -0.654312567452
w8 -0.40162321066617784 0.17749831720825737 0.049731968943911874 -0.2337797753175413 0.2587746009596681 -0.0776910759262412 0.14780596673175742 -0.2988593451166782 -0.3509269799775056 -0.09648551141563678 -0.29909638680045647 -0.44969988348478623 -0.32937715425488584 0.252381146567421 -0.25417208116266166 -0.4599698873861697 -0.6111972155392451 -0.28576229913355167 -0.10305428293065691 0.02803201263394703 -0.12149005943930993 0.10648416515014521 -0.20436289533245633 -0.1072701501374355 -0.32467196261712356 -0.42935024849003406 0.33462941559428533 0.07942371394800098 -0.2944680288044947 -0.1624422307672046
b8 -0.310214814672
w9 -0.47760529599691726 0.315250406417199 -0.27914569488605573 -0.20254954783547735 0.3050989635323394 -0.2598690716268317 -0.6145012174644772 -0.20160415202112653 0.10440247635462734 -0.201429168783176 -0.3164567936859277 -0.016463907634779812 -0.5271098138676068 0.2684310865155084 0.21365875918061464 -0.41307114100085307 -0.2585964020258184 0.1618865870862747 -0.31760452867965816 -0.32789911483770834 -0.20896460304206355 0.18292782946073474 -0.42762278181553137 -0.6502782223676258 -0.4660679923431257 -0.3889765086397245 -0.05286886255286097 0.035147072290571166 -0.1792561195026437 -0.4642110054732743
b9 -0.565166887122
w10 0.6366752189452726 -0.3673052436644161 0.5612194807597937 0.5018541728032931 -0.18710417390796533 1.3733970113065521e-05 0.06005158814210146 0.18716069965970078 -0.09366286257041528 0.0035066074058971203 0.21308672534308232 0.3953786273550246 -0.2369853743848289 0.017748936715638947 0.34170127316697246 0.5928911821297004 0.29508947232373917 0.12781531275678443 0.32367518017679603 -0.36494376164321685 0.5746170403868708 -0.1079290649024145 -0.20436390207154878 0.4525918114139059 0.2892264292932974 0.13612455813562163 0.2882155132403077 0.11407488517485069 0.4218383503884809 0.26300537658407125
b10 0.208255046139
w11 0.20506927464902394 -0.05790019481340815 0.5779450465617894 0.4664906080604531 -0.28373145677012623 0.266498560418659 0.3074066391265324 0.17907297489735255 0.47696561263865545 0.31168627829576306 0.29440826053018165 -0.22133301510246559 0.26872328357700426 0.47831406491026685 0.12567033756520826 -0.20204472166271772 -0.1638629953523662 -0.0322808310479113 0.45851280758315105 0.2412968737782357 0.5190134262764221 0.03157402055753175 -0.19825716039535887 0.3755576834329728 -0.40640874164355983 0.6079570060602124 0.5001327203048629 0.39822139746511775 0.1900412179524495 0.1771199498652022
b11 0.546281907632
w12 -0.5604416459745916 -0.7303369783986229 0.04414053550781464 -0.021203372296071953 -0.39975273755358554 0.06733148885648509 -0.16836567692631246 -0.35401969526460175 -0.7376319301093276 -0.02235253218191634 -0.30881561535472885 -0.059039250260989995 -0.4356652868763993 -0.5027128040474557 -0.2201251603775296 -0.07551356918495711 -0.25745917282233133 -0.2304471271653023 0.16549198571071852 0.17522895440298816 -0.40628585356702845 -0.6353936259174348 -0.09538243091798734 0.34612912265046475 -0.3993843201563172 -0.6692074663455293 -0.021993256440956732 -0.12765698928784414 0.1471531065643199 -0.11977660924135294
b12 0.00237351828806
w13 -0.3010261294577476 -0.11117401005431564 0.5459414655843732 0.5494202243464091 -0.563046429366129 0.06297124457797319 0.1265870226050753 -0.09718374564952481 0.006789699719304778 0.21005646141874035 -0.34235685206316396 -0.05361042363325314 -0.0014212818153037533 -0.09403076174440084 0.2247143457402644 0.15877104165048805 -0.057982962108725354 0.6162334903353938 0.45170376690652686 -0.0589849855212981 -0.13556758919202344 0.3870095860816688 0.26974935390672905 -0.26516390344315377 0.310056614331382 -0.27853882000511354 0.19271063004423766 0.16414051680472744 0.4951092637639155 0.5500843184566356
b13 0.300799766798
w14 0.3117140613857162 0.09069214439642032 -0.22920384010446526 0.33087893260548684 -0.2220777828616863 0.4136524602711213 0.2832764855111729 -0.07285063746706018 0.07046814983644262 0.6542332898615459 -0.07798818213757731 0.44849070336826313 0.15863390115218157 0.009950623662823371 0.19500634737334577 0.21806795110565674 -0.016965711006117677 0.11307895159145356 -0.003695314301201775 0.28216570033220095 0.475854680992565 -0.1241877402096224 0.3737229909246303 -0.1312778399186946 0.23086362581587758 0.42033883842304953 0.7828061977766745 0.4683840707505979 0.5196716407883576 0.34660879053523364
b14 -0.0736473179885
w15 -0.02258840382007891 0.23122592514293597 0.056531044551998026 -0.13301503356306174 -0.18258477664836092 0.23787143429650084 0.3022619375180994 0.2983591863031124 -0.06809555568700738 0.12104215435891531 -0.18628415860369218 0.4521221120972641 -0.05970532373742902 0.3182617515511342 0.3665602314119839 0.23397510860318377 0.48238907309084506 0.28644916799077186 0.3799022058421589 0.10635310863889982 -0.40495537676682897 0.7217809347659554 0.5421184650844457 0.39943296157605 0.631426442452193 -0.3130176171855125 -0.36076318886938025 0.24130419633340536 0.40034883704809404 -0.06675597799191257
b15 0.399346802568
w16 -0.11803711752353416 -0.5074230763645889 -0.025867020613830265 -0.16055978970747606 0.08234303852204578 -0.27224010425609435 -0.1775957752738844 -0.7315873937890837 0.0029880585526379376 -0.6567259118153613 0.12538750203425775 -0.4276411178079393 -0.6347787411768189 -0.3998925805165889 -0.042761499438744764 0.12204687196846449 -0.4498498797005692 -0.39908314908548037 -0.3774741898875758 0.18321036772417298 -0.23417222254610986 -0.6262341046197527 0.04926179820432413 -0.4398085751080828 -0.2063153321465867 -0.018053772004096497 -0.20064220707993874 -0.6621561401744954 -0.681614448237178 0.07661520663755343
b16 0.20990186712
w17 -0.5147058554589556 -0.08175655078209582 0.020365897383260043 -0.09252148913776141 0.2474342660156188 -0.45439837178592474 -0.046695653794194436 -0.5120859269075241 -0.20914681951020347 -0.7187962687642717 -0.2785882390771843 -0.21809116276733745 -0.8260022449075486 0.07727050504186979 -0.561392204703537 -0.062231605281032734 0.057049025971617914 -0.3052447874747715 0.2202206707181716 -0.3871812564919142 -0.28708437464882924 0.12044257330829967 -0.09266157449050504 -0.22491752080745717 0.010571594997551217 0.33995576316813525 0.16208175742796316 -0.2680118114304119 0.050486184700464815 -0.05425718293252073
b17 0.1541398266
w18 -0.09606603930600674 0.3496015872070336 0.11824940009097973 0.5345032915418475 -0.6309076827731792 -0.1654242163483685 0.3638255895625452 0.6205826746477375 0.17195087283764798 0.24753789246184044 0.3734281563882652 -0.04540707436126374 0.2780752760548181 0.7440360601732311 -0.19055261015266084 -0.17500017085366432 0.34537360884599827 0.10551766417756682 0.4531942415474418 0.4012763016287687 -0.02035853864039059 -0.06036610926686236 0.017121295484690068 0.2769041273907746 -0.30589470505484495 -0.00636246667680052 0.07997864555900756 -0.01755634736012169 -0.09146858725589911 0.4966946379472048
b18 -0.076507145569
w19 -0.3966651519157311 0.05159534072806334 0.1786684454273879 -0.8441059254074392 -0.10107097420702842 0.08546004069316046 -0.3550620392096723 -0.5333235110808242 -0.2752546962631403 -0.066400570204785 0.10550531424439429 -0.23013228345434827 0.3036468697045548 -0.5213884324984123 -0.260770516467976 -0.18620058990267085 -0.15603946377597666 -0.5820546856960196 0.10945998680738339 -0.17906233113593292 -0.10813160281356621 -0.06509292817759184 -0.1529321068248786 0.25075316462696706 0.1441907459605517 -0.42793487430796273 0.03084326356997626 -0.001991478026553514 -0.4795493073813357 -0.12174536139123
b19 -0.031591006137
w20 0.5672542250807455 0.1274549357435878 -0.36015081849444464 -0.08067167074320614 0.08509798553951495 0.00016811450446824598 0.03777424456680006 0.132555657214379 -0.09294841804897641 0.5440523218901998 0.08165231198117162 0.47990251606945633 0.10901296036973795 0.4707279869296919 -0.07139865377306123 -0.5030693494862899 0.3597843448509447 0.3057819583017998 0.03229325122390492 0.21275384509939546 0.3954876353303708 0.1641344028769754 0.36980019450085877 0.2766447151832672 0.4072923229239971 -0.17348447523274246 -0.03844141160437416 0.2916264891620168 0.16220424137880957 0.03629658849563707
b20 0.176498702776
w21 0.4779505873463952 0.22498048140185276 0.3728312896065749 -0.15507434896992395 -0.17595484754962595 -0.15554134340596237 -0.13563895179052465 0.33227942003674926 0.425211074143145 0.22892552779635622 0.2328939497669502 0.20011721413670316 0.3447745364088755 0.13345028866033778 -0.07162834829900276 0.40975403916254843 0.10682300768367203 -0.09741635065154783 0.5988581775996208 -0.06783780481348282 0.14099217307069886 0.04128404625860584 0.7680730322783554 -0.20692977109530095 0.3505733237685041 0.06489411754001492 -0.27192344907508303 0.07995960544137853 -0.16929053627823765 0.15847700500941972
b21 0.113676947196
w22 -0.3847913531890772 -0.058888471768866114 0.014964250183160773 -0.6173110999122124 -0.22622597671088074 -0.04582799052273706 -0.1488343584855848 -0.6447765366787929 -0.1341927803054047 -0.26190393649661203 0.09799739414361985 -0.1414845952518148 -0.17203397761762831 0.10341769621251544 -0.01807902202610597 -0.2657659564457475 -0.04372980571014758 -0.47964039357976 -0.4187765710688782 -0.44663265403190267 -0.21668683681656226 0.18425694635152465 0.032597938213343405 -0.001695184618880605 -0.10012636775587518 -0.4749003370445315 0.11039038920599752 -0.13660758818404134 0.01488613710115618 -0.1292562023308838
b22 -0.488945231166
w23 0.033288512660390006 -0.2573376186917364 0.5542594033278081 0.7767072144171924 -0.16042628648549767 0.026885138816796106 0.44023499695531354 0.41927474413988813 0.0990261957964525 0.3333534299717446 -0.058359617280119194 0.6107064615437102 0.41926210830408156 0.26745095967803617 -0.08588860963759257 0.022708959689687034 0.07301344901763307 0.5088418293873309 0.10790000585693658 -0.1873819306418108 0.2836481148758096 0.1661466934994788 -0.26418666351365594 -0.36419783441395276 0.052674164549576734 -0.3571364673892163 0.37483538265013644 0.2779165389038164 0.17222046634741553 0.3163353037181392
b23 0.225494312829
w24 -0.33415207343787656 -0.5412318604510582 -0.4914736798449089 -0.5409493831898475 -0.09787223252733801 -0.09946668509774673 -0.06668246494311789 -0.48695572811188964 -0.5299436958938875 -0.2359661716437003 -0.45066467321116155 -0.19732627210084905 -0.21905273945375175 -0.6056841892667513 0.24374100617214509 -0.1496517950412117 -0.060374149659991536 -0.05257652637308791 -0.6655170332323305 -0.48440863409932694 -0.21287971892546692 -0.7687794570330149 -0.15482631257516904 -0.6818843058718612 -0.3990397673583248 -0.49781380734885267 0.11981719147353229 -0.8375119209046795 -0.10494905258793724 -0.6934527836576307
b24 -0.858661136917
w25 0.5242519500740448 -0.13445493304389983 -0.010390306178093708 -0.015525022708391038 -0.3911234414689813 -0.17139705365378904 0.1430521560671913 -0.0760239962330799 0.40152998978470833 0.48533923495122006 0.2070537442311589 0.48136861995347646 0.26608448508019966 0.5503022880500118 0.35987537658278956 0.5276417313220135 0.014937647868603911 -0.14483361334117875 -0.22052444483522235 0.06987479971468946 0.2118040149340503 0.1935445189139468 0.16284485745678273 0.4014108787672368 0.22773650843818213 0.11217643815231065 0.2834270792637471 0.13909522515552875 -0.09693322777770684 -0.062079384123568046
b25 0.168832080477
w26 0.20704154046534337 0.36005423651998647 -0.13079026479322092 0.12944418362747495 0.22188878268120632 0.38091344675868105 0.07152029220513836 0.040413445293711756 0.5358589436978631 0.05765376637138915 0.4564296552064663 0.1281063265620666 0.8051740234602986 0.29489290046963457 0.2039111575539358 0.21029446570746424 0.2976295524779971 -0.03674069318072005 0.40060190209865115 0.41612069730038326 -0.01815870815339938 -0.1642468557001408 0.2711105866082384 0.38549176126235046 0.07711366430590282 -0.35183154096953534 -0.3899201225673026 0.04789662965684338 -0.0354476046537123 0.19663293893700592
b26 -0.225226986254
w27 0.06417876360512619 -0.09111203126885344 -0.25087428958876523 0.23820769257611032 -0.44136773726834405 0.11538767218365828 0.5106517359132468 -0.39977439926996094 0.5373426582959654 0.026346752149074067 0.4205504687539574 0.532035091557477 0.5232535709619573 -0.06773538065854467 -0.10051818109974751 -0.48397297421207364 0.08841351792914852 0.2508646792863565 -0.31808864209322724 0.3347255625391038 0.2915733334750438 0.4207257709959006 0.4351770452411559 0.041671820580342384 0.26480994243351313 0.615388846843646 -0.07455068669260521 -0.08462452417445736 0.2927064719605565 0.32574699074046753
b27 -0.251634098685
w28 0.4032828294498286 0.1594170595003064 0.31554756819900753 0.5468674362716157 0.09726644006163895 0.2650121648871796 0.010936885165420832 0.1564756652725344 -0.40468899454360563 0.4904518842422721 0.2531136484439638 0.07908319748788754 0.48205828152845587 -0.14523756765697726 0.3844672752551615 0.6507616895342138 -0.20033741343266728 -0.006326083251657416 0.10354737253003857 0.08647698277923005 0.1751784281989982 0.6429482062396112 0.1721289048472004 -0.03370892743302569 0.2337317883558511 0.038588072051356226 -0.029630783914060058 0.314817010093935 0.15743513671937115 0.13764122950306926
b28 -0.453199005606
w29 0.168274608642832 -0.41637615319896826 -0.04598555965291396 0.2791590631714024 0.35579094091274027 0.6418631742378942 0.6612221007892399 -0.09588391978140198 0.22273490549875216 -0.10588987061454619 -0.08446167903534386 0.4477302278303588 0.09115347093498692 0.5784506674716008 0.05426135577965186 0.650192574661566 0.19474275881264333 0.4230004070660779 0.2967470562826947 0.21787148178766133 -0.26174683668691195 0.5162579749900519 0.5974204426378258 0.2968458390425587 0.025606956277305852 -0.03208501983106463 0.2214875836610866 0.756363934940012 0.12949166892638916 0.22523429333754855
b29 -0.0219445921192
LAYER 2 linear
w0 -0.2970962660276736 0.24963143980319624 -0.5094604921933329 0.07333476783108946 0.027222916752886427 0.3788850035539772 0.021704335415670042 0.11708419156605475 0.30893651722952786 0.03494547507916752 -0.3245368172539948 -0.41574539346802286 0.15548432625348496 -0.8040848251679176 -0.318938126445305 -0.4027874860827931 0.03869471993304929 0.078444471876736 -0.49005931645769646 0.36697085201500645 -0.8965263913955533 -0.6128217736323844 0.20097461319355875 -0.5807071570801926 0.02525316385225664 -0.6443463092973751 -0.6606044026482261 -0.7369283208534756 -0.23655286842968906 -0.33067394434652375
b0 -0.674871428512

"""

amorphous_bise_json_sample = """
[
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/0/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -65891.43648651696,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.12880000000000003, -0.23080000000000034, -0.2958999999999996, 0.2644000000000002, -0.24130000000000074, 0.1999000000000004, 0.03300000000000036, 0.3171999999999997, 0.24509999999999987, -0.19549999999999912, -0.49380000000000024, -0.2746999999999993, 0.18379999999999974, 0.15810000000000013, 0.013700000000000045, 0.20980000000000043, -0.05620000000000047, -0.1556999999999995, -0.2718000000000007, 0.19610000000000039, -0.13959999999999972, -0.05829999999999913, 0.08230000000000004, 0.031200000000000117, 0.16990000000000016, -0.03769999999999918, 0.22970000000000024, 0.12230000000000008, 0.20370000000000044, 0.3996000000000004, -0.2766000000000002, -0.007999999999999119, 0.10069999999999979, 0.20099999999999962, -0.15770000000000017, -0.08549999999999969, -0.07049999999999912, -0.13119999999999976, -0.006000000000000227, 0.04870000000000019, 0.1596000000000002, -0.04860000000000042, 0.09049999999999958, 0.11340000000000039, 0.10449999999999982, -0.042299999999999116, 0.14139999999999997, -0.12379999999999924, -0.31290000000000084, 0.05339999999999989, 0.005000000000000782, 0.15920000000000023, -0.3246000000000002, 0.12359999999999971, -0.40859999999999985, 0.09989999999999988, -0.3071999999999999, -0.22409999999999997, 0.13889999999999958, -0.15000000000000036, -0.07429999999999914, 0.17049999999999965, 0.06639999999999979, 0.2179000000000002, 0.019999999999999574 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -0.6067803962206323, -14.002228973803234, -4.807963309036365 ],
          [ 24.55917942669271, 13.97651794006507, -7.795585429410836 ],
          [ 17.493787355445686, 16.542479107133676, 30.051056233164196 ],
          [ -31.10006640968122, -8.46921451335069, -18.825618903082496 ],
          [ -39.29160175865976, 6.2374967848781955, -19.13929351468808 ],
          [ 21.63326378728983, -11.868213173535759, -26.708621847203084 ],
          [ -3.815517406743298, -17.447507494716994, -4.3965867692257685 ],
          [ -2.725369576245213, -9.898747989192518, 19.951762180814008 ],
          [ -12.665255219418789, 1.712354846961615, 7.296791374890486 ],
          [ -24.857427418055394, 12.032763789459997, -3.7846641662575027 ],
          [ 32.92554980509075, -3.6458245840714265, 20.728235399706517 ],
          [ 36.36054391250924, -2.375699517406204, 32.030805831002695 ],
          [ 12.387576055046639, -12.048190409702892, -0.6479180502016921 ],
          [ -5.286188536566186, -5.779840384338904, 14.027940007541394 ],
          [ -42.11981546985763, -12.017337169217097, -11.544254148434911 ],
          [ 7.173378412947305, 12.238452059365295, 8.818884572189699 ],
          [ -5.764413764096007, -6.098657202692118, 2.401410551144367 ],
          [ 40.71599302775395, -32.714719328437816, -28.122728702802018 ],
          [ -21.76696116272828, -3.5121272086329816, -7.379066682852604 ],
          [ 6.792855113622502, -7.32764461537628, -5.440454738995161 ],
          [ 19.54038564100341, -3.0904662553271187, 10.932331545466646 ],
          [ 3.728099892033545, -1.5992262985137005, 0.7147667379209143 ],
          [ -3.640682377323794, -0.6170648097158973, -2.370557310658572 ],
          [ 25.46420781427603, -3.6098291368379987, 0.8587485268546237 ],
          [ -1.7792035346808373, -0.7353355649114441, -0.3291012318484785 ],
          [ 2.329419656677512, -13.626847881226062, -16.629896621843432 ],
          [ -3.3424343859611105, 1.2032763789459997, 1.2444140329270597 ],
          [ 6.726006425903281, -2.7202273694975805, -3.193310390279768 ],
          [ 11.06602892090509, 8.350943758155141, -2.6585208885259908 ],
          [ -0.5039362612679827, 0.8896017673404186, 1.2855516869081194 ],
          [ -1.5169509905515806, -0.41651874655823057, 0.030853240485794863 ],
          [ -6.273492232111621, -13.328599889863378, -5.10621130039905 ],
          [ 3.9235037484435797, 5.152491161127742, -7.466484197562357 ],
          [ -0.005142206747632477, -1.9129009101192813, -6.911125868818049 ],
          [ 1.8666210493905893, 0.5810693624824698, 1.8563366358953244 ],
          [ 2.555676753573341, 9.430807175157963, 23.952399030472076 ],
          [ -19.632945362460795, -6.360909746821374, 14.583298336285706 ],
          [ 7.877860737372956, -6.828850560855929, 0.7610465986496067 ],
          [ -14.429032133856731, 20.87735939538786, -12.176745578393707 ],
          [ -2.0311716653148286, 18.25483395409529, -9.48737144938192 ],
          [ -11.477405460715687, -4.777110068550571, -14.259339311184858 ],
          [ -22.599998655844736, 7.08081869148992, 3.676677824557221 ],
          [ 12.171603371646073, -1.05929459001229, -8.700613816994151 ],
          [ -5.35817943103304, 19.514674607265253, 4.910807443989016 ],
          [ 1.6763593997281871, -6.5048915357550845, 14.449600960847263 ],
          [ -21.98807605287647, -10.325551149246014, -10.094151845602552 ],
          [ 14.799271019686268, 8.068122387035357, 2.853924744936025 ],
          [ -0.23139930364346142, -0.29824799136268365, 0.0874175147097521 ],
          [ 14.706711298228884, -0.025711033738162387, -3.671535617809589 ],
          [ -5.959817620506041, 12.094470270431586, 12.027621582712365 ],
          [ -0.3548122655866409, 0.550216121996675, -0.04113765398105981 ],
          [ -0.09770192820501707, -9.975881090407004, -4.221751739806264 ],
          [ 25.07340010145596, -4.874811996755588, -1.8820476696334865 ],
          [ 4.725688001074246, -1.270125066665222, 0.19026164966240167 ],
          [ -8.726324850732311, 12.032763789459997, 16.352217457471276 ],
          [ -2.2162911082295977, -0.23139930364346142, -1.712354846961615 ],
          [ -3.722957685285914, 1.2392718261794269, 0.8484641133593587 ],
          [ -2.1494424205103755, 13.498292712535253, 16.341933043976013 ],
          [ -3.3167233522229473, 1.9026164966240164, -0.11312854844791449 ],
          [ -5.93924879351551, 1.378111408365504, 2.817929297702597 ],
          [ 0.7147667379209143, 3.429851900670862, -5.856973485553391 ],
          [ -9.63135323831563, 5.126780127389579, 2.956768879888674 ],
          [ 14.084504281765353, -5.970102034001305, -13.025209691753066 ],
          [ -8.073264593782987, 9.518224689867715, 4.684550347093186 ],
          [ -18.095425544918683, 24.456335291740064, -5.193628815108802 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.3700171463650666, 0.8328277796857171, 0.08757056301078632 ],
        [ 0.8379814340821757, 0.0960353018178723, 0.9765343846708282 ],
        [ 0.4699315428899503, 0.969642064611049, 0.6003938102325505 ],
        [ 0.7510412239612786, 0.03851386887675779, 0.280707917690959 ],
        [ 0.120362767194702, 0.2961273191513301, 0.1186033206668789 ],
        [ 0.3178641034202628, 0.4141072138831536, 0.06408818612369838 ],
        [ 0.6795550500749225, 0.5873849890543937, 0.2752079155528034 ],
        [ 0.526919600308851, 0.09974814960886905, 0.5716885094006648 ],
        [ 0.9299506134125196, 0.3192425674322187, 0.6659297299165443 ],
        [ 0.1333577344631908, 0.7150279857795763, 0.290821271748525 ],
        [ 0.1868130449167771, 0.5808459436911458, 0.001011335405756589 ],
        [ 0.8284499442306613, 0.004807306654760774, 0.678384394707985 ],
        [ 0.2701512385240205, 0.735427867765557, 0.9617868978293502 ],
        [ 0.2487746559064531, 0.5761702491782301, 0.5919152175157967 ],
        [ 0.5488434123583004, 0.1752519572989158, 0.001364610102288001 ],
        [ 0.4565833009249302, 0.8364090153348691, 0.7006199197249618 ],
        [ 0.2956147244936178, 0.829759138694278, 0.3992142609901627 ],
        [ 0.881164070517015, 0.58137931921336, 0.8816974460392293 ],
        [ 0.6992760904871761, 0.7389606147308712, 0.514354104240067 ],
        [ 0.9561206487751798, 0.6440336256864304, 0.4238672932441881 ],
        [ 0.6130493567141757, 0.06570216660000855, 0.313195335862181 ],
        [ 0.6600556722173554, 0.2892834877753882, 0.6189649761423685 ],
        [ 0.4283421060669192, 0.1357960225647409, 0.298586388117382 ],
        [ 0.5402401344545352, 0.6275059114526278, 0.5635631913804423 ],
        [ 0.6456129713885709, 0.6381595679872418, 0.4181040668223423 ],
        [ 0.9080822170017416, 0.3720398171765799, 0.4457703244291355 ],
        [ 0.870413436614726, 0.8287270224240195, 0.6966230667857731 ],
        [ 0.06632559253506398, 0.9075349875698596, 0.7209920938916068 ],
        [ 0.9989223026941524, 0.1493728540392815, 0.8682037380226961 ],
        [ 0.1585995578781018, 0.6205651027090107, 0.1425705843923433 ],
        [ 0.846002847779889, 0.8057364593301417, 0.5537476963807364 ],
        [ 0.3966997763854391, 0.0707449897191236, 0.6990336470679875 ],
        [ 0.4534246095206495, 0.7220865527553708, 0.8663888758562015 ],
        [ 0.9755299762199056, 0.8558391236440968, 0.0118173849467174 ],
        [ 0.3586846482567257, 0.7201123706276951, 0.1810151837207616 ],
        [ 0.5197017133718759, 0.05472987014303297, 0.1977922683285866 ],
        [ 0.01631297863395046, 0.7952351958018749, 0.2226738900921323 ],
        [ 0.3495341409210788, 0.9288076658649178, 0.6961451069022309 ],
        [ 0.03219648606819608, 0.1647645476803166, 0.6215140955212619 ],
        [ 0.5867407822548366, 0.2801745421687449, 0.8740916496315527 ],
        [ 0.6264668682275355, 0.519798690739551, 0.6189095605036968 ],
        [ 0.6710972382226704, 0.2938899127399645, 0.4276286297190224 ],
        [ 0.2097481923719831, 0.1861064955237143, 0.9446080498411563 ],
        [ 0.7525720809795813, 0.4695228525547474, 0.2168621749864489 ],
        [ 0.254385489321952, 0.05808251628266439, 0.4344447532756284 ],
        [ 0.3138880313455759, 0.6804971159323396, 0.3758634962449198 ],
        [ 0.179588231024968, 0.02481927917004013, 0.06712219234096814 ],
        [ 0.6964152581407548, 0.4347703201528241, 0.5192860960818388 ],
        [ 0.897283094415615, 0.9901527778743725, 0.2165296811544193 ],
        [ 0.677026711560531, 0.2688281901507362, 0.03214799738435843 ],
        [ 0.8057710941043114, 0.3322790964297111, 0.3426903095451369 ],
        [ 0.5892829746788958, 0.8309852096998867, 0.6286973476840672 ],
        [ 0.8718057545363498, 0.2731367560574526, 0.7995368347537574 ],
        [ 0.1789786589995805, 0.9683675049216021, 0.6339133446740309 ],
        [ 0.2370542483274109, 0.9465268163301599, 0.7882874601034235 ],
        [ 0.2538936755287415, 0.2132393776082934, 0.5181431485342372 ],
        [ 0.02593451889830596, 0.2074138085929421, 0.4246015504565867 ],
        [ 0.3733559385950301, 0.460039851387071, 0.2809365072004794 ],
        [ 0.5867615631193384, 0.8637912677934704, 0.117501934848281 ],
        [ 0.5271758976377071, 0.1386360740466601, 0.7209574591174371 ],
        [ 0.397399398823668, 0.5671582809392619, 0.179996921360171 ],
        [ 0.1448772603520484, 0.4880732376000636, 0.355636788129788 ],
        [ 0.9651741787431515, 0.7441973925853367, 0.7716212067729419 ],
        [ 0.9037528702305236, 0.08349058661359018, 0.5516280482015478 ],
        [ 0.5671790618037639, 0.91567415949975, 0.2848779445009965 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  },
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/1/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -66023.54536400155,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.09940000000000015, -0.23049999999999926, -0.28669999999999973, 0.2671999999999999, -0.23579999999999934, 0.20669999999999966, 0.037799999999999834, 0.27369999999999983, 0.21670000000000034, -0.23109999999999964, -0.4206000000000003, -0.27500000000000036, 0.15629999999999988, 0.16849999999999987, 0.02660000000000018, 0.12370000000000037, -0.0693999999999999, -0.18340000000000067, -0.2331000000000003, 0.2526999999999999, -0.07840000000000025, -0.041100000000000136, 0.08560000000000034, 0.07760000000000034, 0.12439999999999962, -0.12950000000000017, 0.1814, 0.13999999999999968, 0.20420000000000016, 0.3449, -0.26500000000000057, -0.037200000000000344, 0.07749999999999968, 0.21729999999999983, -0.10890000000000022, -0.043999999999999595, -0.12650000000000006, -0.1504999999999992, -0.019099999999999895, 0.1075999999999997, 0.13510000000000044, -0.06670000000000087, 0.09220000000000006, 0.1615000000000002, 0.1253000000000002, -0.09970000000000034, 0.1477000000000004, -0.1521000000000008, -0.25709999999999944, 0.07819999999999983, -0.0686, 0.18069999999999986, -0.2665000000000006, 0.13600000000000012, -0.34500000000000064, 0.09830000000000005, -0.2568999999999999, -0.22969999999999935, 0.0895999999999999, -0.16080000000000005, -0.10720000000000063, 0.18810000000000038, 0.09930000000000039, 0.2131999999999996, 0.040899999999999714 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -2.6996585425070503, -8.649191749517826, -3.7126732717906488 ],
          [ 18.450237810505328, 10.891193891485585, -6.299203265849784 ],
          [ 11.58024959566834, 10.62894134735633, 18.97474289876384 ],
          [ -16.275084356256787, -7.1013875184804505, -10.006734330892801 ],
          [ -18.33196705530978, -0.14398178893370933, -19.339839577845748 ],
          [ 15.663161753288524, -8.356085964902777, -19.838633632366093 ],
          [ -5.101069093651417, -14.866119707405492, -3.8772238877148877 ],
          [ -2.7922182639644353, -7.214516066928366, 14.737564538714679 ],
          [ -11.45683663372516, 1.336973754384444, 6.664299944931689 ],
          [ -17.668622384865188, 9.281683179476621, -3.1418883228034438 ],
          [ 20.563684783782275, -2.9413422596457766, 13.729692016178715 ],
          [ 20.357996513876977, -3.6818200313048535, 24.37920219052557 ],
          [ 10.726643275561347, -10.243275841283893, -0.7970420458830338 ],
          [ -3.9749258159199043, -4.951945097970075, 12.973787624276742 ],
          [ -25.489918848014188, -5.754129350600742, -6.150079270168442 ],
          [ 5.805551418077066, 9.96559667691174, 7.106529725228083 ],
          [ -5.327326190547246, -5.923822173272613, 2.632809854787828 ],
          [ 24.399771017516102, -20.070032936009554, -17.20068157083064 ],
          [ -18.614788426429566, -2.4785436523588538, -7.0191122105183315 ],
          [ 5.394174878266468, -5.558725494190707, -4.679408140345554 ],
          [ 16.994993300925337, -2.072309319295888, 8.114402247764048 ],
          [ 3.5532648626140415, -1.4963821635610508, 0.786757632387769 ],
          [ -3.9646414024246397, -0.7610465986496067, -2.9773377068792044 ],
          [ 19.838633632366093, -2.3499884836680422, 1.4758133365705208 ],
          [ -1.8666210493905893, -0.8124686661259314, -0.2571103373816238 ],
          [ 1.6815016064758201, -10.06844081186439, -12.30530074708452 ],
          [ -3.193310390279768, 1.1107166574886151, 1.228987412684162 ],
          [ 6.751717459641442, -2.771649436973905, -3.8000907865004 ],
          [ 9.785619440744602, 7.224800480423632, -2.0208872518195635 ],
          [ -0.5193628815108802, 0.9153128010785809, 1.2906938936557517 ],
          [ -1.6969282267187173, -0.44222978029639304, 0.05142206747632477 ],
          [ -5.02393599243693, -11.055744507409827, -3.5326960356235113 ],
          [ 3.5069850018853486, 4.262889393787324, -6.12436823643028 ],
          [ -0.2725369576245213, -1.7432080874474098, -5.8775423125439215 ],
          [ 1.7534925009426743, 0.529647295006145, 1.6969282267187173 ],
          [ 2.329419656677512, 7.8572919103824255, 19.339839577845748 ],
          [ -14.932968395124714, -7.55904391901974, 12.999498658014902 ],
          [ 7.440773163824194, -6.216927957887664, 0.5039362612679827 ],
          [ -12.027621582712365, 17.2109659843259, -8.669760576508356 ],
          [ -2.853924744936025, 12.361865021308475, -8.530920994322278 ],
          [ -9.626211031567998, -3.980068022667537, -11.976199515236038 ],
          [ -17.75089769282731, 5.8775423125439215, 1.4809555433181532 ],
          [ 10.330693355993647, -0.776473218892504, -7.55904391901974 ],
          [ -5.363321637780674, 16.37792849120944, 3.7589531325193404 ],
          [ 2.051740492305358, -5.594720941424135, 12.45442474276586 ],
          [ -18.157132025890277, -8.71604043723705, -7.913856184606383 ],
          [ 12.197314405384237, 6.751717459641442, 2.154584627258008 ],
          [ -0.31367461160558113, -0.2931057846150512, 0.09770192820501707 ],
          [ 12.757814940876175, -0.11312854844791449, -3.172741563289238 ],
          [ -4.6999769673360845, 9.847325921716195, 10.58780369337527 ],
          [ -0.3496700588390084, 0.5142206747632476, -0.06684868771922219 ],
          [ 0.14398178893370933, -9.045141669085526, -3.7898063730051357 ],
          [ 17.936017135742077, -2.7202273694975805, -2.046598285557726 ],
          [ 4.854243169765058, -0.8896017673404186, -0.08227530796211963 ],
          [ -7.276222547899954, 11.827075519554697, 16.78930503102004 ],
          [ -2.144300213762743, -0.19540385641003413, -1.5940840917660677 ],
          [ -3.4041408669326993, 1.1724231384602049, 0.9461660415643757 ],
          [ -1.4860977500657857, 9.919316816183047, 11.971057308488406 ],
          [ -3.244732457756093, 1.9026164966240164, 0.03599544723342733 ],
          [ -4.442866629954461, 1.0490101765170254, 2.663663095273623 ],
          [ 0.5605005354919399, 3.157314943046341, -5.5381566672001785 ],
          [ -8.674902783255988, 4.309169254516016, 3.460705141156657 ],
          [ 12.346438401065578, -4.9673717182129735, -10.742069895804244 ],
          [ -6.705437598912749, 7.965278252082708, 3.897792714705418 ],
          [ -12.027621582712365, 18.34739367555268, -8.30466389742645 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.3758773501545877, 0.847298188333837, 0.07595405975425344 ],
        [ 0.8383208548690388, 0.0940957544643665, 0.9787717910821939 ],
        [ 0.4753276407055969, 0.9590022619861025, 0.573558787205831 ],
        [ 0.7582591108982537, 0.0411738195329943, 0.2835064074438746 ],
        [ 0.1256203259136695, 0.2968130876798911, 0.1152576014820814 ],
        [ 0.3145253111902993, 0.4106160286468431, 0.06412282089786814 ],
        [ 0.6765002629931509, 0.5934807093082692, 0.259968614918115 ],
        [ 0.534005875103981, 0.1169339245518971, 0.555846563695423 ],
        [ 0.9367944447884614, 0.3258508823438062, 0.659155168088942 ],
        [ 0.1365025719578037, 0.7095833992800923, 0.3065939479054274 ],
        [ 0.1867853370974412, 0.5722980814260524, -0.01299496726848877 ],
        [ 0.8202415027524317, 0.00950378203217836, 0.6863088310380231 ],
        [ 0.2712110626136147, 0.7377068359059262, 0.9566886590715638 ],
        [ 0.2503955633375972, 0.5772023654484885, 0.5871910343190433 ],
        [ 0.5456293053153478, 0.1713867165015721, 0.00347040437180857 ],
        [ 0.4670291488145258, 0.8139864625373753, 0.7184291206030455 ],
        [ 0.2953099384809241, 0.8475129239336897, 0.4021512898397571 ],
        [ 0.88347074647672, 0.5829309570961645, 0.8809701157816642 ],
        [ 0.6992622365775079, 0.7424310191026794, 0.5149498223557866 ],
        [ 0.9568618329424123, 0.6459939539044384, 0.4224126327290588 ],
        [ 0.6070506138279756, 0.07442320273595066, 0.3262387918145074 ],
        [ 0.6664561784839242, 0.2868105648996683, 0.6280392869748419 ],
        [ 0.4224819022773981, 0.1405479135808301, 0.3019598151215154 ],
        [ 0.5276122957922458, 0.6316759382626653, 0.5655304465532839 ],
        [ 0.6341488611383852, 0.6252685050412623, 0.4111147693948875 ],
        [ 0.9239449435714856, 0.383746370845954, 0.4567772556602809 ],
        [ 0.8592194776030638, 0.8278057374311037, 0.7098050618347788 ],
        [ 0.05826261710834706, 0.9055330976228486, 0.7245594756310907 ],
        [ 0.9986590784104619, 0.1491373375749272, 0.8697484489506666 ],
        [ 0.1536052234428244, 0.6170669905178664, 0.1489295289299087 ],
        [ 0.8672547452104452, 0.8103982999333895, 0.5360562537348299 ],
        [ 0.3732104725435171, 0.08948240254495632, 0.7040695432322686 ],
        [ 0.4499542051488408, 0.7206665270144113, 0.8697068872216631 ],
        [ 0.9759733013292781, 0.8571621720173811, 0.01440806605461442 ],
        [ 0.3530183992025552, 0.7295538100663681, 0.1933659441896931 ],
        [ 0.5111677050164504, 0.0565655131740295, 0.1837166961060018 ],
        [ 0.001039043225092386, 0.8001879685081483, 0.2116461779964851 ],
        [ 0.3335398022094899, 0.9071470780991587, 0.6863157579928569 ],
        [ 0.03719082050347348, 0.1666071176661471, 0.6216387807082728 ],
        [ 0.5846557688498178, 0.2859862572744283, 0.8711476938271245 ],
        [ 0.6212647251472396, 0.5206229983647911, 0.6375015072780166 ],
        [ 0.6537452163636275, 0.2820448199739113, 0.4230845473479519 ],
        [ 0.2066726244257096, 0.1836543535124963, 0.9526225365840353 ],
        [ 0.759859237464896, 0.4636141600813887, 0.2085359752760419 ],
        [ 0.2548980839796642, 0.05955795766229557, 0.4344793880497983 ],
        [ 0.3205586888506691, 0.6597578131594953, 0.3905417135380583 ],
        [ 0.1797475509861488, 0.02792255493564939, 0.06284133425358751 ],
        [ 0.7111973797564024, 0.4452369489069214, 0.5121513326028712 ],
        [ 0.9075696223440297, 0.9917806122603504, 0.2082104083988463 ],
        [ 0.6843207950006795, 0.267893051248153, 0.03599245731720026 ],
        [ 0.8096778966306588, 0.3218678833142854, 0.3211959686953922 ],
        [ 0.6056028802676802, 0.838556371333393, 0.6329782057714478 ],
        [ 0.8630085218972342, 0.2727696274512533, 0.8082301630703635 ],
        [ 0.1711581269920517, 0.9785293476630058, 0.6222137179594907 ],
        [ 0.217949706895379, 0.9549777012275781, 0.8165217280066007 ],
        [ 0.252605261929627, 0.2134956749371496, 0.5172218635413219 ],
        [ 0.03212028956502264, 0.2071436573544181, 0.4214982746909774 ],
        [ 0.3652998901231472, 0.4462759921320137, 0.2951298376552414 ],
        [ 0.586546827519486, 0.8625513428781935, 0.1175573504869526 ],
        [ 0.5489680975453113, 0.1403539588454795, 0.7374228307577342 ],
        [ 0.4120014196136331, 0.5620046265428038, 0.1595970393741905 ],
        [ 0.1470246163505727, 0.4862930102077386, 0.3553527829815961 ],
        [ 0.972475189138134, 0.7313548183231947, 0.7797395978383302 ],
        [ 0.9031571521148039, 0.08250695902716942, 0.545476912309001 ],
        [ 0.5660984568496679, 0.9022358671218886, 0.2856606903972327 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  },
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/2/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -66057.7818206241,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.0940000000000003, -0.23820000000000086, -0.27560000000000073, 0.25180000000000025, -0.24939999999999962, 0.23080000000000034, 0.0602999999999998, 0.24939999999999962, 0.20579999999999998, -0.2051999999999996, -0.39649999999999963, -0.2988999999999997, 0.16000000000000014, 0.22109999999999985, 0.030400000000000205, 0.1357999999999997, -0.033500000000000085, -0.2120999999999995, -0.27059999999999995, 0.28640000000000043, -0.04900000000000038, -0.04870000000000019, 0.08059999999999956, 0.10949999999999971, 0.14569999999999972, -0.1374999999999993, 0.16110000000000024, 0.14939999999999998, 0.2168000000000001, 0.3059000000000003, -0.2505000000000006, -0.11550000000000082, 0.06660000000000021, 0.24479999999999968, -0.13320000000000043, -0.019099999999999895, -0.19340000000000046, -0.20669999999999966, -0.02660000000000018, 0.15909999999999958, 0.13339999999999996, -0.11389999999999922, 0.11040000000000028, 0.17499999999999982, 0.1440999999999999, -0.15380000000000038, 0.14749999999999996, -0.15499999999999936, -0.21330000000000027, 0.12520000000000042, -0.09980000000000011, 0.19390000000000018, -0.23789999999999978, 0.15749999999999975, -0.3178000000000001, 0.10459999999999958, -0.2697000000000003, -0.2505000000000006, 0.05339999999999989, -0.21729999999999983, -0.1515000000000004, 0.22970000000000024, 0.11789999999999967, 0.20579999999999998, 0.07699999999999996 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -4.504573110926049, -3.327007765718212, -2.437405998377794 ],
          [ 12.665255219418789, 7.790443222663202, -5.018793785689298 ],
          [ 7.564186125767373, 6.664299944931689, 11.51854311469675 ],
          [ -6.612877877455365, -6.4123318142976995, -4.247462773544426 ],
          [ -9.646779858558526, -1.424391269094196, -16.043685052613327 ],
          [ 10.75235430929951, -5.56386770093834, -13.986802353560336 ],
          [ -6.052377341963425, -12.017337169217097, -3.373287626446905 ],
          [ -2.895062398917085, -4.627986072869229, 9.657064272053791 ],
          [ -9.749623993511175, 0.8278952863688287, 5.8775423125439215 ],
          [ -11.590534009163603, 6.869988214836989, -2.514539099592281 ],
          [ 12.855516869081193, -1.357542581374974, 9.6107844113251 ],
          [ 11.035175680419297, -2.931057846150512, 18.470806637495855 ],
          [ 8.674902783255988, -8.119544454511681, -1.013014729283598 ],
          [ -2.4322637916301617, -4.124049811601246, 11.4156989797441 ],
          [ -15.370055968673475, -2.072309319295888, -2.982479913626837 ],
          [ 4.370875735487606, 7.548759505524477, 5.275904123070921 ],
          [ -4.581706212140537, -5.558725494190707, 2.9207734326552472 ],
          [ 15.987120778389372, -12.773241561119072, -10.407826457208133 ],
          [ -14.593582749780971, -1.3883958218607688, -6.391762987307169 ],
          [ 3.8412284404814603, -3.5378382423711443, -3.8360862337338277 ],
          [ 13.729692016178715, -1.465528923075256, 5.430170325499896 ],
          [ 3.3064389387276827, -1.3421159611320765, 0.8947439740880508 ],
          [ -4.154903052087041, -0.8998861808356835, -3.5429804491187773 ],
          [ 14.480454201333055, -1.1467121047220425, 2.0568826990529905 ],
          [ -1.9746073910908712, -0.8998861808356835, -0.16455061592423925 ],
          [ 1.0798634170028203, -6.787712906874869, -8.34580155140751 ],
          [ -2.9876221203744695, 0.9513082483120082, 1.228987412684162 ],
          [ 6.057519548711058, -2.529965719835179, -4.1291920183488795 ],
          [ 8.212104175969067, 5.846689072058126, -1.3266893408891791 ],
          [ -0.5347895017537775, 0.9564504550596407, 1.3061205138986491 ],
          [ -1.9900340113337684, -0.4833674342774529, 0.08227530796211963 ],
          [ -3.7178154785382813, -8.618338509032032, -1.8666210493905893 ],
          [ 3.0904662553271187, 3.054470808093691, -4.910807443989016 ],
          [ -0.4885096410250853, -1.5220931972992133, -4.540568558159477 ],
          [ 1.573515264775538, 0.45765640053929046, 1.4758133365705208 ],
          [ 2.0568826990529905, 6.350625333326109, 14.537018475557014 ],
          [ -10.623799140608698, -8.309806104174083, 11.168873055857741 ],
          [ 6.787712906874869, -5.445596945742793, 0.22111489014819652 ],
          [ -9.286825386224255, 13.385164164087335, -5.579294321181237 ],
          [ -3.3424343859611105, 6.690010978669852, -7.533332885281578 ],
          [ -7.5436172987768435, -3.1624571497939735, -9.389669521176902 ],
          [ -13.194902514424935, 4.766825655055307, -0.2828213711197862 ],
          [ 8.165824315240373, -0.46794081403455545, -6.175790303906605 ],
          [ -5.0033671654464005, 12.87094348932409, 2.596814407554401 ],
          [ 2.308850829686982, -4.5148575244213145, 9.94502784992121 ],
          [ -13.935380286084012, -7.188805033190203, -5.615289768414665 ],
          [ 9.389669521176902, 5.41988591200463, 1.4346756825894609 ],
          [ -0.43194536680112805, -0.2931057846150512, 0.11312854844791449 ],
          [ 10.407826457208133, -0.22625709689582899, -2.5453923400780765 ],
          [ -3.337292179213477, 7.3687822693573395, 8.839453399180227 ],
          [ -0.3393856453437435, 0.4936518477727178, -0.09770192820501707 ],
          [ 0.3548122655866409, -7.877860737372956, -3.2704434914942557 ],
          [ 11.863070966788124, -1.0747212102551877, -2.051740492305358 ],
          [ 4.849100963017425, -0.41651874655823057, -0.5090784680156153 ],
          [ -3.7178154785382813, 9.98616550390227, 14.398178893370936 ],
          [ -2.005460631576666, -0.14398178893370933, -1.455244509579991 ],
          [ -3.028759774355529, 1.0387257630217603, 0.9924459022930681 ],
          [ -0.8690329403498885, 6.597451257212468, 7.929282804849279 ],
          [ -3.1418883228034438, 1.8666210493905893, 0.24168371713872644 ],
          [ -2.7767916437215376, 0.689055704182752, 2.4219793781348966 ],
          [ 0.37538109257717084, 2.751080609983375, -5.0496470261750925 ],
          [ -7.09624531173282, 3.2241636307655632, 3.095608462074751 ],
          [ 10.268986875022055, -3.7589531325193404, -8.155539901745108 ],
          [ -5.157633367875375, 6.22721237138293, 3.0133331541126314 ],
          [ -7.3687822693573395, 13.122911619958082, -9.384527314429272 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.4018326499173955, 0.8427056172789289, 0.07086274795130072 ],
        [ 0.8348365965875625, 0.09138038816945836, 0.9836830020594636 ],
        [ 0.4636834296297282, 0.9531420581965814, 0.546024141740883 ],
        [ 0.7691621378068897, 0.0469855346386777, 0.3007545249804082 ],
        [ 0.1380126481116047, 0.3058458367833609, 0.109584425473077 ],
        [ 0.3087413039039517, 0.4078660275777653, 0.06607622216104181 ],
        [ 0.6805733124355128, 0.6007955736129196, 0.2453458132636482 ],
        [ 0.5271343359087034, 0.1272273794351457, 0.5574466902620652 ],
        [ 0.9555110767497923, 0.3344333793830693, 0.6600418183076873 ],
        [ 0.1283703269827473, 0.7094656410479152, 0.3274648628201165 ],
        [ 0.1859402486076995, 0.5668119331975647, -0.01858501981948581 ],
        [ 0.8147207197497737, 0.009905545412547416, 0.6980153847073972 ],
        [ 0.2701581654788544, 0.7415651497484358, 0.9515696394492753 ],
        [ 0.2548218874764908, 0.58299329968967, 0.5823490928901127 ],
        [ 0.547631195262359, 0.1739496897901334, 0.007474184265831231 ],
        [ 0.4886689557157832, 0.830244025532654, 0.7440657804434915 ],
        [ 0.3038439468363495, 0.8513712377761993, 0.3946009090707525 ],
        [ 0.8912150819810755, 0.5835613099860539, 0.8803259089821072 ],
        [ 0.7044435987933022, 0.7381016723314614, 0.5130172019571149 ],
        [ 0.9578177527094973, 0.6532603295252509, 0.4211103652202762 ],
        [ 0.5995902834718125, 0.07695846820517609, 0.3274302280459467 ],
        [ 0.6774700366699036, 0.2893873920978975, 0.6351948313183116 ],
        [ 0.4187898353509031, 0.1460271348544839, 0.3057419324608516 ],
        [ 0.5208862226484811, 0.6381041523485701, 0.5759693674880454 ],
        [ 0.6088724029493044, 0.61928361606473, 0.403661365993558 ],
        [ 0.9393297102576867, 0.3970184163078007, 0.451007102283601 ],
        [ 0.8362358414640204, 0.8113195849263047, 0.7110588406597237 ],
        [ 0.05564422818111425, 0.9080198744082362, 0.7305582185172907 ],
        [ 0.9893631050233022, 0.1543048458810533, 0.8732950498256489 ],
        [ 0.1411574856062177, 0.6090871385491569, 0.152981797507769 ],
        [ 0.8904392630396731, 0.8165632897356045, 0.5247653173554927 ],
        [ 0.3619680248480175, 0.0826870598528521, 0.6985556871844453 ],
        [ 0.4367929909643373, 0.7122779847104987, 0.876266713449413 ],
        [ 0.9771993723348873, 0.8643177163608503, 0.01753212268472553 ],
        [ 0.3300763247925153, 0.7310431053556669, 0.2007847128168527 ],
        [ 0.5015253838875929, 0.05844271793402973, 0.1740328132481407 ],
        [ -0.01310579854583196, 0.7875116411620212, 0.1992815636178857 ],
        [ 0.3154258153187127, 0.8742371156830656, 0.6679385468183896 ],
        [ 0.03869396970244047, 0.1687406197550035, 0.6221444484111511 ],
        [ 0.5762602995910715, 0.2804585473169369, 0.8591779158740602 ],
        [ 0.6073553998406696, 0.5073093911739407, 0.6465273294266524 ],
        [ 0.6363654866852488, 0.2935158571789312, 0.4228767387029334 ],
        [ 0.2019969299127939, 0.1831417588547839, 0.9668297209484651 ],
        [ 0.7660588620412805, 0.4572552155438234, 0.205661289019953 ],
        [ 0.2567060191913249, 0.06088100603557987, 0.4297205700788752 ],
        [ 0.3246733000220348, 0.6482244333609699, 0.4216645216069922 ],
        [ 0.1830378545322748, 0.02497859913122097, 0.04774749967041211 ],
        [ 0.7276004088031944, 0.4593125211295063, 0.5118326926805093 ],
        [ 0.9143788189458019, 1.001346736886034, 0.1917727445778847 ],
        [ 0.7003289876219364, 0.2551336004440185, 0.03955291210185016 ],
        [ 0.8152263874526522, 0.3014887821928068, 0.3202677567476431 ],
        [ 0.626127447440672, 0.8718958049491911, 0.6362823632272416 ],
        [ 0.8482471811460884, 0.2764270596035785, 0.8024807905581857 ],
        [ 0.1569994313114595, 0.9988876679199822, 0.618327696297645 ],
        [ 0.2234566359883686, 0.9681389154120817, 0.8258038474840927 ],
        [ 0.2484698698937592, 0.2173055000958216, 0.5129271515442735 ],
        [ 0.04779598835424976, 0.2106486965003964, 0.4212489043169553 ],
        [ 0.3453502602013733, 0.4500304016520142, 0.2925737913215141 ],
        [ 0.5844618141144673, 0.8598567574477871, 0.1193098700599417 ],
        [ 0.5594970688929143, 0.1064603688429659, 0.7496766138589903 ],
        [ 0.4362596154421233, 0.5680310772483396, 0.1534943921654812 ],
        [ 0.1555309168866623, 0.4776689514394718, 0.3487652489345103 ],
        [ 0.9745532755883187, 0.7226891978259243, 0.7827112614620947 ],
        [ 0.9005872518714089, 0.07559385810288806, 0.5426992034205872 ],
        [ 0.5699290628728418, 0.8912012280714073, 0.2893319764592259 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  },
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/3/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -66070.45647909814,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.11010000000000009, -0.2589000000000006, -0.27839999999999954, 0.2112999999999996, -0.2375000000000007, 0.2342000000000004, 0.07779999999999987, 0.2483000000000004, 0.1897000000000002, -0.19069999999999965, -0.35660000000000025, -0.33370000000000033, 0.16929999999999978, 0.24950000000000028, 0.039699999999999847, 0.1418999999999997, 0.00569999999999915, -0.21310000000000073, -0.33670000000000044, 0.3086000000000002, -0.008000000000000007, -0.10999999999999943, 0.08399999999999963, 0.1266999999999996, 0.17079999999999984, -0.15339999999999954, 0.17469999999999963, 0.16779999999999973, 0.22299999999999986, 0.26280000000000037, -0.2942999999999998, -0.18849999999999945, 0.07390000000000008, 0.25950000000000006, -0.18190000000000062, 0.006800000000000139, -0.2355999999999998, -0.2218, 0.000700000000000145, 0.20359999999999978, 0.15950000000000042, -0.13269999999999982, 0.1294000000000004, 0.19760000000000044, 0.1346999999999996, -0.2301000000000002, 0.13680000000000003, -0.12700000000000067, -0.16910000000000025, 0.16000000000000014, -0.13260000000000005, 0.24570000000000025, -0.24590000000000067, 0.16349999999999998, -0.30489999999999995, 0.13750000000000018, -0.2992000000000008, -0.2637999999999998, 0.040600000000000414, -0.22990000000000066, -0.17440000000000033, 0.2679, 0.12490000000000023, 0.19779999999999998, 0.07260000000000044 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -5.157633367875375, 0.46279860728692285, -1.0335835562741278 ],
          [ 7.975562665577971, 5.1422067476324775, -4.149760845339409 ],
          [ 4.993082751951135, 4.134334225096511, 6.756859666389075 ],
          [ -1.5992262985137005, -5.72841831686258, -1.1107166574886151 ],
          [ -5.980386447496571, -0.9358816280691109, -11.780795658826007 ],
          [ 7.173378412947305, -3.563549276109306, -9.595357791082202 ],
          [ -5.959817620506041, -9.230261112000298, -2.84364033144076 ],
          [ -3.0390441878507937, -2.5351079265828114, 5.507303426714382 ],
          [ -7.6927412944581866, 0.2571103373816238, 5.059931439670358 ],
          [ -7.245369307414161, 5.034220405932195, -1.959180770847974 ],
          [ 8.284095070435919, -0.020568826990529906, 7.379066682852604 ],
          [ 6.06266175545869, -1.820341188661897, 13.750260843169245 ],
          [ 6.5511713964837766, -6.02152410147763, -1.2855516869081194 ],
          [ -0.9513082483120082, -3.4349941074184946, 9.405096141419799 ],
          [ -9.235403318747927, -0.005142206747632477, -1.1827075519554697 ],
          [ 3.1161772890652815, 5.389032671518836, 3.6663934110619563 ],
          [ -3.4658473479042895, -4.890238616998486, 3.2190214240179307 ],
          [ 10.927189338719012, -8.27895286368829, -6.160363683663707 ],
          [ -10.335835562741279, -0.6736290839398545, -5.471307979480955 ],
          [ 2.4425482051254264, -1.6249373322518628, -3.033901981103161 ],
          [ 10.310124529003117, -1.2495562396746918, 3.2087370105226656 ],
          [ 3.0081909473649993, -1.1467121047220425, 1.0181569360312306 ],
          [ -4.098338777863083, -1.023299142778863, -3.9337881619388444 ],
          [ 10.130147292835979, -0.2056882699052991, 2.493970272601751 ],
          [ -2.113446973276948, -0.9873036955454356, -0.056564274223957246 ],
          [ 0.6273492232111623, -4.319453668011281, -5.363321637780674 ],
          [ -2.725369576245213, 0.6941979109303844, 1.2392718261794269 ],
          [ 4.555995178402374, -1.9129009101192813, -4.016063469900965 ],
          [ 6.5511713964837766, 4.417155596216297, -0.7096245311732818 ],
          [ -0.550216121996675, 0.9975881090407005, 1.3215471341415466 ],
          [ -2.3962683443967343, -0.5347895017537775, 0.11827075519554696 ],
          [ -2.586529994059136, -6.432900641288229, -0.4370875735487605 ],
          [ 2.704800749254683, 1.650648365990025, -4.036632296891494 ],
          [ -0.5193628815108802, -1.2958361004033843, -3.054470808093691 ],
          [ 1.2906938936557517, 0.37538109257717084, 1.1981341721983672 ],
          [ 1.8357678089047944, 5.188486608361169, 10.469532938179723 ],
          [ -7.281364754647588, -8.129828868006946, 9.168554631028707 ],
          [ 5.903253346282083, -4.591990625635802, -0.025711033738162387 ],
          [ -6.643731117941162, 9.981023297154637, -3.409283073680332 ],
          [ -3.470989554651922, 2.4116949646396315, -6.4843227087645525 ],
          [ -5.5381566672001785, -2.416837171387264, -6.880272628332254 ],
          [ -9.52850910336298, 3.9852102294151694, -1.1775653452078374 ],
          [ 6.047235135215793, -0.19026164966240167, -4.7359724145695115 ],
          [ -4.412013389468665, 9.585073377586937, 1.552946437785008 ],
          [ 2.324277449929879, -3.4864161748948197, 7.296791374890486 ],
          [ -10.053014191621493, -5.784982591086537, -3.5944025165951015 ],
          [ 6.823708354108298, 4.27831601403022, 0.8176108728735639 ],
          [ -0.5759271557348373, -0.2931057846150512, 0.15426620242897432 ],
          [ 8.05783797354009, -0.3548122655866409, -1.8923320831287513 ],
          [ -2.103162559781683, 5.034220405932195, 7.029396624013596 ],
          [ -0.30853240485794864, 0.47822522752982033, -0.11827075519554696 ],
          [ 0.47822522752982033, -6.607735670707733, -2.6996585425070503 ],
          [ 7.440773163824194, -0.10284413495264955, -1.9026164966240164 ],
          [ 4.679408140345554, 0.061706480971589726, -1.0798634170028203 ],
          [ -0.8330374931164611, 7.697883501205817, 10.937473752214279 ],
          [ -1.7894879481761017, -0.0874175147097521, -1.3061205138986491 ],
          [ -2.6122410277972983, 0.8073264593782988, 0.9873036955454356 ],
          [ -0.4062343330629657, 4.016063469900965, 4.823389929279263 ],
          [ -2.9979065338697333, 1.7534925009426743, 0.4833674342774529 ],
          [ -1.3061205138986491, 0.39080771282006826, 2.0671671125482556 ],
          [ 0.21597268340056403, 2.2574287622106572, -4.437724423206827 ],
          [ -5.111353507146682, 2.108304766529316, 1.948896357352709 ],
          [ 8.237815209707229, -2.5196813063399137, -5.769555970843639 ],
          [ -3.7178154785382813, 4.627986072869229, 2.190580074491435 ],
          [ -4.427440009711562, 9.209692285009767, -8.530920994322278 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.4263332891650739, 0.8547100300061627, 0.066734282870267 ],
        [ 0.820594777448963, 0.07684070997299894, 0.9858165041483203 ],
        [ 0.4539649119976975, 0.9512232917075778, 0.5195423934106951 ],
        [ 0.7939052204737566, 0.05141878573240521, 0.3350013896794532 ],
        [ 0.1401322962907931, 0.3173930704915542, 0.1084345509706414 ],
        [ 0.3130152350364983, 0.414190337341161, 0.07493579739366289 ],
        [ 0.6741381713947743, 0.6002414172262037, 0.2346159602258608 ],
        [ 0.5242111609687768, 0.138379776717804, 0.570441657530554 ],
        [ 0.9726899247379862, 0.3440618466022588, 0.660942322436101 ],
        [ 0.1229257404832632, 0.7128667758713841, 0.3477331326642519 ],
        [ 0.1839175777961863, 0.5595524845315857, -0.02372482030627615 ],
        [ 0.8102112721528731, 0.006871539195277649, 0.7106362964148528 ],
        [ 0.2642702538699975, 0.7459222043389901, 0.9483486054514888 ],
        [ 0.2473823379848293, 0.6061431827447283, 0.6012596795867943 ],
        [ 0.5596702427637628, 0.1812714810496177, 0.00575629946701182 ],
        [ 0.4997313025856, 0.8373164464181162, 0.7576079771438623 ],
        [ 0.3062753079830657, 0.8455456687608478, 0.3744642513684619 ],
        [ 0.9060456922805609, 0.5740298201345397, 0.8884373730926617 ],
        [ 0.7106085885955169, 0.7147301267217165, 0.5371091508695903 ],
        [ 0.948161577670972, 0.6598201557530008, 0.4293880762468457 ],
        [ 0.6099460809485666, 0.07945217194539782, 0.3227822413523668 ],
        [ 0.6768327568251803, 0.2912576699030638, 0.6378132202455443 ],
        [ 0.4120360543878027, 0.1475926266469565, 0.3046336196874198 ],
        [ 0.5093043541661181, 0.6462017625494568, 0.581490150490703 ],
        [ 0.5860757945907775, 0.6267578003305614, 0.3981336560360667 ],
        [ 0.9577415562063237, 0.4046934822638165, 0.4440316587658142 ],
        [ 0.8348019618133928, 0.7967937606395132, 0.6988466192874712 ],
        [ 0.0570296191479041, 0.9195601811615959, 0.7391961311952254 ],
        [ 0.9688039030761408, 0.161446536314855, 0.8777213739645424 ],
        [ 0.117093244513078, 0.6035178668626615, 0.1541663067843743 ],
        [ 0.9000885111233642, 0.8369008291280795, 0.5096299210433136 ],
        [ 0.3459736861364289, 0.08270091376251999, 0.6870500152052555 ],
        [ 0.4245946235017526, 0.7083365474099815, 0.8684184736225484 ],
        [ 0.9830595761244084, 0.8784556311769409, 0.02553968247277085 ],
        [ 0.3102444531029186, 0.7332181691735271, 0.1770183307815729 ],
        [ 0.485551826040506, 0.06368642274332934, 0.1661291577826047 ],
        [ -0.0309357802884173, 0.762311379476114, 0.1881083854707256 ],
        [ 0.3135693914232142, 0.8459751399605527, 0.6650638605623007 ],
        [ 0.03401827518952472, 0.1709780261663691, 0.624070141854989 ],
        [ 0.5624687325166783, 0.2653785666434295, 0.8362219875543523 ],
        [ 0.5903774335426598, 0.4931576224481822, 0.64983841383728 ],
        [ 0.6212716521020735, 0.3093023872455016, 0.4195725812471395 ],
        [ 0.1985957950893247, 0.1880460428772201, 0.9723089422221192 ],
        [ 0.7705198209543437, 0.4513465230704646, 0.2054396264652666 ],
        [ 0.2663344864105144, 0.06133818505462054, 0.430018429136735 ],
        [ 0.3425240626291221, 0.6335739238871674, 0.4404088613876587 ],
        [ 0.1808350828950789, 0.0209748192371983, 0.03268829986140647 ],
        [ 0.734458094088804, 0.4742470357515009, 0.5138969252210264 ],
        [ 0.9236609384232936, 1.007802658791275, 0.1735479264097643 ],
        [ 0.7233611124448176, 0.2401783049575221, 0.04623742351661118 ],
        [ 0.8140903668598842, 0.2839428055984133, 0.3206487392635103 ],
        [ 0.631031731463108, 0.8991741530852833, 0.619013464826206 ],
        [ 0.8395607797843158, 0.2942431874364959, 0.8001948954629822 ],
        [ 0.1577683232980279, 1.000938046550832, 0.6078056519048762 ],
        [ 0.2270517255471882, 0.9581918082705306, 0.8423869773565673 ],
        [ 0.2492456888351616, 0.2317066391956021, 0.4988169445475188 ],
        [ 0.06915871706214921, 0.2148395041749357, 0.4236871924185053 ],
        [ 0.3387488722446197, 0.4358717059714221, 0.2753741624688181 ],
        [ 0.5938409109596346, 0.8505607840606273, 0.1315151644773603 ],
        [ 0.5596425349444272, 0.07821917398495483, 0.7639461408169261 ],
        [ 0.4697445151094339, 0.5819542564645778, 0.1674799139752248 ],
        [ 0.1519150464633408, 0.4730278917007258, 0.3436046675832182 ],
        [ 0.9801779629134857, 0.7122918386201663, 0.7883428757420955 ],
        [ 0.8894833432725878, 0.0689578353719647, 0.5419233844791851 ],
        [ 0.5811922914328432, 0.8851747773658718, 0.3012948274574562 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  },
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/4/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -66073.48006312546,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.11690000000000023, -0.2726000000000006, -0.2901000000000007, 0.1764000000000001, -0.24130000000000074, 0.24380000000000024, 0.09030000000000005, 0.2504999999999997, 0.18789999999999996, -0.22489999999999988, -0.3191000000000006, -0.3282000000000007, 0.16380000000000017, 0.26039999999999974, 0.04670000000000041, 0.1501999999999999, 0.01789999999999914, -0.18490000000000073, -0.3520000000000003, 0.3216999999999999, 0.010600000000000165, -0.17830000000000013, 0.10390000000000033, 0.16439999999999966, 0.17999999999999972, -0.17660000000000053, 0.17070000000000007, 0.18960000000000043, 0.22829999999999995, 0.2705000000000002, -0.30760000000000076, -0.20010000000000083, 0.07669999999999977, 0.2541000000000002, -0.20480000000000054, 0.02400000000000002, -0.2652000000000001, -0.25399999999999956, 0.019599999999999618, 0.20800000000000018, 0.18229999999999968, -0.11870000000000047, 0.13710000000000022, 0.20709999999999962, 0.13250000000000028, -0.26539999999999964, 0.1398999999999999, -0.14259999999999984, -0.16050000000000075, 0.1612, -0.13649999999999984, 0.2697000000000003, -0.25210000000000043, 0.16169999999999973, -0.3305000000000007, 0.15340000000000042, -0.29579999999999984, -0.2636000000000003, 0.044500000000000206, -0.24680000000000035, -0.17709999999999937, 0.2826000000000004, 0.13649999999999984, 0.18689999999999962, 0.06709999999999994 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -4.473719870440255, 1.8769054628858541, 0.18511944291476914 ],
          [ 4.417155596216297, 3.1110350823176485, -3.676677824557221 ],
          [ 3.4555629344090244, 2.601956614302033, 3.8412284404814603 ],
          [ -0.06684868771922219, -4.674265933597921, 0.15426620242897432 ],
          [ -3.7589531325193404, -0.30339019811031614, -8.03212693980193 ],
          [ 4.679408140345554, -2.0774515260435207, -6.453469468278758 ],
          [ -4.833674342774528, -6.695153185417486, -2.211148901481965 ],
          [ -3.167599356541606, -1.0181569360312306, 2.463117032115956 ],
          [ -5.5381566672001785, -0.2468259238863589, 4.283458220777853 ],
          [ -4.38116014898287, 3.7486687190240757, -1.4809555433181532 ],
          [ 5.394174878266468, 0.5193628815108802, 6.134652649925545 ],
          [ 3.5841181030998364, -0.9873036955454356, 9.914174609435415 ],
          [ 4.658839313355024, -4.216609533058632, -1.542662024289743 ],
          [ 0.21597268340056403, -2.9156312259076147, 7.229942687171262 ],
          [ -5.512445633462016, 1.0952900372457175, -0.26225254412925636 ],
          [ 2.164869040753273, 3.692104444800118, 2.468259238863589 ],
          [ -2.103162559781683, -3.94407257543411, 3.460705141156657 ],
          [ 7.358497855862074, -5.332468397294878, -3.5275538288758788 ],
          [ -6.499749329007451, -0.5605005354919399, -4.360591321992341 ],
          [ 1.455244509579991, -0.11827075519554696, -2.355130690415675 ],
          [ 7.301933581638117, -1.208418585693632, 1.5375198175421105 ],
          [ 2.668805302021256, -0.9153128010785809, 1.1467121047220425 ],
          [ -3.6972466515477516, -1.1364276912267774, -4.021205676648597 ],
          [ 6.869988214836989, 0.39594991956770076, 2.709942956002315 ],
          [ -2.272855382453555, -1.054152383264658, 0.0874175147097521 ],
          [ 0.32395902510084607, -2.673947508768888, -3.3938564534374347 ],
          [ -2.4116949646396315, 0.30853240485794864, 1.2444140329270597 ],
          [ 2.6122410277972983, -1.002730315788333, -3.5429804491187773 ],
          [ 4.993082751951135, 3.1418883228034438, -0.25196813063399137 ],
          [ -0.5399317085014101, 1.0284413495264952, 1.3061205138986491 ],
          [ -2.859066951683657, -0.5913537759777349, 0.15426620242897432 ],
          [ -1.7534925009426743, -4.674265933597921, 0.5810693624824698 ],
          [ 2.3911261376491018, 0.26225254412925636, -3.568691482856939 ],
          [ -0.3291012318484785, -1.0952900372457175, -1.6403639524947602 ],
          [ 0.874175147097521, 0.32395902510084607, 0.8433219066117262 ],
          [ 1.7226392604568799, 4.360591321992341, 7.502479644795784 ],
          [ -4.869669790007956, -6.921410282313314, 7.024254417265963 ],
          [ 4.843958756269793, -3.764095339266973, -0.21597268340056403 ],
          [ -4.427440009711562, 7.265938134404691, -2.123731386772213 ],
          [ -3.193310390279768, 0.1388395821860769, -5.0496470261750925 ],
          [ -3.856655060724358, -1.738065880699777, -4.679408140345554 ],
          [ -6.741433046146177, 3.5326960356235113, -1.2598406531699569 ],
          [ 4.257747187039691, 0.020568826990529906, -3.4555629344090244 ],
          [ -3.7538109257717083, 6.803139527117767, 0.678771290687487 ],
          [ 2.13915800701511, -2.704800749254683, 4.951945097970075 ],
          [ -6.972832349789639, -4.376017942235237, -2.0825937327911532 ],
          [ 4.751399034812408, 3.3578610062040077, 0.334243438596111 ],
          [ -0.7250511514161793, -0.2931057846150512, 0.23654151039109392 ],
          [ 6.031808514972895, -0.47308302078218784, -1.316404927393914 ],
          [ -1.1364276912267774, 3.069897428336589, 5.363321637780674 ],
          [ -0.2776791643721538, 0.45251419379165797, -0.1285551686908119 ],
          [ 0.45765640053929046, -5.41988591200463, -2.1340158002674783 ],
          [ 4.458293250197357, 0.344527852091376, -1.6557905727376574 ],
          [ 4.355449115244708, 0.46279860728692285, -1.7277814672045122 ],
          [ 0.2725369576245213, 5.646143008900459, 7.682456880962921 ],
          [ -1.4963821635610508, -0.05142206747632477, -1.1518543114696747 ],
          [ -2.1597268340056406, 0.5090784680156153, 0.9307394213214785 ],
          [ -0.10798634170028201, 2.1802956609961703, 2.668805302021256 ],
          [ -2.8025026774597, 1.5118087838039482, 0.7199089446685468 ],
          [ -0.2571103373816238, 0.21597268340056403, 1.6660749862329223 ],
          [ 0.11312854844791449, 1.7329236739521447, -3.8103751999956654 ],
          [ -3.126461702560546, 1.1672809317125723, 0.7353355649114441 ],
          [ 6.5511713964837766, -1.4758133365705208, -3.8926505079577853 ],
          [ -2.5711033738162388, 3.373287626446905, 1.5323776107944782 ],
          [ -2.704800749254683, 6.417474021045331, -6.777428493379604 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.4366752327321602, 0.8690903882414414, 0.06784259564369886 ],
        [ 0.8098857052756772, 0.06674813677993491, 0.9893977397974718 ],
        [ 0.4506469006322359, 0.95143802730743, 0.5105719869007308 ],
        [ 0.8059373410203263, 0.05659322099336529, 0.3519170133839572 ],
        [ 0.1361285163967705, 0.3257192702019612, 0.1024981506779469 ],
        [ 0.3134516331910371, 0.4178546964483201, 0.07587786325107998 ],
        [ 0.6762231847997928, 0.6012111909029565, 0.2312563871313954 ],
        [ 0.523885594091581, 0.1422796522893174, 0.5846834766691535 ],
        [ 0.9798731769007917, 0.346486280794141, 0.6597439592498276 ],
        [ 0.1159087352364727, 0.7035569485745566, 0.3547570648658765 ],
        [ 0.1641341947904272, 0.5522514741366034, -0.0333532875254656 ],
        [ 0.8029310426223925, 0.004391689364723819, 0.717930379855001 ],
        [ 0.2573225181715464, 0.745520440958621, 0.9463674963689793 ],
        [ 0.2430045025297733, 0.6428006277259878, 0.6124536385984561 ],
        [ 0.5663270463591882, 0.1860510798850427, 0.004079976397196103 ],
        [ 0.4996273982630908, 0.8283460399081523, 0.7607320337739736 ],
        [ 0.302139915947198, 0.8364020883800352, 0.3624667655960619 ],
        [ 0.930137641193036, 0.5584788065323236, 0.9003448084522203 ],
        [ 0.7062930957339666, 0.7205002800983965, 0.5440845943873771 ],
        [ 0.9394128337156943, 0.6616419448743297, 0.4386979035436733 ],
        [ 0.6242779505000076, 0.07610645276060032, 0.3227476065781971 ],
        [ 0.6717206641577257, 0.290821271748525, 0.6400852614310797 ],
        [ 0.4139963826058103, 0.1561127810927141, 0.2996046504779726 ],
        [ 0.5033263921444199, 0.6527477348675389, 0.5812961957553525 ],
        [ 0.5865953162033235, 0.632811958855433, 0.3979881899845537 ],
        [ 0.9691571777726721, 0.4080946170872856, 0.442826368624707 ],
        [ 0.8476930247593722, 0.792880031158332, 0.6937137457555146 ],
        [ 0.05823490928901127, 0.9304077924315602, 0.7500021807361863 ],
        [ 0.9484317289094962, 0.1601442688060725, 0.8746319521086009 ],
        [ 0.1057815272692389, 0.6010449439869419, 0.1499062295614955 ],
        [ 0.8980450594473492, 0.8455664496253498, 0.5040883571761542 ],
        [ 0.333394336157977, 0.0812254723828888, 0.6802200377389815 ],
        [ 0.4154718239854416, 0.702635663581641, 0.864511671096201 ],
        [ 0.9909147429061068, 0.878407142493103, 0.03511273405328871 ],
        [ 0.3113943276053542, 0.7343057010824573, 0.1590913716713122 ],
        [ 0.4773710923816119, 0.07120909569299821, 0.1611971659408328 ],
        [ -0.03682369189727416, 0.745541221823123, 0.1802670725986951 ],
        [ 0.315786016970078, 0.8265727394706612, 0.6583724221927055 ],
        [ 0.03403905605402657, 0.170853340979358, 0.6210153547732175 ],
        [ 0.5572873703008844, 0.2587217630480042, 0.8253743762843878 ],
        [ 0.5879529993507777, 0.4857249999113547, 0.6487855167025199 ],
        [ 0.6182999884783094, 0.3137772000682327, 0.4146336624505338 ],
        [ 0.1947582621113168, 0.1931096468608369, 0.9709651129843329 ],
        [ 0.7703327931738272, 0.4490052123365898, 0.2014081387519082 ],
        [ 0.2737186202635043, 0.05868516135321796, 0.4367791370546695 ],
        [ 0.3504762067784958, 0.6254832406411146, 0.4484926176788774 ],
        [ 0.174538480951019, 0.02570592938878563, 0.03121978543660922 ],
        [ 0.732165272038767, 0.4790474154514278, 0.51202664741586 ],
        [ 0.9328807153072801, 1.016537548836885, 0.1653117771121986 ],
        [ 0.7313340374586932, 0.2372066413337578, 0.05247860982199946 ],
        [ 0.8131829357766371, 0.2819270617417342, 0.3178571764654289 ],
        [ 0.6306368950375729, 0.9036489659080142, 0.6154599369963901 ],
        [ 0.8427056172789289, 0.3183974789424769, 0.8071911198452713 ],
        [ 0.1577683232980279, 0.9948284723872881, 0.5968610632672364 ],
        [ 0.2286310712493287, 0.9464714006914883, 0.8510525978538377 ],
        [ 0.2626354925291855, 0.2418615549821717, 0.483224369216299 ],
        [ 0.07719398466953035, 0.2154352222906554, 0.4257860597331919 ],
        [ 0.3429188990546571, 0.4263263622102401, 0.2715297025359764 ],
        [ 0.5972697536024394, 0.8398724927518435, 0.1406102561743357 ],
        [ 0.5549183517476737, 0.06622861516738869, 0.773636950629621 ],
        [ 0.4765329308467041, 0.5824807050319577, 0.1710750035340444 ],
        [ 0.1511184466574367, 0.4757432579956339, 0.3459459783170931 ],
        [ 0.9897648684036712, 0.7012087108858478, 0.7898321710313944 ],
        [ 0.8746942947021064, 0.07108441050598711, 0.5437382466456797 ],
        [ 0.5899341084332872, 0.8870727629903739, 0.3102860148319224 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  },
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/5/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -66076.01087120819,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.12739999999999974, -0.28659999999999997, -0.2873999999999999, 0.1708999999999996, -0.2563999999999993, 0.2504999999999997, 0.11329999999999973, 0.2508999999999997, 0.1974999999999998, -0.27449999999999974, -0.2538999999999998, -0.3131000000000004, 0.15620000000000012, 0.26119999999999965, 0.032600000000000406, 0.15169999999999995, 0.030699999999999505, -0.14129999999999932, -0.3625000000000007, 0.33199999999999985, 0.006199999999999761, -0.24080000000000013, 0.1333000000000002, 0.20779999999999976, 0.16830000000000034, -0.20069999999999943, 0.16500000000000004, 0.1814, 0.23690000000000033, 0.2972999999999999, -0.29850000000000065, -0.22439999999999927, 0.0658000000000003, 0.2694000000000001, -0.23850000000000016, 0.049100000000000144, -0.28309999999999924, -0.27120000000000033, 0.028500000000000192, 0.21980000000000022, 0.2054999999999998, -0.09440000000000026, 0.15559999999999974, 0.20500000000000007, 0.13710000000000022, -0.2718000000000007, 0.13149999999999995, -0.21480000000000032, -0.2171000000000003, 0.1698000000000004, -0.1266999999999996, 0.3106, -0.25420000000000087, 0.14670000000000005, -0.3545999999999996, 0.1620999999999997, -0.29320000000000057, -0.2859999999999996, 0.053300000000000125, -0.2649000000000008, -0.1698000000000004, 0.29800000000000004, 0.14540000000000042, 0.1905000000000001, 0.06590000000000007 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -3.2087370105226656, 1.4501023028323585, 1.002730315788333 ],
          [ 2.6996585425070503, 2.0208872518195635, -3.167599356541606 ],
          [ 2.5608189603209732, 1.7432080874474098, 2.13915800701511 ],
          [ 0.020568826990529906, -3.409283073680332, 0.49879405452035025 ],
          [ -1.4758133365705208, -0.10284413495264955, -5.697565076376784 ],
          [ 3.157314943046341, -1.1621387249649395, -4.4788620771878875 ],
          [ -3.5121272086329816, -4.720545794326614, -1.6609327794852904 ],
          [ -2.8076448842073325, -0.334243438596111, 1.0644367967599226 ],
          [ -3.9749258159199043, -0.6479180502016921, 3.321865558970581 ],
          [ -2.936200052898144, 2.900204605664717, -0.9667348685549058 ],
          [ 3.4452785209137597, 0.4473719870440254, 5.219339848846965 ],
          [ 2.277997589201187, -0.689055704182752, 6.905983662070417 ],
          [ 3.4041408669326993, -2.7356539897404777, -1.5169509905515806 ],
          [ 0.7816154256401365, -2.4219793781348966, 5.35817943103304 ],
          [ -3.470989554651922, 1.3832536151131363, -0.0874175147097521 ],
          [ 1.5323776107944782, 2.6379520615354606, 1.6917860199710848 ],
          [ -1.3729692016178714, -2.7767916437215376, 3.1881681835321354 ],
          [ 4.370875735487606, -3.285870111737153, -1.861478842642957 ],
          [ -3.8360862337338277, -0.7199089446685468, -3.3527187994563743 ],
          [ 1.069579003507555, 0.41651874655823057, -1.6917860199710848 ],
          [ 5.008509372194032, -1.3421159611320765, 0.7044823244256493 ],
          [ 2.324277449929879, -0.7404777716590766, 1.1107166574886151 ],
          [ -2.6996585425070503, -1.187849758703102, -3.3064389387276827 ],
          [ 4.807963309036365, 0.5399317085014101, 2.437405998377794 ],
          [ -2.2677131757059223, -1.0284413495264952, 0.21083047665293156 ],
          [ 0.22625709689582899, -1.928327530362179, -2.4888280658541193 ],
          [ -2.051740492305358, -0.19540385641003413, 1.1929919654507346 ],
          [ 1.2392718261794269, -0.3548122655866409, -2.7870760572168023 ],
          [ 3.8206596134909305, 2.1957222812390675, -0.025711033738162387 ],
          [ -0.47822522752982033, 1.013014729283598, 1.187849758703102 ],
          [ -2.745938403235743, -0.46279860728692285, 0.11312854844791449 ],
          [ -1.3009783071510166, -3.4144252804279644, 0.9358816280691109 ],
          [ 2.103162559781683, -0.24168371713872644, -2.936200052898144 ],
          [ 0.025711033738162387, -0.8433219066117262, -0.8638907336022561 ],
          [ 0.550216121996675, 0.32395902510084607, 0.5913537759777349 ],
          [ 1.7226392604568799, 3.5429804491187773, 5.152491161127742 ],
          [ -3.476131761399554, -4.890238616998486, 4.7359724145695115 ],
          [ 3.4555629344090244, -2.84364033144076, -0.344527852091376 ],
          [ -2.8230715044502297, 5.327326190547246, -1.6969282267187173 ],
          [ -2.586529994059136, -0.334243438596111, -3.6612512043143237 ],
          [ -2.668805302021256, -1.0747212102551877, -2.895062398917085 ],
          [ -5.029078199184562, 2.9516266731410417, -1.0952900372457175 ],
          [ 2.889920192169452, 0.1748350294195042, -2.4528326186206915 ],
          [ -3.0081909473649993, 4.597132832383434, 0.061706480971589726 ],
          [ 1.928327530362179, -2.1340158002674783, 3.265301284746623 ],
          [ -4.972513924960605, -2.8282137111978622, -1.1775653452078374 ],
          [ 3.2241636307655632, 2.576245580563871, -0.025711033738162387 ],
          [ -0.7970420458830338, -0.29824799136268365, 0.31881681835321357 ],
          [ 4.185756292572836, -0.5142206747632476, -0.9667348685549058 ],
          [ -0.5039362612679827, 1.7226392604568799, 3.938930368686478 ],
          [ -0.26739475087688874, 0.3650966790819059, -0.14398178893370933 ],
          [ 0.25196813063399137, -4.448008836702092, -1.542662024289743 ],
          [ 2.848782538188392, 0.30339019811031614, -1.3318315476368114 ],
          [ 3.429851900670862, 0.5862115692301024, -2.0671671125482556 ],
          [ 0.19540385641003413, 3.9543569889293746, 5.594720941424135 ],
          [ -1.2238452059365295, -0.07713310121448716, -1.0644367967599226 ],
          [ -1.6969282267187173, 0.32395902510084607, 0.6839134974351194 ],
          [ -0.005142206747632477, 1.2495562396746918, 1.6403639524947602 ],
          [ -2.293424209444085, 0.8844595605927861, 0.7559043919019741 ],
          [ 0.38566550607243577, 0.31367461160558113, 1.347258167879709 ],
          [ 0.09255972145738457, 1.1827075519554697, -3.0441863945984267 ],
          [ -1.542662024289743, 0.6273492232111623, -0.07713310121448716 ],
          [ 4.987940545203502, -0.8690329403498885, -2.4425482051254264 ],
          [ -1.846052222400059, 2.555676753573341, 1.1055744507409826 ],
          [ -2.1597268340056406, 4.766825655055307, -4.5714217986452725 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.4453200723649289, 0.877354245358343, 0.0762172840379435 ],
        [ 0.8018642915779639, 0.06857685285609749, 0.996490941547436 ],
        [ 0.4435814067016076, 0.9541395396926703, 0.509726898410989 ],
        [ 0.8169165644321359, 0.05592130637447223, 0.3546462335885333 ],
        [ 0.1273105028931531, 0.3482318734122963, 0.07582937456724234 ],
        [ 0.3196166229932519, 0.4172381974680986, 0.0851946175027417 ],
        [ 0.6849511478905687, 0.604148219752551, 0.2305429107834986 ],
        [ 0.5199510837458979, 0.143159375553229, 0.6022017454442112 ],
        [ 0.984652775736217, 0.347047364135691, 0.657243328554772 ],
        [ 0.1026643975939617, 0.6804971159323396, 0.3552627325687547 ],
        [ 0.1404093744841511, 0.5295864779199213, -0.05112785362937934 ],
        [ 0.7844083653964119, 0.002168136863026113, 0.7245733295407587 ],
        [ 0.2474931692621725, 0.7423617495543401, 0.9395375189027052 ],
        [ 0.2294692327842365, 0.6573680137417829, 0.6069536364603003 ],
        [ 0.5641866173154979, 0.1932343320478481, 0.01057746003144049 ],
        [ 0.4903660596501007, 0.8162169419939072, 0.7664259906474798 ],
        [ 0.2953445732550938, 0.8203176992556048, 0.3607488807972426 ],
        [ 0.9336496072938482, 0.5439114205165284, 0.9107698754773141 ],
        [ 0.7029196687298334, 0.741856081851462, 0.5537476963807364 ],
        [ 0.9284751720328885, 0.6574580641546242, 0.4526487905792472 ],
        [ 0.6436803509898992, 0.0654250884066506, 0.3211197721922189 ],
        [ 0.6695317464301977, 0.2884176184211446, 0.6446293438021502 ],
        [ 0.4302331647365875, 0.1873533473938251, 0.2919988540702964 ],
        [ 0.5008673231783678, 0.6609284685264328, 0.5769114333454626 ],
        [ 0.6005877649679011, 0.6371413056266512, 0.4024283680331152 ],
        [ 0.980406552423006, 0.4095007889185772, 0.4486865724142282 ],
        [ 0.8709191043176041, 0.7936419961900661, 0.6985210524102752 ],
        [ 0.06531425712930738, 0.939336637212521, 0.7595752323167042 ],
        [ 0.9202805844643266, 0.1499062295614955, 0.8519115402532474 ],
        [ 0.106862132223335, 0.5951778132425868, 0.1377702046924165 ],
        [ 0.896188635551851, 0.8514058725503689, 0.5051481812657483 ],
        [ 0.3240637279966474, 0.08884512270023297, 0.6747546703749957 ],
        [ 0.404492600573632, 0.690679739538245, 0.866839127920408 ],
        [ 1.001014243054005, 0.8676772894553157, 0.05036588859764492 ],
        [ 0.3193187639353921, 0.7324492771869586, 0.1477311657436354 ],
        [ 0.4724668083591759, 0.08986338506082348, 0.1515964065409791 ],
        [ -0.04354283808620494, 0.7217124971943375, 0.1747255087315357 ],
        [ 0.3215561703467578, 0.8264203464643144, 0.6562181392393474 ],
        [ 0.03983691725004208, 0.169772736025262, 0.6215695111599333 ],
        [ 0.5547867396058287, 0.2552652125858635, 0.826323369096639 ],
        [ 0.5944435560301881, 0.4757155501762981, 0.6462017625494568 ],
        [ 0.6247420564738821, 0.3100712792320699, 0.4086834082481713 ],
        [ 0.1940655666279219, 0.202239373331982, 0.9606716581010842 ],
        [ 0.7676866964272587, 0.448582668091719, 0.1868892414199506 ],
        [ 0.2751455729592979, 0.05143263964207312, 0.4326575989284696 ],
        [ 0.348259581231632, 0.6223661109658374, 0.4529743574564427 ],
        [ 0.1543325537003891, 0.04356361895070678, 0.03782810034819681 ],
        [ 0.719198012589614, 0.4866047231752662, 0.4953049784467067 ],
        [ 0.9535992372156221, 1.032968285703013, 0.1558010681251863 ],
        [ 0.7312439870458518, 0.2387859870358982, 0.06379032706583858 ],
        [ 0.8179209728830585, 0.2949428098747248, 0.3094755611163503 ],
        [ 0.6273188836721112, 0.9057478332227008, 0.6247004947448784 ],
        [ 0.8530614147556831, 0.3436185214928861, 0.8143397372339066 ],
        [ 0.1557941411703524, 0.9933183962334874, 0.5920260487931398 ],
        [ 0.2290813233135353, 0.9373278203106753, 0.8613737605564221 ],
        [ 0.2759075379910323, 0.2414182298727989, 0.4603861991287684 ],
        [ 0.08289486849787059, 0.2123180926153782, 0.4288685546342995 ],
        [ 0.3542860319371679, 0.4107199329693523, 0.2782904104539108 ],
        [ 0.596223783422513, 0.8263718577804766, 0.1497676904648166 ],
        [ 0.5510323300858283, 0.06306299680827387, 0.7828982892426112 ],
        [ 0.473422728126261, 0.5706771739949084, 0.168117193819948 ],
        [ 0.1579553510785446, 0.4866670657687717, 0.3537942181439575 ],
        [ 1.005641448883083, 0.6829838927177273, 0.7863548397047518 ],
        [ 0.8591848428288942, 0.07945909890023174, 0.5541356058514375 ],
        [ 0.5972281918734357, 0.8944846046626992, 0.3191732978838792 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  },
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/6/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -66077.76373465522,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.1520999999999999, -0.27449999999999974, -0.31039999999999957, 0.17689999999999984, -0.2652000000000001, 0.2656999999999998, 0.1557000000000004, 0.2544000000000004, 0.21009999999999973, -0.2726000000000006, -0.2699999999999996, -0.29770000000000074, 0.14920000000000044, 0.2699999999999996, 0.024799999999999933, 0.15620000000000012, 0.04860000000000042, -0.1725999999999992, -0.3609000000000009, 0.3398000000000003, 0.022400000000000198, -0.23029999999999973, 0.14900000000000002, 0.19810000000000016, 0.15920000000000023, -0.2085000000000008, 0.16049999999999986, 0.15950000000000042, 0.24680000000000035, 0.2919999999999998, -0.3224999999999998, -0.19549999999999912, 0.0708000000000002, 0.2892999999999999, -0.24629999999999974, 0.02880000000000038, -0.28030000000000044, -0.27009999999999934, 0.021099999999999675, 0.23850000000000016, 0.2264999999999997, -0.11469999999999914, 0.16389999999999993, 0.19920000000000027, 0.16790000000000038, -0.2889999999999997, 0.15329999999999977, -0.23440000000000083, -0.2745999999999995, 0.17030000000000012, -0.11359999999999992, 0.3128000000000002, -0.26759999999999984, 0.13379999999999992, -0.3414999999999999, 0.16110000000000024, -0.2873999999999999, -0.3078000000000003, 0.03509999999999991, -0.26619999999999955, -0.19369999999999976, 0.31240000000000023, 0.16080000000000005, 0.17630000000000035, 0.054700000000000415 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -2.7922182639644353, 0.9924459022930681, 1.1775653452078374 ],
          [ 2.3499884836680422, 1.6455061592423927, -2.6482364750307252 ],
          [ 2.28313979594882, 1.6095107120089653, 1.7586347076903073 ],
          [ 0.08227530796211963, -2.78193385046917, 0.46794081403455545 ],
          [ -1.2546984464223245, 0.42680316005349556, -4.5714217986452725 ],
          [ 2.4116949646396315, -0.6941979109303844, -3.589260309847469 ],
          [ -2.756222816731008, -3.77952195950987, -1.4089646488512986 ],
          [ -2.4785436523588538, -0.25196813063399137, 0.7353355649114441 ],
          [ -3.3784298331945375, -0.8947439740880508, 2.67908971551652 ],
          [ -2.3962683443967343, 2.447690411873059, -0.6736290839398545 ],
          [ 2.7870760572168023, 0.43194536680112805, 4.828532136026896 ],
          [ 1.9746073910908712, -0.5759271557348373, 5.52273004695728 ],
          [ 2.946484466393409, -2.036313872062461, -1.3009783071510166 ],
          [ 0.874175147097521, -2.0877359395387853, 4.175471879077571 ],
          [ -3.018475360860264, 1.2135607924412646, -0.24168371713872644 ],
          [ 1.1827075519554697, 2.1597268340056406, 1.3112627206462815 ],
          [ -1.3678269948702388, -1.995176218081401, 2.7202273694975805 ],
          [ 3.6612512043143237, -2.936200052898144, -1.4912399568134185 ],
          [ -3.1110350823176485, -0.8998861808356835, -2.8076448842073325 ],
          [ 0.9204550078262134, 0.37538109257717084, -1.2906938936557517 ],
          [ 4.232036153301529, -1.1775653452078374, 0.6633446704445896 ],
          [ 1.8871898763811192, -0.5553583287443076, 1.002730315788333 ],
          [ -1.969465184343239, -1.1775653452078374, -2.601956614302033 ],
          [ 3.7538109257717083, 0.45765640053929046, 1.9797495978385038 ],
          [ -2.0568826990529905, -0.9410238348167432, 0.19540385641003413 ],
          [ 0.2005460631576666, -1.6197951255042302, -2.098020353034051 ],
          [ -1.6043685052613328, -0.4833674342774529, 1.023299142778863 ],
          [ 0.9564504550596407, -0.2725369576245213, -2.2060066947343326 ],
          [ 3.2035948037750335, 1.6917860199710848, 0.07713310121448716 ],
          [ -0.4010921263153332, 0.9564504550596407, 1.0387257630217603 ],
          [ -2.360272897163307, -0.2828213711197862, 0.0874175147097521 ],
          [ -1.0747212102551877, -2.751080609983375, 0.9358816280691109 ],
          [ 1.820341188661897, -0.23654151039109392, -2.401410551144367 ],
          [ 0.10798634170028201, -0.6530602569493246, -0.7507621851543417 ],
          [ 0.334243438596111, 0.26739475087688874, 0.45765640053929046 ],
          [ 1.7226392604568799, 3.095608462074751, 3.94407257543411 ],
          [ -2.84364033144076, -3.9132193349483146, 3.6509667908190586 ],
          [ 2.6996585425070503, -2.355130690415675, -0.37538109257717084 ],
          [ -2.190580074491435, 4.504573110926049, -1.5478042310373754 ],
          [ -2.072309319295888, -0.16455061592423925, -2.9670532933839397 ],
          [ -2.154584627258008, -0.9307394213214785, -2.108304766529316 ],
          [ -4.185756292572836, 2.689374129011785, -0.776473218892504 ],
          [ 2.3808417241538367, 0.2776791643721538, -2.123731386772213 ],
          [ -2.504254686097016, 3.5944025165951015, -0.11827075519554696 ],
          [ 1.5580886445326407, -1.861478842642957, 2.684231922264153 ],
          [ -4.134334225096511, -2.051740492305358, -0.786757632387769 ],
          [ 2.607098821049666, 2.164869040753273, -0.1799772361671367 ],
          [ -0.8124686661259314, -0.2828213711197862, 0.3496700588390084 ],
          [ 3.440136314166127, -0.5450739152490426, -0.874175147097521 ],
          [ -0.2571103373816238, 1.1827075519554697, 3.213879217270298 ],
          [ -0.2468259238863589, 0.29824799136268365, -0.16455061592423925 ],
          [ 0.15940840917660679, -3.728099892033545, -1.2135607924412646 ],
          [ 2.272855382453555, 0.22625709689582899, -1.1569965182173072 ],
          [ 2.5351079265828114, 0.45251419379165797, -1.9334697371098115 ],
          [ 0.07199089446685467, 2.931057846150512, 4.504573110926049 ],
          [ -0.9204550078262134, -0.09770192820501707, -0.9358816280691109 ],
          [ -1.4501023028323585, 0.22625709689582899, 0.4833674342774529 ],
          [ 0.025711033738162387, 0.8896017673404186, 1.2752672734128543 ],
          [ -1.846052222400059, 0.4216609533058631, 0.6376336367064271 ],
          [ 0.3291012318484785, 0.5964959827253673, 1.2238452059365295 ],
          [ 0.07199089446685467, 0.8998861808356835, -2.5659611670686058 ],
          [ -0.9564504550596407, 0.46279860728692285, -0.025711033738162387 ],
          [ 4.046916710386759, -0.7456199784067092, -1.8511944291476914 ],
          [ -1.4809555433181532, 2.13915800701511, 0.8793173538451536 ],
          [ -1.8049145684189993, 4.062343330629657, -3.918361541695948 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.4507023162709073, 0.871778046717014, 0.08693328316606297 ],
        [ 0.8057433862849755, 0.07965998059041628, 0.9984859045396132 ],
        [ 0.4336620073793923, 0.9604430685915639, 0.5112785362937935 ],
        [ 0.8332988126144258, 0.05481299360104035, 0.3542583241178321 ],
        [ 0.1319307817673973, 0.3520832602999721, 0.07278844139513863 ],
        [ 0.3224289666558353, 0.4156311439466224, 0.09071540050539928 ],
        [ 0.6794095840234096, 0.6005531301937315, 0.2262759066057859 ],
        [ 0.5135852122534987, 0.143699678030277, 0.6036633329141746 ],
        [ 0.9892799815652947, 0.3486267098378313, 0.6601387956753627 ],
        [ 0.09155356204030714, 0.6780241930566197, 0.3546531605433673 ],
        [ 0.134701563700977, 0.5298427752487774, -0.06829284770790559 ],
        [ 0.7756665483959679, 0.007065493930628227, 0.7242131278893932 ],
        [ 0.2448609264252717, 0.7475084769959645, 0.9378681227877238 ],
        [ 0.2189887501204713, 0.658476326515215, 0.6006778153807424 ],
        [ 0.5597949279507739, 0.1998565008691036, 0.02304597873254912 ],
        [ 0.4858496850983658, 0.8126357063447552, 0.7765809064340493 ],
        [ 0.2864088015192993, 0.8110355797781128, 0.3579503910443271 ],
        [ 0.9114694979155429, 0.553103489581179, 0.9085255421111146 ],
        [ 0.7164341576108679, 0.7429159059410559, 0.5734964446123255 ],
        [ 0.920467612244843, 0.6552275846980927, 0.4585990447816096 ],
        [ 0.6600625991721892, 0.06412282089786814, 0.3076884067691914 ],
        [ 0.6707785983003088, 0.2844623272109596, 0.6488686401605274 ],
        [ 0.4552741064613138, 0.2219465598345677, 0.2921581740314771 ],
        [ 0.5007772727655265, 0.6652993770266549, 0.5668534949265682 ],
        [ 0.5984750437435467, 0.6427867738163198, 0.408586430880496 ],
        [ 0.986474564857545, 0.4119944926587991, 0.4504598728517191 ],
        [ 0.8747289294762763, 0.8011438882752336, 0.7093755906350739 ],
        [ 0.06993453600355154, 0.9391842442061739, 0.7538466406690277 ],
        [ 0.906987758137978, 0.1408665535031918, 0.836713801347563 ],
        [ 0.1257934997845183, 0.592566351270188, 0.1265831726355884 ],
        [ 0.9012799473548038, 0.8510733787183397, 0.5107243799070775 ],
        [ 0.3221518884624774, 0.08660771628886738, 0.6820071920861404 ],
        [ 0.4003295007184285, 0.6852628608580964, 0.8727755282131027 ],
        [ 1.00388200235526, 0.8607226268020307, 0.06254347519572771 ],
        [ 0.3223527701526619, 0.7280368069577332, 0.1533212182946325 ],
        [ 0.4716494276887698, 0.1089956343121913, 0.1523791524372154 ],
        [ -0.04465807781447075, 0.693533644929832, 0.161425755450353 ],
        [ 0.3181065468394509, 0.8308466706032076, 0.6597370322949937 ],
        [ 0.03979535552103839, 0.1682765137811289, 0.6256079258281257 ],
        [ 0.5621085308653132, 0.2617904040394437, 0.8332641778402559 ],
        [ 0.6023679923602261, 0.4730417456103937, 0.6422741791586074 ],
        [ 0.6365663683754336, 0.2969308459120682, 0.4104774895501641 ],
        [ 0.1858848329690279, 0.2064440349161892, 0.9530658616934082 ],
        [ 0.7709492921540485, 0.4545744840230851, 0.1724326866814985 ],
        [ 0.2667362497908835, 0.0402733154045809, 0.4167325297652202 ],
        [ 0.3409516438818156, 0.6187987292263536, 0.4540895971847086 ],
        [ 0.1421688210119742, 0.06035455746819973, 0.04363288849904628 ],
        [ 0.7157276082178055, 0.4932407459061897, 0.4814995574626456 ],
        [ 0.9706187652426355, 1.035455062488401, 0.1456392253837828 ],
        [ 0.7320682946710916, 0.2443552587223934, 0.07702773775351558 ],
        [ 0.8281659390824694, 0.3070164921502983, 0.3007960867094119 ],
        [ 0.6150858814353568, 0.9094814618781996, 0.6278037705104875 ],
        [ 0.8454625453028407, 0.3294251910381241, 0.7976388491292549 ],
        [ 0.1487286472397241, 0.9972044178953329, 0.5978031291246535 ],
        [ 0.2323231381758236, 0.9467969675686843, 0.8627591515232118 ],
        [ 0.2721531284710317, 0.2238099106848999, 0.4539579850428634 ],
        [ 0.07887030773934607, 0.2091663281659313, 0.4287923581311259 ],
        [ 0.3587677717147331, 0.3985839081002733, 0.282093308657749 ],
        [ 0.6020562793926983, 0.8233794132922105, 0.1631644211136744 ],
        [ 0.5421242661693694, 0.06987912036487993, 0.7894719693800287 ],
        [ 0.4790543424062615, 0.5581255318357922, 0.160767694741128 ],
        [ 0.159527769825851, 0.4825870893715757, 0.3618779744351763 ],
        [ 0.9986105897266245, 0.6708686487131502, 0.7827458962362644 ],
        [ 0.864809530154061, 0.07634889617978853, 0.55435034145129 ],
        [ 0.5971589223250962, 0.8934109266634372, 0.3270977342139171 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  },
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/7/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -66078.7411771705,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.15779999999999994, -0.2927999999999997, -0.32540000000000013, 0.1750999999999996, -0.25869999999999926, 0.24570000000000025, 0.17039999999999988, 0.2667999999999999, 0.20790000000000042, -0.28279999999999994, -0.28219999999999956, -0.2843, 0.14569999999999972, 0.27230000000000043, 0.04260000000000019, 0.15219999999999967, 0.032099999999999795, -0.15479999999999983, -0.3772000000000002, 0.3310000000000004, 0.024499999999999744, -0.2441999999999993, 0.12929999999999975, 0.1737000000000002, 0.16920000000000002, -0.21059999999999945, 0.15829999999999966, 0.1506999999999996, 0.22989999999999977, 0.2965, -0.33000000000000007, -0.19250000000000078, 0.09030000000000005, 0.3036000000000003, -0.2699999999999996, 0.028400000000000425, -0.2873999999999999, -0.2637999999999998, 0.025299999999999656, 0.2392000000000003, 0.23749999999999982, -0.11209999999999987, 0.16310000000000002, 0.21410000000000018, 0.17900000000000027, -0.28279999999999994, 0.13619999999999965, -0.2645999999999997, -0.2670999999999992, 0.1700999999999997, -0.10479999999999912, 0.31979999999999986, -0.2735000000000003, 0.14730000000000043, -0.33859999999999957, 0.17970000000000041, -0.2763000000000009, -0.2848000000000006, 0.03169999999999984, -0.2652000000000001, -0.2004999999999999, 0.30959999999999965, 0.1955, 0.17220000000000013, 0.0528000000000004 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -2.632809854787828, 0.8433219066117262, 1.336973754384444 ],
          [ 2.113446973276948, 1.3678269948702388, -2.28313979594882 ],
          [ 2.0568826990529905, 1.4603867163276236, 1.4295334758418285 ],
          [ 0.1799772361671367, -2.3037086229393493, 0.3702388858295383 ],
          [ -0.8587485268546237, 0.7353355649114441, -3.9646414024246397 ],
          [ 1.9746073910908712, -0.47822522752982033, -3.054470808093691 ],
          [ -2.355130690415675, -3.2087370105226656, -1.2906938936557517 ],
          [ -2.2471443487153926, -0.21597268340056403, 0.5759271557348373 ],
          [ -2.9773377068792044, -1.05929459001229, 2.277997589201187 ],
          [ -2.046598285557726, 2.11858918002458, -0.4833674342774529 ],
          [ 2.3499884836680422, 0.4062343330629657, 4.555995178402374 ],
          [ 1.6866438132234525, -0.5399317085014101, 4.669123726850289 ],
          [ 2.663663095273623, -1.6249373322518628, -1.0901478304980852 ],
          [ 0.8381796998640936, -1.8871898763811192, 3.4349941074184946 ],
          [ -2.673947508768888, 1.069579003507555, -0.2005460631576666 ],
          [ 0.9615926618072733, 1.9180431168669139, 1.0747212102551877 ],
          [ -1.3626847881226065, -1.465528923075256, 2.385983930901469 ],
          [ 3.028759774355529, -2.6379520615354606, -1.187849758703102 ],
          [ -2.6276676480401955, -0.8896017673404186, -2.4836858591064868 ],
          [ 0.7970420458830338, 0.2931057846150512, -1.0490101765170254 ],
          [ 3.6972466515477516, -1.14156989797441, 0.6067803962206323 ],
          [ 1.6249373322518628, -0.45765640053929046, 0.874175147097521 ],
          [ -1.5992262985137005, -1.1621387249649395, -2.2008644879867 ],
          [ 3.1418883228034438, 0.4216609533058631, 1.6917860199710848 ],
          [ -1.8409100156524267, -0.8793173538451536, 0.12341296194317945 ],
          [ 0.2056882699052991, -1.4295334758418285, -1.846052222400059 ],
          [ -1.3318315476368114, -0.6324914299587947, 0.8947439740880508 ],
          [ 0.8947439740880508, -0.26739475087688874, -1.8254833954095293 ],
          [ 2.84364033144076, 1.3986802353560337, 0.1388395821860769 ],
          [ -0.334243438596111, 0.8793173538451536, 0.8793173538451536 ],
          [ -2.098020353034051, -0.14398178893370933, 0.09255972145738457 ],
          [ -0.9101705943309485, -2.3448462769204097, 0.8536063201069911 ],
          [ 1.5940840917660677, -0.16455061592423925, -2.046598285557726 ],
          [ 0.15426620242897432, -0.5090784680156153, -0.6633446704445896 ],
          [ 0.22625709689582899, 0.19026164966240167, 0.43194536680112805 ],
          [ 1.7072126402139822, 2.709942956002315, 3.1830259767845037 ],
          [ -2.463117032115956, -3.3321499724658445, 3.054470808093691 ],
          [ 2.2368599352201275, -2.062024905800623, -0.3548122655866409 ],
          [ -1.8100567751666319, 3.9235037484435797, -1.4038224421036662 ],
          [ -1.6763593997281871, -0.046279860728692286, -2.540250133330444 ],
          [ -1.8563366358953244, -0.8690329403498885, -1.650648365990025 ],
          [ -3.614971343585631, 2.4785436523588538, -0.5913537759777349 ],
          [ 2.015745045071931, 0.3393856453437435, -1.861478842642957 ],
          [ -2.1288735935198453, 2.9619110866363063, -0.16455061592423925 ],
          [ 1.3421159611320765, -1.6866438132234525, 2.308850829686982 ],
          [ -3.589260309847469, -1.6455061592423927, -0.550216121996675 ],
          [ 2.2574287622106572, 1.8717632561382218, -0.2828213711197862 ],
          [ -0.7918998391354015, -0.24168371713872644, 0.344527852091376 ],
          [ 2.9207734326552472, -0.5656427422395724, -0.8176108728735639 ],
          [ -0.14398178893370933, 0.9101705943309485, 2.7407961964881102 ],
          [ -0.22625709689582899, 0.19540385641003413, -0.18511944291476914 ],
          [ 0.15426620242897432, -3.1881681835321354, -1.0387257630217603 ],
          [ 1.9386119438574438, 0.2005460631576666, -1.0490101765170254 ],
          [ 1.907758703371649, 0.334243438596111, -1.738065880699777 ],
          [ 0.010284413495264953, 2.272855382453555, 3.8772238877148877 ],
          [ -0.7096245311732818, -0.1285551686908119, -0.8793173538451536 ],
          [ -1.3112627206462815, 0.1748350294195042, 0.3599544723342734 ],
          [ 0.04113765398105981, 0.6993401176780168, 1.0952900372457175 ],
          [ -1.5478042310373754, 0.16969282267187175, 0.5450739152490426 ],
          [ 0.30853240485794864, 0.8793173538451536, 1.1724231384602049 ],
          [ 0.020568826990529906, 0.7456199784067092, -2.2471443487153926 ],
          [ -0.6119226029682647, 0.4062343330629657, -0.10284413495264955 ],
          [ 3.3938564534374347, -0.7096245311732818, -1.5066665770563157 ],
          [ -1.2546984464223245, 1.8923320831287513, 0.7199089446685468 ],
          [ -1.6403639524947602, 3.6663934110619563, -3.470989554651922 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.4629907341463333, 0.8709468121369399, 0.09737220410082445 ],
        [ 0.8052169377175956, 0.07159007820886543, 1.001755427221238 ],
        [ 0.4231122551672875, 0.9615652352746642, 0.5084384848118743 ],
        [ 0.84882904535214, 0.05010959126878883, 0.3551796091107473 ],
        [ 0.1320277591350725, 0.3613861606419659, 0.0649332746134402 ],
        [ 0.3293767023542863, 0.3981959986295721, 0.08386464217462344 ],
        [ 0.6760153761547744, 0.6053396559839902, 0.2145554990267438 ],
        [ 0.5074548572254536, 0.1433810381079153, 0.5998257999361667 ],
        [ 0.9946552985164393, 0.3527274670995293, 0.6716583215642202 ],
        [ 0.07267761011779544, 0.6784259564369888, 0.3509264588427025 ],
        [ 0.1227040779285768, 0.5350172105097376, -0.08238920079499228 ],
        [ 0.7615840492185494, 0.01458816688029711, 0.7141344086059969 ],
        [ 0.2423395148657141, 0.7626992889468149, 0.9547283308535561 ],
        [ 0.2099698549266694, 0.6626463533252523, 0.6069605634151344 ],
        [ 0.5708434209109231, 0.2040057468146391, 0.02895467120590782 ],
        [ 0.4800379699926824, 0.7999039633599564, 0.7766709568468907 ],
        [ 0.2750555225464565, 0.8024392288291817, 0.3548540422335518 ],
        [ 0.9038221397788629, 0.5500071407704038, 0.9235570341007846 ],
        [ 0.7171268530942633, 0.7521010480508729, 0.5889781886662023 ],
        [ 0.9106867520193067, 0.6532326217059155, 0.470541114915338 ],
        [ 0.6794234379330772, 0.06028528791986025, 0.3034837451849841 ],
        [ 0.6678969850893857, 0.2880020011311076, 0.6471161205875382 ],
        [ 0.4811185749467786, 0.2366871197212116, 0.3080970971043943 ],
        [ 0.4892092581928313, 0.670612351384294, 0.570448584485388 ],
        [ 0.5894422946400768, 0.655054410827244, 0.4159220760496482 ],
        [ 0.9864122222640396, 0.4113987745430793, 0.456874233027956 ],
        [ 0.8666867349140611, 0.8212043494743504, 0.726166529152567 ],
        [ 0.06496790938760992, 0.9409644715984988, 0.7664398445571479 ],
        [ 0.9056924175840292, 0.1405548405356641, 0.8382238775013637 ],
        [ 0.1417462767671033, 0.5874057699188957, 0.1126738473290184 ],
        [ 0.9035034998565012, 0.8525557470528049, 0.5212672051643483 ],
        [ 0.3109302216314795, 0.08934386344827733, 0.6698434593977255 ],
        [ 0.3896827711386485, 0.6842238176330041, 0.8825148267096351 ],
        [ 1.009271173216073, 0.8442156934327296, 0.05789548850214776 ],
        [ 0.335853405124029, 0.7220934797102045, 0.1507166832770676 ],
        [ 0.4797124031154868, 0.1247406026497579, 0.1728829387457051 ],
        [ -0.04115996562332639, 0.6674120982510094, 0.1384490462661435 ],
        [ 0.3116436979793763, 0.830119340345643, 0.6657911908198652 ],
        [ 0.03832684109624115, 0.1727097648748565, 0.6292376501611152 ],
        [ 0.57155689725882, 0.2707954453235777, 0.8327446562277097 ],
        [ 0.6222691335981623, 0.4828503136552658, 0.6372452099491606 ],
        [ 0.6708963565324859, 0.2781657252668996, 0.4030448670133365 ],
        [ 0.1582601370912383, 0.2084251439986987, 0.9395790806317091 ],
        [ 0.7893126494188482, 0.4736166828616115, 0.1604559817736002 ],
        [ 0.2563319636302916, 0.02099560010170015, 0.4088704360286878 ],
        [ 0.328476198225873, 0.6135758052815559, 0.4607048390511301 ],
        [ 0.1646537164029735, 0.06343012541447321, 0.04285706955764396 ],
        [ 0.7136495217676206, 0.4974731153097326, 0.463309374068695 ],
        [ 0.9770054175995366, 1.02049284004707, 0.1435957737077678 ],
        [ 0.7426734625218679, 0.2368187318630566, 0.08687786752739139 ],
        [ 0.8447975576387817, 0.3185567989036577, 0.2806317211877857 ],
        [ 0.6059907897383816, 0.9023674792637337, 0.6317244269465029 ],
        [ 0.8409669516156074, 0.3317526478623311, 0.7972786474778898 ],
        [ 0.1349924958040028, 0.9882270844305346, 0.5963831033836938 ],
        [ 0.2382110497846804, 0.9453215261890532, 0.8612421484145768 ],
        [ 0.2598854914601077, 0.2091524742562634, 0.4374649055832303 ],
        [ 0.06453843818790508, 0.2031260235507275, 0.4289793859116425 ],
        [ 0.3580681492765042, 0.4127633846453673, 0.27921862240166 ],
        [ 0.6072445685633264, 0.814180417272726, 0.1814446549204665 ],
        [ 0.5330083936078922, 0.08327585101373779, 0.7906079899727967 ],
        [ 0.4822338146750442, 0.5457609174571928, 0.1484931307753699 ],
        [ 0.1487909898332297, 0.4946399907826474, 0.3526651245060237 ],
        [ 0.9803095750553305, 0.6576866536641445, 0.775964407453828 ],
        [ 0.8761073934882323, 0.07943831803572991, 0.5490442940484846 ],
        [ 0.6161941942087886, 0.8989801983499326, 0.343085145970672 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  },
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/8/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -66079.54148885334,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.16410000000000036, -0.29690000000000083, -0.3140999999999998, 0.18369999999999997, -0.27139999999999986, 0.2522000000000002, 0.16329999999999956, 0.26869999999999994, 0.20699999999999985, -0.27009999999999934, -0.2797999999999998, -0.27829999999999977, 0.13860000000000028, 0.2610000000000001, 0.025699999999999612, 0.15139999999999976, 0.03340000000000032, -0.15140000000000065, -0.3796999999999997, 0.31789999999999985, 0.028699999999999726, -0.2644000000000002, 0.13339999999999996, 0.16220000000000034, 0.16819999999999968, -0.19009999999999927, 0.17889999999999961, 0.13279999999999959, 0.20980000000000043, 0.2964000000000002, -0.3310999999999993, -0.18249999999999922, 0.10379999999999967, 0.26529999999999987, -0.27369999999999983, 0.017599999999999838, -0.28529999999999944, -0.2645999999999997, 0.042500000000000426, 0.2575000000000003, 0.24340000000000028, -0.13170000000000037, 0.15869999999999962, 0.2206999999999999, 0.19010000000000016, -0.2850999999999999, 0.14149999999999974, -0.25900000000000034, -0.2674000000000003, 0.17379999999999995, -0.10249999999999915, 0.3334999999999999, -0.2688000000000006, 0.15920000000000023, -0.33949999999999925, 0.1882999999999999, -0.2867999999999995, -0.2835000000000001, 0.025900000000000034, -0.2638999999999996, -0.19870000000000054, 0.29710000000000036, 0.1897000000000002, 0.1830999999999996, 0.05119999999999969 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -2.555676753573341, 0.7610465986496067, 1.4912399568134185 ],
          [ 1.9386119438574438, 1.1518543114696747, -2.015745045071931 ],
          [ 1.8666210493905893, 1.3266893408891791, 1.1672809317125723 ],
          [ 0.2571103373816238, -1.8717632561382218, 0.23654151039109392 ],
          [ -0.5450739152490426, 1.013014729283598, -3.5275538288758788 ],
          [ 1.6609327794852904, -0.3496700588390084, -2.6585208885259908 ],
          [ -2.072309319295888, -2.7870760572168023, -1.228987412684162 ],
          [ -2.051740492305358, -0.1748350294195042, 0.49879405452035025 ],
          [ -2.596814407554401, -1.14156989797441, 1.9900340113337684 ],
          [ -1.7843457414284696, 1.861478842642957, -0.3702388858295383 ],
          [ 2.005460631576666, 0.3496700588390084, 4.288600427525486 ],
          [ 1.444960096084726, -0.5245050882585127, 4.057201123882024 ],
          [ 2.416837171387264, -1.3678269948702388, -0.9101705943309485 ],
          [ 0.7661888053972391, -1.7432080874474098, 2.889920192169452 ],
          [ -2.416837171387264, 0.9718770753025381, -0.15940840917660679 ],
          [ 0.7816154256401365, 1.7586347076903073, 0.8998861808356835 ],
          [ -1.316404927393914, -1.0644367967599226, 2.113446973276948 ],
          [ 2.514539099592281, -2.4116949646396315, -0.9513082483120082 ],
          [ -2.272855382453555, -0.8690329403498885, -2.2368599352201275 ],
          [ 0.689055704182752, 0.2056882699052991, -0.874175147097521 ],
          [ 3.2910123184847855, -1.1158588642362477, 0.5656427422395724 ],
          [ 1.4295334758418285, -0.4062343330629657, 0.7507621851543417 ],
          [ -1.357542581374974, -1.131285484479145, -1.9026164966240164 ],
          [ 2.6996585425070503, 0.42680316005349556, 1.4758133365705208 ],
          [ -1.6403639524947602, -0.8124686661259314, 0.03599544723342733 ],
          [ 0.21083047665293156, -1.2906938936557517, -1.6403639524947602 ],
          [ -1.14156989797441, -0.7250511514161793, 0.7918998391354015 ],
          [ 0.874175147097521, -0.2828213711197862, -1.563230851280273 ],
          [ 2.586529994059136, 1.187849758703102, 0.1748350294195042 ],
          [ -0.28796357786741866, 0.7918998391354015, 0.7250511514161793 ],
          [ -1.9026164966240164, -0.056564274223957246, 0.09770192820501707 ],
          [ -0.7610465986496067, -2.0311716653148286, 0.7713310121448715 ],
          [ 1.4141068555989311, -0.12341296194317945, -1.799772361671367 ],
          [ 0.18511944291476914, -0.3702388858295383, -0.5656427422395724 ],
          [ 0.1799772361671367, 0.07713310121448716, 0.46794081403455545 ],
          [ 1.6763593997281871, 2.3499884836680422, 2.643094268283093 ],
          [ -2.185437867743803, -2.900204605664717, 2.632809854787828 ],
          [ 1.9180431168669139, -1.8666210493905893, -0.31367461160558113 ],
          [ -1.542662024289743, 3.4504207276613923, -1.2804094801604866 ],
          [ -1.336973754384444, 0.10284413495264955, -2.185437867743803 ],
          [ -1.630079538999495, -0.8278952863688287, -1.3421159611320765 ],
          [ -3.167599356541606, 2.298566416191717, -0.44222978029639304 ],
          [ 1.7432080874474098, 0.3702388858295383, -1.650648365990025 ],
          [ -1.820341188661897, 2.4888280658541193, -0.1799772361671367 ],
          [ 1.1775653452078374, -1.563230851280273, 2.046598285557726 ],
          [ -3.1830259767845037, -1.4038224421036662, -0.4113765398105982 ],
          [ 2.0106028383242984, 1.6352217457471279, -0.3650966790819059 ],
          [ -0.7456199784067092, -0.18511944291476914, 0.32395902510084607 ],
          [ 2.504254686097016, -0.5862115692301024, -0.7661888053972391 ],
          [ -0.07199089446685467, 0.7353355649114441, 2.3808417241538367 ],
          [ -0.2056882699052991, 0.061706480971589726, -0.19026164966240167 ],
          [ 0.1748350294195042, -2.756222816731008, -0.9255972145738457 ],
          [ 1.7020704334663497, 0.19026164966240167, -0.9615926618072733 ],
          [ 1.444960096084726, 0.24168371713872644, -1.5323776107944782 ],
          [ -0.03599544723342733, 1.7792035346808373, 3.3527187994563743 ],
          [ -0.5605005354919399, -0.14912399568134183, -0.8536063201069911 ],
          [ -1.208418585693632, 0.11312854844791449, 0.28796357786741866 ],
          [ 0.05142206747632477, 0.5810693624824698, 0.9770192820501706 ],
          [ -1.3524003746273414, 0.020568826990529906, 0.4885096410250853 ],
          [ 0.2725369576245213, 1.1261432777315123, 1.1261432777315123 ],
          [ -0.05142206747632477, 0.6324914299587947, -1.995176218081401 ],
          [ -0.3702388858295383, 0.38052329932480333, -0.16969282267187175 ],
          [ 2.889920192169452, -0.6839134974351194, -1.2649828599175894 ],
          [ -1.0952900372457175, 1.7329236739521447, 0.5964959827253673 ],
          [ -1.5220931972992133, 3.3784298331945375, -3.126461702560546 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.4715732311855965, 0.8644216206833597, 0.108898656944516 ],
        [ 0.8152818030913238, 0.05621916543233203, 0.9999751998289124 ],
        [ 0.4161645194688365, 0.9619185099711954, 0.508895663830915 ],
        [ 0.8627660784780457, 0.03487721758893443, 0.3547293570465407 ],
        [ 0.132228640825257, 0.3542791049823338, 0.05628150802583759 ],
        [ 0.3313162497077921, 0.3769025394700122, 0.07533063381919801 ],
        [ 0.6774423288505678, 0.6030399069791192, 0.2242463088394387 ],
        [ 0.5088125403729076, 0.1510145423349274, 0.5903081639943205 ],
        [ 0.9934153736011625, 0.3524019002223337, 0.68069107066769 ],
        [ 0.06129662332561685, 0.6875141211791301, 0.340633003959454 ],
        [ 0.1233205769087984, 0.5331469327045714, -0.08854726364237314 ],
        [ 0.7581344257112427, 0.01909068752236411, 0.7127420906843732 ],
        [ 0.2326002163691816, 0.7762761204213557, 0.9621748073000516 ],
        [ 0.2080441614828315, 0.6571602050967645, 0.632811958855433 ],
        [ 0.5798623161047249, 0.2118886214156734, 0.04112533084915664 ],
        [ 0.4676941364785849, 0.7940368326156014, 0.7813951400436439 ],
        [ 0.2673042600872673, 0.7917301566558964, 0.3594050515594564 ],
        [ 0.9011760430322943, 0.5447703629159382, 0.9212988468249169 ],
        [ 0.7078170257974353, 0.7526274966182529, 0.5894769294142466 ],
        [ 0.9237786966554706, 0.6606029016492374, 0.4834044700419818 ],
        [ 0.6929309998592784, 0.05484070142037614, 0.3000687564518472 ],
        [ 0.6767911950961768, 0.2985794611625481, 0.6531564252027419 ],
        [ 0.4869095091879601, 0.2504786867956046, 0.324119143635319 ],
        [ 0.48364691346117, 0.6657634830005293, 0.5699221359180079 ],
        [ 0.5891998512208886, 0.6657011404070239, 0.4238188045603505 ],
        [ 0.9869109630120843, 0.4132067097547401, 0.4510971526964426 ],
        [ 0.8582912656553148, 0.8241552322336129, 0.7251136320178064 ],
        [ 0.0643444834525545, 0.9492421826250683, 0.773602315855451 ],
        [ 0.905068991648974, 0.1276222158606808, 0.8334442786659388 ],
        [ 0.1410466543288745, 0.5795852379113671, 0.1115586076007525 ],
        [ 0.8923926643028469, 0.8590185959128793, 0.5216066259512118 ],
        [ 0.3050838717516264, 0.095799785353518, 0.6556916906719673 ],
        [ 0.3734182811885357, 0.6829977466273952, 0.8858189841654289 ],
        [ 1.022799516006775, 0.8345525914393706, 0.02337154560974473 ],
        [ 0.3378068063872027, 0.7195443603313115, 0.1526631575854074 ],
        [ 0.506969970387077, 0.1330183136763273, 0.1904912579336042 ],
        [ -0.03952520428251437, 0.6698780941718951, 0.1253778824944813 ],
        [ 0.3034214025914787, 0.8345872262135405, 0.6672943400188324 ],
        [ 0.03468326285358385, 0.1776486836714622, 0.6365317336012637 ],
        [ 0.5716330937619932, 0.2751802077334676, 0.831761028641289 ],
        [ 0.6414706523978696, 0.4940304187572599, 0.6348761913959499 ],
        [ 0.6856161355546281, 0.2827998580508118, 0.4008698031954765 ],
        [ 0.1283841808924152, 0.1976606561867416, 0.9338712698485351 ],
        [ 0.8072950241677802, 0.4910102664496581, 0.1633168141200213 ],
        [ 0.2424642000527253, 0.009725444586864735, 0.407083281681529 ],
        [ 0.3102513800577526, 0.6071268103311492, 0.4757432579956339 ],
        [ 0.1562097584603894, 0.06629095776089425, 0.04473427431764421 ],
        [ 0.720680380924079, 0.5031047295897335, 0.4539094963590258 ],
        [ 0.987063356018431, 0.993616255291347, 0.1358445112485786 ],
        [ 0.7555298906936777, 0.2284301895591442, 0.07706929948251925 ],
        [ 0.8628284210715511, 0.3340662507768701, 0.2752009885979694 ],
        [ 0.597872398672993, 0.9079575318147307, 0.6330059135907834 ],
        [ 0.8434537284009955, 0.3225952135718502, 0.8091168132891091 ],
        [ 0.128966045098467, 0.9859966049740029, 0.6027489748760932 ],
        [ 0.241141151679441, 0.9570557876777631, 0.8586861020808495 ],
        [ 0.2528199975294794, 0.1984018403539741, 0.4157350482691316 ],
        [ 0.05898302041107779, 0.2001820677462991, 0.4326991606574733 ],
        [ 0.3618571935706745, 0.41159272927843, 0.2651153423597393 ],
        [ 0.6175865121304125, 0.8106961589912496, 0.1922022157775896 ],
        [ 0.5306740098288514, 0.09019587889285308, 0.7777861965751566 ],
        [ 0.4926381008356361, 0.5422558783112146, 0.1394603816719001 ],
        [ 0.1400491728327858, 0.5020518324549731, 0.3457450966269085 ],
        [ 0.9703555409589455, 0.6614202823196432, 0.7813258704953046 ],
        [ 0.8659801855209982, 0.08606048685698539, 0.5469107919596286 ],
        [ 0.6226154813398597, 0.8963410285581979, 0.3519100864291234 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  },
  {
    "vectors": {
      "_type": "numpy",
      "data": [
        [ 14.436358024148879, 0.0, 0.0 ],
        [ 0.0, 14.436358024148879, 0.0 ],
        [ 0.0, 0.0, 14.436358024148879 ]
      ],
      "complex": false,
      "units": "angstrom"
    },
    "meta": {
      "source-file-name": "../../data/dft/ml-data/openmx-small/fixed-grid-0/9/openmx.dat",
      "total-energy": {
        "_type": "numpy",
        "data": -66079.9734702407,
        "complex": false,
        "units": "eV"
      },
      "charges": {
        "_type": "numpy",
        "data": [ 0.16659999999999986, -0.3031000000000006, -0.30569999999999986, 0.1607000000000003, -0.2771000000000008, 0.2549000000000001, 0.17600000000000016, 0.2668999999999997, 0.21480000000000032, -0.2591999999999999, -0.2741000000000007, -0.2657000000000007, 0.12990000000000013, 0.2477999999999998, 0.0246000000000004, 0.15620000000000012, 0.02319999999999922, -0.1465999999999994, -0.3661999999999992, 0.3139000000000003, 0.03840000000000021, -0.25259999999999927, 0.13780000000000037, 0.14649999999999963, 0.17110000000000003, -0.18950000000000067, 0.17579999999999973, 0.13729999999999976, 0.19420000000000037, 0.30900000000000016, -0.3415999999999997, -0.18740000000000023, 0.10280000000000022, 0.2386999999999997, -0.2680000000000007, 0.03469999999999995, -0.2807999999999993, -0.26069999999999993, 0.0669000000000004, 0.2427999999999999, 0.26419999999999977, -0.1266999999999996, 0.15700000000000003, 0.20009999999999994, 0.1759000000000004, -0.2942, 0.1487999999999996, -0.2607999999999997, -0.2569999999999997, 0.18240000000000034, -0.12449999999999939, 0.33640000000000025, -0.2721999999999998, 0.16709999999999958, -0.34220000000000006, 0.18599999999999994, -0.28470000000000084, -0.2845999999999993, 0.03249999999999975, -0.25210000000000043, -0.20449999999999946, 0.3072999999999997, 0.17220000000000013, 0.17330000000000023, 0.04659999999999975 ],
        "complex": false,
        "units": null
      },
      "forces": {
        "_type": "numpy",
        "data": [
          [ -2.4888280658541193, 0.689055704182752, 1.6197951255042302 ],
          [ 1.7792035346808373, 0.9718770753025381, -1.7792035346808373 ],
          [ 1.6866438132234525, 1.187849758703102, 0.9564504550596407 ],
          [ 0.29824799136268365, -1.4758133365705208, 0.09255972145738457 ],
          [ -0.26739475087688874, 1.2495562396746918, -3.1624571497939735 ],
          [ 1.4192490623465637, -0.2725369576245213, -2.3448462769204097 ],
          [ -1.846052222400059, -2.4322637916301617, -1.187849758703102 ],
          [ -1.8769054628858541, -0.1285551686908119, 0.45765640053929046 ],
          [ -2.2060066947343326, -1.1107166574886151, 1.7792035346808373 ],
          [ -1.563230851280273, 1.6557905727376574, -0.28796357786741866 ],
          [ 1.712354846961615, 0.2931057846150512, 3.9697836091722722 ],
          [ 1.2546984464223245, -0.49879405452035025, 3.568691482856939 ],
          [ 2.175153454248538, -1.1724231384602049, -0.7559043919019741 ],
          [ 0.678771290687487, -1.5940840917660677, 2.4528326186206915 ],
          [ -2.2008644879867, 0.8947439740880508, -0.13369737543844437 ],
          [ 0.6273492232111623, 1.6403639524947602, 0.7559043919019741 ],
          [ -1.2238452059365295, -0.7353355649114441, 1.861478842642957 ],
          [ 2.0414560788100933, -2.2162911082295977, -0.7404777716590766 ],
          [ -2.0003184248290333, -0.8381796998640936, -2.026029458567196 ],
          [ 0.5964959827253673, 0.12341296194317945, -0.7301933581638118 ],
          [ 2.9413422596457766, -1.0644367967599226, 0.5399317085014101 ],
          [ 1.2649828599175894, -0.3650966790819059, 0.6427758434540597 ],
          [ -1.1621387249649395, -1.0644367967599226, -1.650648365990025 ],
          [ 2.3499884836680422, 0.44222978029639304, 1.2958361004033843 ],
          [ -1.4398178893370936, -0.776473218892504, -0.05142206747632477 ],
          [ 0.21597268340056403, -1.1724231384602049, -1.4603867163276236 ],
          [ -0.9924459022930681, -0.786757632387769, 0.7147667379209143 ],
          [ 0.8638907336022561, -0.29824799136268365, -1.3524003746273414 ],
          [ 2.370557310658572, 1.023299142778863, 0.2056882699052991 ],
          [ -0.2571103373816238, 0.6993401176780168, 0.570784948987205 ],
          [ -1.7277814672045122, -0.015426620242897432, 0.09770192820501707 ],
          [ -0.6222070164635298, -1.7586347076903073, 0.6839134974351194 ],
          [ 1.2546984464223245, -0.09770192820501707, -1.6043685052613328 ],
          [ 0.19540385641003413, -0.23654151039109392, -0.46794081403455545 ],
          [ 0.1748350294195042, -0.061706480971589726, 0.5399317085014101 ],
          [ 1.6197951255042302, 1.9746073910908712, 2.2060066947343326 ],
          [ -1.969465184343239, -2.529965719835179, 2.288282002696452 ],
          [ 1.6763593997281871, -1.7226392604568799, -0.2725369576245213 ],
          [ -1.3215471341415466, 3.0390441878507937, -1.1775653452078374 ],
          [ -1.0387257630217603, 0.2725369576245213, -1.846052222400059 ],
          [ -1.4295334758418285, -0.7970420458830338, -1.1107166574886151 ],
          [ -2.7767916437215376, 2.1340158002674783, -0.30853240485794864 ],
          [ 1.5272354040468454, 0.3650966790819059, -1.4603867163276236 ],
          [ -1.552946437785008, 2.092878146286418, -0.1748350294195042 ],
          [ 1.05929459001229, -1.444960096084726, 1.8357678089047944 ],
          [ -2.8230715044502297, -1.2444140329270597, -0.334243438596111 ],
          [ 1.8100567751666319, 1.424391269094196, -0.4370875735487605 ],
          [ -0.678771290687487, -0.11827075519554696, 0.2828213711197862 ],
          [ 2.1288735935198453, -0.5913537759777349, -0.7199089446685468 ],
          [ -0.030853240485794863, 0.6067803962206323, 2.072309319295888 ],
          [ -0.19026164966240167, -0.10284413495264955, -0.1748350294195042 ],
          [ 0.2005460631576666, -2.385983930901469, -0.8433219066117262 ],
          [ 1.4963821635610508, 0.1748350294195042, -0.874175147097521 ],
          [ 1.0850056237504528, 0.16455061592423925, -1.3061205138986491 ],
          [ -0.046279860728692286, 1.3729692016178714, 2.853924744936025 ],
          [ -0.44222978029639304, -0.14912399568134183, -0.8381796998640936 ],
          [ -1.131285484479145, 0.04113765398105981, 0.22625709689582899 ],
          [ 0.061706480971589726, 0.49879405452035025, 0.8947439740880508 ],
          [ -1.2135607924412646, -0.07713310121448716, 0.45765640053929046 ],
          [ 0.22625709689582899, 1.2906938936557517, 1.0798634170028203 ],
          [ -0.1285551686908119, 0.5450739152490426, -1.7792035346808373 ],
          [ -0.19026164966240167, 0.3599544723342734, -0.22625709689582899 ],
          [ 2.447690411873059, -0.6530602569493246, -1.069579003507555 ],
          [ -0.9718770753025381, 1.6197951255042302, 0.4936518477727178 ],
          [ -1.424391269094196, 3.1316039093081787, -2.8230715044502297 ]
        ],
        "complex": false,
        "units": "eV/angstrom"
      }
    },
    "coordinates": {
      "_type": "numpy",
      "data": [
        [ 0.4637319183135658, 0.8559499549214397, 0.1158948813268048 ],
        [ 0.8132383514153089, 0.05609448024532096, 0.9952025279483213 ],
        [ 0.4167879454038918, 0.9704525183266205, 0.513405111427816 ],
        [ 0.8625513428781935, 0.02614232754332444, 0.3719497667637385 ],
        [ 0.1334339309663642, 0.3564403148905261, 0.05151576310008051 ],
        [ 0.3348282158086046, 0.3820769747309722, 0.07076577058362546 ],
        [ 0.6751287259360289, 0.5821482111999282, 0.2388829644035735 ],
        [ 0.5065543530970401, 0.1636908696810545, 0.585563199933065 ],
        [ 0.9927365320274357, 0.359599006294807, 0.6902294874740381 ],
        [ 0.06460078078141061, 0.684937293980901, 0.3282891704453564 ],
        [ 0.1295894710335224, 0.5206022175002891, -0.09777396748119352 ],
        [ 0.7529807713147841, 0.01238539524310124, 0.7050947325476933 ],
        [ 0.2152274136456369, 0.7780355669491789, 0.9646615840854392 ],
        [ 0.2115422736739759, 0.6539391710989781, 0.6584416917410452 ],
        [ 0.6005531301937315, 0.225022127780841, 0.04015555717240375 ],
        [ 0.4555234768353362, 0.79641970507848, 0.7912383428626861 ],
        [ 0.2674358722291124, 0.7787421163422418, 0.363138680214955 ],
        [ 0.9118989691152478, 0.5531796860843524, 0.9048958177781249 ],
        [ 0.7107263468276941, 0.7490808957432711, 0.5941041352433246 ],
        [ 0.9408536403211556, 0.6615034057776507, 0.4820052251655241 ],
        [ 0.699663999957877, 0.05178591433860451, 0.2962520043383412 ],
        [ 0.6825474945631885, 0.3018004951603346, 0.66134408581647 ],
        [ 0.4996481791275926, 0.2599478340536132, 0.3280467270261682 ],
        [ 0.475466179802276, 0.6561696505555098, 0.5789548850214776 ],
        [ 0.5783383860412561, 0.6691161291401609, 0.4339806473017539 ],
        [ 0.9888089486365863, 0.4181109937771761, 0.4546160457520886 ],
        [ 0.8624405116008502, 0.8236080028017311, 0.7291035580021613 ],
        [ 0.06480166247159515, 0.9547698925825596, 0.774613651261208 ],
        [ 0.9032818373018148, 0.1145510520890186, 0.8233101437438709 ],
        [ 0.1358306573389106, 0.5831734005153526, 0.09786401789403486 ],
        [ 0.896735864983733, 0.8536432789617346, 0.5254926476130573 ],
        [ 0.3042249293522167, 0.1027336671423012, 0.6553453429302699 ],
        [ 0.3607696616617444, 0.6840644976718235, 0.8945123124820354 ],
        [ 1.003210087736367, 0.8311237487965658, -0.008097610200886665 ],
        [ 0.329833881373327, 0.7107402007373617, 0.1502941390321967 ],
        [ 0.524439750478297, 0.1487425011493921, 0.1909415099978109 ],
        [ -0.04542004284620517, 0.664745220639939, 0.1023041959425964 ],
        [ 0.2963004930221788, 0.8345802992587064, 0.6663799819807511 ],
        [ 0.03680291103277232, 0.1880806776513897, 0.6390185103866515 ],
        [ 0.5697004733633213, 0.2733791994766408, 0.8401842057193714 ],
        [ 0.6572502555096058, 0.496870470239179, 0.6451350115050287 ],
        [ 0.6976344021915302, 0.2901978458134696, 0.4144812694441868 ],
        [ 0.1201133968206798, 0.204566830156189, 0.9227604342948803 ],
        [ 0.8028063574353812, 0.4843396089445649, 0.1558634107186919 ],
        [ 0.2391531156420975, 0.007301010394982499, 0.4122023013038174 ],
        [ 0.3019598151215154, 0.597325169241111, 0.490608503069289 ],
        [ 0.1551360804611272, 0.07483189307115368, 0.04077205615262524 ],
        [ 0.7193088438669569, 0.511624884035491, 0.4559737288995428 ],
        [ 0.989370031978136, 0.9853523981744453, 0.1149320346048858 ],
        [ 0.78115962357929, 0.2357727616831303, 0.07050254629993537 ],
        [ 0.86633346021753, 0.3343017672412243, 0.2757066563008477 ],
        [ 0.5918043862384534, 0.9006357405552462, 0.635541179060009 ],
        [ 0.8455456687608478, 0.3121978543660923, 0.8185651796826157 ],
        [ 0.1332053414568439, 0.9895362788941509, 0.601959302025023 ],
        [ 0.2419585323498469, 0.9524701435776886, 0.860023004363802 ],
        [ 0.2497028678542023, 0.1953470532722025, 0.411308724130238 ],
        [ 0.05507621788473041, 0.2037771573051188, 0.4347010506044846 ],
        [ 0.3631594610794568, 0.4055662785728941, 0.2634320923350896 ],
        [ 0.605256532525983, 0.7981514437869672, 0.2044352180143439 ],
        [ 0.5257281640774116, 0.09292509909742906, 0.7700141532514656 ],
        [ 0.493351577183533, 0.5408219986605871, 0.1433464033337456 ],
        [ 0.1401045884714574, 0.5009227388170394, 0.3490492540827023 ],
        [ 0.9892176389717893, 0.6793264605654021, 0.7791646605871125 ],
        [ 0.8676634355456481, 0.09293202605226301, 0.5476450491720269 ],
        [ 0.6159101890605969, 0.9005456901424049, 0.3514806152294185 ]
      ],
      "complex": false,
      "units": null
    },
    "values": {
      "_type": "numpy",
      "data": [ "se", "bi", "bi", "se", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "se", "se", "bi", "bi", "bi", "se", "se", "bi", "se", "se", "se", "bi", "se", "se", "se", "se", "bi", "bi", "se", "se", "bi", "se", "bi", "bi", "se", "se", "se", "bi", "se", "se", "se", "bi", "se", "bi", "bi", "se", "bi", "se", "bi", "se", "bi", "se", "bi", "bi", "se", "bi", "bi", "se", "se", "se", "se" ],
      "complex": false,
      "units": null
    },
    "type": "dfttools.utypes.CrystalCell"
  }
]
"""

yaml_main_sample = """
fit:
  init:
    seed: 0
    units: default
  prepare:
    fn_cells: {fn_cells}
    fn_cells_root: {fn_cells_root}
  run:
    n_epochs: 1
    save: True
    save_fn: {potential}

test-direct:
  init:
    units: default
  prepare:
    fn_cells: {fn_cells}
    fn_cells_root: {fn_cells_root}
    potentials: {potential}
"""