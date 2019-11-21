
from sympy import *
from sympy.physics.units import *

from random import choice

def rand_str(length=64):
    return ''.join([choice("qwertyuiopasdfghjklzxcvbnm") for _ in range(length)])

# Settings
equation_str = "P_{in} = w*h*P+log(w/h)*P"
input_sym    = 'P w h'.split()
input_val    = '150 0.258 0.211'.split()
input_unc    = '36  0.001 0.001'.split()
input_units  = [watt, meter, meter]

# parse
eq = simplify(equation_str.split("=")[1].strip())
to_cal_sym = (equation_str.split("=")[0].strip())
syms = symbols(input_sym)
unc_syms = symbols([f"u_{s}" for s in input_sym])

numerical_values = dict(zip(
    input_sym+list(map(lambda x: f"u_{x}", input_sym)),
    input_val+input_unc
))

tmp_sym = [(s, rand_str()) for s in (syms + unc_syms)]
assert len(tmp_sym) == len(set(tmp_sym))


# Uncertainty

print("""
To find the uncertainty of ${}$, the partial derivatives are first calculated. Sample calculation is based on the first row of Table 1 where """.format(f"{to_cal_sym}={latex(eq)}") + ', '.join(
    [f"${s}={v}~{latex(u)}$" for s,u,v in zip(input_sym, input_units, input_val)]
))

print("""
% unc
\\begin{equation*}
\\begin{aligned}""")
for sym in syms:
    print("\\left(\\frac{\\partial "+to_cal_sym+"}{\\partial "+str(sym)+"}\\right)^2", end='&=')
    deq_sym = Derivative(eq, sym, evaluate=True)
    print(f"\\left({latex(deq_sym)}\\right)^2", end='=')
    intermediate = latex(deq_sym.subs(tmp_sym), mul_symbol="dot")
    for s, tmp_str in tmp_sym:
        intermediate = intermediate.replace(tmp_str, numerical_values[str(s)])
    print(f"\\left({intermediate}\\right)^2", end='=')
    print(f"\\left({latex(deq_sym.evalf(2,subs=numerical_values))}\\right)^2", end='=')
    print(latex((deq_sym**2).evalf(2,subs=numerical_values)), end='~')
    print(latex((deq_sym**2).subs(zip(syms, input_units))), end="\\\\\n")
    
print("""\\end{aligned}
\\end{equation*}""")

print("""
Then, the uncertainty of ${}$ is given by the following formula where """.format(to_cal_sym) + ', '.join(
    [f"$u_{{{s}}}={v}~{latex(u)}$" for s,u,v in zip(input_sym, input_units, input_unc)]
))

unc = simplify(0)
print("""
\\begin{equation*}
\\begin{aligned}""")
print(f"u_{{{to_cal_sym}}}&=\sqrt"+"{")
for sym, unc_sym in zip(syms, unc_syms):
    print("\\left(\\frac{\\partial "+to_cal_sym+"}{\\partial "+str(sym)+"}\\right)^2{"+str(unc_sym)+"}^2", end="")
    deq_sym = Derivative(eq, sym, evaluate=True)
    unc += (unc_sym**2) * ((deq_sym**2).evalf(2,subs=numerical_values))
    if sym is not syms[-1]: print("+", end="")
print("}\\\\\n&=", end='')
unc = sqrt(unc)

intermediate = latex(unc.subs(tmp_sym), mul_symbol="dot")
for s, tmp_str in tmp_sym:
    intermediate = intermediate.replace(tmp_str, numerical_values[str(s)])
print(f"{intermediate}", end="")

print("\\\\\n&=", end='')
if str(unc.evalf(5,subs=numerical_values))[0] == '1' and str(unc.evalf(2,subs=numerical_values))[0] == '1':
    print((unc.evalf(2,subs=numerical_values)), end='~')
else:
    print((unc.evalf(1,subs=numerical_values)), end='~')
print(latex(eq.subs(zip(syms, input_units))))
print("""\\end{aligned}
\\end{equation*}""")


# Result

print("""
% result
\\begin{equation*}
\\begin{aligned}""")
print(f"{to_cal_sym}&={latex(eq)}\\\\")
print("&=", end='')

intermediate = latex(eq.subs(tmp_sym), mul_symbol="dot")
for s, tmp_str in tmp_sym:
    intermediate = intermediate.replace(tmp_str, numerical_values[str(s)])
print(f"{intermediate}", end="\\\\\n")
print("% TODO: Fix sf")
print("&=", end='')

print(latex(eq.evalf(6,subs=numerical_values)), end=' ')
print("\\pm", end=' ')
if str(unc.evalf(5,subs=numerical_values))[0] == '1' and str(unc.evalf(2,subs=numerical_values))[0] == '1':
    print((unc.evalf(2,subs=numerical_values)), end='~')
else:
    print((unc.evalf(1,subs=numerical_values)), end='~')
print(latex(eq.subs(zip(syms, input_units))))
print("""\\end{aligned}
\\end{equation*}""")
