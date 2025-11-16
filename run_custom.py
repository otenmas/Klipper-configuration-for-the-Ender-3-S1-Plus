#!/usr/bin/env python3
"""
run_custom.py

Pequeno utilitário para renderizar templates Jinja2 de macros (gcode) localmente.

Uso:
  python run_custom.py            # usa template de exemplo embutido
  python run_custom.py --file macro.ini

O script tenta extrair o bloco `gcode:` (linhas indentadas após a linha `gcode:`)
se presente; caso contrário renderiza o arquivo inteiro como template.

É destinado a validação sintática e renderização Jinja2 — não executa nenhum comando
no hardware. Forneça os parâmetros necessários na variável `SAMPLE_PARAMS` ou via JSON
no futuro.
"""
import argparse
import json
import sys
import traceback
from jinja2 import Environment, StrictUndefined, TemplateSyntaxError, UndefinedError

DEFAULT_TEMPLATE = '''M117 Executando homing
{% for i in range(3) %}
G1 X{{ 10 * i }} Y{{ 5 * i }} F600
{% endfor %}
; exemplo: linha final
'''

SAMPLE_PARAMS = {
    "X": 5,
    "Y": 10,
    "LEN": 100,
    "LINE_HEIGHT": 0.2,
    "WIDTH": 0.45,
    "BED_TEMP": 60,
    "EXTRUDER_TEMP": 200,
    "FILAMENT": "PLA",
    "REPS": 3,
    "z_safety": 0.1,
    "z_offset": 0.0,
    "NOZZLE": 0.4,
    "FEED": 1000,
}


def extract_all_macros(text: str) -> list:
    """Procura por todos os blocos [gcode_macro ...] e extrai o bloco gcode: de cada um.
    Retorna uma lista de tuplas (macro_name, gcode_content)."""
    lines = text.splitlines()
    macros = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        # Procura por linha que comece com [gcode_macro
        if ln.strip().lower().startswith("[gcode_macro"):
            # Extrai nome da macro
            macro_name = ln.strip()[len("[gcode_macro"):].strip().rstrip("]").strip()
            i += 1
            # Procura pelo bloco gcode: dentro desta macro
            gcode_start = None
            while i < len(lines):
                if lines[i].strip().lower().startswith("gcode:"):
                    gcode_start = i
                    break
                if lines[i].strip().startswith("["):
                    # Próxima seção encontrada, sair
                    break
                i += 1
            
            if gcode_start is not None:
                # Extrai linhas indentadas após gcode:
                collected = []
                for ln2 in lines[gcode_start+1:]:
                    if ln2.strip() == "":
                        collected.append("")
                        continue
                    if ln2.startswith(" ") or ln2.startswith("\t"):
                        collected.append(ln2.lstrip())
                    else:
                        # parou o bloco indentado
                        break
                macros.append((macro_name, "\n".join(collected)))
        i += 1
    return macros


def render_template(template_text: str, params: dict) -> str:
    env = Environment(undefined=StrictUndefined)
    tpl = env.from_string(template_text)
    # disponibiliza `params` e as chaves diretamente no contexto
    ctx = {"params": params}
    ctx.update(params)
    return tpl.render(**ctx)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Renderiza um template Jinja2 de macro gcode localmente.")
    parser.add_argument("--file", "-f", help="Arquivo com macro (ou somente o bloco gcode). Se ausente, usa exemplo embutido.")
    parser.add_argument("--out", "-o", help="Arquivo para salvar o resultado renderizado (stdout se ausente)")
    parser.add_argument("--params", "-p", help="JSON com parâmetros para o template (opcional)")
    args = parser.parse_args(argv)

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                raw = fh.read()
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}", file=sys.stderr)
            sys.exit(2)
        
        # Tenta extrair todas as macros
        macros = extract_all_macros(raw)
        if not macros:
            # Se não encontrou [gcode_macro...], tenta extrair um bloco gcode: genérico
            template_text = extract_gcode_block(raw) if hasattr(sys.modules[__name__], 'extract_gcode_block') else raw
            macros = [("generic", template_text)]
    else:
        macros = [("example", DEFAULT_TEMPLATE)]

    params = SAMPLE_PARAMS.copy()
    if args.params:
        try:
            params.update(json.loads(args.params))
        except Exception as e:
            print(f"Erro ao parsear JSON de params: {e}", file=sys.stderr)
            sys.exit(2)

    output_lines = []
    
    for macro_name, template_text in macros:
        output_lines.append(f"\n{'='*70}")
        output_lines.append(f"[gcode_macro {macro_name}]")
        output_lines.append(f"{'='*70}\n")
        
        try:
            out = render_template(template_text, params)
            output_lines.append(out)
            output_lines.append("")
        except TemplateSyntaxError as e:
            output_lines.append(f"❌ TemplateSyntaxError em {macro_name}:")
            output_lines.append(traceback.format_exc())
            output_lines.append("")
        except UndefinedError as e:
            output_lines.append(f"❌ UndefinedError em {macro_name} (variável ausente):")
            output_lines.append(traceback.format_exc())
            output_lines.append("")
        except Exception:
            output_lines.append(f"❌ Erro ao renderizar {macro_name}:")
            output_lines.append(traceback.format_exc())
            output_lines.append("")

    full_output = "\n".join(output_lines)
    
    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(full_output)
            print(f"Renderizado salvo em: {args.out}")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}", file=sys.stderr)
            sys.exit(4)
    else:
        print(full_output)


if __name__ == "__main__":
    main()
