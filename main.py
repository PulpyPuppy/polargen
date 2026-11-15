import os
import ctypes
import struct
import argparse
import aerosandbox as asb
import aerosandbox.numpy as np

NAME_SIZE   = 32
MACH        = [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
RE          = [5e5, 1e6, 3e6, 7e6, 1.5e7, 3e7, 5e7]
ALPHA_MIN   = -180
ALPHA_MAX   = 180
ALPHA_N     = 720
ALPHA_SEQ   = np.linspace(ALPHA_MIN, ALPHA_MAX, ALPHA_N)

def running_as_sudo() -> bool:
    if os.name == 'nt':
        return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return os.getuid() == 0

def encode_f32(val):
    return struct.pack("f", val)

def encode_str(s):
    return s.encode("utf-8")

def save_bincode(data, af_name, out_path):
    with open(out_path, "wb") as f:
        # Write airfoil name
        name_enc = encode_str(af_name.strip())
        if len(name_enc) > NAME_SIZE:
            name_enc = name_enc[:NAME_SIZE]
        elif len(name_enc) < NAME_SIZE:
            name_enc = name_enc + encode_str(" " * (NAME_SIZE - len(name_enc)))
        f.write(name_enc)

        # Write the data: Cl, Cd, Cm
         for (cl, cd, cm) in re_data:
             f.write(bytes().join(map(encode_f32, cl)))
             f.write(bytes().join(map(encode_f32, cd)))
             f.write(bytes().join(map(encode_f32, cm)))

def process_airfoil(codename):
    airfoil = asb.Airfoil(codename)
    data = []

    for mach in MACH:
        for re in RE:
            try:
                aero = airfoil.get_aero_from_neuralfoil(
                    alpha=ALPHA_SEQ,
                    Re=re,
                    mach=mach,
                    model_size="xxxlarge",
                )
            except Exception as e:
                print(f"ERROR: Couldn't process airfoil: {codename}.")
                print(e)
                return None
            data.append(aero["CL"])
            data.append(aero["CD"])
            data.append(aero["CM"])

    print(f"Processed airfoil {codename}. Saving...")
    return data

def process(in_file, out_dir):
    with open(in_file) as f:
        af_codenames = [l.rstrip() for l in f]

    for codename in af_codenames:
        data = process_airfoil(codename)
        if not data:
            continue

        out_file = f"{codename}_polar.bin"
        out_path = os.path.join(out_dir, out_file)

        # Should fetch airfoil names but I'm lazy
        save_bincode(data, codename, out_path)

def main():
    if running_as_sudo():
        print("This should not run under root")
        exit(1)

    parser = argparse.ArgumentParser(
            description="This tool creates airfoil polar binary files for OVER-G game.")
    parser.add_argument("input", help="UIUC airfoil codenames listing TXT input file")
    parser.add_argument("output", help="Output directory")
    parser.add_argument("-g", action='ignore_nonempty' help="Ignore directory non-emptiness")
    args = parser.parse_args()

    in_file, out_dir = args.input, args.output

    if not os.path.exists(in_file) or not os.path.isfile(in_file):
        print("Argument error: input path doesn't exist or is not a file.")
        exit(1)
    if not os.path.exists(out_dir) or not os.path.isdir(out_dir):
        print("Argument error: output path doesn't exist or is not a directory.")
        exit(1)

    if not parger.ignore_nonempty:
        for _ in os.scandir(out_dir):
            print("Output directory is not empty.")
            print("Script overwrites files when name collisions.")
            print("Turn on -g flag to ignore.")
            exit(0)

    process(in_file, out_dir)
    exit(0)

if __name__ == "__main__":
    main()
