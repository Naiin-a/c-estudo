import tkinter as tk
from tkinter import messagebox
from bd import BancoDeDados
from cadastro import Cadastro
from datetime import datetime
from adm import mostrar_usuarios

# Iniciar banco
bd = BancoDeDados()
bd.conectar()
bd.criar_tabelas()

# Janela principal
root = tk.Tk()
root.title("Sistema de Login")
root.configure(bg="gray")
root.geometry("300x300")

cpf_adm_logado_global = None

def reiniciar_para_login():
    for widget in root.winfo_children():
        widget.destroy()
    root.deiconify()
    mostrar_tela_login()

def fazer_login():
    global cpf_adm_logado_global
    login = entry_login.get()
    senha = entry_senha.get()
    cpf_adm_logado_global = None

    if not bd.conn:
        if not bd.conectar():
            messagebox.showerror("Erro", "Falha ao conectar ao banco de dados.")
            return

    resultado_login = bd.validar_login(login, senha)

    if resultado_login:
        tipo_usuario = resultado_login[0]
        if tipo_usuario == "adm":
            cpf_adm = resultado_login[1]
            nome_adm = resultado_login[2]
            cpf_adm_logado_global = cpf_adm

            messagebox.showinfo("Sucesso", f"Bem-vindo, {nome_adm} (ADM)")

            root.withdraw()

            painel_adm = tk.Toplevel(root)
            painel_adm.title("Painel do Administrador")
            painel_adm.geometry("700x600")

            def on_adm_close():
                painel_adm.destroy()
                reiniciar_para_login()

            painel_adm.protocol("WM_DELETE_WINDOW", on_adm_close)

            mostrar_usuarios(painel_adm, cpf_adm_logado_global, on_adm_close)

        elif tipo_usuario == "pessoa":
            dados = resultado_login[1:]
            messagebox.showinfo("Sucesso", "Login de usuário bem-sucedido!")
            mostrar_dados_usuario(dados)
        else:
            messagebox.showerror("Erro", "Tipo de usuário desconhecido.")
    else:
        messagebox.showerror("Erro", "Login ou senha inválidos.")

def mostrar_dados_usuario(dados):
    cpf, nome, bloco, numero_ap, email = dados
    for widget in root.winfo_children():
        widget.destroy()

    root.title(f"Bem-vindo, {nome}")
    root.geometry("400x300")
    root.configure(bg="#f0f8ff")

    tk.Label(root, text="Informações do Usuário", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=10)

    info = [
        f"Nome: {nome}",
        f"CPF: {cpf}",
        f"Bloco: {bloco if bloco is not None else 'N/A'}",
        f"Apartamento: {numero_ap if numero_ap is not None else 'N/A'}",
        f"Email: {email}"
    ]

    for text in info:
        tk.Label(root, text=text, anchor="w", bg="#f0f8ff").pack(fill="x", padx=10, pady=2)

    tk.Button(root, text="Logout", command=reiniciar_para_login).pack(pady=10)

def mostrar_tela_login():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Sistema de Login")
    root.geometry("300x300")
    root.configure(bg="gray")

    tk.Label(root, text="Login", font=("Helvetica", 14, "bold"), bg="gray").pack(pady=10)

    global entry_login, entry_senha
    tk.Label(root, text="Login:", bg="gray").pack()
    entry_login = tk.Entry(root)
    entry_login.pack()

    tk.Label(root, text="Senha:", bg="gray").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()

    tk.Button(root, text="Entrar", command=fazer_login).pack(pady=10)

if __name__ == "__main__":
    mostrar_tela_login()
    root.mainloop()
