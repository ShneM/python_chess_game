import abc
import copy


class Game:
    def __init__(self):
        self.list_board = [["  "] * 8 for _ in range(8)]
        self.list_pieces = []
        self.str_actual_color = "w"
        self.bool_can_move = False

        for y, c in zip((0, 7, 1, 6), ("b", "w") * 2):
            for x in range(8):
                list_position = [y, x]

                if y in (0, 7):
                    if x in (1, 6):
                        self.list_board[y][x] = Knight(list_position, c)
                    elif x in (2, 5):
                        self.list_board[y][x] = Bishop(list_position, c)
                    elif x == 3:
                        self.list_board[y][x] = Queen(list_position, c)
                    elif x == 4:
                        self.list_board[y][x] = King(list_position, c)
                    else:
                        self.list_board[y][x] = Rook(list_position, c)
                else:
                    self.list_board[y][x] = Pawn(list_position, c)

        for y in 0, 1, 6, 7:
            self.list_pieces.extend(self.list_board[y])

        self.obj_b_king = self.list_pieces[4]
        self.obj_w_king = self.list_pieces[28]

    def fn_display_board(self):
        print(f"\n  {'_' * 55}{' ' * 47}{'_' * 55}")

        for y in range(8):
            print(f" |{'      |' * 8}{' ' * 45}|{'      |' * 8}"
                  f"\n |  {self.list_board[y][0]}  |  {self.list_board[y][1]}  |  {self.list_board[y][2]}  |  "
                  f"{self.list_board[y][3]}  |  {self.list_board[y][4]}  |  {self.list_board[y][5]}  |  "
                  f"{self.list_board[y][6]}  |  {self.list_board[y][7]}  | {8 - y}{' ' * 41}{y + 1} |  "
                  f"{self.list_board[7 - y][7]}  |  {self.list_board[7 - y][6]}  |  {self.list_board[7 - y][5]}  |  "
                  f"{self.list_board[7 - y][4]}  |  {self.list_board[7 - y][3]}  |  {self.list_board[7 - y][2]}  |  "
                  f"{self.list_board[7 - y][1]}  |  {self.list_board[7 - y][0]}  |"
                  f"\n |{'______|' * 8}{' ' * 45}|{'______|' * 8}")

        print(f"    A      B      C      D      E      F      G      H{' ' * 52}"
              "H      G      F      E      D      C      B      A")

    def fn_generate_valid_moves(self) -> None:
        for e in self.list_pieces:
            if e.str_color == self.str_actual_color:
                list_valid_moves = e.fn_valid_moves(self.list_board)

                for e2 in list_valid_moves:
                    obj_game_copy = copy.deepcopy(self)
                    obj_game_copy.fn_execute_move(obj_game_copy.list_board[e.int_y][e.int_x], e2)

                    if not obj_game_copy.fn_check():
                        e.list_valid_moves.append(e2)
                        self.bool_can_move = True

    def fn_check(self) -> bool:
        if self.str_actual_color == "w":
            obj_king = self.obj_w_king
        else:
            obj_king = self.obj_b_king

        for e in self.list_pieces:
            if e.str_color != self.str_actual_color:
                list_valid_moves = e.fn_valid_moves(self.list_board)

                if obj_king.list_position in list_valid_moves:
                    return True

                for x in 2, 3, 5, 6:
                    list_castling_danger = [obj_king.int_y, x]

                    if list_castling_danger in list_valid_moves:
                        King.list_castling_danger.append(list_castling_danger)

        return False

    def fn_execute_move(self, p_piece, p_destination: list) -> None:
        int_y2, int_x2 = p_destination

        if isinstance(p_piece, Pawn) and int_x2 != p_piece.int_x and self.list_board[int_y2][int_x2] == "  ":
            self.list_pieces.remove(self.list_board[p_piece.int_y][int_x2])
            self.list_board[p_piece.int_y][int_x2] = "  "
        elif isinstance(p_piece, King):
            int_vx = int_x2 - p_piece.int_x

            if int_vx == 2:
                int_rook_x = 7
            elif int_vx == -2:
                int_rook_x = 0

            if abs(int_vx) == 2:
                obj_rook = self.list_board[p_piece.int_y][int_rook_x]
                obj_rook.list_position[1] = obj_rook.int_x = p_piece.int_x + int_vx // 2
                self.list_board[p_piece.int_y][obj_rook.int_x] = obj_rook
                self.list_board[p_piece.int_y][int_rook_x] = "  "

        obj_destination = self.list_board[int_y2][int_x2]

        if obj_destination != "  ":
            self.list_pieces.remove(obj_destination)

        self.list_board[int_y2][int_x2] = p_piece
        self.list_board[p_piece.int_y][p_piece.int_x] = "  "
        p_piece.list_position = p_piece.int_y, p_piece.int_x = p_destination


class Piece(abc.ABC):
    def __init__(self, p_position: list, p_color: str):
        self.list_position = self.int_y, self.int_x = p_position
        self.str_color = p_color
        self.list_valid_moves = []

    @abc.abstractmethod
    def fn_valid_moves(self, p_board: list) -> list:
        pass


class Pawn(Piece):
    list_en_passant = []

    def __init__(self, p_position: list, p_color: str):
        super().__init__(p_position, p_color)
        self.bool_first_move = True

        if self.str_color == "w":
            self.int_d = -1  # Direction
        else:
            self.int_d = 1

    def __str__(self):
        return f"{self.str_color}P"

    def fn_valid_moves(self, p_board: list) -> list:
        list_valid_moves = []
        int_y2 = self.int_y + 1 * self.int_d

        for vx in -1, 1:
            int_x2 = self.int_x + vx

            if -1 < int_x2 < 8:
                obj_destination = p_board[int_y2][int_x2]

                if (
                    self.str_color != str(obj_destination)[0] != " " or
                    obj_destination == "  " and Pawn.list_en_passant == [self.int_y, int_x2]
                ):
                    list_valid_moves.append([int_y2, int_x2])

        if p_board[int_y2][self.int_x] == "  ":
            list_valid_moves.append([int_y2, self.int_x])
            int_y2 += self.int_d

            if self.bool_first_move and p_board[int_y2][self.int_x] == "  ":
                list_valid_moves.append([int_y2, self.int_x])

        return list_valid_moves


class Rook(Piece):
    def __init__(self, p_position: list, p_color: str):
        super().__init__(p_position, p_color)
        self.bool_first_move = True

    def __str__(self):
        return f"{self.str_color}R"

    def fn_valid_moves(self, p_board: list) -> list:
        list_valid_moves = []

        for vy in -1, 0, 1:
            if vy:
                tuple_vx = 0,
            else:
                tuple_vx = -1, 1

            for vx in tuple_vx:
                int_y2 = self.int_y + vy
                int_x2 = self.int_x + vx

                while -1 < int_y2 < 8 and -1 < int_x2 < 8:
                    obj_destination = p_board[int_y2][int_x2]

                    if self.str_color != str(obj_destination)[0]:
                        list_valid_moves.append([int_y2, int_x2])

                    if obj_destination != "  ":
                        break

                    int_y2 += vy
                    int_x2 += vx

        return list_valid_moves


class Knight(Piece):
    def __str__(self):
        return f"{self.str_color}N"

    def fn_valid_moves(self, p_board: list) -> list:
        list_valid_moves = []

        for vy in -2, -1, 1, 2:
            if abs(vy) == 1:
                int_vx = 2
            else:
                int_vx = 1

            for vx in -int_vx, int_vx:
                int_y2 = self.int_y + vy
                int_x2 = self.int_x + vx

                if -1 < int_y2 < 8 and -1 < int_x2 < 8 and self.str_color != str(p_board[int_y2][int_x2])[0]:
                    list_valid_moves.append([int_y2, int_x2])

        return list_valid_moves


class Bishop(Piece):
    def __str__(self):
        return f"{self.str_color}B"

    def fn_valid_moves(self, p_board: list) -> list:
        list_valid_moves = []
        tuple_v = -1, 1

        for vy in tuple_v:
            for vx in tuple_v:
                int_y2 = self.int_y + vy
                int_x2 = self.int_x + vx

                while -1 < int_y2 < 8 and -1 < int_x2 < 8:
                    obj_destination = p_board[int_y2][int_x2]

                    if self.str_color != str(obj_destination)[0]:
                        list_valid_moves.append([int_y2, int_x2])

                    if obj_destination != "  ":
                        break

                    int_y2 += vy
                    int_x2 += vx

        return list_valid_moves


class Queen(Piece):
    def __str__(self):
        return f"{self.str_color}Q"

    def fn_valid_moves(self, p_board: list) -> list:
        return (
            Rook(self.list_position, self.str_color).fn_valid_moves(p_board) +
            Bishop(self.list_position, self.str_color).fn_valid_moves(p_board)
        )


class King(Piece):
    bool_check = None
    list_castling_danger = []

    def __init__(self, p_position: list, p_color: str):
        super().__init__(p_position, p_color)
        self.bool_first_move = True

    def __str__(self):
        return f"{self.str_color}K"

    def fn_valid_moves(self, p_board: list) -> list:
        list_valid_moves = []
        tuple_vy = -1, 0, 1

        for vy in tuple_vy:
            if vy:
                tuple_vx = tuple_vy
            else:
                tuple_vx = -1, 1

            for vx in tuple_vx:
                int_y2 = self.int_y + vy
                int_x2 = self.int_x + vx

                if -1 < int_y2 < 8 and -1 < int_x2 < 8 and self.str_color != str(p_board[int_y2][int_x2])[0]:
                    list_valid_moves.append([int_y2, int_x2])

        if self.bool_first_move and not King.bool_check:
            obj_rip = p_board[self.int_y][0]  # Rook's initial position

            if (
                isinstance(obj_rip, Rook) and obj_rip.bool_first_move and
                p_board[self.int_y][1] == p_board[self.int_y][2] == p_board[self.int_y][3] == "  " and
                [self.int_y, 2] not in King.list_castling_danger and [self.int_y, 3] not in King.list_castling_danger
            ):
                list_valid_moves.append([self.int_y, self.int_x - 2])

            obj_rip = p_board[self.int_y][7]

            if (
                isinstance(obj_rip, Rook) and obj_rip.bool_first_move and
                p_board[self.int_y][5] == p_board[self.int_y][6] == "  " and
                [self.int_y, 5] not in King.list_castling_danger and [self.int_y, 6] not in King.list_castling_danger
            ):
                list_valid_moves.append([self.int_y, self.int_x + 2])

        return list_valid_moves
