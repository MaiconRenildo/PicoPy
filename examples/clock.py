from picopy.pico import PicoPy

#### Configurações e Constantes ####
FRAME_DELAY_MS = 16
TIMER_FONT_SIZE = 12  # Tamanho grande para destacar o relógio

# Inicialização do PicoPy
pico = PicoPy()
world_width, world_height = pico.get_dim_world()
pico.init(True, fullscreen=False)

running = True
event = pico.new_event_object()

print("Cronômetro iniciado! Pressione ESC ou feche a janela para sair.")

while running:
    
    # Captura eventos do teclado/janela para fechar o script com segurança
    while pico.input_event_ask(event, pico.EVENT_ANY):
        if pico.is_quit_event(event) or pico.is_key_event(event, pico.SCANCODE_ESCAPE):
            running = False

    # --- Lógica do Relógio ---
    # get_ticks() retorna o tempo em milissegundos. Dividimos por 1000 para ter segundos.
    total_seconds = pico.get_ticks() // 1000
    
    # Formata o tempo no padrão clássico MM:SS (Minutos:Segundos)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_string = f"{minutes:02d}:{seconds:02d}"

    # --- Renderização ---
    pico.output_clear()
    
    # Configura a fonte e cor do texto (Branco)
    pico.set_color(pico.COLOR_WHITE)
    pico.set_font(None, TIMER_FONT_SIZE)
    
    # Pega as coordenadas exatas do centro da tela do mundo
    center_x, center_y = pico.pos((pico.POS_CENTER, pico.POS_MIDDLE))
    
    # Âncoras cruciais: garantem que o texto use o seu próprio centro como referência.
    # Sem isso, o texto começaria a desenhar a partir do centro para a direita (ficando descentralizado).
    pico.set_anchor_pos((pico.POS_CENTER, pico.POS_MIDDLE))
    pico.set_anchor_rotate((pico.POS_CENTER, pico.POS_MIDDLE))
    pico.set_angle(0)
    
    # Desenha o texto do cronômetro
    pico.output_draw_text((center_x, center_y), time_string)
    
    # Controla a taxa de atualização (FPS)
    pico.input_delay(FRAME_DELAY_MS)

# Finalização limpa do sistema gráfico
pico.init(False)
print("Relógio encerrado.")