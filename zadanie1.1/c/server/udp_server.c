#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define BUFSIZE 4096

void start_server(const char *host, int port) {
    int server_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);
    unsigned char buffer[BUFSIZE];

    if ((server_socket = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Błąd tworzenia gniazda");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(server_socket, (const struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Błąd bindowania");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    printf("Serwer nasłuchuje na %s:%d\n", host, port);

    while (1) {
        int received_len = recvfrom(server_socket, buffer, BUFSIZE, 0, (struct sockaddr *)&client_addr, &client_addr_len);
        if (received_len < 2) {
            fprintf(stderr, "Odebrano niepoprawny datagram - za mały rozmiar\n");
            continue;
        }

        int length = (buffer[0] << 8) | buffer[1];
        unsigned char *content = buffer + 2;

        if (received_len - 2 == length) {
            int valid_data = 1;
            for (int i = 0; i < length; i++) {
                if (content[i] != 'A' + (i % 26)) {
                    valid_data = 0;
                    break;
                }
            }

            if (valid_data) {
                printf("Odebrano poprawny datagram od %s:%d o rozmiarze %d bajtów\n",
                       inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port), length);
                sendto(server_socket, "OK", 2, 0, (struct sockaddr *)&client_addr, client_addr_len);
            } else {
                printf("Odebrano błędny datagram od %s:%d - dane uległy zmianie\n",
                       inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
                sendto(server_socket, "Błędne dane", 11, 0, (struct sockaddr *)&client_addr, client_addr_len);
            }
        } else {
            printf("Odebrano błędny datagram od %s:%d - niezgodna długość danych [(%d) != (%d)]\n",
                   inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port), received_len - 2, length);
            sendto(server_socket, "Niepoprawna długość datagramu", 28, 0, (struct sockaddr *)&client_addr, client_addr_len);
        }
    }

    close(server_socket);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Użycie: %s <host> <port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *host = argv[1];
    int port = atoi(argv[2]);

    start_server(host, port);
    return 0;
}
