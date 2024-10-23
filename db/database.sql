CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    senha VARCHAR(255)
);

CREATE TABLE tarefas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    descricao TEXT,
    status VARCHAR(20),
    data_criacao DATE,
    data_limite DATE,
    prioridade VARCHAR(10),
    categoria VARCHAR(50),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
