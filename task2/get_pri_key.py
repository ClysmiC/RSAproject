#!/usr/bin/python
import json, sys, hashlib, math

def usage():
    print """Usage:
        python get_pri_key.py student_id (i.e., qchenxiong3)"""
    sys.exit(1)

# TODO -- get n's factors
# reminder: you can cheat ;-), as long as you can get p and q
def get_factors(n):
    p = 0
    q = 0

    if n % 2 == 0:
        return 2, n / 2
    
    rootN = n ** .5

    # start with testing largest feasible odd numbers
    p = int(math.ceil(rootN))
    if p % 2 == 0:
        p += 1

    # only test dividing by odd numbers since we know that
    # the factors are prime... we can made an edge case for 2 above
    found = False
    
    while p > 1:
        if n % p == 0:
            q = n / p
            found = True
            break

        
        p -= 2

    if not found:
        raise ValueError('n is not the product of two primes')
    
    return (p, q)

# TODO: write code to get d from p, q and e
def get_key(p, q, e):
    def euclidean(high, low):
        remainder = high % low
        quotient = high // low

        if remainder == 1:
            # ( high coefficient,
            #   low coefficient )
            # print "[", high, "] + ", -quotient, " * [", low, "] = [1]"
            return (1, -quotient)

        # "Prime" variables are from the iteration "below us" that
        # we are substituting into
        highCoefficientPrime, lowCoefficientPrime = euclidean(low, remainder)

        # "New" variables are after we substitue and combine terms.
        # They then get passed up the call stack where they are received
        # as "prime" variables for the iteration before
        newLowCoefficient = highCoefficientPrime + lowCoefficientPrime * -quotient
        newHighCoefficient = lowCoefficientPrime

        # print newHighCoefficient, "[", high, "] + ",  newLowCoefficient, "[", low, "] = [1]"
        # sys.stdout.flush()
        # raw_input()
        return ( newHighCoefficient, newLowCoefficient )

    totient = (p - 1) * (q - 1)
    _, inverse = euclidean(totient, e)
    
    while(inverse < 0):
        inverse += totient

    return inverse

def main():
    if len(sys.argv) != 2:
        usage()

    n = 0
    e = 0

    all_keys = None
    with open("keys.json", 'r') as f:
        all_keys = json.load(f)
    
    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print sys.argv[1], "not in keylist"
        usage()
    
    pub_key = all_keys[name]
    n = int(pub_key['N'], 16)
    e = int(pub_key['e'], 16)

    print "your public key: (", hex(n).rstrip("L"), ",", hex(e).rstrip("L"), ")"
    sys.stdout.flush()
    
    (p, q) = get_factors(n)

    print "p = ", str(p)
    print "q = ", str(q)
    sys.stdout.flush()
        
    d = get_key(p, q, e)
    print "your private key:", hex(d).rstrip("L")

if __name__ == "__main__":
    main()
