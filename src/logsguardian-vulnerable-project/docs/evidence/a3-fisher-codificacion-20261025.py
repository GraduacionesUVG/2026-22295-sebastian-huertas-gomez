import json
from math import comb, sqrt

Z = 1.959963984540054


def fisher_bilateral(a, n1, b, n2):
    k = a + b
    n = n1 + n2
    total = comb(n, k)

    def pmf(x):
        return comb(n1, x) * comb(n2, k - x) / total

    p_obs = pmf(a)
    return sum(pmf(x) for x in range(max(0, k - n2), min(n1, k) + 1) if pmf(x) <= p_obs * (1 + 1e-9))


a, n1, b, n2 = 80, 105, 84, 95
p1, p2 = a / n1, b / n2
diff = p2 - p1
se = sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
out = {
    "grupo_codificados": {"k": a, "n": n1, "p": p1},
    "grupo_sin_codificar": {"k": b, "n": n2, "p": p2},
    "diferencia_puntos": diff * 100,
    "ic95_wald_diferencia_puntos": [(diff - Z * se) * 100, (diff + Z * se) * 100],
    "fisher_exacto_bilateral_p": fisher_bilateral(a, n1, b, n2),
    "z": Z,
}
json.dump(out, open("docs/evidence/a3-fisher-codificacion-20261025.json", "w"), indent=1)
print(json.dumps(out, indent=1))
