# O zadaniu
Zadanie miało na celu stworzenie zestawu dwóch programów – klienta i serwera wysyłające datagramy UDP. Klient jak i serwer powinien być napisany zarówno w C jak i Pythonie (łącznie 4 programy). 

# Realizacja zadania
Zadanie zrealizowano z sukcesem - wersje serwera i klienta UDP stworzono zarówno w języku C, jak i Pythonie. Wszystkie pliki znajdują się w odpowiadającym językowi katalogu. 

# Uruchomienie
Aby uruchomić klienta bądź serwer w danym języku należy przejść do katalogu {język}/{klient/serwer} i uruchomić skrypt `run.sh`. 
W tym skrypcie znajdują się polecenia dockera, które budują kontener, a następnie uruchamiają go (oczywiście zalecane jest uprzednie uruchomienie serwera, nim uruchomimy klienta). 


UWAGA!
W dostarczonej konfiguracji założono, że istnieje już sieć dockerowa o nazwie z39_network (odpowiadająca zespołowi). Jeśli taka sieć nie istnieje, to należy ją stworzyć przy użyciu polecenia:
```
docker network create z39_network
```

Jeśli pożądane jest użycie innej sieci, należy podmienić nazwę sieci w skrypcie run.sh, bądź wpisać polecenia ręcznie do terminala z podmienioną nazwą sieci. 


UWAGA!
Jeśli wyskoczy błąd *permission denied*, należy wykonać poniższe polecenie:
```
chmod 755 run.sh
```

UWAGA!
Jeśli klienta chcemy uruchamiać wielokrotnie (np. zmieniając tablicę sizes), należy każdorazowo usuwać pozostały kontener klienta. Można to zrobić przy użyciu polecenia:
```
docker rm <nazwa_kontenera>
```
Nazwą kontenera w dostarczonej konfiguracji jest `pclient` lub `cclient`. 

