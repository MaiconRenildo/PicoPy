import sys
import sdl2  # type: ignore
import sdl2.sdlttf as sdlttf  # type: ignore
import sdl2.sdlmixer as sdlmixer  # type: ignore
import sdl2.sdlimage as sdlimage  # type: ignore
from sdl2 import SDL_GetError # type: ignore
import sdl2.sdlgfx as sdlgfx

from constants import (
    PICO_TITLE,
    PICO_DIM_WINDOW,
    PICO_DIM_WORLD,
    PICO_LEFT,
    PICO_CENTER,
    PICO_TOP,
    PICO_MIDDLE,
    PICO_FILL,
    PICO_STROKE,
    PICO_CLIP_RESET,
    PICO_BYTES_PER_PIXEL_RGBA32,
    PICO_DIM_KEEP,
    PICO_COLOR_GRAY,
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
        self.anchor_pos = (PICO_CENTER, PICO_MIDDLE) # Por padrão, centraliza o objeto
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

####################### PRIVATE FUNCTIONS #######################
def _noclip():
    """Verifica se não há clip ativo"""
    return (S.clip[2] == PICO_CLIP_RESET[2]) or (S.clip[3] == PICO_CLIP_RESET[3])

def _get_current_clip():
    """Obtém a região de clipping atual do renderizador e retorna um objeto SDL_Rect"""
    clip = sdl2.SDL_Rect()
    sdl2.SDL_RenderGetClipRect(REN, clip)
    return clip

def _define_clip(clip):
    """Define a região de clipping do renderizador"""
    sdl2.SDL_RenderSetClipRect(REN, clip)

def _get_current_target():
    """Obtém o target de renderização atual do renderizador(None=janela(BackBuffer))"""
    return sdl2.SDL_GetRenderTarget(REN)

def _define_target(target, w, h):
    """Define o target de renderização e o tamanho lógico"""
    # Parece ser o padrão do pico-sdl, mas não é claro o motivo.
    if target is None:
        sdl2.SDL_SetRenderTarget(REN, target)
        sdl2.SDL_RenderSetLogicalSize(REN, w, h)
    else:
        sdl2.SDL_RenderSetLogicalSize(REN, w, h)
        sdl2.SDL_SetRenderTarget(REN, target)

def _clear_target_with_defined_color():
    """Limpa o target atual com a cor definida previamente"""
    sdl2.SDL_RenderClear(REN)

def _change_target_to_window():
    """Direciona o desenho para a janela(BackBuffer)
    
    Obs: Ao mudar target, o SDL reseta automaticamente o clip para o tamanho total
    do novo target.
    """
    _define_target(None, S.dim_window[0], S.dim_window[1]) # None = direciona para a janela física do sistema

def _change_target_to_TEX():
    """Direciona o desenho de volta para a TEX"""
    zoom_dim = _zoom()
    _define_target(TEX, zoom_dim[0], zoom_dim[1])

def _restore_render_state(clip, target):
    """Restaura o estado do renderer"""
    if target is None:
        _change_target_to_window()
    else:
        # Se for uma textura, usamos o tamanho do zoom
        zoom_dim = _zoom()
        _define_target(target, zoom_dim[0], zoom_dim[1])
    _define_clip(clip)

def _pico_set_color(color):
    """Define a cor de desenho do renderizador"""
    sdl2.SDL_SetRenderDrawColor(REN, color[0], color[1], color[2], color[3])

def _restore_draw_color():
    """Restaura a cor de desenho original (S.color_draw)"""
    _pico_set_color(S.color_draw)

def _create_texture(w, h):
    """Cria uma nova textura"""
    return sdl2.SDL_CreateTexture(
        REN,
        sdl2.SDL_PIXELFORMAT_RGBA32,
        sdl2.SDL_TEXTUREACCESS_TARGET,
        w, h
    )

def _setup_aux_texture(w, h):
    """
    Cria uma textura auxiliar para desenho intermediário. Equivalente ao _draw_aux(w, h) no pico-sdl
    """
    aux = _create_texture(w, h)
    sdl2.SDL_SetTextureBlendMode(aux, sdl2.SDL_BLENDMODE_BLEND)
    sdl2.SDL_SetRenderTarget(REN, aux)
    # Limpa com transparente
    sdl2.SDL_SetRenderDrawColor(REN, 0, 0, 0, 0)
    sdl2.SDL_RenderClear(REN)
    # Restaura a cor de desenho para o aux
    _restore_draw_color()
    return aux

def _pico_output_draw_tex(pos, tex, dim):
    """Desenha uma textura com todas as transformações(crop, scale, rotation, etc)"""
    import ctypes
    
    # Obtém as dimensões originais da textura
    # tw e th armazenarão a largura e altura reais da textura carregada
    tw, th = ctypes.c_int(), ctypes.c_int()
    sdl2.SDL_QueryTexture(tex, None, None, tw, th)
    tw, th = tw.value, th.value

    # Recorte da imagem de origem
    # S.crop define qual pedaço da textura original queremos desenhar (x, y, w, h)
    cx, cy, cw, ch = S.crop
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
    rw = (S.scale[0] * rw) // 100
    rh = (S.scale[1] * rh) // 100

    # Calcula a posição final(rx, ry) onde o objeto será desenhado
    # _X e _Y já embutem o cálculo do Anchor e do Scroll
    rx = _X(pos[0], rw)
    ry = _Y(pos[1], rh)
    # dst_rect é o retângulo de destino na tela(onde e em qual tamanho desenhar)
    dst_rect = sdl2.SDL_Rect(int(rx), int(ry), int(rw), int(rh))

    # Define o ponto exato(em relação ao objeto) sobre o qual ele irá girar.
    # por padrão, se for (50, 50), ele girará em torno do seu próprio centro geométrico
    rot_center = sdl2.SDL_Point(
        int((S.anchor_rotate[0] * rw) // 100),
        int((S.anchor_rotate[1] * rh) // 100)
    )

    # Espelhamento
    # Configura se a imagem deve ser espelhada horizontalmente ou verticalmente
    flip = sdl2.SDL_FLIP_NONE
    angle_offset = 0
    if S.flip[0] and S.flip[1]: # Flip em ambos os eixos é simulado rotacionando
        # a imagem em 180 graus e aplicando um flip vertical
        angle_offset = 180
        flip = sdl2.SDL_FLIP_VERTICAL
    elif S.flip[1]: # Apenas flip vertical
        flip = sdl2.SDL_FLIP_VERTICAL
    elif S.flip[0]: # Apenas flip horizontal
        flip = sdl2.SDL_FLIP_HORIZONTAL

    # Renderização final
    # Copia a textura para o renderizador aplicando todas as transformações:
    # ângulo atual + offset de flip, centro de rotação e modo de espelhamento.
    sdl2.SDL_RenderCopyEx(
        REN, tex,
        src_rect, dst_rect,
        float(S.angle + angle_offset),
        rot_center,
        flip
    )
    _pico_output_present(0)

def _copy_TEX_to_window():
    """Copia a textura principal do mundo(TEX) para a janela(BackBuffer)"""
    sdl2.SDL_RenderCopy(REN, TEX, None, None)

def _show_on_screen():
    """Troca o conteúdo do FrontBuffer pelo BackBuffer, exibindo o que foi preparado"""
    sdl2.SDL_RenderPresent(REN)

def _zoom():
    """Calcula dimensões com zoom aplicado"""
    return (
        S.dim_world[0] * S.zoom[0] // 100,
        S.dim_world[1] * S.zoom[1] // 100
    )

def _show_grid():
    """Mostra a grade se estiver habilitada"""
    if not S.grid:
        return
    
    _pico_set_color(PICO_COLOR_GRAY)
    
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
    
    _restore_draw_color()

def _pico_output_present(force):
    """Apresenta o conteúdo renderizado da textura TEX para a tela"""
    if S.expert and not force:
        return
    
    # Salva
    clip = _get_current_clip()

    # Apresenta
    _change_target_to_window()
    _pico_set_color(PICO_COLOR_GRAY)
    _clear_target_with_defined_color()
    _copy_TEX_to_window() # Seta o conteúdo no BackBuffer da janela
    _show_grid() # Desenha a grade POR CIMA(no BackBuffer da janela)
    _show_on_screen()
    
    # Restaura
    _restore_draw_color()
    _change_target_to_TEX()
    _define_clip(clip)

def _calculate_primitive_dimensions(points):
    """
    Calcula as dimensões (largura, altura) e a posição ancorada (pos)
    para um conjunto de pontos que definem uma primitiva.

    Args:
        points: Uma lista de tuplas (x, y) representando os pontos da primitiva.

    Returns:
        Um dicionário contendo:
        'pos': A posição (x, y) ancorada da bounding box.
        'width': A largura da bounding box.
        'height': A altura da bounding box.
        'min_x': A coordenada X mínima da bounding box.
        'min_y': A coordenada Y mínima da bounding box.
        'max_x': A coordenada X máxima da bounding box.
        'max_y': A coordenada Y máxima da bounding box.
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    # Calcula a posição ancorada (canto superior esquerdo) da bounding box
    pos = (_hanchor(min_x, 1), _vanchor(min_y, 1))
    return {
        'pos': pos,
        'width': width,
        'height': height,
        'min_x': min_x,
        'min_y': min_y,
        'max_x': max_x,
        'max_y': max_y
    }

def __start_primitive_render_context(rect: tuple) -> tuple:
    """
    Prepara o contexto para desenhar uma primitiva.

    Salva o estado atual do renderizador (clip e target) e cria uma textura auxiliar
    com as dimensões fornecidas.

    Args:
        rect: Uma tupla (x, y, w, h) que define a posição e as dimensões da primitiva.

    Returns:
        Uma tupla (pos, clip, target, aux) contendo:
        - pos: A posição (x, y) da primitiva, ajustada pelo anchor.
        - clip: O SDL_Rect de clipping atual do renderizador.
        - target: O SDL_Texture target atual do renderizador.
        - aux: A textura auxiliar SDL_Texture recém-criada.
    """
    pos = (_hanchor(rect[0], rect[2]), _vanchor(rect[1], rect[3]))
    clip = _get_current_clip()
    target = _get_current_target()
    aux = _setup_aux_texture(rect[2], rect[3]) # w, h
    return pos, clip, target, aux

def __finish_primitive_render_context(clip, target, pos, aux):
    """
    Finaliza a renderização de uma primitiva.

    Restaura o estado do renderizador(clip e target), desenha o conteúdo da textura
    auxiliar na textura principal(TEX) e destrói a textura auxiliar.

    Args:
        clip: O SDL_Rect de clipping original a ser restaurado.
        target: O SDL_Texture target original a ser restaurado.
        pos: A posição (x, y) da primitiva, ajustada pelo anchor.
        aux: A textura auxiliar SDL_Texture a ser desenhada e destruída.
    """
    _restore_render_state(clip, target)
    # Salva e redefine o anchor para garantir que _pico_output_draw_tex posicione corretamente
    current_anchor = S.anchor_pos
    S.anchor_pos = (PICO_LEFT, PICO_TOP) # Temporariamente para _pico_output_draw_tex
    _pico_output_draw_tex(pos, aux, PICO_DIM_KEEP)
    S.anchor_pos = current_anchor # Restaura o anchor original
    sdl2.SDL_DestroyTexture(aux)

def _execute_primitive_render(rect: tuple, draw_function, init_function=None, finish_function=None):
    """
    Orquestra o processo de renderização de uma primitiva gráfica.

    Esta função gerencia o ciclo de vida completo do desenho de uma primitiva,
    incluindo a configuração do contexto, a execução do desenho específico e a
    finalização, com tratamento adequado do estado do renderizador e das texturas.

    Args:
        rect: Uma tupla (x, y, w, h) que define a posição e as dimensões da primitiva.
        draw_function: Uma função de callback que realiza o desenho específico
                       da primitiva na textura auxiliar. Ela deve receber um `rect`
                       com as dimensões da textura auxiliar.
        init_function: (Opcional) Função para inicializar o contexto de desenho.
                       Usa _start_primitive_render_context por padrão.
        finish_function: (Opcional) Função para finalizar o contexto de desenho.
                         Usa _finish_primitive_render_context por padrão.
    """
    if not REN:
        return
    init_function = init_function or __start_primitive_render_context
    finish_function = finish_function or __finish_primitive_render_context
    pos, clip, target, aux = init_function(rect)
    draw_function(rect)
    finish_function(clip, target, pos, aux)

def _start_point_primitive_render_context(points: list[tuple]) -> tuple:
    """
    Prepara o contexto para desenhar uma primitiva baseada em pontos.

    Calcula as dimensões da bounding box, salva o estado atual do renderizador
    e cria uma textura auxiliar com as dimensões calculadas.

    Args:
        points: Uma lista de tuplas (x, y) representando os pontos da primitiva.

    Returns:
        Uma tupla (clip, target, primitive_dimensions, aux) contendo:
        - clip: O SDL_Rect de clipping atual do renderizador.
        - target: O SDL_Texture target atual do renderizador.
        - primitive_dimensions: Um dicionário com as dimensões e posição da primitiva.
        - aux: A textura auxiliar SDL_Texture recém-criada.
    """
    clip = _get_current_clip()
    target = _get_current_target()
    primitive_dimensions = _calculate_primitive_dimensions(points)
    aux = _setup_aux_texture(primitive_dimensions['width'], primitive_dimensions['height'])
    return clip, target, primitive_dimensions, aux

def _finish_point_primitive_render_context(clip, target, primitive_dimensions, aux):
    """
    Finaliza a renderização de uma primitiva baseada em pontos.

    Restaura o estado do renderizador, desenha o conteúdo da textura
    auxiliar na textura principal (TEX) e destrói a textura auxiliar.

    Args:
        clip: O SDL_Rect de clipping original a ser restaurado.
        target: O SDL_Texture target original a ser restaurado.
        primitive_dimensions: Um dicionário com as dimensões e posição da primitiva.
        aux: A textura auxiliar SDL_Texture a ser desenhada e destruída.
    """
    _restore_render_state(clip, target)
    # Aplicar transformações e desenhar textura auxiliar na TEX principal
    current_anchor = S.anchor_pos
    S.anchor_pos = (PICO_LEFT, PICO_TOP) # Temporariamente para _pico_output_draw_tex
    _pico_output_draw_tex(primitive_dimensions['pos'], aux, PICO_DIM_KEEP)
    S.anchor_pos = current_anchor # Restaura anchor original
    sdl2.SDL_DestroyTexture(aux)

def _execute_point_primitive_render(points: list[tuple], draw_function, count=None):
    """
    Orquestra o processo de renderização de uma primitiva gráfica baseada em pontos.

    Esta função gerencia o ciclo de vida completo do desenho de uma primitiva,
    incluindo a configuração do contexto, a execução do desenho específico e a
    finalização, com tratamento adequado do estado do renderizador e das texturas.

    Args:
        points: Uma lista de tuplas (x, y) representando os pontos da primitiva.
        draw_function: Uma função de callback que realiza o desenho específico da primitiva
                       na textura auxiliar. Ela deve receber `primitive_dimensions` e `count` (se aplicável).
        count: (Opcional) O número de vértices, necessário para polígonos ctypes.
    """
    if not REN or not points or (count is not None and count == 0):
        return
    clip, target, primitive_dimensions, aux = _start_point_primitive_render_context(points)
    draw_function(primitive_dimensions, count)
    _finish_point_primitive_render_context(clip, target, primitive_dimensions, aux)

# Funções auxiliares para cálculo de posição
def _hanchor(x, w):
    """Calcula posição horizontal com anchor aplicado"""
    return x - (S.anchor_pos[0] * w) // 100

def _vanchor(y, h):
    """Calcula posição vertical com anchor aplicado"""
    return y - (S.anchor_pos[1] * h) // 100

def _X(v, w):
    """Calcula coordenada X final (com anchor e scroll)"""
    return _hanchor(v, w) - S.scroll[0]

def _Y(v, h):
    """Calcula coordenada Y final (com anchor e scroll)"""
    return _vanchor(v, h) - S.scroll[1]
#################################################################

######################### API FUNCTIONS #########################
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

def pico_assert(condition):
    """Assert com mensagem de erro SDL"""
    if not condition:
        error = SDL_GetError()
        if error:
            print(f"SDL ERROR: {error.decode('utf-8')}", file=sys.stderr)
        assert False, "SDL ERROR"

def pico_output_clear():
    """Limpa o target atual com a cor de limpeza"""
    if REN:
        _pico_set_color(S.color_clear)
        if _noclip():
            _clear_target_with_defined_color() # Limpa o target inteiro
        else:
            clip = _get_current_clip()
            sdl2.SDL_RenderFillRect(REN, clip) # Preenche a região do clip com a cor de limpeza
        _restore_draw_color()
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
    TEX = _create_texture(new[0], new[1])
    pico_assert(TEX is not None)
    
    _define_target(TEX, new[0], new[1])
    
    # Define clip
    clip = sdl2.SDL_Rect(0, 0, new[0], new[1])
    _define_clip(clip)

def pico_output_screenshot(path=None):
    """Tira um screenshot da tela"""
    zoom_dim = _zoom()
    rect = sdl2.SDL_Rect(0, 0, zoom_dim[0], zoom_dim[1])
    return pico_output_screenshot_ext(path, rect)

def pico_output_screenshot_ext(path, rect):
    """Tira um screenshot de uma região específica da tela"""
    import ctypes
    from datetime import datetime
    
    if path is None:
        path = f"pico-sdl-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
    
    if not REN or not TEX:
        return None
    
    clip = _get_current_clip()
    current_target = _get_current_target()
    
    # Cria textura temporária com o mesmo tamanho da janela
    # Parâmetros: renderer, formato(RGBA 32 bits), acesso(target=permite renderizar nela), largura, altura
    temp_texture = _create_texture(S.dim_window[0], S.dim_window[1])
    if not temp_texture:
        _restore_render_state(clip, current_target)
        return None

    # A partir daqui, o conteúdo da textura TEX é renderizado para a textura temporária temp_texture
    # Assim como as operações de zoom, scroll, leitura de pixels, etc. são aplicadas na textura temporária temp_text
    _define_target(temp_texture, S.dim_window[0], S.dim_window[1])
    _pico_set_color(PICO_COLOR_GRAY)
    _clear_target_with_defined_color()
    _copy_TEX_to_window()
    _show_grid() # Desenha a grade na textura temporária, pois a grade não é desenhada na TEXT

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

def pico_output_draw_pixel(pos):
    """Desenha um pixel na posição especificada"""
    if not REN:
        return    
    x = _X(pos[0], 1)
    y = _Y(pos[1], 1)

    sdl2.SDL_RenderDrawPoint(REN, x, y)
    _pico_output_present(0)

def pico_output_draw_pixels(vertices):
    """Desenha múltiplos pixels"""
    if not REN:
        return
    for pos in vertices:
        x = _X(pos[0], 1)
        y = _Y(pos[1], 1)
        sdl2.SDL_RenderDrawPoint(REN, x, y)
    _pico_output_present(0)

def pico_output_draw_line(p1, p2):
    """
    Desenha uma linha entre dois pontos(p1 e p2).
    """
    def _draw_line_function(primitive_dimensions, _): # O '_' é para o parâmetro count não utilizado
        # As coordenadas são ajustadas para serem relativas à textura auxiliar (0,0)
        x1, y1 = int(p1[0] - primitive_dimensions['min_x']), int(p1[1] - primitive_dimensions['min_y'])
        x2, y2 = int(p2[0] - primitive_dimensions['min_x']), int(p2[1] - primitive_dimensions['min_y'])
        sdl2.SDL_RenderDrawLine(REN, x1, y1, x2, y2)
    _execute_point_primitive_render([p1, p2], _draw_line_function)



def pico_output_draw_rect(rect):
    """
    Desenha um retângulo.

    Args:
        rect: Uma tupla (x, y, w, h) representando o retângulo.
    """
    def _draw_function(rect: tuple):
        # Redefine rect para ser relativo à textura auxiliar (0, 0)
        draw_rect = sdl2.SDL_Rect(0, 0, rect[2], rect[3])
        
        # A cor já é definida em _setup_aux_texture, então não precisamos setar aqui novamente.
        # Apenas certifica que o estilo de desenho está correto no target auxiliar.
        if S.style == PICO_FILL:
            sdl2.SDL_RenderFillRect(REN, draw_rect)
        elif S.style == PICO_STROKE:
            sdl2.SDL_RenderDrawRect(REN, draw_rect)
    _execute_primitive_render(
        rect=rect,
        draw_function=_draw_function,
    )

def pico_output_draw_tri(rect):
    """
    Desenha um triângulo com um ângulo reto no canto inferior esquerdo.
    
    Args:
        rect: Uma tupla (x, y, w, h) representando os limites do triângulo.
    """
    def _draw_function(rect: tuple):
        # draw
        # Coordenadas do triângulo relativas à textura auxiliar
        # Canto superior esquerdo: (0, 0)
        # Canto inferior esquerdo: (0, rect.h - 1)
        # Canto inferior direito: (rect.w - 1, rect.h - 1)
        x1, y1 = 0, 0
        x2, y2 = 0, rect[3] - 1
        x3, y3 = rect[2] - 1, rect[3] - 1

        color = S.color_draw
        r, g, b, a = color[0], color[1], color[2], color[3]

        if S.style == PICO_FILL:
            sdlgfx.filledTrigonRGBA(REN, x1, y1, x2, y2, x3, y3, r, g, b, a)
        elif S.style == PICO_STROKE:
            sdlgfx.trigonRGBA(REN, x1, y1, x2, y2, x3, y3, r, g, b, a)
    _execute_primitive_render(
        rect=rect,
        draw_function=_draw_function,
    )

def pico_output_draw_oval(rect):
    """
    Desenha uma elipse/oval.
    
    Args:
        rect: Uma tupla (x, y, w, h) representando os limites da elipse.
    """
    def _draw_function(rect: tuple):
        # Coordenadas do centro e raios para a elipse, relativas à textura auxiliar
        center_x, center_y = rect[2] // 2, rect[3] // 2
        radius_x, radius_y = rect[2] // 2, rect[3] // 2

        color = S.color_draw
        r, g, b, a = color[0], color[1], color[2], color[3]

        if S.style == PICO_FILL:
            sdlgfx.filledEllipseRGBA(REN, center_x, center_y, radius_x, radius_y, r, g, b, a)
        elif S.style == PICO_STROKE:
            sdlgfx.ellipseRGBA(REN, center_x, center_y, radius_x, radius_y, r, g, b, a)
    _execute_primitive_render(
        rect=rect,
        draw_function=_draw_function,
    )


def pico_output_draw_poly(vertices, count):
    """
    Desenha um polígono.

    Args:
        vertices: Uma lista de tuplas (x, y) representando os vértices do polígono.
        count: O número de vértices no polígono.
    """
    import ctypes # Este import precisa permanecer aqui se for usado apenas nesta função

    def _draw_poly_function(primitive_dimensions, actual_count):
        color = S.color_draw
        r, g, b, a = color[0], color[1], color[2], color[3]

        # Ajustar coordenadas para serem relativas ao canto superior esquerdo da bounding box
        ax = [p[0] - primitive_dimensions["min_x"] for p in vertices]
        ay = [p[1] - primitive_dimensions["min_y"] for p in vertices]

        # Converter para arrays ctypes para sdl2.gfx
        ax_c = (ctypes.c_short * actual_count)(*ax)
        ay_c = (ctypes.c_short * actual_count)(*ay)

        if S.style == PICO_FILL:
            sdlgfx.filledPolygonRGBA(REN, ax_c, ay_c, actual_count, r, g, b, a)
        elif S.style == PICO_STROKE:
            sdlgfx.polygonRGBA(REN, ax_c, ay_c, actual_count, r, g, b, a)
    _execute_point_primitive_render(vertices, _draw_poly_function, count)

def pico_set_style(style):
    """
    Define o estilo de desenho(Preenchido ou Contorno).
    Ex: pico_set_style(PICO_STYLE.FILL)
    """
    S.style = style
#################################################################