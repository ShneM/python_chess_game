import Classes_Echec as C
import os

dict_coordonees = {
    "a8": [0, 0], "b8": [0, 1], "c8": [0, 2], "d8": [0, 3], "e8": [0, 4], "f8": [0, 5], "g8": [0, 6], "h8": [0, 7],
    "a7": [1, 0], "b7": [1, 1], "c7": [1, 2], "d7": [1, 3], "e7": [1, 4], "f7": [1, 5], "g7": [1, 6], "h7": [1, 7],
    "a6": [2, 0], "b6": [2, 1], "c6": [2, 2], "d6": [2, 3], "e6": [2, 4], "f6": [2, 5], "g6": [2, 6], "h6": [2, 7],
    "a5": [3, 0], "b5": [3, 1], "c5": [3, 2], "d5": [3, 3], "e5": [3, 4], "f5": [3, 5], "g5": [3, 6], "h5": [3, 7],
    "a4": [4, 0], "b4": [4, 1], "c4": [4, 2], "d4": [4, 3], "e4": [4, 4], "f4": [4, 5], "g4": [4, 6], "h4": [4, 7],
    "a3": [5, 0], "b3": [5, 1], "c3": [5, 2], "d3": [5, 3], "e3": [5, 4], "f3": [5, 5], "g3": [5, 6], "h3": [5, 7],
    "a2": [6, 0], "b2": [6, 1], "c2": [6, 2], "d2": [6, 3], "e2": [6, 4], "f2": [6, 5], "g2": [6, 6], "h2": [6, 7],
    "a1": [7, 0], "b1": [7, 1], "c1": [7, 2], "d1": [7, 3], "e1": [7, 4], "f1": [7, 5], "g1": [7, 6], "h1": [7, 7]
}
bool_jeu = True

while bool_jeu:
    bool_partie = True
    obj_game = C.Game()
    bool_message = False
    str_message = None
    input("\n Assurez-vous de mettre full screen (WinKey + Up) et appuyez sur Enter: ")
    C.Roi.bool_echec = False
    obj_game.fn_generer_mvt_valides()

    while bool_partie:
        os.system("cls")
        obj_game.fn_afficher_tableau()

        if bool_message:
            if obj_game.str_couleur_actuelle == "b":
                print(f"\n {str_message}")
            else:
                print(f"\n{' ' * 103}{str_message}")

        if C.Roi.bool_echec:
            if obj_game.str_couleur_actuelle == "b":
                print("\n Échec!")
            else:
                print(f"\n{' ' * 103}Échec!")

        # Position =====================================================================================================
        if obj_game.str_couleur_actuelle == "b":
            str_position = input("\n Entrez la position de la pièce à bouger (a1-h8): ").lower()
        else:
            str_position = input(f"\n{' ' * 103}Entrez la position de la pièce à bouger (a1-h8): ").lower()

        if str_position not in dict_coordonees:
            bool_message = True
            str_message = "Valeur inexacte."
            continue

        list_position = dict_coordonees[str_position]
        int_y = list_position[0]
        obj_position = obj_game.list_tab[int_y][list_position[1]]

        if str(obj_position)[1] != obj_game.str_couleur_actuelle:
            bool_message = True
            str_message = "La position ne correspond pas à une pièce de votre couleur."
            continue

        if not obj_position.list_mvt_valides:
            bool_message = True
            str_message = "Cette pièce n'a aucune possibilité de mouvement."
            continue

        # Destination ==================================================================================================
        print()

        if obj_game.str_couleur_actuelle == "n":
            print(" " * 102, end="")

        for i in range(len(obj_position.list_mvt_valides)):
            for e in dict_coordonees:
                if dict_coordonees[e] == obj_position.list_mvt_valides[i]:
                    if i != len(obj_position.list_mvt_valides) - 1:
                        if i == 13:
                            print(f" {e},")

                            if obj_game.str_couleur_actuelle == "n":
                                print(" " * 102, end="")
                        else:
                            print(f" {e},", end="")
                    else:
                        print(f" {e}")

        if obj_game.str_couleur_actuelle == "b":
            str_destination = input("\n Entrez la destination de la pièce à bouger (a1-h8): ").lower()
        else:
            str_destination = input(f"\n{' ' * 103}Entrez la destination de la pièce à bouger (a1-h8): ").lower()

        if str_destination not in dict_coordonees:
            bool_message = True
            str_message = "Valeur inexacte."
            continue

        list_destination = dict_coordonees[str_destination]

        if list_destination not in obj_position.list_mvt_valides:
            bool_message = True
            str_message = "Mouvement invalide."
            continue

        # Exécution du mouvement =======================================================================================
        obj_game.fn_executer_mvt(obj_position, list_destination)
        bool_message = False
        obj_game.bool_peut_bouger = False
        C.Pion.list_en_passant.clear()
        C.Roi.list_danger_roque.clear()

        for e in obj_game.list_pieces:
            e.list_mvt_valides.clear()

        if isinstance(obj_position, C.Pion):
            obj_position.bool_premier_mvt = False

            if abs(obj_position.int_y - int_y) == 2:
                C.Pion.list_en_passant.extend(list_destination)
            elif obj_position.int_y in (0, 7):
                os.system("cls")
                obj_game.fn_afficher_tableau()

                while True:
                    if obj_game.str_couleur_actuelle == "b":
                        str_promotion = input("\n Entrez la première lettre de la pièce en laquelle vous voulez"
                                              "\n que votre pion se transforme (t/c/f/r): ").lower()
                    else:
                        print(f"\n{' ' * 103}Entrez la première lettre de la pièce en laquelle vous voulez"
                              f"\n{' ' * 103}", end="")
                        str_promotion = input("que votre pion se transforme (t/c/f/r): ").lower()

                    if str_promotion == "t":
                        obj_piece = C.Tour(list_destination, obj_game.str_couleur_actuelle)
                    elif str_promotion == "c":
                        obj_piece = C.Chevalier(list_destination, obj_game.str_couleur_actuelle)
                    elif str_promotion == "f":
                        obj_piece = C.Fou(list_destination, obj_game.str_couleur_actuelle)
                    elif str_promotion == "r":
                        obj_piece = C.Reine(list_destination, obj_game.str_couleur_actuelle)
                    else:
                        os.system("cls")
                        obj_game.fn_afficher_tableau()

                        if obj_game.str_couleur_actuelle == "b":
                            print("\n Valeur inexacte.")
                        else:
                            print(f"\n{' ' * 103}Valeur inexacte.")

                        continue

                    obj_game.list_tab[obj_position.int_y][obj_position.int_x] = obj_piece
                    obj_game.list_pieces[obj_game.list_pieces.index(obj_position)] = obj_piece
                    break
        elif isinstance(obj_position, (C.Tour, C.Roi)):
            obj_position.bool_premier_mvt = False

        if obj_game.str_couleur_actuelle == "b":
            obj_game.str_couleur_actuelle = "n"
        else:
            obj_game.str_couleur_actuelle = "b"

        C.Roi.bool_echec = obj_game.fn_echec()
        obj_game.fn_generer_mvt_valides()

        # Analyse du jeu ===============================================================================================
        if not obj_game.bool_peut_bouger:
            os.system("cls")
            obj_game.fn_afficher_tableau()
            bool_partie = False

            if C.Roi.bool_echec:
                if obj_game.str_couleur_actuelle == "b":
                    print("\n Échec et mat!")
                else:
                    print(f"\n{' ' * 103}Échec et mat!")
            else:
                print(f"\n{' ' * 58}Match nul!")

            if input(f"\n{' ' * 58}Voulez-vous continuer? (o/n): ").lower() == "o":
                os.system("cls")
            else:
                bool_jeu = False

os.system("cls")
print("\n Au-revoir!", end="\n ")
os.system("pause")
