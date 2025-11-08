# Trading AI for MetaTrader 5

Sistema automatizado de trading que utiliza Inteligencia Artificial (LSTM) para tomar decisiones de trading en MetaTrader 5.

## Estructura del Proyecto

```
.
├── mql5/
│   └── MTF_MA_AI.mq5         # Expert Advisor para MetaTrader 5
├── python/
│   ├── config.py             # Configuración del modelo y parámetros
│   ├── ai_model.py           # Implementación del modelo LSTM
│   └── mt5_interface.py      # Interfaz entre MQL5 y Python
├── requirements.txt          # Dependencias de Python
└── README.md                # Este archivo
```

## Requisitos

- MetaTrader 5
- Python 3.9 o superior
- Bibliotecas de Python (ver requirements.txt)

## Instalación

1. **Configurar el entorno Python:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # En Windows
   pip install -r requirements.txt
   ```

2. **Configurar MetaTrader 5:**
   - Copiar `MTF_MA_AI.mq5` a la carpeta de Expert Advisors
   - Compilar el EA en MetaTrader 5

## Uso

1. Activar el entorno virtual:
   ```bash
   source venv/Scripts/activate  # En Windows
   ```

2. Abrir MetaTrader 5 y arrastrar el EA a un gráfico

3. El sistema:
   - Entrenará automáticamente el modelo con datos históricos
   - Analizará el mercado en tiempo real
   - Ejecutará operaciones según las predicciones de la IA

## Características

- Modelo LSTM para análisis de patrones
- Indicadores técnicos múltiples
- Gestión automática de riesgos
- Stop Loss y Take Profit configurables

## Contribuir

Siéntete libre de:
1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## Contacto

Tu Nombre - [@monkeluffy13](https://github.com/monkeluffy13)

Project Link: [https://github.com/monkeluffy13/Trd](https://github.com/monkeluffy13/Trd)