import math

# Persamaan non-linear: potensial kesetimbangan membran
# f(V) = 58.2 * log10(140 / V) - 25 = 0

def f(V):
    return 58.2 * math.log10(140.0 / V) - 25.0

def fprime(V):
    return -58.2 / (V * math.log(10))

def g(V):
    # bentuk iterasi titik tetap: g(V) = V + f(V)
    return V + f(V)

tol = 1e-6       # toleransi error (%)
max_iter = 20    # maksimum iterasi


def print_table(title, hist):
    print(f"\n=== {title} ===")
    print(f"{'k':>3} | {'V (mV)':>15} | {'Error (%)':>15}")
    print("-" * 40)
    for k, V, err in hist:
        err_str = "-" if err is None else f"{err:.6f}"
        print(f"{k:>3} | {V:>15.6f} | {err_str:>15}")


# a. Simple Fixed-Point Iteration
def fixed_point(V0):
    hist = [(0, V0, None)]
    V = V0
    for k in range(1, max_iter + 1):
        V_next = g(V)
        err = abs((V_next - V) / V_next) * 100
        hist.append((k, V_next, err))
        if err < tol:
            break
        V = V_next
    return hist


# b. Newton-Raphson Method
def newton_raphson(V0):
    hist = [(0, V0, None)]
    V = V0
    for k in range(1, max_iter + 1):
        V_next = V - f(V) / fprime(V)
        err = abs((V_next - V) / V_next) * 100
        hist.append((k, V_next, err))
        if err < tol:
            break
        V = V_next
    return hist


# c. Secant Method
def secant(V0, V1):
    hist = [(0, V0, None), (1, V1, abs((V1 - V0) / V1) * 100)]
    for k in range(2, max_iter + 1):
        f0, f1 = f(V0), f(V1)
        V_next = V1 - f1 * (V1 - V0) / (f1 - f0)
        err = abs((V_next - V1) / V_next) * 100
        hist.append((k, V_next, err))
        if err < tol:
            break
        V0, V1 = V1, V_next
    return hist


# d. Brent's Method
def brent(a, b):
    fa, fb = f(a), f(b)
    if abs(fa) < abs(fb):
        a, b = b, a
        fa, fb = fb, fa
    c, fc = a, fa
    mflag = True
    d = 0
    hist = [(0, b, None)]

    for k in range(1, max_iter + 1):
        if fa != fc and fb != fc:
            s = (a * fb * fc) / ((fa - fb) * (fa - fc)) \
                + (b * fa * fc) / ((fb - fa) * (fb - fc)) \
                + (c * fa * fb) / ((fc - fa) * (fc - fb))
        else:
            s = b - fb * (b - a) / (fb - fa)

        cond1 = not ((3 * a + b) / 4 <= s <= b or b <= s <= (3 * a + b) / 4)
        cond2 = mflag and abs(s - b) >= abs(b - c) / 2
        cond3 = (not mflag) and abs(s - b) >= abs(c - d) / 2
        cond4 = mflag and abs(b - c) < tol
        cond5 = (not mflag) and abs(c - d) < tol

        if cond1 or cond2 or cond3 or cond4 or cond5:
            s = (a + b) / 2
            mflag = True
        else:
            mflag = False

        fs = f(s)
        err = abs((s - b) / s) * 100.0
        hist.append((k, s, err))

        if abs(fs) < 1e-12 or err < tol:
            break

        d = c
        c, fc = b, fb
        if fa * fs < 0:
            b, fb = s, fs
        else:
            a, fa = s, fs
        if abs(fa) < abs(fb):
            a, b = b, a
            fa, fb = fb, fa

    return hist


# Jalankan semua metode
if __name__ == "__main__":
    print_table("1. Fixed-Point Iteration (V0 = 30)", fixed_point(30.0))
    print_table("2. Newton-Raphson Method (V0 = 30)", newton_raphson(30.0))
    print_table("3. Secant Method (V0 = 30, V1 = 50)", secant(30.0, 50.0))
    print_table("4. Brent's Method (a = 20, b = 100)", brent(20.0, 100.0))