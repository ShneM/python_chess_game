import abc
import copy


class Game:
    def __init__(self):
        self.list_tab = [["  "] * 8 for _ in range(8)]
        self.list_pieces = []
        self.str_couleur_actuelle = "b"
        self.bool_peut_bouger = False

        for y, c in zip((0, 7, 1, 6), ("n", "b") * 2):
            for x in range(8):
                list_position = [y, x]

                if y in (0, 7):
                    if x in (1, 6):
                        self.list_tab[y][x] = Chevalier(list_position, c)
                    elif x in (2, 5):
                        self.list_tab[y][x] = Fou(list_position, c)
                    elif x == 3:
                        self.list_tab[y][x] = Reine(list_position, c)
                    elif x == 4:
                        self.list_tab[y][x] = Roi(list_position, c)
                    else:
                        self.list_tab[y][x] = Tour(list_position, c)
                else:
                    self.list_tab[y][x] = Pion(list_position, c)

        for y in 0, 1, 6, 7:
            self.list_pieces.extend(self.list_tab[y])

        self.obj_roi_n = self.list_pieces[4]
        self.obj_roi_b = self.list_pieces[28]

    def fn_afficher_tableau(self):
        print(f"\n  {'_' * 55}{' ' * 47}{'_' * 55}")

        for y in range(8):
            print(f" |{'      |' * 8}{' ' * 45}|{'      |' * 8}"
                  f"\n |  {self.list_tab[y][0]}  |  {self.list_tab[y][1]}  |  {self.list_tab[y][2]}  |  "
                  f"{self.list_tab[y][3]}  |  {self.list_tab[y][4]}  |  {self.list_tab[y][5]}  |  "
                  f"{self.list_tab[y][6]}  |  {self.list_tab[y][7]}  | {8 - y}{' ' * 41}{y + 1} |  "
                  f"{self.list_tab[7 - y][7]}  |  {self.list_tab[7 - y][6]}  |  {self.list_tab[7 - y][5]}  |  "
                  f"{self.list_tab[7 - y][4]}  |  {self.list_tab[7 - y][3]}  |  {self.list_tab[7 - y][2]}  |  "
                  f"{self.list_tab[7 - y][1]}  |  {self.list_tab[7 - y][0]}  |"
                  f"\n |{'______|' * 8}{' ' * 45}|{'______|' * 8}")

        print(f"    A      B      C      D      E      F      G      H{' ' * 52}"
              "H      G      F      E      D      C      B      A")

    def fn_generer_mvt_valides(self) -> None:
        for e in self.list_pieces:
            if e.str_couleur == self.str_couleur_actuelle:
                list_mvt_valides = e.fn_mvt_valides(self.list_tab)

                for e2 in list_mvt_valides:
                    obj_copie_game = copy.deepcopy(self)
                    obj_copie_game.fn_executer_mvt(obj_copie_game.list_tab[e.int_y][e.int_x], e2)

                    if not obj_copie_game.fn_echec():
                        e.list_mvt_valides.append(e2)
                        self.bool_peut_bouger = True

    def fn_echec(self) -> bool:
        if self.str_couleur_actuelle == "b":
            obj_roi = self.obj_roi_b
        else:
            obj_roi = self.obj_roi_n

        for e in self.list_pieces:
            if e.str_couleur != self.str_couleur_actuelle:
                list_mvt_valides = e.fn_mvt_valides(self.list_tab)

                if obj_roi.list_position in list_mvt_valides:
                    return True

                for x in 2, 3, 5, 6:
                    list_danger_roque = [obj_roi.int_y, x]

                    if list_danger_roque in list_mvt_valides:
                        Roi.list_danger_roque.append(list_danger_roque)

        return False

    def fn_executer_mvt(self, p_piece, p_destination: list) -> None:
        int_y2, int_x2 = p_destination

        if isinstance(p_piece, Pion) and int_x2 != p_piece.int_x and self.list_tab[int_y2][int_x2] == "  ":
            self.list_pieces.remove(self.list_tab[p_piece.int_y][int_x2])
            self.list_tab[p_piece.int_y][int_x2] = "  "
        elif isinstance(p_piece, Roi):
            int_vx = int_x2 - p_piece.int_x

            if int_vx == 2:
                int_x_tour = 7
            elif int_vx == -2:
                int_x_tour = 0

            if abs(int_vx) == 2:
                obj_tour = self.list_tab[p_piece.int_y][int_x_tour]
                obj_tour.list_position[1] = obj_tour.int_x = p_piece.int_x + int_vx // 2
                self.list_tab[p_piece.int_y][obj_tour.int_x] = obj_tour
                self.list_tab[p_piece.int_y][int_x_tour] = "  "

        obj_destination = self.list_tab[int_y2][int_x2]

        if obj_destination != "  ":
            self.list_pieces.remove(obj_destination)

        self.list_tab[int_y2][int_x2] = p_piece
        self.list_tab[p_piece.int_y][p_piece.int_x] = "  "
        p_piece.list_position = p_piece.int_y, p_piece.int_x = p_destination


class Piece(abc.ABC):
    def __init__(self, p_position: list, p_couleur: str):
        self.list_position = self.int_y, self.int_x = p_position
        self.str_couleur = p_couleur
        self.list_mvt_valides = []

    @abc.abstractmethod
    def fn_mvt_valides(self, p_tab: list) -> list:
        pass


class Pion(Piece):
    list_en_passant = []

    def __init__(self, p_position: list, p_couleur: str):
        super().__init__(p_position, p_couleur)
        self.bool_premier_mvt = True

        if self.str_couleur == "b":
            self.int_d = -1  # Direction
        else:
            self.int_d = 1

    def __str__(self):
        return f"P{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list) -> list:
        list_mvt_valides = []
        int_y2 = self.int_y + 1 * self.int_d

        for vx in -1, 1:
            int_x2 = self.int_x + vx

            if -1 < int_x2 < 8:
                obj_destination = p_tab[int_y2][int_x2]

                if (
                    self.str_couleur != str(obj_destination)[1] != " " or
                    obj_destination == "  " and Pion.list_en_passant == [self.int_y, int_x2]
                ):
                    list_mvt_valides.append([int_y2, int_x2])

        if p_tab[int_y2][self.int_x] == "  ":
            list_mvt_valides.append([int_y2, self.int_x])
            int_y2 += self.int_d

            if self.bool_premier_mvt and p_tab[int_y2][self.int_x] == "  ":
                list_mvt_valides.append([int_y2, self.int_x])

        return list_mvt_valides


class Tour(Piece):
    def __init__(self, p_position: list, p_couleur: str):
        super().__init__(p_position, p_couleur)
        self.bool_premier_mvt = True

    def __str__(self):
        return f"T{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list) -> list:
        list_mvt_valides = []

        for vy in -1, 0, 1:
            if vy:
                tuple_vx = 0,
            else:
                tuple_vx = -1, 1

            for vx in tuple_vx:
                int_y2 = self.int_y + vy
                int_x2 = self.int_x + vx

                while -1 < int_y2 < 8 and -1 < int_x2 < 8:
                    obj_destination = p_tab[int_y2][int_x2]

                    if self.str_couleur != str(obj_destination)[1]:
                        list_mvt_valides.append([int_y2, int_x2])

                    if obj_destination != "  ":
                        break

                    int_y2 += vy
                    int_x2 += vx

        return list_mvt_valides


class Chevalier(Piece):
    def __str__(self):
        return f"C{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list) -> list:
        list_mvt_valides = []

        for vy in -2, -1, 1, 2:
            if abs(vy) == 1:
                int_vx = 2
            else:
                int_vx = 1

            for vx in -int_vx, int_vx:
                int_y2 = self.int_y + vy
                int_x2 = self.int_x + vx

                if -1 < int_y2 < 8 and -1 < int_x2 < 8 and self.str_couleur != str(p_tab[int_y2][int_x2])[1]:
                    list_mvt_valides.append([int_y2, int_x2])

        return list_mvt_valides


class Fou(Piece):
    def __str__(self):
        return f"F{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list) -> list:
        list_mvt_valides = []
        tuple_v = -1, 1

        for vy in tuple_v:
            for vx in tuple_v:
                int_y2 = self.int_y + vy
                int_x2 = self.int_x + vx

                while -1 < int_y2 < 8 and -1 < int_x2 < 8:
                    obj_destination = p_tab[int_y2][int_x2]

                    if self.str_couleur != str(obj_destination)[1]:
                        list_mvt_valides.append([int_y2, int_x2])

                    if obj_destination != "  ":
                        break

                    int_y2 += vy
                    int_x2 += vx

        return list_mvt_valides


class Reine(Piece):
    def __str__(self):
        return f"r{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list) -> list:
        return (
            Tour(self.list_position, self.str_couleur).fn_mvt_valides(p_tab) +
            Fou(self.list_position, self.str_couleur).fn_mvt_valides(p_tab)
        )


class Roi(Piece):
    bool_echec = None
    list_danger_roque = []

    def __init__(self, p_position: list, p_couleur: str):
        super().__init__(p_position, p_couleur)
        self.bool_premier_mvt = True

    def __str__(self):
        return f"R{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list) -> list:
        list_mvt_valides = []
        tuple_vy = -1, 0, 1

        for vy in tuple_vy:
            if vy:
                tuple_vx = tuple_vy
            else:
                tuple_vx = -1, 1

            for vx in tuple_vx:
                int_y2 = self.int_y + vy
                int_x2 = self.int_x + vx

                if -1 < int_y2 < 8 and -1 < int_x2 < 8 and self.str_couleur != str(p_tab[int_y2][int_x2])[1]:
                    list_mvt_valides.append([int_y2, int_x2])

        if self.bool_premier_mvt and not Roi.bool_echec:
            obj_pit = p_tab[self.int_y][0]  # Position initiale de la tour

            if (
                isinstance(obj_pit, Tour) and obj_pit.bool_premier_mvt and
                p_tab[self.int_y][1] == p_tab[self.int_y][2] == p_tab[self.int_y][3] == "  " and
                [self.int_y, 2] not in Roi.list_danger_roque and [self.int_y, 3] not in Roi.list_danger_roque
            ):
                list_mvt_valides.append([self.int_y, self.int_x - 2])

            obj_pit = p_tab[self.int_y][7]

            if (
                isinstance(obj_pit, Tour) and obj_pit.bool_premier_mvt and
                p_tab[self.int_y][5] == p_tab[self.int_y][6] == "  " and
                [self.int_y, 5] not in Roi.list_danger_roque and [self.int_y, 6] not in Roi.list_danger_roque
            ):
                list_mvt_valides.append([self.int_y, self.int_x + 2])

        return list_mvt_valides
