#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netdb.h>

int resolve_host(const char *host, int port, struct sockaddr_in *addr) {
    struct addrinfo hints, *res;

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;

    if (getaddrinfo(host, NULL, &hints, &res) != 0) {
        perror("Błąd podczas rozwiązywania nazwy hosta");
        return -1;
    }

    memcpy(addr, res->ai_addr, sizeof(struct sockaddr_in));
    addr->sin_port = htons(port);

    freeaddrinfo(res);
    return 0;
}

void start_client(const char *host, int port) {
    int client_socket;
    struct sockaddr_in server_addr;
    socklen_t addr_len = sizeof(server_addr);
    int sizes[] = {1, 2, 100, 200, 500, 1000, 2000, 4000, 4095, 4096, 4097};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
    unsigned char message[4096];

    if ((client_socket = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Błąd tworzenia gniazda");
        exit(EXIT_FAILURE);
    }

    if (resolve_host(host, port, &server_addr) < 0) {
        fprintf(stderr, "Błąd rozwiązywania nazwy hosta: %s\n", host);
        close(client_socket);
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < num_sizes; i++) {
        int size = sizes[i];
        int content_length = size > 2 ? size - 2 : 0;

        message[0] = (content_length >> 8) & 0xFF;
        message[1] = content_length & 0xFF;

        for (int j = 0; j < content_length; j++) {
            message[2 + j] = 'A' + (j % 26);
        }

        printf("Wysyłanie wiadomości - rozmiar zawartości %d bajtów...\n", size);
        sendto(client_socket, message, size, 0, (const struct sockaddr *)&server_addr, addr_len);

        struct timeval timeout = {1, 0};
        setsockopt(client_socket, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

        char response[128];
        int response_len = recvfrom(client_socket, response, sizeof(response), 0, (struct sockaddr *)&server_addr, &addr_len);

        if (response_len > 0) {
            response[response_len] = '\0';
            if (strcmp(response, "OK") == 0) {
                printf("Otrzymano potwierdzenie dla datagramu o rozmiarze %d bajtów\n", size);
            } else {
                printf("Odpowiedź: %s\n", response);
            }
        } else {
            printf("Brak odpowiedzi\n");

        }

        sleep(1);
    }

    close(client_socket);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Użycie: %s <host> <port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *host = argv[1];
    int port = atoi(argv[2]);

    start_client(host, port);
    return 0;
}

