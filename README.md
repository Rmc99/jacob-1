1º Projeto do professor Jacob referente a disciplina de analise e projeto de algoritmos

Para executar o arquivo precisa instalar o pacote "request" devido o programa chamar uma API externa para gerar a imagem do grafo. Executar o comando no terminal: pip install requests

Para evitar o passo acima gerei o arquivo principal.exe através do pacote pyinstaller, dessa forma precisa apenas ter o executável e o arquivo .txt que deve ser chamado de "meu_arquivo.txt"; Ambos os arquivos devem estar dentro da pasta "dist".

Layout do arquivo "meu_arquivo.txt";
1º linha: d -> direcionado ou nd -> não direcionado
A partir da 2º linha: arestas -> 1,2; 1,3; 2,4; 3,5; 4,5

Segue como ficaria o layout de arquivo para o programa poder executar:

d<br>
1,2<br>
1,3<br>
2,4<br>
3,5<br>
4,5<br>
