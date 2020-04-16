# Bot com informações sobre o COVID em São Carlos

## Instalação
1. Tenha o python3 instalado no seu computador (é recomendo a versão >= 3.6).
2. Instale os seguintes pacotes:
```python
# Libs necessárias para ligar o bot:
pyTelegramBotAPI
pandas

# Libs necessárias para a criação de gráficos
matplotlib
numpy
# pandas
```
3. Crie um arquivo chamado `token` e nele coloque (em uma linha) o token do seu bot.

## Ligando o bot
Rode o comando `python bot.py` ou `python3 bot.py` (depdendo de como o python está instalado no seu sistema).
Durante a execução o bot gera um arquivo `bot.log` que contém o `logging` de informações, útil para solucionar erros do bot.

## Criando os gráficos e modificando os dados
O notebook `genereatePlots.ipynb` serve para criar os gráficos e transformar ele em arquivos `.png`, ele pode ser editado para gerar novos gráficos ou alterar os já existentes.
Os dados que o bot usa para gerar as informações nos comandos e os gráficos se encontra em `dataset.csv`, você pode encontrar mais informações sobre esses dados em: https://github.com/MetlHedd/datasets/tree/master/covid19/saocarlos