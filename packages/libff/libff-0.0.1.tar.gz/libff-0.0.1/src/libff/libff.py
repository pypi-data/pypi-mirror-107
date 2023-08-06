#! usr/bin/python3 env
import math, sys

class Factors(object):
    """To calculate a number factors first create an "Factors" object with your int value
    
    Then you can see the documention of:
    1. object.all_factors() # returns list of the "n" factors
    2. object.prime_factors() # returns list of prime "n" factors
    3. object.multiplication() # returns list of the multiplication of prime factors of "n"
    """

    def __init__(self, n):
        super(Factors, self).__init__()
        self.n = int(n)
        self.all_out = []
        self.prime_out = []
        self.multiplication_out = []

    def all_factors(self):
        """call object.all_factors to fetch a list of "n" factors"""
        for a in range(1, int(self.n/2)):
            if self.n % a == 0:
                self.all_out.append(a)
                self.all_out.append(int(self.n/a))
        self.all_out = list(set(self.all_out))
        self.all_out.sort()
        return self.all_out

    def prime_factors(self):
        """call object.prime_factors to fetch a list of "n" prime factors"""
        if self.all_out == []:
            self.all_factors()
        for c in self.all_out:
            if c == 1:
                continue
            if is_prime(c) == True:
                self.prime_out.append(c)
        return self.prime_out

    def multiplication(self):
        """call object.multiplication to fetch a multiplication of prime factors of "n"
        
        see this (you can do this to see the best output format):
        
        for i in obj.multiplication():
        print(f"{i[0]}^{i[1]}", end="*")
        
        """
        if self.prime_out == []:
            self.prime_factors()
        for i in self.prime_out:
            count = 0
            e = self.n
            self.multiplication_out.append(i)
            while e % i == 0:
                e = e / i
                count += 1
            self.multiplication_out.append(count)
        return [self.multiplication_out[g:g + 2] for g in range(0, len(self.multiplication_out), 2)]

def is_prime (number):
    counter = 0
    for b in range(1, int(math.pow(number, 0.5))+1):
        if number % b == 0:
            counter += 1
    if counter <= 1:
        return True
    else:
        return False

def main():
    try:
        in_value = input("Please enter your number: ")
    except:
        raise
        sys.exit(1)
    number_factors = Factors(in_value)
    print(f"all factors of {number_factors.n} is: ", number_factors.all_factors())
    print(f"prime factors of {number_factors.n} is: ", number_factors.prime_factors())
    print(f"and {number_factors.n} is equal to: ", end="")
    for l in number_factors.multiplication():
        print(f"{l[0]}^{l[1]}", end="*")
    print("\b", end=" \n")

if __name__ == "__main__":
    main()
