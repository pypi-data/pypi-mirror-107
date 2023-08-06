#include "rsa.h"
#include <iostream>

int gcd(int a, int b) {
	if (b == 0)
		return a;
	return gcd(b, a % b);
}


unsigned long long int constexpr IntPower(const unsigned int x, unsigned long p, unsigned long mod)
{
	if (p == 0) return 1;
	if (p == 1) return x;

	unsigned long long int tmp = IntPower(x, p/2, mod);
	tmp = tmp % mod;
	if ((p % 2) == 0) { 
		return tmp * tmp; 
	}
	else { 
		return x * tmp * tmp; 
	}
}

int modInverse(int a, int prime)
{
	a = a % prime;
	for (int x = 1; x < prime; x++)
		if ((a * x) % prime == 1)
			return x%prime;

	return -1;
}

RSA::PrivateKey::PrivateKey(const long p, const long q, long e) {
	// p, q are primes
	this->n = p * q;
	long gamma = (p - 1) * (q - 1)/gcd(p-1, q-1);
	while (!(gcd(e, gamma) == 1)) {
		e = std::rand()%gamma;
	}
	this->e = e;
	this->d = modInverse(e, gamma);
	auto i = d * e;
}

std::string RSA::PrivateKey::decript(std::vector<long long> inp)
{
	std::string res;
	for (auto const& val : inp) {
		auto v = IntPower(val, this->d, this->n)%this->n;
		res.push_back(char(v%this->n));
	}
	return res;
}

std::vector<int> RSA::PrivateKey::intdecript(std::vector<long long> inp)
{
	std::vector<int> res;
	for (auto const& val : inp) {
		auto v = IntPower(val, this->d, this->n)%this->n;
		res.push_back(v%this->n);
	}
	return res;
}

std::vector<long long> RSA::PublicKey::encript(std::string str)
{
	std::vector<long long>res;
	for (auto const& c : str) {
		int val = int(c);
		auto v = IntPower(val, this->e, this->n);
		res.push_back(v%this->n);
		
	}

	return res;
}

std::vector<long long> RSA::PublicKey::intencript(std::vector<int> inp)
{
	std::vector<long long>res;
	for (auto const& val : inp) {
		auto v = IntPower(val, this->e, this->n);
		res.push_back(v % this->n);

	}

	return res;
}
