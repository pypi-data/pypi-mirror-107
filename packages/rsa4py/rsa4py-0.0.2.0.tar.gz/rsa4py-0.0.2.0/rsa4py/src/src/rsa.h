#pragma once
#include <vector>
#include <string>

namespace RSA {
	struct PublicKey {
		long n;
		long e;
		PublicKey(long n, long e);
		PublicKey();
		std::vector<long long> encript(std::string inp);
		std::vector<long long> intencript(std::vector<int> inp);
		long long isSigned(long long val);
	};
	struct PrivateKey : public PublicKey{
	public:
		long d;

		PrivateKey(const long p, const long q, long e);
		PrivateKey();

		std::string decript(std::vector<long long>inp);
		std::vector<int> intdecript(std::vector<long long>inp);
		long long getSignature(long long val);

		long long test(long long val);
	};
}


inline RSA::PublicKey::PublicKey(long n, long e) {
	this->n = n;
	this->e = e;
}

inline RSA::PublicKey::PublicKey() {};

inline RSA::PrivateKey::PrivateKey() 
{
	this->n = 1;
	this->e = 1;
	this->d = 1;
};
