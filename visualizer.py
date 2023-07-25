import pygame
import os
from string import ascii_uppercase

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
SQUARE_BLACK_FILENAME = 'square gray dark _png_shadow_128px.png'
SQUARE_WHITE_FILENAME = 'square gray light _png_shadow_128px.png'
TILES_IN_ROW = 8


class Piece:
    filename_dict = {
        'ROOK_BLACK': 'b_rook_png_shadow_128px.png',
        'BISHOP_BLACK': 'b_bishop_png_shadow_128px.png',
        'KNIGHT_BLACK': 'b_knight_png_shadow_128px.png',
        'QUEEN_BLACK': 'b_queen_png_shadow_128px.png',
        'KING_BLACK': 'b_king_png_shadow_128px.png',
        'PAWN_BLACK': 'b_pawn_png_shadow_128px.png',

        'ROOK_WHITE': 'w_rook_png_shadow_128px.png',
        'BISHOP_WHITE': 'w_bishop_png_shadow_128px.png',
        'KNIGHT_WHITE': 'w_knight_png_shadow_128px.png',
        'QUEEN_WHITE': 'w_queen_png_shadow_128px.png',
        'KING_WHITE': 'w_king_png_shadow_128px.png',
        'PAWN_WHITE': 'w_pawn_png_shadow_128px.png'
    }

    def __init__(self, position_notation, piece_name):
        self.position_notation = position_notation
        self.image = pygame.image.load(os.path.join('static', '128px', self.filename_dict[piece_name]))

    def convert_position_notation_to_image_position_indices(self):
        row = ord(self.position_notation[0]) - ord('A')
        column = ord('8') - ord(self.position_notation[1])
        return row, column


class ChessVisualizer:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.__clock = pygame.time.Clock()
        self.__createPieces()
        self.__loadImagesExceptPieces()
        self.is_running = True

    def __createPieces(self):
        self.__pawns_white = [Piece((str(ascii_uppercase[idx-1])+'2'), 'PAWN_WHITE') for idx in range(1, 9)]
        self.__pawns_black = [Piece((str(ascii_uppercase[idx-1])+'7'), 'PAWN_BLACK') for idx in range(1, 9)]
        self.__rooks_white = [Piece('A1', 'ROOK_WHITE'), Piece('H1', 'ROOK_WHITE')]
        self.__rooks_black = [Piece('A8', 'ROOK_BLACK'), Piece('H8', 'ROOK_BLACK')]
        self.__knights_white = [Piece('B1', 'KNIGHT_WHITE'), Piece('G1', 'KNIGHT_WHITE')]
        self.__knights_black = [Piece('B8', 'KNIGHT_BLACK'), Piece('G8', 'KNIGHT_BLACK')]
        self.__bishops_white = [Piece('C1', 'BISHOP_WHITE'), Piece('F1', 'BISHOP_WHITE')]
        self.__bishops_black = [Piece('C8', 'BISHOP_BLACK'), Piece('F8', 'BISHOP_BLACK')]
        self.__queen_white = [Piece('D1', 'QUEEN_WHITE')]
        self.__queen_black = [Piece('D8', 'QUEEN_BLACK')]
        self.__king_white = [Piece('E1', 'KING_WHITE')]
        self.__king_black = [Piece('E8', 'KING_BLACK')]

    def __loadImagesExceptPieces(self):
        self.__square_black = pygame.image.load(os.path.join('static', '128px', SQUARE_BLACK_FILENAME))
        self.__square_white = pygame.image.load(os.path.join('static', '128px', SQUARE_WHITE_FILENAME))

    def visualize(self):
        while self.is_running:
            self.__handle_events()
            self.__refresh_screen()
            self.__render()
            self.__clock.tick(60)
        pygame.quit()

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.VIDEORESIZE:
                self.__resize_images()

    def __resize_images(self):
        width, height = self.__screen.get_size()
        self.__square_black = pygame.transform.scale(self.__square_black, (width / TILES_IN_ROW, height / TILES_IN_ROW))
        self.__square_white = pygame.transform.scale(self.__square_white, (width / TILES_IN_ROW, height / TILES_IN_ROW))

    def __refresh_screen(self):
        self.__screen.fill("black")

    def __render(self):
        width, height = self.__screen.get_size()

        # Board
        for row in range(1, 9):
            for column in range(1, 9):
                square_img = self.__square_white
                if column % 2 == 0:
                    if row % 2 == 1:
                        square_img = self.__square_black
                else:
                    if row % 2 == 0:
                        square_img = self.__square_black

                self.__screen.blit(square_img,
                                   ((column - 1) * (width // TILES_IN_ROW), (row - 1) * (height // TILES_IN_ROW)))

        # Pieces
        pawn_offset_px = 10
        self.__render_pieces(zip(self.__pawns_white, self.__pawns_black), pawn_offset_px)
        knight_offset_px = 6
        self.__render_pieces(zip(self.__knights_white, self.__knights_black), knight_offset_px)
        bishop_offset_px = 0.5
        self.__render_pieces(zip(self.__bishops_white, self.__bishops_black), bishop_offset_px)
        rook_offset_px = 5
        self.__render_pieces(zip(self.__rooks_white, self.__rooks_black), rook_offset_px)
        queen_offset_px = 0
        self.__render_pieces(zip(self.__queen_white, self.__queen_black), queen_offset_px)
        king_offset_px = 0
        self.__render_pieces(zip(self.__king_white, self.__king_black), king_offset_px)

        pygame.display.flip()

    def __render_pieces(self, pieces_zipped, width_offset):
        width, height = self.__screen.get_size()
        for w, b in pieces_zipped:
            idx_w, idx_h = w.convert_position_notation_to_image_position_indices()
            self.__screen.blit(w.image,
                               (idx_w * width // TILES_IN_ROW + width_offset, idx_h * height // TILES_IN_ROW))

            idx_w, idx_h = b.convert_position_notation_to_image_position_indices()
            self.__screen.blit(b.image,
                               (idx_w * width // TILES_IN_ROW + width_offset, idx_h * height // TILES_IN_ROW))
