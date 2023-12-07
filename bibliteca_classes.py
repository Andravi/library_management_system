# representação em terminal por
#    https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python



class Node:
    """Nó genérico"""
    def __init__(self, data = None, pai = None) -> None:
        self.data = data
        self.esquerda:Node = None
        self.direita:Node = None
        self.__pai = pai
        self.bf = 0

    def __le__(self, other):
        if isinstance(other, Node):
            return self.data <= other.data

    def display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.direita is None and self.esquerda is None:
            line = str(self.data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.direita is None:
            lines, n, p, x = self.esquerda.display_aux()
            s = str(self.data)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.esquerda is None:
            lines, n, p, x = self.direita.display_aux()
            s = str(self.data)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.esquerda.display_aux()
        right, m, q, y = self.direita.display_aux()
        s = str(self.data)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


    def set_parent(self, parent) -> None:
        """definir Pai do nó"""
        self.__pai = parent


    def get_parent(self) -> object:
        """Returna o Pai do nó"""
        return self.__pai


    def has_left_child(self):
        """Retorna o nó esquerdo caso exista"""
        return self.esquerda is not None


    def has_right_child(self):
        """Retorna o nó direito caso exista"""
        return self.direita is not None


    def __str__(self) -> str:
        return self.data.__str__()



class ArvoreBinaria:
    """Arvore Binária"""
    def __init__(self):
        self.raiz = None

    def __inserir_filho(self, root:Node, node):
        if node <= root:
            if not root.esquerda:
                root.esquerda = node
                root.esquerda.set_parent(root)
            else:
                self.__inserir_filho(root.esquerda, node)  # sub-árvore esquerda
        else:
            if not root.direita:  # não existe nó a direta (caso base)
                root.direita = node
                root.direita.set_parent(root)
            else:
                self.__inserir_filho(root.direita, node)  # sub-árvore direta

        # Sistema de balanceamento
        root.bf = self.get_bf(root)

        if root.bf > 1:
            if root.esquerda.bf == 1:
                self.girar_direita(root)
            elif root.esquerda.bf == -1:
                self.girar_esquerda_direita(root)

        elif root.bf < -1:
            if root.direita.bf == -1:
                self.girar_esquerda(root)
            elif root.direita.bf == 1:
                self.girar_direita_esquerda(root)

        return node


    def inserir(self, node:Node):
        """Inseri num determinado lugar dependendo da data(Idenficador)"""
        if self.raiz is None:
            self.raiz = node
        else:
            self.__inserir_filho(self.raiz, node)

    def get_bf(self, node: Node):
        """Retorna o fator de balanço de um nó na arvore"""
        return (self.get_height(node.esquerda) - self.get_height(node.direita))


    def get_height(self, node: Node):
        """Retorna a altura de um derterminado node dentro da arvore"""
        if not node:
            return -1
        return 1 + max(self.get_height(node.esquerda), self.get_height(node.direita))


    def encontrar(self, identificador) -> (bool, Node | None):
        """Encontra um determinador Nó com base no seu identificador"""
        no = self.raiz
        while no is not None:
            if identificador == no.data:
                return (True, no)
            if identificador < no.data:
                no = no.esquerda
            else:
                no = no.direita
        return (False, None)

    def __str__(self) :
        self.__display()
        return ""


    def minimum(self, root):
        """Retorna o o menor valor de uma arvore balanceada"""
        result = root
        while result.esquerda:
            result = result.esquerda
        return result


    def successor(self, node:Node):
        """Retorna o proximo nó menor que o atual"""
        belongs, n = self.encontrar(node.data)
        if belongs:
            if n.direita:
                return self.minimum(n.direita)
            else:
                return n
        else:
            return None


    def delete(self, value): # Issue, as vezes retorna o próximo numero
        """Deletar um nó da arvore"""
        belongs, z = self.encontrar(value)
        if belongs:
            if not z.has_left_child() or not z.has_right_child():
                y: Node = z
            else:
                y = self.successor(z)


            y_parent: Node | None = y.get_parent()

            if y.esquerda:
                x = y.esquerda
            else:
                x = y.direita

            if x:
                x.set_parent(y_parent)

            if not y_parent:
                self.raiz = x
            elif y == y_parent.esquerda:
                y_parent.esquerda = x
            else:
                y_parent.direita = x

            if y != z:
                z.data = y.data

            y_parent.bf = self.get_bf(y_parent)
            print(y_parent.data,y_parent.bf)
            if y_parent.bf > 1:
                if y_parent.esquerda.bf in (0, 1):
                    self.girar_direita(y_parent)
                elif y_parent.esquerda.bf == -1:
                    self.girar_esquerda_direita(y_parent)

            elif y_parent.bf < -1:
                if y_parent.direita.bf in (0, -1):
                    self.girar_esquerda(y_parent)
                elif y_parent.direita.bf == 1:
                    self.girar_direita_esquerda(y_parent)

            return y


        return None


    def __display(self):
        lines, *_ = self.raiz.display_aux()
        for line in lines:
            print(line)






    # -2
    def girar_direita(self, node: Node):
        """Realiza o movimento de girar uma subarvore para direita"""
        y:Node = node.esquerda
        node_root: Node = node.get_parent()
        if node_root:
            if node_root.direita == node:
                node_root.direita = y
            else:
                node_root.esquerda = y
        else:
            self.raiz = y

        y.set_parent(node_root)
        node.set_parent(y)

        node.esquerda = y.direita
        if y.direita is not None:
            node.esquerda.set_parent(node)
        y.direita = node


        node.bf = self.get_bf(node)
        y.bf = self.get_bf(y)

        return y


    # +2
    def girar_esquerda(self, node: Node):
        """Realiza o movimento de girar uma subarvore para esquerda"""
        y:Node = node.direita
        node_root: Node = node.get_parent()
        if node_root:
            if node_root.esquerda == node:
                node_root.esquerda = y
            else:
                node_root.direita = y
        else:
            self.raiz = y

        y.set_parent(node_root)
        node.set_parent(y)

        node.direita = y.esquerda
        if y.esquerda is not None:
            node.direita.set_parent(node)
        y.esquerda = node

        node.bf = self.get_bf(node)
        y.bf = self.get_bf(y)
        return y


    def girar_direita_esquerda(self, node:Node):
        """Realiza o movimento para o -2 1 0"""

        self.girar_direita(node.direita)
        self.girar_esquerda(node)


    def girar_esquerda_direita(self, node:Node):
        """Realiza o movimento para o -2 -11 0"""
        self.girar_esquerda(node.esquerda)
        self.girar_direita(node)


    def get_elementos(self):
        elementos = []
        self._ler_in_order(self.raiz, elementos)
        # print(f'-> {elementos}')

        return elementos


    # reprecentaçãográfica da Arvore
    def _ler_in_order(self, node, lista) -> list:


        self.__ler_a_esquerda(node, lista)
        lista.append(node)
        self.__ler_a_direita(node, lista)

        return lista


    def __ler_a_esquerda(self, node:Node, lista):
        if not node.esquerda:
            return
        else:
            self._ler_in_order(node.esquerda, lista)


    def __ler_a_direita(self, node, lista):
        if not node.direita:
            return
        else:
            self._ler_in_order(node.direita, lista)



# t = ArvoreBinaria()


# for i in range(0, 63):
#     t.inserir(Node(i))



# print("===================")
# print(t)
# print(t.encontrar(20)[1].bf)



class Usuario(Node):
    """Usuários"""
    def __init__(self, nome, cpf, email):
        super().__init__(cpf)
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.livro_em_pose: Livro = None


    def __str__(self):
        return f"{self.nome} - {self.cpf}"


class Livro(Node):
    """livro"""
    def __init__(self, titulo, autor, ano_publicacao, categoria, ):
        super().__init__(titulo)
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.categoria = categoria
        self.disponibilidade = True



    def __str__(self):
        return f"{self.titulo} - {self.autor} - {self.ano_publicacao}"

    def __repr__(self):
        return f"{self.titulo} - {self.autor} - {self.ano_publicacao}"



class ArvoreLivros(ArvoreBinaria):
    """Arvore de Usuários sadsadsadsadsa"""
    def __init__(self):
        super().__init__()
        self.__tot_livros:int = None


    def __len__(self) -> int:
        if self.__tot_livros < 0:
            return -1
        return  self.__tot_livros


    def inserir_livro(self, titulo, autor, ano_publicacao, categoria):
        """ Inserir Usuários na arvore"""
        return super().inserir(Livro(titulo, autor, ano_publicacao, categoria))

    def buscar_livro(self, identificador) -> [Livro | None]:
        #Tentar fazer uma busca binaria
        # # Fazer uma solução maior log(N)
        achados: list = []
        if self.encontrar_livro_por_titulo(identificador):
            achados.append(self.encontrar_livro_por_titulo(identificador))


        # lógica para pegar possivel nome de autor com esse nome
        

        return achados
         # Fazer uma busca na arvore completamente para fazer a busca

    def encontrar_livro_por_autor(self, autor) -> (bool, Livro | None):
        """Encontra um determinador Nó com base no seu identificador"""
        livros = self.get_elementos()
        out = []
        for livro in livros:
            if livro.autor == autor:
                out.append(livro)
        return out


    def encontrar_livro_por_titulo(self, titulo) -> Livro | None:
        """Encontra um determinador Nó com base no seu identificador"""
        livro = super().encontrar(titulo)
        return None if not livro[0] else livro[1]


class ArvoreUsuarios(ArvoreBinaria):
    """Arvore de Usuários sadsadsadsadsa"""
    def __init__(self):
        super().__init__()
        self.__tot_usuarios:int = None


    def __len__(self) -> int:
        if self.__tot_usuarios < 0:
            return -1
        return  self.__tot_usuarios

    def inserir_usuario(self, nome, cpf, email):
        """ Inserir Usuários na arvore"""
        return super().inserir(Usuario(nome, cpf, email))


    def tem_emprestado(self, titulo):
        """Retorna usuario que possui o emprestimo"""
        users = super().get_elementos()
        for u in users:
            if u.livro_em_pose.titulo == titulo:
                return u
        return False
