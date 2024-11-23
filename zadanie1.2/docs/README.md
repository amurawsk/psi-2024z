# O zadaniu
Zadanie miało na celu stworzenie zestawu programów – klienta i serwera wysyłające datagramy UDP. Klient jak i serwer powinien być napisany w wybranym języku (C / Python) - wybraliśmy język Python. 


Dodatkowym wymaganiem było zmodyfikowanie protokołu UDP tak, aby był on niezawodny - aby gubione pakiety były wykrywane i retransmitowane.

# Realizacja zadania
Zadanie zrealizowano z sukcesem - wersje serwera i klienta UDP stworzono w Pythonie. Pliki źródłowe znajdują się w katalogach server / client. 

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
