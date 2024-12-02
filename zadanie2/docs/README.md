# O zadaniu
Zadanie miało na celu stworzenie zestawu programów – klienta i serwera wysyłające dane poprzez TCP. Klient i serwer powinien być napisany w różnych (C / Python) - wybraliśmy, że serwer będzie napisany w Pythonie, a klient w C. 

# Realizacja zadania
Zadanie zrealizowano z sukcesem - wersje serwera i klienta TCP stworzono w odpowiednich językach. Pliki źródłowe znajdują się w katalogach server / client. 

# Uruchomienie
Aby uruchomić kontenery z klientem oraz serwerem, należy uruchomić polecenie:
```
docker compose up
```
lub też (w innej wersji):
```
docker-compose up
```


UWAGA! W dostarczonej konfiguracji założono, że istnieje już sieć dockerowa o nazwie z39_network (odpowiadająca zespołowi). Jeśli taka sieć nie istnieje, to należy ją stworzyć przy użyciu polecenia:

```
docker network create z39_network
```
Jeśli pożądane jest użycie innej sieci, należy podmienić nazwę sieci w skrypcie run.sh, bądź wpisać polecenia ręcznie do terminala z podmienioną nazwą sieci.


Po wykonaniu tego polecenia pokazane zostaną logi obu kontenerów, jednak mogą być one trochę nieczytelne ze względu na to, że pojawiają się jednocześnie, stąd też stworzyliśmy skrypt `data.sh`, który kopiuje logi obu programów do odpowiednich plików `.log` w katalogu docs.


Aby usunąć powstałe kontenery (np. w celu ponownego uruchomienia) należy wykorzystać polecenie
```
docker compose down
```

# Konfiguracja testowa
Aby przetestować działanie stworzono proste drzewo binarne składające się z korzenia i dwóch węzłów podrzędnych. Każdy węzeł zawiera liczbę całkowitą 16-bitową, liczbę całkowitą 32-bitową oraz napis o ograniczonej (ale zmiennej - realizowanej poprzez liczbę losową) długości 50kB. Taki napis może reprezentować np. przesyłanie jakiegoś dokumentu.

# Wyniki
Przykładowe logi z uruchomienia kontenerów znajdują się w katalogu `docs/examples`. 

Można zauważyć, że komunikacja działa, wysyłanie drzewa binarnego struktur odbywa się poprawnie, serwer jest w stanie odtworzyć taką strukturę. 


# Podsumowanie
Po powyższych uruchomieniach programów widać, że komunikacja przez TCP działa - struktura jest wysyłana i rekonstruowana na serwerze.