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


Aby łatwo wprowadzić opóźnienie do kontenera (np. aby zasymulować realną sieć) można użyć skryptu `delay.sh`. Skrypt ten symuluje opóźnienie i możliwość gubienia pakietów w kontenerze klienta. 



# Wyniki
Przykładowe logi z uruchomienia kontenerów znajdują się w katalogu `docs/examples`. Są tam pliki z "normalnego" uruchomienia, a także z takiego, w którym w trakcie wysyłania pakietów wprowadzono opóźnienie. 

Można zauważyć, że przy normalnym uruchomieniu czasy są bliskie 0, a jeśli wprowadzono opóźnienie, to pakiety zaczynają się gubić, czy też dochodzić po sporym czasie. 


UWAGA! Długiego czasu między wysłaniem a odebraniem pierwszej wiadomości (o nr 0) nie należy brać pod uwagę, gdyż wynika ona z kolejności uruchomienia kontenerów serwera i klienta w Dockerze. Jeśli pierwszy zostanie uruchomiony klient, to musi on poczekać na uruchomienie serwera, który odbierze wiadomość - stąd dodatkowy czas. 


# Podsumowanie
Po powyższych uruchomieniach programów widać, że pakiety dochodzą do serwera nawet mimo braku stabilności i niezawodności łącza. Pakiet jest retransmitowany do tego momentu, kiedy serwer potwierdzi odbiór, co gwarantuje dostarczenie wszystkich pakietów. 
