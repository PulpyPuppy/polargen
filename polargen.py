import os
import sys
import ctypes
import struct
import argparse
import aerosandbox as asb
import aerosandbox.numpy as np

# This bitch is fragile as fuck

MACH   = [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
RE     = [5e5, 1e6, 3e6, 7e6, 1.5e7, 3e7, 5e7]
A_MIN  = -180
A_MAX  = 180
A_STEP = 0.5
A_SEQ  = np.arange(A_MIN, A_MAX, A_STEP)

def running_as_sudo() -> bool:
    if os.name == 'nt':
        return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return os.getuid() == 0

def encode_f32(val):
    return struct.pack("f", val)

def encode_i64(val):
    return val.to_bytes(8, byteorder="little")

def encode_str(s):
    sbyte = s.encode("utf-8")
    return encode_i64(len(sbyte)) + sbyte

def save_bincode(foil_name, out_path, data):
    with open(out_path, "wb") as f:
        # Write airfoil codename
        f.write(encode_str(foil_name))

        # Write array of Alpha values
        f.write(encode_i64(len(A_SEQ)))
        f.write(bytes().join(map(encode_f32, A_SEQ)))

        # Write array of Mach values
        f.write(encode_i64(len(MACH)))
        f.write(bytes().join(map(encode_f32, MACH)))

        # Write array of Reynolds values
        f.write(encode_i64(len(RE)))
        f.write(bytes().join(map(encode_f32, RE)))

        # Write the data: Cl, Cd, Cm
        for (mach, re_data) in data:
             for (_, cl, cd, cm) in re_data:
                 f.write(encode_i64(len(cl)))
                 f.write(bytes().join(map(encode_f32, cl)))
                 f.write(encode_i64(len(cd)))
                 f.write(bytes().join(map(encode_f32, cd)))
                 f.write(encode_i64(len(cm)))
                 f.write(bytes().join(map(encode_f32, cm)))

def process_foil(foil_name, out_dir):
    af = asb.Airfoil(foil_name)

    out_file = f"{foil_name}_polar_overg.bincode"
    out_path = os.path.join(out_dir, out_file)
    data = []

    for mach in MACH:
        re_data = []
        for re in RE:
            try:
                aero = af.get_aero_from_neuralfoil(
                    alpha=A_SEQ,
                    Re=re,
                    mach=mach,
                    model_size="xxxlarge",
                )
            except Exception as e:
                print(e)
                print(f"ERROR: Couldn't process {foil_name} airfoil. Skipping.")
                return
            cl = aero["CL"]
            cd = aero["CD"]
            cm = aero["CM"]
            re_data.append((re, cl, cd, cm))
        data.append((mach, re_data))
    save_bincode(foil_name, out_path, data)
    print(f"OK: {foil_name}")

def process(in_file, out_dir):
    with open(in_file) as f:
        foils = [l.rstrip() for l in f]

    for foil in foils:
        process_foil(foil, out_dir)

def main():
    if running_as_sudo():
        print("This should not run under root")
        exit(1)

    parser = argparse.ArgumentParser(description="Populates airfoil polar data files for the full range of angles of attack")
    parser.add_argument("input", help="TXT file listing airfoil UIUC codenames")
    parser.add_argument("output", help="Directory to write result files to")

    args = parser.parse_args()
    in_file, out_dir = args.input, args.output

    if not os.path.exists(in_file) or not os.path.isfile(in_file):
        print("Provided input path doesn't exist or is not a file")
        exit(1)
    if not os.path.exists(out_dir) or not os.path.isdir(out_dir):
        print("Provided output path doesn't exist or is not a directory")
        exit(1)

    process(in_file, out_dir)

if __name__ == "__main__":
    main()
