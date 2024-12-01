#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>

#define BUFFER_SIZE 1024

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

typedef struct TreeNode {
    uint16_t data_16;
    uint32_t data_32;
    char text[20];
    struct TreeNode* left;
    struct TreeNode* right;
} TreeNode;

int serialize_tree(TreeNode* root, uint8_t* buffer, int offset) {
    if (root == NULL) {
        return offset;
    }

    uint16_t data_16 = htons(root->data_16);
    uint32_t data_32 = htonl(root->data_32);

    memcpy(buffer + offset, &data_16, sizeof(data_16));
    offset += sizeof(data_16);
    
    memcpy(buffer + offset, &data_32, sizeof(data_32));
    offset += sizeof(data_32);
    
    memcpy(buffer + offset, root->text, sizeof(root->text));
    offset += sizeof(root->text);
    
    offset = serialize_tree(root->left, buffer, offset);
    offset = serialize_tree(root->right, buffer, offset);
    
    return offset;
}

TreeNode* create_sample_tree() {
    TreeNode* root = (TreeNode*)malloc(sizeof(TreeNode));
    root->data_16 = 1;
    root->data_32 = 100;
    strcpy(root->text, "root");
    
    root->left = (TreeNode*)malloc(sizeof(TreeNode));
    root->left->data_16 = 2;
    root->left->data_32 = 200;
    strcpy(root->left->text, "left");
    root->left->left = NULL;
    root->left->right = NULL;

    root->right = (TreeNode*)malloc(sizeof(TreeNode));
    root->right->data_16 = 3;
    root->right->data_32 = 300;
    strcpy(root->right->text, "right");
    root->right->left = NULL;
    root->right->right = NULL;

    return root;
}

int start_client(const char *host, int port) {
    int sockfd;
    struct sockaddr_in server_addr;
    uint8_t buffer[BUFFER_SIZE];
    TreeNode* root = create_sample_tree();
    int data_size = serialize_tree(root, buffer, 0);

    sleep(3); // zeby serwer mogl wystartować pierwszy

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Błąd tworzenia gniazda");
        exit(EXIT_FAILURE);
    }

    if (resolve_host(host, port, &server_addr) < 0) {
        fprintf(stderr, "Błąd rozwiązywania nazwy hosta: %s\n", host);
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_pton(AF_INET, host, &server_addr.sin_addr);

    if (connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection failed");
        exit(EXIT_FAILURE);
    }
    send(sockfd, buffer, data_size, 0);
    printf("Tree data sent to server.\n");

    close(sockfd);
    return 0;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Użycie: %s <host> <port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    
    const char *host = argv[1];
    int port = atoi(argv[2]);
    start_client(host, port);

    return 0;
}
