This small utility reads a list of UIUC airfoil codenames:

```
naca2412
naca0010
raf15
clarky
...
```

Calculates Cl, Cd, Cm coefficients across specified ranges of angles of attack
[-180; 180), Reynolds numbers, and Mach numbers using
[AeroSandbox](https://github.com/peterdsharpe/AeroSandbox) and
[NeuralFoil](https://github.com/peterdsharpe/NeuralFoil). 
Parameters are configurable directly in the `.py` file.

The utility generates a binary file for each airfoil with the following
structure:

```
<airfoil-name_[u8]>             // length: NAME_SIZE
<cl_[f32]><cd_[f32]><cm_[f32]>  // array of ALPHA_N values per condition
<cl_[f32]><cd_[f32]><cm_[f32]>
...
<cl_[f32]><cd_[f32]><cm_[f32]>  // total blocks: len(RE) * len(MACH)
```

Where each `(Cl, Cd, Cm)` block corresponds to a `(mach_i, re_j)` pair, 
and individual elements within a block correspond to angle of attack `alpha_k`.
