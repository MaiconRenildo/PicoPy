import sys
import sdl2  # type: ignore
import sdl2.sdlttf as sdlttf  # type: ignore
import sdl2.sdlmixer as sdlmixer  # type: ignore
import sdl2.sdlimage as sdlimage  # type: ignore
from sdl2 import SDL_GetError # type: ignore

from constants import (
    PICO_TITLE,
    PICO_DIM_WINDOW,
    PICO_DIM_WORLD,
    PICO_CENTER,
    PICO_MIDDLE,
    PICO_FILL,
    PICO_CLIP_RESET,
    PICO_BYTES_PER_PIXEL_RGBA32,
)
from tiny_ttf import pico_tiny_ttf, pico_tiny_ttf_len

# Variáveis globais
WIN = None  # Janela(objeto da janela do sistema operacional)
REN = None  # Renderer(responsável por desenhar na janela)
TEX = None  # Textura(superfície de renderização alvo)
_pico_hash = None  # Tabela hash

class PicoState:
    def __init__(self):
        # Anchor(ponto de referência)
        # Define qual ponto do objeto é usado como referência para posicionamento ao dar zoom/mover
        self.anchor_pos = (PICO_CENTER, PICO_MIDDLE)
        # Define qual ponto do objeto é usado como centro de rotação ao rotacionar algo
        self.anchor_rotate = (PICO_CENTER, PICO_MIDDLE)
        
        self.angle = 0
        self.clip = (0, 0, 0, 0)  # (x, y, w, h)
        self.color_clear = (0, 0, 0, 255)  # (r, g, b, a) - preto
        self.color_draw = (255, 255, 255, 255)  # branco
        self.crop = (0, 0, 0, 0)
        self.cursor_x = 0
        self.cursor_cur = (0, 0)
        self.dim_window = PICO_DIM_WINDOW
        self.dim_world = PICO_DIM_WORLD
        self.expert = 0
        self.flip = (0, 0)
        self.font_ttf = None
        self.font_h = 0
        self.fullscreen = 0
        self.grid = 1
        self.scroll = (0, 0)
        self.style = PICO_FILL
        self.scale = (100, 100)
        self.zoom = (100, 100)

S = PicoState()

def pico_assert(condition):
    """Assert com mensagem de erro SDL"""
    if not condition:
        error = SDL_GetError()
        if error:
            print(f"SDL ERROR: {error.decode('utf-8')}", file=sys.stderr)
        assert False, "SDL ERROR"

def _noclip():
    """Verifica se não há clip ativo"""
    return (S.clip[2] == PICO_CLIP_RESET[2]) or (S.clip[3] == PICO_CLIP_RESET[3])

def _zoom():
    """Calcula dimensões com zoom aplicado"""
    return (
        S.dim_world[0] * S.zoom[0] // 100,
        S.dim_world[1] * S.zoom[1] // 100
    )

def _pico_output_present(force):
    """Apresenta o conteúdo renderizado"""
    if S.expert and not force:
        return
    
    # Salva a região de clipping atual
    clip = sdl2.SDL_Rect()
    sdl2.SDL_RenderGetClipRect(REN, clip)
    
    # Mudar target para tela
    sdl2.SDL_SetRenderTarget(REN, None)
    sdl2.SDL_RenderSetLogicalSize(REN, S.dim_window[0], S.dim_window[1])
    
    # Limpar com cor cinza
    sdl2.SDL_SetRenderDrawColor(REN, 119, 119, 119, 119)
    sdl2.SDL_RenderClear(REN)
    
    # Copiar a textura TEX para a tela
    sdl2.SDL_RenderCopy(REN, TEX, None, None)
    
    # Mostrar grid na tela somente(o target aqui já é None)
    # A grade é desenhada diretamente na tela, portanto, ao fazer screenshot, a grade não é copiada
    # automaticamentepara o arquivo da screenshot. Nesse caso é necessário forçar a apresentação da grade na tela
    # para garantir que ela seja salva no arquivo
    _show_grid()
    
    # Apresentar
    sdl2.SDL_RenderPresent(REN)
    
    # Restaurar cor de desenho
    sdl2.SDL_SetRenderDrawColor(
        REN,
        S.color_draw[0],
        S.color_draw[1],
        S.color_draw[2],
        S.color_draw[3]
    )
    
    # Restaurar target e clip
    zoom_dim = _zoom()
    sdl2.SDL_RenderSetLogicalSize(REN, zoom_dim[0], zoom_dim[1])
    sdl2.SDL_SetRenderTarget(REN, TEX)
    sdl2.SDL_RenderSetClipRect(REN, clip)

def _show_grid():
    """Mostra a grade se estiver habilitada"""
    if not S.grid:
        return
    
    sdl2.SDL_SetRenderDrawColor(REN, 119, 119, 119, 119)
    
    zoom_dim = _zoom()
    
    # Linhas verticais
    if (S.dim_window[0] % zoom_dim[0] == 0) and (zoom_dim[0] < S.dim_window[0]):
        step = S.dim_window[0] // zoom_dim[0]
        for i in range(0, S.dim_window[0] + 1, step):
            sdl2.SDL_RenderDrawLine(REN, i, 0, i, S.dim_window[1])
    
    # Linhas horizontais
    if (S.dim_window[1] % zoom_dim[1] == 0) and (zoom_dim[1] < S.dim_window[1]):
        step = S.dim_window[1] // zoom_dim[1]
        for j in range(0, S.dim_window[1] + 1, step):
            sdl2.SDL_RenderDrawLine(REN, 0, j, S.dim_window[0], j)
    
    # Restaurar cor de desenho
    sdl2.SDL_SetRenderDrawColor(
        REN,
        S.color_draw[0],
        S.color_draw[1],
        S.color_draw[2],
        S.color_draw[3]
    )

def pico_output_clear():
    """Limpa a tela com a cor de limpeza"""
    if REN:
        sdl2.SDL_SetRenderDrawColor(
            REN,
            S.color_clear[0],
            S.color_clear[1],
            S.color_clear[2],
            S.color_clear[3]
        )
        if _noclip():
            sdl2.SDL_RenderClear(REN)
        else:
            # Preencher região do clip
            clip = sdl2.SDL_Rect()
            sdl2.SDL_RenderGetClipRect(REN, clip)
            sdl2.SDL_RenderFillRect(REN, clip)
        
        # Restaurar cor de desenho
        sdl2.SDL_SetRenderDrawColor(
            REN,
            S.color_draw[0],
            S.color_draw[1],
            S.color_draw[2],
            S.color_draw[3]
        )
        
        # Apresentar
        _pico_output_present(0)

def pico_output_present():
    """Apresenta o conteúdo renderizado na tela"""
    if REN and TEX:
        _pico_output_present(1)

def pico_set_zoom(pct):
    """Define o zoom"""
    old = _zoom()
    S.zoom = pct
    new = _zoom()
    
    dx = new[0] - old[0]
    dy = new[1] - old[1]
    
    # Ajusta scroll baseado no anchor
    S.scroll = (
        S.scroll[0] - (dx * S.anchor_pos[0] // 100),
        S.scroll[1] - (dy * S.anchor_pos[1] // 100)
    )
    
    global TEX
    if TEX:
        sdl2.SDL_DestroyTexture(TEX)
    
        # Criar nova textura
    TEX = sdl2.SDL_CreateTexture(
        REN,
        sdl2.SDL_PIXELFORMAT_RGBA32,
        sdl2.SDL_TEXTUREACCESS_TARGET,
        new[0],
        new[1]
    )
    pico_assert(TEX is not None)
    
    sdl2.SDL_RenderSetLogicalSize(REN, new[0], new[1])
    sdl2.SDL_SetRenderTarget(REN, TEX)
    
    # Define clip
    clip = sdl2.SDL_Rect(0, 0, new[0], new[1])
    sdl2.SDL_RenderSetClipRect(REN, clip)

def pico_output_screenshot(path=None):
    """Tira um screenshot da tela"""
    zoom_dim = _zoom()
    rect = sdl2.SDL_Rect(0, 0, zoom_dim[0], zoom_dim[1])
    return pico_output_screenshot_ext(path, rect)

def _render_to_target(target, width, height):
    """Renderiza conteúdo (textura + grade) em um target"""

    # Definição da cor de fundo do target
    sdl2.SDL_SetRenderTarget(REN, target)  # Define onde o renderer vai desenhar(None=tela, ou textura)
    sdl2.SDL_RenderSetLogicalSize(REN, width, height)  # Define o tamanho lógico da área de renderização
    sdl2.SDL_SetRenderDrawColor(REN, 119, 119, 119, 119)  # Define a cor de desenho(cinza)
    sdl2.SDL_RenderClear(REN)  # Limpa o target com a cor definida
    # Sobreposição da textura TEX no target
    sdl2.SDL_RenderCopy(REN, TEX, None, None)  # Copia a textura TEX para o target atual
    _show_grid() # Desenha a grade por cima da textura TEX se estiver habilitada

def _restore_render_state(clip, target):
    """Restaura o estado do renderer"""
    zoom_dim = _zoom()
    sdl2.SDL_RenderSetLogicalSize(REN, zoom_dim[0], zoom_dim[1])
    sdl2.SDL_SetRenderTarget(REN, target)
    sdl2.SDL_RenderSetClipRect(REN, clip)

def pico_output_screenshot_ext(path, rect):
    """Tira um screenshot de uma região específica da tela"""
    import ctypes
    from datetime import datetime
    
    if path is None:
        path = f"pico-sdl-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
    
    if not REN or not TEX:
        return None
    
    # Salvar estado atual do renderer para restaurar depois
    clip = sdl2.SDL_Rect()  # Retângulo para armazenar a região de clipping atual
    sdl2.SDL_RenderGetClipRect(REN, clip)  # Obtém a região de clipping atual e salva em clip
    current_target = sdl2.SDL_GetRenderTarget(REN)  # Obtém o target atual(None=tela, ou textura)
    
    # Cria textura temporária com o mesmo tamanho da janela
    # Parâmetros: renderer, formato(RGBA 32 bits), acesso(target=permite renderizar nela), largura, altura
    temp_texture = sdl2.SDL_CreateTexture(REN, sdl2.SDL_PIXELFORMAT_RGBA32, sdl2.SDL_TEXTUREACCESS_TARGET, S.dim_window[0], S.dim_window[1])  
    if not temp_texture:
        _restore_render_state(clip, current_target)
        return None
    
    # Renderiza o conteúdo da textura TEX para a textura temporária temp_texture
    # A partir daqui, o conteúdo da textura TEX é renderizado para a textura temporária temp_texture
    # Assim como as operações de zoom, scroll, leitura de pixels, etc. são aplicadas na textura temporária temp_text
    _render_to_target(temp_texture, S.dim_window[0], S.dim_window[1])
    
    # Lê pixels da textura temporária
    screen_rect = sdl2.SDL_Rect(0, 0, S.dim_window[0], S.dim_window[1])  # Retângulo: x=0, y=0, largura=janela[0], altura=janela[1]
    buf = (ctypes.c_uint8 * (PICO_BYTES_PER_PIXEL_RGBA32 * screen_rect.w * screen_rect.h))() # Calcula o tamanho do buffer em bytes
    # Lê do temp_texture a região definida em screen_rect e salva no buffer buf
    sdl2.SDL_RenderReadPixels(REN, screen_rect, sdl2.SDL_PIXELFORMAT_RGBA32, buf, PICO_BYTES_PER_PIXEL_RGBA32 * screen_rect.w)
    # Destrói a textura temporária temp_texture, já que não é mais necessária
    sdl2.SDL_DestroyTexture(temp_texture)
    
    # Cria uma surface(imagem em memória) a partir do buffer buf
    surface = sdl2.SDL_CreateRGBSurfaceWithFormatFrom(buf, screen_rect.w, screen_rect.h, 32, PICO_BYTES_PER_PIXEL_RGBA32 * screen_rect.w, sdl2.SDL_PIXELFORMAT_RGBA32)
    if not surface:
        _restore_render_state(clip, current_target)
        return None
    
    # Salva PNG
    result = sdlimage.IMG_SavePNG(surface, path.encode('utf-8') if isinstance(path, str) else path)
    sdl2.SDL_FreeSurface(surface) # Libera a surface da memória
    _restore_render_state(clip, current_target) # Restaura o estado do renderer
    
    return path if result == 0 else None

def pico_set_font(file, h):
    """Define a fonte"""
    if h == 0:
        h = max(8, S.dim_world[1] // 10)
    S.font_h = h
    
    if S.font_ttf is not None:
        sdlttf.TTF_CloseFont(S.font_ttf)
        S.font_ttf = None
    
    if file is None:
        # Carregar fonte embutida
        rw = sdl2.SDL_RWFromConstMem(pico_tiny_ttf, pico_tiny_ttf_len)
        S.font_ttf = sdlttf.TTF_OpenFontRW(rw, 1, S.font_h)
    else:
        S.font_ttf = sdlttf.TTF_OpenFont(file.encode('utf-8'), S.font_h)
    
    pico_assert(S.font_ttf is not None)

def pico_set_grid(on):
    """Define se a grade deve ser exibida"""
    S.grid = on
    _pico_output_present(0)

def pico_init(on):
    """
    Inicializa ou termina o pico-sdl
    
    Args:
        on: 1 para inicializar, 0 para terminar
    """
    global WIN, REN, TEX, _pico_hash
    
    if on:
        # Criar hash
        _pico_hash = {}
        
        # Inicializar SDL
        pico_assert(sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) == 0)
        
        # Criar janela
        WIN = sdl2.SDL_CreateWindow(
            PICO_TITLE.encode('utf-8'),
            sdl2.SDL_WINDOWPOS_UNDEFINED, # Posição X da janela -> sistema que define
            sdl2.SDL_WINDOWPOS_UNDEFINED, # Posição Y da janela -> sistema que define
            S.dim_window[0], # Largura da janela
            S.dim_window[1], # Altura da janela
            sdl2.SDL_WINDOW_SHOWN # Janela visível ao ser criada
        )
        pico_assert(WIN is not None)
        
        # Criar renderer
        REN = sdl2.SDL_CreateRenderer(
            WIN,
            -1, # Índice do driver de renderização -> -1 para usar o primeiro driver disponível
            sdl2.SDL_RENDERER_ACCELERATED # Usar aceleração de hardware(GPU) quando disponível
        )
        pico_assert(REN is not None)
        
        # Configurar blend mode
        sdl2.SDL_SetRenderDrawBlendMode(REN, sdl2.SDL_BLENDMODE_BLEND) # Define o modo de blend(transparência)
        
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
        pico_set_zoom(S.zoom) # Aqui a textura TEX é definida como target
        
        # Carregar fonte embutida(tiny_ttf)
        pico_set_font(None, 0)

        # Limpar tela
        pico_output_clear()
        
        # Limpar eventos
        sdl2.SDL_PumpEvents()
        sdl2.SDL_FlushEvents(sdl2.SDL_FIRSTEVENT, sdl2.SDL_LASTEVENT)
        
        # Tornar janela redimensionável
        sdl2.SDL_SetWindowResizable(WIN, 1)
        
    else:
        if S.font_ttf is not None:
            sdlttf.TTF_CloseFont(S.font_ttf)
            S.font_ttf = None
        
        sdlmixer.Mix_CloseAudio()
        sdlttf.TTF_Quit()
        
        # Destruir textura antes do renderer
        if TEX:
            sdl2.SDL_DestroyTexture(TEX)
            TEX = None
        
        if REN:
            sdl2.SDL_DestroyRenderer(REN)
            REN = None
        
        if WIN:
            sdl2.SDL_DestroyWindow(WIN)
            WIN = None
        
        sdl2.SDL_Quit()
        
        # Limpar hash
        _pico_hash = None