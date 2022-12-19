import threading
import time
import random

class Game(object):
    def __init__(self, player1, player2):
        # O tabuleiro é um array de arrays que representa as posições
        # dos navios e dos tiros. Cada posição pode ser um dos seguintes:
        # '.' para água, 'X' para tiro, 'O' para navio
        self.board = [['.' for _ in range(10)] for _ in range(10)]
        self.p1 = player1
        self.p2 = player2

        self.has_ships = 0 # quantidade de navios
        # O semáforo é usado para proteger o acesso ao tabuleiro
        self.board_lock = threading.Semaphore(1)
        self.jogadas = 0

    def lock_board(self):
        self.board_lock.acquire()
    def free_board(self):
        self.board_lock.release()

    def add_ship(self, x, y):
        # Adquire o lock do tabuleiro
        self.lock_board()

        # Verifica se a posição está disponível
        if self.board[x][y] != '.':
            print("Posição já ocupada!")
            self.free_board()
            return

        # Adiciona o navio na posição
        self.board[x][y] = 'O'
        print(f"Navio adicionado com sucesso! -> Posição ({x},{y})")
        self.has_ships += 1

        # Libera o lock do tabuleiro
        self.free_board()
    
    def check_ships(self):
        print("Navios Restantes: ", self.has_ships, end="\n\n")
        is_over = True if self.has_ships == 0 else False
        if is_over: 
            print("Jogo Acabou!!")
            exit()

    def main(self):
        # Cria duas threads para simular dois jogadores
       

        threads = []
        threads.append(threading.Thread(target=self.p1.run_player, args=(self, self.p2 )))
        threads.append(threading.Thread(target=self.p2.run_player, args=(self, self.p1 )))

        for i in range(5):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            self.add_ship(x,y)
        
        # Inicia as threads
        for thread in threads:
            thread.start()
            thread.join()



class Player(object):
    def __init__(self, name: str) -> None:
        self.name = name
        pass

    # A função shoot tenta atirar em uma determinada posição do tabuleiro
    def shoot(self, x, y, game: Game):
        # Adquire o lock do tabuleiro
        game.lock_board()

        # Verifica se a posição já foi atingida
        if game.board[x][y] == 'X':
            print(f'{self.name} tenta jogar na posição ({x},{y}), mas já foi atingida!')
            game.free_board()
            return            
        # Verifica se acertou um navio
        if game.board[x][y] == 'O':
            print(f'{self.name} acertou um navio na posição ({x},{y}) \o/!')
            game.has_ships -= 1
        else:
            print(f'ERROU! {self.name} só acertou água na posição ({x},{y})!')

        # Atira na posição
        game.board[x][y] = 'X'

        # Libera o lock do tabuleiro
        game.free_board() 

    # A função run_player simula o jogador atirando em posições aleatórias
    def run_player(self, game: Game, next_player):
        if game.has_ships == 0:
            exit()

        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            self.shoot(x, y, game)

            time.sleep(0.5)
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            next_player.shoot(x, y, game) # para poder ter os dois jogadores jogando, não ficar apenas um só
            
            game.check_ships()

p1 = Player("Rogério")
p2 = Player("Raimunda")

game = Game(p1, p2)
game.main()