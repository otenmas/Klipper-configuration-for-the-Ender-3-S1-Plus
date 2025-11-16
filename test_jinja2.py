#!/usr/bin/env python3
"""
Script para testar e debugar templates Jinja2 do Klipper
Use este script para validar suas macros antes de usar no Klipper
"""

from jinja2 import Environment, Template
import json

def test_start_print():
    """Testa a macro START_PRINT com valores de exemplo"""
    
    print("=" * 60)
    print("TESTANDO MACRO START_PRINT")
    print("=" * 60)
    
    # Template simplificado da macro START_PRINT
    template_str = """
{%- set x = params.X|default(5)|float %}
{%- set y = params.Y|default(10)|float %}
{%- set length = params.LEN|default(100)|float %}
{%- set line_height = params.LINE_HEIGHT|default(0.2)|float %}
{%- set width = params.WIDTH|default(0.45)|float %}
{%- set bed = params.BED_TEMP|default(60)|float %}
{%- set extruder = params.EXTRUDER_TEMP|default(200)|float %}
{%- set material = params.FILAMENT|default("Desconhecido") %}
{%- set rep = params.REPS|default(3)|int %}
{%- set z_safety = params.z_safety|default(0.1)|float %}
{%- set z_off = 0.0|float %}
{%- set z_height = z_off + z_safety %}
{%- set nozzle = params.NOZZLE|default(0.4)|float %}
{%- set feedrate = params.FEED|default(1000)|float %}
{%- set spacing_factor = 1.10 %}
{%- set line_spacing = width * spacing_factor %}
{%- set area_filamento = 2.405 %}
{%- set Ecalc = ((width * line_height * length) / area_filamento) %}

DEBUG: PARAMETROS
x = {{ x }}
y = {{ y }}
length = {{ length }}
line_height = {{ line_height }}
width = {{ width }}
bed = {{ bed }}
extruder = {{ extruder }}
material = {{ material }}
rep = {{ rep }}
z_safety = {{ z_safety }}
z_height = {{ z_height }}
nozzle = {{ nozzle }}
feedrate = {{ feedrate }}

DEBUG: CALCULOS
spacing_factor = {{ spacing_factor }}
line_spacing = {{ line_spacing }}
area_filamento = {{ area_filamento }}
Ecalc (extrusao) = {{ Ecalc|round(4) }}

DEBUG: LOOP DE PURGA
{% for i in range(rep) %}
  Purga {{ i+1 }}/{{ rep }}
  {% set cur_x = x + i * line_spacing %}
  cur_x = {{ cur_x|round(2) }}
{% endfor %}
"""
    
    # Parametros que seriam passados pelo slicer
    params = {
        'X': 5,
        'Y': 10,
        'LEN': 100,
        'LINE_HEIGHT': 0.2,
        'WIDTH': 0.45,
        'BED_TEMP': 60,
        'EXTRUDER_TEMP': 200,
        'FILAMENT': 'PLA',
        'REPS': 3,
        'z_safety': 0.1,
        'NOZZLE': 0.4,
        'FEED': 1000
    }
    
    try:
        env = Environment()
        template = env.from_string(template_str)
        result = template.render(params=params)
        print("\n✓ TEMPLATE RENDERIZADO COM SUCESSO!\n")
        print(result)
        return True
    except Exception as e:
        print(f"\n✗ ERRO AO RENDERIZAR TEMPLATE:\n{type(e).__name__}: {e}")
        return False


def test_end_print():
    """Testa a macro END_PRINT com valores de exemplo"""
    
    print("\n" + "=" * 60)
    print("TESTANDO MACRO END_PRINT")
    print("=" * 60)
    
    template_str = """
{%- set max_x = 235|float %}
{%- set max_y = 235|float %}
{%- set max_z = 250|float %}
{%- set z_now = 150|float %}
{%- set safe_raise = 100.0 %}
{%- set z_threshold = max_z * 0.66 %}
{%- set ultimo_material = "PLA" %}
{%- set ultimo_nozzle = 0.4 %}

DEBUG: POSICAO ATUAL
z_now = {{ z_now }}
z_threshold = {{ z_threshold|round(2) }}

DEBUG: CONDICAO
z_now > z_threshold = {{ z_now > z_threshold }}

{% if z_now > z_threshold %}
  Peca esta ALTA - elevando apenas 10mm
  {% set park_z = z_now + 10 %}
  {% if park_z > max_z %}
    park_z ultrapassaria limite, usando max_z
    {% set park_z = max_z %}
  {% endif %}
  park_z final = {{ park_z }}
  Ir para X={{ max_x/2|round(2) }} Y={{ max_y - 20|round(2) }}
{% else %}
  Peca esta BAIXA - elevando {{ safe_raise }}mm
  {% set park_z = z_now + safe_raise %}
  {% if park_z > max_z %}
    park_z ultrapassaria limite, usando max_z
    {% set park_z = max_z %}
  {% endif %}
  park_z final = {{ park_z }}
  Ir para X={{ max_x - 10 }} Y={{ max_y - 10 }}
{% endif %}

Material final = {{ ultimo_material }}
Nozzle = {{ ultimo_nozzle }}
"""
    
    try:
        env = Environment()
        template = env.from_string(template_str)
        result = template.render()
        print("\n✓ TEMPLATE RENDERIZADO COM SUCESSO!\n")
        print(result)
        return True
    except Exception as e:
        print(f"\n✗ ERRO AO RENDERIZAR TEMPLATE:\n{type(e).__name__}: {e}")
        return False


def test_custom_template(template_code):
    """Testa um template customizado"""
    
    print("\n" + "=" * 60)
    print("TESTANDO TEMPLATE CUSTOMIZADO")
    print("=" * 60)
    
    try:
        env = Environment()
        template = env.from_string(template_code)
        result = template.render(params={})
        print("\n✓ TEMPLATE RENDERIZADO COM SUCESSO!\n")
        print(result)
        return True
    except Exception as e:
        print(f"\n✗ ERRO AO RENDERIZAR TEMPLATE:\n{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "DEBUGGER JINJA2 PARA KLIPPER" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Executar testes
    resultado1 = test_start_print()
    resultado2 = test_end_print()
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"START_PRINT: {'✓ PASSOU' if resultado1 else '✗ FALHOU'}")
    print(f"END_PRINT:   {'✓ PASSOU' if resultado2 else '✗ FALHOU'}")
    
    if resultado1 and resultado2:
        print("\n✓ Todos os testes passaram!")
    else:
        print("\n✗ Alguns testes falharam. Verifique os erros acima.")
    
    print("\n" + "=" * 60)
    print("DICA: Copie seu código Jinja2 na funcao test_custom_template()")
    print("      para testar templates customizados.")
    print("=" * 60 + "\n")
