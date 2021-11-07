def p_f(f, n, i):
    return f*(1 + i)**-n


def f_p(p, n, i):
    return p*(1 + i)**n


def p_g(g, n, i):
    j = (1 + i)**n
    return g*(j - i * n - 1)/(i**2 * j)


def p_a(a, n, i):
    j = (1 + i)**n
    return a*(j - 1)/(i * j)

i1 = 0.00313
i2 = 0.00393