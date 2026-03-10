# HyperLogLog Algoritması ve Analizi
__Tanım:__ Bu projede Büyük Veri Analitiğinde "Cardinality Estimation" (Küme Büyüklüğü Tahmini) problemini çözen algoritmalardan biri olan HyperLogLog Algoritması ele alınmıştır.
HyperLogLog, “count-distinct” problemi için kullanılan bir algoritmadır ve bir çokluset (multiset) içindeki farklı elemanların sayısını yaklaşık olarak tahmin eder. Bir çokluset içindeki farklı elemanların tam sayısını hesaplamak, eleman sayısı ile orantılı bir bellek gerektirir; bu, çok büyük veri setleri için pratik değildir.

Olasılıksal kardinalite tahmincileri (probabilistic cardinality estimators) — örneğin HyperLogLog algoritması — bu işlem için çok daha az bellek kullanır, ancak yalnızca yaklaşık tahmin yapabilir. HyperLogLog algoritması, >10⁹ boyutundaki kardinaliteleri bile tipik olarak %2 standart hata ile yaklaşık olarak tahmin edebilir ve bunun için yalnızca 1,5 kB bellek gerektirir.

HyperLogLog Algoritmasının yaptığı tahmin işlemini şöyle basit bir örnekle açıklayalım; 
Bir yazı-tura attığımızı varsayalım. 10 kere art arda tura gelme ihtimali 1/1024 'tür. HyperLogLog algoritmasının burada yaptığı yorum: Bu olasılığın gerçekleşmesi için yaklaşık olarak 1000 farklı atış yapılmıştır.

HyperLogLog gelen veriyi rastgele olarak hashler ve bit tipine dönüştürür. Yazı-tura örneğinde de olduğu gibi bir 0 ve 1 lerden oluşan bir veride art arda 0' ların olma olasılığı 0 sayısına göre üstel şekilde artar. Bu doğrultuda yine hata oranını düşürmek için bazı işlemler kullanır ve nihai tahmin yapar.

## HyperLogLog Algoritması İşlemleri

1. **Veriyi Hashleme**  
   - Her eleman, uniform dağılım sağlayan bir hash fonksiyonuna gönderilir (örneğin MD5).  
   - Hash işlemi, elemanı **128-bit’lik rastgele bir sayı** olarak temsil eder.

2. **Bucket Seçimi**
   
   -> Sadece tek bir maksimum değere bakmak, şans eseri gelen aşırı uç bir değer nedeniyle (örneğin ilk denemede 10 sıfır gelmesi) büyük yanılgılara yol açabilir.    Bu yüzden HLL, hash'in ilk birkaç bitini kullanarak verileri farklı "kovalara" (buckets) dağıtır ve her kova için maksimum sıfır sayısını ayrı ayrı takip eder.
   - Hash sonucu sayının ilk **b bit’i** bir bucket (kayıt kutusu) numarasını belirler.  
   - Toplam bucket sayısı: `m = 2^b`.

4. **Leading Zero (başındaki sıfır) Sayısı**  
   - Bucket dışında kalan bitlerdeki **en uzun baştaki sıfır uzunluğu** hesaplanır.  
   - Bu değer, her bucket’ta saklanan **register değerini** günceller (maksimum değeri alır).

5. **Tahmin Hesaplama**  
   - Tüm bucket’larda saklanan değerler kullanılarak **harmonik ortalama** benzeri bir formülle tahmin yapılır:  

   \[
   E = \alpha_m \cdot m^2 \cdot \left(\sum_{j=1}^{m} 2^{-M[j]}\right)^{-1}
   \]

   - Burada:
     - \(M[j]\) → j’inci bucket’taki maksimum leading zero sayısı  
     - \(\alpha_m\) → bias düzeltme katsayısı  

6. **Merge (birleştirme)**

   ->Merge İşleminin Amacı: Büyük veri setleri genellikle birden fazla kaynaktan veya sunucudan gelir. Her veri kaynağı için ayrı bir HyperLogLog nesnesi             oluşturulur. Merge işlemi, bu farklı HLL nesnelerini tek bir tahmin için birleştirmeyi sağlar. Bu işlemin yapılabilmesi için bucket sayılarının aynı olması        gerekir.
   - HyperLogLog’ler, dağıtık sistemlerde veya farklı veri setlerinde **register’larını kaybetmeden birleştirilebilir**.  
   - Her bucket için maksimum değer alınır.

