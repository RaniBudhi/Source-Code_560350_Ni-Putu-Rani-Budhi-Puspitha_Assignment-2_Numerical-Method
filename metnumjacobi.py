"""
Metode Jacobi

KASUS (parameter hipotetis):
I = 0,5 mA diinjeksikan lewat elektroda di permukaan kulit. 
Jaringan dimodelkan sebagai jaringan resistif 4 simpul dengan tegangan simpul (V):
  V1 = kulit (di bawah elektroda), 
  V2 = lemak subkutan,
  V3 = otot,                       
  V4 = jaringan dalam/tulang.

RUMUS JACOBI (hanya memakai nilai iterasi SEBELUMNYA):
    x_i^(k+1) = ( b_i - sum_{j != i} a_ij * x_j^(k) ) / a_ii
"""
import numpy as np

A = np.array([[ 3.5, -2.0, -1.0,  0.0],
              [-2.0,  7.3, -3.0, -1.5],
              [-1.0, -3.0,  7.2, -2.0],
              [ 0.0, -1.5, -2.0,  5.5]])
b = np.array([0.5, 0, 0, 0])
NAMA = ["V1", "V2", "V3", "V4"]
G_GND = np.array([0.5, 0.8, 1.2, 2.0])   # konduktansi ke referensi (mS)

x0 = np.zeros(4)
TOL = 1e-6
MAX_ITER = 200


def jacobi(A, b, x0, tol, max_iter):
    n = len(b)
    x = x0.copy()
    riwayat = []
    for k in range(1, max_iter + 1):
        x_baru = np.zeros(n)
        for i in range(n):
            s = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_baru[i] = (b[i] - s) / A[i, i]
        galat = np.max(np.abs(x_baru - x))
        riwayat.append((k, x_baru.copy(), galat))
        x = x_baru
        if galat < tol:
            return x, riwayat, True
    return x, riwayat, False


if __name__ == "__main__":
    dominan = all(abs(A[i, i]) > np.sum(np.abs(A[i])) - abs(A[i, i]) for i in range(4))
    print("METODE JACOBI - Model Bioimpedansi Jaringan Tubuh (tegangan simpul, V)")
    print("Dominan diagonal secara ketat:", dominan)
    print(f"Tebakan awal = {x0}, toleransi = {TOL:g}, iterasi maks = {MAX_ITER}\n")
    print(f"{'k':>3} {'V1':>12} {'V2':>12} {'V3':>12} {'V4':>12} {'max|dx|':>12}")
    x, rw, ok = jacobi(A, b, x0, TOL, MAX_ITER)
    for k, xv, g in rw:
        print(f"{k:>3} " + " ".join(f"{v:12.6f}" for v in xv) + f" {g:12.3e}")
    print("\nKonvergen:", ok, "| jumlah iterasi:", len(rw))
    print("Solusi akhir (V):", " ".join(f"{n}={v:.6f}" for n, v in zip(NAMA, x)))
    eksak = np.linalg.solve(A, b)
    print("Solusi eksak (numpy):", " ".join(f"{n}={v:.6f}" for n, v in zip(NAMA, eksak)))
    print(f"Residu ||Ax-b||inf = {np.max(np.abs(A @ x - b)):.3e}")
    print(f"Cek KCL: arus ke elektroda kembali = {G_GND @ x:.6f} mA (arus injeksi = 0.5 mA)")
    print(f"Impedansi masukan Z = V1/I = {x[0] / 0.5:.4f} kOhm")