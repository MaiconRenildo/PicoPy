from picopy.pico import PicoPy
pico = PicoPy()

pico.init(True)
pico.set_color((255, 0, 0, 255))

for i in range(5):
    pico.output_draw_rect((2 + i * 12, 10, 10, 10))
    pico.input_delay(500)

pico.init(False)