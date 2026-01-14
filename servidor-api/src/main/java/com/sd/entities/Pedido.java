package com.sd.entities;

public abstract class Pedido implements Avaliavel {
    protected int idPedido;
    protected String nomeCliente;
    protected double preco;
    protected int nota;
    protected String comentario;
    protected String status; 
    private long tempoCriacao;

    public Pedido() {
        this.tempoCriacao = System.currentTimeMillis();
    }

    public Pedido(int id, String cliente, double preco) {
        this.idPedido = id;
        this.nomeCliente = cliente;
        this.preco = preco;
        this.nota = 0;
        this.comentario = "";
        this.tempoCriacao = System.currentTimeMillis();
        this.status = "Criado";
    }

    public int getIdPedido() { return idPedido; }
    public void setIdPedido(int idPedido) { this.idPedido = idPedido; }
    public String getNomeCliente() { return nomeCliente; }
    public void setNomeCliente(String nomeCliente) { this.nomeCliente = nomeCliente; }
    public double getPreco() { return preco; }
    public void setPreco(double preco) { this.preco = preco; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    @Override
    public void avaliar(int nota, String comentario) {
        this.nota = nota;
        this.comentario = comentario;
    }
    
    @Override // Métodos da interface
    public int getNota() { return nota; }
    @Override
    public String getComentario() { return comentario; }
}