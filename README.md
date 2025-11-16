# Klipper Configuration for Ender 3 S1 Plus

Configuração personalizada do Klipper para a impressora 3D **Creality Ender 3 S1 Plus**.

## 📋 Sobre

Este repositório contém arquivos de configuração otimizados para rodar Klipper na Ender 3 S1 Plus, incluindo:

- Configuração principal (`printer.cfg`)
- Macros personalizadas
- Configurações de nivelamento de mesa
- Perfis de impressão otimizados

## 🖨️ Especificações da Impressora

- **Modelo:** Creality Ender 3 S1 Plus
- **Volume de impressão:** 300 x 300 x 300mm
- **Placa-mãe:** [Especifique sua placa - ex: Creality v2.4.S1]
- **Extrusora:** Direct Drive Sprite
- **Nivelamento:** CR-Touch (BLTouch compatível)
- **Display:** Touch screen

## 🚀 Instalação

### Pré-requisitos

- Raspberry Pi (recomendado: Pi 3B+ ou superior) ou BTT Pi
- Klipper instalado ([guia oficial](https://www.klipper3d.org/Installation.html))
- Moonraker e Mainsail/Fluidd (interface web)

### Passos

1. **Clone este repositório:**
   ```bash
   cd ~
   git clone https://github.com/otenmas/Klipper-configuration-for-the-Ender-3-S1-Plus.git
   ```

2. **Backup da configuração atual:**
   ```bash
   cp ~/printer_data/config/printer.cfg ~/printer_data/config/printer.cfg.backup
   ```

3. **Copie os arquivos de configuração:**
   ```bash
   cp ~/Klipper-configuration-for-the-Ender-3-S1-Plus/printer.cfg ~/printer_data/config/
   cp ~/Klipper-configuration-for-the-Ender-3-S1-Plus/macros.cfg ~/printer_data/config/
   ```

4. **Edite o `printer.cfg` com suas configurações:**
   - Ajuste o `serial` da sua placa
   - Verifique os pinos (podem variar dependendo da versão da placa)
   - Configure os offsets do probe

5. **Reinicie o Klipper:**
   ```bash
   sudo systemctl restart klipper
   ```

## ⚙️ Configuração Inicial

### 1. PID Tuning

**Hotend:**
```gcode
PID_CALIBRATE HEATER=extruder TARGET=210
SAVE_CONFIG
```

**Mesa aquecida:**
```gcode
PID_CALIBRATE HEATER=heater_bed TARGET=60
SAVE_CONFIG
```

### 2. Nivelamento da Mesa

```gcode
G28                      # Home all axes
PROBE_CALIBRATE         # Calibrar Z-offset do probe
BED_MESH_CALIBRATE      # Criar mesh da mesa
SAVE_CONFIG
```

### 3. Calibração de E-steps

```gcode
# Marque 120mm do filamento
# Extrudar 100mm
M83
G1 E100 F100

# Meça quanto sobrou
# Calcule: novo_e_steps = atual_e_steps * (100 / filamento_extrudado)
# Ajuste no printer.cfg em [extruder] -> rotation_distance
```

## 📁 Estrutura de Arquivos

```
.
├── README.md              # Este arquivo
├── printer.cfg            # Configuração principal
├── macros.cfg             # Macros personalizadas
├── adxl.cfg              # Configuração do acelerômetro (opcional)
├── timelapse.cfg         # Configuração de timelapse (opcional)
└── mesh/                 # Meshes salvos da mesa
```

## 🎯 Macros Incluídas

- `START_PRINT` - Rotina de início de impressão
- `END_PRINT` - Rotina de finalização
- `PAUSE` / `RESUME` / `CANCEL_PRINT` - Controles de impressão
- `LOAD_FILAMENT` / `UNLOAD_FILAMENT` - Troca de filamento
- `BED_MESH_CALIBRATE` - Nivelamento automático

## 🔧 Customizações

### Velocidades recomendadas:
- Impressão: 60-80mm/s
- Travel: 150mm/s
- Primeira camada: 30mm/s

### Acelerações:
- Impressão: 1500-2000mm/s²
- Travel: 3000mm/s²

## 📝 Changelog

### [Em desenvolvimento]
- [ ] Adicionar configuração inicial
- [ ] Testar macros de início/fim
- [ ] Calibrar Input Shaping
- [ ] Otimizar Pressure Advance

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## ⚠️ Aviso

**Use estas configurações por sua conta e risco!** Sempre:
- Faça backup das configurações originais
- Teste movimentos manualmente antes de imprimir
- Monitore a primeira impressão
- Ajuste conforme necessário para seu hardware

## 📚 Recursos Úteis

- [Documentação oficial do Klipper](https://www.klipper3d.org/)
- [Klipper GitHub](https://github.com/Klipper3d/klipper)
- [Reddit r/klippers](https://www.reddit.com/r/klippers/)
- [Discord Klipper](https://discord.klipper3d.org/)

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✉️ Contato

Samuel Neto - [@otenmas](https://github.com/otenmas)

Link do projeto: [https://github.com/otenmas/Klipper-configuration-for-the-Ender-3-S1-Plus](https://github.com/otenmas/Klipper-configuration-for-the-Ender-3-S1-Plus)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!
