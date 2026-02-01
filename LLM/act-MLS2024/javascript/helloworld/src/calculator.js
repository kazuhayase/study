class Calculator {
  add(a, b) {
    return a + b;
  }

  subtract(a, b) {
    return a - b;
  }

  multiply(a, b) {
    return a * b;
  }

  divide(a, b) {
    return a / b;
  }
  factorial(n) {
    if (n === 0) {
      return 1;
    }
    return n * this.factorial(n - 1);
  }
}