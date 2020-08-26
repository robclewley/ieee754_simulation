# ieee754_simulation

A Python module to simulate binary floating point representations and arithmetic to IEEE 754 standards of arbitrary fixed precision, or to infinite precision, and different rounding modes.
You may find it is easier to learn about machine epsilon, denormalized numbers, representation and rounding error using low-bit formats compared to the standard single or double precision.

The design is loosely based on the Decimal module. This code was written in 2008 when I was teaching a numerical analysis class.

## Features
 * Primarily intended for teaching purposes, e.g. in a numerical analysis course. It demonstrates representation formats and facilitates exploration of the distribution of represented values along the real number line.
 * It's not intended to be an efficient implementation for computation. It focuses on transparency to aid learning.
 * It can represent any (sign, characteristic, significand) IEEE 754-style format, and is not restricted to representations with total precision less than 64 bits. The internal representations and arithmetic are done using arbitrary precision and do not depend on the python 'float' (64 bit) class.
 * Available rounding modes are 'up', 'down', 'floor', 'ceiling', 'half_up', and 'half_down'.
 * Arithmetic operations are only permitted between numbers represented in exactly the same format.
 * A binary integer class is also implemented with its associated integer arithmetic and shift operations (no logical operations).
 * max, min, sqrt, power functions are defined for the appropriate numeric classes.

See the following for details, and references therein:
 - http://en.wikipedia.org/wiki/Floating_point
 - http://en.wikipedia.org/wiki/Rounding
 - http://en.wikipedia.org/wiki/IEEE_754
 - http://en.wikipedia.org/wiki/Binary_numeral_system

## Known issues

 * Binary floating point arithmetic not simulated in its native form, but through
  internal use of arbitrary precision Decimal floating point numbers. It would
  be preferable to have a pure binary arithmetic implementation that
  demonstrates shifting of exponents, etc. before addition.
 * Does not directly simulate the algorithmic implementations by which
  IEEE 754 arithmetic and rounding is performed in CPUs. e.g. rounding up
  is *not* achieved by adding 0.5 and then truncating in this code.
 * Creation of higher precision floats is slow due to python implementation of
  frexp function.
 * Boolean operations on binary floating point numbers are not supported at this
  time.
 * `ContextClass` does not support initialization from numpy float128 values. Needs
  additional code to extract byte-by-byte hex representation from the 'data'
  attribute of such a value, and conversion into equivalent binary string.
 * `eval(repr(x))`, when `x` is a `ContextClass` instance, creates a Binary object with
  the same representation (fixed precision, rounding) as x, not another
  ContextClass instance. However, `x == eval(repr(x))`.
* decimal context precision value must not be changed by the user to be less
  than the precision required by any ContextClass instances (Binary numbers of a
  fixed precision), otherwise arithmetic on those numbers may be inaccurate.
  In Python 2.5 and above, local context could be established for these
  calculations using the with statement (see here for implementation details:
  http://docs.python.org/lib/decimal-decimal.html). See binary_py25.py.
* mod, floordiv, divmod methods are not supported.
* Can be slow to evaluate expressions involving high precision values.
* Can hash a binary context (ContextClass instance), but cannot hash
  a decimal.context instance.
* Requires numpy to be installed, in order to use numpy.sign, numpy.zeros
  and provide compatibility with numpy.float32, numpy.float64, and
  numpy.float128 values. The sign function and array use provide better speed
  in key parts of the algorithms, but could be easily replaced to make
  numpy installation optional.
* Does not support use of minifloats (IEEE-754 style formats with very low
  bit lengths for the exponent and characteristic) for integer-only
  representations. (This is a common application of such values, according to
  http://en.wikipedia.org/wiki/Minifloat.)
* Historical: `float(Decimal("Inf"))` will not work in Python 2.5 due to a
  problem in Python itself. This has been fixed in Python 2.6 and above
  (http://bugs.python.org/issue3188).

## Usage

### Constructors

```
>>> context = define_context(5, 12, ROUND_DOWN)
```

Equivalent binary float values in a given context:

```
>>> x = Binary('-0.1111', context)          # binary fraction assumed by default
>>> x = Binary(Decimal("-0.9375"), context) # decimal fraction
```

The following represent the same binary number (in context) but are a way
to directly specify the representation in terms of the underlying context

```
>>> a = context('1 01110 111000000000')   # (sign, characteristic, significand)
>>> a = context('101110111000000000')     # (sign, characteristic, significand)
```

These alternative forms are also valid, for convenience:

```
>>> a = context(Decimal("-0.9375"))
>>> a = context(Binary('-0.1111'))
```

If the python float literal `-0.9375` is exactly representable in the context,
then this is also equivalent:

```
>>> a = context(-0.9375)
>>> a = context(numpy.float64(-0.9375))
```

Otherwise, the resulting representation in a will be to the "nearest"
representable value under the rules of the context's precision and rounding
mode.
The values in a are instances of the context, and are not Binary class
instances.
Note that a context instance cannot be initialized directly using a string
literal for a binary fraction, to avoid ambiguity with the primary use
case, namely with input strings for (sign, characteristic, significand).
The Binary constructor can also represent _arbitrary_ precision binary values in
the absence of a given context. After any of the above definitions of `x`:

```
>>> x.context
<class 'binary.Float_5_12_D'>
```

However:

```
>>> y = Binary('0.110100101010101011110001111100001e5')
>>> y.context is None
True
```

Note that infinite binary precision is not possible to specify from a
Decimal object, in case the binary representation is non-terminating.

```
>>> b = Binary(Decimal("0.1"))
ValueError: Cannot create arbitrary precision binary value without a
   representation context
```

### Views

For a context instance `x` (not a Binary instance), we slightly break the
tradition that `eval(repr(x))` is identically the same type as `x`. However,
`eval(repr(x)) == x` and the evaluation leads to a Binary object with the same
context.

```
>>> x = context(Decimal("-0.9375"))
>>> x                 # default 'view' is as binary
Binary("-0.1111E0", (5, 12, ROUND_DOWN))
>>> bx = eval(repr(x))
>>> bx == x
True
>>> bx.context
<class 'binary.Float_5_12_D'>
>>> bx.context == x.context   # bx really quacks like a duck
True
>>> x.as_binary()     # output always in scientific notation with 0 before radix
Binary("-0.1111E0")
>>> x.as_binary() == bx  # x.as_binary() keeps the same context
True
>>> x.as_decimal()
Decimal("-0.9375")
>>> print x
1 01110 111000000000
```

### Comparisons

You can only compare like representations from the same context.

```
>>> d = double(1)
>>> q = quadruple(1)
>>> d == q
ValueError: Mismatched precision
```

If you want to compare the actual values that these objects represent, convert
them to a Binary number first

```
>>> bd = Binary(double(1))
>>> bq = Binary(quadruple(1))
>>> bd == bq
True
>>> bd == 1.0   # cannot compare with python-native floats
TypeError: Invalid object for comparison
>>> bd > 1
False
>>> bd == Decimal("1")
True
```

### Conversions

For high precision floats with long mantissas, convert them accurately to
Decimal type. Note that Decimal(str(f)) will not be accurate for floats f
with mantissas longer than the displayable length of f by the str function.
Thus float(Decimal(str(f))) != f for some f. To avoid this, create the
representation of the float in the appropriate context by
double(f)
which will be a precise representation of f in double precision, where f
can be a python float, numpy.float64. For numpy.float32 use single(f).
Binary values in one context can be converted (coerced) to another thus:

```
>>> xs = Binary('-1111.001', single)
>>> xd = Binary(xs, double)
```

or

```
>>> xd = Binary(double(xs))
```

### Arithmetic

Can only perform arithmetic on representations from a given context with
other instances of the same context (including Binary instances with
identical context).

To perform arbitray precision arithmetic with mixed representations,
first convert to Binary type, which does not care about the precision of
the operands: the operation returns a new Binary value of the precise
result, without context if neither operand had context, otherwise with
the highest precision context. In a tie, arithmetic is not possible unless
the rounding is the same.

```
>>> bd = Binary(double(1.5))
>>> bq = Binary(quadruple(0.1))
>>> c = bd + bq
>>> print c
0.11001100110011001100110011001100110011001100110011001101E1
>>> c.__class__
<class 'binary.Binary'>
>>> c.context   # coerced to the higher precision
<class 'binary.Float_15_112_HU'>
```