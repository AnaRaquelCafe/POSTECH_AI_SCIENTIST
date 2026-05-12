-- 1. Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS globaltech_db;
USE globaltech_db;

-- 2. Tabela de Clientes
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    data_cadastro DATE,
    cidade VARCHAR(100)
) ENGINE=InnoDB;

-- 3. Tabela de Produtos
CREATE TABLE produtos (
    id_produto INT PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    preco DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;

-- 4. Tabela de Pedidos
CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY,
    id_cliente INT,
    data_pedido DATE,
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (id_cliente) 
        REFERENCES clientes(id_cliente) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 5. Tabela de Itens do Pedido (Tabela Fato)
CREATE TABLE itens_pedido (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT,
    id_produto INT,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_item_pedido FOREIGN KEY (id_pedido) 
        REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    CONSTRAINT fk_item_produto FOREIGN KEY (id_produto) 
        REFERENCES produtos(id_produto)
) ENGINE=InnoDB;