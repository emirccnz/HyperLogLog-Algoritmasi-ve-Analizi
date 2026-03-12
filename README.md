# HyperLogLog Algoritması ve Analizi
__Tanım:__ Bu projede Büyük Veri Analitiğinde "Cardinality Estimation" (Küme Büyüklüğü Tahmini) problemini çözen algoritmalardan biri olan HyperLogLog Algoritması ele alınmıştır.
HyperLogLog, “count-distinct” problemi için kullanılan bir algoritmadır ve bir çokluset (multiset) içindeki farklı elemanların sayısını yaklaşık olarak tahmin eder. Bir çokluset içindeki farklı elemanların tam sayısını hesaplamak, eleman sayısı ile orantılı bir bellek gerektirir; bu, çok büyük veri setleri için pratik değildir.

Olasılıksal kardinalite tahmincileri (probabilistic cardinality estimators) — örneğin HyperLogLog algoritması — bu işlem için çok daha az bellek kullanır, ancak yalnızca yaklaşık tahmin yapabilir. HyperLogLog algoritması, >10⁹ boyutundaki kardinaliteleri bile tipik olarak %2 standart hata ile yaklaşık olarak tahmin edebilir ve bunun için yalnızca 1,5 kB bellek gerektirir.

HyperLogLog Algoritmasının yaptığı tahmin işlemini şöyle basit bir örnekle açıklayalım; 
Bir yazı-tura attığımızı varsayalım. 10 kere art arda tura gelme ihtimali 1/1024 'tür. HyperLogLog algoritmasının burada yaptığı yorum: Bu olasılığın gerçekleşmesi için yaklaşık olarak 1000 farklı atış yapılmıştır.

HyperLogLog gelen veriyi rastgele olarak hashler ve bit tipine dönüştürür. Yazı-tura örneğinde de olduğu gibi bir 0 ve 1 lerden oluşan bir veride art arda 0' ların olma olasılığı 0 sayısına göre üstel şekilde artar. Bu doğrultuda yine hata oranını düşürmek için bazı işlemler kullanır ve nihai tahmin yapar.

## HyperLogLog Algoritması İşlemleri

1. **Veriyi Hashleme:**  
   - Her eleman, uniform dağılım sağlayan bir hash fonksiyonuna gönderilir (örneğin MD5).  
   - Hash işlemi, elemanı **128-bit’lik rastgele bir sayı** olarak temsil eder.

2. **Bucket Seçimi:**
   
   -> Sadece tek bir maksimum değere bakmak, şans eseri gelen aşırı uç bir değer nedeniyle (örneğin ilk denemede 10 sıfır gelmesi) büyük yanılgılara yol açabilir.    Bu yüzden HLL, hash'in ilk birkaç bitini kullanarak verileri farklı "kovalara" (buckets) dağıtır ve her kova için maksimum sıfır sayısını ayrı ayrı takip eder.
   - Hash sonucu sayının ilk **b bit’i** bir bucket (kayıt kutusu) numarasını belirler.  
   - Toplam bucket sayısı: `m = 2^b`.

4. **Leading Zero (başındaki sıfır) Sayısı:**  
   - Bucket dışında kalan bitlerdeki **en uzun baştaki sıfır uzunluğu** hesaplanır.  
   - Bu değer, her bucket’ta saklanan **register değerini** günceller (maksimum değeri alır).

5. **Tahmin Hesaplama:**  
   - Tüm bucket’larda saklanan değerler kullanılarak **harmonik ortalama** benzeri bir formülle tahmin yapılır:  

    `E = αm * m² * ( 1 / Σ(2^(-M[j])) )`

   Burada:

   - **E** → Tahmin edilen unique eleman sayısı  
   - **m** → Bucket sayısı, m = 2^b  
   - **M[j]** → j'inci bucket'ta saklanan değer (leading zero sayısı)  
   - **αm** → Bias düzeltme katsayısı  

6. **Merge (birleştirme):**

   ->Merge İşleminin Amacı: Büyük veri setleri genellikle birden fazla kaynaktan veya sunucudan gelir. Her veri kaynağı için ayrı bir HyperLogLog nesnesi             oluşturulur. Merge işlemi, bu farklı HLL nesnelerini tek bir tahmin için birleştirmeyi sağlar. Bu işlemin yapılabilmesi için bucket sayılarının aynı olması        gerekir.
   - HyperLogLog’ler, dağıtık sistemlerde veya farklı veri setlerinde **register’larını kaybetmeden birleştirilebilir**.  
   - Her bucket için maksimum değer alınır.

## HyperLogLog Algoritması Analizi

### Best Case (En İyi Durum):

En iyi durumda hash fonksiyonu verileri bucket’lara dengeli bir şekilde dağıtır ve her eleman için aşağıdaki işlemler yapılır:

- Hash değerinin hesaplanması  
- Bucket numarasının belirlenmesi  
- İlgili register değerinin güncellenmesi  

Bu işlemler sabit sayıda olduğu için işlem süresi değişmez.

**Zaman Karmaşıklığı:**  
O(1)

**Bellek Karmaşıklığı:**  
O(m)  
Burada m = 2^b olup bucket sayısını ifade eder.

### Average Case (Ortalama Durum):

Ortalama durumda hash fonksiyonu verileri bucket’lara rastgele ve dengeli bir şekilde dağıtır. 
Algoritma her eleman için yine aynı sabit işlemleri gerçekleştirir.
Bu nedenle her eleman için işlem süresi yine sabittir.

**Zaman Karmaşıklığı:**  
O(1)

n adet veri işlendiğinde toplam süre:

O(n)

### Worst Case (En Kötü Durum):

En kötü durumda hash fonksiyonu verileri bucket’lara dengesiz dağıtabilir. 
Bazı bucket’lar daha fazla veri alırken bazıları boş kalabilir. Bu durum tahmin doğruluğunu etkileyebilir ancak algoritmanın çalışma süresi yine değişmez çünkü her eleman için yapılan işlem sayısı sabittir.

**Zaman Karmaşıklığı:**  
O(1)

**Bellek Karmaşıklığı:**  
O(m)

Genel durumda HyperLogLog algoritması her durumda sabit işlemleri yapacağı için karmaşıklık değişmez ancak bucket sayısı gibi parametreler algoritmanın doğruluğunu etkileyebilir. 

## Avantajlar ve Dezavantajlar

### Avantajlar

**1. Çok düşük bellek kullanımı:**  
HyperLogLog algoritması milyonlarca hatta milyarlarca veri için yalnızca birkaç kb bellek kullanır. 
Bu, tüm verileri saklayan klasik yöntemlere göre büyük bir avantajdır.

**2. Büyük veri setlerinde yüksek performans:**  
Algoritma her veri için sabit sayıda işlem yaptığı için veri büyüklüğü artsa bile performans büyük ölçüde korunur.

**3. Dağıtık sistemlere uygunluk:**  
HyperLogLog yapıları kolayca birleştirilebilir. 
Bu sayede farklı sistemlerde hesaplanan sonuçlar tek bir tahmin hâline getirilebilir.

**4. Streaming veri ile çalışabilme:**  
Veri akışı sürekli olsa bile tüm veriyi saklamaya gerek yoktur. 
Yeni gelen her veri yalnızca ilgili bucket değerini günceller.

### Dezavantajlar

**1. Tam sonuç üretmez:**  
HyperLogLog algoritması kesin sonuç değil yaklaşık sonuç üretir.

**2. Küçük veri setlerinde doğruluk düşebilir:**  
Algoritma özellikle çok büyük veri setleri için tasarlanmıştır. 
Küçük veri setlerinde hata oranı daha belirgin olabilir.

**3. Elemanların kendisi saklanmaz:** 
Algoritma yalnızca farklı eleman sayısının tahminini verir. 
Veri setinde hangi elemanların bulunduğu bilgisi tutulmaz.

**4. Hash fonksiyonuna bağımlıdır:**  
Algoritmanın doğruluğu kullanılan hash fonksiyonunun veriyi ne kadar dengeli dağıttığına bağlıdır.
