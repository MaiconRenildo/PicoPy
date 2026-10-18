from picopy.pico import PicoPy

pico = PicoPy()
pico.init(True)
pico.set_size((800, 600), (320, 240))
pico.set_grid(False)
pico.set_font(None, 8)

# Desenha o fundo da janela
pico.set_style(pico.DRAW_FILL) 
pico.set_color((240, 238, 252, 255)) 
pico.output_draw_rect((0, 0, 800, 600)) 

# Desenha o primeiro retângulo de preenchimento
pico.set_anchor_pos((pico.POS_RIGHT, pico.POS_BOTTOM))
pico.set_style(pico.DRAW_FILL)
pico.set_color((240, 238, 252, 255)) 
pico.output_draw_rect((296, 216, 170, 80))

# Desenha o retângulo de borda
pico.set_style(pico.DRAW_STROKE)
pico.set_color((70, 60, 170, 255))
pico.output_draw_rect((296, 216, 170, 80))

# Desenha o texto "Atualizacao"
pico.set_anchor_pos((pico.POS_CENTER, pico.POS_TOP))
pico.output_draw_text((211, 144), "Atualizacao")

# Desenha os retângulos dos botões
pico.set_anchor_pos((pico.POS_CENTER, pico.POS_MIDDLE))
pico.set_style(pico.DRAW_FILL)
pico.output_draw_rect((183, 192, 44, 16))
pico.output_draw_rect((240, 192, 44, 16))

# Desenha o texto dos botões
pico.set_color((255, 255, 255, 255))
pico.output_draw_text((183, 192), "Depois")
pico.output_draw_text((240, 192), "OK")
while True:
    pico.input_delay(100)

    