# O zadaniu  
Zadanie miało na celu zaprojektowanie i implementację szyfrowanego protokołu komunikacyjnego opartego na TCP, tzw. mini TLS. Projekt został zrealizowany przy użyciu języka Python.
### Wybrany wariant funkcjonalny
Został przez nas wybrany wariant wykorzystujący mechanizm encrypt-then-mac dla wysłanych szyfrowanych wiadomości jako mechanizm integralności i autentyczności.

# Realizacja zadania  
Zadanie zostało zrealizowane z sukcesem. Implementacja obejmuje zarówno klienta, jak i serwer, które wymieniają wiadomości w celu uzgodnienia wspólnego sekretu oraz klucza AES do szyfrowania dalszej komunikacji. Wszystkie pliki źródłowe znajdują się w katalogu `src`.  

# Uruchomienie  

**Uwaga!**   
Wymagane jest, aby na komputerze był zainstalowany Python oraz poetry.      

W celu uruchomienia zalecane jest utworzenie środowiska wirtualnego, w którym zainstalowane zostaną pakiety niezbędne do działania projektu. Aby to zrobić należy w katalogu 'src' wykonać polecenia:

```
poetry shell
poetry install
```

Aby uruchomić serwer, należy wykonać następujące polecenie w katalogu z kodem projektowym:   
```
python server.py <host> <port> <max_clients>
```

W celu uruchomienia klienta należy wykonać polecenie:   
```
python client.py <server_host> <server_port>
```   
Po uruchomieniu serwer nasłuchuje na połączenia, a klient może się z nim połączyć. Do ustanowienia połączenia wykorzystane są wiadomości ClientHello i ServerHello. Po zakończeniu tego procesu, obie strony obliczają wspólny sekret s oraz generują klucz AES. Klient może teraz przesyłać zaszyfrowane wiadomości do serwera lub zakończyć połączenie. Na serwerze istnieje możliwość wyświetlenia listy podłączonych klientów, zakończenia połączenia z wybranym klientem lub zatrzymania serwera. Otrzymane wiadomości są odszyfrowywane i wyświetlane na serwerze.

# Wyniki  
Po uruchomieniu protokołu, komunikacja odbywa się bezproblemowo – klient i serwer mogą wymieniać zaszyfrowane wiadomości, a mechanizmy szyfrowania i autentyczności działają zgodnie z założeniami. Przykładowe logi z sesji można znaleźć w katalogu `docs/example/logs`, a w katalogu `docs/example/wireshark` umieszczono dane z programu wireshark, który został uruchomiony w momencie przesyłania wiadomości między klientem a serwerem. 

# Podsumowanie  
Po zakończeniu testów, protokół działa zgodnie z oczekiwaniami – klient i serwer skutecznie wymieniają dane po zaszyfrowaniu ich przy użyciu klucza AES, a dodatkowo zapewniona jest integralność i autentyczność wiadomości przy pomocy HMAC.
