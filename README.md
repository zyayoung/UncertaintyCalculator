# Standalone Uncertainty Calculator

Generate sample uncertainly calculation from equation.

## Demo

![](demo/demo.png)

[code](demo/demo.tex)

## Features

- [x] Auto symbolic partial derivative calculation
- [x] Latex code generation
- [x] Sample numerical calculation
- [x] Simple description of calculation
- [x] Unit propagation
- [ ] Significant figure

## Usage

Install SymPy
```bash
pip install sympy
```

Change settings
```python
equation_str = "P_{in} = w*h*P+log(w/h)*P"
input_sym    = 'P w h'.split()
input_val    = '150 0.258 0.211'.split()
input_unc    = '36  0.001 0.001'.split()
input_units  = [watt, meter, meter]
```

Generate code
```bash
python part.py
```

## Credits

- [SymPy](https://github.com/sympy/sympy)

