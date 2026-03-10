import hashlib
import random

class HyperLogLog:
    def __init__(self,b=10):
        self.b = b
        self.m = 2 ** b
        self.registers = [0] * self.m

    def hash(self,value):
        return int(hashlib.md5(value.encode()).hexdigest(),16)
    
    def add(self,value):
        x = self.hash(value)
        bucketNum = x >> (128 - self.b)
        kalanbitler = x & ((1<<(128-self.b))-1)
        strKB = bin(kalanbitler)[2:].zfill(128-self.b)
        sifirlar = len(strKB) - len(strKB.lstrip('0'))+1
        self.registers[bucketNum] = max(self.registers[bucketNum],sifirlar)
    
    def tahmin(self):
        alpha = 0.7213 / (1 + 1.079 / self.m)
        Z = sum(2**-bucket for bucket in self.registers)
        E = alpha * self.m ** 2/Z
        return int(E)
    
    def birlestirme(self, diger):
        if self.m != diger.m :
            raise ValueError("Bucket Sayıları Farklı!")
        for i in range(self.m):
            self.registers[i] = max(self.registers[i], diger.registers[i])

hll = HyperLogLog()
hll2 = HyperLogLog()
data = set()

for i in range(100000):
    x = str(random.randint(0,500000))
    data.add(x)
    hll.add(x)

for i in range(1000000):
    x = str(random.randint(0, 500000))
    data.add(x)
    hll2.add(x)

print("Gerçek Değer = ", len(data))
hll.birlestirme(hll2)
print("HyperLogLog Tahmini = ", hll.tahmin())