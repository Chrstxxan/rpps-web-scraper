# Coleta Autônoma de Atas de RPPS

## Descrição Geral
Este projeto implementa uma rotina automatizada em **Python 3** para descoberta, download e organização de **atas de reuniões** de **Comitê de Investimentos e Conselhos** em sites heterogêneos de RPPS, sem depender de caminhos fixos.
O sistema realiza descoberta (utilizando Selenium + BeautifulSoup), download robusto (com requests), extração de texto (PDF, DOC, DOCX, HTML) e gera metadados em JSONL e TXT.

---

## Objetivo
- Descoberta automática de páginas de atas em 5 RPPS diferentes.

- Download dos documentos e registro do link de origem.

- Armazenamento organizado por RPPS e UF.

- Geração de arquivo de metadados com:

  - Nome da entidade e UF.
  
  - Tipo de reunião (Comitê / Conselho / Desconhecido).
  
  - Data da reunião (quando identificável).
  
  - URL de origem, nome e formato do arquivo.

- Diferencial: extração do texto integral das atas em .txt.

---

## Estrutura do Projeto
A solução foi estruturada em módulos independentes dentro da pasta `core/`:

```text
.
├── app.py
├── core/
│   ├── __init__.py       # Torna o diretório um pacote Python importável
│   ├── discovery.py      # Busca links de atas
│   ├── downloader.py     # Faz o download e salva os arquivos
│   ├── extractor.py      # Extrai texto, tipo e data das reuniões
│   ├── metadata.py       # Gera e salva os metadados
│   └── utils.py          # Funções auxiliares
├── requirements.txt
└── README.md
```

---

## Estrutura de Diretórios
Após a execução, a estrutura resultante segue o padrão:

```text
data/
├── atas_geral.jsonl
├── atas_geral.txt
├── PR/
│   ├── FPMU_Umuarama/
│   │   ├── relatorios/
│   │   │   ├── atas.jsonl
│   │   │   └── atas_resumo.txt
│   │   └── arquivos extraídos (.pdf, .doc, .docx, .html, .txt)
│   └── ToledoPrev/
│       ├── relatorios/
│       │   ├── atas.jsonl
│       │   └── atas_resumo.txt
│       └── arquivos extraídos (.pdf, .doc, .docx, .html, .txt)
├── RJ/
│   └── FUPREVAS_Vassouras/
│       └── relatorios/
│           ├── atas.jsonl
│           └── atas_resumo.txt
└── SP/
    ├── IPMO_Osasco/
    │   ├── relatorios/
    │   │   ├── atas.jsonl
    │   │   └── atas_resumo.txt
    │   └── arquivos extraídos (.pdf, .doc, .docx, .html, .txt)
    ├── IPSMI_Itaquaquecetuba/
    │   ├── relatorios/
    │   │   ├── atas.jsonl
    │   │   └── atas_resumo.txt
    │   └── arquivos extraídos (.pdf, .doc, .docx, .html, .txt)
    └── FPGPREV_Praia_Grande/
        └── relatorios/
            ├── atas.jsonl
            └── atas_resumo.txt
```

---

## Instalação
Crie um ambiente virtual (opcional) e instale as dependências:

```pip install -r requirements.txt```

É necessário ter o Google Chrome instalado.
O Selenium Manager gerencia o driver automaticamente, não precisando de nenhum download manual.

## Execução
A partir da raiz do projeto, rode:

```python app.py --out ./data```

O parâmetro ```--out``` define o diretório base de saída (padrão: ```./data```).

**O projeto já acompanha uma amostra real de coletas executadas, disponível na pasta data/. Caso deseje refazer a coleta, basta excluir a pasta e executar novamente o comando acima.**

---

## Como funciona:

1. Descoberta (```core/discovery.py```)
Usa Selenium em modo headless e BeautifulSoup para encontrar links que contenham palavras-chave relevantes (“ata”, “reunião”, “comitê”, “conselho”, “transparência”, “publicações”, etc.).
Ignora links de “política de investimentos” e normaliza URLs relativas.

2. Download (```core/downloader.py```)
Varre cada página identificada, encontra links diretos para arquivos (PDF, DOC, DOCX, HTML) e faz download com:

- Headers aleatórios simulando diferentes navegadores;

- Requisições robustas (retries e timeouts);

- Deduplicação por hash SHA1 do conteúdo;

- Registro da página e link de origem.

3. Extração (```core/extractor.py```)
Lê e extrai texto de:

- PDF (pdfplumber);

- DOC e DOCX (mammoth, python-docx);

- HTML (BeautifulSoup).
Detecta:

- Tipo da reunião (Comitê, Conselho, Desconhecido);

- Data da reunião (regex para DD/MM/AAAA ou “D de mês de AAAA”);

- E salva cada texto extraído em ```.txt.```

4. Metadados (```core/metadata.py```)
Gera dois relatórios:

```atas.jsonl``` (estrutura para análise programática);

```atas_resumo.txt``` (resumo legível para leitura manual).

além de dois arquivos que são gerais para todas as atas extraídas (para facilitar leitura geral): 

```atas_geral.jsonl``` (estrutura para análise programática contendo o conteúdo unificado de todos os ```atas.jsonl```)

```atas_geral.txt``` (resumo legível contendo o conteúdo unificado de todos os ```atas_resumo.txt```)

---

## Boas Práticas Aplicadas

- Descoberta generalista, sem caminhos fixos.

- Tolerância a erros e tempo de resposta com retry e timeout.

- Deduplicação por conteúdo (hash SHA1).

- Armazenamento rastreável por UF e nome da entidade.

- Código modular e comentado em português.

- Extração completa de texto como diferencial.

---

## Limitações / Reflexões de possíveis melhorias

- A detecção de datas é baseada em regex e pode falhar com formatos não padronizados.

- A classificação de tipo depende de palavras-chave — atas com títulos atípicos podem ser marcadas como “Desconhecido”.

### Situações Encontradas Durante os Testes 

- FUPREVAS (Vassouras/RJ) e FPGPREV (Praia Grande/SP) não apresentaram atas disponíveis em suas páginas oficiais, nem nas seções de transparência ou publicações.
A ausência foi confirmada manualmente durante a validação. O sistema identificou corretamente que não havia arquivos válidos para coleta e prosseguiu sem erros, evidenciando que o comportamento da rotina é resiliente e estável mesmo quando o site não contém atas.

- Foi incluído FPMU Umuarama (PR) como RPPS extra opcional, com o objetivo de demonstrar a capacidade de generalização e robustez do algoritmo em outro domínio real.
Esse site, baseado em ASP.NET, reforça a adaptabilidade da solução, já que utiliza carregamento dinâmico — cenário comum em portais públicos.

---

## Melhorias Futuras (Reflexões a respeito do sistema)

- Filtro semântico (NLP) para eliminar documentos que não sejam atas.

- Extração automática de pautas, decisões e nomes de participantes.

- Execução paralela para acelerar a coleta.

- Interface web para visualizar os resultados e monitorar novas coletas.

---

## Observação:
**O projeto foi desenvolvido e testado em ambiente Windows 11 com Python 3.14 e Google Chrome 141.0.7390.108**

---
# Autor

Christian Delucca