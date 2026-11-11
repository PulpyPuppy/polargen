This small utility reads a list of UIUC airfoil codenames:

```
naca2412
naca0010
raf15
clarky
...
```

Calculates Cl, Cd, Cm coefficients for a range of angles of attack [-180; 180)
at a range of Reynolds numbers at a range of Mach numbers using
[AeroSandbox](https://github.com/peterdsharpe/AeroSandbox)/
[NeuralFoil](https://github.com/peterdsharpe/NeuralFoil).
The numbers are configurable, just enter your ones in the .py file.
The result is a Bincode file for each airfoil. The structure is:

```
<size_u64><airfoil-codename_utf8>
<size_u64><alpha-values_f32>
<size_u64><mach_values_f32>
<size_u64><re_values_f32>
<size_u64><cl_f32><size_u64><cd_f32><size_u64><cm_f32>
<size_u64><cl_f32><size_u64><cd_f32><size_u64><cm_f32>
<size_u64><cl_f32><size_u64><cd_f32><size_u64><cm_f32>
...
<size_u64><cl_f32><size_u64><cd_f32><size_u64><cm_f32>
```

Where (cl, cd, cm)_ij is associated with (mach_i, re_j)
And cl_i, cd_i, cm_i are associated with alpha_i
