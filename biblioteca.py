"""Sistema de Biblioteca"""
from datetime import datetime
from bibliteca_classes import ArvoreLivros, ArvoreUsuarios, Livro

# A principio deixarei as propriedades publicas para poder visualizar melhor as informações
class Biblioteca:
    """ Sistema de biblioteca """
    usuarios: ArvoreUsuarios = ArvoreUsuarios()
    livros: ArvoreLivros = ArvoreLivros()
    emprestimos: dict = {}
    devolucoes: dict = {}


    def inserir_usuario(self, nome:str, cpf:int, email:str):
        """Inserir usuarios para poderem usar a biblioteca"""
        self.usuarios.inserir_usuario(nome, cpf, email)


    def inserir_livro(self, titulo, autor, ano_publicacao, categoria):
        """Inserir usuarios para poderem usar a biblioteca"""
        self.livros.inserir_livro(titulo, autor, ano_publicacao, categoria)


    def buscar_usuario(self, cpf):
        """procura o usuario com o cpf informado"""
        return self.usuarios.encontrar(cpf)[1]


    def buscar_livro_por_titulo(self, titulo):
        """ Retorna o livro atraves do título, caso seja 100% igual"""
        return self.livros.encontrar_livro_por_titulo(titulo)


    def buscar_livro_por_autor(self, nome) -> list:
        """Buscar lirvos feitos por um determinado autor"""
        return self.livros.encontrar_livro_por_autor(nome)


    def emprestar(self, titulo, cpf):
        """ Realiza um Empréstimo a um usuário já cadastrado"""
        user_cadastrado, user = self.usuarios.encontrar(cpf)
        livro_cadastrado, livro = self.livros.encontrar(titulo)

        if livro_cadastrado:
            if user_cadastrado:
                if livro.disponibilidade:
                    if not user.livro_em_pose:
                        data = datetime.now()
                        livro.disponibilidade = False

                        user.livro_em_pose = livro
                        self.emprestimos[f"{data}_{user.cpf}"] = {
                            "livro": livro,
                            "usuario": user,
                            "data": data
                        }
                        # * Imprime um registro do empréstimo na tela.
                        print(f"O {livro.titulo} foi emprestado para {user.nome}\n")
                    else:
                        print(f"O {user.nome} já esta com o livro ({user.livro_em_pose}) emprestado.\n")
                else:
                    # * Informa que o livro solicitado não está disponível.
                    print(f"O {livro.titulo} se encontra indisponível\n")
            else:
                # * Imprime que o usuário solicitante não existe.
                print("O usuário solicitante do emprestimo não está cadastrado\n")
                print("Por favor, realize o cadastro e tente novamente.\n")
        else:
            # * Imprime que o livro solicitado não existe.
            print("O livro solicitado não está cadastrado\n")
            print("Por favor, registre a obra e tente novamente.\n")
        # if titulo.disponivel -> emprestar pro usuario com o Cpf


    def devolver(self, titulo, cpf):
        """Devolver um lívro"""
        livro_cadastrado, livro = self.livros.encontrar(titulo)
        user_cadastrado, usuario = self.usuarios.encontrar(cpf)

        if livro_cadastrado:
            if user_cadastrado:
                if not livro.disponibilidade and livro == usuario.livro_em_pose:
                    livro.disponibilidade = True
                    usuario.livro_em_pose = None
                    data = datetime.now()
                    self.devolucoes[f"{data}_{usuario.cpf}"] = {
                            "livro": livro,
                            "usuario": usuario,
                            "data": data
                        }

                    print(f"O {livro.titulo} foi devolvido por {usuario.nome}\n")
                else:
                    print(f"O {livro.titulo} não se encontra em posse do usuário {usuario.nome}\n")
            else:
                # * Imprime que o usuário solicitante não existe.
                print("O usuário solicitante do emprestimo não está cadastrado\n")
                print("Por favor, realize o cadastro e tente novamente.\n")
        else:
            # * Imprime que o livro solicitado não existe.
            print("O livro solicitado não está cadastrado\n")
            print("Por favor, registre a obra e tente novamente.\n")


    def mostrar_relatorio_emprestimo(self):
        """Mostrar historico de emprestimos feitos"""
        print("################ Relatório de Empréstimos ##################")
        for info in self.emprestimos.values():
            print(f'O livro {info["livro"].titulo}, foi emprestado para {info["usuario"].nome} na data {(info["data"])}')
        print("\n")


    def mostrar_relatorio_devolucoes(self):
        """Mostrar historico de emprestimos feitos"""
        print("################ Relatório de Devoluções ###################")
        for info in self.devolucoes.values():
            print(f'O livro {info["livro"].titulo}, foi devolvido por {info["usuario"].nome} em {(info["data"])}')
        print("\n")


    def mostrar_livros_emprestados(self):
        """ mostrar_livros_emprestados """
        livros: [Livro] = self.livros.get_elementos()


        for l in livros:
            if not l.disponibilidade:
                usuario = self.usuarios.tem_emprestado(l.titulo)
                print(f'{l.titulo} está emprestado para {usuario.nome}')




if __name__ == "__main__":

    bib: Biblioteca = Biblioteca()

    bib.inserir_usuario("Carlos Douglas", 20202020, "carlinhos@gmail,com")
    bib.inserir_usuario("joão", 200, "joze@outlook.com")
    bib.inserir_usuario("Joze", 202, "joaoze@outlook.com")
    bib.inserir_livro("O Senhor dos Anéis",
                        "J.R.R. Tolkien",
                        "1954",
                        ["fantasia", "aventura"]
                    )
    bib.inserir_livro("Romeu e Julieta",
                        "Sheskpare",
                        "1870",
                        ["romance", "mediaval"]
                    )
    bib.inserir_livro("O Senhor do Anéis",
                        "J.R.R. Tolkien",
                        "1954",
                        ["fantasia", "aventura"]
                    )


    # Buscas
    # print(bib.buscar_livro_por_titulo("Romeu e Julieta"))
    # print(bib.buscar_livro_por_autor("J.R.R. Tolkien"))
    # print(bib.buscar_usuario(200).email)
    # print("===================")


    # Emprestimos
    bib.emprestar(titulo='Romeu e Julieta', cpf=200)
    print("===================")
    # bib.emprestar(titulo='Romeu e Julieta', cpf=201)
    # print("===================")
    # bib.emprestar(titulo='O Senhor do Anéis', cpf=200)
    # print("===================")
    bib.emprestar(titulo='O Senhor do Anéis', cpf=202)
    print("===================")
    bib.devolver(titulo='O Senhor do Anéis', cpf=202)

    # Arvores
    print("=================== Visualização da Arvore Livro")
    print(bib.livros)

    print("=================== Visualização da Arvore Usuários")
    print(bib.usuarios)

    bib.mostrar_relatorio_emprestimo()
    bib.mostrar_relatorio_devolucoes()
    bib.mostrar_livros_emprestados()
