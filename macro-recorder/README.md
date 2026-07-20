# Macro Recorder - TinyTask para macOS

Um gravador de macros simples e funcional para macOS, similar ao TinyTask. Permite gravar ações de mouse e teclado e reproduzi-las automaticamente.

## Funcionalidades

- ✅ Gravar cliques de mouse
- ✅ Gravar movimento do mouse
- ✅ Gravar scroll do mouse
- ✅ Gravar teclas do teclado
- ✅ Reproduzir macros com velocidade ajustável
- ✅ Reproduzir em loop
- ✅ Salvar e carregar macros em arquivos JSON
- ✅ Interface gráfica intuitiva

## Requisitos

- macOS 10.13 ou superior
- Python 3.7 ou superior
- Permissões de Accessibility e Input Monitoring

## Instalação

1. Certifique-se de ter o Python instalado:
```bash
python3 --version
```

2. Navegue até a pasta do projeto:
```bash
cd macro-recorder
```

3. Instale as dependências:
```bash
pip3 install -r requirements.txt
```

## Configuração de Permissões

Para que o gravador funcione corretamente, você precisa conceder permissões no macOS:

1. Abra **Preferências do Sistema** > **Segurança e Privacidade** > **Privacidade**
2. Na guia **Acessibilidade**, clique no cadeado e adicione:
   - Python (ou Terminal, dependendo de como você executa)
3. Na guia **Monitoramento de Entrada**, clique no cadeado e adicione:
   - Python (ou Terminal)
4. Reinicie o aplicativo após conceder as permissões

## Como Usar

### Interface Gráfica

Execute o aplicativo com interface gráfica:

```bash
python3 gui.py
```

### Controles

1. **Gravar**: Clique para começar a gravar suas ações
2. **Parar Gravação**: Clique novamente para parar a gravação
3. **Reproduzir**: Reproduz a macro gravada
4. **Parar**: Para a reprodução a qualquer momento

### Configurações

- **Velocidade**: Ajuste a velocidade de reprodução (0.1x a 3.0x)
- **Loop**: Marque para reproduzir a macro em loop infinito

### Arquivos

- **Salvar Macro**: Salva a macro atual em um arquivo JSON
- **Carregar Macro**: Carrega uma macro salva de um arquivo JSON

### Atalhos

- **F9**: Para a gravação durante o processo

## Exemplo de Uso

1. Execute `python3 gui.py`
2. Clique em "Gravar"
3. Execute as ações que deseja automatizar (cliques, digitação, etc.)
4. Clique em "Parar Gravação" ou pressione F9
5. Ajuste a velocidade se necessário
6. Clique em "Reproduzir" para executar a macro
7. Opcional: Salve a macro para uso futuro

## Solução de Problemas

### "Permissão negada" ou eventos não são gravados

- Verifique se você concedeu as permissões de Accessibility e Input Monitoring
- Reinicie o aplicativo após conceder as permissões
- Verifique se Python/Terminal está na lista de aplicativos permitidos

### A reprodução não funciona corretamente

- Ajuste a velocidade para um valor mais baixo (0.5x ou 0.8x)
- Verifique se os aplicativos estão nas mesmas posições durante gravação e reprodução
- Algumas teclas especiais podem não funcionar em todos os aplicativos

### Interface não abre

- Verifique se tkinter está instalado: `python3 -m tkinter`
- Se não estiver, instale: `brew install python-tk` (via Homebrew)

## Arquivos do Projeto

- `macro_recorder.py` - Núcleo do gravador de macros
- `gui.py` - Interface gráfica do usuário
- `requirements.txt` - Dependências do Python
- `README.md` - Este arquivo

## Notas

- Este projeto foi desenvolvido como alternativa ao TinyTask para macOS
- A gravação de movimento do mouse pode gerar muitos eventos
- Para tarefas simples, considere desativar o movimento do mouse se não for necessário
- Sempre salve suas macros importantes antes de fechar o aplicativo

## Licença

Este projeto é open source e pode ser usado livremente.