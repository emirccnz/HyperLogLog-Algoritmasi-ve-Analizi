# HyperLogLog Algoritması ve Python Implementasyonu

## Proje Açıklaması
Bu projede HyperLogLog algoritmasının Python ile implementasyonu yapılmıştır.  
HyperLogLog, büyük veri sistemlerinde farklı eleman sayısını yaklaşık olarak hesaplamak için kullanılan olasılıksal bir algoritmadır.  
Algoritma, milyonlarca veri içinden **unique (farklı) eleman sayısını** tahmin ederken çok düşük bellek kullanır.

## Problem Tanımı
Büyük veri sistemlerinde veri setleri milyonlarca hatta milyarlarca elemandan oluşabilir.  
Farklı eleman sayısını tam olarak hesaplamak, her bir elemanı saklamayı gerektirir ve **çok fazla bellek kullanır**.  

HyperLogLog algoritması, bu problemi **çok az bellekle ve yüksek hızda yaklaşık olarak** çözer.

## Kullanılan Teknolojiler
- Python 3  
- hashlib  
- random  

## Kurulum ve Çalıştırma
1. Projeyi klonlayın:
```bash
git clone https://github.com/kullanici/hyperloglog
```
2. Python dosyasını çalıştırın:
```bash
python hyperloglog.py
```
## Örnek Çıktılar:
### 1.
Bucket Sayısı = 10 iken
