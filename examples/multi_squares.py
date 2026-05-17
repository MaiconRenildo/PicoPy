import sys

from picopy.pico import PicoPy


pico = PicoPy()
pico.init(True)

# use default values for window and world dimensions
square_size = 1  # Equivalente a uma unidade da grade logica
frame_delay_ms = 16

pico.set_color(pico.COLOR_BLUE)
pico.set_style(pico.DRAW_FILL)

# Calcula a posicao do quadrado no centro do mundo logico
center_x, center_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))

running = True
event = pico.new_event_object()

print("Multiplos quadrados azuis serao desenhados. Feche a janela para sair.")

while running:
    # Processa eventos de forma nao bloqueante
    while pico.input_event_ask(event, pico.EVENT_ANY):
        if pico.is_quit_event(event):
            running = False
            print("Evento QUIT detectado. Fechando...")
        # Outros eventos, como cliques do mouse, sao ignorados neste exemplo.

    # Logica de desenho
    pico.output_clear()

    # Quadrado no centro
    original_anchor = pico.get_anchor_pos()
    pico.set_anchor_pos((pico.POS_CENTER, pico.POS_MIDDLE))
    center_x, center_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
    pico.output_draw_rect((int(center_x), int(center_y), square_size, square_size))
    

    # Quadrado no canto superior esquerdo
    pico.set_anchor_pos(original_anchor)
    top_left_x, top_left_y = pico.pos((pico.POS_LEFT, pico.POS_TOP))
    pico.output_draw_rect((top_left_x, top_left_y, square_size, square_size))

    # Quadrado no canto superior direito
    pico.set_anchor_pos((pico.POS_RIGHT, pico.POS_TOP))
    top_right_x, top_right_y = pico.pos((pico.POS_RIGHT, pico.POS_TOP))
    pico.output_draw_rect((top_right_x, top_right_y, square_size, square_size))

    # Quadrado no canto inferior esquerdo
    pico.set_anchor_pos((pico.POS_LEFT, pico.POS_BOTTOM))
    bottom_left_x, bottom_left_y = pico.pos((pico.POS_LEFT, pico.POS_BOTTOM))
    pico.output_draw_rect((bottom_left_x, bottom_left_y, square_size, square_size))

    # Quadrado no canto inferior direito
    pico.set_anchor_pos((pico.POS_RIGHT, pico.POS_BOTTOM))
    bottom_right_x, bottom_right_y = pico.pos((pico.POS_RIGHT, pico.POS_BOTTOM))
    pico.output_draw_rect((bottom_right_x, bottom_right_y, square_size, square_size))
    
    # Restaura a âncora global original
    pico.set_anchor_pos(original_anchor)

    pico.output_present()
    pico.input_delay(frame_delay_ms)

pico.init(False)
print("Pico-SDL encerrado.")