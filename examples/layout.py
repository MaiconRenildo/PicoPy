from picopy.pico import PicoPy

# Constantes de cor (RGBA)
COLOR_BACKGROUND = (240, 238, 252, 255)
COLOR_BORDER = (70, 60, 170, 255)
COLOR_TEXT = (255, 255, 255, 255)
COLOR_PANEL = (255, 255, 255, 255)

FRAME_DELAY_MS = 100

pico = PicoPy()
pico.set_title("Experimento 2")
pico.init(True)
pico.set_size((800, 600), (320, 240))
pico.set_grid(False)
pico.set_font(None, 8)  # fonte embutida (tiny)

while True:
    # --- Renderização ---
    world_w, world_h = pico.pos((100, 100))

    pico.set_style(pico.DRAW_FILL)
    pico.set_color(COLOR_BACKGROUND)
    pico.set_anchor_pos((pico.POS_LEFT, pico.POS_TOP))
    pico.output_draw_rect((0, 0, world_w, world_h))

    # Footer / popup
    foot_w, foot_h = pico.pos((53, 33))
    margin_x, margin_y = pico.pos((10, 10))
    foot = (world_w - margin_x, world_h - margin_y, foot_w, foot_h)

    pico.set_anchor_pos((pico.POS_RIGHT, pico.POS_BOTTOM))
    pico.set_style(pico.DRAW_FILL)
    pico.set_color(COLOR_PANEL)
    pico.output_draw_rect(foot)

    pico.set_style(pico.DRAW_STROKE)
    pico.set_color(COLOR_BORDER)
    pico.output_draw_rect(foot)

    # Título
    title_pos = pico.pos_ext((50, 0), foot, (pico.POS_RIGHT, pico.POS_BOTTOM))
    pico.set_anchor_pos((pico.POS_CENTER, pico.POS_TOP))
    pico.output_draw_text((title_pos[0], title_pos[1] + 8), "Atualizacao")

    # Botões
    btn_w = foot_w * 26 // 100
    btn_h = foot_h * 20 // 100
    btn1_pos = pico.pos_ext((33, 70), foot, (pico.POS_RIGHT, pico.POS_BOTTOM))
    btn2_pos = pico.pos_ext((67, 70), foot, (pico.POS_RIGHT, pico.POS_BOTTOM))

    pico.set_anchor_pos((pico.POS_CENTER, pico.POS_MIDDLE))
    pico.set_style(pico.DRAW_FILL)
    pico.set_color(COLOR_BORDER)
    pico.output_draw_rect((btn1_pos[0], btn1_pos[1], btn_w, btn_h))
    pico.output_draw_rect((btn2_pos[0], btn2_pos[1], btn_w, btn_h))

    pico.set_color(COLOR_TEXT)
    pico.output_draw_text(btn1_pos, "Depois")
    pico.output_draw_text(btn2_pos, "OK")

    pico.input_delay(FRAME_DELAY_MS)

# pico.init(False)