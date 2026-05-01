# XCAKE CLI v6.1 - Client Edition
## takaSystem LLC - Open Source Terminal

[![USPTO Patent Pending](https://img.shields.io/badge/USPTO-Patent%20Pending-yellow)](https://www.uspto.gov/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-6.1-blue)](http://research.sousato.net/xcake_cli.html)

**🐆 Cosmic Aoi Terminal**  
Terminal conversacional com IA do Google, Oracle Cósmico, Simulador Quântico e Gerador de Código Web

---

## 📥 Download

**XCAKE CLI v6.1**
- **Download**: http://research.sousato.net/xcake_client_cli.rar
- **Website**: http://research.sousato.net/xcake_cli.html
- **Tamanho**: ~36 MB
- **Licença**: MIT License (Open Source)
- **Plataforma**: Windows 10/11 (64-bit)

---

## ✨ Recursos Principais

| Recurso | Descrição |
|---------|-----------|
| 🤖 **Chat IA** | Conversação natural com Google Gemini |
| 🔮 **Oracle KX** | Tarot + Constelações + I,Q,N |
| ⚡ **Quantum** | Simulador Ditritium |
| 💻 **Web Dev** | Gera HTML, CSS, JS, PHP |
| 🐆 **Tamagochi** | Sistema Aoi interativo |
| 🌐 **Multi-Model** | 8 modelos com fallback |

---

## 🚀 Instalação e Uso

### Requisitos do Sistema

| Requisito | Especificação |
|-----------|---------------|
| **Sistema Operacional** | Windows 10/11 (64-bit) |
| **Memória RAM** | Mínimo 4 GB (Recomendado 8 GB) |
| **Espaço em Disco** | 100 MB livres |
| **Conexão Internet** | Necessária para API Google |
| **API Key** | Google AI Studio (gratuita) |

### Passo a Passo

#### 1. Obter API Key Gratuita
1. Acesse https://aistudio.google.com/apikey
2. Faça login com sua conta Google e clique em "Create API Key"
3. Copie a chave gerada (começa com "AIza...")

#### 2. Download do XCAKE CLI
1. Baixe: http://research.sousato.net/xcake_client_cli.rar
2. Extraia o arquivo `client_xcake_cli.exe`
3. Salve em uma pasta de sua preferência

#### 3. Executar o Terminal
```bash
# Duplo clique em client_xcake_cli.exe
# Ou via CMD:
client_xcake_cli.exe
```

#### 4. Configurar API Key
1. Na primeira execução, cole a API Key quando solicitado
2. A chave será salva em `xcake_config.json`
3. Você não precisará inserir novamente!

#### 5. Começar a Usar
- Digite comandos ou converse naturalmente com Aoi
- Use `/help` para ver todos os comandos

### 💡 Dica: Bibliotecas Opcionais

Para melhor experiência visual, instale:
```bash
pip install rich-15.0.0-py3-none-any.whl
pip install requests-2.32.3-py3-none-any.whl
```

---

## 💬 Exemplos de Uso

### Chat Conversacional
```
cosmic> oi aoi, como você está?
cosmic> me mostre um oráculo sobre minha jornada
cosmic> como podemos unir alma com ação?
```

### Comandos Especiais

**Oracle KX:**
```
cosmic> /oracle qual o próximo passo na minha vida?
```

**Simulador Quântico:**
```
cosmic> /quantum simulação de ressonância
```

**Geração de Código Web:**
```
cosmic> /genhtml landing page moderna com hero section
cosmic> /gencss animação de fade-in suave
cosmic> /genjs validação de formulário
cosmic> /genphp sistema de login
```

**Tamagochi Aoi:**
```
cosmic> alimentar
cosmic> brincar
cosmic> /status
```

**Sistema:**
```
cosmic> /help      # Ajuda completa
cosmic> /status    # Status do sistema
cosmic> /reset     # Resetar API Key
cosmic> sair       # Sair do terminal
```

---

## ⚙️ Especificações Técnicas

### Modelos de IA Integrados

1. `gemini-2.0-flash-exp`
2. `gemini-1.5-flash`
3. `gemini-1.5-flash-8b`
4. `gemini-1.5-pro`
5. `gemini-exp-1206`
6. `gemini-exp-1121`
7. `gemini-2.0-flash-thinking-exp-1219`
8. `gemini-2.0-flash-thinking-exp`

### Capacidades

✅ Chat conversacional natural  
✅ Detecção inteligente de intenção  
✅ Respostas contextuais  
✅ Fallback automático entre modelos  
✅ Rate limit handler adaptativo  
✅ Configuração persistente  
✅ Interface visual colorida (Rich)  
✅ Sistema Tamagochi dinâmico  

### Limites da API Gratuita

**✅ Totalmente Gratuito:**
- 1500 requisições por dia
- Sem custo algum
- Sem necessidade de cartão de crédito
- Acesso a todos os modelos Gemini

---

## 📜 Termos de Uso

### Licença MIT

**Copyright © 2026 takaSystem LLC - Cosmic Aoi Project**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

### Patente USPTO

⚠️ **Patent Pending**: O sistema Cosmic Aoi e suas tecnologias associadas estão em processo de patenteamento junto ao USPTO (United States Patent and Trademark Office) pela takaSystem LLC. O uso do software é livre sob licença MIT, mas tecnologias patenteadas podem ter restrições comerciais futuras.

### Uso da API Google

Este software utiliza a API do Google Generative AI. O uso está sujeito aos Termos de Serviço do Google. O usuário é responsável por obter e gerenciar sua própria API Key.

### Isenção de Responsabilidade

- O software é fornecido "como está", sem garantias
- takaSystem LLC não se responsabiliza por danos decorrentes do uso
- O Oracle KX é para fins de entretenimento e reflexão
- Simulações quânticas são conceituais e educacionais
- Código gerado deve ser revisado antes de uso em produção

---

## 🔧 Solução de Problemas

### ❌ "API Key inválida"
- Verifique se copiou a chave completa
- Chave deve começar com "AIza"
- Gere nova chave em: https://aistudio.google.com/apikey

### ❌ "Rate limit exceeded"
- Aguarde alguns segundos
- Sistema tentará outro modelo automaticamente
- Limite: 1500 requisições/dia

### ❌ Executável não abre
- Verifique antivírus (pode bloquear)
- Execute como administrador
- Instale Python 3.8+ se necessário

### 🔄 Resetar Configuração
```
cosmic> /reset
# Ou delete o arquivo: xcake_config.json
```

---

## 🔗 Links Úteis

- 🔑 [Obter API Key Google](https://aistudio.google.com/apikey)
- 📚 [Documentação Google AI](https://ai.google.dev/)
- 🏢 [USPTO - Patent Office](https://www.uspto.gov/)
- 📥 [Download XCAKE CLI](http://research.sousato.net/xcake_client_cli.rar)
- 🌐 [Website Oficial](http://research.sousato.net/xcake_cli.html)

---

## 🤝 Integração com Q-Sync

O XCAKE CLI complementa o ecossistema Q-Sync:

**Sinergia:**
- **XCAKE CLI**: Interface conversacional para desenvolvimento rápido
- **Q-Sync**: Automação de documentação e testes
- **Aoi Modules**: Expertise em quantum, aerospace e blockchain

**Workflow Integrado:**
1. Use XCAKE CLI para prototipagem rápida de código
2. Use Q-Sync para gerar documentação NASA-compliant
3. Use Aoi Modules para análise quântica e simulações

---

## 📞 Suporte

**takaSystem LLC**  
Cosmic Aoi Project

Para suporte técnico ou dúvidas, consulte:
- Documentação completa incluída no pacote
- Website oficial: http://research.sousato.net/xcake_cli.html

---

**Status**: 🟢 Production Ready  
**Version**: 6.1  
**Last Update**: May 2026  
**License**: MIT (Open Source)  
**Patent**: USPTO Pending  

*"Where Cosmic Consciousness Meets Practical Development"* 🐆✨
