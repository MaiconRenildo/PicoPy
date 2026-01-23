import sys
import ctypes
import sdl2  # type: ignore
import sdl2.sdlttf as sdlttf  # type: ignore
import sdl2.sdlmixer as sdlmixer  # type: ignore
import sdl2.sdlimage as sdlimage  # type: ignore
from sdl2 import SDL_GetError # type: ignore
import sdl2.sdlgfx as sdlgfx
from state import PicoState
from constants import (
    PICO_TITLE,
    PICO_LEFT,
    PICO_TOP,
    PICO_FILL,
    PICO_STROKE,
    PICO_CLIP_RESET,
    PICO_BYTES_PER_PIXEL_RGBA32,
    PICO_DIM_KEEP,
    PICO_COLOR_GRAY,
)
from tests.utils import PicoTest
from tiny_ttf import pico_tiny_ttf, pico_tiny_ttf_len


class PicoPy(PicoTest):
    def __init__(self):
        self.S = PicoState()
        self.WIN = None  # Janela(objeto da janela do sistema operacional)
        self.REN = None  # Renderer(responsável por desenhar na janela)
        self.TEX = None  # Textura(superfície de renderização alvo)
        self._pico_hash: dict | None = None  # Tabela hash

    ####################### PRIVATE FUNCTIONS #######################
    def _noclip(self):
        """Verifica se não há clip ativo"""
        return (self.S.clip[2] == PICO_CLIP_RESET[2]) or (self.S.clip[3] == PICO_CLIP_RESET[3])

    def _get_current_clip(self):
        """Obtém a região de clipping atual do renderizador e retorna um objeto SDL_Rect"""
        clip = sdl2.SDL_Rect()
        sdl2.SDL_RenderGetClipRect(self.REN, clip)
        return clip

    def _define_clip(self, clip):
        """Define a região de clipping do renderizador"""
        sdl2.SDL_RenderSetClipRect(self.REN, clip)

    def _get_current_target(self):
        """Obtém o target de renderização atual do renderizador(None=janela(BackBuffer))"""
        return sdl2.SDL_GetRenderTarget(self.REN)

    def _define_target(self, target, w, h):
        """Define o target de renderização e o tamanho lógico"""
        # Parece ser o padrão do pico-sdl, mas não é claro o motivo.
        if target is None:
            sdl2.SDL_SetRenderTarget(self.REN, target)
            sdl2.SDL_RenderSetLogicalSize(self.REN, w, h)
        else:
            sdl2.SDL_RenderSetLogicalSize(self.REN, w, h)
            sdl2.SDL_SetRenderTarget(self.REN, target)

    def _clear_target_with_defined_color(self):
        """Limpa o target atual com a cor definida previamente"""
        sdl2.SDL_RenderClear(self.REN)

    def _change_target_to_window(self):
        """Direciona o desenho para a janela(BackBuffer)
        
        Obs: Ao mudar target, o SDL reseta automaticamente o clip para o tamanho total
        do novo target.
        """
        self._define_target(None, self.S.dim_window[0], self.S.dim_window[1]) # None = direciona para a janela física do sistema

    def _change_target_to_TEX(self):
        """Direciona o desenho de volta para a TEX"""
        zoom_dim = self._zoom()
        self._define_target(self.TEX, zoom_dim[0], zoom_dim[1])

    def _restore_render_state(self, clip, target):
        """Restaura o estado do renderer"""
        if target is None:
            self._change_target_to_window()
        else:
            # Se for uma textura, usamos o tamanho do zoom
            zoom_dim = self._zoom()
            self._define_target(target, zoom_dim[0], zoom_dim[1])
        self._define_clip(clip)

    def _pico_set_color(self, color):
        """Define a cor de desenho do renderizador"""
        sdl2.SDL_SetRenderDrawColor(self.REN, color[0], color[1], color[2], color[3])

    def _restore_draw_color(self):
        """Restaura a cor de desenho original (S.color_draw)"""
        self._pico_set_color(self.S.color_draw)

    def _create_texture(self, w, h):
        """Cria uma nova textura"""
        return sdl2.SDL_CreateTexture(
            self.REN,
            sdl2.SDL_PIXELFORMAT_RGBA32,
            sdl2.SDL_TEXTUREACCESS_TARGET,
            w, h
        )

    def _setup_aux_texture(self, w, h):
        """
        Cria uma textura auxiliar para desenho intermediário. Equivalente ao _draw_aux(w, h) no pico-sdl
        """
        aux = self._create_texture(w, h)
        sdl2.SDL_SetTextureBlendMode(aux, sdl2.SDL_BLENDMODE_BLEND)
        sdl2.SDL_SetRenderTarget(self.REN, aux)
        # Limpa com transparente
        sdl2.SDL_SetRenderDrawColor(self.REN, 0, 0, 0, 0)
        sdl2.SDL_RenderClear(self.REN)
        # Restaura a cor de desenho para o aux
        self._restore_draw_color()
        return aux

    def _pico_output_draw_tex(self, pos, tex, dim):
        """Desenha uma textura com todas as transformações(crop, scale, rotation, etc)"""
        
        # Obtém as dimensões originais da textura
        # tw e th armazenarão a largura e altura reais da textura carregada
        tw, th = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_QueryTexture(tex, None, None, tw, th)
        tw, th = tw.value, th.value

        # Recorte da imagem de origem
        # S.crop define qual pedaço da textura original queremos desenhar (x, y, w, h)
        cx, cy, cw, ch = self.S.crop
        if cw == 0: cw = tw  # Se w=0, usa a largura total da textura
        if ch == 0: ch = th  # Se h=0, usa a altura total da textura
        # src_rect é o retângulo que "recorta" a imagem de origem
        src_rect = sdl2.SDL_Rect(cx, cy, cw, ch)

        # Tamanho final do desenho
        # aqui que decidimos qual será o tamanho(rw, rh) do desenho no mundo
        rw, rh = 0, 0
        if dim == PICO_DIM_KEEP: # mantém o tamanho definido no recorte (crop)
            rw, rh = cw, ch
        elif dim[0] == 0: # se a largura for 0, calcula a largura proporcional baseada na altura desejada
            rw = int(cw * (dim[1] / ch))
            rh = dim[1]
        elif dim[1] == 0: # se a altura for 0, calcula a altura proporcional baseada na largura desejada
            rh = int(ch * (dim[0] / cw))
            rw = dim[0]
        else: # usa as dimensões exatas passadas no parâmetro 'dim'
            rw, rh = dim

        # aplica o fator de escala definido em S.scale
        rw = (self.S.scale[0] * rw) // 100
        rh = (self.S.scale[1] * rh) // 100

        # Calcula a posição final(rx, ry) onde o objeto será desenhado
        # _X e _Y já embutem o cálculo do Anchor e do Scroll
        rx = self._X(pos[0], rw)
        ry = self._Y(pos[1], rh)
        # dst_rect é o retângulo de destino na tela(onde e em qual tamanho desenhar)
        dst_rect = sdl2.SDL_Rect(int(rx), int(ry), int(rw), int(rh))

        # Define o ponto exato(em relação ao objeto) sobre o qual ele irá girar.
        # por padrão, se for (50, 50), ele girará em torno do seu próprio centro geométrico
        rot_center = sdl2.SDL_Point(
            int((self.S.anchor_rotate[0] * rw) // 100),
            int((self.S.anchor_rotate[1] * rh) // 100)
        )

        # Espelhamento
        # Configura se a imagem deve ser espelhada horizontalmente ou verticalmente
        flip = sdl2.SDL_FLIP_NONE
        angle_offset = 0
        if self.S.flip[0] and self.S.flip[1]: # Flip em ambos os eixos é simulado rotacionando
            # a imagem em 180 graus e aplicando um flip vertical
            angle_offset = 180
            flip = sdl2.SDL_FLIP_VERTICAL
        elif self.S.flip[1]: # Apenas flip vertical
            flip = sdl2.SDL_FLIP_VERTICAL
        elif self.S.flip[0]: # Apenas flip horizontal
            flip = sdl2.SDL_FLIP_HORIZONTAL

        # Renderização final
        # Copia a textura para o renderizador aplicando todas as transformações:
        # ângulo atual + offset de flip, centro de rotação e modo de espelhamento.
        sdl2.SDL_RenderCopyEx(
            self.REN, tex,
            src_rect, dst_rect,
            float(self.S.angle + angle_offset),
            rot_center,
            flip
        )
        self._pico_output_present(0)

    def _copy_TEX_to_window(self):
        """Copia a textura principal do mundo(TEX) para a janela(BackBuffer)"""
        sdl2.SDL_RenderCopy(self.REN, self.TEX, None, None)

    def _show_on_screen(self):
        """Troca o conteúdo do FrontBuffer pelo BackBuffer, exibindo o que foi preparado"""
        sdl2.SDL_RenderPresent(self.REN)

    def _zoom(self):
        """Calcula dimensões com zoom aplicado"""
        return (
            self.S.dim_world[0] * self.S.zoom[0] // 100,
            self.S.dim_world[1] * self.S.zoom[1] // 100
        )

    def _show_grid(self):
        """Mostra a grade se estiver habilitada"""
        if not self.S.grid:
            return
        
        self._pico_set_color(PICO_COLOR_GRAY)
        
        zoom_dim = self._zoom()
        
        # Linhas verticais
        if (self.S.dim_window[0] % zoom_dim[0] == 0) and (zoom_dim[0] < self.S.dim_window[0]):
            step = self.S.dim_window[0] // zoom_dim[0]
            for i in range(0, self.S.dim_window[0] + 1, step):
                sdl2.SDL_RenderDrawLine(self.REN, i, 0, i, self.S.dim_window[1])
        
        # Linhas horizontais
        if (self.S.dim_window[1] % zoom_dim[1] == 0) and (zoom_dim[1] < self.S.dim_window[1]):
            step = self.S.dim_window[1] // zoom_dim[1]
            for j in range(0, self.S.dim_window[1] + 1, step):
                sdl2.SDL_RenderDrawLine(self.REN, 0, j, self.S.dim_window[0], j)
        
        self._restore_draw_color()

    def _pico_output_present(self, force):
        """Apresenta o conteúdo renderizado da textura TEX para a tela"""
        if self.S.expert and not force:
            return
        
        # Salva
        clip = self._get_current_clip()

        # Apresenta
        self._change_target_to_window()
        self._pico_set_color(PICO_COLOR_GRAY)
        self._clear_target_with_defined_color()
        self._copy_TEX_to_window() # Seta o conteúdo no BackBuffer da janela
        self._show_grid() # Desenha a grade POR CIMA(no BackBuffer da janela)
        self._show_on_screen()
        
        # Restaura
        self._restore_draw_color()
        self._change_target_to_TEX()
        self._define_clip(clip)

    # Funções auxiliares para cálculo de posição
    def _hanchor(self, x, w):
        """Calcula posição horizontal com anchor aplicado"""
        return x - (self.S.anchor_pos[0] * w) // 100

    def _vanchor(self, y, h):
        """Calcula posição vertical com anchor aplicado"""
        return y - (self.S.anchor_pos[1] * h) // 100

    def _X(self, v, w):
        """Calcula coordenada X final (com anchor e scroll)"""
        return self._hanchor(v, w) - self.S.scroll[0]

    def _Y(self, v, h):
        """Calcula coordenada Y final (com anchor e scroll)"""
        return self._vanchor(v, h) - self.S.scroll[1]
    #################################################################

    ######################### API FUNCTIONS #########################
    def pico_init(self, on):
        """
        Inicializa ou termina o pico-sdl
        
        Args:
            on: 1 para inicializar, 0 para terminar
        """
        # global WIN, REN, TEX, _pico_hash
        
        if on:
            # Criar hash
            self._pico_hash = {}
            
            # Inicializar SDL
            self.pico_assert(sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) == 0)
            
            # Criar janela
            self.WIN = sdl2.SDL_CreateWindow(
                PICO_TITLE.encode('utf-8'),
                sdl2.SDL_WINDOWPOS_UNDEFINED, # Posição X da janela -> sistema que define
                sdl2.SDL_WINDOWPOS_UNDEFINED, # Posição Y da janela -> sistema que define
                self.S.dim_window[0], # Largura da janela
                self.S.dim_window[1], # Altura da janela
                sdl2.SDL_WINDOW_SHOWN # Janela visível ao ser criada
            )
            self.pico_assert(self.WIN is not None)
            
            # Criar renderer
            self.REN = sdl2.SDL_CreateRenderer(
                self.WIN,
                -1, # Índice do driver de renderização -> -1 para usar o primeiro driver disponível
                sdl2.SDL_RENDERER_ACCELERATED # Usar aceleração de hardware(GPU) quando disponível
            )
            self.pico_assert(self.REN is not None)
            
            # Configurar blend mode
            sdl2.SDL_SetRenderDrawBlendMode(self.REN, sdl2.SDL_BLENDMODE_BLEND) # Define o modo de blend(transparência)
            
            # Inicializar TTF -> TrueType Font
            sdlttf.TTF_Init()
            
            # Inicializar Mixer(Sistema de áudio)
            sdlmixer.Mix_OpenAudio(
                22050,  # Frequência de amostragem(Hz): quantas amostras por segundo
                sdl2.AUDIO_S16SYS,  # Formato
                2,  # Canais: 1 = mono(um canal), 2 = estéreo(dois canais: esquerdo + direito)
                1024  # Tamanho do buffer: quantas amostras processadas por vez
            )
            
            # Configurar zoom
            self.pico_set_zoom(self.S.zoom) # Aqui a textura TEX é definida como target
            
            # Carregar fonte embutida(tiny_ttf)
            self.pico_set_font(None, 0)

            # Limpar tela
            self.pico_output_clear()
            
            # Limpar eventos
            sdl2.SDL_PumpEvents()
            sdl2.SDL_FlushEvents(sdl2.SDL_FIRSTEVENT, sdl2.SDL_LASTEVENT)
            
            # Tornar janela redimensionável
            sdl2.SDL_SetWindowResizable(self.WIN, 1)
            
        else:
            if self.S.font_ttf is not None:
                sdlttf.TTF_CloseFont(self.S.font_ttf)
                self.S.font_ttf = None
            
            sdlmixer.Mix_CloseAudio()
            sdlttf.TTF_Quit()
            
            # Destruir textura antes do renderer
            if self.TEX:
                sdl2.SDL_DestroyTexture(self.TEX)
                self.TEX = None
            
            if self.REN:
                sdl2.SDL_DestroyRenderer(self.REN)
                self.REN = None
            
            if self.WIN:
                sdl2.SDL_DestroyWindow(self.WIN)
                self.WIN = None
            
            sdl2.SDL_Quit()
            
            # Limpar hash
            self._pico_hash = None

    def pico_assert(self, condition):
        """Assert com mensagem de erro SDL"""
        if not condition:
            error = SDL_GetError()
            if error:
                print(f"SDL ERROR: {error.decode('utf-8')}", file=sys.stderr)
            assert False, "SDL ERROR"

    def pico_output_clear(self):
        """Limpa o target atual com a cor de limpeza"""
        if self.REN:
            self._pico_set_color(self.S.color_clear)
            if self._noclip():
                self._clear_target_with_defined_color() # Limpa o target inteiro
            else:
                clip = self._get_current_clip()
                sdl2.SDL_RenderFillRect(self.REN, clip) # Preenche a região do clip com a cor de limpeza
            self._restore_draw_color()
            self._pico_output_present(0)

    def pico_output_present(self):
        """Apresenta o conteúdo renderizado na tela"""
        if self.REN and self.TEX:
            self._pico_output_present(1)

    def pico_set_zoom(self, pct):
        """Define o zoom"""
        old = self._zoom()
        self.S.zoom = pct
        new = self._zoom()
        
        dx = new[0] - old[0]
        dy = new[1] - old[1]
        
        # Ajusta scroll baseado no anchor
        self.S.scroll = (
            self.S.scroll[0] - (dx * self.S.anchor_pos[0] // 100),
            self.S.scroll[1] - (dy * self.S.anchor_pos[1] // 100)
        )

        if self.TEX:
            sdl2.SDL_DestroyTexture(self.TEX)
        
        # Criar nova textura
        self.TEX = self._create_texture(new[0], new[1])
        self.pico_assert(self.TEX is not None)
        
        self._define_target(self.TEX, new[0], new[1])
        
        # Define clip
        clip = sdl2.SDL_Rect(0, 0, new[0], new[1])
        self._define_clip(clip)

    def pico_get_dim_window(self):
        """Obtém as dimensões da janela."""
        return self.S.dim_window

    def pico_set_dim_window(self, dim):
        """Define as dimensões da janela.

        Args:
            dim: (w, h) As novas dimensões da janela.
        """
        if self.S.fullscreen:
            return
        self.S.dim_window = dim
        sdl2.SDL_SetWindowSize(self.WIN, dim[0], dim[1])
        zoom_dim = self._zoom()
        clip = sdl2.SDL_Rect(0, 0, zoom_dim[0], zoom_dim[1])
        self._define_clip(clip)

    def pico_get_dim_world(self):
        """Obtém as dimensões do mundo lógico."""
        return self.S.dim_world

    def pico_set_dim_world(self, dim):
        """Define as dimensões do mundo lógico.

        Args:
            dim: (w, h) As novas dimensões do mundo lógico.
        """
        self.S.dim_world = dim
        self.pico_set_zoom(self.S.zoom)

    def pico_output_screenshot(self, path=None):
        """Tira um screenshot da tela"""
        zoom_dim = self._zoom()
        rect = sdl2.SDL_Rect(0, 0, zoom_dim[0], zoom_dim[1])
        return self.pico_output_screenshot_ext(path, rect)

    def pico_output_screenshot_ext(self, path, rect):
        """Tira um screenshot de uma região específica da tela"""
        from datetime import datetime
        
        if path is None:
            path = f"pico-sdl-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
        
        if not self.REN or not self.TEX:
            return None
        
        clip = self._get_current_clip()
        current_target = self._get_current_target()
        
        # Cria textura temporária com o mesmo tamanho da janela
        # Parâmetros: renderer, formato(RGBA 32 bits), acesso(target=permite renderizar nela), largura, altura
        temp_texture = self._create_texture(self.S.dim_window[0], self.S.dim_window[1])
        if not temp_texture:
            self._restore_render_state(clip, current_target)
            return None

        # A partir daqui, o conteúdo da textura TEX é renderizado para a textura temporária temp_texture
        # Assim como as operações de zoom, scroll, leitura de pixels, etc. são aplicadas na textura temporária temp_text
        self._define_target(temp_texture, self.S.dim_window[0], self.S.dim_window[1])
        self._pico_set_color(PICO_COLOR_GRAY)
        self._clear_target_with_defined_color()
        self._copy_TEX_to_window()
        self._show_grid() # Desenha a grade na textura temporária, pois a grade não é desenhada na TEXT

        # Lê pixels da textura temporária
        screen_rect = sdl2.SDL_Rect(0, 0, self.S.dim_window[0], self.S.dim_window[1])  # Retângulo: x=0, y=0, largura=janela[0], altura=janela[1]
        buf = (ctypes.c_uint8 * (PICO_BYTES_PER_PIXEL_RGBA32 * screen_rect.w * screen_rect.h))() # Calcula o tamanho do buffer em bytes
        # Lê do temp_texture a região definida em screen_rect e salva no buffer buf
        sdl2.SDL_RenderReadPixels(self.REN, screen_rect, sdl2.SDL_PIXELFORMAT_RGBA32, buf, PICO_BYTES_PER_PIXEL_RGBA32 * screen_rect.w)
        # Destrói a textura temporária temp_texture, já que não é mais necessária
        sdl2.SDL_DestroyTexture(temp_texture)
        
        # Cria uma surface(imagem em memória) a partir do buffer buf
        surface = sdl2.SDL_CreateRGBSurfaceWithFormatFrom(buf, screen_rect.w, screen_rect.h, 32, PICO_BYTES_PER_PIXEL_RGBA32 * screen_rect.w, sdl2.SDL_PIXELFORMAT_RGBA32)
        if not surface:
            self._restore_render_state(clip, current_target)
            return None
        
        # Salva PNG
        result = sdlimage.IMG_SavePNG(surface, path.encode('utf-8') if isinstance(path, str) else path)
        sdl2.SDL_FreeSurface(surface) # Libera a surface da memória
        self._restore_render_state(clip, current_target) # Restaura o estado do renderer
        
        return path if result == 0 else None

    def pico_set_font(self, file, h):
        """Define a fonte"""
        if h == 0:
            h = max(8, self.S.dim_world[1] // 10)
        self.S.font_h = h
        
        if self.S.font_ttf is not None:
            sdlttf.TTF_CloseFont(self.S.font_ttf)
            self.S.font_ttf = None
        
        if file is None:
            # Carregar fonte embutida
            rw = sdl2.SDL_RWFromConstMem(pico_tiny_ttf, pico_tiny_ttf_len)
            self.S.font_ttf = sdlttf.TTF_OpenFontRW(rw, 1, self.S.font_h)
        else:
            self.S.font_ttf = sdlttf.TTF_OpenFont(file.encode('utf-8'), self.S.font_h)
        
        self.pico_assert(self.S.font_ttf is not None)

    def pico_set_grid(self, on):
        """Define se a grade deve ser exibida"""
        self.S.grid = on
        self._pico_output_present(0)

    def pico_output_draw_pixel(self, pos):
        """Desenha um pixel na posição especificada"""
        if not self.REN:
            return    
        x = self._X(pos[0], 1)
        y = self._Y(pos[1], 1)

        sdl2.SDL_RenderDrawPoint(self.REN, x, y)
        self._pico_output_present(0)

    def pico_output_draw_pixels(self, apos):
        """Desenha múltiplos pixels"""
        if not self.REN:
            return
        for pos in apos:
            x = self._X(pos[0], 1)
            y = self._Y(pos[1], 1)
            sdl2.SDL_RenderDrawPoint(self.REN, x, y)
        self._pico_output_present(0)

    def pico_output_draw_line(self, p1, p2):
        """
        Desenha uma linha entre dois pontos(p1 e p2).
        """
        if not self.REN:
            return

        # salva estado atual para restauração posterior
        clip = self._get_current_clip()
        target = self._get_current_target()

        # bounding box da linha
        min_x = min(p1[0], p2[0])
        max_x = max(p1[0], p2[0])
        min_y = min(p1[1], p2[1])
        max_y = max(p1[1], p2[1])
        w = max_x - min_x + 1
        h = max_y - min_y + 1
        
        # calcula a posição ancorada
        pos = (self._hanchor(min_x, 1), self._vanchor(min_y, 1))

        aux = self._setup_aux_texture(w, h)
        
        # O desenho dentro da aux é relativo à 'pos' para compensar a anchor
        sdl2.SDL_RenderDrawLine(self.REN, p1[0] - pos[0], p1[1] - pos[1], p2[0] - pos[0], p2[1] - pos[1])
        
        self._restore_render_state(clip, target)

        current_anchor = self.S.anchor_pos
        self.S.anchor_pos = (PICO_LEFT, PICO_TOP) # reset da anchor para TOP-LEFT
        self._pico_output_draw_tex(pos, aux, PICO_DIM_KEEP) # também aplica a anchor e o scroll, por isso vale o reset da anchor
        # para evitar confusão, resetamos a anchor original
        
        self.S.anchor_pos = current_anchor # restaura a anchor original
        sdl2.SDL_DestroyTexture(aux) # destroi a textura auxiliar

    def pico_output_draw_rect(self, rect):
        """Desenha um retângulo.

        Args:
            rect: (x, y, w, h) representando o retângulo.
        """
        if not self.REN:
            return

        pos = (rect[0], rect[1])
        clip = self._get_current_clip()
        target = self._get_current_target() # Salva o target atual também

        aux = self._setup_aux_texture(rect[2], rect[3]) # w, h
        
        # Redefine rect para ser relativo à textura auxiliar (0, 0)
        draw_rect = sdl2.SDL_Rect(0, 0, rect[2], rect[3])
        
        # A cor já é definida em _setup_aux_texture, então não precisamos setar aqui novamente.
        # Apenas certifica que o estilo de desenho está correto no target auxiliar.
        if self.S.style == PICO_FILL:
            sdl2.SDL_RenderFillRect(self.REN, draw_rect)
        elif self.S.style == PICO_STROKE:
            sdl2.SDL_RenderDrawRect(self.REN, draw_rect)
        
        self._restore_render_state(clip, target) # Restaura o target e o clip originais
        self._pico_output_draw_tex(pos, aux, PICO_DIM_KEEP)
        sdl2.SDL_DestroyTexture(aux)

    def pico_output_draw_tri(self, rect):
        """Desenha um triângulo com um ângulo reto no canto inferior esquerdo.

        Args:
            rect: (x, y, w, h) representando os limites do triângulo.
        """
        if not self.REN:
            return

        pos = (rect[0], rect[1])
        clip = self._get_current_clip()
        target = self._get_current_target()

        aux = self._setup_aux_texture(rect[2], rect[3]) # w, h
        
        # Coordenadas do triângulo relativas à textura auxiliar
        # Canto superior esquerdo: (0, 0)
        # Canto inferior esquerdo: (0, rect.h - 1)
        # Canto inferior direito: (rect.w - 1, rect.h - 1)
        x1, y1 = 0, 0
        x2, y2 = 0, rect[3] - 1
        x3, y3 = rect[2] - 1, rect[3] - 1

        color = self.S.color_draw
        r, g, b, a = color[0], color[1], color[2], color[3]

        if self.S.style == PICO_FILL:
            sdlgfx.filledTrigonRGBA(self.REN, x1, y1, x2, y2, x3, y3, r, g, b, a)
        elif self.S.style == PICO_STROKE:
            sdlgfx.trigonRGBA(self.REN, x1, y1, x2, y2, x3, y3, r, g, b, a)
        
        self._restore_render_state(clip, target)
        self._pico_output_draw_tex(pos, aux, PICO_DIM_KEEP)
        sdl2.SDL_DestroyTexture(aux)

    def pico_output_draw_oval(self, rect):
        """Desenha uma elipse/oval.

        Args:
            rect: (x, y, w, h) representando os limites da elipse.
        """
        if not self.REN:
            return

        pos = (rect[0], rect[1])
        clip = self._get_current_clip()
        target = self._get_current_target()

        aux = self._setup_aux_texture(rect[2], rect[3]) # w, h
        
        # Coordenadas do centro e raios para a elipse, relativas à textura auxiliar
        center_x, center_y = rect[2] // 2, rect[3] // 2
        radius_x, radius_y = rect[2] // 2, rect[3] // 2

        color = self.S.color_draw
        r, g, b, a = color[0], color[1], color[2], color[3]

        if self.S.style == PICO_FILL:
            sdlgfx.filledEllipseRGBA(self.REN, center_x, center_y, radius_x, radius_y, r, g, b, a)
        elif self.S.style == PICO_STROKE:
            sdlgfx.ellipseRGBA(self.REN, center_x, center_y, radius_x, radius_y, r, g, b, a)
        
        self._restore_render_state(clip, target)
        self._pico_output_draw_tex(pos, aux, PICO_DIM_KEEP)
        sdl2.SDL_DestroyTexture(aux)

    def pico_output_draw_buffer(self,pos, buffer, dim):
        """Desenha um buffer RGBA fornecido pelo usuário.

        Args:
            pos: (x, y) coordenada do canto superior esquerdo onde o buffer será desenhado.
            buffer: Lista de tuplas RGBA (r, g, b, a) ou similar, representando os pixels.
                    O buffer deve ser plano (linear), e não uma lista de listas.
                    Ex: [(255,0,0,255), (0,255,0,255), ...]
            dim: (w, h) dimensões do buffer.
        """
        if not self.REN:
            return

        # Garante que o buffer seja um bytearray para SDL_CreateRGBSurfaceWithFormatFrom
        flat_buffer = bytearray()
        for color in buffer:
            flat_buffer.extend(color)

        # Cria um array ctypes a partir do bytearray (compartilha o mesmo buffer de memória)
        # Isso permite obter um ponteiro válido para passar ao SDL
        buf_array = (ctypes.c_uint8 * len(flat_buffer)).from_buffer(flat_buffer)
        pixels_ptr = ctypes.cast(buf_array, ctypes.c_void_p)

        # Cria uma SDL_Surface a partir do buffer
        surface = sdl2.SDL_CreateRGBSurfaceWithFormatFrom(
            pixels_ptr,
            dim[0], dim[1],  # w, h
            32,              # depth
            4 * dim[0],      # largura em bytes da linha
            sdl2.SDL_PIXELFORMAT_RGBA32
        )
        if not surface:
            print(f"Erro ao criar SDL_Surface: {sdl2.SDL_GetError().decode('utf-8')}")
            return
        # Cria uma SDL_Texture a partir da superfície
        texture = sdl2.SDL_CreateTextureFromSurface(self.REN, surface)
        if not texture:
            print(f"Erro ao criar SDL_Texture: {sdl2.SDL_GetError().decode('utf-8')}")
            sdl2.SDL_FreeSurface(surface)
            return
        sdl2.SDL_FreeSurface(surface)

        # Ajusta o anchor para TOP-LEFT
        current_anchor = self.S.anchor_pos
        self.S.anchor_pos = (PICO_LEFT, PICO_TOP)
        self._pico_output_draw_tex(pos, texture, dim)
        # Restaura o anchor original
        self.S.anchor_pos = current_anchor
        # Libera a textura
        sdl2.SDL_DestroyTexture(texture)

    def pico_output_draw_poly(self, apos, count):
        """Desenha um polígono.

        Args:
            apos: Lista de tuplas (x, y) representando os vértices do polígono.
            count: Número de vértices.
        """
        if not self.REN or count == 0:
            return
        
        # Calcular bounding box
        xs = [p[0] for p in apos]
        ys = [p[1] for p in apos]
        min_x, maxx = min(xs), max(xs)
        min_y, maxy = min(ys), max(ys)

        # Ajustar coordenadas para serem relativas ao canto superior esquerdo da bounding box
        ax = [p[0] - min_x for p in apos]
        ay = [p[1] - min_y for p in apos]

        # Convert to ctypes arrays for sdl2.gfx
        ax_c = (ctypes.c_short * count)(*ax)
        ay_c = (ctypes.c_short * count)(*ay)

        # Calcular a posição (x,y) da textura auxiliar com anchor aplicado
        pos = (self._hanchor(min_x, 1), self._vanchor(min_y, 1))

        # Salvar estado atual do renderizador
        clip = self._get_current_clip()
        target = self._get_current_target()

        # Criar textura auxiliar
        aux_w = maxx - min_x + 1
        aux_h = maxy - min_y + 1
        aux = self._setup_aux_texture(aux_w, aux_h)

        # Desenhar polígono na textura auxiliar
        color = self.S.color_draw
        r, g, b, a = color[0], color[1], color[2], color[3]

        if self.S.style == PICO_FILL:
            sdlgfx.filledPolygonRGBA(self.REN, ax_c, ay_c, count, r, g, b, a)
        elif self.S.style == PICO_STROKE:
            sdlgfx.polygonRGBA(self.REN, ax_c, ay_c, count, r, g, b, a)
        
        # Restaurar estado original do renderizador
        self._restore_render_state(clip, target)

        # Aplicar transformações e desenhar textura auxiliar na TEX principal
        current_anchor = self.S.anchor_pos
        self.S.anchor_pos = (PICO_LEFT, PICO_TOP) # Temporariamente para _pico_output_draw_tex
        self._pico_output_draw_tex(pos, aux, PICO_DIM_KEEP)
        self.S.anchor_pos = current_anchor # Restaura anchor original
        
        # Destruir textura auxiliar
        sdl2.SDL_DestroyTexture(aux)

    def pico_output_draw_image(self, pos, path):
        """Desenha uma imagem.

        Args:
            pos: (x, y) coordenada do canto superior esquerdo onde a imagem será desenhada.
            path: Caminho para o arquivo da imagem.
        """
        self._pico_output_draw_image_internal(pos, path, PICO_DIM_KEEP)


    def _pico_output_draw_image_internal(self, pos, path, dim):
        """Função auxiliar interna para desenhar uma imagem com dimensões personalizadas."""
        if not self.REN:
            return

        # Gerenciamento de cache da imagem
        texture = self._pico_hash.get(path) # type: ignore
        if texture is None:
            texture = sdlimage.IMG_LoadTexture(self.REN, path.encode('utf-8'))
            self.pico_assert(texture is not None)
            self._pico_hash[path] = texture # type: ignore

        self._pico_output_draw_tex(pos, texture, dim)
        self._pico_output_present(0)

    def pico_set_style(self, style):
        """
        Define o estilo de desenho(Preenchido ou Contorno).
        Ex: pico_set_style(PICO_STYLE.FILL)
        """
        self.S.style = style
    #################################################################